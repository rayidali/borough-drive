"""Opt-in P03 corner anatomy; no shared-model dispatch or source-photo textures."""
for name,rgb in {'p03 red brick':(.54,.285,.205),'p03 pale stone':(.67,.63,.52),'p03 pale sash':(.68,.69,.60),
 'p03 olive sash':(.30,.34,.25),'p03 dark recess':(.075,.12,.082)}.items():material(name,rgb,.88)
for name,rgb,kind in [('p03 green metal',(.24,.38,.17),1),('p03 green highlight',(.38,.49,.25),1),
 ('p03 fascia green',(.07,.33,.23),1),('p03 canvas green',(.12,.38,.26),5),('p03 baji timber',(.14,.12,.09),2),
 ('p03 salmon letters',(.77,.28,.22),1),('p03 mural gold',(.67,.51,.23),1),('p03 mural turquoise',(.16,.56,.48),1),
 ('p03 pizza crust',(.68,.44,.19),1),('p03 pizza cheese',(.83,.67,.34),1),('p03 pizza red',(.61,.15,.075),1)]:
 material(name,rgb,.84);MATS[name]['storefront09Surface']=kind

def p03_hood(f,s,w,top,curved):
 green='p03 green metal';bright='p03 green highlight'
 for yy,ww,hh,dd in [(top+.10,w+.26,.17,.20),(top+.24,w+.39,.12,.28),(top+.31,w+.50,.055,.32)]:f.b(s,yy,dd/2,ww,hh,dd,green)
 if curved:
  # Filled segmental pediment and a second nested molding, above rectangular sash.
  for j in range(24):
   t=math.pi*j/24;u=math.pi*(j+1)/24
   face([f.p(s,top+.32,.18),f.p(s+math.cos(t)*(w+.50)/2,top+.32+math.sin(t)*.31,.18),f.p(s+math.cos(u)*(w+.50)/2,top+.32+math.sin(u)*.31,.18)],green)
  for rx,ry,d,r in [((w+.52)/2,.31,.235,.035),((w+.29)/2,.19,.26,.025)]:
   p02_curve(f,[(s+rx*math.cos(j*math.pi/28),top+.33+ry*math.sin(j*math.pi/28)) for j in range(29)],d,bright,r)
  f.b(s,top+.61,.25,.07,.10,.075,green)
 else:
  f.b(s,top+.37,.16,w+.59,.09,.35,bright)
 for dx in [-w*.42,w*.42]:f.b(s+dx,top+.03,.12,.09,.14,.16,green)

def p03_cornice(f,h):
 green='p03 green metal';bright='p03 green highlight'
 for yy,hh,dd in [(h-.98,.08,.12),(h-.84,.16,.16),(h-.66,.055,.25),(h-.40,.46,.18),(h-.12,.10,.51),(h+.01,.085,.64),(h+.10,.05,.69)]:f.strip(yy,hh,dd,green)
 f.b(f.L/2,h-.42,.194,f.L,.32,.016,'p03 dark recess')
 # Large scrolled consoles separated by rows of smaller dentils and panel borders.
 count=5 if f.L<10 else 9
 for j in range(count):
  ss=.10+(f.L-.20)*j/(count-1)
  for yy,ww,hh,dd in [(h-.68,.17,.46,.34),(h-.42,.23,.33,.44),(h-.19,.30,.16,.55)]:f.b(ss,yy,dd/2,ww,hh,dd,green)
  p02_ring(f,ss,h-.51,.071,.11,.445,bright,.017,16)
  p02_ring(f,ss,h-.30,.061,.067,.535,bright,.016,16)
  for dx in [-.12,.12]:f.b(ss+dx,h-.70,.205,.025,.22,.027,bright)
  if j<count-1:
   gap=(f.L-.20)/(count-1);mid=ss+gap/2
   shop09_frame(f,mid,h-.82,gap*.64,.18,.19,bright,.018)
   for k in range(1,max(2,int(gap/.23))):
    xx=ss+gap*k/max(2,int(gap/.23));f.b(xx,h-.31,.26,.085,.17,.25,green)
 for j in range(int(f.L/.15)):f.b((j+.5)*f.L/int(f.L/.15),h-.68,.255,.068,.072,.09,bright)

def p03_lamp(f,s,y,white=True):
 mat='store09 cream enamel' if white else 'store09 dark iron'
 rod(f.p(s,y,.04),f.p(s,y,.085),.045,mat,12)
 pts=[(s,y,.08),(s,y+.13,.18),(s,y+.32,.35),(s,y+.30,.52),(s,y+.13,.64)]
 for aa,bb in zip(pts,pts[1:]):f.line(aa,bb,.015,mat)
 # Flared hollow shade silhouette, with a pale lamp underside.
 for j in range(16):
  t=j*math.tau/16;u=(j+1)*math.tau/16
  face([f.p(s+math.cos(t)*.045,y+.15,.64+math.sin(t)*.045),f.p(s+math.cos(u)*.045,y+.15,.64+math.sin(u)*.045),f.p(s+math.cos(u)*.13,y-.04,.64+math.sin(u)*.13),f.p(s+math.cos(t)*.13,y-.04,.64+math.sin(t)*.13)],mat)
 rod(f.p(s,y-.044,.64),f.p(s,y-.034,.64),.10,'opal lamp',16)

def p03_pizza(f,s,y,r,d,heart=False):
 # Hand-built painted food motif from observed silhouette and color groups.
 def outline(radius):
  if heart:return [(s+radius*math.sin(t)**3,y+radius*(.80*math.cos(t)-.31*math.cos(2*t)-.125*math.cos(3*t)-.0625*math.cos(4*t))) for t in [j*math.tau/64 for j in range(65)]]
  return [(s+radius*math.cos(j*math.tau/64),y+radius*math.sin(j*math.tau/64)) for j in range(65)]
 p=outline(r);face([f.p(x,yy,d) for x,yy in p[:-1]],'p03 pizza cheese');face([f.p(x,yy,d) for x,yy in reversed(p[:-1])],'p03 pizza cheese')
 if not heart and r>.8:
  # The observed round wall mural is eight differently topped slices, not one uniform pizza.
  for wedge,mat in enumerate(['p03 pizza cheese','p03 pizza red','store09 cream enamel','p03 pizza cheese','p03 green metal','p03 green metal','p03 pizza cheese','p03 pizza red']):
   pts=[f.p(s,y,d+.004)]+[f.p(s+math.cos((wedge+j/10)*math.tau/8)*r*.90,y+math.sin((wedge+j/10)*math.tau/8)*r*.90,d+.004) for j in range(11)]
   face(pts,mat);face(list(reversed(pts)),mat)
 p02_curve(f,p,d+.006,'p03 pizza crust',r*.07)
 rng=random.Random(145352)
 for j in range(72 if r>.8 else 35):
  xx=(rng.random()*2-1)*r*.80;yy=(rng.random()*2-1)*r*.78
  if xx*xx+yy*yy>r*r*.64:continue
  if heart and yy>r*.47 and abs(xx)<r*.23:continue
  mat=['p03 pizza red','p03 green metal','store09 cream enamel','store09 dark iron'][j%4]
  p02_disc(f,s+xx,y+yy,r*(.044 if j%4 else .077),r*(.045 if j%4 else .068),d+.012,mat,10)
 if not heart:
  for j in range(8):
   t=j*math.tau/8;f.line((s,y,d+.016),(s+math.cos(t)*r*.91,y+math.sin(t)*r*.91,d+.016),.012,'p03 pizza crust')

def p03_stickers(f,a,b,lo,hi,d,seed,count):
 rng=random.Random(seed);colors=['store09 paper','store09 printed blue','p03 salmon letters','p03 mural gold','p03 mural turquoise']
 for j in range(count):
  ss=rng.uniform(a,b);yy=rng.uniform(lo,hi);ww=rng.uniform(.035,.095);hh=rng.uniform(.035,.11)
  if j%4==0:p02_disc(f,ss,yy,ww/2,hh/2,d,colors[j%5],8)
  else:f.b(ss,yy,d,ww,hh,.005,colors[j%5])
  if j%3==0:f.b(ss,yy,d+.005,ww*.63,.008,.005,'store09 dark iron')

def p03_tags(f,a,b,lo,hi,d,seed):
 # Unreadable source tags retained as overlapping strokes, never invented words.
 rng=random.Random(seed)
 for j in range(12):
  ss=rng.uniform(a,b-.15);yy=rng.uniform(lo,hi-.10);w=min(rng.uniform(.13,.4),b-ss);h=min(rng.uniform(.09,.25),hi-yy)
  pts=[(ss,yy),(ss+w*.2,yy+h),(ss+w*.6,yy+h*.82),(ss+w*.36,yy+h*.35),(ss+w,yy+h*.14)]
  p02_curve(f,pts,d,'store09 paper' if j%3 else 'p03 mural turquoise',.009)

def p03_skyline(f,a,b):
 rng=random.Random(145)
 for j in range(int((b-a)/.14)):
  s=a+j*.14;h=rng.uniform(.09,.35);f.b(s,.72-h/2,.126,.13,h,.007,'p03 mural gold')
  if j%4==0:f.b(s,.72+.027,.129,.024,.10,.006,'p03 mural gold')
  for yy in [.31,.41,.52]:
   if yy>.72-h:
    for dx in [-.035,.025]:f.b(s+dx,yy,.137,.017,.026,.005,'p03 pizza cheese')

def p03_table(f,s,d,red=False):
 iron='store09 dark iron';wood='store09 oak timber'
 for j in range(4):f.b(s-.285+j*.19,1.01,d,.178,.055,.60,wood)
 for dx in [-.25,.25]:
  for dd in [-.22,.22]:f.line((s+dx,.17,d+dd),(s+dx*.8,1.0,d+dd*.8),.018,iron)
 for dd in [-.22,.22]:f.line((s-.25,.43,d+dd),(s+.25,.43,d+dd),.013,iron)
 for shift in [-.51,.51]:
  ss=s+shift;mat='store09 printed red' if red and shift>0 else iron
  f.b(ss,.72,d+.21,.32,.042,.30,mat)
  for dx in [-.13,.13]:
   for dd in [-.12,.12]:f.line((ss+dx*1.25,.16,d+.21+dd*1.25),(ss+dx,.70,d+.21+dd),.014,mat)
  for dd in [-.15,.15]:f.line((ss-.16,.36,d+.21+dd),(ss+.16,.36,d+.21+dd),.011,mat)

class P03CornerRoom:
 def __init__(self,f,w):self.base=f;self.width=w
 def __getattr__(self,k):return getattr(self.base,k)
 def b(self,s,y,d,w,h,depth,mat):
  # The two corner fronts share a room; per-face back walls would cross the entry.
  if mat=='dark glass' and d<0 and abs(w-self.width)<.001:return
  return self.base.b(s,y,d,w,h,depth,mat)

_p03_previous_shop=photographed_shop
def photographed_shop(f,a,b,r):
 spec=r['design'];detail=spec.get('detailP03')
 if not detail:return _p03_previous_shop(f,a,b,r)
 kind=detail['kind'];w=b-a;c=(a+b)/2
 _p03_previous_shop(P03CornerRoom(f,w) if kind.startswith('pizza') else f,a,b,r)
 # Visible shallow room boundaries; no sky behind the recessed glass.
 if kind=='baji':
  for ss in [a+.025,b-.025]:f.b(ss,1.71,-.63,.05,3.06,1.26,'store09 dark timber')
 elif kind=='pizza-first':
  # Shared bounded dark shell; only observed shallow displays are furnished.
  f.b(c,1.71,-10.9,w,3.06,.08,'store09 dark timber')
  f.b(a,1.71,-5.45,.06,3.06,10.9,'store09 dark timber')
  f.b(c,.17,-5.45,w,.025,10.9,'store09 gray plaster')
  f.b(c,3.19,-5.45,w,.04,10.9,'store09 cream enamel')
 if kind=='baji':
  f.b(c,3.68,.065,w,.82,.16,'p03 baji timber')
  for j in range(int(w/.095)):f.b(a+j*.095,3.68,.153,.009,.79,.014,'store09 dark timber')
  ss=a+w*.78;shop09_frame(f,ss,3.70,.67,.68,.19,'p03 salmon letters',.026)
  for yy in [3.87,3.57]:sign_text(f,ss,yy,.58,'BAJI','p03 salmon letters',.32,.213,'store09:narrow')
  sign_text(f,a+w*.28,3.98,.45,'145','store09 paper',.095,.18,'store09:condensed')
  sign_text(f,a+w*.27,3.47,w*.34,'212-777-8888','store09 paper',.095,.18,'store09:condensed')
  for at in [.18,.73]:p03_lamp(f,a+w*at,4.06,False)
  # Source-defined yellow circular window graphic with small surrounding decals.
  p02_disc(f,a+w*.29,1.30,.47,.47,.061,'p03 mural gold',48)
  p02_ring(f,a+w*.29,1.30,.47,.47,.071,'p03 pizza cheese',.013,48)
  for lo,hi in [(a,a+.20),(a+w*.57,a+w*.64),(b-.16,b)]:p03_stickers(f,lo,hi,.28,2.91,.16,145+round(lo*10),90)
  p03_stickers(f,a+.20,a+w*.54,1.85,2.74,.077,351,90)
  p03_tags(f,a,b,.25,.58,.182,511);p03_tags(f,a,b,2.78,3.11,.182,610)
  # Upper small notices on the deeper door leaf and actual display layers behind.
  p03_stickers(f,a+w*.68,a+w*.94,.30,2.74,-.399,911,120)
  p03_tags(f,a+w*.68,a+w*.95,.48,1.06,-.387,711)
  for yy in [1.30,1.67,2.16]:p02_notice(f,a+w*.82,yy,.17,.21,-.40)
  for yy in [.58,1.70,2.24]:f.b(a+w*.28,yy,-.68,w*.47,.04,.38,'store09 dark timber')
  return
 # Pizza's separate sign fascia, shade, roller, arms and fabric valance.
 f.b(c,3.90,.065,w,.49,.17,'p03 fascia green')
 for yy in [3.666,4.137]:f.b(c,yy,.16,w,.025,.034,'store09 cream enamel')
 observed_awning(f,a,b,{'detail09':True,'y':3.64,'drop':.32,'depth':1.0,'valance':.20,'material':'p03 canvas green','sidePanels':False})
 for dd,yy in [(.15,3.64),(1.0,3.31)]:f.line((a,yy,dd),(b,yy,dd),.029,'store09 cream enamel')
 for ss in [a+.08,b-.08]:
  f.line((ss,3.61,.13),(ss,3.24,.53),.022,'store09 cream enamel');f.line((ss,3.24,.53),(ss,3.31,.99),.022,'store09 cream enamel')
 if kind=='pizza-first':
  sign_text(f,a+w*.59,3.89,w*.32,'PIZZA','store09 paper',.39,.167,'store09:narrow')
  sign_text(f,a+w*.245,3.95,w*.29,'EAST VILLAGE','store09 paper',.13,.168,'store09:condensed')
  sign_text(f,a+w*.87,4.02,w*.24,'212-529-4545','store09 paper',.093,.168,'store09:condensed')
  sign_text(f,a+w*.58,3.215,w*.42,'EAST VILLAGE PIZZA','store09 paper',.16,1.14,'store09:condensed')
  sign_text(f,a+w*.18,3.205,w*.30,'212-529-4545','store09 paper',.092,1.14,'store09:condensed')
  sign_text(f,b-.17,3.205,.22,'145','store09 paper',.102,1.14,'store09:bold')
  for at in [.08,.48,.89]:p03_lamp(f,a+w*at,4.42)
  sign_text(f,a+w*.40,2.77,w*.23,'PIZZA','p02 green tube',.20,.078,'store09:serif')
  ss=a+w*.83;p02_notice(f,ss,2.10,.23,.29,-.19)
  sign_text(f,ss,2.10,.19,'A','store09 printed blue',.20,-.176,'store09:bold')
  p03_stickers(f,ss-.14,ss+.14,.46,1.76,-.185,543,28)
  p03_tags(f,a+.06,a+w*.67,.25,.64,.156,411)
  shop09_ink(f,a+w*.26,a+w*.67,.22,.70,'store09 paper',.16,'bubble',fill='store09 black enamel')
  # A shallow stainless slice counter with trays behind the broad display.
  shop09_display(f,a,a+w*.70,.16,3.27,{'kind':'counter','at':.5,'y':.92,'width':.91,'depth':-.66,'material':'store09 brushed steel'})
  for ss in [a+w*.15,a+w*.40]:
   f.b(ss,1.13,-.52,.61,.025,.45,'store09 brushed steel')
   rod(f.p(ss,1.15,-.52),f.p(ss,1.18,-.52),.23,'p03 pizza crust',32)
   rod(f.p(ss,1.18,-.52),f.p(ss,1.193,-.52),.205,'p03 pizza cheese',32)
   for dx,dd in [(-.09,-.07),(.08,.08),(.04,-.1)]:rod(f.p(ss+dx,1.195,-.52+dd),f.p(ss+dx,1.202,-.52+dd),.035,'p03 pizza red',12)
  for ss in [a+w*.06,a+w*.66]:f.b(ss,1.43,-.47,.025,.59,.025,'store09 brushed steel')
  f.b(a+w*.36,1.73,-.47,w*.61,.025,.48,'store09 brushed steel')
  f.b(a+w*.36,1.43,-.225,w*.61,.55,.015,'store09 clear glass')
  # Pier is painted as a tower rather than a plain shared shop post.
  ss=b+.045
  for yy,hh,mat in [(.55,.73,'p03 baji timber'),(1.19,.54,'store09 cream enamel'),(1.83,.73,'p03 mural turquoise'),(2.50,.49,'p03 mural turquoise')]:f.b(ss,yy,.145,.29,hh,.035,mat)
  for j in range(3):
   for yy in [.38,.97,1.57,2.16,2.53]:
    xx=ss-.10+j*.10;f.b(xx,yy,.168,.045,.28,.009,'p03 dark recess');p02_curve(f,[(xx-.025,yy+.14),(xx,yy+.18),(xx+.025,yy+.14)],.178,'store09 cream enamel',.007)
 else:
  sign_text(f,a+w*.11,3.95,w*.15,'PIZZA','store09 paper',.23,.168,'store09:narrow')
  sign_text(f,a+w*.32,3.90,w*.29,'eastvillagepizza.net','store09 paper',.19,.168,'store09:condensed')
  sign_text(f,a+w*.64,3.99,w*.20,'EAST VILLAGE','store09 paper',.17,.168,'store09:condensed')
  sign_text(f,a+w*.83,3.89,w*.27,'PIZZA','store09 paper',.44,.168,'store09:narrow')
  sign_text(f,a+w*.23,3.17,w*.34,'212-529-4545','store09 paper',.20,1.14,'store09:condensed')
  sign_text(f,a+w*.74,3.17,w*.35,'EAST VILLAGE PIZZA','store09 paper',.17,1.14,'store09:condensed')
  for at in [.04,.22,.40,.58,.77,.96]:p03_lamp(f,a+w*at,4.43)
  p03_skyline(f,a+.05,b-.06)
  ss=a+w*.16;p02_ring(f,ss,2.20,.40,.47,.12,'p02 blue tube',.010,48)
  for text,yy,mat in [('East',2.43,'p02 red tube'),('Village',2.20,'p02 green tube'),('Pizza',1.98,'p02 red tube')]:sign_text(f,ss,yy,.72,text,mat,.205,.132,'store09:script')
  p03_pizza(f,a+w*.50,1.75,.65,.09,True)
  ss=a+w*.84;p02_curve(f,[(ss-.32,2.47),(ss+.28,2.26),(ss-.25,1.92),(ss-.32,2.47)],.12,'p02 yellow tube',.016)
  for xx,yy in [(ss-.15,2.34),(ss+.07,2.24),(ss-.16,2.13)]:p02_ring(f,xx,yy,.045,.047,.134,'p02 red tube',.009,14)
  for at in [.13,.48,.83]:
   shop09_display(f,a,b,.16,3.27,{'kind':'counter','at':at,'y':.91,'width':.27,'depth':-.67,'material':'store09 brushed steel'})
   p03_table(f,a+w*at,.71,at==.83)
  for at in [.07,.30,.60,.92]:p02_notice(f,a+w*at,2.57,.18,.24,.084)
  # Ceiling light, menu panels and display shelf legs anchor the visible room depth.
  for at in [.15,.50,.85]:
   f.b(a+w*at,3.07,-.85,w*.16,.035,.12,'opal lamp')
   f.b(a+w*at,2.41,-1.06,w*.20,.47,.035,'store09 paper')
   for j in range(6):f.b(a+w*at,2.56-j*.06,-1.035,w*.165,.012,.005,'p03 pizza red' if j==0 else 'store09 dark iron')
   for dx in [-w*.10,w*.10]:f.b(a+w*at+dx,.49,-.68,.035,.72,.035,'store09 brushed steel')
  # Unequal stacked trays and service shelving visible through the windows.
  for j in range(6):f.b(a+w*.67,1.15+j*.12,-.78,.75-j*.05,.045,.35,'store09 paper')

_p03_previous_render=render_building
def render_building(b):
 if b['id']!=241822237:return _p03_previous_render(b)
 b['renderHeight']=b['firstStmarksHeight'];h=b['renderHeight'];owner('145 First / 352 Ninth P03 dated observed corner')
 wall_mass(b,'p03 red brick',False)
 for index in [1,0]:
  r=b['firstStmarksArchitecture'][str(index)];v=b['frontages'][index];f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']);f.wall=r['wall']
  fidelity_elevation({**b,'businesses':[],'seventhArchitecture':r},f,r)
  shop09_face(f,{'paintSurround':{'bottom':.17,'top':3.28,'material':'store09 black enamel'}})
  p03_cornice(f,h)
  for i,win in enumerate(r['windows']):
   if win.get('p03Plain'):continue
   ss=win['at']*f.L;ww=win['width']*f.L;y=win['bottom'];top=y+win['height']
   p03_hood(f,ss,ww,top,win['p03Pediment'])
   for dx in ([] if win['p03Pediment'] else [-ww*.44,ww*.44]):f.b(ss+dx,y-.16,.14,.105,.21,.19,'p03 green metal')
   for xx in [ss-ww/2+.07,ss+ww/2-.07]:f.b(xx,y+win['height']/2,-.086,.012,win['height']-.12,.018,'p03 pale sash')
   # Dated blinds vary by observed lower/upper panes, not randomized window types.
   drop=([.63,.82,.35,.68,.25,.40,.55,.25,.47,.32,.53,.25,.20,.35,.50,.27] if index==1 else [.49,.76,.45,.30,.39,.27,.48,.22])[i]
   for j in range(int(win['height']*drop/.055)):f.b(ss,top-.06-j*.055,-.13,ww-.13,.021,.010,'store09 cream canvas')
  if index==1:
   for ss,y in [(1.82,4.63),(3.72,7.32),(5.61,7.31),(6.17,12.87)]:
    rod(f.p(ss,y,.08),f.p(ss,y,.145),.092,'store09 cream enamel',20)
   f.line((.17,3.99,.055),(.17,h-.95,.055),.009,'p03 olive sash')
  else:
   # Small paired-window landing and drop only, not a full-height escape preset.
   p02_escape(f,{'span':[(10.60-.59)/f.L,(10.60+.59)/f.L],'levels':[3.98],'material':'p03 green metal','dropAt':10.60/f.L})
   for xx in [10.25,10.95]:f.line((xx,4.03,.94),(xx,8.34,.94),.019,'p03 green metal')
   for j in range(17):f.line((10.25,4.05+j*.25,.94),(10.95,4.05+j*.25,.94),.014,'p03 green metal')
   # Painted service field/mural and louvers, separated from the residential leaf.
   p03_pizza(f,14.38,1.57,1.12,.125)
   letters='east village pizza'
   for j,ch in enumerate(letters):
    if ch==' ':continue
    t=math.pi*.92-j/(len(letters)-1)*math.pi*.84
    sign_text(f,14.38+math.cos(t)*1.50,1.74+math.sin(t)*1.40,.26,ch,'p03 mural gold' if j%3 else 'p03 salmon letters',.29,.142,'store09:serif')
   f.b(14.38,2.62,.16,1.21,.50,.19,'store09 dark iron')
   for j in range(7):f.b(14.38,2.43+j*.061,.273,1.12,.025,.034,'p03 olive sash')
   f.line((11.48,3.76,.09),(19.85,3.76,.09),.012,'store09 dark iron')
   for ss in [12.02,18.20]:f.line((ss,3.76,.09),(ss,4.40,.09),.009,'store09 cream enamel');p03_lamp(f,ss,4.39)
   ss=18.79
   f.b(ss,.19,.31,1.28,.14,.61,'p03 pale stone')
   sign_text(f,ss+.625,2.47,.21,'352','store09 paper',.113,.19,'store09:condensed')
   f.b(ss-.68,1.39,.20,.11,.21,.035,'store09 brushed steel')
   for j in range(6):f.b(ss-.68,1.32+j*.026,.223,.05,.009,.006,'store09 dark iron')
   p02_notice(f,ss,1.71,.26,.36,-.13)
   for xx in [ss-.43,ss+.43]:f.b(xx,1.48,-.14,.025,2.31,.026,'store09 brushed steel')
   for yy in [.43,1.18,2.59]:f.b(ss,yy,-.14,.91,.023,.026,'store09 brushed steel')
   f.b(ss,2.91,-.12,1.01,.48,.015,'store09 clear glass')
   f.line((19.82,.21,.13),(19.82,5.70,.13),.045,'p03 olive sash')
   p02_curve(f,[(19.82,5.70),(19.72,5.83),(19.54,5.83)],.13,'p03 olive sash',.045)
