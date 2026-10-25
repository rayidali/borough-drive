"""Eleventh Second–First: 22 isolated owners, observed architecture and shops.

Dimensions not supplied by municipal footprints are visual estimates. All artwork
and lettering are authored geometry; private source imagery is never a texture.
"""
E11_BLOCK_IDS={247851916,247851917,247851918,247851919,247851921,247851922,247851923,247851924,247851925,247851926,247851927,247851928,247851929,247851930,247851931,247851932,247851933,247851934,247851936,247851937,247851941,247851942}
for name,rgb in {'tan brick':(.58,.48,.35),'bluegray paint':(.30,.36,.40),'pale stone':(.76,.77,.71),'school brick':(.66,.62,.49),'pale yellow brick':(.72,.69,.53),'burgundy wood':(.27,.08,.09),'turquoise canvas':(.25,.48,.49),'rose paint':(.63,.27,.38),'mural blue':(.13,.40,.56),'mural violet':(.38,.30,.49),'mural skin':(.63,.49,.38),'mural cream':(.76,.73,.62),'bronze paint':(.39,.31,.20)}.items():
 material('el '+name,rgb,.89)
 if 'wood' in name:MATS['el '+name]['storefront09Surface']=2
 if 'canvas' in name:MATS['el '+name]['storefront09Surface']=5

def el_offset(f,d):
 p=f.p(0,0,d);g=Facade(p[0],p[2],f.rx,f.rz,f.L);g.wall=getattr(f,'wall','eb red brick');return g

def el_skin(f,a,b,lo,hi,mat,depth=0):
 if hi>lo:fidelity_clipped_surface(f,a,b,lo,hi,depth,.025,mat)

def el_grille(f,a,b,lo=.20,hi=2.85,d=.12,mat='eb silver metal',perforated=False):
 if not perforated:
  for j in range(max(2,round((b-a)/.14))+1):
   xx=a+(b-a)*j/max(2,round((b-a)/.14));f.line((xx,lo,d),(xx,hi,d),.008,mat)
 for j in range(max(2,round((hi-lo)/.10))+1):
  yy=lo+(hi-lo)*j/max(2,round((hi-lo)/.10));f.line((a,yy,d),(b,yy,d),.012,mat)
 if perforated:
  for row in range(max(2,round((hi-lo)/.12))):
   yy=lo+(row+.5)*(hi-lo)/max(2,round((hi-lo)/.12))
   for col in range(max(2,round((b-a)/.20))):
    xx=a+(col+.5)*(b-a)/max(2,round((b-a)/.20));f.b(xx,yy,d,.035,.11,.035,mat)

def el_letters(f,a,b,y,h,text,colors,font='sans',d=.29):
 n=max(1,len(text));unit=(b-a)/n
 for i,ch in enumerate(text):
  if ch!=' ':et_text(f,a+(i+.5)*unit,y,unit*.96,h,ch,colors[i%len(colors)],d,font)

# Isolated finishes: modern limestone/paint must not inherit the mottled older
# stone shader. The source colors are daylight estimates, not colorimetry.
for name,rgb in {'smooth limestone':(.70,.72,.69),'ivory paint':(.78,.75,.64),'cobalt enamel':(.025,.07,.48),'leaf dark':(.07,.17,.055),'leaf light':(.16,.29,.07),'skin shadow':(.43,.29,.24),'skin light':(.74,.60,.46),'skin mid':(.62,.46,.34),'portrait hair':(.22,.22,.20),'lace shadow':(.48,.52,.49)}.items():
 material('el '+name,rgb,.87)
 MATS['el '+name]['storefront09Surface']=0

def el_leaf(f,x,y,d,w,h,angle=0,mat='el leaf dark'):
 # Tapered, folded blade, with its own midrib and a slight depth ridge.
 ca,sa=math.cos(angle),math.sin(angle)
 def p(u,v,dd=0):return f.p(x+u*ca-v*sa,y+u*sa+v*ca,d+dd)
 pts=[p(0,-h*.5),p(-w*.42,-h*.17),p(-w*.5,h*.15),p(0,h*.5),p(w*.45,h*.12),p(w*.35,-h*.22)]
 mid=p(0,0,.035)
 for j in range(6):ee_front([pts[j],pts[(j+1)%6],mid],mat if j%2 else 'el leaf light')
 f.line((x+sa*h*.5,y-ca*h*.5,d),(x-sa*h*.5,y+ca*h*.5,d+.037),.006,'el leaf light')

def el_shrub(f,x,y,d,size=.55):
 for j in range(25):
  ang=j*2.399;rr=size*math.sqrt((j+.5)/25)*.52;xx=x+math.cos(ang)*rr;yy=y+size*.5+math.sin(ang)*rr*.65
  el_leaf(f,xx,yy,d+math.cos(j)*.14,.12,.20,j*.7)

def el_bloom(f,x,y,d,size,mat):
 for ring in [1.,.57]:
  for j in range(7):
   ang=j*math.tau/7+ring;dx=math.cos(ang)*size*.38*ring;dy=math.sin(ang)*size*.38*ring
   p02_disc(f,x+dx,y+dy,size*.28*ring,size*.18*ring,d+(1-ring)*.035,mat,10)
 p02_disc(f,x,y,size*.09,size*.09,d+.04,'eb yellow wood',10)

def el_big_tags(f,a,b,lo=.55,hi=2.1,d=.17,variant=0,mat='eb iron'):
 # Independent contours for each observed shutter; illegible text is not
 # transcribed. These are thin surface strokes, not repeated raised coils.
 w=b-a;hh=hi-lo
 def stroke(points,color=mat,r=.018):p02_curve(f,[(a+u*w,lo+v*hh) for u,v in points],d,color,min(r,hh*.04))
 if variant==0:
  for pts in [[(.08,.33),(.16,.46),(.27,.40),(.23,.22),(.10,.16),(.07,.28),(.16,.36),(.25,.16),(.36,.19),(.40,.31)],[(.43,.41),(.57,.23),(.62,.12),(.74,.34),(.90,.20),(.83,.40),(.70,.45),(.67,.34),(.90,.20)],[(.10,.57),(.31,.68),(.20,.77),(.14,.53),(.33,.58),(.09,.65)]]:stroke(pts)
  stroke([(.56,.78),(.73,.56),(.77,.55),(.81,.76),(.97,.82),(.77,.55),(.70,.80),(.56,.78)],'eb purple enamel',.015)
 elif variant==1:
  # Four unequal connected lobes and their separate internal cuts (338).
  pts=[(.02,.68),(.11,.72),(.17,.95),(.24,.96),(.28,.78),(.35,.96),(.43,.95),(.46,.78),(.54,.96),(.63,.95),(.65,.80),(.72,.85),(.81,.84),(.84,.77),(.98,.80),(.92,.60),(.98,.52),(.96,.21),(.90,.11),(.77,.08),(.69,.13),(.58,.08),(.48,.10),(.42,.18),(.34,.10),(.22,.09),(.17,.17),(.09,.16),(.03,.25),(.07,.35),(.13,.37),(.10,.56),(.02,.68)]
  stroke(pts,r=.028)
  for pts in [[(.20,.70),(.26,.57),(.28,.29),(.23,.17)],[(.33,.69),(.38,.52),(.40,.23),(.35,.13)],[(.47,.73),(.52,.57),(.50,.28),(.46,.16)],[(.62,.62),(.69,.51),(.72,.27),(.68,.15)],[(.85,.59),(.89,.48),(.91,.35)]]:stroke(pts,r=.025)
  stroke([(.68,.74),(.69,.67),(.73,.66),(.74,.73),(.78,.72),(.80,.66)],r=.013)
 elif variant==2:
  #299: silver-filled left bubbles and angular right forms, red outer edge.
  shapes=[[(.02,.36),(.05,.63),(.13,.69),(.12,.92),(.19,.99),(.26,.94),(.27,.72),(.35,.87),(.40,.83),(.39,.57),(.44,.28),(.38,.17),(.26,.17),(.21,.25),(.13,.14),(.04,.19),(.02,.36)],[(.44,.22),(.49,.91),(.61,.96),(.64,.25),(.58,.25),(.56,.45),(.52,.44),(.50,.23),(.44,.22)],[(.65,.24),(.65,.95),(.72,.98),(.72,.54),(.79,.61),(.81,.27),(.75,.17),(.65,.24)],[(.80,.71),(.84,.99),(.94,.94),(.91,.77),(.99,.73),(.97,.55),(.93,.53),(.96,.28),(.89,.19),(.83,.31),(.82,.50)]]
  for pts in shapes:
   stroke(pts,'eb red metal',.045)
   ee_front([f.p(a+u*w,lo+v*hh,d+.003) for u,v in pts],'eb silver metal')
   p02_curve(f,[(a+u*w,lo+v*hh) for u,v in pts],d+.009,'eb iron',.013)
  for x,y in [(.55,.71),(.87,.76),(.90,.43)]:p02_disc(f,a+x*w,lo+y*hh,.035,.055,d+.014,'eb iron',12)
 elif variant==3:
  # White outlines on the broad corner shutter, irregular individual marks.
  for pts in [[(.07,.17),(.05,.44),(.09,.76),(.14,.81),(.19,.68),(.17,.22),(.13,.13),(.07,.17)],[(.21,.15),(.22,.82),(.28,.91),(.31,.78),(.29,.38),(.24,.35),(.23,.58),(.33,.72),(.37,.61),(.35,.22),(.30,.15),(.21,.15)],[(.43,.81),(.49,.91),(.54,.71),(.52,.23),(.46,.12),(.40,.26),(.41,.65),(.49,.76)],[(.62,.19),(.61,.69),(.67,.88),(.75,.82),(.79,.57),(.78,.22),(.72,.12),(.62,.19)],[(.83,.18),(.87,.71),(.93,.80),(.98,.64),(.96,.22),(.91,.13),(.83,.18)]]:stroke(pts,r=.019)
 else:
  for pts in [[(.02,.17),(.10,.76),(.22,.83),(.15,.51),(.29,.18),(.38,.29)],[(.40,.13),(.47,.91),(.60,.69),(.51,.48),(.68,.21)],[(.71,.25),(.82,.81),(.95,.78),(.87,.44),(.98,.20)]]:stroke(pts,r=.004)

def el_valance(f,a,b,y,drop,dep,text,h=.14,font='serif',mat='store09 paper'):
 et_text(f,(a+b)/2,y-drop-.11,(b-a)*.86,h,text,mat,dep+.138,font)

def el_outline_text(f,x,y,w,h,text,front='eb red metal',d=.12,font='italic'):
 for dx,dy in [(-.009,0),(.009,0),(0,-.009),(0,.009)]:et_text(f,x+dx,y+dy,w,h,text,'store09 paper',d,font)
 et_text(f,x,y,w,h,text,front,d+.006,font)

def el_pendant(f,x,y=2.4,d=-.65):
 f.line((x,2.85,d),(x,y+.12,d),.007,'eb iron');ee_ball(f,x,y,d,.075,'store09 paper')

def el_pastries(f,a,b):
 for row,y in enumerate([.83,1.18,1.53]):
  f.b((a+b)/2,y,-.58,b-a,.045,.35,'eb oak wood')
  for j in range(max(2,round((b-a)/.22))):
   xx=a+(j+.5)*(b-a)/max(2,round((b-a)/.22));f.b(xx,y+.035,-.52,.19,.025,.23,'store09 paper')
   if (j+row)%3==0:
    f.b(xx,y+.10,-.50,.15,.12,.16,'eb brown stone');f.b(xx,y+.17,-.50,.15,.025,.16,'store09 paper')
   elif (j+row)%3==1:
    for q in [-.05,.05]:ee_ball(f,xx+q,y+.10,-.50,.05,'eb yellow wood');ee_ball(f,xx+q,y+.145,-.50,.018,'eb red metal')
   else:
    rod(f.p(xx,y+.02,-.50),f.p(xx,y+.14,-.50),.075,'el rose paint',12);p02_ring(f,xx,y+.09,.06,.04,-.41,'store09 paper',.008,12)

def el_neon_veniero(f,x):
 # Two-sided perpendicular neon blade; separate side date box and curved foot.
 for flip in [False,True]:
  pp=f.p(x+(.045 if flip else -.045),0,1.65 if flip else .15)
  ff=Facade(pp[0],pp[2],(-1 if flip else 1)*f.nx,(-1 if flip else 1)*f.nz,1.50)
  ff.b(1.12,5.56,0,.62,4.38,.07,'eb brown metal');ff.b(1.12,5.56,.045,.48,4.22,.02,'eb blue metal')
  for j,ch in enumerate('VENIERO'):
   yy=7.37-j*.53;el_outline_text(ff,1.12,yy,.43,.40,ch,'eb red metal' if j in [0,3] else 'eb yellow wood',.068,'sans')
  ff.b(.58,5.86,0,.39,2.28,.09,'eb brown metal');ff.b(.58,5.86,.06,.31,2.16,.02,'eb blue metal')
  et_text(ff,.58,6.80,.28,.09,'SINCE','store09 paper',.08,'sans')
  for j,ch in enumerate('1894'):et_text(ff,.58,6.46-j*.42,.25,.35,ch,'store09 paper',.08,'italic')
  pts=[ff.p(0,3.2,0),ff.p(1.42,3.2,0),ff.p(1.43,3.8,0),ff.p(1.23,4.0,0),ff.p(1.1,3.72,0),ff.p(0,3.72,0)];ee_front(pts,'eb brown metal')
  et_text(ff,.71,3.47,1.34,.23,'PASTICCERIA','eb green wood',.06,'condensed')
  for yy in [3.26,3.74]:ff.line((.02,yy,.06),(1.39,yy,.06),.015,'eb gold metal')
 for yy in [3.5,7.5]:f.line((x,yy,.03),(x,yy,1.65),.035,'eb brown metal')

def el_skyline(f,a,b,lo=.20,hi=2.78):
 f.b((a+b)/2,(lo+hi)/2,.06,b-a,hi-lo,.025,'el mural blue')
 # Individually constructed city silhouettes/windows, approximating observed cover.
 hs=[.44,.66,.56,.92,.38,.61,.77,.48,.57];w=(b-a)/len(hs)
 for j,hh in enumerate(hs):
  xx=a+(j+.5)*w;top=lo+.45+hh*(hi-lo)*.70
  f.b(xx,(lo+top)/2,.082,w*.87,top-lo,.022,['eb blue metal','eb iron','el mural violet'][j%3])
  for row in range(2,round((top-lo)/.15)):
   for side in [-1,1]:f.b(xx+side*w*.20,lo+row*.15,.097,w*.13,.045,.012,'store09 paper')
 for yy in [lo+.24,lo+.32]:f.line((a,yy,.105),(b,yy,.105),.012,'eb yellow wood')

_el_previous_shop=photographed_shop
def photographed_shop(f,a,b,r):
 detail=r['design'].get('detailE11Block')
 if not detail:return _el_previous_shop(f,a,b,r)
 _el_previous_shop(f,a,b,r)
 k=detail['kind'];w=b-a;c=(a+b)/2;d=r['design'];mat=d['detail09']['frame'];low=d['base'];top=d['head']
 f.b(c,(low+top)/2,-1.07,w,top-low,.06,'recess shadow')
 for xx in [a+.02,b-.02]:f.b(xx,(low+top)/2,-.52,.04,top-low,1.1,mat)
 for yy in [low,top]:f.b(c,yy,-.52,w,.04,1.1,mat)
 if k=='clinic':
  eb_panel(f,a,b,3.25,.40,'eb iron');f.b(a+w*.34,3.27,.25,w*.25,.33,.03,'eb white wood')
  for yy,line in [(3.35,'EAST VILLAGE'),(3.20,'ANIMAL CLINIC')]:et_text(f,a+w*.34,yy,w*.23,.11,line,'eb iron',.28,'condensed')
  f.b(a+w*.25,1.73,-.28,w*.46,1.94,.025,'te cyan board')
  # Authored cat/dog poster silhouettes, matching the observed two-animal layout.
  ee_animal(f,a+w*.35,2.07,w*.17,.49,'eb yellow wood',-.23)
  ee_animal(f,a+w*.27,1.45,w*.12,.36,'store09 paper',-.22,cat=True)
  for yy,line in [(2.38,'The Best Veterinary Care'),(2.24,'for Your Best Friend')]:et_text(f,a+w*.17,yy,w*.24,.066,line,'eb iron',-.21,'serif')
  for yy,line in [(1.06,'EAST VILLAGE'),(.94,'ANIMAL CLINIC')]:et_text(f,a+w*.17,yy,w*.23,.078,line,'eb iron',-.21,'sans')
  for xx,yy,ww,hh,ma in [(a+w*.35,1.62,w*.13,.63,'eb yellow wood'),(a+w*.27,1.20,w*.085,.29,'store09 paper')]:
   p02_disc(f,xx,yy,ww*.44,hh*.48,-.235,ma,20)
   for side in [-1,1]:f.b(xx+side*ww*.28,yy-hh*.35,-.225,ww*.19,hh*.35,.014,ma)
  f.b(a+w*.64,2.74,.11,w*.20,.20,.12,'eb iron');p02_disc(f,a+w*.64,2.74,.13,.06,.18,'store09 paper',20);et_text(f,a+w*.64,2.74,.19,.07,'318','eb iron',.19,'serif')
  eb_blade(f,b-.12,3.13,'ANIMAL\nCLINIC','eb white wood',False,'eb iron')
  f.b(a+w*.25,.48,.07,w*.49,.56,.06,'eb red brick')
  for xx in [a+.15,b-.15]:f.b(xx,2.93,.15,.22,.055,.15,'store09 paper')
  for xx in [a+w*.63,a+w*.84]:p02_notice(f,xx,1.75,.24,.35,.07)
 elif k=='bowprint':
  ee_curved(f,a,b,'el burgundy wood','Bowprint Vintage','script',y=3.50,drop=.58,dep=.90,scallop=True)
  et_text(f,c,2.84,w*.66,.075,'MOST EXCELLENT THREADS','store09 paper',1.04,'condensed')
  et_text(f,b-.20,2.84,.25,.09,'320','store09 paper',1.04,'serif')
  et_text(f,a+.20,2.84,.25,.09,'320','store09 paper',1.04,'serif')
  el_grille(f,a+w*.35,b,.84,2.78);ee_shutter(f,a,a+w*.30,.75,2.70,'eb gray metal')
  eb_clothes(f,a+w*.40,b-.10,2.20)
  for j in range(3):f.b(a+w*.16,.17+(j+1)*.18/2,.30+(2-j)*.25,w*.33,.18,.25,'eb charcoal stone')
 elif k in ['322west','328closed','328paper']:
  if k=='322west':f.b(c,3.22,.23,w,.46,.46,'eb black canvas');te_grid_glass(f,a+w*.72,.20,2.50,w*.29,.02,3,5,'eb white wood')
  else:
   et_canopy(f,a,b,'el turquoise canvas' if k=='328paper' else 'eb black canvas',y=3.47,drop=.64,dep=.85)
   et_text(f,b-.18,2.72,.30,.08,'328','store09 paper',.99,'sans')
  el_grille(f,a,b)
  if k=='328paper':
   for row in range(5):
    for col in range(6):
     xx=a+(col+.5)*w/6;yy=.55+row*.38;f.b(xx,yy,-.28,w/7,.29,.025,['eb yellow enamel','eb cyan enamel','eb red wood','store09 paper'][((row*7+col)%4)])
  else:
   te_curtain(f,a+.08,b-.08,mat='eb pale fabric',d=-.70)
   if k=='328closed':el_big_tags(f,a+w*.35,b-.12,.22,.33,.30,4,'eb gray metal')
 elif k=='stamps':
  eb_panel(f,a,b,3.24,.46,'eb yellow enamel');et_text(f,c,3.23,w*.76,.14,'RUBBER STAMPS','eb iron',.28,'serif')
  for j in range(11):
   xx=a+(j+.5)*w/11;yy=3.42 if j%2 else 3.06;ma=['eb blue enamel','eb green wood','el rose paint'][j%3]
   if j%3==0:el_bloom(f,xx,yy,.28,.065,ma)
   elif j%3==1:
    f.b(xx,yy,.28,.052,.055,.01,ma);p02_curve(f,[(xx-.04,yy+.025),(xx,yy+.065),(xx+.04,yy+.025)],.29,ma,.006)
   else:shop09_frame(f,xx,yy,.075,.060,.28,ma,.008)
  el_grille(f,a,b)
  for row in range(4):
   f.b(c,.62+row*.42,-.55,w*.9,.04,.24,'eb oak wood')
   for j in range(9):f.b(a+(j+.5)*w/9,.72+row*.42,-.52,.13,.15,.12,'eb brown stone');f.b(a+(j+.5)*w/9,.84+row*.42,-.52,.07,.06,.07,'eb iron')
 elif k=='salon':
  ee_hood(f,a,b,3.02,'eb gray metal');f.b(a+w*.34,1.10,.05,w*.64,.67,.025,'el bluegray paint');et_text(f,a+w*.33,1.22,w*.53,.075,'TECHNI SALON','store09 paper',.075,'serif');et_text(f,a+w*.33,1.05,w*.43,.045,'SINCE 2014','store09 paper',.075,'sans')
  nb_ac(f,b-w*.15,2.67,.58,.31,.17);et_hatch(f,a+.10,a+w*.55,True)
  for xx in [a+w*.20,a+w*.45]:p02_ring(f,xx,1.94,.19,.32,-.75,'eb silver metal',.025);ee_chair(f,xx,-.57,'eb iron')
  eb_board(f,a+.02,.17,'TECHNI|SALON','eb oak wood',1.35);p02_notice(f,b-w*.14,1.95,.22,.29,.08)
 elif k=='shake':
  eb_panel(f,a,b,3.23,.46,'el cobalt enamel');et_text(f,c,3.18,w*.60,.13,'Shake & Tail','store09 paper',.28,'sans')
  # Side-profile orange dog mark: long body, raised tail, neck and muzzle.
  pts=[(-.19,0),(-.23,.09),(-.18,.12),(-.12,.04),(.08,.04),(.11,.16),(.18,.16),(.23,.11),(.18,.08),(.14,.08),(.13,-.05),(-.11,-.05),(-.14,-.10),(-.18,-.10)]
  ee_front([f.p(c+x,3.36+y,.29) for x,y in pts],'te orange board')
  for yy,line in [(3.04,'www.shakeandtailnyc.com'),(2.98,'646.797.7152')]:et_text(f,c,yy,w*.60,.045,line,'store09 paper',.28,'sans')
  for xx in [a+.24,b-.24]:f.b(xx,.33,.70,.29,.33,.29,'te orange board');el_shrub(f,xx,.50,.70,.36)
  for xx in [a+.04,b-.04]:f.b(xx,1.55,.13,.10,2.72,.07,'el cobalt enamel')
  f.b(a+w*.69,.76,-.40,w*.48,.18,.20,'el cobalt enamel')
  et_text(f,a+w*.70,2.42,w*.40,.13,'Shake & Tail','eb gold metal',.09,'italic');et_text(f,a+w*.70,2.23,w*.42,.08,'646.797.7152','eb gold metal',.09,'sans')
  for xx in [a+w*.50,a+w*.68,a+w*.83]:p02_notice(f,xx,1.40,.18,.23,.09)
 elif k=='buffalo':
  eb_panel(f,a,b,3.27,.55,'eb iron');el_letters(f,a+.10,a+w*.55,3.34,.37,'Buffalo',['te orange board','eb yellow wood','eb red metal','eb cyan enamel','eb green wood','eb purple enamel','el rose paint'],'script')
  f.b(a+w*.78,3.36,.265,w*.37,.23,.025,'store09 paper');et_text(f,a+w*.78,3.36,w*.35,.16,'E X C H A N G E','eb iron',.29,'condensed');et_text(f,a+w*.77,3.09,w*.40,.10,'New & Recycled Fashion','store09 paper',.28,'serif')
  eb_blade(f,a+w*.10,4.15,'Buffalo\nEXCHANGE','te orange board',False,'store09 paper')
  eb_clothes(f,a+.15,b-.15,2.38)
  for xx in [a+w*.12,a+w*.66,a+w*.88]:
   rod(f.p(xx,.70,-.60),f.p(xx,1.66,-.60),.08,'eb pale fabric',12);ee_ball(f,xx,1.83,-.60,.12,'eb pale fabric');f.b(xx,1.33,-.55,.40,.55,.15,['eb yellow wood','eb blue metal','el rose paint'][int(xx*10)%3])
   shop09_frame(f,xx,.34,.28,.20,.17,'eb iron',.02)
  for xx in [a+w*.14,a+w*.74]:el_pendant(f,xx)
  for xx in [a+w*.13,a+w*.56,a+w*.85]:et_text(f,xx,.78,w*.22,.075,'Buy. Sell. Trade.','store09 paper',.10,'serif')
  for yy in [1.25,1.65,2.05]:p02_notice(f,a+w*.38,yy,.23,.28,.11)
  for xx in [a+w*.14,a+w*.74]:
   for j in range(8):f.b(xx+(j-3.5)*.032,.33,.19,.012,.17,.025,'eb iron')
 elif k=='334plants':
  ee_hood(f,a,b,3.03,'eb white wood');nb_ac(f,b-w*.16,2.60,.55,.30,.14)
  for xx in [a+w*.17,a+w*.42,a+w*.65]:
   el_pendant(f,xx);eb_plant(f,xx,.35,-.58,.40)
   for j in range(5):
    yy=1.1+j*.22;dx=math.sin(j*1.8)*.25;f.line((xx,.60,-.54),(xx+dx,yy,-.47),.015,'el leaf dark');el_leaf(f,xx+dx,yy,-.45,.24,.70,math.sin(j)*.50)
  for j in range(7):f.b(a+w*(.08+j*.09),.80,-.30,.18,.28,.035,['store09 paper','eb blue enamel','el rose paint'][j%3])
 elif k in ['334closed','338closed','299closed']:
  ee_shutter(f,a,b,.19,2.85,'eb silver metal' if k!='299closed' else 'eb iron');el_grille(f,a,b,2.15,2.83,.13,perforated=True)
  el_big_tags(f,a+.03,b-.03,.55,2.15,.17,0 if k=='334closed' else 1 if k=='338closed' else 2,'eb gray metal' if k=='299closed' else 'eb iron')
  if k=='338closed':f.b(c,.40,.13,w,.20,.025,'el rose paint')
  if k=='334closed':
   eb_panel(f,a,b,3.20,.48,'eb white stone')
   for xx in [a+.1,c,b-.1]:eb_lamp(f,xx,3.42,.42,'eb white wood')
  if k=='299closed':
   for j in range(5):
    xx=a+(j+.5)*w/5;nb_ac(f,xx,3.25,.70,.45,.35)
    for off in [-.25,.25]:f.line((xx+off,2.88,.03),(xx+off,3.05,.55),.022,'eb iron')
   for j in range(5):
    xx=a+w*(.18+j*.12);dd=.70;ma='eb blue metal' if j==4 else 'eb silver metal'
    rod(f.p(xx,.18,dd),f.p(xx,.91,dd),.23,ma,20)
    rod(f.p(xx,.90,dd),f.p(xx,.96,dd),.25,ma,20)
    for q in range(16):
     ang=q*math.tau/16;f.line((xx+math.cos(ang)*.231,.25,dd+math.sin(ang)*.231),(xx+math.cos(ang)*.231,.85,dd+math.sin(ang)*.231),.008,ma)
    f.line((xx-.07,.985,dd),(xx+.07,.985,dd),.012,'eb iron')
 elif k=='flowers':
  for side in [a+.05,b-.05]:
   for phase in [0,.3]:p02_curve(f,[(side+math.sin(j*.9+phase)*.12,.35+j*.18) for j in range(17)],.20,'eb brown stone',.028)
  for j in range(44):
   xx=a+(j+.5)*w/44;yy=3.0+math.sin(j*.7)*.16;el_leaf(f,xx,yy,.24,.16,.25,j*.7)
   if j%3==0:el_bloom(f,xx,yy+.05,.35,.20,'eb red metal')
  for xx in [a+.04,b-.04]:
   for j in range(12):el_leaf(f,xx+math.sin(j)*.10,.65+j*.18,.25,.16,.23,j*.6)
  for row in range(3):
   for j in range(5):
    xx=a+(j+.5)*w/6;yy=.45+row*.55;f.b(xx,yy,-.50,.12,.25,.12,['store09 paper','eb silver metal','eb green wood'][j%3])
    for q in range(4):
     dx=(q-1.5)*.065;f.line((xx,yy,-.5),(xx+dx,yy+.30+q*.025,-.45),.006,'el leaf dark');el_bloom(f,xx+dx,yy+.30+q*.025,-.43,.12,['el rose paint','eb red metal','store09 paper'][((j+row)%3)])
  f.b(a+w*.36,.64,.65,w*.68,.09,.43,'eb oak wood')
  for xx in [a+.15,a+w*.66]:f.b(xx,.38,.65,.06,.52,.34,'eb oak wood')
  for j in range(5):
   xx=a+w*(.08+j*.12);eb_plant(f,xx,.69,.65,.30)
   for q in range(4):el_bloom(f,xx+(q-1.5)*.06,1.04+math.sin(q+j)*.07,.72,.14,['el rose paint','eb red metal','store09 paper'][j%3])
 elif k in ['veniero340','venierodining','venieropastry']:
  et_canopy(f,a,b,'eb black canvas',y=3.53,drop=.55 if k=='veniero340' else .22,dep=.84 if k=='veniero340' else .72)
  el_valance(f,a,b,3.53,.55 if k=='veniero340' else .22,.84 if k=='veniero340' else .72,'Veniero’s',.12,'script')
  if k=='venierodining':
   for j in range(4):te_grid_glass(f,a+(j+.5)*w/4,.20,2.80,w/4-.055,.06,2,5,'eb oak wood')
   for j in range(4):ee_chair(f,a+(j+.5)*w/4,.90,'eb red wood')
   for xx in [a+.03,c,b-.03]:
    p02_disc(f,xx,2.64,.11,.075,.19,'eb gold metal',20);p02_disc(f,xx,2.64,.075,.045,.21,'store09 paper',20)
    f.b(xx,2.16,.14,.19,.33,.035,'eb iron');et_text(f,xx,2.16,.15,.20,'V','eb gold metal',.17,'script');p02_notice(f,xx,1.50,.18,.34,.17)
  else:
   el_pastries(f,a+.08,a+w*.58)
   if k=='veniero340':
    f.b(a+w*.33,.92,.06,w*.63,.60,.028,'eb iron');et_text(f,a+w*.30,2.02,w*.48,.18,'Veniero’s','eb red metal',.09,'italic');et_text(f,a+w*.30,1.84,w*.48,.075,'ORDER & PICKUP','eb red metal',.09,'serif')
   else:
    te_grid_glass(f,a+w*.78,.19,2.81,w*.40,.05,2,3,'eb oak wood');et_text(f,a+w*.28,2.67,w*.50,.17,'PASTICCERIA','eb iron',.10,'serif');et_hatch(f,a+.12,a+w*.51,True)
    f.b(a+w*.45,.95,.09,.30,.38,.02,'store09 paper');et_text(f,a+w*.45,.95,.20,.25,'A','eb blue metal',.11,'serif')
   p02_notice(f,b-w*.10,1.85,.22,.34,.09);eb_board(f,b-.15,.17,'MENU','eb red wood',.75)
 elif k=='340skyline':
  el_skyline(f,a,b);f.b(a+w*.33,1.45,.12,.06,2.60,.08,'eb iron');eb_blade(f,b-.20,3.30,'','eb white wood',True)
  for flip in [False,True]:
   pp=f.p(b-.20+(.035 if flip else -.035),0,.90 if flip else .18);ff=Facade(pp[0],pp[2],(-1 if flip else 1)*f.nx,(-1 if flip else 1)*f.nz,.72)
   p02_curve(ff,[(.17,3.23),(.36,3.39),(.55,3.23),(.17,3.23)],.04,'eb blue metal',.012)
   eb_arc(ff,.36,3.43,.045,.045,.05,.012,'eb blue metal')
 elif k=='smoke':
  eb_panel(f,a,b,3.27,.45,'eb blue metal');el_outline_text(f,c,3.22,w*.93,.24,'SMOKE SHOP','eb red metal',.28,'sans');et_text(f,c,3.43,w*.80,.075,'EAST VILLAGE','store09 paper',.28,'sans')
  eb_blade(f,a+w*.23,4.08,'BEER\nSMOKE\nSHOP','eb white wood',False,'eb blue metal');eb_bottles(f,a+.06,a+w*.52,.70,rows=4)
  for xx in [a+w*.20,a+w*.62]:p02_notice(f,xx,1.85,.30,.35,.08)
  et_text(f,a+w*.22,2.44,w*.34,.13,'OPEN','store09 paper',.09,'sans')
  for xx,yy in [(a+w*.16,1.4),(a+w*.43,1.2),(a+w*.76,2.1)]:p02_notice(f,xx,yy,.18,.25,.10)
 elif k=='lhasa':
  ee_curved(f,a,b,'eb black canvas',y=3.45,drop=.45,dep=.65);et_text(f,c,3.08,w*.65,.18,'LHASA','te orange board',.81,'sans');et_text(f,c,2.94,w*.80,.07,'TIBETAN RESTAURANT','store09 paper',.82,'sans');ee_shutter(f,a,b,.50,2.86)
 elif k=='bottoms':
  et_canopy(f,a,b,'eb black canvas',y=3.35,drop=.44,dep=.67);ee_shutter(f,a,a+w*.55,.35,2.86,'eb brown metal');f.b(a+w*.78,1.55,.05,w*.44,2.50,.05,'eb brown metal');el_big_tags(f,a,b,.60,2.45,.17,3,'eb gray metal')
 elif k=='russo':
  eb_panel(f,a,b,3.26,.48,'eb white wood');et_text(f,c,3.29,w*.65,.29,'RUSSO’S','eb red metal',.28,'sans');et_canopy(f,a,b,'el burgundy wood',y=3.03,drop=.23,dep=.58);el_valance(f,a,b,3.03,.23,.58,'Fresh Mozzarella & Pasta',.10,'script')
  for xx,words in [(a+w*.065,['MFRS','MOZZARELLA','& RICOTTA']),(b-w*.065,['IMPORTED','CHEESES'])]:
   f.b(xx,3.27,.26,w*.12,.39,.03,'eb green wood')
   for j,word in enumerate(words):et_text(f,xx,3.38-j*.10,w*.11,.06,word,'store09 paper',.29,'condensed')
  eb_bottles(f,a+.10,a+w*.63,.74,rows=2)
  for j in range(5):
   xx=a+w*(.08+j*.11);ee_ball(f,xx,1.25,-.45,.10,'store09 paper');f.b(xx,1.51,-.45,.14,.23,.10,'eb yellow wood')
  el_outline_text(f,a+w*.32,1.70,w*.54,.21,'Mozzarella & Pasta','eb red metal',.09,'script');et_text(f,a+w*.32,2.11,w*.52,.12,'HOMEMADE','store09 paper',.09,'sans')
  te_flat_hatch(f,a+.05,a+w*.63);p03_tags(f,a+.10,a+w*.62,.26,.55,.13,344);eb_board(f,b-.10,.17,'MENU','eb green wood',.72)
 elif k=='lovemama':
  eb_panel(f,a,b,3.23,.48,'eb red metal');et_text(f,c,3.27,w*.72,.25,'LoveMama','store09 paper',.28,'italic');et_text(f,c,3.05,w*.94,.075,'THAI   MALAYSIAN   VIETNAMESE','store09 paper',.28,'sans')
  for xx in [a+.18,b-.18]:f.b(xx,.43,.75,.41,.54,.41,'eb iron');el_shrub(f,xx,.68,.75,.55)
  for xx in [a+w*.25,a+w*.70]:ee_round_table(f,xx,-.65)
  f.b(c,.41,.17,w,.42,.03,'el bluegray paint');p02_notice(f,a+w*.42,2.25,.23,.32,.10)
 elif k=='love-return':
  eb_panel(f,a,b,3.10,.23,'eb red metal');et_text(f,c,3.10,w*.90,.12,'Keep Calm Curry On','store09 paper',.26,'italic')
  for j in range(3):
   xx=a+(j+.5)*w/3;shop09_frame(f,xx,1.60,w/3-.12,2.20,.13,'eb oak wood',.055);te_curtain(f,xx-w/6+.09,xx+w/6-.09,mat='eb pale fabric',d=.04)
  for at in [.13,.67]:nb_ac(f,a+at*w,3.55,.65,.40,.24)
 elif k=='insomnia':
  eb_panel(f,a,b,3.25,.48,'eb purple enamel');et_text(f,c,3.27,w*.80,.23,'insomnia cookies','store09 paper',.28,'sans')
  for yy in [2.98,3.50]:p02_curve(f,[(a+j*w/40,yy+math.sin(j*.55)*.04) for j in range(41)],.28,'store09 paper',.014)
  for j in range(3):
   xx=a+w*(.12+j*.22);p02_disc(f,xx,1.4,.18,.18,.09,'eb yellow wood',20)
   for k2 in range(4):p02_disc(f,xx+math.cos(k2*1.6)*.10,1.4+math.sin(k2*1.6)*.10,.025,.025,.10,'eb brown stone',8)
  p02_curve(f,[(a+j*w/32,1.85+math.sin(j*.65)*.10) for j in range(33)],.10,'store09 paper',.018)
  p02_disc(f,a+w*.12,3.26,.16,.16,.29,'store09 paper',28);p02_disc(f,a+w*.17,3.30,.125,.125,.30,'eb purple enamel',28)
  for xx in [a+w*.20,a+w*.47]:p02_notice(f,xx,1.18,.38,.52,.11)
  p02_notice(f,b-w*.17,1.95,.22,.32,.11)
 elif k=='pinnacle':
  ee_curved(f,a,b,'el burgundy wood','PINNACLE CLEANERS','serif',y=3.54,drop=.62,dep=.9);et_text(f,c,2.92,w*.62,.10,'299 E. 11 STREET','store09 paper',1.06,'sans');el_grille(f,a,b);eb_clothes(f,a+.08,b-.08,2.3)
 elif k in ['divin','divin-return','eyes','abacus']:
  et_canopy(f,a,b,'eb black canvas',y=4.10,drop=.60,dep=.86)
  name={'divin-return':'DIVIN WINE BAR','eyes':'EYES ON SECOND','abacus':'ABACUS PHARMACY'}.get(k)
  if name:el_valance(f,a,b,4.10,.60,.86,name,.15,'serif')
  else:
   for dx,dy in [(-.075,.04),(0,.04),(.075,.04),(-.038,-.025),(.038,-.025),(0,-.09)]:p02_disc(f,c+dx,3.39+dy,.027,.027,.998,'store09 paper',16)
  if k.startswith('divin'):
   eb_bottles(f,a+.1,b-.1,3.10,rows=1);f.b(c,.54,.08,w,.50,.03,'eb brown metal')
   for xx in [a+w*.25,a+w*.75]:f.b(xx,2.95,.10,w*.48,.045,.06,'eb oak wood')
   for xx in [a+w*.24,a+w*.73]:ee_round_table(f,xx,-.60)
  elif k=='eyes':
   for row in range(4):
    f.b(a+w*.34,.61+row*.40,-.41,w*.58,.035,.30,'eb oak wood')
    for j in range(5):
     xx=a+(j+.5)*w*.62/5;yy=.72+row*.40
     for side in [-1,1]:p02_ring(f,xx+side*.055,yy,.050,.035,-.38,'eb gold metal',.007,12)
     f.line((xx-.02,yy,-.38),(xx+.02,yy,-.38),.007,'eb gold metal')
   p02_notice(f,b-w*.16,1.9,.26,.34,.10);et_text(f,a+w*.33,2.65,w*.56,.08,'BY APPOINTMENT','store09 paper',.10,'serif')
  else:
   el_grille(f,a,b,.20,3.40)
   for row in range(5):
    for j in [0,1,2,5,6,7]:f.b(a+(j+.5)*w/8,.63+row*.42,-.45,w/11,.25,.15,['store09 paper','eb blue enamel','eb green wood'][j%3])
    for lo,hi in [(a+.08,a+w*.31),(a+w*.68,b-.08)]:f.b((lo+hi)/2,.48+row*.42,-.46,hi-lo,.035,.25,'eb oak wood')
   et_text(f,a+w*.70,2.65,w*.48,.16,'Rx PHARMACY','eb red metal',.17,'sans');p02_notice(f,a+w*.25,1.70,.27,.40,.17)

def el_bin(f,x,d=.75):
 f.b(x,.55,d,.43,.76,.43,'eb iron');f.b(x,.95,d,.47,.07,.47,'eb iron')
 for yy in [.37,.72]:f.b(x,yy,d+.23,.35,.025,.025,'eb iron')
 for side in [-1,1]:ee_ball(f,x+side*.16,.20,d-.15,.07,'eb iron')

def el_balcony(f,a,b,y,mat='eb iron',cross=False,horizontal=False,glass=False):
 dep=.85;f.b((a+b)/2,y,dep/2,b-a,.08,dep,'el pale stone' if glass else mat)
 for yy in [y+.10,y+.95]:f.line((a,yy,dep),(b,yy,dep),.018,mat)
 for xx in [a,b]:
  f.line((xx,y,.02),(xx,y+.95,.02),.016,mat);f.line((xx,y,.85),(xx,y+.95,.85),.016,mat);f.line((xx,y+.95,0),(xx,y+.95,.85),.016,mat)
 if glass:
  for lo,hi in [(a+(b-a)*j/3,a+(b-a)*(j+1)/3) for j in range(3)]:
   ee_front([f.p(lo+.02,y+.12,.84),f.p(hi-.02,y+.12,.84),f.p(hi-.02,y+.90,.84),f.p(lo+.02,y+.90,.84)],'store09 clear glass')
   f.line((hi,y,.85),(hi,y+.95,.85),.015,mat)
  for xx in [a,b]:ee_front([f.p(xx,y+.12,.05),f.p(xx,y+.12,.84),f.p(xx,y+.90,.84),f.p(xx,y+.90,.05)],'store09 clear glass')
 elif horizontal:
  for yy in [y+.25,y+.42,y+.59,y+.76]:f.line((a,yy,.85),(b,yy,.85),.012,mat)
 else:
  n=max(2,round((b-a)/(.85 if cross else .17)))
  for j in range(n+1):
   xx=a+(b-a)*j/n;f.line((xx,y+.10,.85),(xx,y+.95,.85),.010,mat)
   if cross and j<n:
    xx2=a+(b-a)*(j+1)/n
    for lo,hi in [(y+.15,y+.89),(y+.89,y+.15)]:f.line((xx,lo,.86),(xx2,hi,.86),.011,mat)
    ee_star(f,(xx+xx2)/2,y+.52,.09,.88,mat)

def el_garage(f):
 for a,b,top in [(f.L*.025,f.L*.405,3.80),(f.L*.535,f.L*.87,4.45)]:
  # Register the aperture directly: the generic window helper adds a level
  # bottom reveal that would cap this observed descending vehicle ramp.
  OPENINGS[frontage_key(f)].append((a,.17,b,top))
  f.b((a+b)/2,(top-1.10)/2,-4.0,b-a,top+1.10,.08,'recess shadow')
  for side in [a,b]:f.b(side,(top-1.10)/2,-2,.14,top+1.10,4.,'eb red brick')
  ee_front([f.p(a,.17,.02),f.p(b,.17,.02),f.p(b,-1.05,-4),f.p(a,-1.05,-4)],'eb gray stone')
  f.b((a+b)/2,top-.15,-.25,b-a,.30,.45,'eb gray metal')
  for j in range(8):f.b((a+b)/2,top-.28+j*.025,-.01,b-a,.014,.035,'eb silver metal')
  for yy in [1.,2.]:f.b((a+b)/2,yy,-3.95,b-a,.10,.03,'eb yellow wood')
  f.b((a+b)/2,top,-2.,b-a,.08,4.,'eb charcoal stone')
 eb_blade(f,f.L*.43,5.1,'PARK\n24 HRS','eb iron',False,'store09 paper')
 for yy,text in [(3.5,'PARKING'),(2.6,'NO PARKING')]:et_text(f,f.L*.47,yy,.85,.12,text,'store09 paper',.15,'sans')
 for row in range(4):
  yy=5.05+row*3.45;xx=f.L*.28
  shop09_frame(f,xx,yy+1.,1.10,2.0,.07,'eb cream stone',.07);f.b(xx,yy+1.,.015,.94,1.84,.02,'eb dark red brick')
  f.strip(yy+2.6,.14,.18,'eb cream stone')
  for j in range(round(f.L/.26)):f.b((j+.5)*f.L/round(f.L/.26),yy+2.42,.10,.12,.23,.20,'eb red brick')
 et_text(f,f.L*.58,18.9,f.L*.70,.25,'PARKING GARAGE','eb brown stone',.03,'condensed')

def el_architecture(f,r,h):
 s=r['e11Block'];n=s['number'];mat=s['trim'];neutral={**s,'number':'e11-'+n}
 # Mechanics get a namespaced number so old street-specific exceptions cannot fire.
 ee_architecture(f,{**r,'e09East':neutral,'observedGround':{**r['observedGround'],'basementAreaways':[]}},h)
 for well in r['observedGround'].get('basementAreaways',[]):
  xx=well['at']*f.L;ww=well['width']*f.L;dep=well['depth'];below=well['depthBelow']
  for aa,bb in [((xx-ww/2,0),(xx-ww/2,dep)),((xx-ww/2,dep),(xx+ww/2,dep)),((xx+ww/2,dep),(xx+ww/2,0))]:ee_front([f.p(aa[0],-below,aa[1]),f.p(bb[0],-below,bb[1]),f.p(bb[0],.14,bb[1]),f.p(aa[0],.14,aa[1])],'eb gray stone')
 if n in ['304','306']:
  for yy in [3.55,7.25,10.6,14.0]:f.strip(yy,.16,.17,'eb brown stone')
  for d in r['doors']:
   xx=d['at']*f.L;eb_lamp(f,xx-.85,2.80,.20);eb_lamp(f,xx+.85,2.80,.20);et_text(f,xx+.77,2.10,.30,.14,n,'store09 paper',.18,'serif')
  el_bin(f,f.L*.10);el_bin(f,f.L*.88)
 if n in ['314','316']:
  # Shared six-bay facade keeps its two cadastral owners and continuous cornice.
  for w in r['windows']:
   if 'row' not in w:continue
   xx=w['at']*f.L;yy=w['bottom']+w['height']
   if w['row']==3:et_fan(f,xx,yy+.10,w['width']*f.L*.65,.36,'eb brown stone')
  for j in range(max(1,round(f.L/.60))):ee_scroll(EtCarvedRelief(f),(j+.5)*f.L/max(1,round(f.L/.60)),h-.65,.15,'eb brown stone',.22)
  for yy in [4.2,7.65,11.1,14.55]:el_balcony(f,.05,f.L-.05,yy)
  # Only the broader316owner owns diagonal stair flights; no duplicate pair mass.
  if n=='316':
   for yy in [4.2,7.65,11.1]:
    for side in [0,.35]:f.line((f.L*.10+side,yy,.75),(f.L*.52+side,yy+3.45,.10),.025,'eb iron')
    for j in range(14):
     t=j/14;f.b(f.L*(.10+.42*t)+.17,yy+3.45*t,.75-.65*t,.40,.035,.09,'eb iron')
  for xx in [.08*f.L,.60*f.L]:el_bin(f,xx)
  ac=s['access'];xx=ac['at']*f.L;ww=ac['width'];rise=ac['rise'];dep=ac['depth']
  for j in range(4):f.b(xx,.17+(j+1)*(rise-.17)/4,.04+dep*(1-j/4),ww,.055,.11,'eb brown stone')
 if n=='318':
  for row in range(5):
   yy=3.85+row*3.0
   for xx in [f.L*.29,f.L*.67]:
    f.b(xx,yy+1.,.10,.35,2.35,.24,'eb cream stone');te_mask(f,xx,yy+2.10,.80,'eb cream stone')
    for j in range(5):f.b(xx,yy+.2+j*.32,.24,.27,.035,.05,'eb brown stone')
   et_foliage(f,f.L*.30,f.L*.67,yy+2.48,'eb cream stone',.25)
   f.strip(yy-.29,.18,.19,'eb cream stone')
 if n=='320':
  pts=[f.p(f.L*.86+math.cos(j*math.tau/8)*.30,3.40+math.sin(j*math.tau/8)*.30,.09) for j in range(8)];ee_front(pts,'eb gray stone')
 if n=='322':
  for row in range(6):
   yy=3.9+row*2.95
   if row in [1,5]:
    for y2 in [yy-.23,yy+.15,yy+1.25,yy+2.05]:el_skin(f,0,f.L,y2,y2+.08,'eb brown stone')
   for w in r['windows']:
    if w.get('row')!=row:continue
    xx=w['at']*f.L;ww=w['width']*f.L
    if row in [2,3]:shop09_frame(f,xx,yy-.50,ww+.12,.52,.12,'eb cream stone',.075);te_mask(f,xx,yy-.50,.65,'eb cream stone')
    if row in [1,4]:eb_arc(f,xx,yy+w['height'],ww*.62,.27,.20,.06,'eb cream stone')
  ee_escape(f,{'span':[.29,.73],'levels':[6.7+i*2.95 for i in range(5)],'material':'eb iron','dropAt':.30,'ornament':'plain'})
  el_balcony(f,.60*f.L,.99*f.L,3.70)
  x=.50*f.L;f.b(x,4.63,.05,1.30,.68,.015,'el mural blue');pts=[f.p(x-.65,4.96,.06),f.p(x+.65,4.96,.06)]+[f.p(x+.65*math.cos(j*math.pi/24),4.96+.65*math.sin(j*math.pi/24),.06) for j in range(25)];ee_front(pts,'el mural blue');eb_arc(f,x,4.96,.65,.65,.08,.04,'eb blue metal')
  for j in range(5):eb_arc(f,x+(j-2)*.20,4.65,.14,.37,.09,.018,'el mural violet')
  for xx in [x-.72,x+.72]:eb_lamp(f,xx,3.50,.23)
 if n=='326':
  el_skin(f,0,f.L,.17,3.70,'el bluegray paint',.04)
  for w in r['windows']:
   if 'row' not in w:continue
   ww=w['width']*f.L;xx=w['at']*f.L;yy=w['bottom']
   if w['row'] in [1,2,3]:shop09_frame(f,xx,yy-.48,ww*.95,.40,.14,'eb gray stone',.06);et_foliage(f,xx-ww*.40,xx+ww*.40,yy-.48,'eb gray stone',.24)
   top=yy+w['height'];kind=s['rowHeads'][w['row']]
   if kind=='segmental':eb_arc(f,xx,top,ww*.62,.25,.19,.075,'eb gray stone')
   else:
    for off,thick,dep in [(0,.09,.14),(.10,.08,.21),(.19,.045,.26)]:f.b(xx,top+off,dep,ww+.20+off*.7,thick,.14,'eb gray stone')
   if kind=='keystone':f.b(xx,top+.16,.27,.23,.38,.16,'eb gray stone')
   if kind=='molded':et_foliage(f,xx-ww*.42,xx+ww*.42,top+.23,'eb gray stone',.29)
 if n in ['322','326']:
  d=r['doors'][0];xx=d['at']*f.L;ww=d['width']*f.L
  te_grid_glass(f,xx,.35,d['leafTop']-.08,ww*.80,-.02,3 if n=='322' else 2,5,'eb white wood' if n=='322' else 'eb iron')
  f.line((xx+ww*.32,1.20,.045),(xx+ww*.32,1.50,.045),.015,'eb silver metal')
  if n=='322':shop09_frame(f,xx,1.75,ww+.10,2.95,.08,'eb oak wood',.055)
 if n=='330':
  for w in r['windows']:
   if w.get('col')==2:f.b(w['at']*f.L-w['width']*f.L/6,w['bottom']+w['height']/2,.035,.055,w['height'],.055,'eb sash')
 if s.get('crossedBalconies'):
  for i in range(4):el_balcony(f,.25*f.L,.76*f.L,s['upperBottom']-.17+i*s['step'],cross=True)
 if n=='338':
  for row in range(1,4):
   for a,b in [(.04,.22),(.78,.97)]:el_balcony(f,a*f.L,b*f.L,s['upperBottom']-.16+row*s['step'])
 if n=='340':
  for lo,hi in [(0,.25),(.75,1)]:
   p=f.p(lo*f.L,0,0);sub=Facade(p[0],p[2],f.rx,f.rz,(hi-lo)*f.L);eb_cornice(sub,h,{**s,'cornice':'brackets','corniceColor':'gray stone'})
  et_fan(f,f.L*.5,h-.05,f.L*.25,.75,'eb gray stone');p02_ring(f,f.L*.5,h+.18,.15,.15,.31,'eb gray stone',.04)
  for xx in [f.L*.37,f.L*.63]:ee_scroll(EtCarvedRelief(f),xx,h+.03,.15,'eb gray stone',.30)
  for xx in [f.L*.26,f.L*.74]:f.b(xx,h-.30,.25,.25,.65,.38,'eb gray stone');et_mask(f,xx,h-.20,.70,'eb gray stone')
  for yy in [h-.32,h-.14]:f.b(f.L*.5,yy,.30,f.L*.47,.075,.36,'eb gray stone')
 if n=='342':
  for j in range(7):
   xx=(j+.5)*f.L/7;shop09_frame(f,xx,h-.63,f.L/8,.30,.32,'eb cream stone',.055);te_mask(f,xx,h-.63,.55,'eb cream stone')
  el_neon_veniero(f,f.L*.54)
  for xx,colors in [(f.L*.04,['eb blue metal','store09 paper','eb red metal']),(f.L*.16,['eb green wood','store09 paper','eb red metal'])]:
   f.line((xx,5.6,.08),(xx,6.4,1.60),.018,'eb gray metal')
   if colors[0]=='eb blue metal':
    for j in range(13):ee_front([f.p(xx,6.35-j*.062,1.55),f.p(xx+.80,6.20-j*.062,1.60),f.p(xx+.80,6.138-j*.062,1.60),f.p(xx,6.288-j*.062,1.55)],'eb red metal' if j%2==0 else 'store09 paper')
    ee_front([f.p(xx,6.35,1.56),f.p(xx+.34,6.286,1.60),f.p(xx+.34,5.85,1.60),f.p(xx,5.916,1.56)],'eb blue metal')
    for row in range(5):
     for col in range(6):ee_star(f,xx+.025+col*.052,6.31-row*.075-col*.009,.013,1.615,'store09 paper')
   else:
    for j,ma in enumerate(colors):
     lo=xx+j*.80/3;hi=xx+(j+1)*.80/3;ee_front([f.p(lo,6.35-j*.05,1.60),f.p(hi,6.30-j*.05,1.60),f.p(hi,5.49-j*.05,1.60),f.p(lo,5.54-j*.05,1.60)],ma)
 # Per-entry label, jamb and fittings; no inherited every-door transom number.
 for d in r['doors']:
  xx=d['at']*f.L;ww=d['width']*f.L;num=d.get('observedNumber',n.split('-')[0])
  if n.startswith(('school','177','170','300','311','305')) or n in ['304','306','310']:continue
  if n=='322':f.b(xx,d['top']-.25,.015,.34,.14,.025,'store09 paper');et_text(f,xx,d['top']-.25,.30,.095,num,'eb iron',.035,'serif')
  else:et_text(f,xx,d['top']-.25,min(.70,ww*.80),.15,num,'eb gold metal' if n in ['304','306','314','316'] else 'store09 paper',-.02,'serif')
  f.b(xx+ww/2+.13,1.48,.11,.09,.23,.035,'eb silver metal')
  for j in range(4):f.b(xx+ww/2+.13,1.42+j*.035,.135,.018,.012,.008,'eb iron')
 if s.get('tower'):
  for yy in [4.1,7.45,10.55,17.0,38.4,47.3]:f.strip(yy,.20,.20,'eb cream stone')
  el_skin(f,0,f.L,.17,9.0,'eb cream stone');el_skin(f,0,f.L,.17,.80,'eb gray stone')
  for col in range(7 if n=='170-Second' else 13):
   xx=(col+.5)*f.L/(7 if n=='170-Second' else 13)
   for yy in [7.3,10.35,38.1,41.3]:
    shop09_frame(f,xx,yy-.34,.65,.50,.13,'eb cream stone',.04);te_mask(f,xx,yy-.34,.75,'eb cream stone')
  for xx in [f.L*.04,f.L*.96]:f.b(xx,42.75,.12,.34,8.7,.24,'eb cream stone')
  if n=='170-Second':
   xx=f.L*.39;te_lancet(f,xx,.25,4.1,1.7,'eb gray stone');et_text(f,xx,3.20,.9,.21,'170','eb gold metal',.15,'serif')
   for side in [-1,1]:eb_plant(f,xx+side*1.25,.17,.65,.50)
  else:
   xx=f.L*.43;te_lancet(f,xx,.75,5.15,2.65,'eb cream stone')
   for side in [-1,1]:f.b(xx+side*1.9,5.5,.12,.40,10.7,.25,'eb cream stone');te_mask(f,xx+side*1.9,6.0,1.7,'eb cream stone')
   xx=f.L*.255;et_text(f,xx,2.70,.52,.20,'300','eb gold metal',.13,'serif')
   for side in [-1,1]:eb_lamp(f,xx+side*.70,2.9,.23)
   for at in [.22,.50,.78]:
    el_balcony(f,at*f.L-.95,at*f.L+.95,16.88,'eb cream stone');et_foliage(f,at*f.L-.85,at*f.L+.85,16.68,'eb cream stone',.25)

def el_face(b,idx,r):
 v=b['frontages'][idx];f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']);f.wall=r['wall']
 clean=deepcopy(r);clean['observedGround']['basementAreaways']=[];clean['windows']=[w for w in r['windows'] if not w.get('planeDepth')];clean['doors']=[d for d in r['doors'] if not d.get('planeDepth')]
 fidelity_elevation({**b,'businesses':[],'seventhArchitecture':clean},f,clean)
 for w in r['windows']:
  if dep:=w.get('planeDepth'):fidelity_window(el_offset(f,dep),w)
 for d in r['doors']:
  if dep:=d.get('planeDepth'):fidelity_door(el_offset(f,dep),d)
 return f

def el_shell(b,records,h,mat,roof=True):
 # Side/rear closures only. Detailed street skins are emitted after their holes.
 fronts=[b['frontages'][idx] for idx,r in records]
 def belongs(a,c,v):
  return all(-.16<=(q[0]-v['x'])*v['rx']+(q[1]-v['z'])*v['rz']<=v['length']+.16 and abs(-(q[0]-v['x'])*v['rz']+(q[1]-v['z'])*v['rx'])<.16 for q in [a,c])
 for a,c in zip(b['p'],b['p'][1:]+b['p'][:1]):
  if any(belongs(a,c,v) for v in fronts):continue
  ee_front([(a[0],.17,a[1]),(c[0],.17,c[1]),(c[0],h,c[1]),(a[0],h,a[1])],mat)
 # Two-sided tops are deliberately above facade skins, never cover open recesses.
 if not roof:return
 verts=[Vector((a[0],h,a[1])) for a in b['p']]
 for tri in tessellate_polygon([verts]):ee_front([verts[v] if isinstance(v,int) else v for v in tri],'roof')

def el_lot_mass(b,r):
 # Painted, windowed light-well sides at324: use the actual stepped municipal
 # edges. Adding temporary skin frontages lets the normal wall finisher cut
 # real openings, without moving the footprint or creating another owner.
 p=b['p']
 if sum(a[0]*c[1]-c[0]*a[1] for a,c in zip(p,p[1:]+p[:1]))>0:p=list(reversed(p))
 fronts=list(b['frontages']);east=b['id']==247851925
 for a,c in zip(p,p[1:]+p[:1]):
  length=math.dist(a,c)
  if length<2.5:continue
  rx=(c[0]-a[0])/length;rz=(c[1]-a[1])/length;mid=(a[0]+c[0])/2
  if abs(rz)<.95 or not(-rz>.8 if east else -rz<-.8) or not(mid>-109 if east else mid<-97) or min(a[1],c[1])<-67.1 or max(a[1],c[1])>-48.8:continue
  f=Facade(a[0],a[1],rx,rz,length);f.wall='el ivory paint';fronts.append({'x':a[0],'z':a[1],'rx':rx,'rz':rz,'length':length,'street':'Eleventh324lotSide'})
  if min(a[1],c[1])<-61.0:continue
  for row in range(6 if east else 5):
   fidelity_window(f,{'at':.5,'width':.85/length,'bottom':3.95+row*(2.95 if east else 3.15),'height':1.65,'frame':'eb sash','trim':'eb gray stone','hood':'none','rails':[.5]})
 wall_mass({**b,'frontages':fronts,'facadeSpec':{'elevations':{'Eleventh324lotSide':{'wall':'el ivory paint'}}}},r['wall'],False)

def el_court(b,records):
 idx,r=records[0];f=el_face(b,idx,r);h=b['renderHeight'];mat=r['wall'];rear=el_offset(f,-2.0);a=f.L*.38;bb=f.L*.62
 el_shell(b,records,h,mat,False)
 # Roof follows the observed central notch, rather than bridging the courtyard.
 poly=list(b['p']);poly[0:2]=[poly[0],[f.x+bb*f.rx,f.z+bb*f.rz],[rear.x+bb*rear.rx,rear.z+bb*rear.rz],[rear.x+a*rear.rx,rear.z+a*rear.rz],[f.x+a*f.rx,f.z+a*f.rz],poly[1]]
 verts=[Vector((p[0],h,p[1])) for p in poly]
 for tri in tessellate_polygon([verts]):ee_front([verts[v] if isinstance(v,int) else v for v in tri],'roof')
 el_skin(f,0,a,.17,h,mat);el_skin(f,bb,f.L,.17,h,mat);el_skin(rear,a,bb,.17,h,mat)
 for xx in [a,bb]:ee_front([f.p(xx,.17,0),f.p(xx,.17,-2),f.p(xx,h,-2),f.p(xx,h,0)],mat)
 ee_front([f.p(a,.17,0),f.p(bb,.17,0),f.p(bb,.17,-2),f.p(a,.17,-2)],'eb gray stone')
 # Remove roof over the entrance court by dark recess top ledge below parapet.
 for wing in [(0,a),(bb,f.L)]:
  lo,hi=wing
  for yy in [3.25,14.8]:f.b((lo+hi)/2,yy,.10,hi-lo,.15,.25,'eb buff stone')
  for row in range(4):
   yy=3.8+row*2.55
   for p1,p2 in [(.16*f.L,.22*f.L)] if lo==0 else [(.78*f.L,.84*f.L)]:
    for j in range(8):
     for k in range(6):f.b(p1+(p2-p1)*(j+.5)/8,yy+.12+k*.27,.10,.085,.17,.18,mat)
   for at in [.045,.135,.245,.335] if lo==0 else [.665,.755,.865,.955]:
    xx=at*f.L
    for y2 in [yy-.10,yy+1.85]:f.b(xx,y2,.12,1.76,.12,.28,'eb buff stone')
  for xx in [lo+.18,hi-.18]:f.b(xx,h/2,.07,.22,h,.18,mat)
 for row in range(4):el_balcony(rear,a+.12,bb-.12,3.60+row*2.55,horizontal=True)
 # Alternating stairs in the real inset courtyard, horizontal front railings.
 for row in range(3):
  yy=3.60+row*2.55;aa=a+.30;cc=bb-.55
  if row%2:aa,cc=cc,aa
  for off in [0,.36]:rear.line((aa+off,yy,.65),(cc+off,yy+2.55,.05),.023,'eb iron')
  for j in range(12):
   t=j/12;rear.b(aa+(cc-aa)*t+.18,yy+2.55*t,.65-.60*t,.40,.035,.10,'eb iron')
 x=f.L*.50;ww=3.20
 # Projecting white door portal has a shallow concave crown and small square vent.
 for side in [-1,1]:f.b(x+side*(ww/2-.25),1.6,.35,.50,2.86,.70,'eb white stone')
 f.b(x,3.20,.35,ww,.50,.70,'eb white stone')
 for j in range(16):
  xx=x-ww/2+(j+.5)*ww/16;cy=3.65-.16*math.cos((xx-x)/ww*math.pi);f.b(xx,cy,.35,ww/16+.005,.18,.70,'eb white stone')
 f.b(x,3.42,.72,.35,.27,.02,'eb iron');et_text(f,x,2.98,.65,.17,'305','eb brown metal',.72,'serif')
 for side in [-1,1]:
  xx=x+side*2.10;f.b(xx,.55,.40,.85,.78,.80,'eb white stone')
  for j in range(8):f.b(xx+(j-3.5)*.09,.55,.82,.025,.64,.04,'eb buff stone')
 for w in r['windows']:
  if [w.get('row',-1),w.get('col',-1)] in r['e11Block'].get('windowAC',[]):nb_ac(f,w['at']*f.L,w['bottom']+.15,.65,.35,.18)

def el_modern(b,records):
 idx,r=records[0];f=el_face(b,idx,r);low=18.2;high=b['renderHeight'];a=f.L*.32;bb=f.L*.68
 el_shell(b,records,low,'eb red brick')
 rear=el_offset(f,-.50);el_skin(rear,0,f.L,.17,3.0,r['wall']);el_skin(f,0,f.L,3.,low,r['wall']);el_skin(f,a,bb,low,high,r['wall'])
 for xx in [a,bb]:ee_front([f.p(xx,low,0),f.p(xx,low,-15),f.p(xx,high,-15),f.p(xx,high,0)],r['wall'])
 ee_front([f.p(a,high,0),f.p(bb,high,0),f.p(bb,high,-15),f.p(a,high,-15)],'roof')
 ee_front([f.p(a,low,-15),f.p(bb,low,-15),f.p(bb,high,-15),f.p(a,high,-15)],'eb red brick')
 for yy in [3.02,3.2,18.2]:f.strip(yy,.12,.14,r['wall'])
 for yy in [1.,1.55,2.10,2.65,3.5,4.0,4.5,5.0,5.5]:el_skin(rear if yy<3.0 else f,0,f.L,yy,yy+.015,'eb gray stone')
 for row in range(1,5):
  yy=3.24+row*2.9
  for lo,hi in [(.16,.315),(.315,.47),(.66,.83)]:el_balcony(f,lo*f.L,hi*f.L,yy,'eb silver metal',glass=True)
  ee_front([f.p(f.L*.315,yy,.03),f.p(f.L*.315,yy,.85),f.p(f.L*.315,yy+2.3,.85),f.p(f.L*.315,yy+2.3,.03)],'store09 clear glass')
 for yy in [17.74,20.39]:el_balcony(f,.32*f.L,.48*f.L,yy,'eb silver metal',glass=True)
 for xx in [f.L*.015,f.L*.16,f.L*.31,f.L*.46,f.L*.61,f.L*.76,f.L*.90]:
  rod(f.p(xx,.17,-.03),f.p(xx,3.0,-.03),.20,'el smooth limestone',24)
  f.b(xx+.62,.37,.18,.85,.40,.55,'eb iron');el_shrub(f,xx+.62,.57,.18,.65)
 x=f.L*.825
 ee_front([f.p(x-1.6,3.04,-.05),f.p(x+1.6,3.04,-.05),f.p(x+1.6,3.04,.90),f.p(x-1.6,3.04,.90)],'store09 clear glass')
 for side in [-1,1]:f.line((x+side*1.40,2.75,.0),(x+side*1.40,3.04,.90),.025,'eb silver metal')
 for side in [-1,1]:et_text(f,x+side*.50,2.64,.43,.13,'311','store09 paper',-.36,'serif')
 # Observed exposed schoolyard side: narrow windows and horizontal pale bands.
 v=b['frontages'][idx];p=f.p(f.L,0,0);side=Facade(p[0],p[2],-f.nx,-f.nz,22.0);side.wall='eb red brick'
 # Its side skin overlays the generic red closure only at positive depth.
 for row in range(5):
  yy=3.4+row*2.9
  for at in [.12,.30,.51,.72,.88]:
   side.b(at*side.L,yy+1.05,.04,.72,2.1,.04,'seventh reflective glass');shop09_frame(side,at*side.L,yy+1.05,.78,2.17,.08,'eb white stone',.07)
  side.strip(yy-.26,.17,.12,'eb white stone')

def el_projected_corner(b,records):
 low=6.45;h=b['renderHeight'];el_shell(b,records,h,'el tan brick')
 for idx,r in records:
  f=el_face(b,idx,r);back=el_offset(f,-1.05);first=r['e11Block']['number']=='174-Second';split=f.L if first else f.L*.63
  el_skin(f,0,split,.17,low,r['wall']);el_skin(back,0,split,low,h,r['wall'])
  if split<f.L:el_skin(f,split,f.L,.17,h,r['wall']);ee_front([f.p(split,low,0),f.p(split,low,-1.05),f.p(split,h,-1.05),f.p(split,h,0)],r['wall'])
  ee_front([f.p(0,low,0),f.p(split,low,0),f.p(split,low,-1.05),f.p(0,low,-1.05)],'roof')
  for ff,lo,hi,yy in [(f,0,split,low),(back,0,split,h),(f,split,f.L,h)]:
   if hi>lo:ff.b((lo+hi)/2,yy,.09,hi-lo,.16,.20,'eb cream stone')
  for w in r['windows']:
   ff=el_offset(f,w.get('planeDepth',0));x=w['at']*f.L;ww=w['width']*f.L
   for yy in [w['bottom']-.10,w['bottom']+w['height']+.10]:ff.b(x,yy,.08,ww+.18,.13,.18,'eb cream stone')
  if first:
   ee_escape(back,{'span':[.13,.65],'levels':[6.30,9.15,12.0],'material':'eb iron','dropAt':.60,'ornament':'plain'})
   
   for yy in [low+.12,low+.75]:f.line((.03,yy,.10),(split-.03,yy,.10),.014,'eb iron')
   for j in range(max(2,round(split/.16))+1):
    xx=.03+(split-.06)*j/max(2,round(split/.16));f.line((xx,low,.10),(xx,low+.75,.10),.009,'eb iron')
  else:
   for ff,span,levels in [(back,[.17,.32],[6.3,9.15,12.0]),(f,[.72,.94],[3.43,6.28,9.13,11.98])]:ee_escape(ff,{'span':span,'levels':levels,'material':'eb iron','dropAt':span[0]+.02,'ornament':'plain'})
   el_architecture(f,{**r,'e11Block':{**r['e11Block'],'cornice':'carriage','head':'none','windowAC':[]},'windows':[]},h)

def el_school(b,records):
 # The yard exposes the owner's west wall. Its southern30m is visible in the
 # dated oblique; beyond that depth the plain closure remains an explicit limit.
 a=b['p'][2];c=b['p'][1];length=math.dist(a,c);v={'x':a[0],'z':a[1],'rx':(c[0]-a[0])/length,'rz':(c[1]-a[1])/length,'length':length,'street':'schoolyard-side'}
 side=Facade(v['x'],v['z'],v['rx'],v['rz'],length);side.wall='el school brick'
 el_shell({**b,'frontages':[*b['frontages'],v]},[*records,(len(b['frontages']),{})],b['renderHeight'],'el school brick')
 for lo,hi in [(.52,.73),(.76,.96)]:
  for row,yy in enumerate([3.05,6.15]):
   count=round((hi-lo)*length/.95)
   for j in range(count):fidelity_window(side,{'at':lo+(j+.5)*(hi-lo)/count,'width':((hi-lo)*length/count-.07)/length,'bottom':yy,'height':1.95,'frame':'eb brown metal','trim':'eb gray stone','hood':'none','rails':[.2,.4,.6,.8]})
   side.b((lo+hi)*length/2,yy+2.05,.16,(hi-lo)*length+.20,.13,.38,'eb gray stone')
 for at in [.63,.89]:fidelity_door(side,{'at':at,'width':1.7/length,'bottom':.20,'top':2.85,'leafTop':2.2,'leaves':2,'material':'eb gold metal','trim':'eb gray stone','recess':.25,'panels':[{'y':.5,'height':.85,'width':.80}]})
 for at in [.54,.72,.79,.96]:fidelity_window(side,{'at':at,'width':.90/length,'bottom':.65,'height':1.10,'frame':'eb brown metal','trim':'eb gray stone','hood':'none','grille':True})
 el_skin(side,0,length,.17,9.25,'el school brick');side.strip(9.22,.15,.18,'eb gray stone')
 for idx,r in records:
  f=el_face(b,idx,r);back=el_offset(f,-.70)
  if idx==0:el_skin(f,0,f.L,.17,9.25,r['wall'])
  else:
   el_skin(f,.20*f.L,.44*f.L,.17,9.25,r['wall'])
   for lo,hi in [(0,.20),(.44,1)]:el_skin(back,lo*f.L,hi*f.L,.17,9.25,r['wall'])
   for x in [0,.20*f.L,.44*f.L,f.L]:ee_front([f.p(x,.17,0),f.p(x,.17,-.70),f.p(x,9.25,-.70),f.p(x,9.25,0)],r['wall'])
  f.strip(9.22,.15,.18,'eb gray stone')
  for yy in [5.10,8.20]:
   if idx==0:f.b(f.L/2,yy,.28,f.L-.65,.14,.65,'eb gray stone')
   else:
    for lo,hi in [(.20,.44),(.54,.84)]:
     ff=f if lo==.20 else back;ff.b((lo+hi)*f.L/2,yy,.26,(hi-lo)*f.L+.30,.14,.60,'eb gray stone')
  for yy in [9.40,9.72]:f.line((.15,yy,.10),(f.L-.15,yy,.10),.015,'eb gray metal')
  for j in range(round(f.L/1.5)+1):f.line((.15+j*(f.L-.30)/round(f.L/1.5),9.25,.10),(.15+j*(f.L-.30)/round(f.L/1.5),9.72,.10),.012,'eb gray metal')
  if idx==0:
   for w in r['windows']:
    if [w.get('row',-1),w.get('col',-1)] in r['e11Block'].get('windowAC',[]):nb_ac(f,w['at']*f.L,w['bottom']+1.63,.61,.40,.24)
    if 'row' not in w:el_grille(f,w['at']*f.L-.45,w['at']*f.L+.45,w['bottom'],w['bottom']+w['height'],.10,'eb brown metal',True)
   eb_blade(f,f.L-.70,5.20,'P.S.19\nEAST VILLAGE\nCOMMUNITY SCHOOL','eb white wood',False,'eb blue metal')
  else:
   el_skin(f,.20*f.L,.39*f.L,.17,2.90,'eb charcoal stone')
   et_text(f,.29*f.L,2.55,f.L*.17,.25,'P.S. 19 ASHER LEVY P.S.','eb gold metal',.15,'serif');p02_disc(f,.385*f.L,2.50,.33,.33,.16,'eb gold metal',32)
   for x in [.16,.50,.88]:back.b(x*f.L,3.04,.40,2.70,.13,.95,'eb gray stone')
   for x in [.16,.42,.50,.88]:
    f.b(x*f.L,.23,.45,2.5,.13,.85,'eb gray stone')
    for side in [-1,1]:f.b(x*f.L+side*1.1,2.74,-.08,.25,.08,.03,'store09 paper')
   for lo,hi in [(.01,.13),(.185,.385),(.53,.85),(.91,.99)]:
    # Green fence and planted strip; entries stay separately open.
    a=lo*f.L;bb=hi*f.L
    for yy in [.30,1.1]:f.line((a,yy,1.10),(bb,yy,1.10),.018,'eb green wood')
    for j in range(max(2,round((bb-a)/.15))+1):
     xx=a+(bb-a)*j/max(2,round((bb-a)/.15));f.line((xx,.17,1.10),(xx,1.30,1.10),.011,'eb green wood')
    for j in range(max(1,round((bb-a)/1.6))):eb_plant(f,a+(j+.5)*(bb-a)/max(1,round((bb-a)/1.6)),.17,.55,.40)

def el_mural(f):
 # Authored layered contours, based on the dated mural view. This is a visual
 # interpretation rather than a reproduction/texture of the original painting.
 L=f.L*.74
 el_skin(f,0,L,3.3,12.50,'el mural blue')
 def poly(points,mat,d=.056):ee_front([f.p(x*L,y,d) for x,y in points],mat)
 def line(points,mat='el skin shadow',r=.025,d=.074):p02_curve(f,[(x*L,y) for x,y in points],d,mat,r)
 # Angular architectural/collage fields behind the two figures.
 poly([(0,12.4),(.14,12.4),(.08,10.9),(0,10.1)],'el mural cream')
 poly([(0,10.5),(.18,9.7),(.07,7.2),(0,7.5)],'eb red wood')
 poly([(.39,12.5),(.64,12.0),(.55,9.4),(.43,10.1)],'el mural violet')
 poly([(.44,3.3),(.52,5.4),(.48,8.1),(.65,7.1),(.64,3.3)],'eb cyan enamel')
 poly([(0,3.3),(.08,6.8),(.20,7.4),(.36,7.3),(.48,6.2),(.55,3.3)],'eb iron',.059)
 # Portrait hair cap, swept back with fine gray strands and shadowed temples.
 poly([(.075,9.5),(.070,10.4),(.09,11.3),(.14,11.77),(.24,11.96),(.32,11.76),(.37,11.25),(.39,10.4),(.36,9.4)],'el portrait hair',.061)
 for j in range(28):
  x=.10+j*.0095;line([(x,10.8),(x-.012,11.25),(.20+(x-.22)*.60,11.73)],'eb gray metal',.014,.064)
 # Tapered jaw/cheeks, neck and individually placed light/shadow planes.
 poly([(.105,10.95),(.14,11.26),(.22,11.37),(.31,11.14),(.355,10.55),(.36,9.9),(.35,9.0),(.32,8.22),(.27,7.68),(.22,7.55),(.16,7.85),(.11,8.4),(.085,9.4)],'el skin mid',.066)
 poly([(.11,10.9),(.17,11.10),(.23,11.12),(.215,10.1),(.19,9.25),(.15,8.45),(.11,8.9),(.095,9.7)],'el skin light',.068)
 poly([(.25,10.8),(.32,10.7),(.35,10.1),(.34,9.2),(.31,8.5),(.28,8.25),(.28,9.2)],'el skin shadow',.068)
 poly([(.16,8.1),(.23,7.75),(.29,8.15),(.29,7.05),(.24,6.75),(.18,7.05)],'el skin mid',.067)
 poly([(.18,7.4),(.25,7.0),(.29,7.3),(.29,6.9),(.23,6.75)],'el skin shadow',.069)
 # Eye sockets, eyelids, irises, raised brows and the strong dark glasses.
 for x,y,tilt in [(.15,9.91,.08),(.286,9.63,-.04)]:
  poly([(x-.045,y),(x-.022,y+.19),(x+.020,y+.16),(x+.042,y-.02),(x+.015,y-.12),(x-.02,y-.12)],'el mural cream',.072)
  p02_disc(f,x*L,y+.02,.10,.15,.076,'el portrait hair',20);p02_disc(f,x*L+.025,y+.055,.027,.035,.080,'store09 paper',12)
  line([(x-.044,y+.03),(x-.020,y+.17),(x+.015,y+.16),(x+.040,y-.01)],'el portrait hair',.032,.078)
  line([(x-.048,y+.40),(x-.018,y+.52),(x+.020,y+.43),(x+.042,y+.32)],'el portrait hair',.05,.075)
  pts=[(x-.060,y+.36),(x+.052,y+.28),(x+.048,y-.23),(x+.018,y-.40),(x-.040,y-.31),(x-.060,y+.36)]
  line(pts,'eb iron',.067,.083)
 line([(.205,10.04),(.222,10.08),(.232,9.94)],'eb iron',.06,.084)
 line([(.086,10.25),(.067,10.42)],'eb iron',.07,.084)
 line([(.337,9.90),(.376,10.1)],'eb iron',.07,.084)
 # Nose ridge, alae and subtle mouth/chin rather than a generic smile.
 poly([(.215,10.0),(.207,9.4),(.19,8.98),(.21,8.82),(.245,8.91),(.25,9.13),(.23,9.8)],'el skin light',.074)
 line([(.218,9.80),(.21,9.30),(.198,9.04),(.21,8.94)],'el skin shadow',.025,.078)
 line([(.19,9.02),(.205,8.85),(.224,8.86),(.242,9.03)],'el skin shadow',.034,.080)
 poly([(.16,8.55),(.19,8.61),(.217,8.50),(.244,8.53),(.276,8.38),(.246,8.28),(.203,8.28),(.18,8.40)],'eb brown metal',.078)
 line([(.168,8.49),(.207,8.43),(.241,8.40),(.271,8.39)],'el skin shadow',.025,.081)
 poly([(.185,8.22),(.227,8.14),(.264,8.24),(.248,8.03),(.213,7.98)],'el skin light',.078)
 line([(.12,9.15),(.13,8.82),(.15,8.67)],'el skin shadow',.018,.080)
 for j in range(3):line([(.106,9.50-j*.08),(.13,9.44-j*.08)],'el skin shadow',.014,.080)
 p02_disc(f,L*.082,8.95,.065,.18,.082,'eb green wood',20)
 # RBG's asymmetric gold/bead collar and white lace jabot, with real layered
 # thread arcs and repeated bead strands (observed motif, not generated noise).
 poly([(.12,7.5),(.18,7.0),(.24,6.75),(.31,7.15),(.38,6.45),(.33,5.75),(.31,3.3),(.19,3.3),(.20,5.8)],'el mural cream',.073)
 poly([(.21,6.7),(.245,6.45),(.25,3.3),(.22,3.3)],'el lace shadow',.075)
 for j in range(12):
  x=.11+j*.010;line([(x,7.35-j*.018),(x+.016,6.65-j*.025),(x+.085,5.90-j*.04)],'eb gold metal',.030,.080)
  for k in range(7):
   t=k/6;xx=x+.07*t*t;yy=7.25-j*.018-t*(1.25+j*.025);p02_disc(f,xx*L,yy,.040,.045,.083,'el mural cream',12)
 for j in range(11):
  y=6.72-j*.12;line([(.27,y),(.29+j*.006,y-.25),(.32+j*.005,y-.28),(.34+j*.004,y-.04)],'store09 paper',.016,.081)
  for k in range(5):p02_ring(f,L*(.29+j*.005+k*.007),y-.12,.045,.070,.083,'store09 paper',.011,12)
 for j in range(10):line([(.20+j*.011,5.8),(.195+j*.011,4.6),(.18+j*.013,3.38)],'store09 paper',.018,.080)
 # Large shaded burgundy flowers layered across the left shoulder.
 for xx,yy,size in [(L*.07,5.65,.95),(L*.08,3.95,.55),(L*.16,4.1,.63)]:
  for j in range(16):
   ang=j*math.tau/16;dx=math.cos(ang)*size*.67;dy=math.sin(ang)*size*.67
   p02_disc(f,xx+dx,yy+dy,size*.34,size*.19,.088,'el rose paint' if j%3 else 'eb red wood',18)
   f.line((xx+dx*.3,yy+dy*.3,.091),(xx+dx*1.28,yy+dy*1.28,.091),.016,'eb brown metal')
  p02_disc(f,xx,yy,size*.24,size*.22,.094,'eb iron',20);p02_ring(f,xx,yy,size*.13,size*.12,.097,'el mural cream',.025,20)
 # Right allegorical woman: shaded hood, brows/eyes, narrow nose and closed
 # mouth, flowing drapery and a hand resting on the named book stack.
 poly([(.65,8.1),(.66,9.1),(.69,10.15),(.75,10.54),(.81,10.20),(.85,9.35),(.88,8.0)],'el lace shadow',.065)
 poly([(.68,8.35),(.69,9.25),(.715,9.88),(.76,10.22),(.80,9.83),(.82,8.90),(.80,8.15)],'el mural cream',.068)
 poly([(.715,9.72),(.75,9.88),(.785,9.58),(.795,8.98),(.777,8.54),(.75,8.40),(.723,8.73),(.71,9.2)],'eb gray stone',.071)
 poly([(.73,9.63),(.75,9.65),(.75,9.07),(.733,8.83),(.72,9.20)],'el mural cream',.073)
 for x,y in [(.731,9.40),(.773,9.32)]:
  line([(x-.014,y+.09),(x,y+.15),(x+.015,y+.05)],'el portrait hair',.025,.078);p02_disc(f,L*x,y,.040,.065,.079,'el portrait hair',14)
 line([(.751,9.4),(.748,9.05),(.763,8.99)],'el lace shadow',.025,.080)
 line([(.742,8.78),(.758,8.75),(.777,8.80)],'el portrait hair',.023,.079)
 line([(.69,8.4),(.70,9.3),(.75,10.3)],'el mural violet',.028,.078)
 poly([(.57,3.3),(.61,7.7),(.69,8.35),(.81,8.20),(.91,7.25),(.97,3.3)],'el mural cream',.069)
 for j in range(8):line([(.61+j*.035,7.65),(.60+j*.043,6.2),(.64+j*.037,4.0)],'el lace shadow',.035,.077)
 poly([(.40,7.45),(.55,7.12),(.68,6.91),(.83,7.20),(.98,8.17),(.99,7.38),(.85,6.64),(.69,6.34),(.53,6.60),(.40,6.99)],'eb red wood',.082)
 line([(.42,7.17),(.60,6.84),(.75,6.75),(.91,7.35),(.97,7.75)],'el rose paint',.055,.087)
 poly([(.80,5.2),(.83,5.6),(.86,5.48),(.90,5.22),(.94,5.10),(.93,4.87),(.88,4.94),(.85,5.10)],'el mural cream',.092)
 for j in range(4):line([(.85+j*.018,5.25),(.86+j*.018,4.99)],'el lace shadow',.018,.096)
 for j,word in enumerate(['Reed','United','Virginia','Windsor']):
  yy=4.82-j*.42;f.b(L*.87,yy,.085,L*.20,.39,.025,'el mural violet' if j%2 else 'el mural blue');et_text(f,L*.87,yy,L*.19,.24,word,'el mural cream',.105,'serif')
  for off in [-.175,.175]:f.b(L*.87,yy+off,.105,L*.20,.018,.015,'el lace shadow')
 # Fine-art brushwork and the partly eroded background collage remain limited;
 # actual apertures are reopened in el_corner above all these shallow layers.

def el_corner(b,records):
 el_shell(b,records,9.05,'eb cream brick')
 for idx,r in records:
  f=el_face(b,idx,r)
  if idx==1:
   el_skin(f,0,f.L,.17,12.5,r['wall']);el_architecture(f,r,12.5)
  else:
   
   for lo,hi in [(0,f.L*.75)]:ee_front([f.p(lo,9.05,-6.8),f.p(hi,9.05,-6.8),f.p(hi,12.5,-6.8),f.p(lo,12.5,-6.8)],r['wall'])
   xx=f.L*.75;ee_front([f.p(xx,9.05,0),f.p(xx,9.05,-6.8),f.p(xx,12.5,-6.8),f.p(xx,12.5,0)],r['wall'])
   el_skin(f,0,f.L*.75,.17,12.5,r['wall']);el_skin(f,0,f.L*.75,.17,3.35,'eb brown metal',.04);el_skin(f,f.L*.75,f.L,.17,9.05,'eb gray stone');el_mural(f)
   # Mural overlay uses opening-clipped fields; decorative polygons have their
   # own clipping in final renderer, preserving the real window apertures.
   for w in r['windows']:
    if w['at']<.75:
     # Readable opening lip above shallow mural geometry.
     ff=el_offset(f,.08);fidelity_window(ff,w)
     te_grid_glass(f,w['at']*f.L,w['bottom'],w['bottom']+w['height'],w['width']*f.L,.14,1,2,'eb sash')
   ee_escape(f,{'span':[.79,.98],'levels':[3.53,6.33],'material':'eb rust iron','dropAt':.80,'ornament':'plain'})
   x=f.L*.735;f.b(x,6.7,.38,.48,6.3,.50,'eb silver metal')
   f.line((x,3.55,.38),(x-.55,2.60,.45),.22,'eb silver metal');f.b(x-.55,2.58,.40,.48,.45,.55,'eb silver metal')
   for yy in [4.,5.3,6.6,7.9,9.2]:f.b(x,yy,.65,.53,.025,.03,'eb gray metal')
   et_text(f,f.L*.52,2.22,1.00,.17,'BOTTOMS','store09 paper',.10,'sans');et_text(f,f.L*.52,2.01,.94,.16,'UPTOWN','store09 paper',.10,'sans')
   et_text(f,f.L*.52,2.91,.90,.13,'177 1ST AVE','store09 paper',.13,'sans')
  if idx==1:
   # Tall street mass closes over the lower rear, within the same mapped owner.
   ee_front([f.p(0,12.5,0),f.p(f.L,12.5,0),f.p(f.L,12.5,-14.4),f.p(0,12.5,-14.4)],'roof')

_el_previous_render=render_building
def render_building(b):
 if b['id'] not in E11_BLOCK_IDS:return _el_previous_render(b)
 owner(str(b['id'])+' Eleventh individually observed');h=b['firstStmarksHeight'];b['renderHeight']=h
 records=[(int(i),r) for i,r in b['firstStmarksArchitecture'].items() if r.get('e11Block')]
 if b['id']==247851917:return el_court(b,records)
 if b['id']==247851941:return el_modern(b,records)
 if b['id']==247851937:return el_projected_corner(b,records)
 if b['id']==247851934:return el_school(b,records)
 if b['id']==247851936:return el_corner(b,records)
 if b['id'] in [247851925,247851926]:el_lot_mass(b,records[0][1])
 else:wall_mass(b,records[0][1]['wall'],False)
 for idx,r in records:
  f=el_face(b,idx,r);s=r['e11Block']
  if s.get('garage'):el_garage(f)
  if paint:=s.get('groundPaint'):shop09_face(f,{'paintSurround':{'bottom':.17,'top':3.65,'material':'eb '+paint}})
  el_architecture(f,r,h)
