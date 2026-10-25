"""Four owned Ninth faces. Mapped mass; independently observed storefronts.
Relief dimensions are visual estimates; no source pixels become runtime assets.
"""
import json
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'model-source/east-village-e09-n01a'
DATA={b['id']:b for b in json.loads((ROOT/'dist/reconstruction/neighborhood.json').read_text())['buildings']}
OBS=json.loads((OUT/'observations.json').read_text());E=[];SHOPS=[]
def elevation(bid,index,address,wall,sources):
 b=DATA[bid];f=b['frontages'][index]
 a={'wall':wall,'windows':[],'doors':[],'returnShops':[],'observedGround':{'replaceWindows':False,'replaceDoors':False},'n01a':True,
 'observation':{'sources':sources,'facts':[v for k in sources for v in OBS['sources'][k]['observations']],'unknown':OBS['limits']}}
 E.append({'faceId':f'{bid}:{index}','buildingId':bid,'frontageIndex':index,'address':address,'sourceFace':deepcopy(f),'buildingHeight':b['height'],'architecture':a});return a,f

def window(a,f,s,y,w,h,frame,trim,**kw):
 a['windows'].append({'at':s/f['length'],'width':w/f['length'],'bottom':y,'height':h,'frame':frame,'trim':trim,'hood':'none','rails':[.49],**kw})
def door(a,f,s,w,bottom,top,mat):
 a['doors'].append({'at':s/f['length'],'width':w/f['length'],'bottom':bottom,'top':top,'leafTop':top-.35,'material':mat,'trim':mat,'recess':.25,'leaves':1,'hardware':'store09 aged brass','panels':[{'y':.53,'height':.79,'width':.83,'glass':True}]})
def shop(a,f,bid,index,name,business,span,kind,panels,identity,sources,**kw):
 key=f'{bid}:{index}:{len(a["returnShops"])}'
 design={'top':2.95,'head':2.65,'base':.57,'recess':.22,'transom':True,'panels':panels,'signs':[],
 'detail09':{'id':key,'frame':'n01 black timber','surround':'n01 black timber','frameWidth':.05,'pierWidth':.06,'floor':.17,'molding':True,'displayDepth':.72,'doorSolidTop':.30,'displays':[],'furniture':[],'identity':identity,'sourceIds':sources},'detailN01A':{'kind':kind},**kw}
 a['returnShops'].append({'name':name,'span':span,'design':design})
 SHOPS.append({'id':key,'businessId':business,'faceId':f'{bid}:{index}','name':name,'span':span,'component':kind,'identity':identity,'sourceIds':sources,'reviewState':'authored; served review separately','unknown':['Dated external appearance; relief, lettering, artwork and shallow display details are estimates. Deep interiors unobserved.']})
 return design

a,f=elevation(247852691,1,'147 First Avenue — Ninth-facing return','painted n01 sky',['corner-historic','corner-may','market-may','hotel-realty-may'])
for row,y in enumerate([4.36,6.92,9.45]):
 for col,s in enumerate([1.65,4.02,6.37,8.94,11.72,14.34,19.08]):window(a,f,s,y,1.30,1.75,'n01 black metal','n01 black metal',n01Multipane=True)
shop(a,f,247852691,1,'East Village Hotel — EVH entrance','east-village-hotel',[.01,.19],'hotel',[['door',.25],['glass',.75]],'Separate narrow black hotel leaf and broad blue curtained EVH window; small number at entry.', ['hotel-realty-may','corner-historic'],transom=False,base=.28,top=3.16,head=3.06)
shop(a,f,247852691,1,'Sweet Village Market Place — Ninth return','sweet-village-market',[.198,.988],'market',[['glass',.13],['glass',.13],['glass',.11],['glass',.20],['glass',.18],['glass',.25]],'Six unequal food/display fields, dark decorated piers, separate east MARKET PLACE fascia and oval Sweet Village mark; no Ninth awning.', ['market-may','corner-may'],top=3.28,head=3.10,base=.18,transom=False)

a,f=elevation(247852690,0,'345 East Ninth Street','n01 realty red brick',['realty-architecture','realty-residential-access','hotel-realty-may','ninth-oblique-september'])
for row,y in enumerate([3.66,6.10,8.47]):
 for col,at in enumerate([.13,.375,.625,.88]):window(a,f,f['length']*at,y,1.10,1.68,'n01 dark sash','n01 cream stone',n01Head='rect',n01Vent=col in [0,3],ac=(row,col) in [(0,0),(1,3),(2,1)])
door(a,f,7.97,.94,.43,3.17,'n01 brown timber')
spec=shop(a,f,247852690,0,'Universal Realty Group','universal-realty',[.018,.84],'realty',[['door',.17],['glass',.33],['glass',.20],['glass',.30]],'Navy inclined fabric canopy with large white serif identity and small services strip; taupe metal glazing, listing sheets, raised ramp and slim rail.', ['realty-architecture','realty-residential-access','hotel-realty-may'],top=2.82,head=2.65,base=.55,transom=False)
spec['detail09'].update(frame='n01 taupe metal',surround='n01 taupe metal',floor=.43,molding=False)

a,f=elevation(247852697,0,'343 East Ninth Street','n01 residential red brick',['ninth-upper-september','realty-residential-access','immigrant-access-historic'])
for row,y in enumerate([1.89,4.50,7.08,9.65]):
 for col,at in enumerate([.18,.51,.84]):window(a,f,f['length']*at,y,1.28,1.96,'n01 white sash','n01 cream stone',columns=2,rails=[],n01Head='rect',ac=(row,col)==(3,1))
for at in [.51,.84]:window(a,f,f['length']*at,.03,1.05,.91,'n01 black metal','n01 cream stone',grille=True,rails=[])
door(a,f,f['length']*.17,1.19,-.25,1.66,'n01 black metal')
a['observedGround']['basementAreaways']=[{'at':.50,'width':.95,'depth':.87,'depthBelow':.43}]

a,f=elevation(247852689,0,'341 East Ninth Street','n01 immigrant red brick',['ninth-upper-september','immigrant-current','immigrant-access-historic'])
for row,y in enumerate([3.98,6.75,9.52,12.24]):
 for col,at in enumerate([.115,.35,.65,.885]):window(a,f,f['length']*at,y,.95,1.97 if row<3 else 1.76,'n01 dark sash','n01 olive stone',n01Head='arch',ac=(row,col) in [(0,0),(0,3),(1,3),(2,0),(2,3),(3,3)])
 if row>0:window(a,f,f['length']*.50,y+.20,.34,1.16,'n01 rust iron','n01 olive stone',rails=[],n01Narrow=True)
door(a,f,f['length']*.50,.77,.51,2.93,'n01 brown timber')
shop(a,f,247852689,0,'The Immigrant — Tap Room','the-immigrant',[.016,.433],'tap',[['glass',.69],['door',.31]],'Gold arched Tap Room lettering in broad west pane, separate narrow door, navy panels and independent small shades.', ['immigrant-current','immigrant-access-historic'],top=2.99,head=2.68,base=.72,transom=False)
s=shop(a,f,247852689,0,'The Immigrant — Wine Bar','the-immigrant',[.571,.985],'wine',[['door',.30],['glass',.70]],'Warm timber door then broad gold-lettered Wine Bar pane with shallow bottle display; separate from Tap Room and central 341 entry.', ['immigrant-current','immigrant-access-historic'],top=2.99,head=2.68,base=.72,transom=False)
s['detail09'].update(frame='n01 brown timber')
result={'schema':1,'id':'01-E09-21-N01A','parent':'01-E09-21','splitParent':'01-E09-21-N01','revision':'N01A-01','scopeFaces':[r['faceId'] for r in E],'elevations':E,'businesses':SHOPS,'uniqueBusinesses':4,'junctions':[{'pair':[a,b],'condition':'Mapped touching party wall, no inferred through-alley; independent cornice/roof height and surface.', 'protectedOrDeferredNeighbor':b==247852687} for a,b in [(247852691,247852690),(247852690,247852697),(247852697,247852689),(247852689,247852687)]],'ownership':'Four Ninth faces. 147 First-facing facade stays plain context; no 339 or south-side Ninth detail.','sourceLedger':'model-source/east-village-e09-n01a/observations.json','targetCapture':'2024 primary with 2017 access supplements; not current survey','counts':{'upperOpenings':64,'basementWindows':2,'shopfronts':5,'uniqueBusinesses':4,'separateResidentialEntries':3}}
assert sum(len(r['architecture']['windows']) for r in E)==66
(OUT/'schedule.json').write_text(json.dumps(result,indent=2)+'\n')
print('N01A: four faces, 64 upper openings / 2 basement windows, five distinct shopfronts, four businesses')
