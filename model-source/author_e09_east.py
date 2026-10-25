"""Ninth / First–Avenue A: explicit observed elevations and individual shops.

Regenerate schedule with python3 model-source/author_e09_east.py. Footprints
are mapped; relief, openings and furniture dimensions are visual estimates.
Sources, corrections and unresolved dated details remain in observations.json.
"""
import json
from copy import deepcopy
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'model-source/east-village-e09-east'
DATA={b['id']:b for b in json.loads((ROOT/'dist/reconstruction/neighborhood.json').read_text())['buildings']}
OBS=json.loads((OUT/'observations.json').read_text())
INV=json.loads((OUT/'inventory.json').read_text())
E=[];BY={};SHOPS=[]

def elevation(bid,num,wall,rows,cols,trim='brown stone',cornice='brackets',escape=True,idx=0,**kw):
 b=DATA[bid];f=deepcopy(b['frontages'][idx]);fid=f'{bid}:{idx}'
 h=kw.pop('height',b['height']);bottom=kw.pop('bottom',3.9)
 wh=kw.pop('windowHeight',1.8);step=kw.pop('step',(h-bottom-wh-.85)/max(1,rows-1))
 positions=kw.pop('positions',[(c+.5)/cols for c in range(cols)] if cols else [])
 sources=[k for k,v in OBS['sources'].items() if fid in v.get('faceIds',v.get('faces',[]))]
 spec={'number':num,'rows':rows,'upperBottom':bottom,'step':step,'cornice':cornice,'trim':'eb '+trim,'head':'molded',**kw}
 a={'wall':wall if wall.startswith(('p02 ','ee ','painted ee ')) else 'eb '+wall,'windows':[],'doors':[],'returnShops':[],
    'observedGround':{'replaceWindows':False,'replaceDoors':False},'e09East':spec,
    'observation':{'sources':sources,'facts':[fact for k in sources for fact in OBS['sources'][k].get('observations',[])],'unknown':OBS['limits']}}
 for row in range(rows):
  for col,at in enumerate(positions):win(a,f,at,bottom+row*step,kw.get('windowWidth',min(1.07,f['length']/max(cols,1)*.55)),wh,row=row,col=col,trim='eb '+trim)
 if escape and rows:spec['escape']={'span':kw.get('escapeSpan',[.28,.75]),'levels':[bottom-.17+j*step for j in range(rows)],'material':'eb '+kw.get('escapeColor','iron'),'dropAt':kw.get('dropAt',.69),'reverse':kw.get('reverse',False),'balconyOnly':kw.get('balconyOnly',False),'ornament':kw.get('escapeOrnament','plain')}
 r={'faceId':fid,'buildingId':bid,'frontageIndex':idx,'address':str(num),'sourceFace':f,'sourceHeight':b['height'],'buildingHeight':h,'architecture':a}
 E.append(r);BY[str(num)]=(a,f,bid,idx);return a,f

def win(a,f,at,y,w,h,**kw):
 a['windows'].append({'at':at,'width':w/f['length'],'bottom':y,'height':h,'frame':'eb sash','trim':a['e09East']['trim'],'hood':'none','rails':[.49],**kw})
def door(num,at=.5,w=1.04,low=.18,top=3.1,mat='dark wood',**kw):
 a,f,_,_=BY[str(num)];d={'at':at,'width':w/f['length'],'bottom':low,'top':top,'leafTop':top-.45,'material':'eb '+mat,'trim':'eb '+mat,'recess':.25,'leaves':1,'hardware':'store09 aged brass','panels':[{'y':.63,'height':.48,'width':.74,'glass':True},{'y':.16,'height':.22,'width':.74}],**kw};a['doors'].append(d);return d
def access(num,at=.5,rise=.65,width=1.5,depth=1.2,well=True,**kw):
 a,f,_,_=BY[str(num)];a['e09East']['access']={'at':at,'rise':rise,'width':width,'depth':depth,**kw}
 if well:
  spans=kw.get('wellSpans',[[.025,at-width/f['length']/2-.025],[at+width/f['length']/2+.025,.975]])
  a['observedGround']['basementAreaways']=[{'at':(x+y)/2,'width':y-x,'depth':kw.get('wellDepth',.95),'depthBelow':.58} for x,y in spans if y-x>.05]
def residential(num,at=.5,rise=.7,top=3.25,positions=(.13,.30,.70,.87),windowWidth=.85,**kw):
 a,f,_,_=BY[str(num)];door(num,at,low=rise,top=top,**kw)
 for x in positions:win(a,f,x,rise+.38,windowWidth,top-rise-.40,grille=True)
 access(num,at,rise,depth=max(1.,rise*1.5))
def shop(num,name,span,kind,panels,identity,frame='dark wood',**kw):
 a,f,bid,idx=BY[str(num)];key=f'{bid}:{idx}:{kind}'
 d={'top':3.08,'head':2.80,'base':.38,'recess':.24,'transom':False,'panels':panels,'signs':[],
    'detail09':{'id':key,'frame':'eb '+frame,'surround':'eb '+frame,'frameWidth':.045,'pierWidth':.065,'floor':.17,'molding':True,'displayDepth':1.,'doorSolidTop':.24,'displays':[],'furniture':[],'identity':identity,'sourceIds':a['observation']['sources']},'detailE09East':{'kind':kind},**kw}
 a['returnShops'].append({'name':name,'span':span,'design':d});SHOPS.append({'id':key,'faceId':f'{bid}:{idx}','name':name,'businessId':kind,'span':span,'identity':identity,'sourceIds':a['observation']['sources'],'reviewState':'authored; needs served comparison','unknown':OBS['limits']});return d

# North residential and mixed-use row; each declaration follows its own source.
elevation(248142921,'411','red brick',4,4,escape=False,head='flat',corniceColor='brown stone')
elevation(248142923,'413','yellow brick',4,4,'gray stone',head='molded',corniceColor='green metal',groundPaint='cream stone')
elevation(248142925,'415','red brick',4,4,head='pediment-first',escapeOrnament='scroll')
elevation(248142926,'417','red brick',4,4,'gray stone',bottom=5.0,head='pediment-first',escapeColor='silver metal',edgeTrim=True,corniceColor='brown stone')
elevation(248142927,'419','pink brick',3,4,escape=False,head='flat',flag=True)
elevation(248142929,'421','red brick',4,4,bottom=4.3,head='round-second',groundPaint='ee coral',entryCanopy=True,bands=True)
elevation(248142930,'423','red brick',3,2,'gray stone','dentils',False,head='flat',groundPaint='ee sage')
elevation(248142932,'425','red brick',3,2,'gray stone','dentils',False,head='flat',groundPaint='ee sage')
elevation(248142934,'427','red brick',3,2,'gray stone',escape=False,head='flat',groundPaint='brown stone',shutters=True)
elevation(248142936,'429','red brick',3,3,head='molded',escapeColor='rust iron')
elevation(248142938,'431','cream stone',4,3,'cream stone',head='pediment-first',groundPaint='cream stone',ornate431=True)
elevation(248142940,'433','pink brick',4,3,'gray stone',head='flat',escapeColor='rust iron',groundPaint='cream stone')
elevation(248142942,'435','red brown brick',3,3,'cream stone',corniceColor='green metal',head='flat')
elevation(248142944,'437','red brick',4,3,'gray stone',head='segmental')
elevation(248142945,'439','red brick',3,4,'cream stone','rail-blocks',head='flat',escapeColor='green metal',escapeOrnament='scroll')
for bid,num in [(248142947,'441'),(248142948,'443'),(248142950,'445')]:
 a,f=elevation(bid,num,'painted ee white brick',5,4,'charcoal stone','plain',positions=[.13,.33,.67,.87],bottom=3.9,windowHeight=1.60,head='flat',escapeSpan=[.56,.99],balconyOnly=True,escapeOrnament='spindles')
 for row in range(5):win(a,f,.5,3.9+row*a['e09East']['step']+.45,.32,.62,row=row,col=4,trim='eb charcoal stone')

door('411');access('411',rise=.20,depth=.42,well=False)
for n in ['413','415']:residential(n,rise=.85,top=3.5)
residential('417',rise=1.1,top=4.25)
residential('419',rise=.42,top=3.25,positions=(.12,.30,.70,.88));BY['419'][0]['e09East']['groundPaint']='pink brick'
residential('421',rise=.75,top=3.85,positions=(.21,.79),windowWidth=1.65)
# One shared-looking pale ground band, but only the photographed 425 entrance.
for n in ['423','425']:
 a,f,_,_=BY[n]
 for at in ([.24,.72] if n=='423' else [.68]):win(a,f,at,1.10,1.18,2.05,grille=True,trim='eb gray stone')
 access(n,at=.14 if n=='425' else .99,rise=.48,width=1.10,depth=.8,wellSpans=[[.04,.96]] if n=='423' else [[.34,.96]])
door('425',at=.14,low=.48,top=3.28,w=.86)
BY['423'][0]['e09East'].pop('access',None)
residential('427',at=.20,rise=.40,top=3.2,positions=(.70,),windowWidth=1.12)
residential('429',rise=.68,top=3.3,positions=(.21,.79),windowWidth=1.36)
residential('431',rise=.88,top=3.65,positions=(.19,.81),windowWidth=1.28,shape='round',leaves=2,w=1.30)
residential('433',rise=.30,top=3.5,positions=(.21,.81),windowWidth=1.45,shape='round',w=1.25)
for n in ['435','437','439','441','443','445']:door(n,at=.5,top=3.23)
BY['445'][0]['doors'][0]['label']='No. 445'
door('445',at=.973,w=.54,top=2.90,label='')

# South: residential houses, paired parcels, basements and the tall ornate 406.
elevation(248142661,'402','red brick',2,3,escape=False,bottom=4.45,windowHeight=1.85)
elevation(248142662,'404','red brick',2,3,escape=False,height=11.49,bottom=4.40,step=2.60,roofAddition=True,streetWallHeight=10.20)
elevation(248142663,'406','red brick',5,6,'gray stone','stepped',bottom=4.1,windowHeight=1.67,positions=[.10,.23,.435,.565,.77,.90],head='paired-carved',ornate406=True,escapeSpan=[.34,.66])
elevation(248142664,'410','red brick',2,3,'green metal',bottom=5.0,step=3.0,escapeSpan=[.31,.98],corniceColor='green metal')
elevation(248142710,'412','red brick',4,6,'gray stone',bottom=5.4,windowHeight=1.8,head='flat',escapeSpan=[.66,.97],groundPaint='gray stone')
elevation(248142666,'416','red brick',4,5,'gray stone',bottom=5.,head='flat',escapeSpan=[.30,.70])
elevation(248142669,'418','buff brick',4,3,'brown stone','plain',bottom=5.0,head='flat',escapeSpan=[.05,.64])
elevation(248142668,'418.5','red brick',4,2,'gray stone','plain',False,bottom=4.3,head='flat',roofRail=True,groundPaint='ee sage')
for bid,num in [(248142672,'420'),(248142675,'422')]:
 elevation(bid,num,'red brick',4,3,'brown stone',bottom=5.05,head='segmental',balconyOnly=True,escapeSpan=([.01,.39] if num=='420' else [.60,.99]),escapeOrnament='circles')
elevation(248142676,'424','red brick',4,6,bottom=5.,head='segmental',escapeSpan=[.32,.68],sideBalconies=True)
elevation(248142677,'426','red brick',4,4,head='curved-first',groundPaint='ee pale yellow')
elevation(248142679,'428','red brick',4,4,head='molded',groundPaint='dark wood')
elevation(248142681,'430','red brick',4,4,bottom=5.6,head='pediment-first',bands=True)
elevation(248142682,'432','red brick',3,4,'cream stone',head='flat')
elevation(248142683,'434','red brick',4,4,head='flat')
elevation(248142684,'436','red brick',4,4,'charcoal stone',head='flat')
for bid,num in [(248142685,'438'),(248142702,'440')]:elevation(bid,num,'painted ee white brick',4,4,head='molded')

for n in ['402','404']:
 residential(n,at=.81,rise=1.0,top=3.85,positions=(.18,.47),windowWidth=1.20,mat='oak wood');access(n,.81,1.0,1.25,1.65,wellSpans=[[.02,.64]])
door('406',at=.622,w=.85,top=3.22)
residential('410',at=.83,rise=1.75,top=4.6,positions=(.19,.49),windowWidth=1.10,mat='green wood');access('410',.83,1.75,1.3,2.3,wellSpans=[[.02,.64]])
residential('412',at=.64,rise=1.95,top=4.9,positions=(.065,.17,.29,.41,.78,.94),windowWidth=.66,mat='silver metal',w=1.02)
for w in BY['412'][0]['windows'][-6:]:
 if w['at'] in [.17,.78]:w['width']=1.06/BY['412'][1]['length']
access('412',.64,1.95,1.5,2.7,wellSpans=[[.015,.53],[.75,.99]])
residential('416',rise=1.95,top=4.7,positions=(.10,.28,.72,.90),windowWidth=1.10);access('416',.5,1.95,1.55,2.7)
for at in [.10,.28,.72,.90]:win(BY['416'][0],BY['416'][1],at,-.15,1.1,1.45,shape='segmental',grille=True)
door('418',at=.84,w=1.02,top=2.95);win(BY['418'][0],BY['418'][1],.35,.48,3.1,2.0,grille=True,columns=3)
for at in [.20,.65]:win(BY['418'][0],BY['418'][1],at,3.35,1.52,1.4,columns=2)
access('418',.84,.18,1.1,.35,well=False)
residential('418.5',at=.20,rise=.20,top=2.25,positions=(),w=.85)
for at in [.24,.74]:win(BY['418.5'][0],BY['418.5'][1],at,2.6,.95,1.5,grille=True)
for n,at,positions in [('420',.82,(.20,.46)),('422',.18,(.54,.81))]:
 residential(n,at=at,rise=1.8,top=4.65,positions=positions,windowWidth=1.10,mat='oak wood',shape='segmental');access(n,at,1.8,1.35,2.35,wellSpans=[[.02,.63]] if n=='420' else [[.37,.98]])
residential('424',at=.43,rise=1.8,top=4.65,positions=(.09,.26,.60,.76,.92),windowWidth=1.0,mat='oak wood',shape='segmental');access('424',.43,1.8,1.45,2.5,wellSpans=[[.015,.34],[.53,.99]])
residential('426',rise=.32,top=3.3,positions=(.21,.79),windowWidth=1.75,mat='gray metal');BY['426'][0]['e09East']['pairedParlor']=True
door('428',w=.94,low=.35,top=3.30,mat='oak wood');access('428',rise=.35,depth=.7)
residential('430',rise=2.0,top=5.,positions=(.12,.29,.72,.89),windowWidth=.86,w=1.25);access('430',.5,2.,1.6,2.8,wellSpans=[[.015,.36],[.65,.985]])
door('432',at=.945,w=.81,top=3.1,mat='oak wood')
for n in ['434','436','438','440']:door(n,top=3.2)
BY['434'][0]['doors'][0]['material']='ee blue yellow door'

# School: one irregular footprint, eight articulated planes, no repeated shops.
for idx in [4,3,2,1,0,5,6,7]:
 num=f'PS122-{idx}'
 a,f=elevation(248142955,num,'red brick',0,0,'cream stone','school',False,idx=idx,school=True,head='none')
 a['e09East'].update(rows=3,upperBottom=7.0,step=5.0)
 if idx in [0,4]:groups=[(.5,4.8,3)]
 elif idx in [1,3]:groups=[(.20,2.6,2),(.5,1.0,1),(.80,2.6,2)]
 else:groups=[(.29,1.10,1),(.71,1.10,1)]
 for row in range(3):
  for col,(at,w,lights) in enumerate(groups):
   win(a,f,at,7.+row*5.,w,3.65,columns=lights,rails=[.31,.74],row=row,col=col,frame='ee school green',schoolPointed=(lights==1 and idx in [1,2,3,6]))
 if idx in [2,6]:
  door(num,w=1.7,low=1.05,top=4.65,mat='red wood',leaves=2,label='')
  access(num,rise=1.05,width=2.0,depth=1.85,wellSpans=[[.01,.23],[.77,.99]])
 else:
  if idx in [1,3]:ground=[(.11,1.05,1),(.30,1.05,1),(.50,1.05,1),(.70,1.05,1),(.89,1.05,1)]
  else:ground=groups
  for at,w,lights in ground:win(a,f,at,1.45,w,3.5,columns=lights,rails=[.42,.76],frame='ee school green',grille=True,schoolPointed=idx in [1,3])
  a['observedGround']['basementAreaways']=[{'at':.5,'width':.97,'depth':.95,'depthBelow':.65}]

# Avenue A north corner: service hatch and blank burgundy side, distinct returns.
a,f=elevation(248142963,'145A-Ninth','painted ee white brick',5,3,'charcoal stone','plain',False,positions=[.18,.36,.83],bottom=3.8,windowHeight=1.64,head='flat',groundPaint='ee burgundy',ralphSide=True)
a,f=elevation(248142963,'145A-Avenue','painted ee white brick',5,4,'charcoal stone','plain',False,idx=1,bottom=3.8,windowHeight=1.64,head='flat',groundPaint='ee burgundy',ralph=True)
for w in list(a['windows']):
 if w['row']==4 and w['col'] in [0,1]:a['windows'].remove(w)
win(a,f,.25,a['e09East']['upperBottom']+4*a['e09East']['step'],3.0,1.64,columns=3,row=4,col=0,trim='eb charcoal stone')

# South corner and its low Celeste infill retain open sky above the shop.
a,f=elevation(248142716,'141A-Ninth','painted ee white brick',4,3,'brown stone',escapeSpan=[.45,.97],positions=[.52,.69,.87],bottom=3.8,windowHeight=1.80,docSide=True,corniceColor='cream stone',groundPaint='ee burgundy')
for row in range(4):
 a['e09East'].setdefault('blindWindows',[]).append({'at':.35,'bottom':3.8+row*a['e09East']['step'],'width':.94,'height':1.8})
door('141A-Ninth',at=.94,w=.78,top=3.05,label='')
a,f=elevation(248142716,'141A-Avenue','painted ee white brick',4,4,'brown stone',idx=1,bottom=3.8,windowHeight=1.8,doc=True,corniceColor='cream stone',groundPaint='ee burgundy')

# Existing 148 First: only the previously deferred Ninth face; exact mass retained.
base148=next(r for r in json.loads((ROOT/'model-source/east-village-p02/schedule.json').read_text())['elevations'] if r['buildingId']==248142713)
a,f=elevation(248142713,'148-Ninth','p02 aged cream stucco',0,0,'brown stone','plain',False,idx=1,height=base148['buildingHeight'],head='flat',marketSide=True)
for row,y in enumerate([4.0,7.2,10.3]):
 for col,at in enumerate([.58,.67,.79,.89]):win(a,f,at,y,.58 if row else (.95 if col==0 else .52),1.15 if row else (1.9 if col==0 else 1.03),row=row,col=col,trim='p02 salmon lintel')
for col,at in enumerate([.10,.26,.41]):win(a,f,at,4.0,1.10,1.92,row=0,col=col+4,trim='p02 salmon lintel')
door('148-Ninth',at=.33,w=1.10,low=.65,top=3.25,label='400');access('148-Ninth',.33,.65,1.4,1.1,wellSpans=[[.015,.23]])
win(a,f,.12,1.0,2.1,1.9,grille=True,columns=2)

for w in BY['427'][0]['windows']:w['frame']='eb white wood';w['columns']=2
for n in ['406','431','433']:
 for w in BY[n][0]['windows']:w['frame']='eb white wood'
for a,f,bid,idx in BY.values():
 if a['e09East'].get('school'):
  for w in a['windows']:
   if w.get('schoolPointed'):w['shape']='pointed'
  for d in a['doors']:d['shape']='pointed'
BY['431'][0]['doors'][0]['panels']=[{'y':.56,'height':.78,'width':.75,'glass':True}]
BY['431'][0]['doors'][0]['label']='431 E 9TH'

# Business geometry declarations follow below; scopes remain individual.
shop('411','411 west studio — dated tenant unresolved',[.02,.405],'411west',[['glass',.73],['door',.27]],'Blue-gray carved frame, shallow straight fabric shade, closed silver rectangular grille.',frame='blue metal')
shop('411','411 east salon — dated tenant unresolved',[.615,.985],'411east',[['door',.28],['glass',.72]],'Separate blue-gray molded frame, left entrance, broad display, white chair and plants; no invented logo.',frame='blue metal')
shop('435','Psychic / Tarot Card Reading',[.015,.415],'psychic',[['glass',.70],['door',.30]],'Burgundy curved canopy, flowing white Psychic script, side TAROT CARD READING, white frame, oval door grille and wire chair.',frame='white wood')
shop('435','Evil Katsu',[.62,.99],'katsu',[['door',.28],['glass',.72]],'White sign box with angular blue EK, small Evil Katsu wording, separate dark closed roller shutter.')
shop('437','La Fleur Cafe',[.015,.415],'lafleur',[['glass',.72],['door',.28]],'Dark green surround, brilliant green leaf illustration and pink script, silver roll grille.',frame='green wood')
shop('437','Mr. Throwback',[.62,.99],'throwback',[['door',.28],['glass',.72]],'Multicolor athletic wordmark, black frame/grille, numbered sports jerseys and layered garments behind glass.')
shop('439','Neighborhood Barbers',[.015,.415],'barbers',[['glass',.72],['door',.28]],'Tan curved canopy with gold badge, green carved frame, portrait-grid window, striped barber pole, green chair, mirror/salon chair.',frame='green wood')
shop('439','439 east vacant shop',[.62,.99],'439vacant',[['door',.28],['glass',.72]],'Gray blank fascia, closed silver grille, lease placard behind glass, tagged dark lower panels.',frame='gray metal')
shop('441','Poke & Roll',[.015,.415],'poke',[['glass',.72],['door',.28]],'Blue raised capitals on white brick, black window and right entry, food-image band, round blue blade and angled lamps.')
shop('441','441 east vacant storefront',[.62,.99],'441vacant',[['door',.28],['glass',.72]],'Black metal glazing, large pale lease poster, two red stools in closed interior, plain fascia.')
shop('443','Social Tees Animal Rescue',[.015,.415],'socialtees',[['glass',.72],['door',.28]],'Gold outlined dog/lettering on black glass, right entrance, wood slat bench, paper notices and rescue window layers.')
shop('443','Hello Yam',[.62,.99],'yam',[['door',.28],['glass',.72]],'Black frame, left entrance with red EXIT, pink/yellow yam icon and yellow wordmark, white stools/counter.')
shop('445','Village Creperie',[.015,.415],'creperie',[['glass',.72],['door',.28]],'Deep blue/ochre striped retractable canopy with scalloped valance, round cream blade, white round tables, woven chairs, menu board and bulbs.')
shop('445','Villager Smoke Shop',[.62,.925],'smoke',[['door',.27],['glass',.73]],'Brown horizontal wood slats, raised white/red-shadow lettering and left badge, 445 at right, closed silver shutter with multicolor bubble mural.',frame='oak wood')
shop('145A-Avenue',"Ralph’s Famous Italian Ices",[.015,.985],'ralph',[['glass',1]],'Service hatch and projecting ledge surrounded by white picture menus; deep curved blue canopy with white center red script/yellow mascot.',customShell=True)
shop('145A-Ninth',"Ralph’s — short Ninth canopy return",[.77,.995],'ralphside',[['glass',1]],'Short curved blue canopy return above solid burgundy wall, service panels only; no invented entry.',customShell=True)

shop('406','Tsumiki Hair',[.012,.25],'tsumiki',[['glass',.72],['door',.28]],'Narrow black straight sloping fabric shade, small gold cursive name, closed grille with pink bubble graffiti.')
shop('406','Whitmans',[.265,.575],'whitmans',[['door',.28],['glass',.72]],'Independent black shade with spaced white block name, black glazing and cream lower panels, warm exposed bulbs, white outdoor chairs.')
shop('406','Flower Power Herbs & Roots',[.67,.99],'flowerpower',[['glass',.73],['door',.27]],'Ochre ribbed wood surround, hand-painted pale yellow sunflower/blue curved lettering, dark right door, botanical/jar display and brass fittings.',frame='yellow wood')
shop('412','414 basement shop — tenant unresolved',[.015,.53],'414basement',[['glass',.76],['door',.24]],'Dark hood with four gooseneck lamps, closed horizontal shutter over large east window, narrower west entry and 414 hood number.',top=2.15,head=1.91,base=.14)
shop('412','412 west basement shop — tenant unresolved',[.75,.99],'412basement',[['door',.31],['glass',.69]],'Short gold/brown hood with goosenecks, pale metal window and separate shallow descent; sign is blurred.',frame='gray metal',top=2.15,head=1.91,base=.14)
shop('420','Fucking Awesome / FA',[.015,.63],'fa',[['glass',.345],['glass',.345],['door',.31]],'Two rounded display panes in glossy black wood, separate metal hoods, carved scrolling fascia, narrow west door, warm wood displays and two lamps.',top=2.18,head=1.93,base=.15)
shop('422','Good Beer — July 2022 frontage; subsequently closed',[.37,.985],'422basement',[['door',.31],['glass',.69]],'Narrow east door and broad glass with stacked gold GOOD BEER, separate pale metal hoods, three silver lamps and bottle shelving. Historical appearance, closed September 2022.',top=2.18,head=1.93,base=.15)
shop('424','Dr. Green',[.015,.34],'drgreen',[['glass',.70],['door',.30]],'Dark green painted frame, circular green illustrated sign and white script, metal tagged hood, narrow entry and merchandise.',frame='green wood',top=2.18,head=1.93,base=.15)
shop('424','Thursday Kitchen',[.53,.99],'thursday',[['glass',.38],['door',.24],['glass',.38]],'Carved dark scroll fascia, inset amber lit sign with black hand lettering/wood character, industrial silver caged lamp, red center door and warm interior; raw timber curb enclosure.',top=2.18,head=1.93,base=.15)
shop('428','428 east shop — tenant unresolved',[.015,.405],'428east',[['glass',.70],['door',.30]],'Carved dark wood fascia, ornate arched display and diamond grille, narrow right entry, layered ceramics behind glass.',frame='oak wood')
shop('428','Throwback 2',[.62,.99],'throwback2',[['door',.28],['glass',.72]],'Separate black carved frame, narrow left open door, broad right window, silver rectangular grilles, red distressed banner and independent flat metal hoods.')
shop('430','Salads Days — July 2022 frontage',[.015,.36],'salads',[['glass',.68],['door',.32]],'White fascia with two-line italic green name, glass and pale metal frames, low access beside high stoop.',frame='white wood',top=2.18,head=1.93,base=.15)
shop('430','Whiskers',[.65,.99],'whiskers',[['door',.30],['glass',.70]],'Orange banner with blue/cream letters and cat/dog illustration, green painted frame and grille, small red sloping shade.',frame='green wood',top=2.18,head=1.93,base=.15)
shop('432','Chiro-Fit — wood-fronted premises',[.015,.87],'chiro',[['glass',.17],['glass',.17],['glass',.17],['glass',.17],['door',.16],['door',.16]],'Tall reddish timber panels with rounded glass heads, molded kick panels and muted olive fascia; separate residential door at far west.',frame='oak wood')
shop('434','Love Only',[.015,.415],'loveonly',[['glass',.71],['door',.29]],'Black rounded cloth canopy, thin white serif name, white frame and closed rectangular silver grille.',frame='white wood')
shop('434','434 west shop — tenant unresolved',[.62,.99],'434west',[['door',.29],['glass',.71]],'Gold ochre carved surround with scroll brackets, metal hood and silver shutter; preserves September 2024 paint.',frame='gold metal')
shop('436','Nicebrow',[.015,.415],'nicebrow',[['glass',.70],['door',.30]],'White fascia with gold raised lowercase lettering and eyelash ornament, white metal glazing and silver grille.',frame='white wood')
shop('436','436 west star storefront',[.62,.99],'starshop',[['door',.28],['glass',.72]],'Black canopy and white outlined star blade; pale blue star with white central shape painted across grille, red/white lower tags.')
shop('438',"Murphy’s",[.015,.415],'murphys',[['glass',.70],['door',.30]],'Straight blue cloth shade with pale flowing script, hanging/trailing plants, brown bamboo roller screen and blue tagged lower panel.',frame='blue metal')
shop('438','Tacos Cuautla Morelos',[.62,.99],'tacos',[['door',.28],['glass',.72]],'White box fascia with green/red name and red border, green valance, silver/pale glazing, curb dining frame and cones.',frame='white wood')
shop('440','Confectionery',[.015,.415],'confectionery',[['glass',.70],['door',.30]],'Red rounded scalloped canopy with blue cursive name; independent pale frame, closed silver grille.',frame='white wood')
shop('440','Monkey Thrift Shop UpCycling',[.62,.99],'monkey',[['door',.28],['glass',.72]],'Green straight sloping shade, peach lettering and 440 at ends, gold script glass, purple/gold monkey panels and clothing behind grille.',frame='green wood')
shop('141A-Avenue',"Doc Holliday’s Bar",[.015,.99],'docave',[['glass',.33],['door',.21],['glass',.46]],'Mauve rounded ribbed canopy with white slab serif text, dark wood bar windows, poster-covered door, beer tubes and stickers.',frame='oak wood')
shop('141A-Ninth',"Doc Holliday’s — Ninth frontage",[.015,.89],'docside',[['glass',1]],'Short wrap canopy over corner window, red/orange cowboy mural across solid wall, independent west bar window; giant STIK figure on upper blank corner.',customShell=True)
shop('141A-Ninth','Celeste Hair Studio — low infill',[1.006,1.218],'celeste',[['glass',.72],['door',.28]],'One-storey recessed shop in real gap with black sloping CELESTE shade, closed grille; open iron-railed terrace and string lights above.',customShell=True)
shop('148-Ninth','Lime Tree Market — Ninth enclosure',[.43,.998],'marketside',[['glass',.2] for _ in range(5)],'Long burgundy sloping shade with oval market mark, thin silver clear-sheet enclosure and red low panels; shares existing corner grocery.',customShell=True)

# Source-specific equipment only: no procedural address-based dressing.
for n,positions in {
 '413':[(0,3),(1,3),(2,3)],'417':[(0,0),(1,3)],'421':[(0,0),(2,3)],
 '431':[(0,2),(1,1)],'433':[(0,0)],'435':[(0,0),(1,2)],'437':[(0,0),(1,2),(2,2)],
 '439':[(0,3),(1,0)],'441':[(0,0),(2,1),(3,3)],'443':[(1,0),(2,3)],'445':[(0,0),(1,1),(4,3)],
 '406':[(0,4),(1,5),(2,0),(3,3)],'412':[(0,0),(0,3),(1,5)],'416':[(0,0),(1,4)],
 '426':[(0,0),(2,3)],'428':[(1,3),(2,3)],'430':[(1,0)],'432':[(0,0),(1,2)],
 '434':[(0,0),(1,3)],'436':[(0,0),(1,3),(2,2)],'438':[(0,0),(1,3)],'440':[(0,2),(2,3)],
 '148-Ninth':[(0,5)]}.items():BY[n][0]['e09East']['windowAC']=positions

# Keep actual shop entries clear: wells are negative space beside approaches.
for r in E:
 a=r['architecture'];f=r['sourceFace'];clear=[]
 for sh in a['returnShops']:
  lo,hi=sh['span'];cursor=lo
  for kind,fraction in sh['design']['panels']:
   end=cursor+(hi-lo)*fraction
   if kind=='door':clear.append((cursor-.025,end+.025))
   cursor=end
 wells=[]
 for well in a['observedGround'].get('basementAreaways',[]):
  spans=[(well['at']-well['width']/2,well['at']+well['width']/2)]
  for lo,hi in clear:spans=[p for x,y in spans for p in ([(x,min(y,lo)),(max(x,hi),y)] if x<hi and y>lo else [(x,y)]) if p[1]-p[0]>.045]
  wells.extend({**well,'at':(lo+hi)/2,'width':hi-lo} for lo,hi in spans)
 if 'basementAreaways' in a['observedGround']:a['observedGround']['basementAreaways']=wells
 assert a['observation']['sources'],r['faceId']
 assert r['sourceFace']==next(x['sourceFace'] for x in INV['faces'] if x['faceId']==r['faceId'])
assert {r['faceId'] for r in E}=={r['faceId'] for r in INV['faces']}
result={'schema':1,'id':'01-E09-1A','revision':'E09-EAST-01','scopeFaces':[r['faceId'] for r in E],'elevations':E,'businesses':SHOPS,
 'sourceLedger':'model-source/east-village-e09-east/observations.json','targetCapture':'Individually dated 2024/2022 views and named supplements; not verified October 2026 occupancy',
 'ownership':'40 new buildings, one existing Ninth return; all 254 unrelated models and First-facing 148 architecture protected.',
 'auxiliaryFootprints':[{'owner':248142716,'name':'Celeste one-storey infill','box':[183.891,83.638,187.184,88.2],'height':3.25,'basis':'Visible low shop in mapped gap; depth estimated, open terrace above.'}],
 'counts':{'facades':len(E),'upperAndGroundWindows':sum(len(r['architecture']['windows']) for r in E),'entrances':sum(len(r['architecture']['doors']) for r in E),'shopfronts':len(SHOPS)}}
(OUT/'schedule.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result['counts']))
