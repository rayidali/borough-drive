"""145 First Avenue / 352 East Ninth: explicit two-face corner, dated evidence.
Footprint and height are mapped; all relief and feature dimensions are estimates.
"""
import json
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'model-source/east-village-p03'
B=next(b for b in json.loads((ROOT/'dist/reconstruction/neighborhood.json').read_text())['buildings'] if b['id']==241822237)
OBS=json.loads((OUT/'observations.json').read_text());RECORDS=[];SHOPS=[]
def elevation(index,positions):
 f=B['frontages'][index];sources=['first-upper-2024','first-businesses-september','south-context-april'] if index==1 else ['ninth-complete-historic','pizza-corner-may','ninth-sidewalk-may','corner-depth-2022']
 a={'wall':'p03 red brick','windows':[],'doors':[],'returnShops':[],'signs':[],
 'observedGround':{'replaceWindows':False,'replaceDoors':False},'p03Face':index,
 'observation':{'sources':sources,'facts':[v for k in sources for v in OBS['sources'][k]['observations']],
 'unknown':['Mapped mass, visual ratios and estimated relief dimensions; no calibrated acceptance.',
 'Dated 2024 primary views, April 2026 context and explicit older Ninth geometry supplements; not verified unchanged October 2026.',
 'Hidden rear/roof equipment and deep interiors unobserved.']}}
 for row,y in enumerate([4.26,6.81,9.53,12.24]):
  for col,s in enumerate(positions):
   a['windows'].append({'at':s/f['length'],'width':1.02/f['length'],'bottom':y,'height':1.66 if row==0 else 1.84 if row<3 else 1.77,
    'trim':'p03 pale stone' if row==0 and index==1 else 'p03 green metal','frame':'p03 pale sash','hood':'none','rails':[.49],
    'p03Pediment':row==0,'ac':(row,col) in ({(0,0),(0,2),(1,1),(1,2),(2,0),(3,0)} if index==1 else {(0,0),(1,1),(2,0),(2,1),(3,1)})})
 if index==0:
  for s,w in [(14.35,1.00),(17.02,.43)]:a['windows'].append({'at':s/f['length'],'width':w/f['length'],'bottom':4.05,'height':1.51,'trim':'p03 pale stone','frame':'p03 olive sash','hood':'flat','rails':[.48],'p03Plain':True})
  a['doors']=[{'at':18.79/f['length'],'width':1.17/f['length'],'bottom':.25,'top':3.23,'leafTop':2.64,
    'material':'store09 black enamel','trim':'store09 black enamel','leaves':1,'recess':.25,'hardware':'store09 brushed steel',
    'panels':[{'y':.52,'height':.80,'width':.86,'glass':True}]}]
 r={'faceId':f'241822237:{index}','buildingId':241822237,'frontageIndex':index,
 'address':'145 First Avenue' if index==1 else '352 East 9th Street / 145 First Avenue return',
 'sourceFace':deepcopy(f),'buildingHeight':B['height'],'architecture':a};RECORDS.append(r);return a
def shop(a,name,index,span,panels,kind,identity,sources):
 n=len(a['returnShops']);key=f'241822237:{index}:{n}'
 spec={'top':3.27,'head':2.67,'base':.72,'recess':.32,'transom':True,'panels':panels,'signs':[],
 'detail09':{'id':key,'frame':'store09 black enamel','surround':'store09 black enamel','frameWidth':.05,'pierWidth':.065,
 'floor':.16,'molding':False,'displayDepth':1.25,'doorSolidTop':.25,'recessedBase':False,'displays':[],'furniture':[],
 'identity':identity,'sourceIds':sources},'detailP03':{'kind':kind}}
 if kind=='baji':spec.update(top=3.20,head=2.88,base=.40,transom=False,recess=.52)
 a['returnShops'].append({'name':name,'span':span,'design':spec})
 SHOPS.append({'id':key,'businessId':'baji-baji' if kind=='baji' else 'east-village-pizza','faceId':f'241822237:{index}',
 'name':name,'span':span,'identity':identity,'sourceIds':sources,'component':kind,
 'reviewState':'authored; final served review recorded separately',
 'unknown':['Proprietary lettering, murals and sticker artwork are hand-built approximations; illegible source copy is not invented.',
 'Furniture and notices represent dated source appearance; interiors beyond visible shallow display cues are unknown.']})
 return spec
a=elevation(1,[.88,2.81,4.71,6.63])
shop(a,'Baji Baji',1,[.014,.483],[['glass',.60],['door',.40]],'baji',
 'Dark boarded fascia, small 145 and phone, boxed salmon BAJI / BAJI at right; broad yellow-circle display, sticker-covered black surround and deeper narrow right entry; no cloth canopy.', ['first-businesses-september','south-context-april'])
shop(a,'East Village Pizza — First Avenue entrance',1,[.493,.986],[['glass',.70],['door',.30]],'pizza-first',
 'Green fixed fascia plus separate retractable shade/valance, white compressed lettering and goosenecks; black display and corner leaf, layered riser graffiti and turquoise tower-painted corner pier.', ['first-businesses-september','pizza-corner-may'])
a=elevation(0,[7.55,10.60])
shop(a,'East Village Pizza — Ninth Street return',0,[.006,.548],[['glass',.33],['glass',.34],['glass',.33]],'pizza-ninth',
 'Long independent green retractable awning, white curved lamps, three large black display bays, round multicolor neon, heart pizza and slice neon, gold skyline lower panels; square wood standing tables and dark/red backless stools.', ['pizza-corner-may','ninth-sidewalk-may','ninth-complete-historic'])
schedule={'schema':1,'id':'P03','parent':'01-FA08W','revision':'P03-01','scopeFaces':[r['faceId'] for r in RECORDS],
 'elevations':RECORDS,'businesses':SHOPS,'uniqueBusinesses':2,
 'junctions':[{'neighbor':241822211,'face':'First Avenue south','condition':'Touching party wall; separate brown 143 escape/cornice and green 145 cornice. Mapped 12mm street-plane difference retained.','protectedNeighbor':True,'sourceIds':['first-upper-2024','south-context-april']},
 {'neighbor':241822239,'face':'Ninth west','condition':'Municipal footprint touches at x=-34.753; imagery shows next building recessed with exposed pale side wall. Do not invent a through-alley or alter the deferred neighbor. P03 ends at mapped owned boundary.','sourceIds':['west-return-historic','ninth-complete-historic'],'deferredNeighbor':True}],
 'ownership':'One new mass and exactly two complete faces; no 148 Ninth return or other Ninth buildings. Narrow west Ninth viewing/driving stub only.',
 'targetCapture':'2024 storefront detail with April 2026 context and explicit 2017/2022 architectural supplements',
 'sourceLedger':'model-source/east-village-p03/observations.json'}
assert sum(len(r['architecture']['windows']) for r in RECORDS)==26
(OUT/'schedule.json').write_text(json.dumps(schedule,indent=2)+'\n')
print('P03: 1 mass, 2 faces, 26 upper openings, 2 businesses / 3 shopfronts and 1 separate residential entry')
