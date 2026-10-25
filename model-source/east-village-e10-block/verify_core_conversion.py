"""Independent Blender comparison of converted core with frozen source audit."""
import bpy
import hashlib
import json
import struct
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
audit=json.loads((HERE/'core-source-audit.json').read_text())
expected={m['name']:m for m in audit['meshes'] if m['buildingId'] or m['provenance'].startswith('Architectural detail')}
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(ROOT/'engine/first-seventh/assets/protected-core.glb'))
seen=set();mismatches=[];triangles=0
for obj in bpy.context.scene.objects:
 if obj.type!='MESH':continue
 assert obj.name in expected,obj.name
 seen.add(obj.name);mesh=obj.data;mesh.calc_loop_triangles();digest=hashlib.sha256()
 for vertex in mesh.vertices:
  v=obj.matrix_world@vertex.co
  digest.update(struct.pack('<3d',float(v.x),float(v.z),float(-v.y)))
 for tri in mesh.loop_triangles:digest.update(struct.pack('<3I',*tri.vertices))
 triangles+=len(mesh.loop_triangles)
 if digest.hexdigest()!=expected[obj.name]['decodedGeometrySha256']:mismatches.append(obj.name)
assert seen==set(expected)
assert not mismatches,mismatches
report={'decoder':'Blender '+bpy.app.version_string,'sourceAudit':'core-source-audit.json',
 'convertedAsset':'engine/first-seventh/assets/protected-core.glb','matchingMeshes':len(seen),
 'triangles':triangles,'mismatches':mismatches,
 'scope':'Independent import comparison of transformed vertices and triangle indices with the earlier original-GLB audit.',
 'limits':'Engine import, material rendering, runtime ownership and matched-view review remain separate.'}
(HERE/'core-conversion-independent.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
