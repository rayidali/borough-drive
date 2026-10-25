"""Only the 27 assigned Tenth owners dispatch here. Source pixels stay private.

The original core is not an input to these facade generators. All dimensions
beyond mapped footprint/height are visual estimates pending served review.
"""
E10_BLOCK_IDS={247851894,247851895,247851896,247851897,247851898,247851899,247851900,247851901,247851902,247851903,247851904,247851906,247851908,247851911,247851935,247852656,247852658,247852659,247852660,247852662,247852663,247852664,247852665,247852667,247852668,247852693,247852694}
for name,color,kind in [('orange canvas',(.80,.29,.09),5),('pink wall',(.68,.34,.46),0),('pale blue',(.60,.74,.75),1),('frosted cyan',(.54,.67,.64),0),('cream panel',(.84,.80,.68),2),('maroon',(.38,.08,.10),1),('red panel',(.59,.055,.055),2),('brown canvas',(.30,.28,.24),5)]:
 material('et '+name,color,.84)
 if kind:MATS['et '+name]['storefront09Surface']=kind

def et_scaffold(f,h):
 # April 2026 temporary construction, over the retained earlier architecture.
 # Open geometric screen approximates mesh; no source pixels are embedded.
 for j in range(math.ceil(f.L/2.8)+1):
  x=min(f.L,j*2.8)
  f.line((x,.17,1.48),(x,3.93,1.48),.032,'eb silver metal')
  f.line((x,4.05,1.35),(x,h+.45,1.35),.035,'et red panel')
  if j%2==0 and x+2.8<f.L:
   f.line((x,.22,1.48),(x+2.8,3.80,1.48),.025,'eb silver metal')
 for y in [1.1,2.7,3.85]:f.line((0,y,1.48),(f.L,y,1.48),.026,'eb silver metal')
 f.b(f.L/2,3.90,.77,f.L,.15,1.55,'eb gray metal')
 f.b(f.L/2,4.23,1.46,f.L,.58,.07,'eb green wood')
 for y in range(5,math.ceil(h)+1,3):f.line((0,y,1.35),(f.L,y,1.35),.025,'et red panel')
 for j in range(round(f.L/.075)+1):
  x=j*f.L/round(f.L/.075);f.quad(x,(4.53+h+.40)/2,.030,h-4.13,1.29,'eb iron')
 for j in range(round((h-4.13)/.075)+1):
  y=4.53+j*.075;f.quad(f.L/2,y,f.L,.030,1.30,'eb iron')

def et_text(f,s,y,w,h,text,mat='store09 paper',d=.20,font='serif'):
 # Keep the letterforms' natural aspect ratio; width is a maximum, not a stretch.
 font='bold:1:0.18' if font=='italic' else 'bold' if font=='sans' else font
 obj=nb_text(f,s,y,w,h,text,mat,d,font)
 if not obj:return
 bpy.context.view_layer.update()
 bw=max(v[0] for v in obj.bound_box)-min(v[0] for v in obj.bound_box)
 bh=max(v[1] for v in obj.bound_box)-min(v[1] for v in obj.bound_box)
 obj.scale.x=min(w,h*bw/max(.001,bh)*1.12)/max(.001,bw)
 n01_center_text(obj,f,s,y,d);return obj

def et_canopy(f,a,b,color,text='',font='serif',y=3.50,drop=.45,dep=.85,letter='store09 paper'):
 observed_awning(f,a,b,{'detail09':True,'y':y,'drop':drop,'depth':dep,'valance':.22,'material':color,'sidePanels':True})
 if text:
  yy=y-drop*.53;d=.10+(y-yy)/drop*dep+.020
  obj=et_text(f,(a+b)/2,yy,(b-a)*.87,.24,text,letter,d,font)
  slope=math.atan2(drop,dep);cs=math.cos(slope);sn=math.sin(slope)
  obj.rotation_euler=Matrix((Vector((f.rx,-f.rz,0)),Vector((-f.nx*cs,f.nz*cs,sn)),Vector((f.nx*sn,-f.nz*sn,cs)))).transposed().to_euler();obj.scale.y/=sn;n01_center_text(obj,f,(a+b)/2,yy,d)

def et_mask(f,x,y,scale,mat):
 # Authored shallow face/foliate silhouette, not a cast of the real carving.
 p02_disc(f,x,y,.10*scale,.13*scale,.21,mat,12)
 for side in [-1,1]:
  p02_ring(f,x+side*.055*scale,y+.025*scale,.025*scale,.025*scale,.235,mat,.01*scale,10)
  ee_scroll(f,x+side*.16*scale,y,.055*scale,mat,.18)
 f.b(x,y-.035*scale,.25,.032*scale,.080*scale,.04,mat)

def et_fan(f,x,y,rx,ry,mat,depth=.20):
 # Filled masonry pediment, with shallow foliate carving in front.
 points=[f.p(x,y,depth)]+[f.p(x+rx*math.cos(j*math.pi/24),y+ry*math.sin(j*math.pi/24),depth) for j in range(25)]
 ee_front(points,mat);eb_arc(f,x,y,rx,ry,depth+.035,.075,mat)
 for dx in [-.42,0,.42]:ee_scroll(f,x+dx*rx,y+ry*.35,ry*.16,mat,depth+.06)

class EtCarvedRelief:
 # Same centerlines, widths and projecting profile; no hidden cylinder backs.
 # This adapter is used only for attached Tenth masonry, never free ironwork.
 def __init__(self,f):self.f=f
 def line(self,a,b,r,mat):fidelity_stroke(self.f,a,b,r,mat)

def et_foliage(f,a,b,y,mat,depth=.17):
 relief=EtCarvedRelief(f)
 for j in range(max(1,round((b-a)/.35))):
  x=a+(j+.5)*(b-a)/max(1,round((b-a)/.35))
  for side in [-1,1]:
   ee_scroll(relief,x+side*.07,y,.065,mat,depth)
   f.line((x,y-.065,depth),(x+side*.11,y+.065,depth),.016,mat)

def et_closed_box(f,a,b,seed,mat='eb iron'):
 f.b((a+b)/2,.45,.90,b-a,.56,.055,mat)
 ee_front([f.p(a,.73,.90),f.p(b,.73,.90),f.p(b,1.02,.06),f.p(a,1.02,.06)],mat)
 for x in [a,b]:ee_front([f.p(x,.17,.06),f.p(x,.17,.90),f.p(x,.73,.90),f.p(x,1.02,.06)],mat)
 p03_tags(f,a+.05,b-.05,.25,.63,.94,seed)
 for x in [a,b]:f.line((x,.73,.91),(x,1.02,.06),.014,'eb gray metal')
 # Freestanding round utility cover beside the hatch, observed on this row.
 p02_disc(f,a+.10,.63,.25,.34,.12,'eb iron',24)

def et_oriel(f,w,mat):
 x=w['at']*f.L;ww=w['width']*f.L*1.42;y=w['bottom'];hh=w['height'];a=x-ww/2;b=x+ww/2
 OPENINGS[frontage_key(f)].append((a,y-.17,b,y+hh+.17))
 def depth(s):return .08+.62*math.sqrt(max(0,1-((s-x)/(ww/2))**2))
 for j in range(18):
  l=a+ww*j/18;r=a+ww*(j+1)/18;dl=depth(l);dr=depth(r)
  for lo,hi in [(y-.22,y+.08),(y+hh-.08,y+hh+.23)]:ee_front([f.p(l,lo,dl),f.p(r,lo,dr),f.p(r,hi,dr),f.p(l,hi,dl)],mat)
  ee_front([f.p(l,y+.08,dl),f.p(r,y+.08,dr),f.p(r,y+hh-.08,dr),f.p(l,y+hh-.08,dl)],'seventh reflective glass')
  for yy in [y-.23,y+.08,y+hh*.51,y+hh-.08,y+hh+.23]:f.line((l,yy,dl+.025),(r,yy,dr+.025),.028,mat if yy in [y-.23,y+hh+.23] else 'eb sash')
  # Curved lower hanging bowl, with no rectangular box hiding its silhouette.
  ee_front([f.p(l,y-.23,dl),f.p(r,y-.23,dr),f.p(r,y-.57,dr*.36),f.p(l,y-.57,dl*.36)],mat)
 for t in [0,1/3,2/3,1]:
  s=a+ww*t;f.line((s,y+.06,depth(s)+.04),(s,y+hh-.04,depth(s)+.04),.034,'eb sash')
 for side in [-1,1]:
  xx=x+side*ww*.30;f.b(xx,y-.58,.23,.12,.34,.30,mat);p02_ring(f,xx,y-.55,.07,.11,.42,mat,.025,18)
 et_mask(f,x,y-.40,.85,mat)

def et_hatch(f,a,b,opened=False,below=.9):
 if not opened:
  ee_front([f.p(a,.18,1.0),f.p(b,.18,1.0),f.p(b,.82,.07),f.p(a,.82,.07)],'eb iron')
  for xx in [a,(a+b)/2,b]:f.line((xx,.18,1.0),(xx,.82,.07),.017,'eb gray metal')
  f.b((a+b)/2,.50,.56,.18,.035,.028,'eb gray metal');return
 # Separate raised leaves and open central air; steps descend beneath pavement.
 for xx,sign in [(a,-1),(b,1)]:
  ee_front([f.p(xx,.16,.06),f.p(xx,.16,1.08),f.p(xx+sign*.26,1.06,1.08),f.p(xx+sign*.26,1.06,.06)],'eb iron')
 for j in range(7):
  yy=.16-(j+1)*(below+.16)/7;dd=1.08-(j+.5)*1.02/7
  f.b((a+b)/2,yy-.045,dd,b-a,.09,1.02/7,'eb gray stone')

SHOP09_FONTS['japanese']=bpy.data.fonts.load(str(ROOT/'model-source/fonts/tenth/NotoSansJP.ttf'))

def et_japanese(f,x,y,w,text,mat,d,height=.32):
 return et_text(f,x,y,w,height,text,mat,d,'japanese')

class EtDeepShopFacade(FidelityProjectedFacade):
 def __init__(self,f):
  super().__init__(f,0);self.wall='et cream panel'
 def b(self,s,y,d,w,h,depth,mat):
  if mat=='recess shadow':d-=1.25
  self.base.b(s,y,d,w,h,depth,mat)

def et_japanese_blade(f,s,y,text):
 f.line((s,y+.3,.1),(s,y+.3,.9),.018,'eb iron')
 for flip in [False,True]:
  p=f.p(s+(.035 if flip else -.035),0,.90 if flip else .18)
  ff=Facade(p[0],p[2],(-1 if flip else 1)*f.nx,(-1 if flip else 1)*f.nz,.72)
  p02_disc(ff,.36,y,.32,.32,0,'eb red wood',32)
  et_text(ff,.36,y,.54,.18,text,'eb gold metal',.035,'japanese')

_et_previous_shop=photographed_shop
def photographed_shop(f,a,b,r):
 detail=r['design'].get('detailE10Block')
 if not detail:return _et_previous_shop(f,a,b,r)
 k=detail['kind'];w=b-a;c=(a+b)/2
 if k=='prince':
  ff=EtDeepShopFacade(f)
  for j in range(5):
   x=a+w*(j+.5)/5;ww=w/5-.19
   if j==2:fidelity_door(ff,{'at':x/f.L,'width':ww/f.L,'bottom':.17,'top':3.22,'leafTop':2.7,'material':'eb iron','trim':'et cream panel','shape':'round','recess':.24,'panels':[{'y':.53,'height':.78,'width':.88,'glass':True}]})
   else:fidelity_window(ff,{'at':x/f.L,'width':ww/f.L,'bottom':.35,'height':2.87,'shape':'round','frame':'eb iron','trim':'et cream panel','glassMaterial':'store09 clear glass','recess':-.22,'rails':[.80],'hood':'round'})
   for side in [-1,1]:f.b(x+side*(ww/2+.05),1.76,.12,.10,3.12,.20,'et cream panel')
   if j!=2:
    f.b(x,1.53,-.59,ww*.91,2.32,.025,'eb pale fabric')
    for q in range(9):f.b(x-ww*.43+q*ww*.1075,1.53,-.55,ww*.07,2.32,.065,'eb pale fabric')
   ee_chair(f,x,.90,'eb oak wood',True)
  fidelity_clipped_surface(f,a,b,.17,3.78,.04,.08,'et cream panel')
  et_text(f,c,3.49,w*.45,.38,'Prince','eb iron',.12,'script');et_text(f,c,3.19,w*.24,.13,'TEA HOUSE','eb iron',.12,'sans');return
 _et_previous_shop(f,a,b,r)
 if k in ['rairaiken','shabutatsu']:
  # Close the shallow display recess at both ends. The oblique review exposed
  # the outside world through the edge of these otherwise bounded windows.
  head=r['design']['head'];base=r['design']['base']
  f.b(c,(head+base)/2,-1.05,w,head-base,.06,'recess shadow')
  for x in [a+.025,b-.025]:f.b(x,(head+base)/2,-.51,.05,head-base,1.10,'eb iron')
  for yy in [base,head]:f.b(c,yy,-.51,w,.05,1.10,'eb iron')
 if k.startswith('marinara'):
  cursor=a
  for panel,fraction in r['design']['panels']:
   pw=w*fraction;x=cursor+pw/2
   if panel=='window':
    f.b(x,1.58,-.08,pw-.14,2.12,.025,'et frosted cyan')
    f.b(x,2.55,.03,pw-.12,.065,.08,'et red panel')
    f.b(x,1.37,.03,pw-.12,.065,.08,'et red panel')
    f.b(x,2.77,-.08,pw-.14,.36,.025,'et frosted cyan')
    if pw>2.5:f.b(x,2.77,.03,.06,.43,.08,'et red panel')
    eb_panel(f,cursor+.07,cursor+pw-.07,.47,.50,'et red panel',.11)
   cursor+=pw
  if k=='marinara-return':
   eb_panel(f,a,b,3.48,.56,'eb white wood');et_text(f,c,3.48,w*.80,.31,'Marinara','et red panel',.27,'script')
   observed_awning(f,a,b,{'detail09':True,'y':3.25,'drop':.38,'depth':.90,'valance':.20,'material':'eb white canvas','scalloped':True})
   et_text(f,c,2.77,w*.65,.14,'160  PIZZA','eb iron',1.03,'serif')
  else:
   eb_panel(f,a,a+w*.30,3.48,.56,'eb white wood');et_text(f,a+w*.15,3.48,w*.26,.31,'Marinara','et red panel',.27,'script')
   observed_awning(f,a,a+w*.30,{'detail09':True,'y':3.25,'drop':.38,'depth':.90,'valance':.20,'material':'eb white canvas','scalloped':True})
   for j in range(4):
    x=a+w*(.37+j*.17);f.b(x,2.03,.19,.07,.80,.13,'eb gold metal');f.b(x,2.03,.27,.035,.68,.03,'opal lamp')
   f.b(c,.28,1.3,w,.20,2.4,'eb brown stone')
   for yy in [.48,1.21]:f.line((a,yy,2.6),(b,yy,2.6),.025,'et red panel')
   for j in range(round(w/.14)):f.line((a+j*.14,.48,2.6),(a+j*.14,1.21,2.6),.009,'et red panel')
  for x in [a+w*.22,a+w*.68]:ee_round_table(f,x,1.65);ee_chair(f,x-.5,1.65);ee_chair(f,x+.5,1.65)
 elif k=='juicepress':
  et_canopy(f,a,b,'eb black canvas','JUICE PRESS','sans');et_text(f,c,2.41,w*.93,.23,'NON PROCESSED','store09 paper',.05,'condensed')
  f.b(a+w*.32,1.20,.08,w*.58,1.95,.06,'eb plywood');et_text(f,b-w*.16,1.47,w*.25,.12,'RAW','store09 paper',.09,'sans')
  for side in [-1,1]:f.line((b-w*.25+side*.18,.18,.82),(b-w*.25+side*.18,2.47,.13),.018,'eb silver metal')
  for j in range(8):f.line((b-w*.25-.18,.35+j*.27,.77-j*.08),(b-w*.25+.18,.35+j*.27,.77-j*.08),.015,'eb silver metal')
 elif k=='matchahouse':
  et_canopy(f,a,b,'eb green canvas','MATCHA HOUSE','sans',y=3.50,dep=.70);eb_blade(f,b-.06,3.1,'MATCHA','eb green wood');eb_board(f,b-.25,.17,'MATCHA|HOUSE',d=1.1)
  for j in range(6):f.b(a+w*(.12+j*.085),.75,-.30,.15,.13,.15,'eb green wood')
 elif k=='cleaner':
  et_canopy(f,a,b,'eb blue canvas','168 DRY CLEANERS','italic',y=3.48,drop=.62,dep=.86)
  et_text(f,c,2.69,w*.92,.12,'WASH DRY FOLD • ALTERATIONS','store09 paper',.99,'sans');nb_ac(f,b-w*.18,2.48,.64,.36,.18)
  for j in range(3):f.b(a+w*(.18+j*.18),1.5,.02,.34,.47,.012,'store09 paper')
  eb_clothes(f,a+w*.40,b-.1,1.9)
 elif k=='pourquoi':
  et_canopy(f,a,b,'eb white canvas','POURQUOI PAS','italic',letter='eb iron',dep=.65)
  nb_grille(f,a+.03,b-.03,.60,2.7,.18);f.b(c,.39,.15,w-.06,.42,.06,'eb silver metal');eb_blade(f,b-.03,3.1,'POURQUOI','eb white wood',color='eb iron')
 elif k in ['records','galactic']:
  eb_panel(f,a,b,1.22,.32,'eb iron');et_text(f,c,1.23,w*.9,.15,'Limited' if k=='records' else 'GALACTIC','store09 paper' if k=='records' else 'et red panel',.26,'script' if k=='records' else 'sans')
  nb_grille(f,a+.03,b-.03,-.60,1.06,.15)
  if k=='records':
   f.b(a+w*.64,.70,1.10,.60,.91,.045,'store09 paper');et_text(f,a+w*.64,.98,.50,.11,'OPEN','eb blue enamel',1.13,'sans');et_text(f,a+w*.64,.81,.52,.065,'WE BUY & SELL','eb green wood',1.13,'sans');et_text(f,a+w*.64,.71,.45,.08,'VINYL','eb green wood',1.13,'sans');p02_disc(f,a+w*.64,.47,.12,.12,1.13,'eb iron',24);p02_disc(f,a+w*.64,.47,.03,.03,1.14,'store09 paper',12)
  else:et_text(f,c,.98,w*.74,.13,'SMOKERS','store09 paper',.25,'sans')
 elif k=='waxing':
  eb_panel(f,a,b,3.21,.47);et_text(f,c,3.21,w*.92,.27,'Waxing Studio NYC','eb pink enamel',.27,'script')
  f.b(c,1.4,-.97,w-.1,2.3,.025,'et pink wall')
  for j in range(3):ee_portrait(f,a+w*(.14+j*.18),.73,.36,.58,.06)
  et_text(f,b-w*.16,2.20,w*.25,.12,'OPEN','ee pink letters',.04,'sans')
 elif k=='barber':
  eb_panel(f,a,b,3.22,.35);et_text(f,c,2.60,w*.94,.16,'EAST VILLAGE BARBER SHOP','store09 paper',.06,'condensed');eb_blade(f,b-.03,3.04,'BARBER','et pale blue',color='eb iron')
  for t in [.22,.73]:
   x=a+w*t;p02_ring(f,x,1.68,.19,.23,.03,'store09 paper',.015,30);et_text(f,x,1.68,.27,.15,'EV','store09 paper',.035,'serif')
   f.b(x,1.55,-.92,.72,1.5,.025,'seventh reflective glass');shop09_frame(f,x,1.55,.78,1.56,-.88,'eb silver metal',.025)
   f.b(x,.61,-.45,.48,.12,.43,'eb iron');f.b(x,.97,-.68,.48,.61,.08,'eb iron');rod(f.p(x,.18,-.45),f.p(x,.58,-.45),.055,'eb silver metal',12)
 elif k=='madamevo':
  et_canopy(f,a,b,'et orange canvas','MADAME','sans',y=3.60,drop=.57,dep=1.06);et_text(f,c,3.04,w*.32,.20,'VO','store09 paper',1.20,'sans')
  eb_blade(f,b-.08,3.25,'MADAME VO','et orange canvas',icon='flower')
  for x in [a+w*.18,c,b-w*.12]:eb_lamp(f,x,3.80,.58)
  for x in [a+w*.12,b-w*.11]:eb_plant(f,x,.18,.85,.72)
  et_text(f,a+w*.27,2.03,w*.26,.16,'OPEN','ee red orange',.07,'script')
  for j in range(3):ee_chair(f,b-w*.2,.83+j*.12,'eb oak wood',True)
  eb_board(f,a+w*.56,.17,'MADAME VO|MENU',d=.85)
 elif k=='ando':
  et_canopy(f,a,b,'et brown canvas','ando','sans',y=3.45,drop=.42,dep=.75);et_text(f,b-.20,2.91,.30,.10,'214','store09 paper',.90,'sans')
  et_hatch(f,a+w*.13,a+w*.80,True,1.1)
  for x in [a+w*.20,a+w*.49]:eb_plant(f,x,.67,-.35,.45)
  ee_animal(f,a+w*.61,.88,.32,.45,'eb brown stone',-.31)
  ee_round_table(f,c,2.10);ee_chair(f,c-.5,2.1);ee_chair(f,c+.5,2.1)
 elif k in ['214closed','220closed']:
  if k=='214closed':
   ee_shutter(f,a+.04,b-.04,top=2.85);p03_tags(f,a+.10,b-.10,.45,2.30,.25,214)
   for x in [a,b]:f.line((x,3.18,.07),(x,2.80,.85),.025,'eb gray metal')
   f.line((a,2.8,.85),(b,2.8,.85),.025,'eb gray metal')
  else:nb_grille(f,a+.03,b-.03,.2,2.85,.14);eb_panel(f,a,b,3.13,.25,'eb gray metal')
 elif k=='rairaiken':
  for j in range(8):f.b(c,3.03+j*.08,.15,w,.048,.15,'eb iron')
  # Separate stepped sign, floating within the long black slatted fascia.
  shape=[(-.50,-.38),(-.43,-.38),(-.43,-.50),(.43,-.50),(.43,-.38),(.50,-.38),(.50,.38),(.43,.38),(.43,.50),(-.43,.50),(-.43,.38),(-.50,.38)]
  ee_front([f.p(c+x*w*.54,3.28+y*.64,.28) for x,y in shape],'eb iron')
  border=[(c+x*w*.51,3.28+y*.58,.33) for x,y in shape]
  for i in range(len(border)):f.line(border[i],border[(i+1)%len(border)],.010,'eb gold metal')
  et_japanese(f,c,3.34,w*.44,'軒 々 来','eb gold metal',.35,.31);et_text(f,c,3.08,w*.34,.075,'RAI RAI KEN','eb gold metal',.35,'serif')
  et_japanese_blade(f,b-.04,3.13,'来々軒')
  for j in range(10):f.b(a+w*.86,.37+j*.035,.15,w*.26,.017,.05,'eb oak wood')
  for j in range(3):f.b(a+w*.60,1.30+j*.40,.06,.26,.31,.015,'store09 paper')
  f.b(a+w*.46,1.61,.08,.09,2.80,.12,'et red panel');eb_bottles(f,a+.1,a+w*.42,.70,rows=1)
 elif k=='shabutatsu':
  # Four independently observed divisions, from September 2024 close views.
  for x in [a,a+w*.22,a+w*.40,a+w*.61,b]:f.b(x,1.53,.12,.11,2.72,.16,'eb iron')
  # Separate honey-colored door, narrow glazed slit and carved vertical bars.
  dx=a+w*.31;dw=w*.18-.12
  f.b(dx,1.36,.015,dw,2.36,.05,'eb oak wood')
  f.b(dx,1.63,.055,dw*.62,1.32,.025,'store09 clear glass')
  for j in range(4):f.b(dx-dw*.30+j*dw*.20,1.63,.08,.026,1.34,.04,'eb oak wood')
  f.line((dx-dw*.31,1.05,.10),(dx-dw*.31,1.42,.10),.015,'eb iron')
  # Pale shoji-like screen is the tall adjacent window, not part of the door.
  sx=a+w*.505;sw=w*.21-.12
  f.b(sx,1.55,.01,sw,2.48,.025,'eb pale fabric')
  for j in range(7):f.b(sx-sw*.46+j*sw*.1533,1.55,.065,.024,2.48,.035,'eb oak wood')
  for yy in [.38,1.18,1.96,2.75]:f.b(sx,yy,.07,sw,.026,.04,'eb oak wood')
  # Tilted individual timber plaque over this doorway, with a small red seal above.
  px=dx;py=3.14;pw=dw*1.40;ph=.52;tilt=.13
  def signpoint(x,y,depth):return f.p(px+x*math.cos(tilt)-y*math.sin(tilt),py+x*math.sin(tilt)+y*math.cos(tilt),depth)
  ee_front([signpoint(x,y,.52) for x,y in [(-pw/2,-ph/2),(pw/2,-ph/2),(pw/2,ph/2),(-pw/2,ph/2)]],'eb oak wood')
  for text,dy,height,font,mat in [('しゃぶ辰',.07,.20,'japanese','eb iron'),('SHABU-TATSU',-.10,.073,'serif','store09 paper')]:
   obj=et_text(f,px-dy*math.sin(tilt),py+dy*math.cos(tilt),pw*.86,height,text,mat,.55,font)
   if obj:obj.matrix_world=Matrix.Rotation(tilt,4,Vector((f.nx,-f.nz,0)))@obj.matrix_world;n01_center_text(obj,f,px-dy*math.sin(tilt),py+dy*math.cos(tilt),.55)
  for j in range(4):
   yy=3.49+j*.035;f.line((px-.08,yy,.13),(px+.08,yy,.13),.009,'et red panel')
  for j in range(3):f.line((px-.07+j*.07,3.48,.13),(px-.07+j*.07,3.61,.13),.009,'et red panel')
  for yy,dep,ww in [(2.79,.34,dw*1.18),(2.86,.29,dw*1.31),(2.93,.24,dw*1.42)]:f.b(px,yy,dep,ww,.055,.32,'eb iron')
  ee_hood(f,a,b,3.65,dep=.62)
  # Uneven stone polygons keep irregular seams at the lower piers.
  for lo,hi in [(a+.05,a+w*.22-.05),(a+w*.40+.05,b-.05)]:
   f.b((lo+hi)/2,.40,.04,hi-lo,.46,.10,'eb gray stone')
   cells=max(2,round((hi-lo)/.27))
   for row in range(2):
    for j in range(cells):
     l=lo+(hi-lo)*j/cells+.018;rgt=lo+(hi-lo)*(j+1)/cells-.018;y=.19+row*.22
     pts=[(l,y+.02),(rgt-.025,y),(rgt,y+.17),(l+(rgt-l)*.42,y+.205),(l,y+.15)]
     ee_front([f.p(x,yy,.105+(j%2)*.005) for x,yy in pts],'eb cream stone' if (j+row)%3 else 'eb brown stone')
  f.b(a+w*.80,1.08,.04,w*.33,.65,.018,'eb brown stone')
  for x in [a+w*.69,a+w*.86]:eb_plant(f,x,.73,.50,.60)
  eb_plant(f,a+w*.14,.78,-.15,.30)
 elif k=='archies':
  f.b(a+w*.17,1.45,.015,w*.27,1.96,.025,'et cream panel')
  et_text(f,a+w*.17,1.90,w*.25,.065,"Archie’s Press",'eb iron',.04,'sans')
  et_text(f,a+w*.70,2.62,w*.54,.09,"Archie’s Press",'store09 paper',.04,'sans')
  p02_disc(f,a+w*.70,1.68,.31,.31,.035,'store09 paper',32)
  et_text(f,a+w*.70,1.77,.52,.10,"Archie’s",'eb iron',.05,'sans');et_text(f,a+w*.70,1.62,.45,.10,'Press','eb iron',.05,'sans')
  for j in range(3):f.b(a+w*(.40+j*.16),.91,-.07,.32,.50,.02,'eb white wood');p02_ring(f,a+w*(.40+j*.16),.94,.11,.13,-.045,'eb gray metal',.012,20)
  f.b(a+w*.18,1.70,.035,.35,.14,.018,'store09 paper');et_text(f,a+w*.18,1.70,.31,.065,'CLOSED','eb iron',.05,'sans')
  for dx in [-.16,.16]:f.b(a+w*.70+dx*w,.153,.64,w*.30,.024,1.05,'eb iron')
 elif k=='shipping':
  eb_panel(f,a,b,3.30,.78,'et maroon')
  et_text(f,a+w*.115,3.44,w*.20,.17,'United','eb gold metal',.27,'italic')
  et_text(f,a+w*.59,3.44,w*.76,.23,'SHIPPING & PACKAGING','store09 paper',.27,'condensed')
  et_text(f,c,3.13,w*.92,.12,'We Ship, We Pack, The Right Way!','eb gold metal',.27,'italic')
  ee_shutter(f,a+.03,a+w*.70,top=2.89)
  # Large black outlined shutter forms observed April 2026. Hand-authored
  # contour approximation, not photographic pixels or invented legible text.
  contours=[[(.02,.91),(.17,.94),(.25,.98),(.30,.94),(.28,.66),(.22,.47),(.26,.36),(.27,.15),(.19,.09),(.13,.17),(.15,.38),(.08,.49),(.05,.66),(.13,.72),(.19,.77),(.02,.79),(.02,.91)],[(.33,.96),(.38,.89),(.41,.75),(.46,.73),(.42,.62),(.46,.59),(.42,.47),(.39,.43),(.36,.12),(.30,.12),(.35,.52),(.30,.51),(.34,.64),(.30,.67),(.33,.96)],[(.48,.94),(.57,.94),(.64,.88),(.60,.82),(.53,.80),(.60,.74),(.54,.66),(.60,.61),(.55,.55),(.62,.48),(.63,.31),(.57,.30),(.56,.12),(.48,.10),(.50,.31),(.46,.42),(.49,.57),(.44,.63),(.48,.94)]]
  for points in contours:p02_curve(f,[(a+w*u,.38+2.18*v) for u,v in points],.26,'eb iron',.028)
  for u in [.10,.34,.57]:p02_ring(f,a+w*u,1.2,.07,.055,.27,'eb iron',.014,14)
  f.b(b-w*.14,.76,.05,w*.22,.63,.02,'et red panel')
  et_text(f,b-w*.14,.91,w*.20,.08,'UPS','store09 paper',.07,'sans');et_text(f,b-w*.14,.72,w*.20,.065,'Authorized','store09 paper',.07,'sans');et_text(f,b-w*.14,.60,w*.20,.065,'Shipping Outlet','store09 paper',.07,'sans')
  for j in range(3):p02_notice(f,b-w*.16,1.42+j*.27,w*.21,.20,.05)
 elif k=='204shutter':
  ee_shutter(f,a+.02,b-.02,top=3.0)
  # Source's orange/black abstract scroll field, with irregular olive/lilac
  # patches underneath. Shapes are authored, with fine artwork unresolved.
  shapes=[[(.01,.20),(.12,.02),(.28,.08),(.31,.36),(.21,.54),(.05,.49)],[(.32,.03),(.52,.11),(.58,.43),(.45,.62),(.29,.40)],[(.61,.08),(.80,.05),(.93,.27),(.82,.58),(.66,.46)],[(.08,.69),(.24,.49),(.43,.73),(.31,.97),(.14,.92)],[(.46,.67),(.65,.54),(.77,.78),(.64,.98),(.49,.92)],[(.81,.68),(.98,.54),(.99,.98),(.82,.97)]]
  f.quad(c,1.50,w-.06,2.60,.245,'ee red orange')
  for j,points in enumerate(shapes):ee_front([f.p(a+w*u,.20+2.60*v,.25) for u,v in points],['eb green wood','ee mauve canvas','ee red orange'][j%3])
  for j in range(5):
   x=a+w*(.10+j*.19)
   pts=[(x+w*.09*math.sin(t*math.pi*2.3+j),.32+t*2.50) for t in [q/35 for q in range(36)]]
   for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
    dx=x1-x0;dy=y1-y0;length=math.hypot(dx,dy)
    for rad,dep,mat in [(w*.029,.27,'eb iron'),(w*.020,.285,'ee red orange')]:
     ox=-dy/length*rad;oy=dx/length*rad
     ee_front([f.p(x0+ox,y0+oy,dep),f.p(x0-ox,y0-oy,dep),f.p(x1-ox,y1-oy,dep),f.p(x1+ox,y1+oy,dep)],mat)
  for j in range(7):p02_ring(f,a+w*(.08+j*.14),.55+(j%3)*.75,w*.045,.19,.33,'eb iron',.055,28)
 elif k.startswith('chase'):
  eb_panel(f,a,b,3.42,.55,'eb white stone')
  # Broad stone supports distinguish the bank openings from thin shop frames.
  pier=.065;left=a+pier;usable=w-2*pier
  for idx,(_,fraction) in enumerate(r['design']['panels']):
   if idx>0:f.b(left,1.62,.10,.38,2.90,.42,'eb white stone')
   left+=usable*fraction
  for x in [a+.13,b-.13]:f.b(x,1.62,.10,.26,2.90,.42,'eb white stone')
  f.b(c,.30,.10,w,.26,.46,'eb white stone')
  brand=a+2.0 if k=='chase-second' else b-2.0
  for dx,dy in [(-.012,0),(.012,0),(0,-.012),(0,.012)]:et_text(f,brand-.25+dx,3.43+dy,2.8,.34,'CHASE','eb blue enamel',.30,'sans')
  et_text(f,brand-.25,3.43,2.8,.34,'CHASE','store09 paper',.34,'sans')
  x=brand+1.18
  for j in range(8):
   t=j*math.pi/4;u=(j+1)*math.pi/4
   ee_front([f.p(x+math.cos(t)*.24,3.43+math.sin(t)*.24,.28),f.p(x+math.cos(u)*.24,3.43+math.sin(u)*.24,.28),f.p(x+math.cos(u)*.13,3.43+math.sin(u)*.13,.28),f.p(x+math.cos(t)*.13,3.43+math.sin(t)*.13,.28)],'eb blue enamel')
  if k=='chase-second':
   f.b(c,2.80,.44,w,.24,.60,'eb blue enamel')
   for t in [.18,.50,.84]:et_text(f,a+w*t,2.81,w*.16,.14,'CHASE','store09 paper',.76,'sans')


def et_architecture(f,r,h):
 s=r['e10Block'];n=s['number'];mat=s['trim'];bridge={**r,'e09East':s}
 if n in ['205','209','211','213','215','217','206','229','231']:
  fidelity_courses(f,min(3.78,s['upperBottom']-.12),mat,step=.47,bottom=.18,depth=.08)
 # Reuse mechanics with only this explicit observed schedule.
 if s.get('notch'):
  ee_architecture(f,{**bridge,'e09East':{**s,'cornice':'carriage'}},h)
  lo,hi=s['notch']['span']
  for a,b in [(0,lo),(hi,1)]:
   pp=f.p(a*f.L,0,0);sub=Facade(pp[0],pp[2],f.rx,f.rz,(b-a)*f.L);eb_cornice(sub,h,s)
 else:ee_architecture(f,bridge,h)
 for span in s.get('escapes',[]):ee_escape(f,{'span':span,'levels':[s['upperBottom']-.17+i*s['step'] for i in range(s['rows'])],'material':'eb iron','dropAt':span[1]-.03,'ornament':'scroll' if n.startswith('204') else 'plain'})
 for w in r['windows']:
  x=w['at']*f.L;ww=w['width']*f.L;y=w['bottom'];top=y+w['height'];row=w.get('row',-1)
  if w.get('oriel'):et_oriel(f,w,mat)
  if w.get('blindArch') or row in s.get('fanRows',[]):
   eb_arc(f,x,top+.06,ww*.60,.30,.17,.05,mat)
   for j in range(7):
    t=j*math.pi/6;f.line((x,top+.07,.15),(x+math.cos(t)*ww*.52,top+.07+math.sin(t)*.25,.15),.013,mat)
  if s.get('pairedRelief') and row>0:
   shop09_frame(f,x,y-.46,ww*.9,.33,.07,mat,.025)
   for dx in [-.22,0,.22]:ee_scroll(f,x+dx*ww,y-.46,.055,mat,.12)
  if (s.get('topPediments') and row==s['rows']-1) or row in s.get('semicircularHeads',[]):et_fan(f,x,top+.16,ww*.68,.34,mat)
  if s.get('pairedBlindHeads') and row==0 and w['col'] in [0,1,4,5]:et_fan(f,x,top+.05,ww*.63,.42,mat)
  if n in ['213','215','206'] and row<0:
   shoulder=top-ww*.5
   eb_arc(f,x,shoulder,ww/2+.11,ww/2+.11,.16,.10,mat);et_mask(f,x,top+.24,1.25,mat)
  if s.get('groundBlindHeads') and row<0:
   et_fan(f,x,top+.06,ww*.57,.48,mat)
   for j in range(7):
    t=j*math.pi/6;f.line((x+math.cos(t)*ww*.63,top+.06+math.sin(t)*.55,.15),(x+math.cos(t)*ww*.76,top+.06+math.sin(t)*.72,.15),.045,mat)
  if n in ['211','213','215','217','219','221','223','206','214','216–218','220'] and row>=0:
   if not w.get('oriel'):
    et_foliage(f,x-ww*.46,x+ww*.46,top+.15,mat,.20)
    for side in [-1,1]:
     xx=x+side*(ww/2+.10);f.b(xx,top-.03,.12,.12,.30,.24,mat)
     p02_ring(f,xx,top+.02,.045,.07,.26,mat,.015,12)
   if row>0:
    yy=y-.48;shop09_frame(f,x,yy,ww*.88,.30,.10,mat,.032);et_foliage(f,x-ww*.38,x+ww*.38,yy,mat,.15)
  if n in ['225–227','237'] and row>=0 and (n=='225–227' or w['col'] in [0,3]):
   f.b(x,y-.31,.08,ww*.64,.31,.12,'eb white wood')
   for j in range(5):f.b(x,y-.42+j*.05,.15,ww*.57,.015,.025,'eb gray metal')
  if s.get('topArches') and row==s['rows']-1:
   et_fan(f,x,top+.035,ww*.59,.37,mat,.12)
  if s.get('longPanels') and row==2:
   yy=y-.50;shop09_frame(f,x,yy,ww,.47,.10,mat,.035);et_foliage(f,x-ww*.41,x+ww*.41,yy,mat,.16)
  if s.get('groundCarving') and row<0:
   eb_arc(f,x,top+.08,ww*.62,.25,.21,.07,mat);et_mask(f,x,top+.30,.8,mat)
   for side in [-1,1]:
    xx=x+side*(ww/2+.13);f.b(xx,y+w['height']/2,.13,.13,w['height'],.26,mat);p02_ring(f,xx,top-.12,.09,.08,.30,mat,.022,16)
  if n=='212' and row>=0:f.b(x,y-.27,.07,ww+.16,.38,.09,'eb gray stone')
 if s.get('quoins'):
  for x in [.12,f.L-.12]:
   for j in range(round((h-3.7)/.40)):f.b(x,3.8+j*.40,.06,.32 if j%2 else .42,.37,.10,'eb cream stone')
 if s.get('arcadeCornice'):
  for j in range(round(f.L/.55)):eb_arc(f,(j+.5)*f.L/round(f.L/.55),h-.70,.23,.24,.35,.055,mat)
 if n=='201':
  # Three masonry piers with paired tall recessed strips, from the April 2026
  # full elevation. Raised perimeter brick leaves the lower wall exposed.
  for at in [.125,.385,.79]:
   x=at*f.L
   for lo,hi in [(3.88,6.30),(6.72,13.95),(14.33,h-.72)]:
    for dx in [-.34,0,.34]:f.b(x+dx,(lo+hi)/2,.095,.105,hi-lo,.19,'eb red brick')
    for yy in [lo,hi]:f.b(x,yy,.095,.79,.12,.19,'eb red brick')
  for yy in [3.74,6.50,14.13,h-.60]:fidelity_clipped_surface(f,0,f.L,yy,yy+.095,.075,.12,mat)
  for j in range(round(f.L/.19)):
   x=(j+.5)*f.L/round(f.L/.19)
   fidelity_clipped_surface(f,x-.035,x+.035,5.85,6.00,.09,.16,'eb red brick')
 if n in ['211','213','215','217','219','221','223','206','214','216–218','220']:
  for row in range(s['rows']):
   yy=s['upperBottom']+row*s['step']-.73
   fidelity_clipped_surface(f,0,f.L,yy,yy+.09,.08,.09,mat)
  f.strip(3.82,.15,.24,mat)
  for j in range(round(f.L/.20)):f.b((j+.5)*f.L/round(f.L/.20),3.70,.13,.075,.13,.27,mat)
 if s.get('pediment')=='round':
  f.b(f.L*.5,h+.12,.12,f.L*.4,.30,.22,mat);et_fan(f,f.L*.5,h+.25,f.L*.21,.57,mat,.24)
 for d in r['doors']:
  x=d['at']*f.L;ww=d['width']*f.L;low=d['bottom'];top=d['top'];style=s.get('portal')
  if style:
   shoulder=top-ww*.5 if style=='round' else top
   for side in [-1,1]:
    xx=x+side*(ww/2+.16);f.b(xx,(low+shoulder)/2,.13,.23,shoulder-low,.30,mat)
    f.b(xx,shoulder-.12,.18,.36,.24,.43,mat)
    if style=='corbels':
     f.b(xx,shoulder-.08,.25,.34,.55,.48,mat)
     p02_disc(f,xx,shoulder+.02,.11,.12,.51,mat,18);et_mask(f,xx,shoulder-.40,1.3,mat)
     et_foliage(f,xx-.1,xx+.1,(low+shoulder)/2,mat,.30)
   if style=='round':
    eb_arc(f,x,shoulder,ww/2+.27,ww/2+.27,.19,.16,mat)
    for j in range(9):
     t=j*math.pi/8;et_mask(f,x+math.cos(t)*(ww/2+.27),shoulder+math.sin(t)*(ww/2+.27),.38,mat)
   else:f.b(x,top+.12,.18,ww+.72,.22,.40,mat)
  if n=='205' or n in ['208','210','222','237']:
   for side in [-1,1]:eb_lamp(f,x+side*(ww/2+.30),top-.25,.33)
  if n=='201':
   f.b(x,top+.68,.10,ww+.9,.82,.19,mat);shop09_frame(f,x,top+.68,ww+.82,.74,.21,mat,.07);et_text(f,x-ww*.64,2.07,.35,.18,'201','eb gold metal',.31,'serif')
   for side in [-1,1]:eb_lamp(f,x+side*(ww/2+.19),top-ww*.5+.12,.42)
  if s.get('entryNumber')=='arch-and-plaques':
   et_text(f,x,top-.09,.70,.18,'221','eb iron',.28,'serif')
   for side in [-1,1]:f.b(x+side*(ww/2+.35),1.95,.23,.25,.17,.06,'eb gold metal');et_text(f,x+side*(ww/2+.35),1.95,.21,.10,'221','eb iron',.27,'serif')
  if s.get('entryNumber')=='left-door-pane':et_text(f,x-ww*.25,2.12,.30,.065,n,'store09 paper',-.18,'sans')
  if s.get('cheeks'):
   entry=s['access'];dep=entry['depth']
   for side in [-1,1]:
    xx=x+side*(entry['width']/2+.08)
    for j in range(8):
     t=(j+.5)/8;yy=low*(1-t)+.23;f.b(xx,yy/2+.12,dep*t,.19,yy+.24,dep/8+.015,mat)
  if n=='220':
   for j in range(9):
    t=j*math.pi/8;f.line((x,top-.55,-.14),(x+math.cos(t)*ww*.45,top-.55+math.sin(t)*.51,-.14),.012,'eb iron')
 for span in s.get('closedHatches',[]):et_closed_box(f,span[0]*f.L,span[1]*f.L,int(n))
 if n in ['209','213','215','217','206']:
  for a,b in [(f.L*.02,f.L*.33),(f.L*.67,f.L*.98)]:
   for y in [.39,1.02]:f.line((a,y,1.05),(b,y,1.05),.018,'eb iron')
   for j in range(max(2,round((b-a)/.18))):
    xx=a+(j+.5)*(b-a)/max(2,round((b-a)/.18));f.line((xx,.22,1.05),(xx,1.12,1.05),.010,'eb iron')
    if n in ['209','217']:ee_scroll(f,xx,.75,.065,'eb iron',1.05)
 if n=='221':
  for well in r['observedGround']['basementAreaways']:
   a=(well['at']-well['width']/2)*f.L;b=(well['at']+well['width']/2)*f.L
   for j in range(5):f.b((a+b)/2,.12-(j+1)*.144,1.05-(j+.5)*.19,b-a,.10,.19,'eb gray stone')
 if s.get('uprightGuards'):
  for a,b in [(0,f.L*.33),(f.L*.67,f.L)]:nb_grille(f,a+.06,b-.06,.16,.93,.77)
 if s.get('heartRails'):
  for a,b in [(f.L*.02,f.L*.34),(f.L*.66,f.L*.98)]:
   for j in range(6):ee_scroll(f,a+(j+.5)*(b-a)/6,1.1,.11,'eb white wood',.37)
   f.b((a+b)/2,.29,.75,b-a,.28,.32,'eb iron')
   for j in range(9):ee_ball(f,a+(j+.5)*(b-a)/9,.60,.75,.18,'store09 bottle green')
 if s.get('stonePatchwork'):
  for row in range(5):
   for j in range(12):
    xx=(j+.5)*f.L/12;yy=.4+row*.53
    fidelity_clipped_surface(f,xx-f.L/24+.015,xx+f.L/24-.015,yy-.25,yy+.25,.045,.06,['eb gray stone','eb brown stone','eb buff stone'][(j*3+row*7)%3])
 if n=='212':
  ee_escape(f,{'span':[.62,.99],'levels':[s['upperBottom']+i*s['step']-.17 for i in s['balconyRows']],'material':'eb iron','balconyOnly':True,'ornament':'plain','dropAt':.96})
 if n=='228':et_hatch(f,f.L*.515,f.L*.685,True,1.3)
 if n=='233–235':p03_tags(f,.08,f.L-.08,.28,.75,.09,233)
 if n=='226':
  for x in [.16*f.L,.47*f.L]:eb_plant(f,x,3.0,.25,.35)
 if n=='224':p03_tags(f,f.L*.64,f.L-.08,.28,.7,.10,224)

_et_previous_render=render_building
def render_building(b):
 if b['id'] not in E10_BLOCK_IDS:return _et_previous_render(b)
 owner(str(b['id'])+' Tenth individually observed');h=b['firstStmarksHeight'];b['renderHeight']=h
 records=[(int(i),r) for i,r in b['firstStmarksArchitecture'].items() if r.get('e10Block')]
 mass=deepcopy(b)
 if b['id']==247852693:
  # Preserve mapped outline except the photographically visible upper recess.
  p=[]
  for x,z in b['p']:
   p.append([x,z])
   if abs(x+197.644)<.02 and z<10:p.extend([[-197.644,16.67],[-193.779,16.67]])
  mass['p']=p
 wall_mass(mass,records[0][1]['wall'],False)
 for idx,r in records:
  v=b['frontages'][idx];f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']);f.wall=r['wall'];s=r['e10Block']
  clean=deepcopy(r);clean['observedGround']['basementAreaways']=[];clean['windows']=[w for w in clean['windows'] if not w.get('oriel')]
  fidelity_elevation({**b,'businesses':[],'seventhArchitecture':clean},f,clean)
  if paint:=s.get('groundPaint'):shop09_face(f,{'paintSurround':{'bottom':.17,'top':min(3.65,s['upperBottom']-.16),'material':'eb '+paint}})
  if cut:=s.get('notch'):
   a,bb=[x*f.L for x in cut['span']];OPENINGS[frontage_key(f)].append((a,cut['bottom'],bb,h+.5))
   ee_front([f.p(a,cut['bottom'],0),f.p(bb,cut['bottom'],0),f.p(bb,cut['bottom'],-cut['depth']),f.p(a,cut['bottom'],-cut['depth'])],'roof')
  et_architecture(f,r,h)
  if b['id']==247852693:et_scaffold(f,h)
