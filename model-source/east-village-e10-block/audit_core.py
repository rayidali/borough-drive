"""Read the accepted core GLB and audit ownership without exporting or editing it.

Run with Blender --background --python this-file. The resulting bounds use the
original game frame (x, up, z), before the engine's z = source_z - 228 shift.
Shared architectural/street meshes remain explicitly unassigned to a building.
"""
import hashlib
import json
import struct
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'dist/reconstruction/first-and-10th.glb'
OUT = Path(__file__).resolve().parent
data = SOURCE.read_bytes()
source_hash = hashlib.sha256(data).hexdigest()
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(SOURCE))

owners = {
    '163 First Avenue': 247851944, '159–161 First Avenue': 247852692,
    '164 First Avenue': 248142962, '162 First Avenue': 248142976,
    'Theater and tower': 247852695,
    '165 1st Avenue': 247851882, '167 1st Avenue': 247851883,
    '169 1st Avenue': 247851884, '171 1st Avenue': 247851885,
    '166 1st Avenue': 248142864, '168 1st Avenue': 248142866,
    '170 1st Avenue': 248142868, '160 1st Avenue': 248142862,
    '158 1st Avenue': 248142861, '156 1st Avenue': 248142860,
    '153 1st Avenue': 247852655, '151 1st Avenue': 247852701,
    '247 East 10th Street': 248142883, '249 East 10th Street': 248142885,
    '248 East 10th Street': 248142884, '250 East 10th Street': 248142886,
    '254 East 10th Street': 248142889, '239 East 10th Street': 247851912,
}
records = []
for obj in bpy.context.scene.objects:
    if obj.type != 'MESH':
        continue
    mesh = obj.data
    mesh.calc_loop_triangles()
    provenance = obj.get('provenance', obj.name)
    matches = [bid for prefix, bid in owners.items() if provenance.startswith(prefix)]
    assert len(matches) <= 1, obj.name
    # Blender imports glTF Y-up into Z-up; invert its axis conversion here.
    vertices = []
    for vertex in mesh.vertices:
        v = obj.matrix_world @ vertex.co
        vertices.append((float(v.x), float(v.z), float(-v.y)))
    digest = hashlib.sha256()
    for v in vertices:
        digest.update(struct.pack('<3d', *v))
    for triangle in mesh.loop_triangles:
        digest.update(struct.pack('<3I', *triangle.vertices))
    records.append({
        'name': obj.name, 'provenance': provenance,
        'buildingId': matches[0] if matches else None,
        'ownershipState': 'named building source' if matches else 'shared source; explicit ownership still required',
        'vertices': len(vertices), 'triangles': len(mesh.loop_triangles),
        'bounds': [min(v[i] for v in vertices) for i in range(3)] +
                  [max(v[i] for v in vertices) for i in range(3)],
        'decodedGeometrySha256': digest.hexdigest(),
        'materials': [m.name if m else None for m in mesh.materials],
    })

assert {r['buildingId'] for r in records if r['buildingId']} == set(owners.values())
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == source_hash
report = {
    'source': str(SOURCE.relative_to(ROOT)), 'sourceSha256': source_hash,
    'blender': bpy.app.version_string, 'scope': 'Read-only decoded source audit; no engine import or model export',
    'coordinateFrame': 'Original game x/up/z; engine translation not applied',
    'buildingOwners': len(owners), 'meshCount': len(records),
    'sharedMeshCount': sum(r['buildingId'] is None for r in records),
    'limits': ['Geometry digests describe this decoder and vertex order; compare final conversion independently.',
               'Naming establishes source group identity, not complete ownership of shared architectural-detail meshes.',
               'No source-to-game visual preservation or protected-core adapter acceptance is claimed.'],
    'meshes': sorted(records, key=lambda r: r['name']),
}
(OUT / 'core-source-audit.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({k: report[k] for k in ['sourceSha256', 'buildingOwners', 'meshCount', 'sharedMeshCount']}))
