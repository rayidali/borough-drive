"""Reproducible P02: five First Avenue faces, April 2026 target with dated limits.
Mapped footprints/heights retained; proportions and relief depths are estimates.
"""
import json
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'model-source/east-village-p02'
MAP={b['id']:b for b in json.loads((ROOT/'dist/reconstruction/neighborhood.json').read_text())['buildings']}
OBS=json.loads((OUT/'observations.json').read_text());RECORDS=[];BUSINESSES=[]
IDS=[248142657,248142658,248142659,248142660,248142713]
def m(s):return 'store09 '+s

def elevation(bid,wall,trim,positions,bottoms,height,source_ids,escape_specs):
 b=MAP[bid];f=b['frontages'][0]
 a={'wall':wall,'windows':[],'doors':[],'returnShops':[],'signs':[],
    'observedGround':{'replaceWindows':False,'replaceDoors':False},
    'observation':{'sources':source_ids,'facts':[v for k in source_ids for v in OBS['sources'][k]['observations']],
      'unknown':['No survey/calibrated acceptance; mapped height and footprint, visual opening/relief dimensions.', 'Rear and roof equipment are unobserved. Ninth return is deferred and receives only the shared mass.']},
    'p02Face':{'id':bid,'escapeSpecs':escape_specs,'masonryPitch':[.215,.071] if bid==248142657 else [.21,.067],
      'sourceIds':source_ids}}
 acs={248142657:{(1,0)},248142658:{(2,2)},248142659:set(),248142660:{(0,1),(2,0)},248142713:{(0,0),(1,0),(2,0),(2,2)}}
 for row,y in enumerate(bottoms):
  for col,at in enumerate(positions):
   a['windows'].append({'at':at,'width':(1.05 if bid!=248142713 else 1.02)/f['length'],'bottom':y,'height':height,
     'trim':trim,'frame':'white frame' if bid in IDS[:2] else 'p02 olive frame' if bid in IDS[2:4] else 'p02 silver frame',
     'hood':'none' if bid==248142657 else 'flat','surround':bid==248142658,'rails':[.48], 'ac':(row,col) in acs[bid]})
 r={'faceId':f'{bid}:0','buildingId':bid,'frontageIndex':0,'address':b['address'],'sourceFace':deepcopy(f),'buildingHeight':b['height'],'architecture':a}
 RECORDS.append(r);return a

def door(a,at,width,number=None,material='p02 door brown',panels=None):
 d={'at':at,'width':width,'bottom':.23,'top':2.98,'leafTop':2.70,'material':material,'trim':m('cream enamel'),
    'leaves':1,'recess':.24,'hardware':m('aged brass'),
    'panels':panels or [{'y':.69,'height':.44,'width':.76,'glass':True},{'y':.20,'height':.29,'width':.76}]}
 if number:d.update(label=number,labelY=3.035,labelSize=.13,labelMaterial=m('aged brass'),labelDepth=.12,labelPlate=False)
 a['doors'].append(d);return d

def sign(text,font,back,ink,y,height,**kw):
 return {'at':.5,'width':1,'y':y,'height':height,'depth':.26,'material':back,
  'lines':[{'text':text,'material':ink,'size':height*.66,'style':'store09:'+font}],**kw}

def shop(a,name,span,panels,frame,kind,identity,sources,**kw):
 spec={'top':3.20,'head':2.75,'base':.32,'recess':.24,'panels':panels,'transom':False,'signs':[],
  'detail09':{'frame':frame,'surround':frame,'frameWidth':.042,'pierWidth':.07,'floor':.17,
     'molding':False,'displayDepth':1.1,'displays':[],'furniture':[]},'detailP02':{'kind':kind},**kw}
 a['returnShops'].append({'name':name,'span':span,'design':spec})
 bid=RECORDS[-1]['buildingId'];key=f'{bid}:0:0'
 spec['detail09'].update(id=key,identity=identity,sourceIds=sources)
 BUSINESSES.append({'id':key,'faceId':f'{bid}:0','name':name,'span':span,'identity':identity,'sourceIds':sources,
  'targetCapture':'2026-04','component':kind,'reviewState':'authored; served-game review recorded separately',
  'unknown':['Exact proprietary letterforms, graphic art and small illegible notices are approximate; no invented legible copy.',
    'Movable objects reflect dated imagery, not a claim of unchanged October 2026 conditions.', 'Deep interiors and source-obscured fittings remain unverified.']})
 return spec,spec['detail09']

def display(d,kind,**kw):d['displays'].append({'kind':kind,**kw})

a=elevation(248142657,'p02 dark red brick','p02 ivory stone',[.16,.50,.84],[4.17,7.04],1.82,['south-group','wines-detail'],[])
door(a,.895,.15,material=m('cream enamel'))
s,d=shop(a,'East Village Wines',[.02,.80],[['glass',.44],['glass',.27],['door',.29]],m('black enamel'),'wines',
 'Folded ivory/red projecting sign above burgundy fascia; dark window, copper mesh panel, recessed south door, bottle poster and stacked cartons; separate cream residence grille.', ['wines-detail','south-group'],top=3.18,head=2.80,base=.20)
s['signs']=[sign('EAST VILLAGE WINES','condensed',m('maroon canvas'),m('paper'),3.42,.51)]
s['signs'][0]['lines'][0].update(size=.47,width=.97)
display(d,'bottles',at=.24,y=.62,width=.35,rows=4,count=6,rowStep=.42,depth=-.60,colors=[m('bottle green'),m('aged brass'),m('paper')])
display(d,'poster',at=.24,y=1.12,width=.35,height=1.00,depth=.11,text='',material=m('paper'))
s['boards']=[{'at':.015,'depth':1.15,'height':1.0,'width':.47,'frame':m('oak timber')}]

a=elevation(248142658,'p02 faded pink brick','p02 ivory stone',[.16,.50,.84],[4.15,7.02,9.92],1.86,['south-group','bar-detail'],[{'span':[.06,.68],'levels':[4.05,6.92,9.82],'material':'p02 salmon iron'}])
door(a,.12,.175,material=m('black enamel'),panels=[{'y':y,'height':.22,'width':.80,'glass':True} for y in [.21,.47,.73]])
s,d=shop(a,'Area 140 First',[.24,.987],[['glass',.36],['glass',.38],['door',.26]],m('black enamel'),'bar',
 'Olive BAR fabric shade, circular mathematical monogram, rainbow tube, drooping bulb string; solid vivid green south door and four gray folding chairs with red wire stool.', ['bar-detail'],top=3.22,head=2.80,base=.38)
s['awning']={'detail09':True,'y':3.69,'drop':.28,'depth':.83,'valance':.16,'material':'p02 olive canvas','text':'BAR','textSize':.24,'font':'store09:bold','sidePanels':True}
d.update(doorMaterial='p02 green door',doorSolidTop=2.75,hardware=m('dark iron'))
display(d,'counter',at=.31,y=.84,width=.61,depth=-.62,material=m('dark timber'))

a=elevation(248142659,'p02 red brick','p02 dark lintel',[.16,.50,.84],[4.12,6.99,9.85],1.88,['south-group','laundry-detail','north-elevations-older'],[{'span':[.055,.945],'levels':[4.0,6.88,9.74],'material':'p02 olive iron','flights':[[.37,.68],[.37,.68]],'dropAt':.60}])
door(a,.115,.15,'142')
s,d=shop(a,'Cosmos Launderama',[.265,.987],[['glass',.37],['glass',.39],['door',.24]],'p02 silver frame','laundry',
 'Raised red narrow LAUNDERAMA and small COSMOS/stars on white; folded gray metal canopy, silver windows with low white rail, separate brown 142 entrance and visible washer drums.', ['laundry-detail'],top=3.19,head=2.85,base=.27)
s['signs']=[sign('LAUNDERAMA','narrow',m('white enamel'),'p02 laundry red',3.65,.66)]
s['signs'][0]['lines'][0].update(offset=.105,width=.78,size=.57)
d.update(displayDepth=1.45,baseMaterial=m('white enamel'),doorSolidTop=.18,hardware=m('brushed steel'))

a=elevation(248142660,'p02 fine red brick','p02 dark lintel',[.265,.735],[4.11,6.99,9.85],1.90,['north-oblique','laundry-detail','north-elevations-older'],[{'span':[.12,.88],'levels':[4.0,6.88,9.74],'topSpan':[.59,.89],'material':'p02 olive iron','flights':[[.20,.72],[.20,.72]]}])
door(a,.115,.15)
s,d=shop(a,'Cosmos Dry Cleaners',[.27,.985],[['glass',.65],['door',.35]],'p02 silver frame','drycleaner',
 'Separate WASH & DRY ivory/red fascia and green serif dry-cleaning sign, thin silver shop framing, brown base, narrow south leaf and freestanding sage ATM cabinet.', ['laundry-detail','north-shops-april'],top=3.14,head=2.75,base=.70)
s['signs']=[sign('WASH & DRY','narrow',m('cream enamel'),'p02 laundry red',3.85,.69),sign('COSMOS DRY CLEANERS','serif',m('green enamel'),m('paper'),3.29,.48)]
s['signs'][1]['lines'][0].update(size=.24,width=.94,y=.07)
s['signs'][1]['lines'].append({'text':'144 1st Ave   7 Days Drop Off Service','style':'store09:condensed','size':.092,'y':-.125,'material':m('paper')})
d.update(baseMaterial=m('brushed steel'),doorMaterial='p02 door brown',doorSolidTop=.70,displayDepth=.9)

a=elevation(248142713,'p02 aged cream stucco','p02 salmon lintel',[.13,.38,.63,.875],[4.05,6.97,9.90],1.75,['north-oblique','148-upper-older','north-shops-april','north-elevations-older','148-flight-reinspection'],[{'span':[.235,.565],'levels':[3.97,6.87,9.80],'material':'p02 salmon iron','reverse':True,'flights':[[.48,.31],[.48,.31]],'dropAt':.455}, {'span':[.565,.985],'levels':[3.97,6.87,9.80],'topSpan':[.795,.970],'material':'p02 salmon iron','flights':[[.67,.88],[.67,.88]],'dropAt':.73}])
s,d=shop(a,'Lime Tree Market',[.008,.988],[['glass',.18],['glass',.12],['door',.105],['glass',.185],['glass',.20],['glass',.21]],'p02 silver frame','market',
 'Broad burgundy cloth canopy over a projecting silver-glazed enclosure with red lower panels, unequal glass bays, north-of-center leaf, layered product/window notices and recessed cream upper mass.', ['north-shops-april','148-upper-older'],top=3.08,head=2.89,base=.57)
d.update(baseMaterial='p02 market red',doorMaterial='p02 market red',displayDepth=1.95,doorSolidTop=.55,pierWidth=.025,frameWidth=.035)
display(d,'bottles',at=.71,y=.88,width=.29,rows=4,count=12,rowStep=.34,depth=-.55,colors=[m('paper'),m('bottle green'),m('orange enamel')])
for at in [.22,.52,.77]:display(d,'poster',at=at,y=1.55,width=.06,height=.58,depth=.10,text='',material=m('paper'),layout='grid')
BUSINESSES[-1]['unknown'].append('April tree occlusion leaves central exact pane proportions uncertain; two dated obliques support enclosure, not surveyed dimensions. Ninth shop return is deferred.')

junctions=[]
for north,south in zip(reversed(IDS),list(reversed(IDS))[1:]):
 n=MAP[north];s=MAP[south];nf=n['frontages'][0];sf=s['frontages'][0]
 junctions.append({'northId':north,'southId':south,'condition':'setback with short exposed return' if north==248142713 else 'touching party walls; separate cornices',
 'mappedStreetOffsetMetres':round(nf['x']+nf['rx']*nf['length']-sf['x'],3),'openAlleyObserved':False,'sourceIds':['south-group','north-oblique'],
 'reviewState':'pending served obliques','heightNorth':n['height'],'heightSouth':s['height']})
junctions.append({'northId':248142657,'southId':248142711,'condition':'touching party wall; low 138 exposes tall protected southern wall','openAlleyObserved':False,'sourceIds':['south-group'],'protectedNeighbor':True})
for r in RECORDS:
 for sh in r['architecture']['returnShops']:assert abs(sum(x[1] for x in sh['design']['panels'])-1)<1e-8
assert sum(len(r['architecture']['windows']) for r in RECORDS)==42
schedule={'schema':1,'id':'P02','parent':'01-FA08E','revision':'P02-01','scopeFaces':[r['faceId'] for r in RECORDS],
 'elevations':RECORDS,'businesses':BUSINESSES,'junctions':junctions,'targetCapture':'2026-04 with explicit 2024 architectural supplements',
 'ownership':'Five First Avenue faces and their shared masses only. 148 Ninth return remains deferred; no invented generic side storefront.',
 'sourceLedger':'model-source/east-village-p02/observations.json'}
(OUT/'schedule.json').write_text(json.dumps(schedule,indent=2)+'\n');print('P02',len(RECORDS),'faces',len(BUSINESSES),'shops, 42 upper openings')
