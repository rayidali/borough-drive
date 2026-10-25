import json,struct,math,collections,hashlib
from pathlib import Path
D=Path('model-source/east-village-e09-east');base=json.loads((D/'baseline-slice.json').read_text());b=next(b for b in base['buildings'] if b['id']==248142713)
def read(path):
 raw=Path(path).read_bytes();n=struct.unpack_from('<I',raw,12)[0];g=json.loads(raw[20:20+n]);blob=raw[28+n:]
 def acc(i):
  a=g['accessors'][i];v=g['bufferViews'][a['bufferView']];typ={5126:'f',5125:'I',5123:'H',5121:'B'}[a['componentType']];cnt={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']];sz=struct.calcsize(typ);off=v.get('byteOffset',0)+a.get('byteOffset',0);st=v.get('byteStride',sz*cnt)
  rows=[struct.unpack_from('<'+typ*cnt,blob,off+j*st) for j in range(a['count'])]
  if a.get('normalized'):rows=[tuple(x/(65535 if typ=='H' else 255) for x in r) for r in rows]
  return rows
 def transform(p,node):
  p=[p[i]*node.get('scale',[1,1,1])[i] for i in range(3)];x,y,z,w=node.get('rotation',[0,0,0,1]);u=[x,y,z];uv=[y*p[2]-z*p[1],z*p[0]-x*p[2],x*p[1]-y*p[0]];uuv=[y*uv[2]-z*uv[1],z*uv[0]-x*uv[2],x*uv[1]-y*uv[0]]
  return tuple(p[i]+2*(w*uv[i]+uuv[i])+node.get('translation',[0,0,0])[i]+b['position'][i] for i in range(3))
 result=collections.Counter()
 for node in g['nodes']:
  if 'mesh' not in node:continue
  for pr in g['meshes'][node['mesh']]['primitives']:
   pos=[transform(p,node) for p in acc(pr['attributes']['POSITION'])];col=acc(pr['attributes']['COLOR_0']);ids=[r[0] for r in acc(pr['indices'])];mat=g['materials'][pr['material']]['name']
   for j in range(0,len(ids),3):
    ix=ids[j:j+3];pts=[pos[i] for i in ix]
    if not all(p[0]<16.1 and p[2]>-143.65 for p in pts):continue
    row=(mat,tuple(sorted(tuple(round(x,4) for x in (*pos[i],*col[i])) for i in ix)));result[row]+=1
 return result
old=read(D/'preserved-148-first.glb');new=read('engine/first-seventh/assets/neighborhood/building-248142713.glb');missing=old-new;extra=new-old
r={'scope':'148 First-facing geometry with world x<16.1 and z>-143.65 (corner seam excluded); mapped footprint/height separately verified. Transformed triangle positions and vertex colors rounded to 0.1 mm; triangle order ignored.','oldTriangles':old.total(),'newTriangles':new.total(),'missing':missing.total(),'added':extra.total(),'oldHash':hashlib.sha256(repr(sorted(old.items())).encode()).hexdigest(),'newHash':hashlib.sha256(repr(sorted(new.items())).encode()).hexdigest(),'limits':'Not a whole-model byte test. New Ninth wall openings and corner junction must be visually reviewed.'}
(D/'first-face-preservation.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
