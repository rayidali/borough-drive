"""Reproduce the individual business pass over the frozen revision 08 streets.

Run from the repo: python3 model-source/author_storefront_09.py
Each call below owns a particular observed business, never a generated style.
Fine dimensions/material mechanics and font substitutions remain estimates.
"""
import json,math,runpy
from pathlib import Path
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'model-source/author_stmarks_08.py'),run_name='__main__')
PATH=ROOT/'model-source/storefront-details.json'
DATA=json.loads(PATH.read_text());S=DATA['firstStmarksEngine']
F={r['faceId']:r for r in S['elevations']}
LEDGER_PATH=ROOT/'model-source/storefront-observations-09.json'
LEDGER=json.loads(LEDGER_PATH.read_text());OLD=json.loads((ROOT/'model-source/first-stmarks-browser-08.json').read_text())
E={r['faceId']:r for r in OLD['faces']};BUSINESSES=[];SEEN=set()

def m(name):return 'store09 '+name
def arch(face):return F[face]['architecture']
def detail(face,index,identity,frame,font='condensed',**kw):
    key=face+':'+str(index);assert key not in SEEN,key;SEEN.add(key)
    shop=arch(face)['returnShops'][index];spec=shop['design']
    sources=[x+'-detail' if x+'-detail' in LEDGER['sources'] else '08:'+x for x in E[face]['sources']]
    record={'id':key,'faceId':face,'shopIndex':index,'displayName':shop.get('name') or 'Unnamed/partly unreadable unit',
      'identity':identity,'sourceIds':sources,'observed':E[face]['observations'],
      'unknown':E[face]['unknown']+['Exact finish, fine product inventory and font identity are not measured.'],
      'fontSubstitution':font,'state':'authored; final-game detail review pending'}
    BUSINESSES.append(record)
    d={'id':key,'sourceIds':sources,'identity':identity,'frame':m(frame),'surround':m(frame),
       'frameWidth':.055,'pierWidth':.12,'molding':True,'displays':[],'furniture':[],**kw}
    spec['detail09']=d
    for sign in spec.get('signs',[]):
        for line in sign.get('lines',[]):line['style']='store09:'+font
    for item in spec.get('windowText',[]):item['style']='store09:'+font
    if spec.get('awning'):spec['awning'].update(detail09=True,font='store09:'+font)
    return spec,d

def display(d,kind,**kw):d['displays'].append({'kind':kind,**kw})
def furniture(d,kind,at,depth=.95,**kw):d['furniture'].append({'kind':kind,'at':at,'depth':depth,**kw})
def seating(d,at,depth=1.0,width=.56,wood='honey timber',profile='slat',umbrella=None):
    furniture(d,'round-table',at,depth,width=width,material=m('cream enamel'))
    # Seat clearance is in world metres, independent of the basement bay width.
    for side in [-1,1]:furniture(d,'chair',at,depth,offset=side*(width/2+.28),material=m(wood),profile=profile,yaw=side*math.pi/2)
    if umbrella:furniture(d,'umbrella',at,depth,material=m(umbrella),radius=.90,height=2.35)
def sign(spec,text,font='condensed',mat='black enamel',letters='warm white',y=3.05,height=.5,**kw):
    spec['signs']=[{'at':.5,'width':1,'y':y,'height':height,'depth':.24,'material':m(mat),
                   'lines':[{'text':text,'material':m(letters),'size':height*.80,'style':'store09:'+font}],**kw}]
    return spec['signs'][0]
def awning(spec,material='black canvas',**kw):
    spec['awning']={'detail09':True,'y':3.35,'drop':.43,'depth':1.02,'valance':.20,'material':m(material),'font':'store09:condensed',**kw}
    return spec['awning']
def addtext(spec,text,at=.5,y=1.9,width=.65,font='condensed',material='warm white',size=.17,**kw):
    spec.setdefault('windowText',[]).append({'text':text,'at':at,'y':y,'width':width,'style':'store09:'+font,'material':m(material),'size':size,**kw})
def poster(d,at=.5,y=1.5,width=.2,text='',**kw):display(d,'poster',at=at,y=y,width=width,text=text,**kw)
def face_extra(face):return arch(face).setdefault('storefront09',{'signs':[],'furniture':[],'displays':[],'graphics':[]})

# First Avenue, west side: separate timber/metal assemblies and visible layers.
sp,d=detail('241822212:0',0,'Maroon display front with mustard circle frieze, narrow left door and red/orange textiles.','maroon enamel',baseMaterial=m('red enamel'))
sp['panels']=[['door',.20],['glass',.80]];sp['base']=.50
display(d,'cloth',at=.74,y=1.08,width=.28,height=.55,material=m('red canvas'))
display(d,'jars',at=.64,y=.68,width=.55,rows=2,count=7,colors=[m('orange enamel'),m('aged brass'),m('red enamel')])
poster(d,.53,1.80,.16,text='',layout='grid');poster(d,.87,1.74,.12,text='',material=m('printed red'))
sp,d=detail('241822295:0',0,'Scaffold-obscured pale metal glazing, taped paperwork and plywood perimeter.','cream enamel',molding=False,frameWidth=.045)
poster(d,.22,1.5,.40,height=.80,text='',material=m('paper'))
sp,d=detail('241822247:0',0,'Teal laundry fascia, pale aluminum framing, multi-pane transoms and taped window notices.','white enamel','bold',molding=False,kickplate=True)
sp['signs'][0]['lines'][0]['size']=.58
sp['head']=2.60;sp['base']=.35
for at,y,w in [(.18,2.0,.12),(.37,1.4,.10),(.65,1.65,.13),(.84,1.55,.09)]:poster(d,at,y,w,height=.34,text='',material=m('paper'))
addtext(sp,'SELF SERVICE',.30,2.33,.26,size=.105);addtext(sp,'DROP OFF',.62,2.33,.20,size=.105)
# Unseen washers are deliberately not inferred; interior contents remain unknown.
sp,d=detail('241822288:0',0,'Cream fascia with broad red COMPTON’S lettering, scripted subline, bright stacked product panel and red bench.','cream enamel','bold',molding=False,frameWidth=.04)
sp['signs'][0]['lines'][0]['size']=.62
sp['signs'][0]['lines'][1]['style']='store09:script';sp['signs'][0]['lines'][1]['size']=.17
display(d,'bottles',at=.88,y=.73,width=.11,rows=5,count=3,rowStep=.28,colors=[m('printed red'),m('printed blue'),m('paper')])
display(d,'counter',at=.38,y=.96,width=.62,depth=-.34,material=m('brushed steel'))
poster(d,.55,1.66,.13,height=.40,text='',layout='grid')
sp['benches']=[{'at':.40,'width':1.4,'depth':.82,'material':m('red enamel')}]
sp,d=detail('241822228:0',0,'Nudibranch pale framed multiple glass leaves under dated shed, understated dark transom lettering.','cream enamel','condensed',frameWidth=.045,doorSolidTop=.22)
arch('241822228:0')['signs']=[]
sp['panels']=[['glass',.25],['door',.25],['glass',.25],['door',.25]]
addtext(sp,'nudibranch',.28,2.70,.38,size=.14);addtext(sp,'nudibranch',.78,2.70,.37,size=.14)
poster(d,.20,1.8,.10,height=.36,text='')
sp,d=detail('241822263:0',0,'Cream storefront and dark transoms beneath the construction shed; lower details partly hidden.','cream enamel',molding=False)
poster(d,.30,1.65,.18,height=.60,text='')
sp,d=detail('241822220:0',0,'Nail shop dark fascia with tall narrow cream lettering and horizontal interior/display slats.','dark timber','narrow',frameWidth=.045)
display(d,'blind',at=.36,y=1.40,width=.54,height=1.2,material=m('cream canvas'),depth=-.18)
addtext(sp,'NAILS',.5,2.96,.86,font='narrow',size=.39)
sp['signs']=[]
sp,d=detail('241822220:0',1,'AT&T dark metal entry/display with blue promotional panel and blue pavement board.','black enamel','bold',molding=False)
poster(d,.35,1.8,.52,height=.92,text='25',material=m('printed blue'),ink=m('paper'))
sp['boards']=[{'at':.84,'depth':.85,'height':.98,'frame':m('blue enamel')}]
sp,d=detail('241822308:0',0,'Vacant dark-framed broad pane with layered pale outlined graffiti and low tags.','dark iron',molding=False,frameWidth=.045)
sp['panels']=[['glass',.52],['glass',.48]];sp['base']=.18
d['graffiti']={'ink':m('paper'),'color':m('blue enamel'),'band':[.36,2.15]}
sp,d=detail('241822308:0',1,'Narrow left door and a broad paper-covered pale-gray window.','brushed steel',molding=False,frameWidth=.045)
sp['panels']=[['door',.22],['glass',.78]]
display(d,'cloth',at=.62,y=1.53,width=.68,height=2.15,depth=.0,material=m('linen canvas'))
sp,d=detail('241822308:0',2,'Small active coffee unit with fine dark glazing and a pale logo panel.','black enamel','condensed',molding=False,frameWidth=.045)
poster(d,.53,2.11,.58,height=.55,text='COFFEE',material=m('paper'))
poster(d,.47,1.3,.20,height=.4,text='',material=m('printed blue'))

# First Avenue, east side.
for idx in [0,1]:
 sp,d=detail('248142642:0',idx,'Red-painted individual unit with broad dark pane and a separate narrow left entry; no unsupported MaLa sign.','red enamel',molding=False,baseMaterial=m('red enamel'))
 sp['panels']=[['door',.26],['glass',.74]]
 if idx==0:poster(d,.63,1.86,.19,height=.38,text='',material=m('paper'))
 else:poster(d,.72,1.92,.33,height=.37,text='',layout='grid')
sp,d=detail('248142646:0',0,'Full-width maroon organic-grocery canopy, gold window script, bottle-lined ledge and plain timber bench.','brushed steel','bold',molding=False,frameWidth=.04)
arch('248142646:0').pop('displayBottles',None)
for ledge in arch('248142646:0').get('detailBoxes',[]):ledge.update(y=.705,material=m('honey timber'),height=.045)
aw=arch('248142646:0')['awnings'][0];aw.update(detail09=True,font='store09:bold:1.0:0.16',material=m('maroon canvas'),letters=m('warm white'),valance=.27)
sp['windowText']=[];addtext(sp,'East Village',.59,2.03,.42,'serif','aged brass',.17);addtext(sp,'Organic',.59,1.81,.35,'script','aged brass',.20)
addtext(sp,'Organic Produce',.60,1.48,.40,'condensed','aged brass',.12)
display(d,'bottles',at=.36,y=.74,width=.70,rows=1,count=17,depth=.16,colors=[m('bottle green')])
poster(d,.21,1.62,.21,height=.65,text='',layout='grid')
sp['benches']=[{'at':.39,'width':1.65,'depth':.95,'material':m('honey timber')}]
sp,d=detail('248142648:0',0,'Grafton cream paneled pub surround, olive fascia, serif name and three timber Venetian blinds.','cream enamel','serif',frameWidth=.075,baseMaterial=m('cream enamel'))
sp['panels']=[['glass',.24],['glass',.24],['glass',.24],['door',.28]]
for at in [.14,.37,.60]:display(d,'blind',at=at,y=1.69,width=.18,height=1.2,material=m('honey timber'),depth=-.025)
sp['signs'][0]['lines'][1]['style']='store09:serif'
sp,d=detail('248142651:0',0,'Noreetuh black fold-out canopy, small cursive text, fine pale glass rails and painted leafy lower panel.','brushed steel','script',molding=False,frameWidth=.045,baseMaterial=m('black enamel'))
aw=sp['awning'];aw.update(material=m('black canvas'),font='store09:script',detail09=True,sidePanels=True)
sp['base']=.75
d['paintedLeaves']=True
sp,d=detail('248142654:0',0,'Utshob teal sign and compact glazed doorway with blue covered window.','cream enamel','condensed',molding=False)
sp['signs'][0]['lines'][0]['size']=.49
display(d,'cloth',at=.34,y=1.64,width=.49,height=1.38,material=m('blue enamel'))
sp,d=detail('248142654:0',1,'Kolachi white surround, recessed left entrance and stacked white lettering on the broad dark right pane.','white enamel','condensed',molding=False,pierWidth=.15)
sp['signs']=[];sp['windowText']=[];sp['panels']=[['door',.32],['glass',.68]]
for text,y in [('PAKISTANI',2.49),('STREET (ISH)',2.27),('FOOD',2.05)]:addtext(sp,text,.64,y,.54,'condensed','warm white',.19)
furniture(d,'stool',.10,.63,material=m('honey timber'),seat=.72)

# Second Avenue / western St. Marks: Cafe Maud and the distinct neighboring room.
for face,idx,panels in [('241822164:0',0,[['glass',.23],['glass',.23],['glass',.23],['door',.31]]),('241822164:1',0,[['glass',.22],['glass',.22],['door',.18],['glass',.19],['glass',.19]])]:
 sp,d=detail(face,idx,'Cafe Maud: peach wall, round-headed honey timber openings, green restrained fascia, bistro chairs and orange parasols.','honey timber','serif',surround=m('pink plaster'),baseMaterial=m('pink plaster'),archedPanels=list(range(len(panels))),frameWidth=.08,pierWidth=.17)
 sp.update(panels=panels,top=3.55,head=3.00,base=.73,transom=False)
 awning(sp,'olive canvas',y=3.80,drop=.12,depth=.27,valance=.24,text='café maud',font='store09:serif',textSize=.27)
 sp['signs']=[]
 for at in ([.18,.52,.84] if face.endswith(':0') else [.16,.49,.81]):seating(d,at,1.40,wood='honey timber',profile='wishbone',umbrella='orange canvas')
 for at in [.12,.42,.74]:display(d,'pendant',at=at,y=2.53,depth=-.40)
sp,d=detail('241822164:0',1,'Separate black-fascia bar: warm wood rectangular opening bank and transoms, gray plinth, two small round tables and a folded pale umbrella.','honey timber','serif',baseMaterial=m('gray plaster'),frameWidth=.07)
sp['panels']=[['door',.16],['glass',.21],['glass',.21],['glass',.21],['glass',.21]];sp['base']=.82
sp.pop('awning',None);sign(sp,'',mat='black enamel',y=3.43,height=.52)
seating(d,.20,1.15,wood='honey timber',profile='wishbone');seating(d,.35,1.40,wood='honey timber',profile='wishbone')
furniture(d,'closed-umbrella',.41,1.0,material=m('cream canvas'),height=2.55)
for idx in [0,1]:
 sp,d=detail('241822224:0',idx,'41 basement unit beside the raised stoop: dark-framed glass, independent low entry and visible shutter/trellis.','black enamel',frameWidth=.045,doorSolidTop=-.28)
 if idx==0:d['closedShutter']=True
 else:display(d,'cloth',at=.46,y=.9,width=.62,height=1.15,material=m('linen canvas'))
sp,d=detail('241822284:0',0,'42½ lower glass entry: pale surround, metal gate and small white window lettering.','cream enamel','serif',frameWidth=.045)
poster(d,.40,1.04,.28,height=.28,text='',material=m('paper'))
sp,d=detail('241822300:0',0,'Anthony Aiden optical shop: black/timber framing, arched sign silhouette, fine mixed-case lettering and eyewear displays.','dark timber','condensed',frameWidth=.075)
ss=sign(sp,'anthony aiden opticians','condensed',y=3.00,height=.63,shape='store09-arch')
ss['lines'][0].update(size=.17,y=-.16)
ss['lines'].append({'text':'aa','size':.22,'y':.24,'style':'store09:serif','material':m('warm white')})
display(d,'optical',at=.39,y=.80,width=.59,rows=4,count=7,rowStep=.35)
sp,d=detail('241822306:0',0,'Northwell Health: wide white medical fascia with blue words, barred glazing and two pale posted notices.','black enamel','bold',molding=False)
sign(sp,'Northwell Health','bold','white enamel','blue enamel',y=2.72,height=.46)
poster(d,.25,1.85,.24,height=.50,text='Northwell',material=m('paper'));poster(d,.72,1.85,.24,height=.50,text='Health',material=m('paper'))
sp,d=detail('241822310:0',0,'Porto Rico: red enamel doorway/display, cream serif fascia, red fabric canopy, bags and coffee tins visible behind glass.','red enamel','serif',frameWidth=.08)
aw=arch('241822310:0')['awnings'][0];aw.update(detail09=True,material=m('red canvas'),font='store09:serif',scalloped=True,text='COFFEE & TEA')
display(d,'jars',at=.33,y=.70,width=.55,rows=3,count=7,rowStep=.42,colors=[m('paper'),m('aged brass'),m('printed red')])
poster(d,.84,1.31,.15,height=.58,text='',layout='grid')
sp,d=detail('241822190:0',0,'Vegan Grill: vivid green italic vegan / thin GRILL fascia, small green canopy and picture menu beside descending entry.','black enamel','bold',molding=False)
sign(sp,'vegan GRILL','bold:1.0:0.15','black enamel','lime enamel',y=1.97,height=.49)
awning(sp,'olive canvas',y=1.81,drop=.14,depth=.58,valance=.15,text='58 St. Marks Pl.',textSize=.10)
sp['boards']=[{'at':.05,'depth':.6,'height':1.06,'frame':m('dark iron')}];poster(d,.24,1.16,.30,height=.66,text='',layout='grid')
sp,d=detail('241822190:0',1,'Separate low unit beneath the left stoop, dark barred access, details partly obscured.','dark iron',molding=False,frameWidth=.045)
sp,d=detail('241822279:0',0,'Jiang’s Kitchen: compact below-grade restaurant under black canopy, white name and smaller cuisine line, visible menu notices.','black enamel','serif',frameWidth=.05)
aw=sp['awning'];aw.update(detail09=True,material=m('black canvas'),font='store09:serif',valance=.24)
poster(d,.18,.98,.20,height=.55,text='',layout='grid');addtext(sp,'NORTHERN CHINESE FOOD',.5,1.55,.76,'condensed','warm white',.085)
sp,d=detail('241822217:0',0,'75 Cocktail Lounge: corrugated stainless-steel walls around narrow glass door, rounded burgundy canopy and white condensed lettering.','brushed steel','narrow',baseMaterial=m('brushed steel'),molding=False,frameWidth=.045)
sp['panels']=[['glass',.32],['door',.30],['glass',.38]]
d['corrugatedSides']=True
aw=sp['awning'];aw.update(detail09=True,material=m('maroon canvas'),text='COCKTAIL LOUNGE',font='store09:narrow',topText='75',textSize=.23,sidePanels=True,shape='round',inset=.22,drop=.55,depth=.84)
sp,d=detail('241822271:0',0,'La Palapa basement/entry edge: dark metal and pale painted surrounds beneath the separate tan restaurant canopy.','black enamel','condensed',frameWidth=.06)
arch('241822271:0')['awnings'][0].update(detail09=True,material=m('linen canvas'),font='store09:serif')
sp,d=detail('241822320:0',0,'Narrow dark restaurant front: glass entrance and food photograph/menu panels in the fascia.','black enamel','condensed',molding=False)
poster(d,.42,2.97,.75,height=.40,text='',layout='grid')
poster(d,.16,1.65,.13,height=.42,text='',layout='grid')
sp,d=detail('241822234:0',0,'E Ramen: black square fascia with large yellow script, dark double glass doors and a picture-menu A-frame.','black enamel','script',molding=False,doorSolidTop=.30)
sign(sp,'E Ramen','script','black enamel','aged brass',y=3.07,height=.65)
sp['panels']=[['double-door',1.0]];sp['boards']=[{'at':.45,'depth':.85,'height':1.08,'frame':m('cream enamel')}]
poster(d,.45,1.10,.16,height=.45,text='',layout='grid')

# First / St. Marks corner shops, with their own seating and canopy structures.
sp,d=detail('241822219:0',0,'Stromboli avenue return: deep red fascia and shallow valance, open counter with red high stools.','dark timber','serif',frameWidth=.07)
sign(sp,'STROMBOLI PIZZA','serif','maroon enamel',y=3.25,height=.36)
awning(sp,'maroon canvas',y=2.94,drop=.15,depth=.52,valance=.18,text='Stromboli PIZZA',font='store09:serif',textSize=.14)
display(d,'counter',at=.5,y=1.20,width=.90,depth=.10)
for at in [.20,.39,.58,.77]:furniture(d,'stool',at,.64,material=m('red enamel'),seat=.72)
sp,d=detail('241822219:0',1,'Camino: white fascia with spaced black letters, open tall timber/glass leaves and narrow sidewalk counter seating.','cream enamel','condensed',frameWidth=.06)
sign(sp,'C A M I N O','condensed','white enamel','black enamel',y=3.18,height=.43)
display(d,'bottles',at=.35,y=1.30,width=.44,rows=3,count=8,depth=-.48,colors=[m('bottle green'),m('aged brass')])
for at in [.14,.38,.68,.85]:furniture(d,'stool',at,.69,material=m('honey timber'),seat=.75)
sp,d=detail('241822219:1',0,'Stromboli street face: burgundy-and-cream horizontal awning, serif valance lettering, open glass wall and small interior tables.','dark timber','serif',frameWidth=.055,doorSolidTop=.22)
sp['signs']=[]
awning(sp,'maroon canvas',y=3.47,drop=.43,depth=1.02,valance=.22,text='Stromboli PIZZA',font='store09:serif',textSize=.20,horizontalStripes=True)
display(d,'counter',at=.32,y=.83,width=.57,depth=-.37,material=m('paper'))
poster(d,.54,1.92,.22,height=.43,text='',layout='grid')
sp,d=detail('248142711:1',0,'Narrow craft beer and smoke unit: red/white fascia, small projecting sign, glazed entry and product notices.','white enamel','bold',molding=False)
sign(sp,'BEER & SMOKE','bold','maroon enamel',y=3.10,height=.54)
poster(d,.64,1.52,.38,height=.70,text='',layout='grid')
for face,idx in [('248142711:1',1),('248142711:0',0)]:
 sp,d=detail(face,idx,'Goodnight Sonny: dark olive enamel, folded glass divisions, fine gold-striped dark canvas and source-specific outdoor seating.','black enamel','condensed',frameWidth=.065,baseMaterial=m('black enamel'))
 sp['signs']=[]
 awning(sp,'black canvas',y=3.60,drop=.47,depth=1.17,valance=.22,stripe=m('linen canvas'),stripeSpacing=.14,stripeWidth=.02,scalloped=True)
 sign(sp,'GOODNIGHT sonny','condensed','black enamel',y=3.92,height=.24,at=.72,width=.25)
 if face.endswith(':1'):
  sp['panels']=[['glass',.18],['glass',.18],['door',.19],['glass',.22],['door',.23]]
  for at in [.14,.35,.57,.78]:seating(d,at,1.05,wood='dark timber',profile='slat')
  for at in [.035,.91]:furniture(d,'barrel',at,1.06,material=m('dark timber'),width=.58,height=.55)
 else:
  d['closedShutter']=True;d['shutterMaterial']=m('dark iron');d['graffiti']={'ink':m('gray plaster'),'band':[.5,2.3]}
  for at in [.22,.48,.75]:furniture(d,'chair',at,.7,profile='mesh',material=m('dark iron'))
for face,idx in [('248142712:0',0),('248142712:1',0),('248142712:1',1)]:
 sp,d=detail(face,idx,'Cream corner cafe: narrow divided-light leaves, pale solid side shutters, black/cream striped retractable canopy and warm hanging globes.','cream enamel','condensed',frameWidth=.055,baseMaterial=m('cream enamel'))
 sp['smallPanes']=True
 if spec_aw:=sp.get('awning'):spec_aw.update(detail09=True,material=m('cream canvas'),stripe=m('black canvas'),stripeSpacing=.24,stripeWidth=.10,sidePanels=True)
 for at in [.25,.55,.82]:display(d,'pendant',at=at,y=2.42,depth=-.36)

# Eastern St. Marks, each basement/unit retains its separate entry and identity.
sp,d=detail('248142694:0',0,'Cecilia: dark green lower wall, cream inset display surround and small gold serif lettering on the left panel.','green enamel','serif',surround=m('cream enamel'),baseMaterial=m('green enamel'),frameWidth=.06)
sp['signs']=[];addtext(sp,'Cecilia',.19,1.82,.30,'serif','aged brass',.19)
for face in ['248142698:0','248142696:0']:
 sp,d=detail(face,0,'East Village Books lower entry with yellow/red signs and crowded visible books.' if face.endswith('698:0') else 'Colorfully framed basement unit adjoining the bookshop, with dark glass and a recessed right door.','dark timber' if face.endswith('698:0') else 'maroon enamel','serif',frameWidth=.065)
 if face.endswith('698:0'):
  sp['panels']=[['door',.36],['glass',.64]];sp['windowText']=[]
  sign(sp,'EAST VILLAGE BOOKS','serif','yellow enamel','printed red',y=2.02,height=.32,at=.68,width=.61)
  addtext(sp,'BOOKS',.68,1.27,.52,'bold','printed red',.23)
  display(d,'books',at=.68,y=.35,width=.51,rows=3,count=28,rowStep=.28,colors=[m('paper'),m('printed green'),m('printed red'),m('printed blue'),m('yellow enamel'),m('black enamel')])
 else:poster(d,.44,1.14,.45,height=.48,text='',layout='grid')
for idx in [0,1]:
 sp,d=detail('248142692:0',idx,'Xing Fu Tang: compact orange basement sign and glass counter front.' if idx==0 else 'Physical GraffiTea: weathered green lower front, decorative warm lettering and fine dark security grille.','orange enamel' if idx==0 else 'sage enamel','condensed' if idx==0 else 'script',frameWidth=.055)
 if idx==0:
  sign(sp,'XING FU TANG','condensed','orange enamel',y=1.84,height=.32);poster(d,.35,1.0,.23,height=.50,text='',layout='grid')
 else:
  sign(sp,'Physical GraffiTea','script','dark timber','aged brass',y=1.87,height=.27)
  sp['grille']=True;display(d,'jars',at=.5,y=.50,width=.70,rows=3,count=6)
for idx in [0,1]:
 sp,d=detail('248142695:0',idx,'98 pale blue-gray basement access with fine iron rails and closed/recessed glazing; no invented tenant.','navy enamel',molding=False,frameWidth=.045)
sp,d=detail('248142614:0',0,'100 left basement: metal grille and a pale blue open canopy frame, separate from Dumpling Man.','dark iron',molding=False,closedShutter=True)
sp,d=detail('248142614:0',1,'Dumpling Man: gray lower surround, red script name, projecting dumpling face, dense notices and a menu stand.','navy enamel','script',frameWidth=.05)
sign(sp,'Dumpling Man','script','red enamel',y=1.90,height=.25)
for at,y,w in [(.25,1.12,.22),(.65,1.42,.20),(.71,.96,.27)]:poster(d,at,y,w,height=.32,text='',layout='grid')
sp['boards']=[{'at':.93,'depth':.80,'height':.92,'frame':m('brushed steel')}]
d['dumplingLogo']=True
sp,d=detail('248142617:0',0,'Cakes shop: slender black divisions, warm illuminated shelves, white cakes lettering on the right display.','black enamel','condensed',frameWidth=.045,molding=False)
addtext(sp,'cakes',.68,1.92,.40,'condensed','warm white',.24)
display(d,'shelves',at=.62,y=.64,width=.53,rows=3,count=0,rowStep=.43)
display(d,'pendant',at=.63,y=2.44,depth=-.34)
for idx in [0,1]:
 sp,d=detail('248142616:0',idx,'Cafe Mogador: green fascia, striped pale/olive fabric, timber lower glazing, menu layers and planted street edge.','honey timber','serif',frameWidth=.07,baseMaterial=m('sage enamel'))
 for aw in arch('248142616:0').get('awnings',[]):aw.update(detail09=True,material=m('cream canvas'),stripe=m('olive canvas'),font='store09:serif',sidePanels=True)
 poster(d,.18,1.12,.24,height=.48,text='',material=m('paper'))
 for at in [.35,.75]:display(d,'pendant',at=at,y=1.58,depth=-.42)
 furniture(d,'planter',.15,.90,material=m('dark timber'),width=.5,height=.43)
sp,d=detail('248142619:0',0,'Anjelly basement: pale blue sign with blue letterforms above a dated closed metal shutter.','brushed steel','bold',molding=False,closedShutter=True)
sign(sp,'Anjelly','bold','white enamel','blue enamel',y=1.94,height=.37)
for idx in [0,1]:
 sp,d=detail('248142622:0',idx,'109 projecting timber shop bay with scalloped striped canvas, trellis lattice, window planting and little notices.','honey timber','serif',frameWidth=.075,baseMaterial=m('gray plaster'),rails=[.43])
 sp['awning'].update(detail09=True,material=m('linen canvas'),stripe=m('cream canvas'),stripeSpacing=.12,stripeWidth=.05,scalloped=True,sidePanels=True)
 d['lattice']=True
 for at in [.15,.62]:furniture(d,'planter',at,1.0,material=m('oak timber'),width=.65,height=.50)
 poster(d,.50,1.04,.25,height=.36,text='',material=m('paper'))
sp,d=detail('248142623:0',0,'110 broad pale-framed glazed frontage beside the painted site edge, posted blue/pale notices and shallow metal canopy.','cream enamel','condensed',frameWidth=.045,molding=False)
poster(d,.70,1.32,.25,height=.72,text='',material=m('printed blue'))
sp,d=detail('248142627:0',0,'Crif Dogs: basement dark timber/glass, bold slanted cream lettering with a star divider and red open light.','black enamel','narrow',frameWidth=.06)
sp['windowText']=[]
ss=sign(sp,'CRIF','narrow','black enamel',y=1.92,height=.42)
ss['lines'][0].update(offset=-.14,width=.23)
ss['lines'].append({**ss['lines'][0],'text':'DOGS','offset':.16})
addtext(sp,'CRIF',.39,1.58,.20,'narrow','warm white',.24)
addtext(sp,'DOGS',.62,1.58,.23,'narrow','warm white',.24)
d['crifStars']=[{'at':.5,'y':1.92,'radius':.10,'depth':.37},{'at':.5,'y':1.58,'radius':.078,'depth':.145}]
poster(d,.15,.79,.14,height=.30,text='',layout='grid')
sp,d=detail('248142631:0',0,'116 warm timber entry with red-framed low window bank and weathered decorative header.','honey timber','serif',baseMaterial=m('black enamel'),frameWidth=.07)
sp['panels']=[['door',.26],['glass',.25],['glass',.25],['glass',.24]]
d['panelFrames']={'1':m('red enamel'),'2':m('red enamel'),'3':m('red enamel')}
display(d,'counter',at=.67,y=.70,width=.57,depth=-.10)
sp,d=detail('248142634:0',0,'Romeo’s: cream facade, red classical line illustrations and cats/hearts, red door, white divided windows and green closed parasols.','cream enamel','serif',baseMaterial=m('cream enamel'),frameWidth=.07)
sp['panels']=[['door',.33],['glass',.34],['glass',.33]];d['doorSolidTop']=2.5;d['doorMaterial']=m('red enamel')
sign(sp,"ROMEO'S",'serif','cream enamel','printed red',y=3.01,height=.36)
for at in [.58,.77]:furniture(d,'closed-umbrella',at,.80,material=m('olive canvas'),height=2.35)
d['romeoGraphics']=True
sp,d=detail('248142636:0',0,'Hanoi House: weathered timber glazing, black valance with small No.119, leafy planters, warm interior pendants and slim outdoor tables.','dark timber','serif',frameWidth=.075)
sp['signs']=[];awning(sp,'black canvas',y=3.44,drop=.30,depth=.65,valance=.20,text='no. 119',textAt=.83,textWidth=.27,font='store09:serif',textSize=.14)
for at in [.22,.57]:display(d,'pendant',at=at,y=2.29,depth=-.43)
seating(d,.27,1.03,width=.51,wood='dark timber');furniture(d,'planter',.83,.79,material=m('dark timber'),height=.66,width=.47)
sp['boards']=[{'at':.95,'depth':1.20,'height':.89,'text':'HANOI HOUSE','frame':m('cream enamel')}]
sp,d=detail('248142641:0',0,'121 left dark metal room with paired broad glass leaves, shallow canopy and hanging pale blade.','black enamel','condensed',molding=False,frameWidth=.055)
poster(d,.16,1.6,.14,height=.60,text='',material=m('paper'))
sp['lights']=[.12,.52,.88]
sp,d=detail('248142641:0',1,'Moody Tongue: sculpted dark lettering over dark tiled piers and glazed lower opening.','black tile','bold',surround=m('black tile'),frameWidth=.06)
sign(sp,'MOODY TONGUE','bold','gray plaster','black enamel',y=3.17,height=.60)
addtext(sp,'PST',.56,2.56,.35,'bold','aged brass',.19)
for idx in [0,1]:
 sp,d=detail('248142643:0',idx,'122 left dark bar with broad pale-striped canopy and open glazing.' if idx==0 else 'Holyland Market: slate fascia with pale serif title and smaller grocery line above closed gray roller shutters.','dark timber' if idx==0 else 'navy enamel','serif',frameWidth=.055,closedShutter=idx==1)
 if idx==1:
  ss=sign(sp,'HOLYLAND MARKET','serif','navy enamel',y=3.12,height=.55)
  ss['lines'].append({'text':'Fine Kosher Grocery','size':.12,'y':-.34,'style':'store09:serif','material':m('warm white')})
  d['shutterMaterial']=m('brushed steel');d['graffiti']={'ink':m('black enamel'),'band':[.65,2.40]}
 else:sp['awning'].update(detail09=True,material=m('cream canvas'),stripe=m('black canvas'),stripeSpacing=.27,stripeWidth=.10)
for idx in [0,1]:
 sp,d=detail('248142649:0',idx,'126 dark restaurant glazing with pale retractable striped canopy and individually framed doors.','dark timber','serif',frameWidth=.06)
 if sp.get('awning'):sp['awning'].update(detail09=True,material=m('cream canvas'),stripe=m('black canvas'),stripeSpacing=.25,stripeWidth=.10)
sp,d=detail('248142655:0',0,'Cafe Aperitif: black and gold scalloped canopy, open right display/flower box, narrow glass left door and blue bistro chairs.','black enamel','narrow',frameWidth=.07,baseMaterial=m('black enamel'))
awning(sp,'black canvas',y=3.37,drop=.35,depth=.92,valance=.22,text='Caffè   Aperitivo   Dinner   Cocktail   Bar',letters=m('aged brass'),font='store09:narrow',textSize=.17,scalloped=True)
sp['panels']=[['door',.29],['glass',.71]]
furniture(d,'planter',.66,.35,material=m('black enamel'),width=1.45,length=.30,height=.68,stems=15)
seating(d,.48,1.10,wood='blue enamel');sp['boards']=[{'at':.16,'depth':1.0,'height':.83,'frame':m('honey timber')}]

# Avenue A corner returns: cafe and separate wood-front business; painted bar.
for face,idxs in [('248142709:0',[0,1,2]),('248142709:1',[0,1])]:
 for idx in idxs:
  star=(face.endswith(':0') and idx==0) or (face.endswith(':1') and idx==1)
  sidewood=face.endswith(':0') and idx==1
  sp,d=detail(face,idx,'Starbucks: bronze/dark glazing, pale stone piers, low cream panels and spaced light fascia letters.' if star else 'Independent dark timber shop with small panes and purple cloth over one window.' if sidewood else 'Separate corner unit with fine dark mullions, pale posted/covered pane and small notices.','dark timber' if sidewood else 'black enamel','bold',frameWidth=.05,surround=m('gray plaster') if star else m('dark timber') if sidewood else m('cream enamel'))
  if star:sign(sp,'STARBUCKS','bold','black enamel',y=3.07,height=.40)
  if sidewood:
   sp['smallPanes']=True
   display(d,'cloth',at=.22,y=2.19,width=.32,height=.54,material=m('purple canvas'))
  elif not star:poster(d,.26,1.7,.27,height=.9,text='',material=m('paper'))
  else:display(d,'counter',at=.54,y=.69,width=.70,depth=-.33,material=m('cream enamel'))
for face in ['248142706:0','248142706:1']:
 sp,d=detail(face,0,'Bar Al Pastor: warm honey timber folding leaves, heavily layered painted base/fascia, narrow glass entry and corner blade.','honey timber','condensed',frameWidth=.075,baseMaterial=m('gray plaster'))
 sp['panels']=[['glass',.12]]*6+[['door',.16],['glass',.12]] if face.endswith(':0') else [['glass',.12]]*6+[['door',.28]]
 sp.update(smallPanes=False,base=.85)
 d['paintLayers']=[
  {'span':[.02,.39],'band':[.24,.79],'variant':'bubble','ink':m('paper'),'fill':m('printed blue')},
  {'span':[.46,.96],'band':[.22,.78],'variant':'bubble','ink':m('printed red'),'fill':m('gray plaster')},
  {'span':[.03,.38],'band':[3.14,3.57],'variant':'collage','ink':m('paper'),'depth':.31},
  {'span':[.37,.70],'band':[3.12,3.52],'variant':'bubble','ink':m('paper'),'fill':m('sage enamel'),'depth':.31},
  {'span':[.70,.98],'band':[3.15,3.57],'variant':'ghost','ink':m('paper'),'depth':.31}]
 sp['boards']=[{'at':.55,'depth':.92,'height':.93,'text':'BAR AL PASTOR','frame':m('honey timber')}]

# Ground-floor businesses which revision 08 represented as architectural
# openings, not returnShops, receive their own authored feature packet too.
def extra_record(face,name,identity,sources):
 record={'id':face+':architecture','faceId':face,'shopIndex':None,'displayName':name,'identity':identity,
         'sourceIds':sources,'observed':[identity],
         'unknown':['Fine dimensions, graphic curves and font substitutions are authored estimates.'],
         'state':'authored; final-game detail review pending'}
 BUSINESSES.append(record);return face_extra(face)
def face_words(x,text,at,y,width,size,font='condensed',ink='warm white',panel=False,material='red enamel',height=.4):
 x['signs'].append({'at':at,'y':y,'width':width,'height':height,'depth':.22,'panel':panel,'material':m(material),
                   'lines':[{'text':text,'size':size,'style':'store09:'+font,'material':m(ink)}]})

x=extra_record('248142689:0','Fun City Tattoo','Bright red painted frontage with distinct cream, yellow and blue display lettering, central arched entrance and black stair rails.',['stmarks-south-east45-detail'])
x['paintSurround']={'material':m('red enamel'),'top':3.62}
arch('248142689:0')['signs']=[]
for w in arch('248142689:0')['windows']:
 if w['bottom']<4:
  w.update(at=.255 if w['at']<.5 else .815,width=.165 if w['at']<.5 else .235,rails=[],columns=1)
for text,at,y,width,size,font,ink in [
 ("Big Steve’s",.08,2.79,.135,.18,'script','warm white'),('WORLD FAMOUS',.08,2.53,.13,.08,'narrow','warm white'),
 ('FUN',.08,2.24,.13,.29,'bold','warm white'),('CITY',.08,1.96,.13,.29,'bold','warm white'),
 ('FUN CITY',.81,3.23,.28,.35,'bold','blue enamel'),
 ("Manhattan’s Oldest",.24,.65,.36,.25,'script','warm white'),("The Big Apple’s Finest",.81,.65,.29,.18,'script','warm white')]:face_words(x,text,at,y,width,size,font,ink)
for word,at in [('TATTOOING',.38),('EXCELLENCE',.65)]:
 for j,ch in enumerate(word):face_words(x,ch,at,2.78-j*.195,.042,.20,'bold','aged brass')
for j,word in enumerate(['TRADITIONAL','TRIBAL','LETTERING','JAPANESE']):face_words(x,word,.08,1.62-j*.16,.13,.075,'condensed','aged brass')

x=extra_record('248142630:0','Augurs Well','Gray canvas valance with outlined narrow letters, silver closed shutters painted with large eyes and tags, vertical center menu and stacked metal chairs.',['stmarks-north-east145-detail'])
x['augursEyes']=True
aw=arch('248142630:0')['awnings'][0];aw.update(detail09=True,material=m('linen canvas'),text='AUGURS WELL',font='store09:narrow',textSize=.27)
x['displays']=[{'kind':'poster','at':.49,'y':1.35,'width':.052,'height':.92,'depth':.25,'material':m('paper')}]
x['furniture']=[{'kind':'square-table','at':.24,'depth':1.0,'width':1.05,'material':m('brushed steel')}]
for at in [.17,.32]:x['furniture'].append({'kind':'chair','at':at,'depth':1.0,'floor':.90,'profile':'mesh','material':m('brushed steel')})

# La Palapa's street enclosure is a projecting set of timber/glass folding
# leaves under the canvas structure; the raised residential door stays behind.
a=arch('241822271:0');a['returnShops'].append({'name':'LA PALAPA street enclosure','span':[.39,.985],'projection':1.25,
 'design':{'top':2.72,'head':2.53,'base':.27,'recess':.035,'panels':[['glass',.25],['door',.25],['door',.25],['glass',.25]],'smallPanes':True,'signs':[]}})
sp,d=detail('241822271:0',1,'La Palapa projecting street enclosure: four warm timber glazed leaves with small panes and pale fabric sides below the tan canopy.','honey timber','serif',frameWidth=.055,doorSolidTop=.29)
sp['awning']={'detail09':True,'y':2.91,'drop':.14,'depth':.35,'material':m('linen canvas'),'valance':.10}
for at in [.04,.95]:display(d,'cloth',at=at,y=1.54,width=.09,height=2.1,material=m('linen canvas'),depth=.1)

# Close-view corrections to the individual packets.
sp=arch('248142696:0')['returnShops'][0]['design'];sp['detail09']['checkerPiers']=True
sp.update(panels=[['glass',.76],['door',.24]],base=.14,top=2.26,head=1.94)
sign(sp,'S O C K S','bold','rose enamel','paper',y=2.18,height=.38)
sp=arch('241822308:0')['returnShops'][2]['design'];sp['detail09']['displays']=[]
sign(sp,'SQUARE COFFEE','condensed','black enamel',y=3.05,height=.26)
poster(sp['detail09'],.22,2.37,.35,height=.62,text='SQUARE',material=m('paper'))
poster(sp['detail09'],.30,1.25,.16,height=.45,text='',layout='grid')
sp=arch('248142636:0')['returnShops'][0]['design'];sp['awning'].update(text='HÀ NỘI HOUSE     no. 119',textAt=.57,textWidth=.84)
for at in [.17,.43,.72]:addtext(sp,'HÀ NỘI HOUSE',at,1.65,.21,'serif','warm white',.085)
for idx in [0,1]:
 sp=arch('248142616:0')['returnShops'][idx]['design']
 for at in ([.20,.60] if idx==0 else [.5]):seating(sp['detail09'],at,1.10,wood='red enamel')
for aw in arch('248142616:0')['awnings']:
 aw.update(material=m('linen canvas'),stripe=None,depth=1.35)

# Retire older overlays only when their owning replacement is present.
arch('248142709:1')['signs']=[]
arch('248142706:1').pop('boards',None)
arch('248142630:0').pop('menus',None)
arch('241822308:0')['returnShops'][0]['design']['detail09']['graffiti']['variant']='vacant-outline'
arch('248142711:0')['returnShops'][0]['design']['detail09']['graffiti']['variant']='ghost'
arch('248142643:0')['returnShops'][1]['design']['detail09']['graffiti']['variant']='bubble'

expected={r['faceId']+':'+str(i) for r in S['elevations'] for i,_ in enumerate(r['architecture'].get('returnShops',[]))}
assert SEEN==expected,(sorted(expected-SEEN),sorted(SEEN-expected))
S.update(revision='09',status='Individual storefront revision; final game review pending',storefrontObservationLedger='model-source/storefront-observations-09.json')
LEDGER['businesses']=BUSINESSES
LEDGER_PATH.write_text(json.dumps(LEDGER,indent=2,ensure_ascii=False)+'\n')
PATH.write_text(json.dumps(DATA,indent=2,ensure_ascii=False)+'\n')
print('STOREFRONT_09_AUTHORED',len(BUSINESSES),'exact business units on',len({b['faceId'] for b in BUSINESSES}),'faces')
