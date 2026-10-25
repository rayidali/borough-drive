"""Individually observed N01B anatomy; no photographic pixels or shared defaults changed."""
N01B_IDS={247852687,247852686,247852685,247852684}
for name,rgb in {'nb residential brick':(.43,.315,.27),'nb red brick':(.445,.285,.235),'nb taupe brick':(.42,.38,.34),'nb cream band':(.70,.69,.59),'nb sandstone':(.60,.46,.31),'nb pale cornice':(.59,.59,.48),'nb dark sash':(.20,.24,.20),'nb iron':(.075,.095,.095),'nb rust iron':(.29,.20,.145)}.items():material(name,rgb,.88)
for name,rgb,kind in [('nb black timber',(.065,.073,.070),2),('nb ochre door',(.43,.29,.135),2),('nb red canvas',(.46,.19,.20),5),('nb faded canvas',(.75,.70,.66),5),('nb gray canvas',(.31,.315,.28),5),('nb black canvas',(.10,.115,.12),5),('nb silver grille',(.49,.51,.46),6),('nb blue jug',(.18,.34,.45),1),('nb pink',(.71,.34,.53),1),('nb white fabric',(.71,.72,.63),5)]:
 material(name,rgb,.85);MATS[name]['storefront09Surface']=kind

def nb_text(f,s,y,w,h,text,mat='store09 paper',d=.19,font='serif'):return n01_text(f,s,y,w,h,text,mat,d,font)
def nb_slope_text(f,s,y,w,h,text,mat,top,drop,depth,font='serif'):
 d=.10+(top-y)/drop*depth+.018;obj=nb_text(f,s,y,w,h,text,mat,d,font)
 slope=math.atan2(drop,depth);cs=math.cos(slope);sn=math.sin(slope)
 obj.rotation_euler=Matrix((Vector((f.rx,-f.rz,0)),Vector((-f.nx*cs,f.nz*cs,sn)),Vector((f.nx*sn,-f.nz*sn,cs)))).transposed().to_euler();obj.scale.y/=sn;n01_center_text(obj,f,s,y,d);return obj

def nb_grille(f,a,b,bottom,top,d,diamond=False):
 if diamond:
  diamond_grille(f,a,b,bottom,top,d,'nb iron');return
 for j in range(int((top-bottom)/.095)+1):f.line((a,bottom+j*.095,d),(b,bottom+j*.095,d),.0065,'nb silver grille')
 for j in range(int((b-a)/.20)+1):
  x=a+j*.20
  for k in range(int((top-bottom)/.095)):
   yy=bottom+k*.095;off=.035 if k%2 else -.035
   f.line((x+off,yy,d),(x+off,yy+.095,d),.005,'nb silver grille')
 for x in [a,b]:f.b(x,(top+bottom)/2,d,.05,top-bottom,.07,'nb iron')

def nb_ac(f,s,y,w=.54,h=.34,d=.12):
 f.b(s,y,d,w,h,.36,'store09 cream enamel')
 for j in range(7):f.b(s,y-h*.38+j*h*.76/6,d+.185,w*.85,.012,.012,'nb dark sash')

def nb_cornice(f,h,ornate=True):
 mat='nb pale cornice' if ornate else 'nb iron'
 spans=[(0,f.L)] if ornate else [(0,f.L*.44),(f.L*.56,f.L)]
 for a,b in spans:
  for yy,hh,dd in [(h-.90,.09,.14),(h-.70,.32,.20),(h-.44,.14,.37),(h-.16,.16,.61),(h+.015,.11,.72)]:f.b((a+b)/2,yy,dd/2,b-a,hh,dd,mat)
  count=round((b-a)/.30)
  for j in range(count):
   ss=a+(b-a)*(j+.5)/count
   for yy,ww,hh,dd in [(h-.51,.10,.29,.35),(h-.30,.13,.26,.52),(h-.15,.16,.11,.66)]:f.b(ss,yy,dd/2,ww,hh,dd,mat)
   p02_ring(f,ss,h-.43,.037,.075,.35,mat,.012,12)
 if ornate:
  for j in range(5):
   ss=.13+(f.L-.26)*j/4
   f.b(ss,h-.52,.25,.18,.74,.42,mat);shop09_frame(f,ss,h-.79,.16,.18,.478,mat,.021)
   for yy in [h-.70,h-.53]:
    for dx in [-.037,.037]:p02_ring(f,ss+dx,yy,.038,.070,.48,mat,.013,14)
  for j in range(4):
   ss=(j+.5)*f.L/4;shop09_frame(f,ss,h-.77,f.L/4-.30,.24,.224,mat,.025)
   for k in range(5):p02_ring(f,ss+(k-2)*.17,h-.76,.057,.072,.26,mat,.012,12)
 else:
  f.strip(h-.90,.08,.14,mat)
  for x in [f.L*.465,f.L*.535]:f.line((x,h-.9,.24),(x,h+.42,.24),.021,'nb iron')
  for j in range(7):f.line((f.L*.465,h-.8+j*.18,.24),(f.L*.535,h-.8+j*.18,.24),.014,'nb iron')

def nb_heads(f,r):
 for w in r['windows']:
  if not w.get('nbHead'):continue
  s=w['at']*f.L;ww=w['width']*f.L;top=w['bottom']+w['height'];mat=w['trim']
  for yy,hh,width,dd in [(top+.10,.17,ww+.20,.20),(top+.22,.08,ww+.34,.28)]:f.b(s,yy,dd/2,width,hh,dd,mat)
  if w['nbHead']=='pediment':
   pts=[f.p(s-ww*.70,top+.26,.19),f.p(s,top+.52,.19),f.p(s+ww*.70,top+.26,.19)];face(pts,mat);face(list(reversed(pts)),mat)
   for rise,dep in [(.52,.24),(.43,.285)]:
    for side in [-1,1]:f.line((s+side*ww*.70,top+.26,dep),(s,top+rise,dep),.027,mat)
  elif w['nbHead']=='flat':
   face([f.p(s-ww*.66,top+.12,.235),f.p(s+ww*.66,top+.12,.235),f.p(s+ww*.59,top+.29,.235),f.p(s-ww*.59,top+.29,.235)],mat)
  for dx in [-ww*.41,ww*.41]:f.b(s+dx,w['bottom']-.15,.10,.12,.19,.17,mat)

def nb_portal(f,s,number):
 mat='nb black timber'
 for dx in [-.69,.69]:
  x=s+dx;f.b(x,1.83,.11,.23,3.26,.31,mat)
  for yy,ww,hh in [(.28,.34,.26),(.48,.29,.12),(1.10,.26,.10),(2.83,.29,.13),(3.29,.34,.16)]:f.b(x,yy,.19,ww,hh,.37,mat)
  for dd in [-.060,0,.060]:f.b(x+dd,1.95,.285,.014,1.49,.018,'nb iron')
  for yy in [.75,2.98]:p02_ring(f,x,yy,.072,.075,.292,'nb dark sash',.017,20)
 f.b(s,3.37,.16,1.65,.18,.35,mat)
 if number=='335':nb_text(f,s,2.99,.62,.21,number,'nb iron',-.105,'serif')
 else:
  f.b(s,2.99,-.12,1.00,.33,.021,'nb cream band')
  for row in range(3):
   for col in range(10):
    x=s-.46+col*.102;yy=2.90+row*.09
    f.line((x,yy,-.099),(x+.045,yy+.065,-.099),.008,'nb ochre door')
    f.line((x+.045,yy+.065,-.099),(x+.09,yy,-.099),.008,'nb ochre door')
 f.b(s,3.39,.44,.43,.08,.40,'store09 cream enamel');f.b(s,3.35,.63,.35,.025,.045,'opal lamp')

_nb_previous_shop=photographed_shop
def photographed_shop(f,a,b,r):
 detail=r['design'].get('detailN01B')
 if not detail:return _nb_previous_shop(f,a,b,r)
 kind=detail['kind'];w=b-a;c=(a+b)/2
 # Projected display at 337 is separate from its deep common entrance.
 original=f
 if kind=='wicked':
  OPENINGS[frontage_key(f)].append((a,.17,b,3.08));f=FidelityProjectedFacade(f,.31)
 _nb_previous_shop(f,a,b,r)
 for ss in [a+.025,b-.025]:f.b(ss,1.6,-.48,.05,2.9,.94,'nb black timber')
 if kind=='cleaners':
  observed_awning(f,a-.03,b+.05,{'detail09':True,'shape':'round','y':3.71,'drop':.40,'depth':.86,'valance':.54,'material':'nb red canvas','sidePanels':True})
  nb_text(f,c,3.07,w*.93,.25,'NEW SEW GOOD CLEANERS','store09 paper',.986,'condensed');nb_text(f,c,2.86,w*.43,.105,'337 E. 9 ST','store09 paper',.987,'bold')
  # Faded crown lies on its cylindrical cloth surface, with subtle uneven edge.
  for j in range(50):
   ss=a+w*(j+.5)/50;t=.59+.12*math.sin(j*.74)
   for section in range(12):
    lo=.02+(t-.02)*section/12;hi=.02+(t-.02)*(section+1)/12
    crown=[f.p(xx,3.717-.40*(1-math.cos(q*math.pi/2)),.117+.86*math.sin(q*math.pi/2)) for xx,q in [(ss-w/100,hi),(ss+w/100,hi),(ss+w/100,lo),(ss-w/100,lo)]]
    face(crown,'nb faded canvas');face(crown[::-1],'nb faded canvas')
  pp=f.p(b+.065,0,.93);side=Facade(pp[0],pp[2],-f.nx,-f.nz,.80)
  for yy,word in [(3.33,'DROP'),(3.13,'OFF'),(2.93,'SERVICE')]:nb_text(side,.41,yy,.61,.14,word,'store09 paper',.015,'condensed')
  for at in [1/3,2/3]:f.b(a+w*at,1.67,-.08,.035,1.96,.05,'nb ochre door')
  for yy in [1.28,1.95]:f.b(c,yy,-.08,w-.16,.055,.14,'nb ochre door')
  for row in range(3):
   for col in range(3):
    ss=a+w*(col+.5)/3;yy=.92+row*.66
    mat=['nb white fabric','nb blue jug','nb pink','store09 printed red','nb ochre door'][(row*3+col)%5]
    if row==0:
     for k in range(4):f.b(ss,yy-.13+k*.073,-.45,w*.19,.049,.31,mat if k%2 else 'nb white fabric')
    else:f.b(ss,yy,-.45,w*.19,.33,.31,mat)
    if row==1 and col==1:
     f.b(ss+.12,yy+.23,-.41,.20,.11,.12,'store09 cream enamel');f.b(ss-.02,yy+.17,-.40,.065,.23,.10,'store09 cream enamel')
     f.b(ss+.13,yy+.05,-.33,.38,.06,.18,'store09 cream enamel');p02_ring(f,ss-.12,yy+.26,.082,.082,-.30,'nb iron',.021,20)
     f.line((ss+.19,yy+.20,-.31),(ss+.19,yy+.085,-.31),.006,'nb silver grille')
    elif row==2:
     p02_ring(f,ss,yy+.21,w*.075,.08,-.45,mat,.022,20)
  for j in range(7):
   ss=a+w*(.07+j*.035);f.b(ss,2.40,-.22,.056,.16,.06,'store09 paper');f.b(ss,2.50,-.22,.027,.047,.03,'nb black timber')
  for ss in [a+w*.29,a+w*.67]:p02_notice(f,ss,1.81,.26,.28,.049)
  nb_ac(f,c,.43,.64,.28,.13)
  rod(f.p(c,.17,.42),f.p(c,.41,.42),.115,'store09 paper',16,r2=.15)
 elif kind=='wicked':
  nb_grille(f,a+.05,b-.05,.72,2.93,.22,True)
  for j in range(3):
   ss=a+w*(j+.5)/3;yy=1.45+.13*(j%2)
   rod(f.p(ss,yy-.31,-.48),f.p(ss,yy+.28,-.48),.18,'nb white fabric',12,r2=.13)
   p02_ring(f,ss,yy+.11,.105,.12,-.25,'store09 aged brass',.007,24)
   f.b(ss,yy-.39,-.47,.21,.13,.19,'nb ochre door')
  for j in range(4):f.b(a+w*(j+.5)/4,.95,-.30,w*.16,.10,.18,'store09 paper')
 elif kind in ['fannys','spark','west333']:
  gray=kind=='fannys';top=3.56;drop=.48;depth=.98
  observed_awning(f,a-.045,b+.045,{'detail09':True,'y':top,'drop':drop,'depth':depth,'valance':.25,'material':'nb gray canvas' if gray else 'nb black canvas','sidePanels':True})
  if gray:
   nb_text(f,c,2.965,w*.69,.18,'Fabulous Fanny’s','store09 paper',1.12,'script')
   for ss in [a+.17,b-.17]:nb_text(f,ss,2.968,.30,.12,'335','store09 paper',1.122,'script')
  elif kind=='spark':
   nb_slope_text(f,c,3.33,w*.48,.16,'SPARK','store09 paper',top,drop,depth,'bold');nb_slope_text(f,c,3.17,w*.50,.115,'pretty','store09 paper',top,drop,depth,'script')
   nb_text(f,a+.22,2.97,.35,.13,'333','nb pink',1.121,'bold')
  else:nb_text(f,b-.35,2.97,.61,.11,'333 E9th','store09 paper',1.121,'condensed')
  if kind=='west333':
   ss=a+w*.845;p02_ring(f,ss,1.83,.23,.23,-.066,'store09 paper',.013,40);p02_ring(f,ss,1.83,.20,.20,-.065,'store09 paper',.006,32)
   # Unreadable seal remains an abstract loop, not fabricated business copy.
   p02_curve(f,[(ss-.16+k*.32/24,1.83+.052*math.sin(k*.9)) for k in range(25)],-.052,'store09 paper',.011)
   for j in range(8):f.b(ss,2.79-j*.037,-.12,w*.24,.016,.014,'store09 cream canvas')
   for xx in [a+w*.20,a+w*.47]:
    f.b(xx,.54,-.41,.43,.07,.39,'nb white fabric');f.b(xx,.81,-.68,.43,.52,.065,'nb white fabric')
    for dx in [-.17,.17]:f.line((xx+dx,.17,-.42),(xx+dx,.54,-.42),.016,'store09 aged brass')
   rod(f.p(ss,.18,-.25),f.p(ss,.59,-.25),.15,'nb blue jug',16,r2=.12);f.b(ss,.65,-.25,.08,.13,.08,'nb blue jug')
  else:
   nb_grille(f,a+.06,b-.06,.19,2.86,.13);nb_ac(f,a+w*.20,2.57,.61,.41,-.16)
   if gray:
    ss=a+w*.65;shop09_frame(f,ss,1.52,w*.56,2.05,-.14,'store09 printed red',.045)
    # Oversized eyeglass motif plus rows of individually shaped frame displays.
    for dx in [-.23,.23]:p02_ring(f,ss+dx,2.36,.20,.135,-.06,'nb sandstone',.022,32)
    f.line((ss-.035,2.37,-.04),(ss+.035,2.37,-.04),.020,'nb sandstone')
    for row in range(4):
     yy=.64+row*.34;f.b(ss,yy-.08,-.42,w*.50,.023,.31,'nb ochre door')
     for col in range(3):
      xx=ss+(col-1)*w*.145
      for dx in [-.055,.055]:p02_ring(f,xx+dx,yy,.052,.032,-.22,'store09 aged brass' if row%2 else 'nb iron',.007,16)
      f.line((xx-.008,yy,-.22),(xx+.008,yy,-.22),.007,'nb iron')
    for xx in [a+w*.57,a+w*.86]:
     rod(f.p(xx,1.13,-.50),f.p(xx,1.43,-.50),.12,'nb white fabric',12,r2=.08);p02_disc(f,xx,1.56,.10,.13,-.37,'nb white fabric',24)
   else:
    # Unequal pale torsos, patterned clothes, boxes and small toy silhouettes.
    for j,xx in enumerate([a+w*.25,a+w*.65]):
     rod(f.p(xx,.92,-.47),f.p(xx,1.56,-.47),.22,'nb white fabric',14,r2=.15);f.b(xx,1.66,-.47,.07,.15,.08,'nb white fabric')
     f.line((xx,.25,-.47),(xx,.90,-.47),.018,'nb iron')
     color='nb pink' if j else 'store09 printed blue'
     f.b(xx,1.21,-.23,.26,.14,.035,color)
     for side in [-1,1]:
      f.line((xx+side*.16,1.48,-.46),(xx+side*.30,1.28,-.44),.065,color)
     for k in range(4):f.b(xx,1.06+k*.10,-.211,.28,.023,.012,'store09 paper' if j else 'store09 printed red')
    for j in range(9):
     xx=a+w*(j+.5)/9;f.b(xx,.41,-.30,.14,.29+.055*(j%3),.14,['nb pink','store09 printed blue','store09 printed red','store09 aged brass'][j%4]);p02_disc(f,xx,.62+(j%3)*.055,.047,.06,-.215,'store09 paper',12)
    for j in range(13):f.b(a+w*.85,1.12+j*.075,-.51,w*.17,.045,.39,['nb pink','store09 printed blue','store09 printed red'][j%3])
    f.b(c,2.30,-.87,w*.61,.43,.018,'store09 printed red')
 elif kind=='layers':
  nb_grille(f,a+.04,b-.04,.18,2.94,.15)
  # Small brown sign at west frame; no borrowed neighboring canopy.
  f.b(a+.23,2.83,.25,.62,.36,.08,'nb ochre door');nb_text(f,a+.23,2.83,.48,.18,'Layers','store09 paper',.30,'script')
  for at in [.32,.72]:
   ss=a+w*at;f.b(ss,1.45,-.84,.65,1.60,.035,'seventh reflective glass');shop09_frame(f,ss,1.45,.70,1.65,-.80,'store09 brushed steel',.035)
   f.b(ss,.62,-.35,.40,.10,.39,'nb white fabric');f.b(ss,.99,-.62,.42,.61,.10,'nb white fabric');rod(f.p(ss,.20,-.40),f.p(ss,.58,-.40),.06,'nb silver grille',12)
  p03_tags(f,a+.04,b-.05,.25,.44,.22,335)

_nb_previous_render=render_building
def render_building(b):
 if b['id'] not in N01B_IDS:return _nb_previous_render(b)
 bid=b['id'];r=b['firstStmarksArchitecture']['0'];b['renderHeight']=b['firstStmarksHeight'];h=b['renderHeight'];owner(str(bid)+' N01B observed Ninth')
 wall_mass(b,r['wall'],False);v=b['frontages'][0];f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']);f.wall=r['wall']
 effective=__import__('copy').deepcopy(r)
 if bid==247852687:effective['observedGround']['basementAreaways']=[]
 fidelity_elevation({**b,'businesses':[],'seventhArchitecture':effective},f,effective)
 for w in r['windows']:
  if w['bottom']<2:continue
  ss=w['at']*f.L;ww=w['width']*f.L;top=w['bottom']+w['height'];fraction=[.67,.26,.51,.82][round(ss*10+top)%4]
  mode=round(ss*10+top)%4
  if mode==0:
   f.b(ss,top-.07-w['height']*fraction/2,-.13,ww-.10,w['height']*fraction,.014,'nb white fabric')
  elif mode==1:
   for dx in [-ww*.32,ww*.32]:
    for j in range(6):f.b(ss+dx+(j-2.5)*ww*.033,w['bottom']+w['height']*.5,-.14,ww*.035,w['height']-.13,.018,'nb white fabric')
  elif mode==2:
   for j in range(int(w['height']*fraction/.063)):f.b(ss,top-.08-j*.063,-.125,ww-.10,.025,.012,'nb white fabric')
 if bid==247852687:
  for yy in [4.67,7.30,10.08,12.86,15.64]:f.strip(yy,.25,.13,'nb cream band')
  for yy in [2.51,5.17,7.95,10.73,13.51]:f.strip(yy,.08,.10,'nb cream band')
  f.strip(h-.025,.08,.065,'nb residential brick')
  for row,y in enumerate([2.58,5.24,8.02,10.80,13.58]):
   for at in [.15,.84]:
    ss=f.L*at;nb_ac(f,ss,y-.34,.65,.25,.035)
  p02_escape(f,{'span':[.285,.735],'levels':[5.02,7.82,10.62,13.42],'material':'nb rust iron','reverse':True,'dropAt':.32})
  ss=f.L*.84;nb_text(f,ss,.69,.39,.13,'339','nb iron',-.115,'serif');nb_text(f,ss,1.85,.49,.10,'339','nb iron',.215,'serif')
  for dx in [-.64,.64]:
   p02_disc(f,ss+dx,2.02,.14,.14,.18,'nb iron',24);p02_disc(f,ss+dx,2.02,.10,.10,.195,'opal lamp',24)
   for off in [-.05,.05]:f.line((ss+dx+off,1.91,.211),(ss+dx+off,2.13,.211),.008,'nb iron')
  f.b(ss+.53,1.33,.19,.09,.22,.05,'nb iron')
  # The full-width well has a low floor; descent only at the observed east entry.
  f.b(f.L*.49,-.52,.47,f.L*.96,.08,.91,'nb residential brick')
  for x in [.08,f.L-.10]:f.b(x,-.15,.48,.07,.70,.96,'nb residential brick')
  f.b(f.L*.37,-.16,.92,f.L*.71,.70,.07,'nb residential brick')
  for j in range(3):f.b(ss,.07-j*.16,.84-j*.27,1.16,.09,.28,'nb cream band')
  # Low well fence stops clear of the east approach, without filling the void.
  for a,end in [(.10,f.L*.69)]:
   for j in range(round((end-a)/.13)+1):f.line((a+j*.13,-.24,.93),(a+j*.13,1.0,.93),.010,'nb iron')
   for yy in [.15,1.0]:f.line((a,yy,.93),(end,yy,.93),.021,'nb iron')
  for x in [f.L*.74,f.L-.12]:
   f.line((x,.18,.05),(x,1.01,.05),.018,'nb iron');f.line((x,1.01,.05),(x,1.01,.94),.020,'nb iron')
   for j in range(7):f.line((x,.18,j*.14),(x,1.01,j*.14),.01,'nb iron')
  # Four real sloping-lid refuse lockers; never duplicate a restaurant shelter.
  left=f.L*.31;right=f.L*.74;c=(left+right)/2;dd=1.17
  f.b(c,.63,dd,right-left,.93,.65,'nb black timber')
  for j in range(4):
   x=left+(right-left)*(j+.5)/4;ww=(right-left)/4-.035
   pts=[f.p(x-ww/2,1.10,dd+.35),f.p(x+ww/2,1.10,dd+.35),f.p(x+ww/2,1.28,dd-.35),f.p(x-ww/2,1.28,dd-.35)];face(pts,'nb black timber');face(list(reversed(pts)),'nb black timber')
   f.line((x-.09,1.18,dd+.12),(x+.09,1.18,dd+.12),.015,'nb silver grille');p02_notice(f,x,1.19,.23,.10,dd+.03)
  for x in [left+.12,c,right-.12]:f.b(x,.88,dd+.34,.04,.10,.025,'nb silver grille')
 else:
  shop09_face(f,{'paintSurround':{'bottom':.17,'top':3.66,'material':'nb black timber'}})
  nb_heads(f,r);nb_cornice(f,h,bid!=247852686)
  levels=[3.53,6.45,9.38,12.31] if bid==247852686 else [3.70,6.84,9.87,12.73]
  p02_escape(f,{'span':[.285,.75],'levels':levels,'material':'nb iron','dropAt':.715,'reverse':bid==247852686})
  if bid==247852686:
   ss=f.L*.557;ww=1.24
   # Deep entry is backed by its door, with separate side walls and three visible treads.
   OPENINGS[frontage_key(f)].append((ss-ww/2,.17,ss+ww/2,3.12))
   for xx in [ss-ww/2,ss+ww/2]:f.b(xx,1.80,-.49,.045,2.63,1.22,'nb black timber')
   for xx in [ss-.44,ss+.44]:f.b(xx,1.78,-.54,.035,2.25,1.05,'nb black timber')
   f.b(ss,2.91,-.54,.91,.035,1.05,'nb black timber')
   f.b(ss,3.04,-.51,ww,.09,1.18,'nb black timber')
   for j in range(3):f.b(ss,.17+(j+1)*.15/2,.82-j*.27,ww,(j+1)*.15,.29,'nb cream band')
   f.b(ss,.62,-.53,ww,.07,1.04,'nb dark sash');nb_text(f,ss,2.71,.43,.13,'337','store09 aged brass',-1.015,'serif')
   for yy in levels:
    for at in [.35,.68]:
     for dx in [-.038,.038]:p02_ring(f,f.L*at+dx,yy+.51,.065,.15,.95,'nb iron',.008,18)
  else:
   nb_portal(f,f.L*.5,'335' if bid==247852685 else '333')
   if bid==247852685:
    for at in [.422,.444]:
     ss=f.L*at;rod(f.p(ss,.18,.37),f.p(ss,.58,.37),.038,'nb silver grille',12);p02_disc(f,ss,.63,.060,.060,.41,'store09 bottle green',16)
 for ss in [.055,f.L-.055]:f.line((ss,3.67,.066),(ss,h-.96,.066),.008,'nb iron')
