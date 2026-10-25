"""Describe immutable core owners in the Seventh coordinate frame.

Run after export_protected_core.py. Scene bytes come from Godot's imported
source groups; this file never generates or replaces accepted geometry.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'model-source/east-village-e10-block'
conversion = json.loads((HERE / 'core-conversion.json').read_text())
geography = json.loads((ROOT / 'dist/reconstruction/neighborhood.json').read_text())
buildings = {b['id']: b for b in geography['buildings']}
ordinary = json.loads((ROOT / 'engine/first-seventh/assets/slice.json').read_text())
existing = {b['id'] for b in ordinary['buildings'] if b.get('kind') != 'protected-core'}
ids = sorted({int(n['owner']) for n in conversion['sourceNodes'] if n['owner'] != 'Details'})
assert len(ids) == 23 and not existing.intersection(ids)
asset = ROOT / conversion['output']
assert hashlib.sha256(asset.read_bytes()).hexdigest() == conversion['outputSha256']
records = []
for bid in ids:
    b = buildings[bid]
    assert b['core']
    records.append({
        'id': bid, 'kind': 'protected-core', 'address': b['address'],
        'asset': 'res://assets/protected-core.glb',
        'group': 'ProtectedCore_' + str(bid),
        'sha256': conversion['outputSha256'],
        'position': [0, 0, -228],
        'footprint': [[p[0], p[1] - 228] for p in b['p']],
        'height': b['height'],
        'protection': 'Unchanged accepted source geometry/materials; translated once.',
    })

# This reserved negative runtime ID is explicitly not a mapped building.
# The shared source material batches span four corners and own no collider.
details = {
    'id': -10010, 'kind': 'protected-core-details',
    'asset': 'res://assets/protected-core.glb', 'group': 'ProtectedCore_Details',
    'sha256': conversion['outputSha256'], 'position': [0, 0, -228],
    'protection': 'Nine unchanged shared architectural-detail meshes; no collision.',
}
result = {'schema': 1, 'source': conversion['source'],
          'sourceSha256': conversion['sourceSha256'],
          'convertedSha256': conversion['outputSha256'],
          'buildingOwners': records, 'sharedModels': [details]}
destination = ROOT / 'engine/first-seventh/assets/protected-core.json'
destination.write_text(json.dumps(result, indent=2) + '\n')
print('Protected core metadata:', len(records), 'building owners and one non-colliding detail owner')
