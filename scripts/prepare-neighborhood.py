"""Build the ten-block geographic manifest from the checked-in OSM snapshot.

Coordinates use exactly the First & 10th reconstruction's metre-scale frame.
Street widths are photographic estimates; footprint coordinates and heights
retain their OSM provenance. No current tenants are inferred from old OSM POIs.
"""
import json, math, re
from pathlib import Path
from neighborhood_evidence import apply_geography

ROOT = Path(__file__).resolve().parents[1]
raw = json.loads((ROOT/'source-data/osm-raw.json').read_text())
base = json.loads((ROOT/'model-source/intersection-base.json').read_text())
lat, lon = base['origin']['lat'], base['origin']['lon']
angle = math.radians(base['axis']['avenueBearing'])
cs, sn = math.cos(angle), math.sin(angle)
EXTENT = [-287, -208, 271, 276]
DRIVE = [-244, -174, 230, 244]
AVENUES = [('Second Avenue', -229, 10.75), ('First Avenue', 0, 10.75), ('Avenue A', 214, 9.3)]
STREETS = [('East 12th Street', -157.8), ('East 11th Street', -76.3), ('East 10th Street', 0), ('East 9th Street', 73.3), ('St. Marks Place', 150.1), ('East 7th Street', 228)]

def point(p):
    e = (p['lon']-lon)*111320*math.cos(math.radians(lat))
    n = (p['lat']-lat)*111320
    return [round(e*cs-n*sn, 3), round(-e*sn-n*cs, 3)]

def number(value, fallback):
    try:
        v = float(re.search(r'[\d.]+', str(value))[0])
        return v*.3048 if 'ft' in str(value) else v
    except (TypeError, ValueError):
        return fallback

def inside(x, z, polygon):
    yes = False
    for a,b in zip(polygon, polygon[1:]+polygon[:1]):
        if (a[1]>z)!=(b[1]>z) and x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0]:
            yes = not yes
    return yes

def closest(point, a, b):
    dx,dz=b[0]-a[0],b[1]-a[1]
    t=max(0,min(1,((point[0]-a[0])*dx+(point[1]-a[1])*dz)/(dx*dx+dz*dz or 1)))
    return [a[0]+dx*t,a[1]+dz*t]

core_ids = set(map(int, re.findall(r'\b(?:247|248)\d{6}\b', (ROOT/'model-source/build_intersection.py').read_text())))
roads = []
for name,x,width in AVENUES:
    roads.append({'name':name,'a':[x,EXTENT[1]],'b':[x,EXTENT[3]],'halfWidth':width,'axis':'avenue','oneway': -1 if name=='First Avenue' else 1 if name=='Second Avenue' else 0})
for name,z in STREETS:
    east_end=214 if name in ['East 9th Street','St. Marks Place'] else EXTENT[2]
    roads.append({'name':name,'a':[EXTENT[0],z],'b':[east_end,z],'halfWidth':4.95,'axis':'street','oneway':-1 if name in ['East 7th Street','East 9th Street','East 11th Street'] else 1})

buildings=[]
for e in raw['elements']:
    tags=e.get('tags',{})
    if e['type']!='way' or 'building' not in tags or len(e.get('geometry',[]))<4: continue
    if tags.get('historic') in ['memorial','monument'] or e['id']==576178058:continue
    p=[point(q) for q in e['geometry'] if q]
    if p[0]==p[-1]:p=p[:-1]
    xs,zs=[q[0] for q in p],[q[1] for q in p]
    box=[min(xs),min(zs),max(xs),max(zs)]
    center=[(box[0]+box[2])/2,(box[1]+box[3])/2]
    if not (EXTENT[0]<center[0]<EXTENT[2] and EXTENT[1]<center[1]<EXTENT[3]):continue
    h=number(tags.get('height'),number(tags.get('building:levels'),5)*3.2)
    address=' '.join(filter(None,[tags.get('addr:housenumber'),tags.get('addr:street')]))
    row=next((i for i in range(5) if STREETS[i][1]<=center[1]<STREETS[i+1][1]),None)
    col=0 if -229<center[0]<0 else 1 if 0<=center[0]<214 else None
    tile=f'block-{row+1}-{col+1}' if row is not None and col is not None else 'edge-'+('west' if center[0]<-229 else 'east' if center[0]>214 else 'north' if center[1]<-157.8 else 'south')
    buildings.append({'id':e['id'],'bin':tags.get('nycdoitt:bin',''),'address':address,'name':tags.get('name',''),'p':p,'box':box,'center':center,'height':round(h,2),'heightEstimated':not bool(tags.get('height') or tags.get('building:levels')),'floors':int(number(tags.get('building:levels'),max(1,round(h/3.25)))),'core':e['id'] in core_ids,'tile':tile,'buildingType':tags.get('building'),'frontages':[]})

# Recover missing addresses only from actual mapped address points inside a footprint.
for e in raw['elements']:
    t=e.get('tags',{})
    if e['type']!='node' or not t.get('addr:housenumber') or not t.get('addr:street'):continue
    p=point(e)
    for b in buildings:
        bb=b['box']
        if bb[0]<=p[0]<=bb[2] and bb[1]<=p[1]<=bb[3] and inside(*p,b['p']):
            address=t['addr:housenumber']+' '+t['addr:street']
            if not b['address']:b['address']=address
            b.setdefault('addressAliases',[]).append(address);break

geography_audit = apply_geography(buildings, point, STREETS, EXTENT)

for b in buildings:
    p=b['p'];area=sum(a[0]*c[1]-c[0]*a[1] for a,c in zip(p,p[1:]+p[:1]))
    if area<0:p=list(reversed(p))
    for a,c in zip(p,p[1:]+p[:1]):
        length=math.dist(a,c)
        if length<2.8:continue
        # CCW in x,z; right normal points out. Facade helper uses left normal,
        # so reverse the edge for the architectural component frame.
        rx,rz=(a[0]-c[0])/length,(a[1]-c[1])/length
        nx,nz=-rz,rx
        mid=[(a[0]+c[0])/2,(a[1]+c[1])/2]
        near=sorted([(math.dist(mid,closest(mid,r['a'],r['b']))-r['halfWidth'],r) for r in roads],key=lambda q:q[0])
        dist,road=near[0];target=closest(mid,road['a'],road['b'])
        dot=nx*(target[0]-mid[0])+nz*(target[1]-mid[1])
        # A street facade must face the road, not merely be close to it.
        # The former sign-only test incorrectly dressed perpendicular alley walls.
        if dot <= 0 or dot / (math.dist(mid,target) or 1) < .65 or dist>13 or dist<-.5:continue
        probe=[mid[0]+nx*1.5,mid[1]+nz*1.5]
        if any(o['id']!=b['id'] and o['box'][0]<=probe[0]<=o['box'][2] and o['box'][1]<=probe[1]<=o['box'][3] and inside(*probe,o['p']) for o in buildings):continue
        b['frontages'].append({'x':c[0],'z':c[1],'rx':rx,'rz':rz,'length':round(length,3),'street':road['name']})
    # Survey outlines include centimetre-scale collinear segments. Join only
    # neighboring coplanar pieces so a single facade gets one window schedule.
    grouped=[]
    for f in b['frontages']:
        found=None
        for g in grouped:
            nx,nz=-g['rz'],g['rx'];offset=(f['x']-g['x'])*nx+(f['z']-g['z'])*nz
            along=(f['x']-g['x'])*g['rx']+(f['z']-g['z'])*g['rz']
            if f['street']==g['street'] and f['rx']*g['rx']+f['rz']*g['rz']>.999 and abs(offset)<.12 and -f['length']-.3<along<g['length']+.3:
                start=min(0,along);end=max(g['length'],along+f['length'])
                g['x']+=g['rx']*start;g['z']+=g['rz']*start;g['length']=end-start;found=g;break
        if found is None:grouped.append(dict(f))
    b['frontages']=grouped

tiles=[]
for key in sorted(set(b['tile'] for b in buildings)):
    bs=[b for b in buildings if b['tile']==key]
    box=[min(b['box'][0] for b in bs),min(b['box'][1] for b in bs),max(b['box'][2] for b in bs),max(b['box'][3] for b in bs)]
    tiles.append({'id':key,'bounds':box,'buildings':len(bs),'url':'neighborhood/'+key+'.glb'})

data={'origin':base['origin'],'axis':base['axis'],'extent':EXTENT,'driveBounds':DRIVE,'blockCount':10,'snapshot':raw['osm3s']['timestamp_osm_base'],'source':'OpenStreetMap contributors · ODbL 1.0; supplemental buildings: NYC OTI','scope':'East 7th–East 12th Streets, Second Avenue–Avenue A','roads':roads,'avenues':AVENUES,'streets':STREETS,'buildings':buildings,'tiles':tiles,'geographyAudit':geography_audit}
out=ROOT/'dist/reconstruction/neighborhood.json';out.write_text(json.dumps(data,separators=(',',':')))
print(json.dumps({'buildings':len(buildings),'corePreserved':sum(b['core'] for b in buildings),'facades':sum(len(b['frontages']) for b in buildings),'tiles':len(tiles),'unmappedAddresses':sum(not b['address'] for b in buildings)}))
