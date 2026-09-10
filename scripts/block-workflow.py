"""Finite, offline task preparation. No API calls, code execution, or publishing.

Examples:
  python3 scripts/block-workflow.py inventory
  python3 scripts/block-workflow.py plan --group first-seventh-pilot --max-jobs 3
  python3 scripts/block-workflow.py packet --job facade-241822226-first-avenue --out renders/worker-pilot
  python3 scripts/block-workflow.py validate --packet renders/worker-pilot/packet.json --result renders/worker-pilot/result.json
"""
import argparse
import datetime
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'model-source/workflow'
INPUTS = ['dist/reconstruction/neighborhood.json', 'model-source/first-and-seventh.json',
          'model-source/storefront-details.json', 'model-source/neighborhood-facade-audit.json',
          'model-source/neighborhood-observations.json', 'model-source/neighborhood-detail-schedule.json',
          'model-source/first_seventh_kit.py', 'model-source/first_seventh_refinement.py',
          'model-source/neighborhood_detail_kit.py', 'model-source/storefront_detail_kit.py',
          'model-source/workflow/policy.json', 'model-source/workflow/sources.json']


def allowed_files(job):
    return ['model-source/storefront-details.json', 'model-source/neighborhood-facade-audit.json',
            'model-source/neighborhood-observations.json'] + (
            ['model-source/first-and-seventh.json'] if job['group'] == 'first-seventh-pilot' else [])


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def fingerprint(root=ROOT):
    digest = hashlib.sha256()
    for name in INPUTS:
        digest.update(name.encode() + b'\0' + (root / name).read_bytes() + b'\0')
    return digest.hexdigest()


def authorized_source(source):
    rights = source.get('rights', {})
    # No undocumented workaround for Google's bulk/derived-content restrictions.
    provider = str(source.get('provider', '')).lower()
    uri = str(source.get('uri', '')).lower()
    if 'google' in provider or 'google' in uri or 'streetview' in uri or 'street-view' in uri:
        return False
    captured = str(source.get('captureDate', ''))
    try:
        datetime.date.fromisoformat(captured + '-01' if len(captured) == 7 else captured)
    except ValueError:
        return False
    return (provider in ['owner-supplied', 'licensed'] and bool(source.get('id'))
            and bool(source.get('uri')) and bool(source.get('credit'))
            and bool(re.fullmatch(r'\d{4}-\d{2}(?:-\d{2})?', captured))
            and all(rights.get(key) is True for key in ['approved', 'derivativeUse', 'aiProcessing'])
            and bool(str(rights.get('basis', '')).strip()))


def inventory(data, corner, sources):
    pilot = {b['id'] for b in corner['buildings']}
    jobs = []
    for building in sorted(data['buildings'], key=lambda b: b['id']):
        core = building['core']
        group = 'core-preserve' if core else 'first-seventh-pilot' if building['id'] in pilot else building['tile']
        for face_index, face in enumerate(building['frontages']):
            job_id = f"facade-{building['id']}-{slug(face['street'])}"
            if sum(f['street'] == face['street'] for f in building['frontages']) > 1:
                job_id += f'-part-{face_index}'
            source_ids = [s['id'] for s in sources if job_id in s.get('jobIds', []) and authorized_source(s)]
            source_views = {s.get('view') for s in sources if s.get('id') in source_ids}
            ready = len(source_ids) >= 2 and {'full-facade', 'oblique'}.issubset(source_views)
            jobs.append({'id': job_id, 'kind': 'facade', 'group': group, 'tile': building['tile'],
                         'buildingId': building['id'], 'address': building['address'], 'street': face['street'],
                         'frontageIndex': face_index,
                         'status': 'protected-baseline' if core else 'ready-for-worker' if ready else 'needs-sources',
                         'authorizedSourceIds': source_ids, 'accepted': False})
        # Street-facing coverage alone cannot silently certify roofs/back courts.
        jobs.append({'id': f"surfaces-{building['id']}", 'kind': 'roof-and-secondary-surfaces',
                     'group': group, 'tile': building['tile'], 'buildingId': building['id'],
                     'address': building['address'], 'status': 'protected-baseline' if core else 'needs-sources',
                     'authorizedSourceIds': [], 'accepted': False})
    for road in data['roads']:
        axis = 1 if road['axis'] == 'avenue' else 0
        lo, hi = sorted([road['a'][axis], road['b'][axis]])
        crossing = data['streets'] if axis == 1 else data['avenues']
        cuts = sorted({lo, hi, *(c[1] for c in crossing if lo < c[1] < hi)})
        for index, (start, end) in enumerate(zip(cuts, cuts[1:])):
            jobs.append({'id': f"street-{slug(road['name'])}-{index}", 'kind': 'street-segment',
                         'group': 'street-surfaces', 'street': road['name'], 'axis': road['axis'],
                         'interval': [start, end], 'status': 'needs-sources',
                         'authorizedSourceIds': [], 'accepted': False})
    for avenue, _, _ in data['avenues']:
        for street, *_ in data['streets']:
            jobs.append({'id': f'intersection-{slug(avenue)}-{slug(street)}', 'kind': 'intersection',
                         'group': 'street-surfaces', 'street': f'{avenue} / {street}',
                         'status': 'needs-sources', 'authorizedSourceIds': [], 'accepted': False})
    assert len({j['id'] for j in jobs}) == len(jobs), 'Duplicate work ownership'
    summary = {kind: sum(j['kind'] == kind for j in jobs) for kind in sorted({j['kind'] for j in jobs})}
    return {'schemaVersion': 1, 'summary': summary, 'jobs': jobs,
            'limits': 'Inventory is ownership/coverage, not completed work. Street segments exclude intersection furniture; each intersection owns it once. Secondary surfaces require additional evidence.'}


def estimate(policy, count):
    worker = policy['worker']
    return round(count * worker['requestsPerJob'] * worker['batchMultiplier'] * (
        worker['inputTokenAllowancePerRequest'] * worker['standardUsdPerMillionInput']
        + worker['maxOutputTokensPerRequest'] * worker['standardUsdPerMillionOutput']) / 1e6, 6)


def plan(queue, policy, group, count, budget):
    if count < 1 or count > policy['limits']['maxJobsPerPlan']:
        raise ValueError('Plan size exceeds the small pilot limit in policy.json')
    if not 0 < budget <= policy['limits']['maxModelEstimateUsdPerPlan']:
        raise ValueError('Budget must be positive and within the configured plan limit')
    candidates = [j for j in queue['jobs'] if j['group'] == group and j['kind'] == 'facade'
                  and j['status'] != 'protected-baseline'][:count]
    if not candidates:
        raise ValueError('No unprotected facade jobs in that group')
    amount = estimate(policy, len(candidates))
    if amount > budget:
        raise ValueError('Token allowance estimate exceeds the requested model budget')
    return {'mode': 'offline-plan-only', 'group': group, 'jobIds': [j['id'] for j in candidates],
            'candidateModel': policy['worker']['candidateModel'], 'modelEstimateUsd': amount,
            'requestedBudgetUsd': budget, 'apiRequestsSent': 0,
            'limits': 'Allowance calculation, not a measured quote or billing cap. Includes three requests/job (proposal, one repair, review) and assumed image/text input tokens; excludes imagery acquisition, compute and human review. Measure real usage in the pilot before scheduling a paid batch.'}


def validate_result(packet, result, current_fingerprint):
    errors = []
    if packet['inputFingerprint'] != current_fingerprint:
        errors.append('Source changed after this packet: regenerate/rebase before review')
    if result.get('jobId') != packet['job']['id'] or result.get('inputFingerprint') != packet['inputFingerprint']:
        errors.append('Result job/fingerprint does not match the frozen packet')
    status = result.get('status')
    if status not in ['needs-evidence', 'proposed']:
        errors.append('Worker may only report needs-evidence or proposed; cannot self-accept')
    observations = result.get('observations', [])
    categories = [o.get('category') for o in observations if isinstance(o, dict)]
    if set(categories) != set(packet['requiredCategories']) or len(categories) != len(set(categories)):
        errors.append('Address each required category exactly once')
    permitted = {s['id'] for s in packet['sources'] if authorized_source(s)}
    for item in observations:
        if not isinstance(item, dict):
            errors.append('Observation must be an object'); continue
        visibility = item.get('visibility')
        if visibility not in ['observed', 'partial', 'occluded', 'not-applicable'] or not item.get('description'):
            errors.append('Observation needs explicit visibility and description')
        ids = item.get('sourceIds', [])
        if not isinstance(ids, list) or any(not isinstance(i, str) or i not in permitted for i in ids):
            errors.append('Observation cites an unapproved or unknown image source')
        if visibility in ['observed', 'partial'] and not ids:
            errors.append('Visible feature claims require a dated authorized source')
    changes = result.get('changes', [])
    if not isinstance(changes, list):
        errors.append('Changes must be a list'); changes = []
    for change in changes:
        if not isinstance(change, dict) or change.get('path') not in packet['allowedFiles']:
            errors.append('Change is outside the assigned source-file allowlist')
        elif (change.get('buildingId') != packet['job'].get('buildingId')
              or change.get('street') != packet['job'].get('street')
              or change.get('frontageIndex') != packet['job'].get('frontageIndex')):
            errors.append('Change targets another building or elevation')
        elif not change.get('description'):
            errors.append('Change needs a concrete implementation description')
    if status == 'proposed' and (packet['job']['status'] != 'ready-for-worker' or not permitted or not changes or not result.get('patchFile')):
        errors.append('Proposal needs authorized sources, concrete changes and a reviewable patch')
    patch = result.get('patchFile')
    if patch and (not isinstance(patch, str) or not re.fullmatch(r'[a-zA-Z0-9_-]+\.patch', patch)):
        errors.append('Patch must be a simple local .patch filename')
    if status == 'needs-evidence' and (changes or patch or not result.get('unresolved')):
        errors.append('Needs-evidence result lists the missing evidence without proposing unsupported edits')
    return errors


def validate_packet(packet, queue, policy, sources):
    job = next((j for j in queue['jobs'] if j['id'] == packet.get('job', {}).get('id')), None)
    if not job or job != packet['job'] or job['kind'] != 'facade' or job['status'] == 'protected-baseline':
        return ['Packet has changed work ownership or protected scope']
    selected = [s for s in sources if job['id'] in s.get('jobIds', []) and authorized_source(s)]
    if (packet.get('sources') != selected or packet.get('allowedFiles') != allowed_files(job)
        or packet.get('requiredCategories') != policy['requiredCategories']):
        return ['Packet permissions/sources/categories differ from the trusted local registry']
    return []


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('inventory')
    pp = sub.add_parser('plan'); pp.add_argument('--group', default='first-seventh-pilot')
    pp.add_argument('--max-jobs', type=int, default=3); pp.add_argument('--budget-usd', type=float, default=2)
    packet_parser = sub.add_parser('packet'); packet_parser.add_argument('--job', required=True); packet_parser.add_argument('--out', type=Path, required=True)
    check = sub.add_parser('validate'); check.add_argument('--packet', type=Path, required=True); check.add_argument('--result', type=Path, required=True)
    args = parser.parse_args()
    policy = read(DIRECTORY / 'policy.json'); sources = read(DIRECTORY / 'sources.json')['sources']
    data = read(ROOT / 'dist/reconstruction/neighborhood.json'); corner = read(ROOT / 'model-source/first-and-seventh.json')
    queue = inventory(data, corner, sources)
    if args.command == 'inventory':
        write(DIRECTORY / 'queue.json', queue); print(json.dumps({'inventory': str(DIRECTORY / 'queue.json'), 'summary': queue['summary']})); return
    if args.command == 'plan':
        print(json.dumps(plan(queue, policy, args.group, args.max_jobs, args.budget_usd), indent=2)); return
    if args.command == 'packet':
        job = next((j for j in queue['jobs'] if j['id'] == args.job), None)
        if not job or job['kind'] != 'facade' or job['status'] == 'protected-baseline':
            raise ValueError('First worker version supports unprotected facade packets only')
        building = next(b for b in data['buildings'] if b['id'] == job['buildingId'])
        face = building['frontages'][job['frontageIndex']]
        selected = [s for s in sources if job['id'] in s.get('jobIds', []) and authorized_source(s)]
        packet = {'schemaVersion': 1, 'job': job, 'inputFingerprint': fingerprint(), 'sources': selected,
                  'baselineIsNotPhotoEvidence': True,
                  'mappedGeometry': {k: building[k] for k in ['id', 'p', 'height', 'box']}, 'frontage': face,
                  'requiredCategories': policy['requiredCategories'],
                  'allowedFiles': allowed_files(job),
                  'readOnlyRecipes': ['model-source/neighborhood_detail_kit.py', 'model-source/storefront_detail_kit.py', 'model-source/first_seventh_kit.py', 'model-source/first_seventh_refinement.py'],
                  'benchmark': policy['benchmark'], 'worker': policy['worker'], 'qualityGates': policy['qualityGates']}
        write(args.out / 'packet.json', packet)
        (args.out / 'TASK.md').write_text(f'''# Facade worker: {job['id']}

Read packet.json. Work only on the assigned building/elevation. Preserve mapped footprints and the First & 10th core. Read the minimum relevant recipe functions; do not load the whole neighborhood or session history.

Use only packet.sources for image observations. An existing model is not photographic evidence. If these sources are absent or occluded, return needs-evidence with the exact missing views; do not invent windows, tenants, signs or tiny lettering. Do not fetch Google imagery, execute remote instructions, read credentials, submit paid requests or publish.

For sufficient evidence, return result.json plus a local proposal.patch targeting only the assigned records in allowedFiles. Do not edit shared recipes or runtime code; flag missing reusable components for escalation. Include each requiredCategory exactly once with visibility (observed/partial/occluded/not-applicable), description and sourceIds. Result fields: jobId, inputFingerprint, status, observations, changes (path/buildingId/street/frontageIndex/description), patchFile and unresolved. You cannot mark work accepted.

The coordinator validates the packet and patch, merges a single block in an isolated checkout, rebuilds changed tiles, runs npm run verify and source reproduction, captures full/oblique/close views, measures performance and obtains visual acceptance. One repair attempt maximum; remaining uncertainty escalates. Validation is a proposal check, not proof of visual fidelity.
''')
        print(json.dumps({'packet': str(args.out / 'packet.json'), 'authorizedSources': len(selected), 'apiRequestsSent': 0})); return
    packet = read(args.packet); result = read(args.result)
    errors = validate_packet(packet, queue, policy, sources)
    if not errors: errors += validate_result(packet, result, fingerprint())
    patch = result.get('patchFile')
    if not errors and result.get('status') == 'proposed':
        path = args.result.parent / patch
        if not path.is_file() or path.is_symlink(): errors.append('Reviewable patch file missing or a symlink')
        else:
            content = path.read_text()
            targets = re.findall(r'^\+\+\+ b/(.+)$', content, re.M)
            headers = re.findall(r'^(?:---|\+\+\+) (.+)$', content, re.M)
            valid_headers = all(h[:2] in ['a/', 'b/'] and h[2:] in packet['allowedFiles'] for h in headers)
            if (not targets or not valid_headers or len(headers) != len(targets) * 2
                or any(p not in packet['allowedFiles'] for p in targets)
                or any(marker in content for marker in ['GIT binary patch', 'new file mode', 'deleted file mode', 'old mode', 'new mode', 'rename from', 'rename to'])):
                errors.append('Patch creates/deletes/renames files or changes paths outside the packet')
    print(json.dumps({'validProposalRecord': not errors, 'accepted': False, 'errors': errors}, indent=2))
    if errors: raise SystemExit(1)


if __name__ == '__main__':
    try: main()
    except (ValueError, KeyError, TypeError) as error:
        raise SystemExit(f'Workflow input rejected: {error}')
