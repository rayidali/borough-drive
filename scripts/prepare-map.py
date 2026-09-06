"""Compile the bundled OpenStreetMap extract into game coordinates (metres).
Derived geographic database: ODbL 1.0; source: OpenStreetMap contributors.
Run after replacing source-data/osm-raw.json with an Overpass out geom extract.
"""
import json, math, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
raw=json.loads((ROOT/'source-data/osm-raw.json').read_text())
LAT,LON=40.727,-73.9845
SX=111320*math.cos(math.radians(LAT))
BOUNDS=[(-73.996-LON)*SX,-(40.735-LAT)*111320,(-73.972-LON)*SX,-(40.719-LAT)*111320]
def point(p):return [round((p['lon']-LON)*SX,2),round(-(p['lat']-LAT)*111320,2)]
def inside(p):return BOUNDS[0]<p[0]<BOUNDS[2] and BOUNDS[1]<p[1]<BOUNDS[3]
def num(s,default):
 try:
  v=float(re.search(r'[\d.]+',str(s))[0]);return v*.3048 if 'ft' in str(s) or "'" in str(s) else v
 except:return default
buildings=[];roads=[];parks=[];pois=[];addresses=[]
allowed={'residential','tertiary','secondary','primary','unclassified','living_street','service','tertiary_link','secondary_link','primary_link'}
for e in raw['elements']:
 t=e.get('tags',{});g=e.get('geometry',[])
 pts=[point(p) for p in g if p]
 if e['type']=='node':center=point(e)
 elif pts:center=[round(sum(p[i] for p in pts)/len(pts),2) for i in (0,1)]
 else:continue
 if 'building' in t and len(pts)>3 and inside(center):
  h=num(t.get('height'),num(t.get('building:levels'),5)*3.2)
  buildings.append({'id':e['id'],'p':pts,'h':round(max(3,min(h,180)),2),'base':num(t.get('min_height'),0),'c':center,'name':t.get('name',''),'address':' '.join(filter(None,[t.get('addr:housenumber'),t.get('addr:street')])),'estimated':not bool(t.get('height') or t.get('building:levels'))})
 if t.get('highway') in allowed and len(pts)>1 and t.get('access')!='private' and t.get('tunnel')!='yes':
  lanes=num(t.get('lanes'),1)
  width=num(t.get('width'),max(8.4,lanes*3.1+4.5))
  if t.get('name','').startswith(('Avenue','1st','2nd','3rd','First','Second','Third')):width=max(width,13)
  roads.append({'id':e['id'],'p':pts,'nodes':e.get('nodes',[]),'name':t.get('name','Service road'),'w':round(min(width,24),2),'oneway':t.get('oneway') in ('yes','-1'),'reverse':t.get('oneway')=='-1','class':t['highway']})
 if t.get('leisure')=='park' and len(pts)>3:
  parks.append({'p':pts,'name':t.get('name','Park')})
 if t.get('name') and ('shop' in t or 'amenity' in t) and inside(center):
  pois.append({'id':e['id'],'p':center,'name':t['name'],'type':t.get('shop',t.get('amenity')),'address':' '.join(filter(None,[t.get('addr:housenumber'),t.get('addr:street')]))})
 if t.get('addr:housenumber') and t.get('addr:street') and inside(center):
  addresses.append({'name':t['addr:housenumber']+' '+t['addr:street'],'p':center})
d={'origin':[LAT,LON],'scale':SX,'bounds':BOUNDS,'snapshot':raw['osm3s']['timestamp_osm_base'],'attribution':'© OpenStreetMap contributors · ODbL 1.0','buildings':buildings,'roads':roads,'parks':parks,'places':pois,'addresses':addresses}
(ROOT/'dist/data/east-village.json').write_text(json.dumps(d,separators=(',',':')))
print({k:len(d[k]) for k in ['buildings','roads','parks','places','addresses']})
print('estimated heights',sum(b['estimated'] for b in buildings))
print('Avenue A sample',next(r for r in roads if r['name']=='Avenue A'))
