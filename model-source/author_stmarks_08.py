"""Manually transcribed St. Marks packet; run after/beside the First packet.

This authors visual estimates, not surveyed geometry. Every face retains its
dated browser observations and the occlusions that limit reconstruction.
"""
from author_first_stmarks_08 import *

buff='first pale buff brick';brown='stmarks brown masonry';gray='seventh grey painted stone'
white='stmarks white stucco';pink='first pink stucco';iron='black iron'
blue='seventh charcoal gray paint';wood='seventh oak recess'

def windows(r,positions,bottom=1.8,height=1.9,width=.13,trim=pale,shape='rectangle',**kw):
    for at in positions:r['windows'].append({**dict(at=at,width=width,bottom=bottom,height=height,trim=trim,frame=iron,hood='flat',shape=shape,rails=[.5]),**kw})

def entry(r,at=.5,rise=1.55,width=.18,number=None,trim=pale,shape='rectangle',**kw):
    d=door(r,at,width,iron,number);d.update(bottom=.17+rise,top=3.05+rise,leafTop=2.55+rise,trim=trim,shape=shape,portal='pilasters',access={'rise':rise,'steps':max(1,round(rise/.18)),'run':max(.28,rise*1.4),'landing':.45,'material':trim,'rails':True},**kw)
    if number:d['labelY']=2.80+rise
    return d

def basement(r,span,at=None,text=None,material=iron,depth=1.02,**kw):
    if at is None:at=(span[0]+span[1])/2
    r['observedGround'].setdefault('basementAreaways',[]).append({'at':at,'width':span[1]-span[0],'depth':depth,'depthBelow':.48,'steps':3,'material':gray})
    d=shop(r,span,[['glass',.60],['door',.40]],material,text,material,top=1.96,head=1.60,base=-.35,**kw)
    if text:d['signs'][0].update(y=1.83,height=.30);d['signs'][0]['lines'][0]['size']=.15
    return d

def fence(r,spans,depth=1.2):
    r['observedGround'].setdefault('groundFences',[]).extend({'span':s,'depth':depth} for s in spans)

def decorate(r,kind='pediment',rows=None):
    for w in r['windows']:
        if rows is None or any(abs(w['bottom']-y)<.01 for y in rows):w.update(hood=kind,moldedHood=kind=='pediment',hoodBacking=kind in ['segmental','round'])

def rowhouse(face,h,rows,bays,wall=red,trim=pale,escape=False,ground=5.5,spacing=2.85,**kw):
    return elevation(face,h,rows if bays else 0,bays,wall,trim,escape=escape,ground=ground,spacing=spacing,**kw)

def parlor(r,door_at=.8,positions=(.17,.46),trim=pale,rise=1.5,number=None,**kw):
    windows(r,positions,2.25,2.0,.15,trim)
    d=entry(r,door_at,rise,.18,number,trim,**kw)
    fence(r,[[.025,door_at-.16]] if door_at>.5 else [[door_at+.16,.975]],1.45)
    return d

def wallbase(r,material,top=4.9,rustic=False):
    r.setdefault('surfaceZones',[]).append({'span':[0,1],'bottom':.17,'top':top,'material':material})
    if rustic:r.setdefault('rustication',[]).append({'bottom':.2,'top':top,'step':.44,'material':material})

def grouped(r,positions,rows,ground,spacing,width=.1):
    r['windows']=[]
    for j in range(rows):windows(r,positions,ground+j*spacing,1.8,width,pale)

def ledge(r,y,material=pale,height=.12):
    r.setdefault('bands',[]).append({'y':y,'height':height,'depth':.15,'material':material})

# Second Avenue north corner. Repeated single/pair/oval groups are separately
# observed; a generic evenly spaced grid would erase this facade's identity.
for face,length_positions in [('241822164:0',[.045,.12,.24,.355,.405,.57,.62,.77,.89,.95]),('241822164:1',[.08,.19,.36,.43,.63,.82,.93])]:
 r=elevation(face,21.1,0,0,buff,olive)
 grouped(r,length_positions,5,4.3,3.15,.048 if face.endswith(':0') else .07)
 for w in r['windows']:
  w.update(hood='segmental' if 10<w['bottom']<14 else 'bracketed',keystone=True,hoodBacking=True)
 for y in [7.0,10.1,13.3,16.4,19.5]:ledge(r,y,pale)
 r['rustication']=[{'bottom':3.9,'top':7,'material':pale,'step':.42}]
 if face.endswith(':0'):
  for y in [7.45,13.75]:windows(r,[.49],y,1.32,.034,pale,'round')
  r['escapes']=[{'at':.635,'width':.24,'levels':[4.15+j*3.15 for j in range(5)],'material':olive}]
  shop(r,[.01,.37],[['glass',.40],['door',.20],['glass',.40]],wood,awning={'material':olive,'y':3.7,'drop':.45,'depth':1.2})
  d=door(r,.425,.08,iron,'37½');d.update(trim=pale,labelMaterial='sign white',labelY=2.60)
  shop(r,[.49,.985],[['glass',.25],['glass',.25],['door',.25],['glass',.25]],wood,awning={'material':iron,'y':3.7,'drop':.42,'depth':.75})
 else:
  shop(r,[.02,.985],[['glass',.28],['glass',.25],['door',.20],['glass',.27]],wood,'CAFE MAUD',olive,awning={'material':olive,'y':3.7,'drop':.45,'depth':1.1})

# 39: recessed taller house and independent narrow masonry projection.
r=rowhouse('241822297:0',14.7,3,3,brown,olive,ground=3.6,spacing=2.8,cornice='plain')
entry(r,.78,1.3,.18,None,olive);fence(r,[[.02,.60]],1.4)
r['mansard']={'bottom':12.2,'top':14.7,'dormers':[.25,.75]}
r=rowhouse('241822297:1',10.25,3,1,buff,pale,ground=3.0,spacing=2.50,cornice='plain')
RECORDS['241822297:1']['buildingHeight']=14.7
r['bodyHeight']=10.25
for w in r['windows']:w.update(width=.65,columns=2,height=1.5)
for y in [4.97,7.47,9.87]:
 for at in [.30,.5,.70]:r.setdefault('ornaments',[]).append({'type':'diamond','at':at,'y':y,'size':.22,'material':'first maroon paint'})
door(r,.5,.63,iron,'39')
r=rowhouse('241822224:0',16.0,3,3,brown,olive,True,ground=6.7,spacing=2.7)
decorate(r,'pediment');parlor(r,.52,[.16,.84],olive,2.0)
basement(r,[.73,.98],text=None);basement(r,[.015,.32],text=None)
r=rowhouse('241822159:0',22.0,5,2,white,pale,ground=6.6,spacing=2.85,cornice='plain')
for w in r['windows']:w.update(width=.30,columns=2,height=1.85)
for j in range(5):
 for at in [.15,.85]:
  for dx in range(9):box_detail(r,at+(dx-4)*.028,6.25+j*2.85,.07,.65,pale,.08)
windows(r,[.15,.85],3.4,2.0,.30,pale,columns=2)
door(r,.15,.23,iron);windows(r,[.60,.85],.3,1.8,.20,pale,grille=True);fence(r,[[.38,.98]],1.5)
r=rowhouse('241822151:0',17.6,3,3,red,pale,ground=7.0,spacing=2.75)
parlor(r,.20,[.52,.84],pale,2.25,hood='pediment');ledge(r,5.8)
r=rowhouse('241822254:0',17.1,3,4,pink,olive,ground=7.15,spacing=2.85)
windows(r,[.17,.83],2.6,3.0,.23,olive,'round',columns=2)
d=entry(r,.5,1.55,.20,None,olive,'round');d.update(leaves=2)
r['signs']=[{'at':.34,'width':.10,'y':3.45,'height':.22,'panel':False,'lines':[{'text':'47','size':.16,'material':iron}]}]
fence(r,[[.03,.34],[.66,.97]],1.4);wallbase(r,pink,5.8,True)
r=rowhouse('241822299:0',16.7,3,3,white,olive,ground=6.2,spacing=2.9)
windows(r,[.15,.50,.85],2.5,2.5,.19,olive,'round');entry(r,.17,.30,.18);fence(r,[[.34,.98]])
r=rowhouse('241822189:0',19.2,4,3,buff,pale,ground=6.7,spacing=2.7)
for w in r['windows']:w.update(shape='round',hood='round',keystone=True)
parlor(r,.80,[.16,.47],pale,1.8,shape='round');wallbase(r,pale,6.0,True)
r=rowhouse('241822338:0',18.2,4,3,brown,brown,ground=6.5,spacing=2.5,cornice='plain')
parlor(r,.80,[.16,.46],brown,1.4);wallbase(r,brown,5.8,True)
r=rowhouse('241822174:0',21.6,5,4,buff,pale,ground=6.25,spacing=2.7)
decorate(r,'bracketed');windows(r,[.19,.81],2.35,2.25,.29,pale,columns=3,grille=True)
d=entry(r,.50,1.2,.25,None,pale);d.update(leaves=2);wallbase(r,pale,5.6,True)
r=rowhouse('241822314:0',17.1,3,3,gray,pale,ground=7.5,spacing=2.65)
for w in r['windows']:
 if w['bottom']<10.5:w.update(shape='pointed',hood='pointed',height=2.45)
windows(r,[.15,.5,.85],2.4,3.1,.19,pale,'pointed',columns=2)
entry(r,.5,1.15,.18,None,pale,'pointed');fence(r,[[.02,.32],[.68,.98]],1.5)
r['awnings']=[{'span':[.01,.99],'y':2.35,'drop':.33,'depth':1.6,'material':'seventh canvas brown'}]
r=rowhouse('241822236:0',16.5,3,3,red,pale,ground=6.7,spacing=2.75,cornice='plain')
parlor(r,.80,[.16,.46],pale,1.7)
r=rowhouse('241822312:0',16.5,3,3,red,pale,ground=6.7,spacing=2.75)
d=parlor(r,.18,[.51,.84],pale,1.7,'61',hood='pediment');d.update(leaves=2,grille=True,labelMaterial='seventh brass lettering')
r=rowhouse('241822282:0',18.54,4,0,brown,pale,ground=6.35,cornice='plain')
grouped(r,[.12,.25,.56,.69,.82],4,6.35,2.7,.10)
windows(r,[.15,.72],2.6,2.15,.25,pale,columns=2,grille=True);entry(r,.49,.38,.16);fence(r,[[.02,.35],[.64,.98]],.9)
r=rowhouse('241822279:0',17.7,4,3,red,brown,True,ground=5.15,spacing=2.8)
decorate(r,'pediment');entry(r,.17,1.1,.20,None,brown);windows(r,[.53,.85],2.8,1.8,.16,brown)
basement(r,[.38,.98],text="JIANG'S KITCHEN",awning={'y':2.6,'drop':.4,'depth':1.0,'material':iron,'text':"JIANG'S KITCHEN   65",'textSize':.13})
r=rowhouse('241822214:0',16.3,4,3,'painted sage',gray,True,ground=4.5,spacing=2.70)
door(r,.18,.17,iron);windows(r,[.64],.55,2.25,.42,gray,columns=2,grille=True)
r=rowhouse('241822291:0',21.83,5,3,red,pale,True,ground=4.5,spacing=3.1,cornice='plain')
scaffold(r,22.4,'69 ST MARKS PL');r['scaffoldGuards']=[{'bottom':3.5,'top':22.4,'depth':1.6,'veil':True}]
entry(r,.5,.30,.25,None,pale,'round');fence(r,[[.02,.34],[.66,.98]])
r=rowhouse('241822230:0',14.93,4,3,brown,brown,ground=4.1,spacing=2.7,cornice='parapet')
windows(r,[.17,.83],.6,2.35,.19,brown,grille=True);door(r,.5,.19,iron)
r=rowhouse('241822267:0',12.9,3,3,white,olive,ground=4.1,spacing=2.8)
r['cornice']['pediment']=True;ledge(r,3.65,pink,.55)
door(r,.16,.16,iron);windows(r,[.51,.85],.65,2.0,.19,olive,grille=True)
r=rowhouse('241822217:0',16.8,4,3,red,brown,True,ground=4.45,spacing=2.8)
decorate(r,'bracketed');door(r,.16,.18,'theater red')
shop(r,[.31,.98],[['glass',.32],['door',.36],['glass',.32]],'metal',awning={'y':3.4,'drop':.60,'depth':1.1,'material':'theater red','text':'75 COCKTAIL LOUNGE','textSize':.17})
r=rowhouse('241822271:0',16.8,4,3,pink,olive,True,ground=4.5,spacing=2.8)
r['cornice']['pediment']=True;entry(r,.79,.75,.19,None,olive);basement(r,[.02,.38]);windows(r,[.46],1.7,1.55,.24,olive)
r['awnings']=[{'span':[.31,.99],'y':3.8,'drop':.5,'depth':1.1,'material':iron,'text':'IL PALAPA','textSize':.17}]
r=rowhouse('241822320:0',19.1,5,1,gray,pale,ground=4.5,spacing=2.7,cornice='plain')
for w in r['windows']:w.update(width=.50,columns=2)
shop(r,[.025,.79],[['glass',.66],['door',.34]],iron);door(r,.90,.12,iron)
r=rowhouse('241822234:0',16.9,4,3,red,brown,True,ground=4.6,spacing=2.8)
decorate(r,'bracketed');shop(r,[.02,.79],[['glass',.45],['door',.55]],iron,'RAMEN',iron,'first mustard paint');door(r,.90,.15,iron)
for face,positions in [('241822219:1',[.28,.72]),('241822219:0',[.40,.51])]:
 r=elevation(face,16.5,0,0,red,brown)
 grouped(r,positions,4,4.35,2.8,.13 if face.endswith(':1') else .064)
 if face.endswith(':1'):shop(r,[.02,.98],[['glass',.36],['glass',.36],['door',.28]],wood,'STROMBOLI',white,'theater red',awning={'material':'theater red','stripe':white,'y':3.6,'drop':.4,'depth':1.0})
 else:
  r['escapes']=[{'at':.45,'width':.22,'levels':[4.2,7,9.8,12.6],'material':iron}]
  shop(r,[.025,.34],[['glass',.64],['door',.36]],wood,'STROMBOLI',white,'theater red');door(r,.395,.06,iron)
  shop(r,[.45,.99],[['glass',.33],['door',.34],['glass',.33]],iron,'CAMINO',iron)

# Second–First south: individual raised entries and forecourts.
for face in ['241822290:1','241822290:0']:
 r=elevation(face,9.7,0,0,buff,pale,cornice='plain')
 wallbase(r,iron,1.7)
 if face.endswith(':1'):
  windows(r,[.17,.87],2.0,3.7,.065,pale,rails=[.25,.50,.75]);windows(r,[.17,.87],6.5,1.3,.065,pale)
  windows(r,[.52],2.0,3.8,.46,pale,columns=5,rails=[]);windows(r,[.52],7.0,1.65,.46,pale,columns=5)
  for j in range(27):box_detail(r,.30+j*.017,6.25,.06,1.2,pale,.10)
  door(r,.065,.065,iron);r['billboard']={'span':[.05,.48],'bottom':9.75,'top':12.2}
 else:
  windows(r,[.30,.72],1.7,5.5,.33,pale,columns=3,rails=[.55]);door(r,.86,.18,iron)
r=elevation('241822310:0',16.95,0,0,buff,pale,cornice=None)
r['bodyHeight']=6.8;r['setbackMass']={'height':16.95,'setback':2.9,'rows':3,'bays':3}
windows(r,[.14,.38,.62,.86],3.8,2.0,.15,pale)
shop(r,[.02,.98],[['glass',.32],['glass',.31],['door',.37]],'theater red','PORTO RICO IMPORTING CO.',white,brown,top=3.5,head=2.8)
r['awnings']=[{'span':[.01,.99],'material':'theater red','text':'COFFEE & TEA','y':2.8,'drop':.28,'depth':.85,'textSize':.19}]
r=rowhouse('241822300:0',16.8,3,2,blue,pale,True,ground=6.25,spacing=2.8)
windows(r,[.28,.72],3.8,1.55,.29,pale,columns=2)
shop(r,[.02,.98],[['glass',.35],['door',.30],['glass',.35]],wood,'anthony AIDEN opticians',iron,'sign white')
r=rowhouse('241822284:0',16.25,3,2,red,pale,ground=6.25,spacing=2.8)
parlor(r,.77,[.25],pale,1.65,shape='round');basement(r,[.05,.43]);r['signs']=[{'at':.57,'width':.12,'y':3.4,'height':.26,'material':'sign white','lines':[{'text':'42½','material':iron,'size':.13}]}]
r=rowhouse('241822306:0',16.2,3,3,brown,brown,ground=6.4,spacing=2.6,hood='segmental')
shop(r,[.23,.98],[['glass',.5],['glass',.5]],iron,'Northwell Health','sign white',blue,top=3.5)
entry(r,.12,.45,.14,None,pale);windows(r,[.5,.84],3.8,1.6,.20,pale,grille=True)
r=rowhouse('241822301:0',17.75,3,3,brown,pale,True,ground=6.8,spacing=2.8)
r['escapes'][0]['material']=pale;parlor(r,.83,[.16,.49],brown,1.7)
r=rowhouse('241822265:0',17.6,3,3,red,brown,ground=6.8,spacing=2.8)
windows(r,[.15,.32,.49],2.0,3.6,.15,pale,'pointed',columns=2)
d=entry(r,.82,1.2,.22,None,pale);r['signs']=[sign('JUBILEE MISSION CENTER',pale,brown,at=.5,width=.97,y=5.9,height=.43)]
fence(r,[[.01,.64]],2.0);r['signs'].append({'at':.82,'width':.12,'y':1.1,'height':.30,'depth':2.6,'material':iron,'lines':[{'text':'48','size':.17}]})
r=rowhouse('241822256:0',17.7,3,3,brown,brown,ground=6.8,spacing=2.8)
parlor(r,.81,[.16,.48],brown,1.75);r['observedGround']['lanterns']=[.65,.965]
r=rowhouse('241822286:0',17.9,4,4,red,pale,True,ground=5.7,spacing=2.55,cornice='plain')
windows(r,[.14,.38,.64],2.0,2.4,.15,pale,grille=True);entry(r,.88,.4,.16);fence(r,[[.02,.73]])
r=rowhouse('241822341:0',23.47,6,0,buff,pale,cornice='plain')
grouped(r,[.08,.19,.31,.69,.81,.92],6,5.15,2.85,.07)
r['balconies']=[{'at':.5,'width':.24,'depth':.72,'y':4.8+j*2.85,'material':pale} for j in range(6)]
for j in range(6):windows(r,[.5],5.15+j*2.85,2.3,.18,pale,columns=2)
d=entry(r,.56,1.0,.23,None,pale);d.update(leaves=2);windows(r,[.14,.85],.3,.85,.20,pale,columns=3,grille=True);wallbase(r,pale,4.45,True)
r=rowhouse('241822190:0',23.4,6,3,'seventh blue gray stone',pale,True,ground=4.85,spacing=2.83)
entry(r,.17,1.2,.20,None,pale);windows(r,[.53,.85],2.75,1.6,.19,pale)
basement(r,[.38,.98],text='VEGAN GRILL',material='awning green');basement(r,[.01,.30],text=None)
r=rowhouse('241822280:0',18.0,4,3,red,pale,True,ground=5.6,spacing=2.7)
windows(r,[.16,.49,.83],2.6,1.9,.18,pale);door(r,.85,.16,iron,'60');windows(r,[.18,.51],.45,1.6,.19,pale,grille=True);fence(r,[[.02,.70]])
r=rowhouse('241822303:0',16.5,2,3,red,pale,ground=10.1,spacing=2.6,cornice='plain')
windows(r,[.17,.83],6.9,1.9,.17,pale)
windows(r,[.5],3.8,5.0,.25,pale,'round',columns=3,rails=[.2,.4,.6,.8])
for at in [.17,.83]:
 d=entry(r,at,1.2,.22,'62' if at>.5 else None,pale,'round');d.update(leaves=2,crossPanels=True,labelSize=.15)
windows(r,[.5],.4,1.45,.30,pale,columns=3,grille=True);wallbase(r,pale,3.1)
r=rowhouse('241822194:0',22.07,5,4,buff,pale,True,ground=6.7,spacing=2.8)
parlor(r,.20,[.52,.84],brown,1.75);wallbase(r,brown,5.9,True)
r=rowhouse('241822181:0',19.0,4,4,buff,pale,ground=6.9,spacing=2.55)
windows(r,[.17,.83],2.8,2.8,.24,pale,'round',columns=2);d=entry(r,.50,1.6,.20,None,pale,'round');d.update(leaves=2)
r['balconies']=[{'at':.5,'width':.36,'depth':.48,'y':6.68,'material':iron}];fence(r,[[.015,.33],[.67,.985]],1.2)
r=rowhouse('241822332:0',17.8,3,3,brown,pale,ground=6.8,spacing=2.9)
d=parlor(r,.82,[.16,.49],pale,1.85);d.update(label='68',labelY=3.35,labelOffset=-.79,labelSize=.16,labelMaterial=iron)
windows(r,[.18,.49],.5,1.5,.17,pale,grille=True)
r=rowhouse('241822167:0',17.35,3,3,brown,pale,True,ground=6.7,spacing=2.85)
r['escapes'][0].update(at=.35,width=.46,material=pale);windows(r,[.16,.49,.83],3.1,1.9,.17,pale);door(r,.82,.17,iron);fence(r,[[.02,.67]],1.4)
r=rowhouse('241822326:0',20.26,5,4,gray,pale,ground=5.55,spacing=2.75,cornice='plain')
for w in r['windows']:w.update(frame='white frame',width=.16,columns=2)
windows(r,[.12,.34,.66,.88],.35,.65,.17,pale,columns=2,grille=True);entry(r,.52,.35,.14);wallbase(r,pale,4.8)
r=rowhouse('241822173:0',18.0,4,4,red,brown,True,ground=6.2,spacing=2.50)
decorate(r,'segmental',[11.2]);windows(r,[.19,.81],2.9,2.4,.28,brown,columns=2)
d=entry(r,.5,1.75,.19,None,pale);d.update(material='east7 navy paint',label='76',labelY=4.3,labelMaterial='seventh brass lettering');fence(r,[[.015,.34],[.66,.98]],1.2)
r=rowhouse('241822323:0',15.5,3,3,white,pale,ground=6.05,spacing=2.6)
parlor(r,.80,[.16,.49],pale,1.5)
r=rowhouse('241822222:0',16.2,3,3,white,pale,True,ground=6.5,spacing=2.65)
r['escapes'][0]['material']='white frame';r['cornice']['pediment']=True
parlor(r,.2,[.53,.84],pale,1.55);wallbase(r,red,1.6)
r['closedShutters']=[{'span':[.01,.98],'bottom':.18,'top':3.1,'material':'awning green'}]
r['observation']['construction']='April 2026 green hoarding takes precedence over exposed September 2024 Theatre 80 canopy.'

# First–Avenue A north, including the long avenue returns.
r=rowhouse('248142711:0',17.1,4,3,red,pale,ground=4.5,spacing=2.85)
decorate(r,'pediment');r['cornice']['pediment']=True
shop(r,[.02,.98],[['glass',.40],['door',.22],['glass',.38]],olive,awning={'material':white,'stripe':iron,'stripeSpacing':.26,'stripeWidth':.10,'y':3.60,'drop':.42,'depth':1.1})
r['closedShutters']=[{'span':[.03,.96],'top':2.9}]
r=elevation('248142711:1',17.1,0,0,red,pale)
grouped(r,[.06,.17,.28,.39,.50,.61,.72,.83,.94],4,4.5,2.85,.041)
for w in r['windows']:w['hood']='bracketed'
r['windows']=[w for w in r['windows'] if abs(w['at']-.72)>.01]
r['escapes']=[{'at':a,'width':.18,'levels':[4.36,7.21,10.06,12.91],'material':iron} for a in [.29,.83]]
shop(r,[.02,.30],[['glass',.62],['door',.38]],iron,'BEER   SMOKE',iron);door(r,.345,.045,iron)
shop(r,[.40,.985],[['glass',.24],['glass',.24],['door',.24],['glass',.28]],olive,'GOODNIGHT SONNY',olive,awning={'material':olive,'y':3.65,'drop':.42,'depth':1.05})
r=rowhouse('248142686:0',16.2,3,6,white,pale,ground=6.1,spacing=2.8)
r['cornice'].update(pediment=True,pedimentAt=.75,pedimentWidth=.22)
for at in [.34,.85]:entry(r,at,1.7,.09,None,brown)
windows(r,[.08,.20,.58,.70],2.5,2.2,.075,pale);wallbase(r,brown,2.3);fence(r,[[.02,.25],[.44,.76],[.95,.99]],1.4)
r=rowhouse('248142688:0',16.8,3,3,red,pale,ground=6.4,spacing=2.75)
r['windows']=[w for w in r['windows'] if w['bottom']<11.9]
windows(r,[.13,.43,.57,.87],11.9,1.85,.13,pale)
d=entry(r,.20,1.65,.27,None,pale);d.update(leaves=2);windows(r,[.59,.85],2.5,2.2,.17,pale)
for at in [.39,.93]:box_detail(r,at,3.2,.30,.42,'east7 bronze')
fence(r,[[.43,.98]],1.25)
r=rowhouse('248142691:0',17.0,3,4,buff,pale,True,ground=6.5,spacing=2.8,cornice='parapet')
r['escapes'][0].update(at=.35,width=.42);windows(r,[.13,.38,.65,.89],3.0,1.8,.14,pale)
entry(r,.66,.38,.16);windows(r,[.14,.38,.88],.50,1.8,.15,pale,grille=True)
r=rowhouse('248142694:0',18.1,5,3,'painted sage',gray,True,ground=4.15,spacing=2.55,cornice='plain',hood='segmental')
shop(r,[.02,.79],[['glass',.65],['door',.35]],olive,'CECILIA',olive);door(r,.90,.14,iron)
for face,pos in [('248142698:0',[.10,.36,.63,.90]),('248142696:0',[.25,.75])]:
 r=elevation(face,20.3,0,0,buff,pale,escape=False,cornice='plain')
 grouped(r,pos,5,4.75,2.85,.135 if face.startswith('248142698') else .23)
 for w in r['windows']:w.update(shape='segmental',hood='segmental')
 if face.startswith('248142698'):
  r['escapes']=[{'at':.58,'width':.62,'levels':[4.6+j*2.85 for j in range(5)],'material':iron}]
  door(r,.16,.16,iron,'99');basement(r,[.34,.98],text='EAST VILLAGE BOOKS',material='theater red')
 else:basement(r,[.03,.98],material='first teal paint')
r=rowhouse('248142616:0',18.65,4,6,red,brown,True,ground=6.6,spacing=2.6)
decorate(r,'pediment');r['escapes'][0].update(at=.38,width=.42)
windows(r,[.10,.25,.42,.82,.94],2.7,2.1,.075,brown)
d=entry(r,.65,1.75,.16,None,brown,'round');d.update(access={**d['access'],'material':'theater red'});wallbase(r,brown,5.7,True)
basement(r,[.02,.49],text='CAFE MOGADOR',material=olive);basement(r,[.78,.98],text=None,material=wood)
r['awnings']=[{'span':[.01,.51],'y':2.3,'drop':.25,'depth':1.15,'material':olive,'text':'CAFE MOGADOR','textSize':.16},{'span':[.77,.99],'y':2.3,'drop':.25,'depth':.85,'material':olive}]
r=rowhouse('248142619:0',19.7,5,6,red,pale,True,ground=5.25,spacing=2.65,cornice='plain')
r['escapes'][0].update(at=.36,width=.45);entry(r,.83,1.2,.14,None,pale);windows(r,[.13,.30,.48,.63],2.65,1.7,.10,pale)
basement(r,[.02,.55],text='ANJELLY   103',material=white,letters='east7 navy paint');ledge(r,4.65,white,.5)
r=rowhouse('248142620:0',19.7,5,0,brown,brown,ground=5.0,cornice='plain')
grouped(r,[.055,.095,.19,.23,.275,.40,.44,.56,.60,.73,.77,.81,.91,.95],5,5.0,2.75,.028)
r['escapes']=[{'at':a,'width':.17,'levels':[4.85+j*2.75 for j in range(5)],'material':iron} for a in [.25,.75]]
for at in [.08,.26,.44,.64,.84]:windows(r,[at],.5,2.35,.09,brown,columns=2,grille=True)
entry(r,.54,.4,.06,None,brown);fence(r,[[.01,.48],[.60,.99]],.7)
r=rowhouse('248142622:0',22.6,6,3,buff,pale,True,ground=5.0,spacing=2.62)
for w in r['windows']:w.update(shape='round' if w['bottom']>15 else 'segmental',hood='round' if w['bottom']>15 else 'pediment',keystone=True)
d=entry(r,.5,.55,.24,None,pale,'round');d.update(leaves=2,label='109 ST MARKS',labelY=3.36,labelSize=.12)
for span in [[.01,.31],[.69,.99]]:
 shop(r,span,[['glass',.65],['door',.35]],wood,top=2.75,head=2.35,awning={'y':2.85,'drop':.48,'depth':1.1,'material':'seventh canvas brown'})
r=rowhouse('248142625:0',16.6,4,3,red,pale,True,ground=4.5,spacing=2.7)
decorate(r,'bracketed');r['cornice']['pediment']=True;door(r,.5,.20,iron);windows(r,[.16,.84],.6,2.25,.19,pale,grille=True);wallbase(r,pale,3.7,True)
r=rowhouse('248142627:0',16.4,4,3,red,pale,True,ground=4.4,spacing=2.7)
scaffold(r,17.0,'113 ST MARKS');r['scaffoldGuards']=[{'bottom':3.5,'top':17.,'depth':1.6,'veil':True}]
shop(r,[.02,.76],[['glass',.62],['door',.38]],iron,'CRIF DOGS',iron);door(r,.87,.16,iron,'113')
r['blades']=[{'at':.30,'y':2.8,'width':.75,'height':.4,'depth':.85,'material':white,'text':'CRIF DOGS','textMaterial':iron}]
r=rowhouse('248142630:0',20.0,5,6,red,pale,True,ground=4.8,spacing=2.8)
decorate(r,'bracketed');r['closedShutters']=[{'span':[.03,.45],'top':2.9},{'span':[.54,.97],'top':2.9}]
r['awnings']=[{'span':[.01,.99],'material':gray,'y':3.5,'drop':.4,'depth':1.0,'text':'AUGERSWELL','textSize':.25}]
r=rowhouse('248142636:0',20.3,5,6,red,pale,True,ground=4.8,spacing=2.85)
decorate(r,'bracketed');shop(r,[.02,.98],[['glass',.31],['door',.25],['glass',.44]],wood,'HANOI HOUSE',iron)
r['signs'].append({'at':.91,'width':.10,'y':3.08,'height':.24,'panel':False,'lines':[{'text':'No. 119','size':.10}]})
for face,h in [('248142641:0',20.3),('248142709:1',20.3)]:
 r=elevation(face,h,0,0,white,pale)
 grouped(r,[.09,.18,.39,.50,.61,.82,.91],5,4.8,2.85,.055)
 for w in r['windows']:w.update(hood='pediment',moldedHood=True)
 r['escapes']=[{'at':.18,'width':.26,'levels':[4.65+j*2.85 for j in range(5)],'material':iron}]
 if face.startswith('248142641'):
  r['escapes'].append({'at':.82,'width':.26,'levels':[4.65+j*2.85 for j in range(5)],'material':iron})
  shop(r,[.01,.41],[['glass',.5],['door',.5]],wood);entry(r,.50,.36,.10,None,pale)
  shop(r,[.59,.99],[['door',.25],['glass',.35],['glass',.40]],olive,'MOODY TONGUE',olive)
 else:
  shop(r,[.01,.44],[['glass',.50],['door',.50]],wood)
  shop(r,[.47,.99],[['glass',.30],['door',.25],['glass',.45]],olive,'STARBUCKS',olive)
r=elevation('248142709:0',20.3,0,0,white,pale)
grouped(r,[.055,.115,.26,.32,.46,.52,.69,.75,.91,.96],5,4.8,2.85,.032)
r['escapes']=[{'at':.50,'width':.18,'levels':[4.65+j*2.85 for j in range(5)],'material':iron}]
for y in [7.65,13.35]:windows(r,[.60],y,1.3,.025,pale,'round')
shop(r,[.01,.35],[['glass',.35],['door',.3],['glass',.35]],olive,'STARBUCKS',olive)
d=door(r,.40,.055,iron,'131');d['labelMaterial']='seventh brass lettering'
shop(r,[.46,.81],[['glass',.65],['door',.35]],wood)
shop(r,[.84,.99],[['glass',.6],['door',.4]],'white frame')

# First–Avenue A south; paired ornamental tenements stay distinct at ground.
r=rowhouse('248142687:0',16.0,4,3,pink,olive,ground=4.35,spacing=2.8)
decorate(r,'bracketed');r['cornice']['pediment']=True;entry(r,.80,.4,.18,None,olive);windows(r,[.19,.49],.9,2.1,.19,olive,grille=True)
r=rowhouse('248142689:0',16.2,4,4,red,iron,ground=4.5,spacing=2.8)
for y in [6.85,9.65,12.45]:
 for at in [.22,.50,.78]:r.setdefault('ornaments',[]).append({'type':'diamond','at':at,'y':y,'size':.17,'material':iron})
entry(r,.5,.55,.19,None,iron,'round');windows(r,[.17,.83],.95,2.0,.27,iron,columns=2)
r['signs']=[sign('FUN CITY TATTOO','theater red',at=.5,width=.96,y=3.65,height=.45)]
for face in ['248142692:0','248142695:0']:
 r=rowhouse(face,18.0,4,4,buff,pale,True,ground=6.0,spacing=2.6)
 r['escapes'][0]['material']='seventh blue gray stone';r['cornice']['pediment']=True;decorate(r,'pediment')
 for w in r['windows']:
  if w['bottom']==6.0:w.update(shape='round',hood='round')
 entry(r,.5,1.55,.21,None,'seventh blue gray stone','round');windows(r,[.17,.83],2.6,2.4,.23,pale,'round',columns=2)
 basement(r,[.02,.32],text='XING FU TANG' if face.startswith('248142692') else None)
 basement(r,[.68,.98],text='Physical GraffiTea' if face.startswith('248142692') else None)
r=rowhouse('248142614:0',18.0,4,4,red,pale,True,ground=6.2,spacing=2.5)
decorate(r,'bracketed');d=entry(r,.5,1.45,.20,None,brown);d.update(label='100',labelY=4.08,labelMaterial='sign white')
windows(r,[.12,.27,.73,.88],2.45,2.3,.12,pale)
basement(r,[.02,.33]);basement(r,[.68,.98],text='DUMPLING MAN',material='east7 navy paint')
r=rowhouse('248142617:0',17.4,4,4,red,red,True,ground=5.7,spacing=2.55,hood='segmental')
shop(r,[.45,.98],[['glass',.64],['door',.36]],wood);entry(r,.21,.5,.18);windows(r,[.14,.40,.68,.90],3.6,1.3,.14,pale)
r=rowhouse('248142717:0',11.3,2,0,red,pale,ground=5.45,cornice='plain')
grouped(r,[.09,.18,.33,.43,.60,.69,.86,.95],2,5.45,2.6,.055)
d=entry(r,.10,1.45,.085,None,pale);d.update(label='106',labelY=3.4,labelMaterial='seventh brass lettering')
windows(r,[.27,.42,.60,.75,.90],2.4,2.1,.065,pale);fence(r,[[.19,.99]],1.4)
r=rowhouse('248142623:0',20.6,5,6,buff,pale,True,ground=4.9,spacing=2.85)
decorate(r,'pediment');shop(r,[.02,.77],[['glass',.34],['glass',.33],['door',.33]],'white frame',top=3.8,head=2.7)
door(r,.83,.085,'white frame');door(r,.95,.065,iron)
r=rowhouse('248142628:0',15.8,3,3,red,brown,ground=6.5,spacing=2.6)
parlor(r,.80,[.16,.48],brown,1.45)
r=rowhouse('248142631:0',16.0,4,3,red,pale,True,ground=4.5,spacing=2.65)
door(r,.15,.18,wood);shop(r,[.30,.98],[['glass',.36],['glass',.34],['door',.30]],'theater red')
r=rowhouse('248142634:0',16.5,4,4,white,pale,True,ground=4.7,spacing=2.7)
d=door(r,.13,.17,iron);d.update(shape='round',top=3.1)
shop(r,[.26,.985],[['door',.26],['glass',.74]],'theater red',"ROMEO'S",white,'theater red')
r['signs'].append({'at':.37,'width':.10,'y':2.62,'height':.22,'panel':False,'lines':[{'text':'118','material':'theater red','size':.14}]})
r=rowhouse('248142638:0',20.8,5,4,'first mustard paint',pale,True,ground=5.0,spacing=2.85,cornice='plain')
windows(r,[.17,.43,.70],.45,2.7,.16,pale,grille=True);door(r,.90,.14,iron)
for face in ['248142643:0','248142649:0']:
 r=rowhouse(face,20.1,5,6,red,pale,True,ground=5.1,spacing=2.8)
 decorate(r,'pediment');entry(r,.50,.8,.12,None,pale)
 shop(r,[.02,.40],[['glass',.55],['door',.45]],wood,awning={'y':3.45,'drop':.4,'depth':1.05,'material':white,'stripe':iron})
 shop(r,[.60,.98],[['door',.35],['glass',.65]],wood,'HOLY LAND MARKET' if face.startswith('248142643') else None,white,iron)
 if face.startswith('248142643'):
  r['closedShutters']=[{'span':[.61,.975],'top':2.7}]
  r['signs'].append({'at':.94,'width':.08,'y':3.1,'height':.21,'panel':False,'lines':[{'text':'122','material':iron,'size':.13}]})
r=rowhouse('248142652:0',16.0,4,4,pink,pale,True,ground=4.5,spacing=2.65,cornice='parapet')
d=door(r,.5,.21,iron,'128');d.update(trim=pale,portal='pilasters',hood='pediment',labelMaterial='sign white',labelY=2.35)
windows(r,[.17,.83],.65,2.25,.22,pale,grille=True)
r=rowhouse('248142655:0',16.2,4,4,red,pale,True,ground=4.5,spacing=2.7,cornice='plain')
r['closedShutters']=[{'span':[.02,.36],'top':2.9}];door(r,.45,.13,iron)
shop(r,[.56,.98],[['glass',.62],['door',.38]],iron,awning={'material':iron,'y':3.5,'drop':.40,'depth':.85,'text':'Cafe Aperitif','textMaterial':'seventh brass lettering','textSize':.14})
r=elevation('248142706:0',20.0,0,0,red,pale)
grouped(r,[.055,.18,.25,.40,.47,.62,.69,.86,.95],5,4.9,2.85,.043)
decorate(r,'bracketed');r['escapes']=[{'at':.51,'width':.35,'levels':[4.75+j*2.85 for j in range(5)],'material':iron}]
shop(r,[.01,.82],[['glass',.20],['glass',.20],['door',.20],['glass',.20],['glass',.20]],wood,smallPanes=True)
door(r,.93,.07,iron);r['entryProjection']={'span':[.865,.995],'height':3.3,'depth':.75}
r=elevation('248142706:1',20.0,0,0,red,pale)
grouped(r,[.12,.29,.57,.86],5,4.9,2.85,.115)
decorate(r,'bracketed');shop(r,[.02,.98],[['glass',.66],['door',.34]],wood,smallPanes=True)
r['blades']=[{'at':.75,'y':3.25,'width':.7,'height':.6,'depth':.8,'material':white,'text':'BAR AL PASTOR','textMaterial':iron}]

# Repairs caught by the opening audit: a low entrance replaces its own
# opening, never a window stacked across the same aperture.
for key,indices in {
 '241822290:0':[1], '241822297:0':[2],
 '241822299:0':[9], '241822314:0':[10],
 '241822326:0':[22], '248142691:0':[14],
}.items():
 a=RECORDS[key]['architecture'];a['windows']=[w for i,w in enumerate(a['windows']) if i not in indices]
# 38's avenue glass stops at the independent entry instead of overlapping it.
windows(RECORDS['241822290:0']['architecture'],[.62],1.7,5.5,.24,pale,columns=2,rails=[.55])
# First/132's observed lateral ramp has an explicit end height and rail.
a=RECORDS['248142712:1']['architecture']
a['doors'].append({'at':.95,'width':.07,'bottom':.48,'top':2.95,'leafTop':2.55,'trim':'white frame','material':'white frame','access':{'material':gray,'ramp':{'start':[-3.0,.17,1.0],'end':[0,.48,1.0],'width':.85}}})
for d in a['returnShops']:
 if d['span'][1]>.9:d['span'][1]=.89
# Sign helper uses explicit lines; readable blades must not silently drop text.
for record in RECORDS.values():
 for blade in record['architecture'].get('blades',[]):
  if 'text' in blade:blade['lines']=[{'text':blade['text'],'material':blade.get('textMaterial','sign white'),'size':.12}]
# Source-to-render refinements of the ornate corner and parlor tenement.
for key in ['241822164:0','241822164:1']:
 a=RECORDS[key]['architecture']
 for w in a['windows']:
  if w['at']<.20 or w['at']>.85:
   w.update(moldedHood=True,hood='pediment',surround=True)
 for at in [.01,.19,.86,.985]:a.setdefault('piers',[]).append({'at':at,'width':.02,'bottom':4.0,'top':20.0,'material':pale,'joints':True})
a=RECORDS['241822181:0']['architecture'];decorate(a,'segmental')
for w in a['windows']:w['surround']=True
a=RECORDS['241822280:0']['architecture'];a['windows'][14].update(bottom=3.15,height=1.35)
a=RECORDS['241822271:0']['architecture'];a['escapes'][0]['material']=pale
a['awnings'][0].update(text='LA PALAPA',material='stmarks tan canvas',letters=iron)
a=RECORDS['241822217:0']['architecture'];a['returnShops'][0]['design']['awning']['shape']='round'
a['doors'][0]['panels']=[];circle(a,.16,1.95,.15,iron,-.075)
a=RECORDS['241822279:0']['architecture'];a['returnShops'][0]['design']['signs']=[]
a=RECORDS['241822303:0']['architecture']
for w in a['windows']:
 if w['at']==.5 and w['height']==5.0:w['rails']=[j/10 for j in range(1,10)]
for d in a['doors']:
 d['panels']=[];d['crossPanels']=False
 for offset in [-.055,.055]:
  box_detail(a,d['at']+offset,2.75,.06,.65,'seventh brass lettering',-.03,.025)
  box_detail(a,d['at']+offset,2.86,.26,.06,'seventh brass lettering',-.03,.025)
# The high-angle September 2024 view resolves 109: five upper rows, with
# round first/fourth rows, a tall rectangular entry and carved corner quoins.
a=elevation('248142622:0',22.6,5,3,buff,pale,ground=7.8,spacing=2.65,window_h=2.05)
for j,w in enumerate(a['windows']):
 row=j//3;w.update(shape='round' if row in [0,3] else 'rectangle',hood='round' if row in [0,3] else 'bracketed',surround=True,keystone=True)
a['escapes']=[{'at':.50,'width':.52,'levels':[7.65+j*2.65 for j in range(5)],'material':iron}]
d=entry(a,.5,1.08,.25,None,pale);d.update(top=6.50,leafTop=5.62,shape='rectangle',leaves=2,label='109',labelY=6.05,labelSize=.27,panels=[{'y':.67,'height':.54,'width':.61,'glass':True},{'y':.13,'height':.13,'width':.60}])
windows(a,[.17,.83],3.55,2.60,.20,pale,grille=True)
for at in [.025,.975]:a.setdefault('piers',[]).append({'at':at,'width':.055,'bottom':.2,'top':21.8,'material':pale,'joints':True})
for y in [6.92,10.3,12.95,15.6,18.25]:ledge(a,y,pale,.24)
for y in [4.0,4.5,5.0,5.5,6.0]:
 for at in [.33,.67]:a.setdefault('ornaments',[]).append({'type':'shell','at':at,'y':y,'width':.045,'height':.30,'material':pale})
for span in [[.01,.30],[.70,.99]]:
 shop(a,span,[['glass',.65],['door',.35]],wood,top=2.80,head=2.45,awning={'y':3.0,'drop':.45,'depth':.95,'material':'seventh canvas brown'})
 a['returnShops'][-1]['projection']=.65
fence(a,[[.32,.68]],2.2)
# Mogador's observed lower striped masonry and curved ornamental hoods.
a=RECORDS['248142616:0']['architecture'];a['surfaceZones']=[];a['rustication']=[]
for row in range(10):a.setdefault('surfaceZones',[]).append({'span':[0,1],'bottom':1.9+row*.37,'top':2.08+row*.37,'material':pale})
for j,w in enumerate(a['windows']):
 if w['bottom']>=6.6:
  w.update(hood='segmental' if j//6 in [1,3] else 'bracketed',hoodBacking=True,moldedHood=False,surround=True)
for shop_record in a['returnShops']:shop_record['design']['signs']=[]
for aw in a['awnings']:aw.update(material=white,stripe=olive,stripeSpacing=.12,stripeWidth=.045,text='')
a['signs']=[sign('Cafe Mogador',olive,at=.26,width=.48,y=2.49,height=.30),sign('Cafe Mogador',olive,at=.88,width=.20,y=2.49,height=.30)]
# Ensure every editable confirmed face is represented. No address-range guess
# or blanket fallback can silently turn missing properties into completion.
scope=json.loads((ROOT/'model-source/first-stmarks-scope-08.json').read_text())
expected={f['faceId'] for f in scope['frontages']+scope['cornerReturns'] if not f['protectedCorner']}
assert expected==set(RECORDS),(sorted(expected-set(RECORDS)),sorted(set(RECORDS)-expected))
for key,r in RECORDS.items():
 r['architecture']['observation']['acceptance']='Observed feature transcription with visual estimates; calibrated multi-view acceptance is not established.'
SCHEDULE['status']='Complete confirmed face schedule authored; export and source-to-game review pending'
SCHEDULE['elevations']=sorted(RECORDS.values(),key=lambda r:r['faceId'])
PATH.write_text(json.dumps(DATA,ensure_ascii=False,indent=2)+'\n')
print('STMARKS_AUTHORED',len(RECORDS),'exact faces')
