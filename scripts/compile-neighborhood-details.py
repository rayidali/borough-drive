"""Apply dated observations, keep inferred details explicit, place street dressing."""
import json,re,math,random
from pathlib import Path
from neighborhood_businesses import compile_businesses
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'dist/reconstruction/neighborhood.json';data=json.loads(path.read_text())
observations=json.loads((ROOT/'model-source/neighborhood-observations.json').read_text())
byid={b['id']:b for b in data['buildings']}
# Address-only corrections can be compiled without resetting footprint geometry.
for change in json.loads((ROOT/'model-source/geography-corrections.json').read_text())['addressCorrections']:
    b=byid[change['id']];b['address']=change['address']
    alias=change.get('retainAlias')
    if alias and alias not in b.setdefault('addressAliases',[]):b['addressAliases'].append(alias)
    b['addressSource']={k:v for k,v in change.items() if k not in ['id','retainAlias']}

def norm(s):
    s=s.lower().replace('½','.5').replace('–','-').replace('—','-')
    s=s.replace("mark's",'marks').replace('second','2nd').replace('first','1st').replace('st. marks','saint marks').replace('st marks','saint marks')
    s=re.sub(r'\s+(?:avenue|ave)\b',' avenue',s);s=s.replace('avenue a','avenue a')
    return re.sub(r'\s+',' ',s).strip()

def first_address(s):return re.sub(r'^(\d+)[-–]\d+',r'\1',s)
aliases={}
for b in data['buildings']:
    for a in [b['address'],*b.get('addressAliases',[])]:
        if a:aliases.setdefault(norm(a),b)
byid={b['id']:b for b in data['buildings']}
# Exact identity corrections use parcel/photographic evidence in source records.
manual={
 '170 2nd avenue':247851942,'181-189 2nd avenue':247852538,
 '107 east 7th street':248142618,'111-115 east 7th street':248142624,
 '287 east 10th street':248142975,'181 avenue a':281499419,
 '307 east 12th street':247852515,'130 2nd avenue':241822290,
 '97 east 7th street':248142701,'97.5 east 7th street':248142693,'135 avenue a':248142700,
}
miss=[]
for entry in observations['buildings']:
    key=norm(entry['address']);b=byid.get(manual.get(key)) or aliases.get(key) or aliases.get(first_address(key))
    if not b:miss.append(entry['address']);continue
    b['facadeSpec']=dict(entry['spec']);b['reference']={k:v for k,v in entry.items() if k!='spec'}
    if not b['address']:b['address']=entry['address']

def update(address,**spec):
    key=norm(address);b=byid.get(manual.get(key)) or aliases.get(key) or aliases.get(first_address(key))
    if b:b.setdefault('facadeSpec',{}).update(spec)
    return b

# Translate observed details into the shared component kit. Current occupancy and
# the photographed design of a sign retain separate dates in each source record.
update('122 2nd avenue',cornicePlain=True,windowRatio=.73,bands=True,ornament=0)
update('124 2nd avenue',wall='painted grey',ornament=2,escapeMat='white frame',bays=4,bayPositions=[.13,.40,.60,.87])
update('126 2nd avenue',landmark='orpheum',business='ORPHEUM THEATRE',height=10.8,floors=2,bays=3,wall='weathered red')
update('128 2nd avenue',wall='buff brick',bays=4,bayPositions=[.13,.40,.60,.87],ornament=2)
update('130 2nd avenue',wall='buff brick',floors=2,ornament=0,cornicePlain=True,windowRatio=.80,business=None,landmark='modern_bank')
update('133 2nd avenue',wall='buff brick',ornament=0,cornicePlain=True,windowRatio=.79,bands=True)
update('135 2nd avenue',landmark='ottendorfer',business='FREIE BIBLIOTHEK',wall='weathered red',height=14,floors=3,bays=3)
update('137 2nd avenue',landmark='dispensary',business=None,wall='weathered red',floors=3,bays=7)
update('138 2nd avenue',wall='warm brick',stoop=True,bays=3,ornament=1)
update('140 2nd avenue',wall='painted ivory',ornament=0,cornicePlain=True,bays=3,windowRatio=.8,bands=True,business=None)
update('144 2nd avenue',wall='painted grey',bays=1,windowRatio=.76,floors=3,ornament=2,business='VESELKA',awning='awning green',fascia='awning green')
update('166 2nd avenue',wall='buff brick',floors=15,ornament=0,cornicePlain=True,landmark='warren',business=None)
update('170 2nd avenue',wall='buff brick',floors=15,ornament=0,cornicePlain=True,landmark='stuyvesant',business=None)
update('178 2nd avenue',business='PANGEA',fascia='nishaan blue',awning='nishaan blue')
update('180 2nd avenue',wall='painted ivory',ornament=0,bands=True,cornicePlain=True)
update('184 2nd avenue',wall='painted ivory',ornament=0,cornicePlain=True)
update('186 2nd avenue',wall='warm brick',cornice='cornice green',escapeMat='red iron',stoop=True)
update('188 2nd avenue',wall='warm brick',cornice='cream stone',ornament=2,escapeMat='red iron',sideEscape=True,business=None)
update('181-189 2nd avenue',landmark='village_east',floors=3,wall='limestone facade',business='VILLAGE EAST',height=23.9)
update('131 east 10th street',landmark='st_marks_church',wall='painted grey',height=16.4,business=None)
update('288 east 10th street',landmark='st_nicholas',wall='warm brick',height=31.4,floors=3,business=None)
update('287 east 10th street',landmark='joyce',wall='painted ivory',floors=7,cornicePlain=True,ornament=0,business=None)
update('107 east 7th street',landmark='st_stanislaus',height=38,wall='limestone facade',floors=2,business=None)
update('111-115 east 7th street',wall='warm brick',escapeCenters=[.27,.73],bays=9,ornament=2,bands=True)
update('62 saint marks place',landmark='st_cyril',wall='warm brick',floors=4,business=None)
update('121 east 7th street',landmark='st_mary',wall='limestone facade',floors=3,business=None)
update('307 east 12th street',landmark='elizabeth',wall='warm brick',floors=4,business=None)
update('321 east 9th street',business='IRVING GREEN',fascia='shop sage',awning=None,frontStreet='East 9th Street')
update('318 east 9th street',business=None,fascia='wood',frontStreet='East 9th Street')
update('322 east 11th street',business='CASEY RUBBER STAMP',fascia='yellow paint',letters='black iron',frontStreet='East 11th Street')
update('268 east 10th street',business='RUSSIAN & TURKISH BATHS',fascia='cream stone',letters='black iron',stoop=True,frontStreet='East 10th Street')
update('109 avenue a',wall='limestone facade',ornament=0,cornicePlain=True,business="MISS LILY'S 7A",fascia='theater red')
update('112 avenue a',business='NIAGARA',fascia='black iron',escape=True)
update('113 avenue a',business="RAY'S CANDY STORE",fascia='shop sage',letters='theater red',profile='gelato',escape=True)
update('115 avenue a',business='MAYA',fascia='awning green',letters='sign white')
update('117 avenue a',business="ST DYMPHNA'S",fascia='gelato yellow',letters='black iron')
update('119 avenue a',business='RESTAURANT',fascia='sign white',letters='theater red',secondarySign='SUPERIORITY BURGER')
update('121 avenue a',business='LUSTER',fascia='nishaan blue')
update('135 avenue a',business="LUCY'S",fascia='black iron',letters='gelato pink',shopFraction=.52)
update('141 avenue a',business="DOC HOLLIDAY'S BAR",fascia='shop burgundy',awning='shop burgundy',wall='painted ivory')
update('145 avenue a',business="RALPH'S ITALIAN ICES",fascia='nishaan blue',wall='painted ivory',profile='gelato')
update('147 avenue a',business='BABA DONER',fascia='black iron',blade='BABA DONER',bladeColor='nishaan blue')
update('149 avenue a',business=None,fascia='shop sage',vacant=True)
update('151 avenue a',business="DANNY & COOP'S",fascia='black iron',letters='theater red',shopFraction=.52)
update('165 avenue a',business='TOMPKINS SQUARE BAGELS',fascia='shop cream',letters='shop burgundy',awning='shop burgundy',profile='bakery',bays=5)
update('169 avenue a',business="LUCINDA'S",fascia='wood',letters='gelato pink')
update('181 avenue a',landmark='steiner',wall='warm brick',ornament=0,cornicePlain=True,windowRatio=.76,escape=False,business=None)
update('170 avenue a',business='THE RABBIT',secondarySign='BOOKS AND BAR',fascia='shop burgundy',awning='shop burgundy')
update('166 avenue a',business='PEACE',fascia='sign white',letters='black iron')

known=[b for b in data['buildings'] if b.get('facadeSpec',{}).get('observed') and b['facadeSpec'].get('observationScope')=='facade']
for b in data['buildings']:
    if 'facadeSpec' not in b:
        candidates=[k for k in known if any(a['street']==f['street'] for a in b['frontages'] for f in k['frontages'])]
        near=min(candidates or known,key=lambda k:math.dist(k['center'],b['center'])) if known else None
        b['facadeSpec']={'observed':False,'wall':near['facadeSpec'].get('wall','warm brick') if near else 'warm brick','trim':'cream stone','ornament':1 if b['height']<25 else 0,'escape':b['buildingType']=='apartments' and 12<b['height']<25,'inference':'Mapped footprint and height; window spacing, finish, metalwork and entrances remain estimates.'}
    b['renderHeight']=b['facadeSpec'].get('height',b['height'])
    if b['buildingType']=='ruins':b['facadeSpec'].update(landmark='ruin',height=4,escape=False);b['renderHeight']=4
    if b['buildingType']=='school' and not b['facadeSpec'].get('landmark'):b['facadeSpec'].update(landmark='school',ornament=0,cornicePlain=True,escape=False)
    if b['id']==248142955:b['facadeSpec'].update(landmark='ps122',floors=5,ornament=2,wall='warm brick',escape=False)
    if b['id']==247852516:b['facadeSpec'].update(landmark='elizabeth_east',wall='warm brick',floors=4)
    # One front, assembled across the two parcels established by the LPC report.
    if b['id']==247852515:b['facadeSpec']['companionId']=247852516

# Revision 03: recorded architectural controls plus a map-wide detail standard.
detail_schedule=json.loads((ROOT/'model-source/neighborhood-detail-schedule.json').read_text())
for b in data['buildings']:
    if not b['core']:
        b['facadeSpec']['detail']=dict(detail_schedule['defaults'])
        b['detailRevision']=detail_schedule['revision']
for entry in detail_schedule['buildings']:
    b=update(entry['address'],**entry.get('spec',{}))
    if not b:raise ValueError('Unmatched detail schedule: '+entry['address'])
    if b['core']:continue
    b['facadeSpec']['detail'].update(entry['detail'])
    b['facadeSpec']['detail']['sourceRecord']=entry['sourceRecord']
    b['facadeSpec']['detail']['captureDate']=entry['captureDate']
facade_audit=json.loads((ROOT/'model-source/neighborhood-facade-audit.json').read_text())
for entry in facade_audit['buildings']:
    b=byid[entry['id']]
    if b['core']:continue
    spec=dict(entry['spec']); detail=spec.pop('detail',{})
    b['facadeSpec'].update(spec)
    b['facadeSpec'].setdefault('detail',{}).update(detail)
    b['architecturalReference']={k:v for k,v in entry.items() if k!='spec'}
    b['facadeSpec']['inference']=entry['limits']
for b in data['buildings']:
    if not b['core']:b['detailRevision']='04'
    b['renderHeight']=b['facadeSpec'].get('height',b['height'])
business_audit=compile_businesses(data)
street_facilities=json.loads((ROOT/'model-source/street-facilities.json').read_text())
for road in data['roads']:
    facility=next((r for r in street_facilities['streets'] if r['name']==road['name']),None)
    if facility:road['facilities']=facility
data['streetFacilitySummary']={'checked':street_facilities['checked'],'source':'model-source/street-facilities.json','scope':street_facilities['basis']}
data['detailSummary']={'revision':'04','buildings':sum(not b['core'] for b in data['buildings']),'sourceSchedule':'model-source/neighborhood-facade-audit.json','scope':'Municipal footprint inventory, individually inspected facade photographs and dated business evidence. Unseen elevations and unmeasured details remain estimated.'}

data['referenceSummary']={'checked':'2026-09-06','newObservedBuildings':sum(b['facadeSpec'].get('observed',False) for b in data['buildings'] if not b['core']),'sourceRecords':len(observations['buildings'])+len(facade_audit['buildings']),'auditedFacadeRecords':len(facade_audit['buildings']),'mappedBuildings':len(data['buildings']),'unmatchedReferences':miss,'scope':'Exterior photo-guided reconstruction. Observation dates vary; unseen elevations, exact dimensions and unresolved occupancy remain explicit estimates. No current photographic survey.'}

# Street dressing is representative. It is deliberately separate from buildings.
rng=random.Random(70912)
def solid(x,z):
    for b in data['buildings']:
        bb=b['box']
        if bb[0]-.7<x<bb[2]+.7 and bb[1]-.7<z<bb[3]+.7:return True
    return False
trees=[];benches=[];furniture=[]
for road in data['roads']:
    a,c=road['a'],road['b'];L=math.dist(a,c);dx,dz=(c[0]-a[0])/L,(c[1]-a[1])/L
    for k in range(1,int(L/27)):
        t=k*27+rng.uniform(-3,3);x,z=a[0]+dx*t,a[1]+dz*t
        if any(other is not road and (abs(x-other['a'][0])<18 if other['axis']=='avenue' else abs(z-other['a'][1])<12) for other in data['roads']):continue
        for side in [-1,1]:
            xx=x-dz*side*(road['halfWidth']+2.0);zz=z+dx*side*(road['halfWidth']+2.0)
            if abs(xx)<69 and abs(zz)<70:continue
            if not solid(xx,zz):trees.append({'x':round(xx,2),'z':round(zz,2),'angle':rng.random()*6.28,'scale':round(rng.uniform(.78,1.1),2)})
    for k in range(1,int(L/43)):
        t=k*43;x,z=a[0]+dx*t,a[1]+dz*t
        xx=x-dz*(road['halfWidth']+.65);zz=z+dx*(road['halfWidth']+.65)
        if abs(xx)<65 and abs(zz)<70:continue
        if not solid(xx,zz):furniture.append({'x':xx,'z':zz,'angle':0 if road['axis']=='avenue' else math.pi/2})
for z in range(16,220,23):
    trees.append({'x':255+rng.uniform(-4,4),'z':z,'angle':rng.random()*6.28,'scale':1.15})
    benches.append({'x':236,'z':z+4,'angle':-math.pi/2})
core=[(8.90,19,0),(8.90,25,0),(8.90,-19,0),(8.9,-26,0),(8.9,42,0),(-4.4,-24,0),(-4.4,34,0),(-23,3.65,math.pi/2),(-29,3.65,math.pi/2),(25,-3.6,-math.pi/2),(32,-3.6,-math.pi/2)]
parked=[{'x':x,'z':z,'angle':a,'core':True} for x,z,a in core]
for road in data['roads']:
    a,c=road['a'],road['b'];L=math.dist(a,c);dx,dz=(c[0]-a[0])/L,(c[1]-a[1])/L
    for k in range(1,int(L/16)):
        t=k*16+3;x,z=a[0]+dx*t,a[1]+dz*t
        if any(other is not road and (abs(x-other['a'][0])<17 if other['axis']=='avenue' else abs(z-other['a'][1])<14) for other in data['roads']):continue
        side=1 if k%2 else -1;offset=road['halfWidth']-1.65
        facility=road.get('facilities',{})
        if road['axis']=='street' and facility.get('bike')=='lane':offset=3.85
        # The accepted straightened cross street is too narrow to insert a
        # parking buffer here while retaining a usable driving lane. Omit
        # illustrative parked cars on the track side instead of blocking it.
        if road['axis']=='street' and facility.get('bike')=='track' and side==facility['side']:continue
        if road['name']=='Avenue A':offset=7.65
        if road['name']=='Second Avenue' and side==1:continue
        if road['name']=='First Avenue' and side==1:offset=4.4
        if road['name']=='Second Avenue' and side==-1:offset=4.4
        xx=x-dz*side*offset;zz=z+dx*side*offset
        if abs(xx)<69 and abs(zz)<73:continue
        parked.append({'x':round(xx,2),'z':round(zz,2),'angle':0 if road['axis']=='avenue' else math.pi/2})
# Small street objects fill the existing streets; coordinates remain estimates.
detail_groups={k:[] for k in ['bicycle-detail','hydrant','litter-bin','utility-cover','drain-grate']}
def outside_core(x,z):return not (abs(x)<72 and abs(z)<75)
def clear_intersection(x,z,road):
    return not any(other is not road and (abs(x-other['a'][0])<19 if other['axis']=='avenue' else abs(z-other['a'][1])<14) for other in data['roads'])
for road in data['roads']:
    a,c=road['a'],road['b'];L=math.dist(a,c);dx,dz=(c[0]-a[0])/L,(c[1]-a[1])/L
    angle=math.pi/2 if road['axis']=='avenue' else 0
    for kind,step,offset in [('bicycle-detail',69,road['halfWidth']+2.4),('litter-bin',61,road['halfWidth']+1.3),('hydrant',48,road['halfWidth']+.65),('drain-grate',35,road['halfWidth']-.40),('utility-cover',57,1.1)]:
        for k in range(1,int(L/step)):
            t=k*step+7;x,z=a[0]+dx*t,a[1]+dz*t
            side=1 if k%2 else -1;xx=x-dz*side*offset;zz=z+dx*side*offset
            if not outside_core(xx,zz) or not clear_intersection(x,z,road) or solid(xx,zz):continue
            detail_groups[kind].append({'x':round(xx,3),'z':round(zz,3),'angle':(math.pi/2-angle if kind=='drain-grate' else angle)})
data['detailProps']=[{'name':name.replace('-',' ').title(),'url':'neighborhood/'+name+'.glb','placements':placements} for name,placements in detail_groups.items()]
data['detailSummary']['streetObjects']=sum(len(g['placements']) for g in data['detailProps'])
data.update(trees=trees,benches=benches,furniture=furniture,parked=parked)
path.write_text(json.dumps(data,separators=(',',':')))
(ROOT/'dist/reconstruction/neighborhood-sources.json').write_text(json.dumps({**observations,'facadeAudit':facade_audit,'businessAudit':business_audit,'geographyAudit':data['geographyAudit']},indent=2))
print(json.dumps({**data['referenceSummary'],'trees':len(trees),'cars':len(parked)}))
