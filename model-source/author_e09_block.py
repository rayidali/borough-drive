"""Remaining Ninth/Second–First block: explicit dated, individually owned faces.

Dimensions are visual estimates on unchanged mapped footprints. This schedule
never changes protected models. Regenerate with python3 model-source/author_e09_block.py.
"""
import json
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'model-source/east-village-e09-block'
DATA={b['id']:b for b in json.loads((ROOT/'dist/reconstruction/neighborhood.json').read_text())['buildings']}
OBS=json.loads((OUT/'observations.json').read_text());INV=json.loads((OUT/'inventory.json').read_text())
E=[];SHOPS=[];BY={}

def elevation(bid,num,wall,rows,cols,cornice,trim,escape=True,**kw):
 b=DATA[bid];idx=1 if bid==241822210 else 0;f=deepcopy(b['frontages'][idx]);effective=deepcopy(f)
 if bid==1063735559:
  effective.update(x=-109.821,z=65.520,length=5.937)
 sources=[k for k,v in OBS['sources'].items() if f'{bid}:{idx}' in v.get('faceIds',v.get('faces',[]))]
 h=kw.pop('height',b['height']);bottom=kw.pop('bottom',3.85);step=kw.pop('step',(h-bottom-2.7)/max(1,rows-1))
 positions=kw.pop('positions',[(j+.5)/cols for j in range(cols)] if cols else [])
 a={'wall':'eb '+wall,'windows':[],'doors':[],'returnShops':[],
    'observedGround':{'replaceWindows':False,'replaceDoors':False},
    'e09Block':{'number':num,'cornice':cornice,'trim':'eb '+trim,'rows':rows,'upperBottom':bottom,'step':step,**kw},
    'observation':{'sources':sources,'facts':[v for k in sources for v in OBS['sources'][k].get('observations',[])],'unknown':OBS['limits']}}
 for row in range(rows):
  for col,at in enumerate(positions):
   win(a,effective,at,bottom+row*step,kw.get('windowWidth',min(1.08,effective['length']/max(cols,1)*.56)),kw.get('windowHeight',min(1.92,step-.6)),trim='eb '+trim,row=row,col=col)
 if escape and rows:
  a['e09Block']['escape']={'span':kw.get('escapeSpan',[.27,.76]),'levels':[bottom-.16+j*step for j in range(rows)],'material':'eb '+kw.get('escapeColor','iron'),'dropAt':kw.get('dropAt',.69),'reverse':kw.get('reverse',False)}
 r={'faceId':f'{bid}:{idx}','buildingId':bid,'frontageIndex':idx,'address':str(num)+' East Ninth Street' if bid not in [247852702,241822210] else str(num)+' / Ninth return',
    'sourceFace':f,'buildingHeight':h,'sourceHeight':b['height'],'architecture':a}
 if effective!=f:r['effectiveFace']=effective;a['e09Block']['effectiveFace']=effective
 E.append(r);BY[str(num)]=(a,effective,bid);return a,effective

def win(a,f,at,y,w,h,**kw):
 a['windows'].append({'at':at,'width':w/f['length'],'bottom':y,'height':h,'frame':'eb sash','trim':'eb brown stone','hood':'none','rails':[.49],**kw})
def door(num,at=.5,w=1.06,low=.20,top=3.05,mat='dark wood',**kw):
 a,f,bid=BY[str(num)];d={'at':at,'width':w/f['length'],'bottom':low,'top':top,'leafTop':top-.45,'material':'eb '+mat,'trim':'eb '+mat,'recess':.25,'leaves':1,'hardware':'store09 aged brass','panels':[{'y':.65,'height':.45,'width':.75,'glass':True},{'y':.18,'height':.22,'width':.75}],**kw};a['doors'].append(d);return d
def access(num,at=.5,low=.65,width=1.5,depth=1.5,well=True,**kw):
 a,f,bid=BY[str(num)];a['e09Block']['access']={'at':at,'rise':low,'width':width,'depth':depth,**kw}
 if well:
  spans=kw.get('wellSpans',[[.025,max(.026,at-width/f['length']/2-.03)],[min(.974,at+width/f['length']/2+.03),.975]])
  a['observedGround']['basementAreaways']=[{'at':(x+y)/2,'width':y-x,'depth':kw.get('wellDepth',.93),'depthBelow':.55} for x,y in spans if y-x>.05]
def residential(num,at=.5,low=.75,top=3.15,shape='rectangle',positions=(.15,.32,.69,.86),**kw):
 a,f,bid=BY[str(num)];door(num,at=at,low=low,top=top,shape=shape,**kw)
 for x in positions:win(a,f,x,low+.40,.88,top-low-.42,grille=True,trim=a['e09Block']['trim'])
 access(num,at,low,width=1.50,depth=max(1.0,low*1.8))
def shop(num,name,span,kind,panels,identity,frame='dark wood',**kw):
 a,f,bid=BY[str(num)];key=f'{bid}:{1 if bid==241822210 else 0}:{kind}';sources=a['observation']['sources']
 d={'top':3.08,'head':2.80,'base':.37,'recess':.22,'transom':False,'panels':panels,'signs':[],
 'detail09':{'id':key,'frame':'eb '+frame,'surround':'eb '+frame,'frameWidth':.045,'pierWidth':.065,'floor':.17,'molding':True,'displayDepth':1.05,'doorSolidTop':.24,'displays':[],'furniture':[],'identity':identity,'sourceIds':sources},
 'detailE09Block':{'kind':kind},**kw}
 a['returnShops'].append({'name':name,'span':span,'design':d});SHOPS.append({'id':key,'businessId':kind,'faceId':f'{bid}:{1 if bid==241822210 else 0}','name':name,'span':span,'identity':identity,'sourceIds':sources,'component':kind,'reviewState':'authored; awaiting final served comparison','unknown':OBS['limits']});return d

# North: each line fixes a separate observed building profile, never an address seed.
elevation(247852683,'331','red brick',4,4,'raised-rosette','brown stone',head='segmental-first',corniceColor='gray stone',checker=True)
elevation(247852682,'329','dark red brick',4,2,'brackets','gray stone',height=16.1,bottom=4.05,step=2.65,escapeSpan=[.12,.83],head='flat',roofAddition=True,corniceColor='gray stone')
elevation(1063735559,'327','limestone',5,2,'dentils','limestone',False,height=18.29,bottom=4.15,step=2.6,windowWidth=1.95,windowHeight=1.95,head='keystone',quoins=True,corniceColor='limestone')
elevation(247852681,'325','cream stone',4,2,'simple','brown stone',False,bottom=4.1,step=2.65,head='flat')
elevation(247852680,'323','red brown brick',4,6,'plain','white stone',positions=[.10,.24,.38,.62,.76,.90],windowWidth=.85,head='none',escapeSpan=[.13,.84])
elevation(247852679,'321','red brick',4,4,'simple','brown stone',positions=[.15,.36,.66,.87],head='segmental',escapeSpan=[.53,.94])
elevation(247852678,'319','red brown brick',3,2,'plain','brown stone',bottom=4.1,step=2.88,windowWidth=2.05,head='dentil',escapeSpan=[.12,.43],scaffold=True)
elevation(247852677,'317','cream stone',4,4,'juliette','brown stone',False,bottom=3.75,step=2.83,head='paired-pediment',aprons=True)
elevation(247852676,'315','yellow brick',5,4,'brackets','brown stone',bottom=4.1,step=3.08,escapeColor='blue iron',head='round-second',checker=True)
elevation(247852675,'313','red brick',4,4,'brackets','brown stone',head='molded',flag=True)
elevation(247852674,'311','red brick',3,3,'simple','white stone',False,bottom=4.1,step=2.75,head='flat',roofRail=True)
elevation(247852673,'309','red brick',4,4,'brackets','brown stone',bottom=5.9,step=3.0,escapeColor='rust iron',head='segmental',corniceColor='cream stone')
elevation(247852672,'307','buff red brick',4,4,'brackets','brown stone',bottom=3.8,step=3.3,escapeSpan=[.57,1.0],escapeColor='rust iron',head='segmental',corniceColor='cream stone')
elevation(247852671,'305','buff red brick',4,4,'brackets','brown stone',bottom=4.0,step=3.3,escapeSpan=[.02,.43],escapeColor='rust iron',head='segmental',corniceColor='cream stone',quoins=True)
a,f=elevation(247852702,'146 Second Avenue','red brick',4,6,'brackets','brown stone',False,bottom=4.15,step=3.2,head='segmental',corniceColor='cream stone',quoins=True)
for w in a['windows']:
 if w['col'] in [2,3]:w.update(ebOriginal={k:w[k] for k in ['width','height','bottom']},width=.35/f['length'],height=.53,bottom=w['bottom']+.67,ebInfill=True)

# South: the two 350 records share a five-bay composition, not two repeated houses.
elevation(241822239,'350','red brick',4,3,'brackets','green metal',False,bottom=3.75,step=2.95,head='molded',corniceColor='green metal')
elevation(241822276,'350A','red brick',4,2,'brackets','green metal',bottom=3.75,step=2.95,head='molded',corniceColor='green metal',escapeSpan=[.09,.91])
elevation(241822204,'348','buff stone',5,4,'ornate','cream stone',bottom=4.0,step=3.05,head='beaded',carvedPanels=True)
elevation(241822315,'346','red brick',4,4,'plain','gray stone',bottom=5.5,step=3.0,head='pediment-first',escapeColor='silver metal')
elevation(241822241,'344','brown stone',4,4,'brackets','brown stone',bottom=4.2,step=3.05,head='molded',escapeColor='rust iron')
elevation(241822261,'342','red brick',4,4,'stepped','cream stone',bottom=3.7,step=3.15,head='banded',carvedPanels=True)
elevation(241822335,'340','pink brick',4,4,'brackets','brown stone',bottom=3.65,step=2.6,head='flat',escapeColor='green metal',corniceColor='green metal')
elevation(241822244,'338','white stucco',0,0,'stepped','white stone',False,garage=True)
elevation(241822293,'336','tan brick',1,4,'carriage','gray stone',False,bottom=4.2,step=3.0,windowHeight=2.35,head='flat',carriage=True)
for bid,num in [(241822229,'334'),(241822251,'332')]:
 elevation(bid,num,'red brick' if num=='334' else 'dark red brick',4,4,'raised-rosette','brown stone',bottom=5.4,step=3.05,head='segmental',corniceColor='brown stone')
elevation(241822179,'328','red brick',5,6,'plain','white stone',bottom=3.9,step=2.9,head='terracotta',carvedPanels=True,quoins=True,escapeColor='green metal',escapeSpan=[.31,.69])
elevation(241822183,'324','red brick',5,6,'ornate','cream stone',bottom=4.0,step=2.9,head='terracotta',carvedPanels=True,quoins=True,escapeSpan=[.30,.70],flag=True)
elevation(241822272,'320','modern red brick',6,2,'plain','gray stone',False,bottom=3.3,step=2.6,windowWidth=2.45,windowHeight=1.8,modern=True)
for bid,num in [(241822187,'318'),(241822165,'314–316'),(241822171,'312')]:
 elevation(bid,num,'buff brick',5,4,'brackets','brown stone',bottom=4.25,step=3.1,head='alternating-pediment',carvedPanels=True)
elevation(241822269,'310','brown stone',3,3,'brackets','brown stone',False,bottom=5.2,step=3.1,head='flat')
a,f=elevation(241822210,'144 Second Avenue','cream brick',0,0,'veselka','brown metal',False,bottom=5.0,step=4.0,veselka=True)
for group in range(7):
 center=(group+.5)/7
 win(a,f,center,5.0,3.50,2.55,columns=4,rails=[],trim='eb brown metal',row=0,col=group)
 for side in [-1,1]:win(a,f,center+side*.66/f['length'],9.35,1.05,2.20,trim='eb brown metal',row=1,col=group*2+(side+1)//2)

# Entrances and wells: visible negative space, raised access and basement entries.
door('331',top=3.35,shape='round',w=1.04);access('331',low=.20,depth=.40,well=False)
residential('329',at=.28,low=1.35,top=3.9,positions=(.78,));BY['329'][0]['doors'][0]['material']='eb oak wood'
door('327',at=.81,w=1.12,top=3.55,mat='plywood');BY['327'][0]['e09Block']['garageSpan']=[.025,.65]
door('325',at=.69,low=.70,top=3.45,shape='round',mat='oak wood');door('325',at=.20,w=1.05,low=-.25,top=1.85,shape='round');access('325',.69,.70,1.40,1.1,wellSpans=[[.03,.38]])
residential('323',at=.88,low=.30,top=3.2,positions=(.14,.29,.44,.66));access('323',.88,.30,1.1,.7,wellSpans=[[.02,.76]])
door('321',at=.5);access('321',.50,.20,1.1,.4,wellSpans=[[.81,.97]],wellDepth=1.0)
residential('319',at=.5,low=.65,positions=(.23,.77))
for w in BY['319'][0]['windows'][-2:]:w.update(width=1.85/BY['319'][1]['length'],columns=2)
residential('317',at=.59,low=.45,top=3.1,positions=(.15,.35,.82));BY['317'][0]['e09Block']['groundPaint']='cream stone'
door('315',at=.5,w=1.21,top=3.65,shape='round');access('315',.5,.20,1.4,.4,wellSpans=[[.04,.39],[.63,.96]])
residential('313',at=.5,low=.65,top=3.35,positions=(.22,.78));BY['313'][0]['e09Block']['groundPaint']='white stone'
for w in BY['313'][0]['windows'][-2:]:w.update(width=1.56/BY['313'][1]['length'],shape='round')
residential('311',at=.20,low=1.50,top=4.0,positions=(.54,.83),mat='oak wood');access('311',.20,1.50,1.35,2.2,wellSpans=[[.43,.97]])
door('309',at=.5,w=1.4,low=2.1,top=5.0,mat='oak wood',leaves=2);access('309',.5,2.1,1.6,2.9,wellSpans=[[.01,.36],[.65,.99]])
for at in [.13,.30,.71,.88]:win(BY['309'][0],BY['309'][1],at,2.65,.86,2.15,trim='eb brown stone')
door('307',at=.5,w=.86,top=3.05);door('305',at=.11,w=.92,top=3.10,mat='oak wood')
door('146 Second Avenue',at=.945,w=1.25,low=.70,top=3.65);access('146 Second Avenue',.945,.70,1.5,1.1,well=False)
for at in [.72,.82]:win(BY['146 Second Avenue'][0],BY['146 Second Avenue'][1],at,.95,1.15,2.05,grille=True)
door('350',at=.78,w=1.1);door('348',at=.5,w=1.65,low=1.15,top=3.8,shape='round',leaves=2);access('348',.5,1.15,2.2,1.8)
for at in [.13,.29,.72,.87]:win(BY['348'][0],BY['348'][1],at,1.55,.87,2.05,shape='segmental',grille=True,trim='eb cream stone')
residential('346',at=.5,low=2.0,top=4.8,positions=(.14,.30,.71,.88));access('346',.5,2.0,1.6,2.7,wellSpans=[[.02,.36],[.65,.98]])
residential('344',at=.5,low=.8,top=3.65,positions=(.12,.29,.72,.89),mat='oak wood',leaves=2)
residential('342',at=.5,low=.30,top=3.15,positions=(.15,.30,.72,.87));BY['342'][0]['e09Block']['groundPaint']='dark brick'
residential('340',at=.5,low=.25,top=3.25,shape='round',positions=(.22,.79));BY['340'][0]['e09Block']['groundPaint']='charcoal stone'
for w in BY['340'][0]['windows'][-2:]:w.update(width=1.55/BY['340'][1]['length'],shape='round')
door('338',at=.89,w=.85,top=2.9,mat='red metal');BY['338'][0]['e09Block']['garageSpan']=[.03,.78]
door('336',at=.10,w=.90,top=3.4,mat='gray metal');BY['336'][0]['e09Block']['garageSpan']=[.24,.77]
for num in ['334','332']:
 residential(num,at=.5,low=2.0,top=4.9,positions=(.13,.30,.71,.88));access(num,.5,2.0,1.50,2.65,wellSpans=[[.02,.36],[.65,.98]]);BY[num][0]['e09Block']['groundPaint']='white stone'
door('328',at=.375,w=.86,top=3.35);door('324',at=.365,w=.90,low=.38,top=3.25);access('324',.365,.38,1.15,.60,well=False)
door('320',at=.77,w=1.6,top=2.95,recess=.46);win(BY['320'][0],BY['320'][1],.27,.48,2.7,2.1,grille=True,trim='eb gray stone')
for num in ['318','314–316','312']:door(num,at=.5,w=.85,top=3.28,mat='red wood' if num=='318' else 'dark wood')
residential('310',at=.79,low=1.8,top=4.8,shape='round',positions=(.19,.46),leaves=2);access('310',.79,1.8,1.65,2.55,wellSpans=[[.02,.62]])

# Source-specific portals, openings and equipment. Row numbers start at the lowest upper floor.
# Fit the observed upper-floor rhythm to each unchanged municipal height.
# The earlier fixed storey steps left an unobserved 2.5 m blank attic band.
# These remain photographic estimates, not surveyed floor elevations.
for num in ['315','348','344','342','334']:
 a,f,bid=BY[num];spec=a['e09Block'];record=next(r for r in E if r['buildingId']==bid)
 upper=[w for w in a['windows'] if 'row' in w]
 top=max(w['bottom']+w['height'] for w in upper);delta=record['buildingHeight']-.95-top
 for w in upper:w['bottom']+=delta*w['row']/(spec['rows']-1)
 spec['step']+=delta/(spec['rows']-1)
 if spec.get('escape'):spec['escape']['levels']=[spec['upperBottom']-.16+j*spec['step'] for j in range(spec['rows'])]
for w in BY['329'][0]['windows']:
 if w.get('row')==3:w.update(bottom=13.75,height=1.60)
BY['329'][0]['e09Block']['escape']['levels']=BY['329'][0]['e09Block']['escape']['levels'][:3]
for w in BY['315'][0]['windows']:
 if w.get('row')==1:w.update(shape='round',height=2.12)
for num in ['323','348','328','324','318','314–316','312','311']:
 for w in BY[num][0]['windows']:w['frame']='eb white wood'
# The outer bays of the twin terracotta houses are close pairs, with two
# separated center windows. Equal six-bay spacing loses the defining arches.
for num in ['328','324']:
 a,f,bid=BY[num]
 for w in a['windows']:
  if 'row' in w:
   w['at']=[.115,.205,.41,.59,.795,.885][w['col']]
   if w['col'] in [0,1,4,5]:w['width']=.78/f['length']
for num,trim,portal in [('325','brown stone','columns'),('315','cream stone','columns'),('311','white stone','pilasters'),('309','brown stone','pilasters'),('146 Second Avenue','brown stone','columns'),('348','cream stone','columns'),('346','gray stone','pilasters'),('334','white stone','pilasters'),('332','white stone','pilasters'),('310','brown stone','columns')]:
 for d in BY[num][0]['doors']:d.update(trim='eb '+trim,portal=portal)
for num in ['344','311','309']:
 for d in BY[num][0]['doors']:
  d['panels']=[{'y':.72,'height':.38,'width':.47,'glass':True},{'y':.34,'height':.26,'width':.72},{'y':.10,'height':.15,'width':.72}]
BY['312'][0]['doors'][0]['grille']=True
BY['320'][0]['doors'][0].update(grille=True)
BY['338'][0]['doors'][0].update(panels=[],leafTop=2.90,openingMaterial='eb red metal')
BY['336'][0]['doors'][0].update(panels=[{'y':.64,'height':.55,'width':.72,'glass':True,'rows':3}],leafTop=3.3,grille=True)
# Only units clearly visible in the individually dated sources; obscured units stay unresolved.
ac_positions={
 '331':[(0,3),(1,0),(2,0),(3,3)],
 '342':[(1,0),(1,3),(2,0),(2,1),(2,3)],
 '313':[(r,c) for r in range(4) for c in [0,3]],
 '311':[(2,0),(2,1),(1,2)],
 '315':[(4,0)],
 '321':[(2,0),(3,2)],
 '334':[(0,0),(1,0),(2,0),(3,0),(3,3)],
 '332':[(r,c) for r in range(4) for c in [0,3]],
 '328':[(1,2),(2,1),(2,2),(3,1),(4,1)],
 '324':[(0,0),(0,1),(1,1),(1,4),(2,2),(3,2),(4,1),(4,5)],
 '348':[(2,3),(4,3)],'346':[(0,0),(0,3),(1,3),(3,3)],
 '344':[(0,0),(1,0),(2,0)],
 '314–316':[(1,0),(1,1),(2,0),(3,1),(4,1)]
}
for num,positions in ac_positions.items():BY[num][0]['e09Block']['windowAC']=positions
# Remove illustrative repeating curtains: unobserved interiors remain neutral.
for a,f,bid in BY.values():a['e09Block']['windowDressing']=[]
for w in BY['336'][0]['windows']:w.update(rails=[],columns=2)
BY['331'][0]['e09Block']['windowDressing']=[{'row':0,'col':0,'type':'blind'},{'row':0,'col':3,'type':'blind'},{'row':1,'col':3,'type':'blind'}]
BY['336'][0]['e09Block']['windowDressing']=[{'row':0,'col':2,'type':'blind'}]

# Store compositions use independent panels, access, sign and display geometry.
shop('331','Source Unltd',[.01,.405],'source',[['glass',.78],['door',.22]],'Black sloping cloth with starburst and service valance; bridge-art shutter, grille and mailbox.')
shop('331','Frida Munchies — retained fascia / vacant display',[.62,.99],'frida',[['door',.28],['glass',.72]],'Rounded two-line white/pink fascia, multicolor bands, rainbow jamb, lease notice and bunting.')
shop('321','The March Hare',[.01,.405],'hare',[['glass',.70],['door',.30]],'White script on red fascia, red window frame, green kick panel with white hare, varied toys and books.',frame='red wood')
shop('321','321 east shop — tenant unresolved',[.63,.99],'321east',[['door',.28],['glass',.72]],'Blue cloth shade and closed metal grille; tenant copy not legible.',frame='blue metal')
shop('315','Rosemary Home',[.01,.39],'rosemary',[['glass',.72],['door',.28]],'Deep green projecting window, stacked glass letters, green bulkhead, flowers, books and tabletop objects.',frame='green wood',base=.63)
shop('315','Gnocchi on 9th',[.63,.99],'gnocchi',[['door',.28],['glass',.72]],'Blue fascia with gold script, circular orange/yellow gnocchi motif, grille and barrel menu stand.',frame='blue metal')
shop('309','Spooksvilla + Friends',[.01,.365],'spook',[['glass',.73],['door',.27]],'Cyan/pink illustrated fascia, outlined irregular lettering, animal window decals, print racks and pale wood counter.',top=2.15,head=1.91,base=.23)
shop('309',"Davey’s Ice Cream",[.64,.99],'daveys',[['door',.29],['glass',.71]],'Raised multicolor ICE CREAM letters on white angled fascia, turquoise frame, rainbow threshold, colored bulbs and cone A-board.',frame='turquoise wood',top=2.15,head=1.91,base=.24)
shop('307','SHW / Still House',[.01,.405],'shw',[['glass',.73],['door',.27]],'Pale box hood, broad left display and deep narrow right entry, silver grille; sparse ceramic/jewelry display.',frame='white wood')
shop('307','MUD',[.62,.99],'mud',[['door',.28],['glass',.72]],'Carved wood, X-braced entry, cream MUD medallion, projecting tripartite window, red curtains, round relief kick panels and warm bulbs.',frame='oak wood',base=.65)
shop('305','Raw Spirit — dated identity, partly obscured front',[.24,.60],'raw',[['glass',.74],['door',.26]],'Dark independent shop frame and recessed doorway; frontage details partly obscured, no unsupported elaborate logo.')
shop('305','Art + Ray — dated identity, partly obscured front',[.64,.99],'artray',[['door',.27],['glass',.73]],'Separate narrow gallery entry and broad window; small framed artwork layers, physical frontage partly obscured.')
shop('146 Second Avenue','Village Farm — closed Ninth frontage',[.01,.65],'farm',[['glass',.25],['glass',.25],['glass',.25],['glass',.25]],'Long blue sloped 24 HR GROCERY awning, white service valance, opaque boarded panes and graffiti.',frame='blue metal')
shop('350','Mizu Sushi — closed frontage',[.01,.65],'mizu',[['glass',.72],['door',.28]],'Black flat fascia, brush white name, closed tagged shutter.')
shop('350A',"Rafael’s Barber Shop",[.01,.99],'rafael',[['glass',.68],['door',.32]],'Gold fascia, red/white/blue shallow striped shade, portrait window grid and projecting barber pole.',frame='gold metal')
shop('346','9th Street Vintage',[.01,.36],'vintage9',[['glass',.72],['door',.28]],'Pale gray serif fascia, diamond grille, right entrance and separate lower approach.',frame='gray metal',top=2.12,head=1.91)
shop('346','Tribes of Morocco',[.65,.99],'morocco',[['door',.29],['glass',.71]],'Red sloped cloth, gold serif name, dark closed shutter, white ornamental areaway fence.',top=2.12,head=1.91)
shop('334','Cloak & Dagger',[.01,.36],'cloak',[['glass',.72],['door',.28]],'White fascia, narrow red serif name, silver grille, round blade and white plant pots.',frame='white wood',top=2.16,head=1.93)
shop('334','Rice Bird',[.65,.99],'ricebird',[['door',.28],['glass',.72]],'Black canopy with white Chinese/Latin lettering, food display panels and string lights.',top=2.16,head=1.93)
shop('332','Lady Wong',[.01,.36],'ladywong',[['glass',.70],['door',.30]],'Taupe canopy with gold letters, black pineapple blade and pastry display.',top=2.16,head=1.93)
shop('332','Sushi Kai',[.65,.99],'sushikai',[['door',.28],['glass',.72]],'Separate taupe canopy, round white flower mark on black blade, narrow basement entry.',top=2.16,head=1.93)
shop('328','an.mé',[.01,.32],'anme',[['glass',.73],['door',.27]],'Lavender blue fascia with small gold name, tagged roll shutter and independent entry.',frame='blue metal')
shop('328','Pillow Cat Books',[.42,.70],'pillowcat',[['glass',.70],['door',.30]],'Green canopy with white italic letters and cat, green grille and pink BOOKS display.',frame='green wood')
shop('328','Jane Cookshop',[.72,.99],'jane',[['door',.28],['glass',.72]],'Pale yellow/white shop frame and kitchenware window, separate pale fascia.',frame='yellow wood')
shop('324','DUO',[.01,.30],'duo',[['glass',.70],['door',.30]],'White hood and restrained gray trim, clothing display and sparse gold glass lettering.',frame='gray metal')
shop('324','D. L. Cerney',[.42,.66],'cerney',[['glass',.70],['door',.30]],'Narrow carved timber fascia and diamond grille, hanging garments behind glass.',frame='oak wood')
shop('324','Sakaya',[.68,.99],'sakaya',[['door',.28],['glass',.72]],'Pale hood, brown vertical SAKAYA blade, bottle shelving behind metal grille.',frame='white wood')
shop('318','318 east shop — obscured tenant',[.01,.41],'318east',[['glass',.72],['door',.28]],'Carved dark timber surround, broad plant/display pane and narrow access; tenant lettering unresolved.',frame='oak wood')
shop('318','A Sustainable Village — Ninth storefront',[.62,.99],'sustainable',[['door',.28],['glass',.72]],'Brown timber display and left entry, silver roll grille, white green-letter blade, refill containers, green bench and chalk A-board.',frame='oak wood',base=.58)
shop('314–316','Cobblestones',[.01,.41],'cobblestones',[['glass',.72],['door',.28]],'Gray pinstriped canopy, white capital letters, low black shutter and clothes behind grille.',frame='gray metal')
shop('314–316','314 west shop — closed dated frontage',[.62,.99],'314west',[['door',.28],['glass',.72]],'Plain silver shutter and pale projecting blade; later tenant identity not imposed on September 2024 appearance.',frame='gray metal')
shop('312','Headdress',[.01,.41],'headdress',[['glass',.73],['door',.27]],'Cream three-part glazing, slender white crossrail and thin name, salon chair/mirror and high right AC.',frame='white wood')
shop('312','Cabin on 9th',[.62,.99],'cabin',[['door',.28],['glass',.72]],'Black fascia with white script, light timber window, plants along low display.',frame='oak wood')
shop('144 Second Avenue','Veselka — Ninth dining frontage',[.012,.988],'veselka',[['glass',1/14] for _ in range(14)],'Long green divided glazing with gold food-name bands, lamps, folk-art color panels and a blue/yellow curb dining shelter.',frame='green wood',top=4.15,head=3.68,base=.60)

# Preserve clear approaches to each independently observed shop doorway.
# Wells stop beside the entry instead of running an unbroken fence across it.
for r in E:
 a=r['architecture'];f=r.get('effectiveFace',r['sourceFace']);clear=[]
 for sh in a['returnShops']:
  left,right=sh['span'];cursor=left
  for kind,fraction in sh['design']['panels']:
   end=cursor+(right-left)*fraction
   if kind=='door':clear.append((cursor-.035,end+.035))
   cursor=end
 wells=[]
 for well in a['observedGround'].get('basementAreaways',[]):
  spans=[(well['at']-well['width']/2,well['at']+well['width']/2)]
  for lo,hi in clear:
   spans=[piece for aa,bb in spans for piece in ([(aa,min(bb,lo)),(max(aa,hi),bb)] if aa<hi and bb>lo else [(aa,bb)]) if piece[1]-piece[0]>.045]
  wells.extend({**well,'at':(lo+hi)/2,'width':hi-lo} for lo,hi in spans)
 if 'basementAreaways' in a['observedGround']:a['observedGround']['basementAreaways']=wells

for r in E:
 a=r['architecture'];a['e09Block']['reviewState']='needs rendered review'
 if not a['observation']['sources']:raise ValueError('Missing inspected source '+r['faceId'])
 expected=next(v for v in INV['faces'] if v['faceId']==r['faceId'])
 assert r['sourceFace']==expected['sourceFace']
assert {r['faceId'] for r in E}==set(INV['scope']['editableRemainingFaceIds'])
protected={r['id'] for r in json.loads((OUT/'protected-models.json').read_text())['models']}
assert not protected & {r['buildingId'] for r in E}
result={'schema':1,'id':'01-E09-21','revision':'E09-BLOCK-01','scopeFaces':[r['faceId'] for r in E],'elevations':E,'businesses':SHOPS,
 'sourceLedger':'model-source/east-village-e09-block/observations.json','targetCapture':'September 2024 with individually dated supplements; not verified October 2026 occupancy',
 'ownership':'34 remaining Ninth faces only; 221 existing models and Second/First avenue faces protected or deferred.',
 'exceptions':[{'faceId':'1063735559:0','condition':'Mapped frontage omits 1.555 m of its own street-edge polygon; effective face covers its garage, without widening the footprint.'},
 {'faceId':'247852682:0','condition':'Approximate 16.1 m roof height includes observed rooftop addition; source mapped height retained separately.'},
 {'condition':'2.657 m gap between 305 and 303 has a low green street wall and open air above; no tall infill mass.'},
 {'condition':'Protected 145 First / 352 Ninth remains byte-identical, including its previously documented return limits.'}],
 'counts':{'facades':len(E),'upperAndGroundWindows':sum(len(r['architecture']['windows']) for r in E),'entrances':sum(len(r['architecture']['doors']) for r in E),'shopfronts':len(SHOPS)}}
(OUT/'schedule.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result['counts']))
