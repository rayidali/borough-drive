"""Offline workflow invariants; synthetic permission records, no API calls."""
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('workflow', ROOT / 'scripts/block-workflow.py')
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
policy = w.read(ROOT / 'model-source/workflow/policy.json')
data = w.read(ROOT / 'dist/reconstruction/neighborhood.json')
corner = w.read(ROOT / 'model-source/first-and-seventh.json')
queue = w.inventory(data, corner, [])
faces = [j for j in queue['jobs'] if j['kind'] == 'facade']
assert len(faces) == sum(len(b['frontages']) for b in data['buildings'])
assert len({(j['buildingId'], j['frontageIndex']) for j in faces}) == len(faces)
assert all(j['status'] == 'protected-baseline' for j in faces if j['group'] == 'core-preserve')
assert not any(j['accepted'] for j in queue['jobs']), 'Inventory must not certify completion'
for count, budget in [(4, 2), (0, 2), (3, 0.001), (3, 20)]:
    try: w.plan(queue, policy, 'first-seventh-pilot', count, budget)
    except ValueError: pass
    else: raise AssertionError('Invalid plan size/cost accepted')
plan = w.plan(queue, policy, 'first-seventh-pilot', 3, 2)
assert len(plan['jobIds']) == 3 and plan['apiRequestsSent'] == 0

job = next(j for j in faces if j['id'] == 'facade-241822226-first-avenue')
source = {'id': 'test-full', 'jobIds': [job['id']], 'provider': 'owner-supplied',
          'uri': 'synthetic-test-photo.jpg', 'view': 'full-facade', 'credit': 'Test only', 'captureDate': '2026-09-10',
          'rights': {'approved': True, 'derivativeUse': True, 'aiProcessing': True, 'basis': 'Synthetic test, no real image'}}
assert w.authorized_source(source)
for edits in [{'provider': 'google'}, {'uri': 'https://maps.googleapis.com/maps/api/streetview'}, {'captureDate': '2026-99-99'}, {'rights': {'approved': True}}]:
    assert not w.authorized_source({**source, **edits})
sources = [source, {**source, 'id': 'test-oblique', 'view': 'oblique'}]
ready_queue = w.inventory(data, corner, sources)
ready = next(j for j in ready_queue['jobs'] if j['id'] == job['id'])
assert ready['status'] == 'ready-for-worker'
packet = {'job': ready, 'inputFingerprint': 'test-hash', 'requiredCategories': policy['requiredCategories'],
          'sources': sources, 'allowedFiles': w.allowed_files(ready)}
assert not w.validate_packet(packet, ready_queue, policy, sources)
forged = copy.deepcopy(packet); forged['allowedFiles'].append('.env')
assert w.validate_packet(forged, ready_queue, policy, sources), 'Worker cannot expand permissions'
forged = copy.deepcopy(packet); forged['sources'].append({**source, 'id': 'forged'})
assert w.validate_packet(forged, ready_queue, policy, sources), 'Worker cannot grant new imagery rights'
result = {'jobId': job['id'], 'inputFingerprint': 'test-hash', 'status': 'proposed',
          'observations': [{'category': c, 'visibility': 'observed', 'description': 'Synthetic test', 'sourceIds': ['test-full']} for c in policy['requiredCategories']],
          'changes': [{'path': packet['allowedFiles'][0], 'buildingId': job['buildingId'], 'street': job['street'], 'frontageIndex': job['frontageIndex'], 'description': 'Synthetic test'}],
          'patchFile': 'proposal.patch', 'unresolved': []}
assert not w.validate_result(packet, result, 'test-hash')
assert w.validate_result(packet, result, 'changed-hash'), 'Stale work must be rejected'
for field, value in [('status', 'accepted'), ('patchFile', '../outside.patch'), ('jobId', 'another-job')]:
    assert w.validate_result(packet, {**result, field: value}, 'test-hash')
bad = copy.deepcopy(result); bad['observations'].pop(); assert w.validate_result(packet, bad, 'test-hash')
bad = copy.deepcopy(result); bad['observations'][0]['sourceIds'] = ['unknown']; assert w.validate_result(packet, bad, 'test-hash')
bad = copy.deepcopy(result); bad['changes'][0]['buildingId'] = 0; assert w.validate_result(packet, bad, 'test-hash')
empty_packet = {**packet, 'job': job, 'sources': []}
blocked = {**result, 'status': 'needs-evidence', 'changes': [], 'patchFile': None, 'unresolved': ['Need authorized full/oblique photos'],
           'observations': [{'category': c, 'visibility': 'occluded', 'description': 'No authorized image supplied', 'sourceIds': []} for c in policy['requiredCategories']]}
assert not w.validate_result(empty_packet, blocked, 'test-hash')
assert w.validate_result(empty_packet, result, 'test-hash'), 'Missing sources cannot pass as a proposal'
print(json.dumps({'uniqueFacadeSections': len(faces), 'allWorkItems': len(queue['jobs']), 'ownershipSourcesBudgetsStaleInputsAndEscalation': 'passed', 'apiCalls': 0}))
