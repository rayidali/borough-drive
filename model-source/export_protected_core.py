"""Losslessly unpack accepted core geometry for Godot; never re-author it.

Reads the original GLB, uses Blender's installed Draco bridge only to decode
compressed accessors, preserves source node transforms/material JSON/image
bytes, and omits separately owned street dressing. No Blender scene export.
Bridge ABI reference: Blender io_scene_gltf2/blender/imp/
draco_compression_extension.py (glTF-Blender-IO authors, Apache-2.0).
"""
import ctypes as C
import hashlib
import json
import struct
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'dist/reconstruction/first-and-10th.glb'
OUTPUT = ROOT / 'engine/first-seventh/assets/protected-core.glb'
REPORT = ROOT / 'model-source/east-village-e10-block/core-conversion.json'
BASELINE = json.loads((REPORT.parent / 'protected-models.json').read_text())
sha = lambda b: hashlib.sha256(b).hexdigest()
raw = SOURCE.read_bytes()
assert sha(raw) == BASELINE['coreSourceSha256']
json_len = struct.unpack_from('<I', raw, 12)[0]
source = json.loads(raw[20:20 + json_len])
bin_start = 20 + json_len + 8
binary = raw[bin_start:]
owners = {
 '163 First Avenue':247851944, '159–161 First Avenue':247852692,
 '164 First Avenue':248142962, '162 First Avenue':248142976,
 'Theater and tower':247852695, '165 1st Avenue':247851882,
 '167 1st Avenue':247851883, '169 1st Avenue':247851884,
 '171 1st Avenue':247851885, '166 1st Avenue':248142864,
 '168 1st Avenue':248142866, '170 1st Avenue':248142868,
 '160 1st Avenue':248142862, '158 1st Avenue':248142861,
 '156 1st Avenue':248142860, '153 1st Avenue':247852655,
 '151 1st Avenue':247852701, '247 East 10th Street':248142883,
 '249 East 10th Street':248142885, '248 East 10th Street':248142884,
 '250 East 10th Street':248142886, '254 East 10th Street':248142889,
 '239 East 10th Street':247851912,
}
C.CDLL('/Applications/Blender.app/Contents/Resources/lib/libdraco.dylib',mode=C.RTLD_GLOBAL)
library = C.CDLL('/Applications/Blender.app/Contents/Resources/5.2/scripts/addons_core/io_scene_gltf2/libbf_intern_draco_bridge.dylib')
signatures = {
 'decoderCreate':(C.c_void_p,[]), 'decoderRelease':(None,[C.c_void_p]),
 'decoderDecode':(C.c_bool,[C.c_void_p,C.c_void_p,C.c_size_t]),
 'decoderReadAttribute':(C.c_bool,[C.c_void_p,C.c_uint32,C.c_size_t,C.c_char_p]),
 'decoderGetVertexCount':(C.c_uint32,[C.c_void_p]),
 'decoderGetIndexCount':(C.c_uint32,[C.c_void_p]),
 'decoderGetAttributeByteLength':(C.c_size_t,[C.c_void_p,C.c_uint32]),
 'decoderCopyAttribute':(None,[C.c_void_p,C.c_uint32,C.c_void_p]),
 'decoderReadIndices':(C.c_bool,[C.c_void_p,C.c_size_t]),
 'decoderGetIndicesByteLength':(C.c_size_t,[C.c_void_p]),
 'decoderCopyIndices':(None,[C.c_void_p,C.c_void_p]),
}
for name,(result,args) in signatures.items():
 fn=getattr(library,name);fn.restype=result;fn.argtypes=args

out={'asset':deepcopy(source['asset']), 'scene':0, 'scenes':[{'nodes':[]}],
     'nodes':[], 'meshes':[], 'accessors':[], 'bufferViews':[], 'buffers':[],
     'materials':deepcopy(source['materials']), 'textures':deepcopy(source['textures']),
     'images':[], 'samplers':deepcopy(source['samplers'])}
for key in ('extensionsUsed','extensionsRequired'):
 values=[v for v in source.get(key,[]) if v!='KHR_draco_mesh_compression']
 if values:out[key]=values
blob=bytearray(); checks=[]; groups={}; selected=[]

def original_view(index):
 view=source['bufferViews'][index];start=view.get('byteOffset',0)
 assert view.get('buffer',0)==0
 return binary[start:start+view['byteLength']]

def append_view(data,target=None):
 while len(blob)%4:blob.append(0)
 view={'buffer':0,'byteOffset':len(blob),'byteLength':len(data)}
 if target:view['target']=target
 index=len(out['bufferViews']);out['bufferViews'].append(view);blob.extend(data)
 return index

def append_accessor(index,data,count,target):
 accessor=deepcopy(source['accessors'][index]);assert 'sparse' not in accessor
 accessor['bufferView']=append_view(data,target);accessor['byteOffset']=0;accessor['count']=count
 result=len(out['accessors']);out['accessors'].append(accessor)
 checks.append({'sourceAccessor':index,'outputAccessor':result,'bytes':len(data),'sha256':sha(data)})
 return result

for source_index,node in enumerate(source['nodes']):
 provenance=node.get('extras',{}).get('provenance',node['name'])
 matches=[bid for prefix,bid in owners.items() if provenance.startswith(prefix)]
 assert len(matches)<=1
 if matches:owner=str(matches[0])
 elif provenance.startswith('Architectural detail'):owner='Details'
 else:continue
 assert not node.get('children') and 'mesh' in node
 copied=deepcopy(node);mesh=deepcopy(source['meshes'][node['mesh']])
 for primitive in mesh['primitives']:
  extension=primitive['extensions'].pop('KHR_draco_mesh_compression')
  if not primitive['extensions']:primitive.pop('extensions')
  decoder=library.decoderCreate()
  try:
   compressed=original_view(extension['bufferView'])
   assert library.decoderDecode(decoder,compressed,len(compressed))
   old=primitive['indices'];accessor=source['accessors'][old]
   assert library.decoderReadIndices(decoder,accessor['componentType'])
   n=library.decoderGetIndicesByteLength(decoder);buffer=C.create_string_buffer(n)
   library.decoderCopyIndices(decoder,buffer)
   primitive['indices']=append_accessor(old,buffer.raw,library.decoderGetIndexCount(decoder),34963)
   for semantic,attribute in extension['attributes'].items():
    old=primitive['attributes'][semantic];accessor=source['accessors'][old]
    assert library.decoderReadAttribute(decoder,attribute,accessor['componentType'],accessor['type'].encode())
    n=library.decoderGetAttributeByteLength(decoder,attribute);buffer=C.create_string_buffer(n)
    library.decoderCopyAttribute(decoder,attribute,buffer)
    primitive['attributes'][semantic]=append_accessor(old,buffer.raw,library.decoderGetVertexCount(decoder),34962)
  finally:library.decoderRelease(decoder)
 copied['mesh']=len(out['meshes']);out['meshes'].append(mesh)
 copied.setdefault('extras',{})['protectedCoreOwner']=owner
 idx=len(out['nodes']);out['nodes'].append(copied);groups.setdefault(owner,[]).append(idx)
 selected.append({'sourceNode':source_index,'outputNode':idx,'owner':owner,'name':node['name']})

assert set(groups)=={str(i) for i in owners.values()}|{'Details'}
assert len(selected)==521 and len(groups['Details'])==9
images=[]
for old in source['images']:
 image=deepcopy(old);data=original_view(old['bufferView']);image['bufferView']=append_view(data)
 out['images'].append(image);images.append({'name':old.get('name'),'bytes':len(data),'sha256':sha(data)})
for owner,children in groups.items():
 out['scenes'][0]['nodes'].append(len(out['nodes']))
 out['nodes'].append({'name':'ProtectedCore_'+owner,'children':children,'extras':{'protectedCoreOwner':owner}})
out['buffers']=[{'byteLength':len(blob)}]
metadata=json.dumps(out,separators=(',',':'),ensure_ascii=False).encode()
metadata+=b' '*((-len(metadata))%4);blob+=b'\0'*((-len(blob))%4)
result=struct.pack('<III',0x46546c67,2,12+8+len(metadata)+8+len(blob))
result+=struct.pack('<II',len(metadata),0x4e4f534a)+metadata
result+=struct.pack('<II',len(blob),0x004e4942)+blob

# Check the actual serialized bytes, independently of the append cursor.
jl=struct.unpack_from('<I',result,12)[0];verify=json.loads(result[20:20+jl]);vb=result[28+jl:]
for check in checks:
 accessor=verify['accessors'][check['outputAccessor']];view=verify['bufferViews'][accessor['bufferView']]
 assert sha(vb[view['byteOffset']:view['byteOffset']+view['byteLength']])==check['sha256']
assert verify['materials']==source['materials'] and verify['textures']==source['textures']
assert verify['samplers']==source['samplers']
for expected,image in zip(images,verify['images']):
 view=verify['bufferViews'][image['bufferView']]
 assert sha(vb[view['byteOffset']:view['byteOffset']+view['byteLength']])==expected['sha256']
for row in selected:
 old=source['nodes'][row['sourceNode']];new=verify['nodes'][row['outputNode']]
 for key in ('matrix','translation','rotation','scale'):assert old.get(key)==new.get(key)
assert sha(SOURCE.read_bytes())==sha(raw)
OUTPUT.parent.mkdir(parents=True,exist_ok=True);OUTPUT.write_bytes(result)
report={'source':str(SOURCE.relative_to(ROOT)),'sourceSha256':sha(raw),
 'output':str(OUTPUT.relative_to(ROOT)),'outputSha256':sha(result),'outputBytes':len(result),
 'scope':'Decode original protected building/detail accessors only; no geometry regeneration, transform or material conversion.',
 'buildingOwners':23,'sharedDetailOwners':1,'meshes':len(selected),
 'materialJsonUnchanged':True,'imageBytesUnchanged':True,'nodeTransformsUnchanged':True,
 'coordinateFrame':'Original core x/up/z; apply z=-228 exactly once in the engine adapter.',
 'sourceNodes':selected,'accessors':checks,'images':images,
 'limits':['Not yet imported, visually reviewed or integrated with runtime collision/loading.',
           'All original materials/images remain, including unused street assets; no texture pruning or atlas change.',
           'Decoded accessor hashes establish this conversion only; final Godot geometry/material checks remain.']}
# Runtime image library keeps the original encoded bytes once. The three
# asphalt maps belong only to deliberately omitted legacy street dressing.
used_materials={primitive['material'] for mesh in verify['meshes'] for primitive in mesh['primitives'] if 'material' in primitive}
used_textures=set()
def collect_textures(value):
 if isinstance(value,dict):
  for key,item in value.items():
   if key.endswith('Texture') and isinstance(item,dict) and 'index' in item:used_textures.add(item['index'])
   else:collect_textures(item)
 elif isinstance(value,list):
  for item in value:collect_textures(item)
for index in used_materials:collect_textures(verify['materials'][index])
used_images=sorted({verify['textures'][i]['source'] for i in used_textures})
assert used_images==list(range(9)),used_images
payload=bytearray();index=[]
for i in used_images:
 img=verify['images'][i];view=verify['bufferViews'][img['bufferView']];data=vb[view['byteOffset']:view['byteOffset']+view['byteLength']]
 index.append({'name':img.get('name','image-'+str(i)),'mime':img['mimeType'],'offset':len(payload),'length':len(data),'sha256':sha(data)});payload.extend(data)
(OUTPUT.parent/'protected-core-textures.bin').write_bytes(payload)
(OUTPUT.parent/'protected-core-textures.json').write_text(json.dumps({'images':index,'sha256':sha(payload),'source':'Original protected-core GLB; nine used images retained byte-for-byte; three unused asphalt images remain in source GLB.'},indent=2)+'\n')
report['runtimeTextureLibrary']={'bytes':len(payload),'sha256':sha(payload),'images':9,'encoding':'Original JPEG/PNG bytes; no resampling, re-encoding or new imagery.'}
REPORT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:report[k] for k in ('output','outputBytes','outputSha256','buildingOwners','meshes')}))
