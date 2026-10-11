"""Author the bounded revision 08 schedule from the October browser ledger.

This is a reproducible, manually transcribed work packet, not an acquisition
pipeline. Heights, recesses and fractions are visual estimates anchored to
mapped widths; obscured upper counts remain explicitly inferred.
"""
import json
import math
from pathlib import Path
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[1]
LEDGER=json.loads((ROOT/'model-source/first-stmarks-browser-08.json').read_text())
EVIDENCE={r['faceId']:r for r in LEDGER['faces']}
MAP={b['id']:b for b in json.loads((ROOT/'dist/reconstruction/neighborhood.json').read_text())['buildings']}
PATH=ROOT/'model-source/storefront-details.json'
DATA=json.loads(PATH.read_text())
# Preserve later bounded units when reproducing this First Avenue packet.
SCHEDULE=DATA.setdefault('firstStmarksEngine',{'schema':1,'revision':'08','elevations':[]})
SCHEDULE.update(scopeInventory='model-source/first-stmarks-scope-08.json',observationLedger='model-source/first-stmarks-browser-08.json',status='First Avenue bounded unit; St. Marks units pending',dimensionPolicy='Mapped footprint widths; heights, depths, coordinates and relief are authored visual estimates, not measured geometry.')
RECORDS={r['faceId']:r for r in SCHEDULE['elevations']}

def elevation(face,h,rows,bays,wall,trim,hood='flat',cornice='bracketed',escape=False,ground=4.1,spacing=2.85,window_h=1.85):
    bid,index=map(int,face.split(':'));f=MAP[bid]['frontages'][index];ev=EVIDENCE[face]
    if not ev['observations']:raise ValueError('Missing inspection '+face)
    r={'wall':wall,'observedGround':{'replaceWindows':False,'replaceDoors':False},'windows':[], 'doors':[], 'returnShops':[], 'signs':[], 'observation':{'sources':ev['sources'],'facts':ev['observations'],'unknown':ev['unknown'],'dimensions':'Visual estimates from mapped width and observed floor/entry ratios.'}}
    positions=[.15+j*.70/(bays-1) for j in range(bays)] if bays>1 else [.5]
    if bays==4:positions=[.12,.365,.635,.88]
    for row in range(rows):
        for at in positions:r['windows'].append({'at':at,'width':min(1.10/f['length'],.58/bays),'bottom':round(ground+row*spacing,3),'height':window_h,'trim':trim,'frame':'black iron','hood':hood,'rails':[.5]})
    if cornice:r['cornice']={'profile':cornice,'material':trim,'y':h}
    if escape:r['escapes']=[{'at':.50,'width':.51,'levels':[round(ground-.14+j*spacing,3) for j in range(rows)],'material':'black iron'}]
    RECORDS[face]={'faceId':face,'buildingId':bid,'frontageIndex':index,'address':MAP[bid]['address'],'sourceFace':deepcopy(f),'buildingHeight':h,'architecture':r,'reviewState':'not yet exported/reviewed'}
    return r

def door(r,at,width=.14,mat='black iron',number=None):
    d={'at':at,'width':width,'bottom':.20,'top':2.90,'material':mat,'trim':mat,'leaves':1,'leafTop':2.37,'recess':.19,'panels':[{'y':.63,'height':.56,'width':.76,'glass':True},{'y':.18,'height':.19,'width':.76}]}
    if number:d.update(label=number,labelY=2.66,labelSize=.17,labelMaterial='seventh brass lettering')
    r['doors'].append(d);return d

def sign(text,material='black iron',letters='sign white',**kw):
    return {'at':.5,'width':1,'y':3.08,'height':.52,'depth':.23,'material':material,'lines':[{'text':text,'material':letters,'size':.28}],**kw}

def shop(r,span,panels,frame='black iron',text=None,fascia=None,letters='sign white',**kw):
    d={'top':3.36,'head':2.63,'base':.34,'frame':frame,'surround':frame,'recess':.19,'panels':panels,'signs':[]}
    d.update(kw)
    if text:d['signs'].append(sign(text,fascia or frame,letters))
    r['returnShops'].append({'name':text or '', 'span':span,'design':d});return d

def scaffold(r,h,board,net=True):
    r['observedGround']['scaffold']=[{'datedShed':True,'at':0,'to':1,'canopyY':3.50,'depth':1.6,'levels':[3.5]+[round(y,2) for y in [6.7,9.9,13.1,16.3,19.5] if y<h]+([h] if h>3.5 else []),'net':net,'material':'metal','board':board}]

red='first warm red brick';pale='seventh pale limestone';olive='first olive trim'
# West side, south to north. Obscured scaffolded counts use the mapped floor
# envelope as an estimate; their April construction silhouette is observed.
r=elevation('241822212:0',13.7,3,3,red,'first mustard paint',ground=4.4,spacing=2.9)
r['escapes']=[{'at':.5,'width':.48,'levels':[4.22,7.12,10.02],'material':'first maroon paint'}]
shop(r,[.03,.79],[['glass',.54],['door',.24],['glass',.22]],'first maroon paint',None)
door(r,.90,.15,'first maroon paint')
r['signs'].append({'at':.40,'width':.34,'y':3.23,'height':.67,'shape':'oval','material':'first mustard paint','lines':[]})
for y in [6.62,9.52,12.42]:
 for at in [.15,.5,.85]:r.setdefault('ornaments',[]).append({'type':'panel','at':at,'y':y,'width':.17,'height':.26,'material':'first mustard paint'})
r=elevation('241822295:0',17.1,4,3,red,'seventh weathered limestone',escape=True,ground=4.35,spacing=2.85)
shop(r,[.03,.80],[['glass',.39],['door',.25],['glass',.36]],'white frame')
door(r,.90,.14,'black iron');scaffold(r,17.1,'119 1 AVE')
r['observation']['inferredUpperEnvelope']='Four rows/three bays behind net are a mapped-envelope estimate; source does not establish a complete opening count.'
r=elevation('241822247:0',13.45,3,3,red,olive,ground=4.35,spacing=2.8)
for w in r['windows']:
 if w['bottom']==4.35:w['hood']='pediment'
d=shop(r,[.025,.81],[['glass',.33],['glass',.33],['door',.34]],'white frame',"COSMO'S LAUNDERAMA",'first teal paint')
d['signs'][0]['lines'][0]['size']=.25
door(r,.90,.145,'first teal paint');r['signs'].append(sign('121','first teal paint',at=.90,width=.16,y=3.08))
r=elevation('241822288:0',13.45,3,3,red,olive,ground=4.35,spacing=2.8)
for w in r['windows']:
 if w['bottom']==4.35:w['hood']='pediment'
d=shop(r,[.025,.81],[['glass',.70],['door',.30]],'white frame',"COMPTON'S",'sign white','first maroon paint')
d['signs'][0]['lines'].append({'text':'SANDWICH SHOP','y':-.32,'size':.09,'material':'first maroon paint'})
door(r,.90,.14,'white frame');r['signs'].append(sign('123','first olive trim',at=.91,width=.14,y=3.09,height=.30,shape='oval'))
r=elevation('241822228:0',17.1,4,3,red,pale,escape=True,ground=4.35,spacing=2.85)
shop(r,[.02,.79],[['glass',.37],['door',.24],['glass',.39]],'white frame','nudibranch','black iron')
door(r,.90,.14,'white frame');scaffold(r,17.1,'125 1st AVE')
r['observation']['inferredUpperEnvelope']='Four rows/three bays behind net are a mapped-envelope estimate.'
r=elevation('241822263:0',17.1,4,4,red,pale,escape=True,ground=4.35,spacing=2.85)
shop(r,[.025,.70],[['glass',.44],['door',.23],['glass',.33]],'white frame')
door(r,.77,.11,'white frame');r['closedShutters']=[{'span':[.855,.99],'top':2.85}];scaffold(r,17.1,'127 1st AVE')
r['observation']['inferredUpperEnvelope']='Four rows/four bays behind net are a mapped-envelope estimate.'
r=elevation('241822220:0',16.25,4,4,'first pale buff brick',pale,cornice='parapet',escape=True,ground=4.05,spacing=2.75,window_h=1.70)
shop(r,[.025,.45],[['glass',.62],['door',.38]],'white frame',"LULU'S NAILS",'seventh grey painted stone')
door(r,.51,.10,'black iron');shop(r,[.58,.98],[['door',.34],['glass',.66]],'black iron','AT&T','black iron')
scaffold(r,3.5,'129 1st AVE',False)
r=elevation('241822308:1',3.8,0,0,red,red,cornice='parapet')
r['closedShutters']=[{'span':[.025,.96],'top':3.0,'material':'seventh charcoal gray paint'}]
r=elevation('241822308:0',3.8,0,0,red,red,cornice='parapet')
shop(r,[.025,.38],[['glass',.5],['glass',.5]],'black iron',top=3.12,head=2.88,transom=False)
shop(r,[.395,.74],[['door',.24],['glass',.76]],'seventh charcoal gray paint',top=3.12,head=2.88,transom=False)
shop(r,[.755,.985],[['glass',.59],['door',.41]],'black iron','COFFEE','black iron',top=3.12,head=2.5)
# East side: observed four-row elevations, with independent shop/residential
# entrances. No unsupported MaLa lettering or random storefront decorations.
r=elevation('248142642:0',17.0,4,4,'first pale buff brick',olive,escape=True,ground=4.1,spacing=2.85)
shop(r,[.025,.44],[['glass',.70],['door',.30]],'first maroon paint')
door(r,.51,.11,'black iron');shop(r,[.60,.98],[['door',.30],['glass',.70]],'first maroon paint')
r=elevation('248142646:0',16.6,4,4,'first pink stucco',pale,cornice='parapet',ground=4.10,spacing=2.80)
shop(r,[.025,.79],[['glass',.38],['glass',.37],['door',.25]],'first maroon paint',awning={'material':'first maroon paint','text':'EAST VILLAGE ORGANIC','y':3.40,'drop':.42,'depth':1.12,'valance':.28,'textSize':.22})
door(r,.90,.14,'seventh oak recess')
r=elevation('248142648:0',16.65,4,3,red,pale,cornice='parapet',ground=4.15,spacing=2.78)
shop(r,[.025,.80],[['glass',.33],['glass',.33],['door',.34]],olive,'THE GRAFTON',olive,'sign white')
door(r,.91,.14,olive)
r=elevation('248142651:0',17.1,4,4,red,olive,'bracketed',escape=True,ground=4.25,spacing=2.85)
shop(r,[.025,.79],[['glass',.71],['door',.29]],'black iron',awning={'material':'black iron','text':'noreetuh','y':3.38,'drop':.43,'depth':.85,'textSize':.23,'textAt':.27})
r['closedShutters']=[{'span':[.84,.985],'top':2.89}]
r['signs'].append({'at':.75,'width':.12,'y':2.84,'height':.25,'depth':1.01,'panel':False,'lines':[{'text':'128','size':.15}]})
r=elevation('248142654:0',17.1,4,4,red,'seventh dark sandstone',escape=True,ground=4.25,spacing=2.85)
shop(r,[.025,.44],[['glass',.60],['door',.40]],'first teal paint','UTSHOB', 'first teal paint')
door(r,.51,.105,'black iron','130')
d=shop(r,[.585,.985],[['door',.35],['glass',.65]],'white frame','KOLACHI','sign white','black iron')
d['windowText']=[{'at':.70,'y':1.78,'width':.58,'text':'PAKISTANI','size':.10},{'at':.70,'y':1.61,'width':.64,'text':'STREET(ISH) FOOD','size':.085}]
r=elevation('248142712:0',17.1,4,3,red,'seventh dark sandstone',ground=4.20,spacing=2.87)
shop(r,[.025,.98],[['glass',.31],['glass',.31],['door',.38]],'white frame',smallPanes=True,awning={'material':'seventh cloth pale','stripe':'black iron','stripeSpacing':.25,'stripeWidth':.09,'y':3.60,'drop':.43,'depth':1.0})
r=elevation('248142712:1',17.1,0,0,red,'seventh dark sandstone')
for row in range(4):
 for at in [.11,.48,.61]:r['windows'].append({'at':at,'width':.067,'bottom':4.20+row*2.87,'height':1.85,'trim':pale,'frame':'white frame','hood':'flat','rails':[.5]})
r['escapes']=[{'at':.545,'width':.27,'levels':[4.06,6.93,9.80,12.67],'material':'black iron'}]
for at in [.31,.81]:r.setdefault('piers',[]).append({'at':at,'width':.045,'bottom':3.6,'top':16.45,'material':red})
shop(r,[.025,.28],[['glass',.55],['door',.45]],'seventh warm plaster')
shop(r,[.30,.98],[['glass',.19],['glass',.19],['glass',.19],['glass',.19],['door',.24]],'white frame',smallPanes=True,awning={'material':'seventh cloth pale','stripe':'black iron','stripeSpacing':.25,'stripeWidth':.09,'y':3.60,'drop':.43,'depth':1.0})
# Source-to-game repairs from the first actual browser elevation review.
def architecture(face):return RECORDS[face]['architecture']
def box_detail(r,at,y,w,h,mat,depth=.20,thickness=.025):
    r.setdefault('detailBoxes',[]).append({'at':at,'y':y,'width':w,'height':h,'material':mat,'depth':depth,'thickness':thickness})
def circle(r,at,y,radius,mat,depth=.22):
    record=next(v for v in RECORDS.values() if v['architecture'] is r)
    length=record['sourceFace']['length']
    for j in range(20):
        a=j*math.tau/20;b=(j+1)*math.tau/20
        r.setdefault('detailFaces',[]).append({'material':mat,'vertices':[[at,y,depth],[at+math.cos(a)*radius/length,y+math.sin(a)*radius,depth],[at+math.cos(b)*radius/length,y+math.sin(b)*radius,depth]]})
r=architecture('241822212:0')
r['cornice']={'profile':'plain','material':red,'y':13.7};r['ornaments']=[]
for w in r['windows']:w['trim']='first brown molding'
r['signs']=[];r['bands']=[{'y':3.05,'height':.065,'depth':.20,'material':'first mustard paint'},{'y':3.57,'height':.065,'depth':.20,'material':'first mustard paint'}]
box_detail(r,.50,3.30,6.0,.48,'first maroon paint',.09,.14)
for at in [.06+j*.088 for j in range(11)]:circle(r,at,3.30,.13,'first mustard paint')
for row in range(3):
 for at in [.15,.5,.85]:
  for col in range(7):
   for rr in range(3):
    if (col+rr)%2==0:box_detail(r,at+(col-3)*.026,4.20+row*2.9-.42+rr*.11,.15,.10,'first mustard paint',.025,.012)
r['returnShops'][0]['design'].update(panels=[['door',.21],['glass',.39],['glass',.40]],top=3.02)
for at in [.30,.38,.46,.55,.64,.72]:
 box_detail(r,at,1.82,.20,1.30,'first maroon paint' if at<.5 else 'first mustard paint',-.30,.045)
for j in range(12):box_detail(r,.29+j*.038,.70,.18,.18,'first mustard paint' if j%2 else 'theater red',-.12,.05)
for key in ['241822247:0','241822288:0']:
 r=architecture(key);r['cornice']['material']='first brown molding'
 for w in r['windows']:w.update(trim='first brown molding',moldedHood=True,lowerMullion=True,rails=[.74])
 d=r['returnShops'][0]['design'];d['signs'][0]['lines'][0]['size']=.36
 # Window notices/products are deliberately simple authored objects; no
 # photographic pixels or invented detailed interior are reproduced.
 if key=='241822247:0':
  d['signs'][0]['lines'].append({'text':'SELF SERVICE   DROP OFF SERVICE','size':.09,'y':-.32})
  r['doors'][0]['material']='white frame';r['doors'][0]['trim']='white frame'
  for at,y,w,h,mat in [(.15,1.3,.4,.55,'first teal paint'),(.30,1.65,.5,.70,'sign white'),(.55,1.45,.32,.62,'first mustard paint'),(.69,1.85,.27,.50,'sign white')]:box_detail(r,at,y,w,h,mat,-.05)
 else:
  d['signs'][0]['lines'][1].update(y=-.36,size=.13)
  for row in range(9):
   for col in range(3):box_detail(r,.72+col*.018,.55+row*.22,.08,.16,['theater red','first teal paint','first mustard paint'][col],-.10)
  d['benches']=[{'at':.25,'depth':.78,'width':1.45,'material':'theater red'}]
for key in ['241822295:0','241822228:0','241822263:0']:
 r=architecture(key);r['scaffoldGuards']=[{'bottom':3.50,'top':17.1,'depth':1.60,'veil':True}]
 if key in ['241822295:0','241822228:0']:r['scaffoldGuards'][0]['angledSide']=1 if key=='241822295:0' else 0
 if key=='241822295:0':
  r['returnShops'][0]['design']['doorMaterial']='east7 navy paint'
  box_detail(r,.27,1.65,2.65,2.35,'east7 plywood',.07,.045)
 if key=='241822228:0':
  r['returnShops'][0]['design']['signs']=[]
  r['signs']=[sign('nudibranch','black iron',at=.48,width=.25,y=2.91,height=.32)]
r=architecture('241822220:0');r['returnShops'][0]['design']['signs'][0]['lines'][0]['text']='NAILS'
r['observedGround']['scaffold'][0].pop('board',None)
for w in r['windows']:
 if w['bottom']==4.05:w['height']=1.0
r=architecture('248142646:0');d=r['returnShops'][0]['design'];aw=d.pop('awning');aw.update(span=[.01,.99],textSize=.29)
r['awnings']=[aw];r['doors'][0].update(material='seventh charcoal gray paint',trim='seventh charcoal gray paint')
d['windowText']=[{'text':'East Village','at':.59,'y':2.05,'width':.45,'size':.14,'material':'first mustard paint'},{'text':'Organic','at':.59,'y':1.84,'width':.45,'size':.16,'material':'first mustard paint'}]
r['displayBottles']=[{'at':.08+j*.019,'bottom':.88,'depth':.26} for j in range(16)]
box_detail(r,.26,.85,3.05,.10,'sign white',.18,.40)
r=architecture('248142648:0');d=r['returnShops'][0]['design']
d.update(frame='white frame',surround='white frame',doorMaterial='black iron',panels=[['glass',.235],['glass',.235],['glass',.235],['door',.295]])
d['signs'][0]['lines'][0].update(text='THE GRAFTON',size=.36)
d['signs'][0]['lines'].append({'text':'Public house','offset':.34,'y':-.20,'width':.23,'size':.08})
r['doors'][0].update(material='white frame',trim='white frame')
r['shopBlinds']=[{'at':at,'width':.125,'bottom':.53,'height':1.73} for at in [.145,.310,.475]]
r=architecture('248142651:0');r['escapes'][0]['material']=olive
r['returnShops'][0]['design']['awning'].update(textAt=.48,textSize=.17)
r=architecture('248142642:0');r['escapes'][0]['material']='first brown molding'
r['doors'][0].update(material='seventh oak recess',trim='black iron')
r=architecture('248142654:0');r['returnShops'][0]['design']['signs'][0]['lines'][0].update(text='UTSHOB RESTAURANT',size=.19)
# Full-block comparison caught an over-tall scaffolded envelope in the first
# candidate. Keep the original four-floor (three upper rows) mapped estimate
# where the mesh conceals the count; do not mistake floors for upper rows.
for key,height,spacing,net_top in [('241822295:0',13.4,2.80,14.2),('241822228:0',14.4,3.10,15.2),('241822263:0',14.4,3.10,15.2)]:
 r=architecture(key);RECORDS[key]['buildingHeight']=height
 bays=3 if key!='241822263:0' else 4
 r['windows']=r['windows'][:3*bays]
 for j,w in enumerate(r['windows']):w['bottom']=4.35+(j//bays)*spacing
 r['cornice']['y']=height;r['escapes'][0]['levels']=[4.21+j*spacing for j in range(3)]
 r['observedGround']['scaffold'][0]['levels']=[3.5,6.6,9.7,12.8,net_top]
 r['scaffoldGuards'][0]['top']=net_top
 r['observation']['inferredUpperEnvelope']='Three upper rows retained from the original four-floor mapped envelope behind net; exact hidden bays/trim remain uncertain. Height and scaffold overrun estimated from neighboring rooflines.'
RECORDS['241822212:0']['buildingHeight']=13.15;architecture('241822212:0')['cornice']['y']=13.15
SCHEDULE['elevations']=sorted(RECORDS.values(),key=lambda r:r['faceId'])
PATH.write_text(json.dumps(DATA,ensure_ascii=False,indent=2)+'\n')
print('FIRST_STMARKS_AUTHORED',len(SCHEDULE['elevations']),'faces; heights/depths are visual estimates')
