"""N01B: 339–333 East Ninth. Four owned faces; six separately observed shopfronts."""
import json
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'model-source/east-village-e09-n01b'
DATA={b['id']:b for b in json.loads((ROOT/'dist/reconstruction/neighborhood.json').read_text())['buildings']}
OBS=json.loads((OUT/'observations.json').read_text());E=[];SHOPS=[]
def elevation(bid,address,wall,sources,height=None):
 b=DATA[bid];f=b['frontages'][0]
 a={'wall':wall,'windows':[],'doors':[],'returnShops':[],'observedGround':{'replaceWindows':False,'replaceDoors':False},'n01b':True,'observation':{'sources':sources,'facts':[v for k in sources for v in OBS['sources'][k]['observations']],'unknown':OBS['limits']}}
 E.append({'faceId':f'{bid}:0','buildingId':bid,'frontageIndex':0,'address':address,'sourceFace':deepcopy(f),'buildingHeight':height or b['height'],'sourceHeight':b['height'],'architecture':a});return a,f

def win(a,f,at,y,w,h,**kw):
 a['windows'].append({'at':at,'width':w/f['length'],'bottom':y,'height':h,'frame':'nb dark sash','trim':'nb sandstone','hood':'none','rails':[.49],**kw})
def door(a,f,at,w,low,top,mat='nb black timber',recess=.24):
 a['doors'].append({'at':at,'width':w/f['length'],'bottom':low,'top':top,'leafTop':top-.42,'material':mat,'trim':mat,'recess':recess,'leaves':1,'hardware':'store09 aged brass','panels':[{'y':.64,'height':.55,'width':.76,'glass':True},{'y':.17,'height':.17,'width':.76}]})
def shop(a,f,bid,name,span,kind,panels,identity,sources,**kw):
 key=f'{bid}:0:{len(a["returnShops"])}';d={'top':3.08,'head':2.81,'base':.39,'recess':.20,'transom':False,'panels':panels,'signs':[], 'detail09':{'id':key,'frame':'nb black timber','surround':'nb black timber','frameWidth':.045,'pierWidth':.07,'floor':.17,'molding':True,'displayDepth':.94,'doorSolidTop':.24,'displays':[],'furniture':[],'identity':identity,'sourceIds':sources},'detailN01B':{'kind':kind},**kw}
 a['returnShops'].append({'name':name,'span':span,'design':d});SHOPS.append({'id':key,'businessId':kind,'faceId':f'{bid}:0','name':name,'span':span,'identity':identity,'sourceIds':sources,'component':kind,'reviewState':'authored; final review separately','identityStatus':'tenant unresolved; physical frontage observed' if kind=='west333' else 'dated source-supported identity','unknown':OBS['limits']});return d

a,f=elevation(247852687,'339 East Ninth Street','nb residential brick',['339-all','339-upper','339-access','337-oblique'])
for row,y in enumerate([2.58,5.24,8.02,10.80,13.58]):
 for col,at in enumerate([.15,.42,.58,.84]):
  win(a,f,at,y,.94 if col in [1,2] else 1.20,1.91 if row else 1.94,trim='nb cream band',ac=(row,col) in [(0,1),(0,2),(1,3),(2,0),(2,3),(3,0),(4,3)],grille=row==0 and col==3)
for at in [.15,.49]:win(a,f,at,-.27,1.13,1.59,trim='nb residential brick',grille=True)
door(a,f,.84,1.01,-.22,1.81,'nb ochre door',.24)
a['doors'][0].update(leafTop=1.75,panels=[{'y':.73,'height':.28,'width':.65,'glass':True}])
a['observedGround']['basementAreaways']=[{'at':.49,'width':.96,'depth':.95,'depthBelow':.52}]

a,f=elevation(247852686,'337 East Ninth Street','nb taupe brick',['337-shop','337-oblique','337-historic'],15.9)
for row,y in enumerate([3.65,6.58,9.51,12.44]):
 for col,at in enumerate([.115,.37,.64,.88]):win(a,f,at,y,1.02,2.08 if row==0 else 1.82,trim='nb cream band',nbHead='flat',ac=(row,col) in [(0,3),(1,0),(1,3),(2,0),(3,2)])
door(a,f,.557,.86,.63,2.93,recess=1.16)
shop(a,f,247852686,'New Sew Good Cleaners',[.01,.455],'cleaners',[['glass',1]],'Curved faded red awning, condensed white name, separate side service text; nine display compartments and low vent, raised sill. Door shares the recessed center passage.', ['337-shop','337-historic'],top=3.03,head=2.84,base=.64)
s=shop(a,f,247852686,'Wicked Heathens — dated east display',[.664,.986],'wicked',[['glass',1]],'Projecting black timber display, diamond grille, jewelry/mannequin and pale fabric behind glass; adjacent recessed entry, no invented fascia brand.', ['337-shop','337-historic'],top=3.08,head=2.91,base=.67)
s['detail09']['floor']=.55

for bid,num in [(247852685,'335'),(247852684,'333')]:
 a,f=elevation(bid,num+' East Ninth Street','nb red brick',['335-upper','335-shop','335-close','333-shop','333-westclose','333-reverse'])
 for row,y in enumerate([3.83,6.97,10.00,12.86]):
  for col,at in enumerate([.12,.365,.63,.875]):win(a,f,at,y,1.03,2.36 if row==0 else 2.13 if row==1 else 1.92,nbHead='pediment' if row==0 else 'molded',row=row,ac=(row,col) in ([(0,2),(1,0),(1,2),(2,0),(3,0),(3,3)] if bid==247852685 else [(0,3),(1,0),(2,0),(2,3),(3,3)]))
 door(a,f,.50,.99,.20,3.15)
 if bid==247852685:
  shop(a,f,bid,"Fabulous Fanny’s",[.01,.405],'fannys',[['door',.26],['glass',.74]],'Gray cloth awning, white script name and two 335 labels; silver rolling grille, giant eyeglass motif, red framed display, busts and eyeglasses, high AC.', ['335-close','335-shop'],base=.23)
  shop(a,f,bid,'Layers',[.631,.989],'layers',[['door',.29],['glass',.71]],'Narrow black/mixed-metal salon glazing, small brown script blade, grille, pale chairs and mirror layers; no awning.', ['335-close','337-historic'],base=.25)
 else:
  shop(a,f,bid,'333 west shop — tenant unresolved',[.01,.403],'west333',[['glass',.70],['door',.30]],'Black inclined canopy with small 333 E9th at right; broad left pane, narrow right door with circular pale script seal, pale chairs, blinds and blue water jug.', ['333-shop','333-westclose','333-reverse'],base=.19)
  shop(a,f,bid,'Spark Pretty',[.63,.99],'spark',[['glass',.72],['door',.28]],'Black inclined cloth, white stacked slanted logo/pink 333; metal grille, colorful clothing and toy display, torso forms, high left AC.', ['333-shop','333-westclose','333-reverse'],base=.24)

result={'schema':1,'id':'01-E09-21-N01B','parent':'01-E09-21','splitParent':'01-E09-21-N01','revision':'N01B-01','scopeFaces':[r['faceId'] for r in E],'elevations':E,'businesses':SHOPS,'junctions':[{'pair':pair,'condition':'Mapped touching party wall; separate materials, rooflines and cornice depth, no invented alley.','sourceIds':['337-oblique','335-upper','333-reverse'],'deferred':pair[1]==247852683} for pair in [[247852689,247852687],[247852687,247852686],[247852686,247852685],[247852685,247852684],[247852684,247852683]]],'heightException':{'buildingId':247852686,'mappedHeight':18.93,'engineHeight':15.9,'basis':'2024 oblique front cornice below both neighboring roofs; approximate comparative height, hidden roof unobserved.'},'counts':{'aboveGradeWindows':68,'basementOpenings':2,'shopfronts':6,'identifiedBusinesses':5,'tenantUnresolved':1,'residentialDoors':4},'sourceLedger':'model-source/east-village-e09-n01b/observations.json','targetCapture':'September 2024 with explicit November 2017 access supplement','ownership':'Four Ninth faces only; 331/south Ninth/147 First face/148 Ninth return deferred.'}
assert sum(len(r['architecture']['windows']) for r in E)==70
(OUT/'schedule.json').write_text(json.dumps(result,indent=2)+'\n')
print('N01B four elevations, 68 above-grade windows, 2 basement openings, six independent shops')
