"""Reproduce P01's four observed faces; never rewrite revision 09 schedules.

April 2026 Street View, with dated supplementary upper-elevation observations.
All dimensions beyond the mapped footprint are visual estimates. See the ledger.
"""
import json
from pathlib import Path
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'model-source/east-village-p01'
SCOPE = json.loads((ROOT/'model-source/east-village-ev003/p01-handoff.json').read_text())
OBS = json.loads((OUT/'observations.json').read_text())
MAP = {b['id']: b for b in json.loads((ROOT/'dist/reconstruction/neighborhood.json').read_text())['buildings']}
RECORDS = []
BUSINESSES = []

def m(name): return 'store09 '+name

def elevation(bid, wall, trim, ground, step, window_height, hood, cornice, source_ids):
    b = MAP[bid]; f = b['frontages'][0]; n = 5 if bid == 241822278 else 4
    assert str(bid)+':0' in {r['faceId'] for r in SCOPE['faces']}
    positions = [.10,.30,.50,.70,.90] if n == 5 else [.115,.37,.63,.885]
    a = {'wall':wall, 'windows':[], 'doors':[], 'returnShops':[], 'signs':[],
         'observedGround':{'replaceWindows':False,'replaceDoors':False},
         'observation':{'sources':source_ids,'facts':[s for k in source_ids for s in OBS['sources'][k]['observations']],
             'unknown':['Dimensions visually estimated; no surveyed or calibrated acceptance.',
                        'Unseen rear/roof details and exact proprietary artwork remain unknown.']}}
    for row in range(4):
        for bay,at in enumerate(positions):
            a['windows'].append({'at':at,'width':(.99 if n==5 else .94)/f['length'],
                'bottom':round(ground+row*step,3),'height':window_height,
                'trim':trim,'frame':'white frame' if n==5 else 'black iron',
                'hood':hood,'hoodBacking':hood=='segmental','rails':[.48],
                'shape':'segmental' if bid in [241822337,241822304] else 'rectangle',
                'grille':bid in [241822304,241822211] and row==0,
                'ac':(row,bay) in {241822278:{(0,1),(0,3),(1,2),(1,3),(2,1),(3,4)},
                    241822337:{(2,0),(3,0),(3,3)},241822304:{(3,0),(2,0)},
                    241822211:{(0,3),(3,3),(2,0)}}[bid]})
    h=b['height']
    a['cornice']={'profile':cornice,'material':trim if n!=5 else wall,'y':h,'brackets':6}
    if n!=5:a['escapes']=[{'at':.50,'width':.55,'levels':[round(ground-.12+j*step,3) for j in range(4)],'material':'black iron' if bid!=241822304 else 'first olive trim'}]
    a['p01Face']={'id':bid,'upperBlindFractions':[.35,.72,.0,.5], 'sourceIds':source_ids}
    record={'faceId':str(bid)+':0','buildingId':bid,'frontageIndex':0,'address':b['address'],
            'sourceFace':deepcopy(f),'buildingHeight':h,'architecture':a}
    RECORDS.append(record)
    return a

def door(a,at,width,number=None,material='store09 dark timber',leaves=1,top=2.9,label_y=2.65):
    d={'at':at,'width':width,'bottom':.20,'top':top,'leafTop':2.42,
       'material':material,'trim':material,'leaves':leaves,'recess':.28,
       'panels':[{'y':.61,'height':.64,'width':.76,'glass':True},
                 {'y':.13,'height':.15,'width':.76}], 'hardware':m('aged brass')}
    if number:d.update(label=number,labelY=label_y,labelSize=.13,labelMaterial=m('aged brass'),labelDepth=-.17,labelPlate=False)
    a['doors'].append(d)
    return d

def sign(text,font='condensed',back='black enamel',ink='warm white',y=3.15,height=.60,**kw):
    return {'at':.5,'width':1,'y':y,'height':height,'depth':.28,'material':m(back),
            'lines':[{'text':text,'material':m(ink),'size':height*.65,'style':'store09:'+font}],**kw}

def shop(a,name,span,panels,frame,identity,kind,source_ids,**kw):
    d={'top':3.45,'head':2.72,'base':.32,'recess':.20,'panels':panels,'transom':False,
       'signs':[], 'detail09':{'frame':frame,'surround':frame,'frameWidth':.050,'pierWidth':.10,
           'floor':.17,'displayDepth':.90,'molding':False,'displays':[],'furniture':[]},
       'detailP01':{'kind':kind}, **kw}
    a['returnShops'].append({'name':name,'span':span,'design':d})
    bid=RECORDS[-1]['buildingId'];key=f'{bid}:0:{len(a["returnShops"])-1}'
    d['detail09'].update(id=key,sourceIds=source_ids,identity=identity)
    BUSINESSES.append({'id':key,'faceId':f'{bid}:0','name':name,'span':span,'identity':identity,
        'sourceIds':source_ids,'targetCapture':'2026-04','component':kind,
        'reviewState':'authored, served-game review pending',
        'unknown':['Exact proprietary letterforms and micrographic artwork are approximated with authored shapes and licensed fonts.',
                   'Unreadable menu/notice copy remains abstract marks; no invented legible text.',
                   'Hidden interiors are not reconstructed; only observed near-window layers.']})
    return d,d['detail09']

def display(d,kind,**kw):d['displays'].append({'kind':kind,**kw})

# 137: the plain five-bay brick house is NOT the legacy ivory template.
a=elevation(241822278,'p01 137 red brick','seventh pale limestone',3.83,2.55,1.86,'flat','plain',['south-elevations','137-front','137-sign-entry'])
sp,d=shop(a,'Spirals',[.02,.415],[['glass',.48],['glass',.13],['glass',.13],['door',.26]],'p01 blue enamel',
    'Powder-blue framed bakery, white/ochre italic serif fascia, separate black lamp housing, broad left window and narrow right leaf.',
    'spirals',['137-front','137-sign-entry'],top=3.33,head=2.80,base=.37)
d.update(baseMaterial=m('black tile'),doorMaterial='p01 blue enamel',molding=True,doorSolidTop=.54,hardware=m('aged brass'),threshold=m('gray plaster'))
sp['signs']=[sign('Spirals','serif:1.0:0.18','white enamel','aged brass',y=3.38,height=.65)]
sp['signs'][0]['lines'][0].update(size=.65,y=.06)
sp['signs'][0]['lines'].append({'text':'Cinnamon Rolls','material':m('gray plaster'),'size':.115,'y':-.32,'style':'store09:condensed'})
display(d,'counter',at=.34,y=.98,width=.72,depth=-.43,material=m('cream enamel'))
display(d,'poster',at=.78,y=1.69,width=.055,height=.26,text='',depth=.08,material=m('paper'))
display(d,'poster',at=.92,y=1.99,width=.12,height=.17,text='',depth=.08,material=m('paper'))
door(a,.49,.12,'137',m('black enamel'),leaves=1,label_y=2.29)
# The occluded fixed/leaf split is explicit; this one-leaf interpretation is not a certified count.
a['observation']['unknown'].append('137 entrance leaf/fixed split remains partly hidden; narrow single operable glazed leaf is an authored interpretation.')
sp,d=shop(a,'Crispy Burger',[.585,.985],[['door',.42],['glass',.29],['glass',.29]],'p01 burger orange',
    'Orange paneled piers, cream/red chunky fascia and chicken medallion, open recessed left entry, red lower food collage and green neon.',
    'crispy',['137-front','137-sign-entry'],top=3.31,head=2.82,base=.24)
d.update(pierWidth=.20,frameWidth=.045,molding=True,kickplate=False,doorSolidTop=.17,hardware=m('brushed steel'))
sp['signs']=[sign('CRISPY BURGER','bold','cream enamel','printed red',y=3.43,height=.74)]
sp['signs'][0]['lines'][0].update(offset=.08,width=.79,y=.14,size=.52)
sp['signs'][0]['lines'].append({'text':'BURGER  FRIED CHICKEN  SNACKS','size':.15,'y':-.15,'material':m('printed red'),'style':'store09:condensed'})
display(d,'counter',at=.65,y=1.0,width=.55,depth=-.52,material=m('brushed steel'))
sp['boards']=[{'at':.43,'depth':1.0,'height':.93,'width':.46,'frame':m('dark iron')}]

# 139: four bays; a residential door, nail shop and separate green food shop.
a=elevation(241822337,'painted p01 cobalt','p01 rose stone',4.05,2.62,1.87,'segmental','bracketed',['south-elevations','139-front'])
a['cornice']['material']='p01 navy cornice'
door(a,.105,.16,'139',m('dark timber'),leaves=2,label_y=2.29)
sp,d=shop(a,'V-One Nail Spa',[.22,.625],[['glass',.62],['door',.38]],m('brushed steel'),
    'Orange handwritten sign on charcoal, slender silver glazing, circular manicure graphics and coral base, visible polish rack and white board.',
    'vone',['139-front'],top=3.23,head=2.81,base=.27)
d.update(frameWidth=.032,pierWidth=.055,kickplate=True,baseMaterial=m('rose enamel'))
sp['signs']=[sign('V-ONE Nail Spa','script','black enamel','orange enamel',y=3.43,height=.74)]
sp['signs'][0]['lines'].append({'text':'139 First Ave','size':.082,'y':-.34,'material':m('orange enamel'),'style':'store09:condensed'})
display(d,'bottles',at=.47,y=.71,width=.20,rows=6,count=6,rowStep=.19,depth=-.65,colors=[m('printed red'),m('rose enamel'),m('paper'),m('purple canvas')])
display(d,'counter',at=.34,y=.64,width=.59,depth=-.53,material=m('cream enamel'))
sp['boards']=[{'at':.64,'depth':1.0,'height':1.05,'width':.52,'frame':m('white enamel')}]
sp,d=shop(a,'SKWR',[.635,.987],[['door',.29],['glass',.71]],m('green enamel'),
    'Olive green skewer fascia with thick white lettering, narrow left entry, broad right window, violet Open tube and layered counter/menu.',
    'skwr',['139-front','141-detail'],top=3.28,head=2.73,base=.32)
sp['signs']=[sign('SKWR','bold','sage enamel','white enamel',y=3.44,height=.76)]
sp['signs'][0]['lines'][0].update(size=.68)
display(d,'counter',at=.64,y=.96,width=.59,depth=-.35,material=m('honey timber'))
display(d,'jars',at=.64,y=1.03,width=.57,rows=1,count=9,depth=-.32,colors=[m('paper'),m('printed red'),m('orange enamel')])
display(d,'poster',at=.55,y=2.25,width=.35,height=.42,depth=-.30,text='',layout='grid')
# The lower frontage is SUV-occluded; do not invent a pavement board.

# 141: shallow arched masonry, separate address portal, long glass sushi shop.
a=elevation(241822304,'p01 141 orange brick','p01 brown stone',4.0,2.70,1.87,'segmental','bracketed',['141-143-older-elevations','141-detail','141-143-april-shops'])
door(a,.105,.17,None,m('black enamel'),top=3.06)
a['signs'].append({'at':.105,'width':.20,'y':3.45,'height':.40,'depth':.22,'material':m('black enamel'),
    'lines':[{'text':'141','material':m('paper'),'size':.16,'style':'store09:condensed'}]})
sp,d=shop(a,'Kikoo',[.225,.987],[['door',.18],['glass',.265],['glass',.265],['glass',.29]],'p01 bronze frame',
    'Long dark restaurant fascia with hand-shaped white Kikoo/sushi-bowl mark, fine bronze glazing, cool blue vertical tubes and readable-depth menu/chair layers.',
    'kikoo',['141-detail','141-143-april-shops'],top=3.48,head=2.86,base=.23)
d.update(frameWidth=.035,pierWidth=.06,baseMaterial=m('cream enamel'),displayDepth=1.25)
# Custom glyph strokes below preserve the distinctive logo silhouette.
sp['signs']=[sign('','bold','black enamel','white enamel',y=3.50,height=.78)]
display(d,'poster',at=.17,y=2.05,width=.29,height=.76,text='',depth=-.19,material=m('dark timber'),ink=m('paper'))
display(d,'poster',at=.57,y=2.02,width=.38,height=.82,text='',depth=-.15,layout='grid',material=m('paper'))
for at in [.39,.58,.78,.93]:d['furniture'].append({'kind':'chair','at':at,'depth':-.53,'material':m('cream enamel'),'profile':'slat','yaw':0})
display(d,'counter',at=.67,y=.72,width=.50,depth=-.95,material=m('dark timber'))

# 143: retain the two businesses visible together in April, not the 2024 smoke shop.
a=elevation(241822211,'p01 143 red brick','p01 dark stone',3.96,2.61,1.85,'bracketed','bracketed',['141-143-older-elevations','141-143-april-shops','143-detail'])
a['cornice'].update(profile='bracketed',brackets=4)
sp,d=shop(a,'Paquitos',[.025,.465],[['glass',.34],['glass',.31],['door',.35]],m('dark iron'),
    'Narrow red dimensional PAQUITOS/sombrero fascia on dark olive, divided low glass, a red folding chair and low blue pavement menu.',
    'paquitos',['143-detail'],top=3.24,head=2.70,base=.30)
sp['signs']=[sign('PAQUITOS','narrow','black enamel','printed red',y=3.47,height=.74)]
sp['signs'][0]['lines'][0].update(size=.72,y=-.07)
display(d,'counter',at=.33,y=.83,width=.62,depth=-.50,material=m('dark timber'))
display(d,'poster',at=.90,y=1.5,width=.08,height=.24,depth=.12,text='A',material=m('paper'))
d['furniture']=[{'kind':'chair','at':.87,'depth':.85,'material':m('red enamel'),'profile':'slat','yaw':-.16}]
sp['boards']=[{'at':.51,'depth':.91,'height':.72,'width':.64,'frame':m('navy enamel')}]
door(a,.55,.135,None,m('black enamel'),leaves=1,top=2.94)
sp,d=shop(a,'Banshee',[.65,.985],[['door',.30],['glass',.70]],m('green enamel'),
    'Dark green timber pub, deep burgundy/ivory quarter-round striped canopy with scalloped hem, white window name and oval Guinness blade.',
    'banshee',['143-detail','141-143-april-shops'],top=3.17,head=2.66,base=.39)
d.update(frameWidth=.067,pierWidth=.11,molding=True,baseMaterial=m('green enamel'),doorSolidTop=.36,hardware=m('aged brass'))
sp['awning']={'detail09':True,'shape':'round','y':3.79,'drop':.73,'depth':1.16,'valance':.17,
    'material':m('maroon canvas'),'stripe':m('cream canvas'),'stripeSpacing':.23,'stripeWidth':.115,
    'scalloped':True,'sidePanels':True,'text':''}
sp['windowText']=[{'text':'BANSHEE','at':.64,'y':1.95,'width':.59,'size':.16,'material':m('paper'),'style':'store09:serif'}]
display(d,'poster',at=.15,y=1.66,width=.065,height=.16,depth=.11,text='',material=m('paper'))
display(d,'counter',at=.67,y=.82,width=.57,depth=-.57,material=m('dark timber'))
# No invented bar-bottle lineup in an obscured source window.

assert len(RECORDS)==4 and len(BUSINESSES)==7
for r in RECORDS:
    assert r['sourceFace']==next(x['sourceFace'] for x in SCOPE['faces'] if x['faceId']==r['faceId'])
    assert len(r['architecture']['windows'])==(20 if r['buildingId']==241822278 else 16)
    for sh in r['architecture']['returnShops']:assert abs(sum(x[1] for x in sh['design']['panels'])-1)<1e-8
schedule={'schema':1,'id':'P01','parent':'01-FA08W','revision':'P01-02','targetCapture':'2026-04',
    'scopeFaces':[r['faceId'] for r in RECORDS],'elevations':RECORDS,'businesses':BUSINESSES,
    'sourceLedger':'model-source/east-village-p01/observations.json',
    'limits':'Authored dimensional/font/artwork estimates; source evidence and served-game review are separate. No source photographic pixels distributed.'}
(OUT/'schedule.json').write_text(json.dumps(schedule,indent=2)+'\n')
print('P01_SCHEDULE',len(RECORDS),'faces',len(BUSINESSES),'businesses')
