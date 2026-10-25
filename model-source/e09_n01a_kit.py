"""N01A-only authored anatomy. No shared recipe behavior or photographic textures."""
N01A_IDS={247852691,247852690,247852697,247852689}
for name,rgb in {'n01 realty red brick':(.53,.29,.225),'n01 residential red brick':(.54,.305,.25),'n01 immigrant red brick':(.56,.28,.19),
 'painted n01 sky':(.27,.45,.61),'painted n01 cloud':(.58,.66,.69),'painted n01 yellow':(.62,.57,.39),'painted n01 pink':(.52,.34,.37),'painted n01 green':(.31,.43,.34),
 'painted n01 tag':(.14,.15,.17),'painted n01 outline':(.76,.75,.65),'n01 cream stone':(.71,.69,.60),'n01 olive stone':(.38,.39,.32),'n01 dark sash':(.18,.22,.19),'n01 white sash':(.77,.78,.71),'n01 black metal':(.09,.105,.105),'n01 rust iron':(.38,.19,.14)}.items():material(name,rgb,.87)
for name,rgb,kind in [('n01 navy canvas',(.035,.09,.22),5),('n01 navy enamel',(.035,.075,.18),1),('n01 gold letters',(.80,.60,.27),1),('n01 black timber',(.065,.075,.073),2),('n01 brown timber',(.32,.20,.12),2),('n01 shelter timber',(.36,.235,.14),2),('n01 taupe metal',(.43,.44,.39),6),('n01 duct metal',(.46,.48,.47),6),('n01 blue curtain',(.075,.24,.58),5),('n01 food green',(.35,.49,.16),1),('n01 food orange',(.89,.40,.08),1),('n01 food yellow',(.86,.67,.18),1),('n01 food red',(.65,.16,.07),1),('n01 food cream',(.84,.74,.49),1)]:
 material(name,rgb,.85);MATS[name]['storefront09Surface']=kind

def n01_center_text(obj,f,s,y,d):
 cx=(max(v[0] for v in obj.bound_box)+min(v[0] for v in obj.bound_box))/2
 cy=(max(v[1] for v in obj.bound_box)+min(v[1] for v in obj.bound_box))/2
 x,yy,z=f.p(s,y,d);obj.location=Vector((x,-z,yy))-obj.rotation_euler.to_matrix()@Vector((cx*obj.scale.x,cy*obj.scale.y,0))

def n01_text(f,s,y,w,h,text,mat,d,font='serif',heavy=False):
 obj=sign_text(f,s,y,w,text,mat,1.0,d,'store09:'+font)
 bpy.context.view_layer.update()
 width=max(v[0] for v in obj.bound_box)-min(v[0] for v in obj.bound_box)
 height=max(v[1] for v in obj.bound_box)-min(v[1] for v in obj.bound_box)
 obj.scale.x=w/max(.001,width);obj.scale.y=h/max(.001,height)
 if heavy:obj.data.bevel_depth=.016;obj.data.bevel_resolution=0
 n01_center_text(obj,f,s,y,d)
 return obj

def n01_cornice(f,h,bid):
 mat='n01 black metal';count=5 if bid==247852697 else 7 if bid==247852690 else 5
 for yy,hh,dd in [(h-.80,.10,.14),(h-.48,.50,.20),(h-.16,.11,.44),(h+.02,.12,.62),(h+.11,.06,.67)]:f.strip(yy,hh,dd,mat)
 for j in range(count):
  ss=.18+(f.L-.36)*j/(count-1)
  for yy,w,hh,d in [(h-.60,.14,.38,.31),(h-.39,.21,.27,.44),(h-.20,.29,.13,.54)]:f.b(ss,yy,d/2,w,hh,d,mat)
  p02_ring(f,ss,h-.47,.067,.10,.43,mat,.02,14)
  if j<count-1:
   gap=(f.L-.36)/(count-1);shop09_frame(f,ss+gap/2,h-.49,gap*.75,.33,.223,mat,.032)
   if bid==247852690:
    for k in range(5):f.b(ss+gap*(k+.5)/5,h-.74,.17,.09,.08,.11,'n01 cream stone')

def n01_hood(f,w,curved=False):
 ss=w['at']*f.L;ww=w['width']*f.L;top=w['bottom']+w['height'];mat=w['trim']
 if curved:
  for j in range(25):
   xx=ss-ww*.65+ww*1.3*j/24;rise=.14*math.sqrt(max(0,1-((xx-ss)/(ww*.65))**2))
   f.b(xx,top+.12+rise/2,.135,ww*1.3/24+.003,.16+rise,.26,mat)
  fidelity_arc(f,ss,top+.20,ww*.64,.14,.285,.028,mat,24)
  for dx in [-ww*.62,ww*.62]:
   f.b(ss+dx,top+.16,.16,.13,.22,.23,mat)
   for k in [-1,0,1]:f.b(ss+dx+k*.028,top+.12,.292,.012,.15,.015,'n01 dark sash')
  p02_ring(f,ss,top+.39,.044,.060,.09,mat,.016,16)
 else:
  for yy,hh,wide,dd in [(top+.09,.15,ww+.23,.20),(top+.205,.075,ww+.34,.26)]:f.b(ss,yy,dd/2,wide,hh,dd,mat)
  for dx in [-ww*.42,ww*.42]:f.b(ss+dx,w['bottom']-.14,.11,.11,.18,.20,mat)

def n01_wall_mural(f,h):
 # Hand-authored color regions laid in brick-sized cells, clipped to real openings.
 # They approximate the observed mural, never claim exact proprietary artwork.
 holes=OPENINGS[frontage_key(f)];dx=.215;dy=.072
 for row in range(int((h-3.45)/dy)+1):
  y=3.45+(row+.5)*dy
  for col in range(int(f.L/dx)+1):
   x=(col+.5)*dx+(row%2)*dx/2
   if x>f.L-.02:continue
   color='painted n01 yellow' if x<7.9 else 'painted n01 sky'
   if 7.9<x<10.0:color='painted n01 pink'
   # Long cloud shapes and painted architecture visible in May 2024.
   if x>9.9 and ((x-13.3)/5.6)**2+((y-11.40)/.45)**2<1:color='painted n01 cloud'
   if x>10 and ((x-16)/5.6)**2+((y-8.75)/.57)**2<1:color='painted n01 cloud'
   if 5.3<x<10.9 and y<5.2+(.7 if 7.4<x<8.5 else 0):color='painted n01 green' if x<7.5 else 'painted n01 pink'
   if 1<x<7.4 and 3.7<y<4.0+.18*math.sin(x*2.2):color='painted n01 pink'
   if 10.1<x<17.0 and 7.75<y<10.2:
    t=(x-10.1)%1.35
    in_stroke=(t<.23 or .64<t<.88 or abs(y-(8.2+(x%1.35)*1.3))<.16)
    outline=(t<.33 or .54<t<.98 or abs(y-(8.2+(x%1.35)*1.3))<.26)
    if outline:color='painted n01 outline'
    if in_stroke:color='painted n01 tag'
   fidelity_clipped_surface(f,max(0,x-dx/2),min(f.L,x+dx/2),y-dy/2,min(h,y+dy/2),.010,.007,color,.002)

def n01_food(f,s,y,w,h,kind,seed):
 rng=random.Random(seed);d=.087
 f.b(s,y,d,w,h,.012,'n01 black timber')
 if kind=='juice':
  sign_text(f,s,y+h*.38,w*.80,'JUICES','store09 paper',.22,d+.016,'store09:serif')
  for j,col in enumerate(['n01 food yellow','n01 food orange','n01 food cream']):
   xx=s+(j-1)*w*.27;f.b(xx,y+.04,d+.018,w*.20,h*.45,.008,col)
   p02_disc(f,xx,y+h*.25,w*.10,.035,d+.022,'store09 paper',20)
   f.line((xx+.03,y+.20,d+.024),(xx+.09,y+h*.34,d+.024),.009,'store09 paper')
  for j in range(7):p02_disc(f,s-w*.40+j*w*.12,y-h*.30,w*.08,h*.09,d+.025,['n01 food green','n01 food orange','n01 food yellow'][j%3],16)
 elif kind=='coffee':
  sign_text(f,s,y+h*.37,w*.90,'HOT & COLD','store09 paper',.13,d+.02,'store09:serif');sign_text(f,s,y+h*.27,w*.8,'COFFEE','store09 paper',.17,d+.02,'store09:serif')
  for j in range(2):
   xx=s+(j-.5)*w*.41;f.b(xx,y-h*.08,d+.02,w*.30,h*.45,.01,'n01 food cream' if j==0 else 'n01 brown timber')
   for yy in [y+h*.15,y-h*.31]:p02_disc(f,xx,yy,w*.155,.045,d+.035,'store09 paper',18)
   p02_ring(f,xx+w*.20,y-.02,w*.08,h*.10,d+.028,'store09 paper',.013,16)
 elif kind=='salad':
  # One broad bowl with smaller side dishes: distinct from the sandwich collage.
  for j,(xx,yy,rx,ry) in enumerate([(s,y-.25,w*.42,h*.17),(s-w*.21,y+h*.30,w*.20,h*.10),(s+w*.24,y+h*.23,w*.19,h*.09)]):
   p02_disc(f,xx,yy,rx,ry,d+.024,'store09 paper',40)
   p02_disc(f,xx,yy+.025,rx*.87,ry*.78,d+.030,'n01 food green',32)
   for k in range(46 if j==0 else 19):
    t=rng.random()*math.tau;rad=math.sqrt(rng.random())*.88
    x=xx+math.cos(t)*rx*rad;z=yy+math.sin(t)*ry*rad
    p02_disc(f,x,z,w*.023,h*.018,d+.04,['n01 food green','n01 food red','n01 food cream','n01 food yellow'][k%4],9)
 elif kind in ['burger','sandwich']:
  for j in range(2):
   yy=y+h*(.20-j*.44);xx=s+(-.05 if j==0 else .07)*w
   p02_disc(f,xx,yy-h*.105,w*.40,h*.065,d+.025,'store09 paper',36)
   for k,col in enumerate(['n01 food cream','n01 brown timber','n01 food green','n01 food red','n01 food yellow']):
    p02_disc(f,xx,yy-h*.06+k*h*.037,w*(.32 if kind=='burger' else .36),h*.048,d+.032+k*.002,col,32)
   p02_disc(f,xx,yy+h*.16,w*.32,h*(.09 if kind=='burger' else .053),d+.045,'n01 food cream',36)
   for k in range(16):
    x=xx+rng.uniform(-w*.26,w*.26);z=yy+h*.16+rng.uniform(-h*.04,h*.04)
    f.b(x,z,d+.053,w*.012,h*.005,.004,'n01 food yellow')
   for k in range(8):
    x=xx-w*.31+k*w*.085
    p02_disc(f,x,yy+h*.04,w*.055,h*.025,d+.048,'n01 food green',8)
 else:
  # Different bowls, leafy salads and layered sandwiches rather than repeated food icons.
  for j in range(3):
   yy=y+h*(.26-j*.26);xx=s+(-.10 if j%2 else .08)*w
   p02_disc(f,xx,yy,w*.39,h*.105,d+.025,'store09 paper',32)
   if (j+seed)%2:
    for k in range(22):
     x=xx+rng.uniform(-w*.30,w*.30);z=yy+rng.uniform(-h*.075,h*.075)
     p02_disc(f,x,z,w*.032,h*.028,d+.035,['n01 food green','n01 food red','n01 food yellow'][k%3],8)
   else:
    for k,col in enumerate(['n01 food cream','n01 food green','n01 food red','n01 brown timber','n01 food cream']):
     p02_disc(f,xx,yy-.06+k*.03,w*.28,h*.028,d+.034+k*.001,col,20)

def n01_arch_letters(f,text,s,y,width,d):
 for j,ch in enumerate(text):
  x=(j-(len(text)-1)/2)*width/len(text);yy=y+.14*(1-(x/(width/2))**2)
  if ch!=' ':sign_text(f,s+x,yy,width/len(text)*.98,ch,'n01 gold letters',.18,d,'store09:serif')

def n01_bottles(f,a,b):
 for yy in [.98,1.48]:
  f.b((a+b)/2,yy,-.55,b-a,.045,.28,'n01 brown timber')
  for j in range(10):
   ss=a+(b-a)*(j+.5)/10
   f.b(ss,yy+.13,-.60,.060,.20,.065,'painted n01 green' if j%3 else 'n01 brown timber')
   f.b(ss,yy+.255,-.60,.025,.08,.028,'n01 black timber')
   f.b(ss,yy+.13,-.561,.042,.07,.008,'store09 paper')

_n01_previous_shop=photographed_shop
def photographed_shop(f,a,b,r):
 detail=r['design'].get('detailN01A')
 if not detail:return _n01_previous_shop(f,a,b,r)
 _n01_previous_shop(f,a,b,r);kind=detail['kind'];w=b-a;c=(a+b)/2
 # Close the shallow visible display room independently for each observed unit.
 f.b(c,1.56,-.91,w,2.78,.05,'n01 black timber')
 for ss in [a+.03,b-.03]:f.b(ss,1.56,-.45,.05,2.78,.92,'n01 black timber')
 if kind=='hotel':
  left=a+w*.28;right=b-.11
  for j in range(64):
   ss=left+(right-left)*(j+.5)/64;f.b(ss,1.65,-.12,(right-left)/64+.002,2.70,.025,'n01 blue curtain' if j%3 else 'n01 navy canvas')
  n01_text(f,(left+right)/2,2.05,w*.38,.44,'evh','store09 paper',.059,'bold')
  n01_text(f,a+w*.13,3.29,.30,.12,'147','store09 paper',.18,'bold')
  p02_notice(f,a+w*.15,1.68,.12,.17,-.18)
 elif kind=='market':
  edges=[0,.13,.26,.37,.57,.75,1]
  for j in range(5):
   lo=a+w*edges[j]+.10;hi=a+w*edges[j+1]-.12
   n01_food(f,(lo+hi)/2,1.70,hi-lo,2.64,['salad','juice','coffee','burger','sandwich'][j],j+147)
  lo=a+w*.75;hi=b
  f.b((lo+hi)/2,3.52,.095,hi-lo,.44,.17,'n01 black timber')
  n01_text(f,(lo+hi)/2,3.52,(hi-lo)*.87,.29,'MARKET PLACE','store09 paper',.185,'bold')
  p02_disc(f,a+w*.47,2.82,w*.095,.28,.13,'n01 food cream',48)
  n01_text(f,a+w*.47,2.86,w*.165,.21,'Sweet Village','n01 brown timber',.146,'script')
  sign_text(f,a+w*.47,2.67,w*.13,'MARKET PLACE','n01 brown timber',.07,.148,'store09:serif')
  n01_food(f,(lo+hi)/2,.75,(hi-lo)*.86,1.06,'sandwich',151)
  p02_ring(f,lo+(hi-lo)*.31,2.24,.39,.45,.082,'store09 paper',.015,48)
  sign_text(f,lo+(hi-lo)*.31,2.20,.55,'OPEN','store09 paper',.13,.105,'store09:narrow')
  sign_text(f,lo+(hi-lo)*.73,2.46,.91,'Modelo','n01 gold letters',.18,.106,'store09:serif')
  for at in edges[1:-1]:p03_tags(f,a+w*at-.075,a+w*at+.12,.55,3.15,.148,round(at*1000))
  for ss in [a+.1,b-.1]:f.line((ss,.19,.13),(ss,3.55,.13),.022,'n01 black metal')
 elif kind=='realty':
  observed_awning(f,a,b,{'detail09':True,'y':3.30,'drop':.47,'depth':1.12,'valance':.24,'material':'n01 navy canvas','sidePanels':True})
  sign_text(f,c,2.71,w*.95,'345  SALES • RENTALS • CONSTRUCTION • MANAGEMENT  (212) 518-7070','store09 paper',.20,1.245,'store09:serif')
  # Main lettering on the visible vertical front of the observed inclined canopy.
  obj=n01_text(f,c,3.055,w*.91,.30,'UNIVERSAL REALTY GROUP','store09 paper',.10+(3.30-3.055)/.47*1.12+.014,'serif',True)
  slope=math.atan2(.47,1.12);cs=math.cos(slope);sn=math.sin(slope)
  obj.rotation_euler=Matrix((Vector((f.rx,-f.rz,0)),Vector((-f.nx*cs,f.nz*cs,sn)),Vector((f.nx*sn,-f.nz*sn,cs)))).transposed().to_euler()
  obj.scale.y/=sn
  n01_center_text(obj,f,c,3.055,.10+(3.30-3.055)/.47*1.12+.014)
  sign_text(f,a+w*.77,3.19,w*.35,'www.urgny.com','store09 paper',.10,.49,'store09:serif')
  for at in [.59,.82]:
   for row in range(3):
    for col in range(2):p02_notice(f,a+w*at+(col-.5)*.27,.93+row*.32,.22,.28,-.065)
  for j in range(22):f.b(a+w*.34,2.53-j*.045,-.13,w*.25,.019,.012,'store09 cream canvas')
  f.b(a+w*.57,2.40,.06,.64,.34,.34,'n01 taupe metal')
  for j in range(5):f.b(a+w*.57,2.27+j*.054,.245,.54,.012,.013,'n01 black metal')
  # Ramp rises toward the west glazing; narrow rail follows its actual incline.
  for j in range(32):
   ss=a+w*(j+.5)/32;h=.29*(1-j/32)+.02;f.b(ss,.17+h/2,.57,w/32+.004,h,1.12,'n01 cream stone')
  f.line((a+.08,1.29,1.12),(b-.10,1.01,1.12),.018,'n01 taupe metal')
  for j in range(5):
   ss=a+.10+(w-.20)*j/4;hh=1.29-.28*j/4;f.line((ss,.17+.29*(1-j/4),1.12),(ss,hh,1.12),.014,'n01 taupe metal')
  sign_text(f,b-.26,1.92,.44,'UNIVERSAL','store09 paper',.075,.083,'store09:condensed')
  sign_text(f,b-.26,1.79,.44,'REALTY','store09 paper',.09,.083,'store09:condensed')
 else:
  # Tap and wine each keep their own shade, panes and warm shallow display.
  if kind=='tap':
   for lo,hi in [(a,a+w*.69),(a+w*.70,b)]:observed_awning(f,lo,hi,{'detail09':True,'y':3.17,'drop':.20,'depth':.59,'valance':.12,'material':'n01 navy canvas','sidePanels':True})
   n01_arch_letters(f,'TAP ROOM',a+w*.35,2.12,w*.55,.085)
   for at in [.19,.42]:
    p02_ring(f,a+w*at,1.44,.13,.18,-.22,'n01 gold letters',.012,24)
    f.b(a+w*at,1.02,-.39,.19,.37,.17,'n01 brown timber')
  else:
   observed_awning(f,a,b,{'detail09':True,'y':3.17,'drop':.20,'depth':.62,'valance':.12,'material':'n01 navy canvas','sidePanels':True})
   n01_arch_letters(f,'WINE BAR',a+w*.66,2.12,w*.55,.085);n01_bottles(f,a+w*.37,b-.17)
  for yy in [.31,.65]:f.b(c,yy,.10,w-.10,.025,.055,'n01 navy enamel')
  f.b(c,.46,.065,w-.10,.30,.025,'n01 navy enamel')
  p02_notice(f,a+w*(.83 if kind=='tap' else .14),1.51,.10,.15,-.165)

def n01_shelter(f):
 a=.18;b=f.L-.16;wood='n01 shelter timber';black='n01 black timber';near=3.07;far=5.04
 # Dated September 2024 curbside enclosure, modeled without hiding sidewalk access.
 for d in [near,far]:
  f.b((a+b)/2,.68,d,b-a,.99,.085,wood)
  for j in range(5):
   ss=a+(b-a)*j/4;f.b(ss,1.49,d,.10,2.61,.12,wood)
   if j<4:
    mid=ss+(b-a)/8;ww=(b-a)/4-.12
    shop09_arch(FidelityProjectedFacade(f,d),mid-ww/2,mid+ww/2,1.22,2.60,0,'store09 clear glass',wood)
  for yy in [1.14,2.66]:f.b((a+b)/2,yy,d,b-a,.09,.12,wood)
  for j in range(26):
   ss=a+(b-a)*(j+.5)/26
   f.b(ss,1.12,d+.068,(b-a)/26,.047,.009,'store09 cream enamel' if j%2 else 'store09 printed red')
 for ss in [a,b]:
  f.b(ss,.68,(near+far)/2,.085,.99,far-near,wood)
  f.b(ss,2.67,(near+far)/2,.11,.10,far-near,wood)
 f.b((a+b)/2,2.82,(near+far)/2,b-a+.18,.09,far-near+.21,black)
 for j in range(21):p02_ring(f,a+j*(b-a)/20,2.77,.028,.028,far+.10,'n01 taupe metal',.008,12)
 for ss in [a+.90,a+2.75,a+4.65]:
  for k in range(32):
   t=k*math.tau/32;u=(k+1)*math.tau/32
   face([f.p(ss,1.03,4.1),f.p(ss+math.cos(t)*.36,1.03,4.1+math.sin(t)*.36),f.p(ss+math.cos(u)*.36,1.03,4.1+math.sin(u)*.36)],wood)
  for dx in [-.25,.25]:f.line((ss+dx,.19,4.1),(ss+dx*.75,1.02,4.1),.019,'n01 black metal')
  for dd in [-.57,.57]:
   f.b(ss,.64,4.1+dd,.37,.05,.37,black)
   for dx in [-.14,.14]:
    for dz in [-.14,.14]:f.line((ss+dx,.19,4.1+dd+dz),(ss+dx,.62,4.1+dd+dz),.013,'n01 black metal')
   f.b(ss,1.01,4.1+dd+(.17 if dd>0 else -.17),.36,.42,.042,black)
 for ss in [a+.28,b-.28]:
  f.b(ss,.55,near+.22,.32,.58,.32,'n01 brown timber')
  for j in range(12):
   t=j*math.tau/12;f.line((ss,.75,near+.22),(ss+math.cos(t)*.34,1.25+.15*math.sin(t),near+.22+math.sin(t)*.30),.021,'n01 food green')
 # Small orange end barrier retained as dated movable context.
 f.b(b+.33,.63,4.12,.22,.91,1.55,'n01 food orange')
 for yy in [.42,.74]:f.b(b+.45,yy,4.12,.035,.05,1.35,'store09 paper')

_n01_previous_render=render_building
def render_building(b):
 if b['id'] not in N01A_IDS:return _n01_previous_render(b)
 bid=b['id'];index=1 if bid==247852691 else 0;r=b['firstStmarksArchitecture'][str(index)]
 b['renderHeight']=b['firstStmarksHeight'];h=b['renderHeight'];owner(str(bid)+' N01A observed Ninth frontage')
 wall_mass(b,r['wall'],False)
 v=b['frontages'][index];f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']);f.wall=r['wall']
 fidelity_elevation({**b,'businesses':[],'seventhArchitecture':r},f,r)
 if bid==247852691:
  n01_wall_mural(f,h)
  for span,reverse in [([.085,.335],True),([.49,.715],False)]:p02_escape(f,{'span':span,'levels':[4.18,6.75,9.28],'material':'n01 black metal','reverse':reverse,'dropAt':span[0]+.02})
  for win in r['windows']:
   ss=win['at']*f.L;ww=win['width']*f.L;y=win['bottom']
   for dx in [-ww/6,ww/6]:f.b(ss+dx,y+1.28,-.07,.018,.80,.021,'n01 black metal')
   for yy in [y+.94,y+1.20,y+1.47]:f.b(ss,yy,-.066,ww,.018,.021,'n01 black metal')
   f.b(ss,y-.30,.13,ww*.60,.36,.22,'n01 black metal')
   for j in range(5):f.b(ss,y-.44+j*.065,.252,ww*.54,.018,.012,'n01 taupe metal')
  ss=16.99
  f.b(ss,8.0,.45,.49,8.8,.62,'n01 duct metal');f.b(ss+.48,12.31,.45,1.38,.53,.62,'n01 duct metal')
  for yy in [4.35,6.5,8.7,10.9,12.28]:f.b(ss,yy,.775,.55,.035,.018,'n01 taupe metal')
  p02_disc(f,ss,3.88,.46,.46,.82,'n01 black metal',48);p02_ring(f,ss,3.88,.44,.44,.85,'n01 duct metal',.055,40)
  for k in range(12):
   t=k*math.tau/12;f.line((ss,3.88,.865),(ss+math.cos(t)*.39,3.88+math.sin(t)*.39,.865),.014,'n01 duct metal')
  shop09_face(f,{'paintSurround':{'bottom':.17,'top':3.50,'material':'n01 black timber'}})
  for ss in [3.9,9.2,16.6,20.9]:p03_tags(f,ss-.09,ss+.10,.28,3.20,.10,round(ss*100))
  # Low cellar covers in front of poster wall, separate seams/hinges.
  for ss in [11.7,12.5]:
   f.b(ss,.22,.49,.73,.11,.89,'n01 black metal')
   for dx in [-.25,.25]:f.b(ss+dx,.286,.23,.11,.02,.05,'n01 taupe metal')
 else:
  n01_cornice(f,h,bid)
  for win in r['windows']:
   if win.get('n01Head'):n01_hood(f,win,win['n01Head']=='arch')
   if win.get('n01Vent'):
    ss=win['at']*f.L;yy=win['bottom']-.30;f.b(ss,yy,.07,.51,.30,.11,'n01 black metal')
    for j in range(4):f.b(ss,yy-.10+j*.06,.135,.45,.018,.018,'n01 taupe metal')
   if win['bottom']>1.5:
    ss=win['at']*f.L;ww=win['width']*f.L;top=win['bottom']+win['height']
    count=round(win['height']*([.30,.61,.43,.18][round(win['bottom'])%4])/.062)
    for j in range(count):f.b(ss,top-.07-j*.062,-.125,ww-.11,.023,.01,'store09 cream canvas')
 if bid==247852690:
  p02_escape(f,{'span':[.30,.71],'levels':[3.50,5.95,8.30],'material':'n01 black metal','dropAt':.32})
  shop09_face(f,{'paintSurround':{'bottom':.17,'top':3.35,'material':'n01 taupe metal'}})
  fidelity_access(f,7.97,1.10,{'rise':.26,'steps':2,'run':.44,'landing':.23,'rails':False,'material':'n01 cream stone'})
  n01_text(f,7.97,2.98,.51,.16,'345','store09 paper',.20)
  f.b(7.36,1.36,.13,.10,.21,.035,'n01 black metal')
 elif bid==247852697:
  shop09_face(f,{'paintSurround':{'bottom':-.31,'top':1.63,'material':'n01 cream stone'}})
  for y,mat in [(4.24,'n01 black metal'),(6.82,'n01 cream stone'),(9.39,'n01 taupe metal')]:
   f.b(f.L*.51,y,.045,.64,.22,.07,mat);shop09_frame(f,f.L*.51,y,.70,.25,.08,'n01 cream stone',.023)
  ss=f.L*.17;f.b(ss,1.77,.29,.66,.20,.035,'n01 cream stone');n01_text(f,ss,1.77,.46,.14,'343','n01 black metal',.314)
  for dx in [-.76,.76]:
   f.b(ss+dx,1.63,.18,.13,.28,.20,'n01 black metal');f.b(ss+dx,1.63,.285,.075,.16,.015,'opal lamp')
  for j in range(8):f.line((ss-.51+j*.145,-.22,.11),(ss-.51+j*.145,1.52,.11),.011,'n01 black metal')
  # Near-grade gate and below-grade floor, independently of the upper casements.
  for j in range(42):f.line((.16+j*(f.L-.32)/41,-.25,.89),(.16+j*(f.L-.32)/41,1.04,.89),.010,'n01 black metal')
  for yy in [.18,1.04]:f.line((.16,yy,.89),(f.L-.16,yy,.89),.021,'n01 black metal')
 elif bid==247852689:
  shop09_face(f,{'paintSurround':{'bottom':.17,'top':3.80,'material':'n01 navy enamel'}})
  f.b(f.L/2,3.54,.14,f.L,.64,.18,'n01 navy enamel')
  n01_text(f,f.L/2,3.54,f.L*.94,.47,'THE IMMIGRANT','n01 gold letters',.241,'serif',True)
  p02_escape(f,{'span':[.265,.735],'levels':[3.89,6.62,9.38,12.08],'material':'n01 rust iron','dropAt':.275})
  for y in [3.89,6.62,9.38,12.08]:
   for at in [.32,.67]:
    ss=f.L*at
    for dx in [-.045,.045]:p02_ring(f,ss+dx,y+.61,.072,.13,.95,'n01 rust iron',.008,20)
    p02_ring(f,ss,y+.32,.13,.06,.95,'n01 rust iron',.009,20)
  fidelity_access(f,f.L*.50,.94,{'rise':.34,'steps':3,'run':.57,'landing':.28,'rails':True,'railMaterial':'n01 black metal','material':'n01 cream stone'})
  for j,ch in enumerate('341'):n01_text(f,f.L*.439,2.55-j*.19,.10,.13,ch,'store09 paper',.25,'serif')
  for yy in [1.16,1.29,1.42]:p02_notice(f,f.L*.50,yy,.16,.10,-.12)
  n01_shelter(f)
 # Attributed utility cable paths at seams; no random clutter or fake neighbor gaps.
 for ss in [.08,f.L-.08]:f.line((ss,3.30,.065),(ss,h-.85,.065),.009,'n01 black metal')
