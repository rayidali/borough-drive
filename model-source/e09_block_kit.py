"""Observed Ninth block components. Dispatch is restricted to 34 new owners.

No source photographs are used as textures. Signs and artwork are authored
approximations. Shared primitives express observed construction, never a
business-name/color substitution over a universal storefront.
"""
E09_BLOCK_IDS={247852683,247852682,1063735559,247852681,247852680,247852679,247852678,247852677,247852676,247852675,247852674,247852673,247852672,247852671,247852702,241822239,241822276,241822204,241822315,241822241,241822261,241822335,241822244,241822293,241822229,241822251,241822179,241822183,241822272,241822187,241822165,241822171,241822269,241822210}
for name,rgb in {'red brick':(.49,.28,.22),'dark red brick':(.40,.235,.20),'red brown brick':(.44,.29,.24),'buff red brick':(.53,.34,.26),'pink brick':(.54,.38,.32),'modern red brick':(.54,.32,.26),'tan brick':(.56,.47,.33),'yellow brick':(.55,.53,.45),'buff brick':(.56,.49,.37),'cream brick':(.73,.69,.55),'dark brick':(.20,.22,.21),'brown stone':(.43,.34,.25),'cream stone':(.73,.69,.58),'white stone':(.80,.78,.70),'gray stone':(.48,.50,.45),'buff stone':(.65,.59,.46),'limestone':(.79,.74,.63),'white stucco':(.77,.78,.73),'charcoal stone':(.23,.25,.25),'sash':(.16,.20,.18),'iron':(.075,.09,.09),'rust iron':(.32,.21,.16),'blue iron':(.24,.31,.33)}.items():material('eb '+name,rgb,.90)
for name,rgb,kind in [('dark wood',(.065,.075,.072),2),('oak wood',(.34,.22,.13),2),('green wood',(.055,.24,.15),2),('red wood',(.48,.14,.13),2),('white wood',(.78,.77,.68),2),('yellow wood',(.78,.70,.40),2),('turquoise wood',(.05,.43,.43),2),('plywood',(.55,.39,.23),2),('green metal',(.21,.31,.25),6),('blue metal',(.10,.22,.36),6),('gray metal',(.45,.47,.43),6),('silver metal',(.58,.60,.56),6),('brown metal',(.32,.30,.23),6),('gold metal',(.67,.49,.22),6),('red metal',(.52,.16,.13),6),('black canvas',(.085,.10,.105),5),('blue canvas',(.08,.19,.34),5),('red canvas',(.49,.12,.13),5),('taupe canvas',(.47,.42,.33),5),('gray canvas',(.38,.39,.34),5),('white canvas',(.77,.76,.68),5),('green canvas',(.09,.29,.18),5),('pink enamel',(.79,.25,.47),1),('cyan enamel',(.08,.55,.66),1),('yellow enamel',(.90,.68,.16),1),('purple enamel',(.31,.14,.35),1),('blue enamel',(.05,.25,.63),1),('pale fabric',(.74,.73,.64),5)]:
 material('eb '+name,rgb,.83);MATS['eb '+name]['storefront09Surface']=kind

material('eb carved stone',(.51,.425,.34),.88)
def eb_arc(f,s,y,rx,ry,depth,thickness,mat,segments=24):
 # Solid shallow tubes keep the molding visible from both street directions.
 for j in range(segments):
  a=j*math.pi/segments;b=(j+1)*math.pi/segments
  f.line((s+rx*math.cos(a),y+ry*math.sin(a),depth),(s+rx*math.cos(b),y+ry*math.sin(b),depth),thickness*.65,mat)

def eb_text(f,s,y,w,h,text,mat='store09 paper',d=.20,font='serif'):
 if not text:return None
 return nb_text(f,s,y,w,h,text,mat,d,'bold' if font=='sans' else font)
def eb_panel(f,a,b,y,h,mat='eb dark wood',d=.17):
 f.b((a+b)/2,y,d,b-a,h,.14,mat)
 for yy in [y-h/2,y+h/2]:f.b((a+b)/2,yy,d+.09,b-a+.05,.045,.08,mat)
def eb_lamp(f,s,y,d=.45,mat='eb iron'):
 f.line((s,y,.10),(s,y+.14,d-.12),.018,mat);f.line((s,y+.14,d-.12),(s,y+.08,d),.018,mat)
 rod(f.p(s,y-.06,d),f.p(s,y+.07,d),.13,mat,12,r2=.06);p02_disc(f,s,y-.07,.09,.025,d+.035,'opal lamp',12)
def eb_canopy(f,a,b,color,text='',font='serif',y=3.50,drop=.45,dep=.85,letter='store09 paper',stripes=False):
 observed_awning(f,a-.025,b+.025,{'detail09':True,'y':y,'drop':drop,'depth':dep,'valance':.22,'material':color,'sidePanels':True})
 if stripes:
  for j in range(round((b-a)/.09)):
   x=a+j*.09
   face([f.p(x,y,.11),f.p(x+.014,y,.11),f.p(x+.014,y-drop,dep+.11),f.p(x,y-drop,dep+.11)],'eb pale fabric')
 if text:nb_slope_text(f,(a+b)/2,y-drop*.53,(b-a)*.87,.22,text,letter,y,drop,dep,'bold' if font=='sans' else font)
def eb_blade(f,s,y,text,mat='eb dark wood',round=False,color='store09 paper',icon=None):
 # The blade is perpendicular to the street, with lettering on both faces.
 f.line((s,y+.30,.10),(s,y+.30,.86),.018,'eb iron')
 for flip in [False,True]:
  pp=f.p(s+(.035 if flip else -.035),0,.90 if flip else .18)
  ff=Facade(pp[0],pp[2],(-1 if flip else 1)*f.nx,(-1 if flip else 1)*f.nz,.72)
  if round:p02_disc(ff,.36,y,.32,.32,.0,mat,32)
  else:ff.b(.36,y,0,.69,.66,.045,mat)
  eb_text(ff,.36,y,.57,.13,text,color,.035,'sans')
  if icon=='pineapple':
   p02_ring(ff,.36,y-.05,.12,.18,.045,'eb gold metal',.025,24)
   for j in [-1,0,1]:ff.line((.36,y+.11,.045),(.36+j*.13,y+.29-abs(j)*.05,.045),.025,'eb gold metal')
   for j in range(3):
    ff.line((.27,y-.16+j*.09,.047),(.45,y-.05+j*.09,.047),.010,'eb gold metal')
    ff.line((.45,y-.16+j*.09,.047),(.27,y-.05+j*.09,.047),.010,'eb gold metal')
  elif icon=='flower':
   for j in range(6):
    ang=j*math.tau/6;p02_disc(ff,.36+math.cos(ang)*.14,y+math.sin(ang)*.14,.09,.09,.047,'store09 paper',20)
   p02_disc(ff,.36,y,.055,.055,.055,'eb dark wood',20)
def eb_bottles(f,a,b,y,d=-.55,rows=2,colors=None):
 colors=colors or ['store09 bottle green','eb oak wood','store09 paper']
 for row in range(rows):
  yy=y+row*.43;f.b((a+b)/2,yy-.08,d,b-a,.035,.27,'eb oak wood')
  for j in range(max(2,int((b-a)/.17))):
   x=a+.10+j*.17;mat=colors[(j+row)%len(colors)]
   rod(f.p(x,yy,d),f.p(x,yy+.22,d),.048,mat,8,r2=.04);f.b(x,yy+.27,d,.035,.10,.035,mat);f.b(x,yy+.12,d+.05,.067,.09,.012,'store09 paper')
def eb_books(f,a,b,y,d=-.50,rows=3):
 colors=['eb red wood','eb blue metal','eb yellow wood','eb pale fabric','eb green wood']
 for row in range(rows):
  yy=y+row*.37;f.b((a+b)/2,yy-.045,d,b-a,.035,.30,'eb oak wood')
  for j in range(max(2,int((b-a)/.09))):
   x=a+.05+j*.09;hh=.20+.045*(j%3);f.b(x,yy+hh/2,d,.065,hh,.17,colors[(j+row)%5]);f.b(x,yy+hh*.65,d+.09,.042,.009,.008,'store09 paper')
def eb_clothes(f,a,b,y,d=-.55):
 f.line((a,y,d),(b,y,d),.012,'eb silver metal')
 for j in range(max(2,int((b-a)/.20))):
  x=a+.12+j*.20;mat=['eb pale fabric','eb red canvas','eb gray canvas','eb blue canvas'][j%4]
  for side in [-1,1]:f.line((x,y-.03,d),(x+side*.12,y-.14,d),.009,'eb oak wood')
  f.b(x,y-.43,d,.18,.58,.08,mat)
  for side in [-1,1]:f.line((x+side*.08,y-.19,d),(x+side*.16,y-.40,d),.040,mat)
def eb_plant(f,s,y,d=.75,size=.45,flowers=False):
 rod(f.p(s,y,d),f.p(s,y+size*.55,d),size*.30,'eb oak wood',10,r2=size*.40)
 for j in range(7):
  angle=j*2.4;xx=s+math.cos(angle)*size*.28;yy=y+size*(.95+.16*(j%3));dd=d+math.sin(angle)*size*.25
  f.line((s,y+size*.5,d),(xx,yy,dd),.009,'store09 bottle green')
  for k in [-1,1]:p02_disc(f,xx+k*.045,yy-.07,.07,.035,dd,'store09 bottle green',8)
  if flowers:p02_disc(f,xx,yy,.055,.055,dd,'eb yellow enamel',8)
def eb_board(f,s,y,text,color='eb oak wood',d=.90):
 f.b(s,y+.52,d,.57,.83,.045,'eb iron');shop09_frame(f,s,y+.52,.63,.90,d+.03,color,.045)
 for side in [-1,1]:
  f.line((s+side*.29,y,d+.26),(s+side*.29,y+.96,d-.04),.025,color)
 for j,line in enumerate(text.split('|')):eb_text(f,s,y+.77-j*.19,.47,.13,line,'store09 paper',d+.034,'script')

_eb_previous_shop=photographed_shop
def photographed_shop(f,a,b,r):
 detail=r['design'].get('detailE09Block')
 if not detail:return _eb_previous_shop(f,a,b,r)
 k=detail['kind'];w=b-a;c=(a+b)/2;spec=r['design'];top=spec['top'];head=spec['head'];base=spec['base'];frame=spec['detail09']['frame']
 _eb_previous_shop(f,a,b,r)
 # Bounded shallow interior. Every shop keeps its own opening/panel order.
 f.b(c,(head+base)/2,-1.02,w-.12,head-base,.035,'eb cream stone')
 for x in [a+.03,b-.03]:f.b(x,(head+base)/2,-.53,.035,head-base,.95,frame)
 if k=='source':
  eb_canopy(f,a,b,'eb black canvas',y=3.47)
  nb_slope_text(f,a+w*.59,3.31,w*.66,.12,'212-473-7833','store09 paper',3.47,.45,.85,'script')
  nb_slope_text(f,a+w*.57,3.15,w*.72,.095,'thesourceunltd.com','store09 paper',3.47,.45,.85,'script')
  eb_text(f,c,2.91,w*.88,.075,'PRINT • COPY • DESIGN','store09 paper',.982,'condensed')
  for j in range(12):
   t=j*math.tau/12;f.line((a+w*.12,3.19,.65),(a+w*.12+.13*math.cos(t),3.19+.13*math.sin(t),.65),.012,'store09 paper')
  f.b(c,1.23,.03,w-.12,1.77,.04,'eb white wood');nb_grille(f,a+.08,b-.08,2.13,2.8,.16)
  for x in [a+w*.23,a+w*.66]:
   for dx in [-.06,.06]:f.b(x+dx,1.18,.066,.045,.90,.012,'eb dark wood')
   f.b(x,1.61,.067,.20,.06,.013,'eb dark wood')
  cable=[]
  for j in range(41):
   x=a+w*.06+j*w*.88/40;yy=1.0+.63*(abs((x-c)/(w*.47))**1.7);cable.append((x,yy,.085));f.line((x,yy,.085),(x,1.0,.085),.007,'eb red wood')
  for p,q in zip(cable,cable[1:]):f.line(p,q,.014,'eb dark wood')
  f.line((a+.05,1.0,.07),(b-.05,1.0,.07),.025,'eb dark wood');f.b(b-.10,1.55,.23,.25,.37,.20,'eb oak wood')
 elif k=='frida':
  eb_panel(f,a,b,3.21,.53)
  for yy,t in [(3.32,'Frida'),(3.10,'Munchies')]:
   eb_text(f,c,yy,w*.68,.20,t,'eb pink enamel',.262,'bold');eb_text(f,c,yy+.008,w*.65,.18,t,'store09 paper',.275,'bold')
  for j,mat in enumerate(['eb cyan enamel','eb yellow enamel','eb pink enamel']):f.b(c,2.89-j*.045,.14,w*.90,.035,.025,mat)
  ss=a+w*.65;f.b(ss,1.58,-.10,w*.60,1.92,.025,'eb yellow wood')
  for yy,t in [(2.05,'RETAIL SPACE'),(1.83,'FOR LEASE')]:eb_text(f,ss,yy,w*.52,.13,t,'eb dark wood',-.08,'bold')
  for j in range(9):
   mat=['eb pink enamel','eb blue enamel','eb yellow enamel','eb green wood'][j%4];f.b(b-.025,.40+j*.22,.17,.06,.21,.06,mat)
   x=a+.05+j*(w-.10)/8;face([f.p(x,2.75,.19),f.p(x+.12,2.73,.19),f.p(x+.06,2.55,.19)],mat)
  p03_tags(f,a+w*.40,b-.12,.6,1.1,.07,331)
 elif k=='hare':
  eb_panel(f,a,b,3.19,.43,'eb red wood');eb_text(f,c,3.20,w*.88,.22,'The March Hare','store09 paper',.27,'script')
  f.b(c,.40,.10,w-.10,.42,.09,'eb green wood')
  for j in range(8):
   x=a+w*(.10+j*.075);yy=1.44+(j%3)*.16;mat=['eb pale fabric','eb yellow wood','eb pink enamel'][j%3]
   p02_disc(f,x,yy,.08,.10,-.26,mat,16)
   for dx in [-.055,.055]:p02_disc(f,x+dx,yy+.09,.034,.04,-.25,mat,12)
   p02_disc(f,x,yy-.13,.10,.13,-.27,mat,16)
  p02_disc(f,c,.45,.15,.08,.16,'store09 paper',18)
  for dx in [-.05,.03]:p02_disc(f,c+.14+dx,.61,.025,.12,.17,'store09 paper',12)
  eb_books(f,a+.15,a+w*.54,.66,rows=3)
  for j in range(5):
   x=a+w*(.15+j*.12);yy=1.85+.12*(j%2);p02_disc(f,x,yy,.085,.085,-.30,['eb yellow enamel','eb pink enamel','eb cyan enamel'][j%3],16);f.b(x,yy-.15,-.34,.12,.19,.12,'eb red wood')
 elif k=='321east':
  eb_canopy(f,a,b,'eb blue canvas',y=3.44);nb_grille(f,a+.05,b-.05,.20,2.84,.14)
  f.b(c,1.5,-.16,w-.15,2.4,.02,'eb charcoal stone')
 elif k=='rosemary':
  f.b(a+w*.35,.45,.24,w*.67,.58,.40,'eb green wood')
  for yy,t in [(1.98,'rose'),(1.76,'mary')]:eb_text(f,a+w*.35,yy,w*.48,.22,t,'store09 paper',.055,'serif')
  eb_text(f,a+w*.55,2.06,.21,.085,'home','store09 paper',.055,'serif')
  f.b(a+w*.35,.76,-.50,w*.64,.05,.56,'eb white wood');eb_plant(f,a+w*.17,.79,-.40,.55,True)
  eb_books(f,a+w*.51,a+w*.68,.83,rows=3)
  for row in range(3):
   for col in range(4):f.b(a+w*.29+col*.09,.82,-.25-row*.08,.08,.025,.07,'eb green wood' if (row+col)%2 else 'eb white wood')
  eb_blade(f,a+.05,3.08,'rosemary','eb green wood',True)
 elif k=='gnocchi':
  eb_panel(f,a,b,3.20,.46,'eb blue metal');eb_text(f,c,3.20,w*.90,.25,'Gnocchi on 9th','eb gold metal',.27,'script')
  p02_disc(f,a+w*.67,1.85,.38,.38,-.07,'eb yellow enamel',32);p02_ring(f,a+w*.67,1.85,.32,.32,-.045,'eb red wood',.022,32);eb_text(f,a+w*.67,1.85,.60,.12,'GNOCCHI','eb red wood',-.025,'bold')
  nb_grille(f,a+w*.32,b-.06,.24,2.79,.15)
  rod(f.p(b-.15,.18,.88),f.p(b-.15,.95,.88),.30,'eb oak wood',16,r2=.29)
  for yy in [.30,.77]:p02_ring(f,b-.15,yy,.30,.06,1.12,'eb iron',.017,24)
  eb_board(f,b-.15,.93,'GNOCCHI|ON 9TH',d=.89)
 elif k=='spook':
  for j,mat in enumerate(['eb cyan enamel','eb green wood','eb purple enamel','eb pink enamel']):f.b(c,2.49-j*.14,.20,w,.14,.07,mat)
  eb_text(f,c,2.39,w*.83,.24,'SPOOKSVILLA','eb dark wood',.25,'bold');eb_text(f,c,2.40,w*.81,.22,'SPOOKSVILLA','store09 paper',.263,'bold')
  eb_text(f,c,2.15,w*.55,.14,'+ FRIENDS','store09 paper',.264,'bold')
  for x in [a+.12,b-.12]:
   p02_ring(f,x,2.47,.055,.078,.265,'eb yellow enamel',.017,18)
  eb_books(f,a+.12,a+w*.60,.43,rows=3)
  # Window-sized line artwork keeps its silhouette without copying source pixels.
  for xx,flip in [(a+w*.25,1),(a+w*.52,-1)]:
   pts=[(xx-.20,1.0),(xx-.28,1.36),(xx-.04,1.62),(xx+.20,1.51),(xx+.34,1.73),(xx+.26,1.21),(xx+.08,.98)]
   for p,q in zip(pts,pts[1:]+pts[:1]):f.line((*p,-.025),(*q,-.025),.014,'store09 paper')
  f.b(a+w*.84,.61,-.69,w*.22,1.03,.37,'eb plywood')
 elif k=='daveys':
  eb_panel(f,a,b,2.45,.62,'eb white wood',.22)
  letters='ICE CREAM';colors=['eb pink enamel','eb yellow enamel','eb cyan enamel','eb purple enamel']
  for j,t in enumerate(letters):
   if t!=' ':eb_text(f,a+w*(j+.5)/len(letters),2.45,w/len(letters)*.83,.28,t,colors[j%4],.34,'bold')
  for j,mat in enumerate(colors*2):f.b(a+w*.17,.19,.12+j*.055,w*.28,.025,.055,mat)
  for j in range(7):p02_disc(f,a+w*(j+.5)/7,1.92,.025,.025,-.10,colors[j%4],12)
  f.b(a+w*.66,.64,-.64,w*.60,.82,.43,'eb white wood');f.b(a+w*.66,1.07,-.63,w*.61,.045,.47,'eb silver metal')
  eb_board(f,a+w*.20,.18,'ICE|CREAM','eb turquoise wood',d=.94)
  for xx in [a+w*.22,a+w*.76]:eb_lamp(f,xx,2.86,.45,'eb white wood')
 elif k=='shw':
  eb_panel(f,a,b,3.24,.38,'eb white wood');nb_grille(f,a+.05,b-.05,.23,2.86,.16)
  for j in range(3):
   x=a+w*(.17+j*.20);f.b(x,.72,-.50,w*.15,.14,.31,'eb pale fabric');p02_ring(f,x,.90,.055,.07,-.31,'eb gold metal',.008,20)
  for x in [a+w*.25,a+w*.48]:rod(f.p(x,.8,-.61),f.p(x,1.16,-.61),.09,'eb white wood',16,r2=.05)
 elif k=='mud':
  # Three projected window panes, circle-relief kick panel and carved entry.
  for at in [.50,.70]:f.b(a+w*at,1.83,.045,.045,1.92,.09,'eb oak wood')
  for j in range(15):f.b(a+w*.64+(j-7)*w*.042,1.85,-.46,.05,1.65,.045,'eb red canvas')
  for yy in [.32,.53]:
   for j in range(4):p02_ring(f,a+w*(.36+j*.17),yy,w*.078,.105,.12,'eb cream stone',.018,22)
  ss=a+w*.14
  for side in [-1,1]:f.line((ss-side*w*.10,.37,-.05),(ss+side*w*.10,1.12,-.05),.045,'eb oak wood')
  p02_ring(f,ss,2.24,.27,.31,.06,'eb cream stone',.025,32);eb_text(f,ss,2.24,.46,.27,'MUD','eb cream stone',.09,'condensed')
  for j in range(10):
   x=a+w*(j+.5)/10;f.b(x,3.02,.18,.09,.18,.16,'eb oak wood');p02_disc(f,x,2.93,.024,.024,.26,'opal lamp',10)
  eb_panel(f,a,b,3.27,.32,'eb dark wood');p02_ring(f,c,3.27,.14,.09,.27,'eb oak wood',.025,22)
  for x in [a+.04,b-.04]:eb_lamp(f,x,2.78,.35,'eb gold metal')
  for xx in [a+.15,b-.18]:
   f.b(xx,.62,.99,.42,.065,.40,'eb red wood');f.b(xx,.92,.77,.42,.53,.045,'eb pale fabric')
   for dx in [-.15,.15]:f.line((xx+dx,.19,1.06),(xx+dx,.61,1.06),.015,'eb iron')
 elif k in ['raw','artray']:
  # Only source-supported physical composition; obscured branding remains absent.
  eb_panel(f,a,b,3.20,.36,'eb dark wood');nb_grille(f,a+.06,b-.06,.22,2.84,.16)
  if k=='raw':eb_bottles(f,a+.16,a+w*.66,.62,rows=2)
  else:
   for j in range(3):
    xx=a+w*(.43+j*.18);f.b(xx,1.36,-.48,.36,.49,.03,'eb pale fabric');shop09_frame(f,xx,1.36,.39,.53,-.45,'eb oak wood',.022)
 elif k=='farm':
  eb_canopy(f,a,b,'eb blue canvas','24 HR GROCERY','bold',y=3.71,drop=.55,dep=1.0)
  eb_text(f,c,3.05,w*.89,.16,'GROCERIES • DAIRY • BEER • FRESH PRODUCE','store09 paper',1.13,'condensed')
  for j in range(7):
   xx=a+w*(j+.5)/7;f.b(xx,1.65,.03,w/7-.04,2.42,.06,'eb white wood' if j<4 else 'eb plywood')
   p03_tags(f,xx-w/15,xx+w/15,.35,1.4,.08,30+j)
  for xx in [a+w*.20,a+w*.72]:nb_ac(f,xx,2.74,.70,.38,.12)
 elif k=='mizu':
  eb_panel(f,a,b,3.22,.46);eb_text(f,c,3.23,w*.82,.26,'Mizu Sushi','store09 paper',.26,'script')
  f.b(c,1.54,.02,w-.12,2.4,.04,'eb gray metal')
  for j in range(33):f.b(c,.27+j*.072,.06,w-.13,.009,.015,'eb iron')
  p03_tags(f,a+.10,b-.10,.40,1.60,.09,350)
 elif k=='rafael':
  eb_panel(f,a,b,3.31,.47,'eb gold metal');eb_text(f,c,3.32,w*.94,.24,"RAFAEL’S BARBER SHOP",'eb dark wood',.27,'condensed')
  for j in range(18):
   xx=a+w*j/18;mat=['eb red wood','eb white wood','eb blue metal'][j%3]
   face([f.p(xx,3.04,.12),f.p(xx+w/18,3.04,.12),f.p(xx+w/18,2.88,.60),f.p(xx,2.88,.60)],mat)
  for row in range(2):
   for col in range(4):
    xx=a+w*(.10+col*.14);yy=1.02+row*.62;f.b(xx,yy,-.04,w*.12,.53,.018,'store09 paper');p02_disc(f,xx,yy+.07,.065,.10,-.02,'eb brown stone',16);f.b(xx,yy-.11,-.02,.15,.12,.015,'eb dark wood')
  for j in range(12):f.b(b-.04,1.18+j*.08,.36,.13,.08,.15,['eb red wood','store09 paper','eb blue metal'][j%3])
  for yy in [1.14,2.17]:p02_disc(f,b-.04,yy,.11,.10,.36,'eb gold metal',16)
 elif k in ['vintage9','morocco','cloak','ricebird','ladywong','sushikai']:
  if k=='vintage9':
   eb_panel(f,a,b,2.37,.37,'eb white wood',.37);eb_text(f,c,2.37,w*.91,.16,'9TH STREET VINTAGE','eb dark wood',.48,'serif');nb_grille(f,a+.04,b-.04,.20,1.92,.15,True);eb_clothes(f,a+.14,a+w*.69,1.80)
  elif k=='morocco':
   eb_canopy(f,a,b,'eb red canvas','Tribes of Morocco','serif',y=2.75,drop=.39,dep=.76,letter='eb gold metal');f.b(c,1.16,.03,w-.13,1.77,.04,'eb iron')
   for j in range(22):f.b(c,.32+j*.075,.06,w-.14,.009,.012,'eb gray metal')
  elif k=='cloak':
   eb_panel(f,a,b,2.42,.38,'eb white wood',.37);eb_text(f,c,2.42,w*.92,.16,'CLOAK & DAGGER','eb red wood',.48,'serif');nb_grille(f,a+.06,b-.06,.19,1.92,.15);eb_blade(f,a+.05,2.75,'C & D',round=True);eb_clothes(f,a+.12,a+w*.62,1.78)
   for x in [a+.10,b-.10]:eb_plant(f,x,.18,.88,.34)
  elif k=='ricebird':
   eb_canopy(f,a,b,'eb black canvas','RICE BIRD','sans',y=2.78,drop=.40,dep=.80)
   for j in range(3):
    xx=a+w*(.42+j*.20);f.b(xx,1.17,-.07,.35,.57,.02,'store09 paper');p02_disc(f,xx,1.20,.12,.10,-.05,'eb yellow wood',20)
   for j in range(7):p02_disc(f,a+w*(j+.5)/7,2.26,.035,.035,.92,'opal lamp',12)
  else:
   eb_canopy(f,a,b,'eb taupe canvas','LADY WONG' if k=='ladywong' else 'SUSHI KAI','serif',y=2.78,drop=.40,dep=.80,letter='eb gold metal')
   eb_blade(f,b-.06,2.91,'',round=True,icon='pineapple' if k=='ladywong' else 'flower')
   if k=='ladywong':
    for j in range(5):
     xx=a+w*(.12+j*.12);f.b(xx,.68,-.42,.20,.13,.20,['eb pink enamel','eb yellow wood','eb green wood'][j%3]);f.b(xx,.78,-.42,.18,.05,.18,'eb pale fabric')
   else:eb_bottles(f,a+w*.37,b-.15,.77,rows=1)
 elif k=='anme':
  eb_panel(f,a,b,3.23,.40,'eb blue metal');eb_text(f,c,3.23,w*.33,.18,'an.mé','eb gold metal',.27,'serif')
  f.b(c,1.53,.02,w-.10,2.42,.04,'eb gray metal')
  for j in range(32):f.b(c,.30+j*.073,.06,w-.12,.009,.012,'eb iron')
  p03_tags(f,a+.13,b-.13,.45,1.5,.08,328)
 elif k=='pillowcat':
  eb_canopy(f,a,b,'eb green canvas','Pillow-Cat Books','script',y=3.54);nb_grille(f,a+.05,b-.05,.25,2.83,.13)
  eb_text(f,c,1.53,w*.84,.34,'BOOKS','eb pink enamel',-.04,'bold');eb_books(f,a+.13,b-.13,.57,rows=3)
  p02_disc(f,b-w*.12,3.30,.095,.065,.63,'store09 paper',20)
  for dx in [-.05,.05]:face([f.p(b-w*.12+dx,3.35,.63),f.p(b-w*.12+dx-.03,3.44,.63),f.p(b-w*.12+dx+.03,3.40,.63)],'store09 paper')
 elif k=='jane':
  eb_panel(f,a,b,3.22,.40,'eb yellow wood');eb_text(f,c,3.22,w*.62,.23,'JANE','eb dark wood',.27,'serif')
  for row in range(3):
   yy=.73+row*.48;f.b(a+w*.66,yy-.09,-.48,w*.53,.035,.29,'eb white wood')
   for j in range(3):
    xx=a+w*(.46+j*.18);p02_ring(f,xx,yy+.13,.10,.13,-.27,'eb gray stone',.025,24);rod(f.p(xx,yy-.01,-.36),f.p(xx,yy+.12,-.36),.08,'eb cream stone',16,r2=.13)
 elif k in ['duo','cerney','sakaya']:
  if k=='duo':
   eb_panel(f,a,b,3.23,.35,'eb white wood');eb_text(f,a+w*.35,1.99,w*.30,.17,'DUO','eb gold metal',-.04,'sans');eb_clothes(f,a+.14,a+w*.60,2.25)
  elif k=='cerney':
   eb_panel(f,a,b,3.20,.43,'eb oak wood');eb_text(f,c,3.20,w*.93,.18,'D. L. CERNEY','eb gold metal',.26,'serif');nb_grille(f,a+.05,b-.05,.21,2.81,.16,True);eb_clothes(f,a+.15,b-.15,2.35)
   for j in range(9):p02_ring(f,a+w*(j+.5)/9,3.08,.045,.04,.27,'eb brown stone',.012,12)
  else:
   eb_panel(f,a,b,3.23,.35,'eb white wood');eb_blade(f,b-.10,3.21,'SAKAYA','eb oak wood');nb_grille(f,a+.05,b-.05,.22,2.81,.14);eb_bottles(f,a+w*.35,b-.15,.63,rows=4)
 elif k in ['318east','sustainable']:
  eb_panel(f,a,b,3.31,.38,'eb dark wood');nb_grille(f,a+.04,b-.04,.22,2.96,.16)
  for x in [a+.055,b-.055]:
   f.b(x,1.69,.11,.11,2.80,.15,'eb oak wood')
   for yy in [.42,2.84]:p02_ring(f,x,yy,.065,.10,.20,'eb oak wood',.019,20)
  if k=='318east':
   for x in [a+w*.16,a+w*.37,a+w*.56]:eb_plant(f,x,.60,-.37,.50)
  else:
   eb_blade(f,a+.04,3.0,'SUSTAINABLE','eb white wood',color='eb green wood');eb_bottles(f,a+w*.39,b-.10,.75,rows=3,colors=['eb white wood','eb oak wood','store09 bottle green'])
   f.b(a+w*.65,.53,.65,w*.51,.065,.34,'eb green wood')
   for xx in [a+w*.44,a+w*.85]:f.b(xx,.35,.65,.06,.35,.30,'eb green wood')
   eb_board(f,a+w*.32,.18,'ZERO WASTE|Refill!|eco-goods',d=1.15);eb_plant(f,b-.04,.18,.83,.65)
 elif k in ['cobblestones','314west']:
  if k=='cobblestones':eb_canopy(f,a,b,'eb gray canvas','COBBLESTONES','serif',y=3.48,stripes=True);eb_clothes(f,a+.12,b-.12,2.3)
  else:eb_panel(f,a,b,3.24,.32,'eb gray metal');eb_blade(f,b-.05,3.04,'','eb white wood')
  nb_grille(f,a+.05,b-.05,.23,2.80,.14)
  if k=='314west':
   f.b(c,1.50,.02,w-.11,2.4,.04,'eb gray metal')
   for j in range(32):f.b(c,.30+j*.075,.06,w-.12,.009,.012,'eb silver metal')
 elif k=='headdress':
  eb_panel(f,a,b,3.26,.32,'eb white wood');eb_text(f,c,2.58,w*.86,.13,'HEADDRESS','eb dark wood',.04,'sans')
  for at in [.24,.54]:f.b(a+w*at,1.56,.05,.026,2.12,.05,'eb white wood')
  f.b(c,1.35,.05,w-.08,.028,.05,'eb white wood');nb_ac(f,b-.35,2.91,.60,.33,.04)
  f.b(a+w*.32,1.55,-.91,.75,1.65,.025,'seventh reflective glass');shop09_frame(f,a+w*.32,1.55,.79,1.70,-.88,'eb gold metal',.028)
  f.b(a+w*.35,.63,-.40,.48,.12,.43,'eb dark wood');f.b(a+w*.35,.97,-.66,.48,.60,.08,'eb dark wood');rod(f.p(a+w*.35,.18,-.42),f.p(a+w*.35,.60,-.42),.055,'eb silver metal',12)
 elif k=='cabin':
  eb_panel(f,a,b,3.26,.45);eb_text(f,c,3.26,w*.88,.22,'Cabin on 9th','store09 paper',.26,'script')
  for xx in [a+w*.44,a+w*.66,a+w*.87]:eb_plant(f,xx,.57,-.30,.42)
  eb_books(f,a+w*.35,b-.12,.67,-.77,2)
 elif k=='veselka':
  # Large divided frontage, food-name strip and individual shallow dining bays.
  eb_panel(f,a,b,4.38,.35,'eb gold metal')
  labels=['LATKES','BLINTZES','PIEROGI','VESELKA','BORSCHT','PIEROGI','BLINTZES']
  for j,t in enumerate(labels):
   x=a+w*(j+.5)/len(labels);eb_text(f,x,4.38,w/len(labels)*.74,.23,t,'eb red wood',.27,'serif');eb_lamp(f,x,4.10,.54)
  for j in range(14):
   x=a+w*(j+.5)/14;f.b(x,1.70,-.99,w/14-.12,2.02,.03,['eb yellow wood','eb red wood','eb green wood'][j%3]);p02_disc(f,x,2.83,.17,.17,-.68,'opal lamp',24)
   f.b(x,1.02,-.48,1.25,.06,.52,'eb oak wood')
   for dx in [-.41,.41]:f.b(x+dx,.56,-.39,.34,.06,.35,'eb dark wood')
  f.b(c,2.08,.04,w-.08,.045,.07,'eb green wood')

def eb_cornice(f,h,spec):
 kind=spec['cornice'];mat='eb '+spec.get('corniceColor','dark wood')
 if kind=='carriage':return
 if kind in ['plain','stepped','veselka']:
  f.strip(h-.10,.17,.11,spec['trim'])
  if kind=='stepped':
   f.b(f.L*.5,h+.14,.035,f.L*.58,.40,.09,spec['trim']);f.b(f.L*.5,h+.37,.035,f.L*.31,.15,.09,spec['trim'])
  return
 levels=[(h-.67,.16,.20),(h-.42,.23,.30),(h-.21,.12,.48),(h+.01,.12,.60)]
 if kind=='simple':levels=[(h-.27,.14,.22),(h-.08,.16,.36)]
 for yy,hh,dep in levels:f.strip(yy,hh,dep,mat)
 if kind!='simple':
  count=max(5,round(f.L/.60))
  for j in range(count):
   x=.15+(f.L-.30)*j/(count-1)
   for yy,ww,hh,dep in [(h-.48,.13,.40,.35),(h-.28,.18,.18,.49),(h-.15,.22,.10,.60)]:f.b(x,yy,dep/2,ww,hh,dep,mat)
   p02_ring(f,x,h-.46,.049,.08,.37,mat,.014,14)
  for j in range(round(f.L/.17)):f.b((j+.5)*.17,h-.72,.13,.08,.11,.17,mat)
 if kind in ['raised-rosette','juliette']:
  c=f.L*.5;ww=f.L*.24
  face([f.p(c-ww,h-.15,.28),f.p(c,h+.47,.28),f.p(c+ww,h-.15,.28)],mat)
  for side in [-1,1]:f.line((c+side*ww,h-.15,.35),(c,h+.47,.35),.045,mat)
  if kind=='juliette':eb_text(f,c,h-.40,f.L*.42,.20,'JULIETTE','store09 paper',.32,'serif')
  else:p02_ring(f,c,h+.10,.12,.12,.32,mat,.028,24)

def eb_heads(f,r):
 spec=r['e09Block'];style=spec.get('head','none');mat=spec['trim']
 for w in r['windows']:
  if 'row' not in w:continue
  x=w['at']*f.L;original=w.get('ebOriginal',w);ww=original['width']*f.L;top=original['bottom']+original['height'];row=w['row'];col=w['col']
  if spec['number'] in ['328','324'] and row==3 and col in [0,1,4,5]:continue
  if style in ['none'] or spec.get('modern'):continue
  if w.get('ebInfill'):
   fidelity_clipped_surface(f,x-ww/2,x+ww/2,original['bottom'],top,-.04,.035,r['wall'])
  f.b(x,w['bottom']-.06,.12,ww+.22,.12,.27,mat)
  if style in ['segmental','round-second','segmental-first'] and (style=='segmental' or (style=='round-second' and row==1) or (style=='segmental-first' and row==0)):
   eb_arc(f,x,top+.06,ww*.65,.22,.22,.065,mat,24)
   for dx in [-ww*.62,ww*.62]:f.b(x+dx,top+.05,.12,.16,.20,.24,mat)
  else:
   for yy,hh,dd,wide in [(top+.08,.15,.20,ww+.20),(top+.20,.07,.31,ww+.33)]:f.b(x,yy,dd/2,wide,hh,dd,mat)
  ped=(style=='pediment-first' and row==0) or (style=='alternating-pediment' and row in [0,2]) or (style=='paired-pediment' and row in [0,2] and col in [1,2])
  if ped:
   face([f.p(x-ww*.67,top+.23,.17),f.p(x,top+.49,.17),f.p(x+ww*.67,top+.23,.17)],mat)
   for side in [-1,1]:f.line((x+side*ww*.67,top+.23,.23),(x,top+.49,.23),.032,mat)
  if style=='beaded':
   for side in [-1,1]:
    for j in range(int(w['height']/.13)):p02_disc(f,x+side*(ww/2+.08),w['bottom']+.07+j*.13,.025,.035,.16,mat,8)
  if style=='keystone':f.b(x,top+.12,.14,.18,.30,.23,mat)
  if style in ['terracotta','banded']:
   for yy in [w['bottom']-.23,top+.35]:fidelity_clipped_surface(f,max(0,x-ww*.75),min(f.L,x+ww*.75),yy,yy+.12,.08,.12,mat)
   if style=='terracotta' and row in [0,2]:
    eb_arc(f,x,top+.15,ww*.66,.27,.24,.06,mat,24);p02_ring(f,x,top+.42,.065,.08,.25,mat,.02,18)
  if (spec.get('carvedPanels') and row>0) or (spec.get('aprons') and row==1):
   yy=w['bottom']-.48;shop09_frame(f,x,yy,ww*.78,.33,.10,mat,.028)
   if style in ['beaded','terracotta'] or spec.get('aprons'):
    for j in range(4):p02_ring(f,x+(j-1.5)*ww*.16,yy,.05,.08,.13,mat,.014,12)
  if spec.get('checker') and row in [1,2] and col in [0,3]:
   for j in range(5):
    for q in range(3):
     if (j+q)%2==0:f.b(x+(j-2)*.13,w['bottom']-.50+(q-1)*.12,.065,.11,.10,.08,mat)

def eb_individual_relief(f,r,h):
 spec=r['e09Block'];num=spec['number'];mat=spec['trim'];upper=[w for w in r['windows'] if 'row' in w]
 # Continuous horizontal stonework has its own depth, interrupted by openings.
 if num in ['342','348','318','314–316','312','315']:
  rows=sorted({w['row'] for w in upper})
  for row in rows:
   wins=[w for w in upper if w['row']==row];low=min(w['bottom'] for w in wins);top=max(w['bottom']+w['height'] for w in wins)
   levels=[low-.17,top+.29] if num in ['342','348'] else [low-.22]
   for yy in levels:fidelity_clipped_surface(f,0,f.L,yy,yy+.11,.12,.12,mat)
   if num=='348':
    for j in range(round(f.L/.18)):f.b((j+.5)*.18,low-.32,.15,.085,.10,.18,mat)
 if num in ['344','310','340','317','348']:
  fidelity_courses(f,spec['upperBottom']-.16,'eb '+spec.get('groundPaint','brown stone' if num in ['344','310'] else 'cream stone'),step=.47,bottom=.18,depth=.085)
 if num in ['328','324']:
  f=FidelityProjectedFacade(f,.28)
  # Two-storey outer pilasters and a single broad arch across each paired bay.
  by={(w['row'],w['col']):w for w in upper}
  for left in [0,4]:
   pair=[by[(3,left)],by[(3,left+1)]];a=pair[0]['at']*f.L-pair[0]['width']*f.L*.6;b=pair[1]['at']*f.L+pair[1]['width']*f.L*.6
   shoulder=max(w['bottom']+w['height'] for w in pair)-.16;rx=(b-a)/2
   eb_arc(f,(a+b)/2,shoulder,rx,.64,.19,.095,mat,32)
   for x in [a,b]:
    lo=by[(1,left)]['bottom']-.16
    f.b(x,(lo+shoulder)/2,.10,.17,shoulder-lo,.20,mat)
    for yy in [lo,by[(2,left)]['bottom']-.10,shoulder]:f.b(x,yy,.15,.29,.18,.32,mat)
   f.b((a+b)/2,shoulder+.63,.22,.23,.39,.30,mat)
  for w in upper:
   if w['row']==4:continue
   x=w['at']*f.L;top=w['bottom']+w['height'];ww=w['width']*f.L
   if not (w['row']==3 and w['col'] in [0,1,4,5]):
    f.b(x,top+.23,.23,.25,.32,.28,mat)
    for dx in [-.07,.07]:p02_ring(f,x+dx,top+.32,.046,.10,.39,mat,.018,16)
    for side in [-1,1]:
     p02_ring(f,x+side*ww*.49,top+.17,.075,.075,.25,mat,.018,18)
  yy=by[(1,0)]['bottom']-.28;f.strip(yy,.17,.34,mat)
  for j in range(round(f.L/.16)):f.b((j+.5)*.16,yy-.16,.16,.07,.16,.22,mat)
  f=f.base
 if num=='317':
  for w in upper:
   if w['row']!=1:continue
   x=w['at']*f.L;yy=w['bottom']-.48
   for side in [-1,1]:
    eb_arc(f,x+side*.14,yy,.13,.07,.19,.018,mat,16)
    p02_ring(f,x+side*.29,yy,.06,.08,.18,mat,.018,16)
 # Carved portal blocks are individually opted into the observed entrances.
 for d in r['doors']:
  if num not in ['315','348','310','146 Second Avenue','331','325','307','320']:continue
  x=d['at']*f.L;ww=d['width']*f.L;bottom=d['bottom'];top=d['top'];shoulder=top-ww*.5 if d.get('shape')=='round' else top
  trim='eb carved stone' if num in ['310','325','146 Second Avenue'] else d.get('trim',mat)
  if num in ['315','348','310','325','146 Second Avenue']:
   for side in [-1,1]:
    xx=x+side*(ww/2+.21)
    f.b(xx,(bottom+shoulder)/2,.18,.25,shoulder-bottom,.37,trim)
    f.b(xx,shoulder-.15,.18,.37,.31,.42,trim)
    for off in [-.09,0,.09]:p02_ring(f,xx+off,shoulder-.09,.055,.08,.41,trim,.019,16)
    for yy in [bottom+.14,shoulder-.36]:f.b(xx,yy,.20,.43,.12,.48,trim)
   if d.get('shape')=='round':
    eb_arc(f,x,shoulder,ww/2+.27,ww/2+.27,.22,.085,trim,32)
    f.b(x,top+.18,.23,.25,.36,.40,trim)
    for j in range(9):
     a=(j+.5)*math.pi/9;f.line((x+math.cos(a)*(ww/2+.20),shoulder+math.sin(a)*(ww/2+.20),.32),(x+math.cos(a)*(ww/2+.35),shoulder+math.sin(a)*(ww/2+.35),.32),.012,'eb gray stone')
   if num=='146 Second Avenue':
    for side in [-1,1]:eb_lamp(f,x+side*(ww/2+.30),top-.30,.42)
  if num=='331':eb_lamp(f,x,top+.20,.28,'eb white wood')
  if num=='307':
   for j in range(5):p02_ring(f,x+(j-2)*ww*.15,top-.24,.07,.13,-.09,'eb iron',.012,20)
  if num=='320':
   nb_grille(f,x-ww*.46,x+ww*.46,bottom+.12,top-.09,-.18,True)
   for side in [-1,1]:eb_lamp(f,x+side*(ww/2+.25),2.62,.28)
 if num=='146 Second Avenue':
  # Visible recessed fire-escape silhouette in the open gap; depth is estimated.
  a=f.L+.18;b=f.L+2.45
  for row in range(3):
   yy=4.0+row*2.8
   for dd in [-5.6,-6.4]:f.line((a,yy+.75,dd),(b,yy+.75,dd),.018,'eb iron')
   for j in range(12):
    xx=a+(b-a)*j/11;f.line((xx,yy,-5.6),(xx,yy+.75,-5.6),.012,'eb iron');f.line((xx,yy,-5.6),(xx,yy,-6.4),.018,'eb iron')
   for j in range(12):
    t=j/11;xx=a+(b-a)*t;f.line((xx,yy+t*2.8,-6.2),(xx,yy+t*2.8,-6.8),.023,'eb iron')

def eb_access(f,r):
 spec=r['e09Block'];entry=spec.get('access');mat=spec['trim']
 # Explicit wells are cut from runtime pavement; none is a black painted rectangle.
 for well in r['observedGround'].get('basementAreaways',[]):
  x=well['at']*f.L;ww=well['width']*f.L;dep=well['depth'];below=well['depthBelow']
  f.b(x,-below,dep/2,ww,.08,dep,mat)
  for xx in [x-ww/2,x+ww/2]:f.b(xx,-below/2,dep/2,.055,below,dep,mat)
  f.b(x,-below/2,dep,ww,below,.055,mat)
  for yy in [.22,.94]:f.line((x-ww/2,yy,dep),(x+ww/2,yy,dep),.021,'eb iron')
  for j in range(max(2,round(ww/.14))+1):
   xx=x-ww/2+ww*j/max(2,round(ww/.14));f.line((xx,-.04,dep),(xx,.94,dep),.011,'eb iron')
 if not entry:return
 x=entry['at']*f.L;ww=entry['width'];rise=entry['rise'];dep=entry['depth'];n=max(1,round(max(0,rise-.16)/.17))
 for j in range(n):
  top=.17+(rise-.17)*(j+1)/n;dd=dep*(n-j-.5)/n
  f.b(x,top/2,dd,ww,top,dep/n+.01,mat)
 if rise>.35:
  for side in [-1,1]:
   xx=x+side*(ww/2-.04);f.line((xx,rise+.83,.08),(xx,1.0,dep),.024,'eb iron')
   for j in range(n+1):
    t=j/n;yy=rise*(1-t)+.17*t;f.line((xx,yy,dep*t),(xx,yy+.83,dep*t),.013,'eb iron')

def eb_garage(f,spec):
 a,b=[x*f.L for x in spec['garageSpan']];k=spec['number'];top=3.35 if k=='327' else 3.1;mat='eb white wood' if k=='327' else 'eb red metal' if k=='338' else 'eb gray metal'
 fidelity_opening(f,(a+b)/2,.17,b-a,top-.17,mat='eb gray stone' if k=='327' else mat,d=-.11)
 if k=='336':
  for j in range(3):
   x=a+(b-a)*(j+.5)/3;ww=(b-a)/3-.045
   shop09_frame(f,x,1.62,ww,2.84,-.045,mat,.045)
   for side in [-1,1]:f.line((x-side*ww*.40,.30,-.015),(x+side*ww*.40,1.40,-.015),.032,mat)
   for col in range(2):
    for row in range(3):f.b(x+(col-.5)*ww*.44,1.73+row*.45,-.08,ww*.40,.40,.022,'eb red wood')
 else:
  for row in range(4):
   for col in range(4):
    x=a+(b-a)*(col+.5)/4;yy=.17+(top-.17)*(row+.5)/4;ww=(b-a)/4-.08;hh=(top-.17)/4-.07
    shop09_frame(f,x,yy,ww,hh,.055,mat,.055)
    if k=='327':f.b(x,yy,-.075,ww-.07,hh-.07,.025,'eb white wood')
    if k=='338':
     f.b(x,yy,.005,ww-.08,hh-.08,.024,'eb red wood')
     for q in range(4):
      for j in range(6):f.b(x+(j-2.5)*ww/7,yy+(q-1.5)*hh/5,.025,.014,.018,.008,'eb iron')
 if k=='338':
  eb_lamp(f,(a+b)/2,3.66,.34,'eb white wood');f.b(b-.25,2.23,.09,.43,.38,.025,'store09 paper');eb_text(f,b-.25,2.24,.37,.10,'NO PARKING','eb red wood',.11,'condensed')

def eb_shelter(f,a,b,kind):
 # Bounded curb-side structures, preserving the clear sidewalk behind them.
 d=3.40;dep=1.55;w=b-a;count=max(2,round(w/2.1));ve=kind=='veselka'
 for j in range(count):
  x0=a+w*j/count;x1=a+w*(j+1)/count;c=(x0+x1)/2;mat=('eb blue enamel' if j%2 else 'eb yellow enamel') if ve else 'eb red wood'
  f.b(c,.65,d+dep/2,x1-x0-.035,.92,.065,mat)
  for xx in [x0,x1]:f.b(xx,1.42,d,.07,2.5,.07,'eb oak wood');f.b(xx,1.42,d+dep/2,.07,2.5,.07,'eb oak wood')
  f.b(c,2.54,d+dep/2,x1-x0,.12,.12,'eb blue enamel' if ve else 'eb red wood')
  for k in range(max(1,int((x1-x0)/.10))):
   x=x0+k*.10
   roof=[f.p(x,2.63,d-.70),f.p(x+.10,2.63,d-.70),f.p(x+.10,2.49,d+.85),f.p(x,2.49,d+.85)]
   face(roof,'eb silver metal');face(roof[::-1],'eb silver metal');f.line((x,2.64,d-.70),(x,2.50,d+.85),.012,'eb gray metal')
  if ve:
   f.b(c,1.17,d+dep/2,x1-x0-.08,.17,.32,'eb green wood')
   for q in range(12):
    xx=x0+(x1-x0)*(q+.5)/12
    for off in [-.10,.02,.13]:
     p02_disc(f,xx,1.43+off*.35,.13,.10,d+dep/2+off,'store09 bottle green',10)
     face([f.p(xx-.10,1.45,d+dep/2+off),f.p(xx,1.61,d+dep/2+off-.08),f.p(xx+.10,1.45,d+dep/2+off)],'eb green wood')
   f.b(x0,1.34,d,.05,1.40,1.28,'eb plywood');eb_text(f,c,1.8,x1-x0-.32,.18,['PIEROGI','BLINTZES','BORSCHT','BON APPETIT'][j%4],'eb red wood',d-.67,'serif')
  f.b(c,.90,d,1.18,.065,.58,'eb oak wood')
  for xx in [c-.38,c+.38]:f.b(xx,.50,d+.42,.36,.065,.33,'eb dark wood')

_eb_previous_render=render_building
def render_building(b):
 if b['id'] not in E09_BLOCK_IDS:return _eb_previous_render(b)
 idx=1 if b['id']==241822210 else 0;r=b['firstStmarksArchitecture'][str(idx)];spec=r['e09Block'];h=b['firstStmarksHeight'];b['renderHeight']=h
 owner(str(b['id'])+' E09 observed block');v=spec.get('effectiveFace',b['frontages'][idx]);f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']);f.wall=r['wall']
 clone={**b,'frontages':list(b['frontages'])};clone['frontages'][idx]=v
 if spec.get('carriage'):clone['renderHeight']=h-.64
 wall_mass(clone,r['wall'],False)
 clean=deepcopy(r);clean['observedGround']['basementAreaways']=[]
 if spec.get('modern'):
  for w in clean['windows']:
   if 'row' in w:w['rails']=[]
 fidelity_elevation({**b,'businesses':[],'seventhArchitecture':clean},f,clean)
 if paint:=spec.get('groundPaint'):shop09_face(f,{'paintSurround':{'bottom':.17,'top':spec['upperBottom']-.15,'material':'eb '+paint}})
 elif r['returnShops'] and spec['number'] not in ['144 Second Avenue','305']:shop09_face(f,{'paintSurround':{'bottom':.17,'top':3.35,'material':'eb dark wood'}})
 eb_heads(f,r);eb_individual_relief(f,r,h);eb_cornice(f,h-2.7 if spec.get('roofAddition') else h,spec);eb_access(f,r)
 if spec.get('escape'):p02_escape(f,spec['escape'])
 for w in r['windows']:
  if 'row' not in w:continue
  x=w['at']*f.L;ww=w['width']*f.L;y=w['bottom'];hh=w['height']
  if spec.get('modern'):
   for dx in [-ww*.23,ww*.23]:f.b(x+dx,y+hh/2,-.08,.045,hh,.08,'eb gray metal')
   for dx in [-ww*.365,ww*.365]:f.b(x+dx,y+hh*.47,-.06,ww*.27,.035,.07,'eb gray metal')
   f.b(x,y-.40,.025,ww*.63,.30,.045,'eb gray metal')
   for j in range(6):f.b(x,y-.51+j*.045,.052,ww*.60,.009,.012,'eb iron')
  elif spec['number']=='327':
   for dx in [-ww*.16,ww*.16]:f.b(x+dx,y+hh/2,-.07,.04,hh,.06,'eb sash')
   if w['row'] in [1,3]:
    for yy in [y+.08,y+.84]:f.line((x-ww*.52,yy,.23),(x+ww*.52,yy,.23),.018,'eb iron')
    for j in range(9):f.line((x-ww*.5+j*ww/8,y+.08,.23),(x-ww*.5+j*ww/8,y+.84,.23),.009,'eb iron')
  elif spec['number']=='319':f.b(x,y+hh/2,-.065,.055,hh,.08,'eb sash')
  # Individually observed units only; no repeated invented curtain cadence.
  if [w['row'],w['col']] in spec.get('windowAC',[]):nb_ac(f,x,y+.16,min(.67,ww*.76),.36,.16)
  for treatment in spec.get('windowDressing',[]):
   if treatment['row']==w['row'] and treatment['col']==w['col']:
    if treatment['type']=='blind':
     f.b(x,y+hh*.62,-.125,ww-.10,hh*.68,.015,'eb pale fabric')
     for j in range(int(hh*.68/.055)):f.b(x,y+hh*.28+j*.055,-.112,ww-.11,.010,.008,'eb gray metal')
    else:
     for dx in [-ww*.33,ww*.33]:
      for j in range(4):f.b(x+dx+(j-1.5)*.033,y+hh/2,-.125,.029,hh-.12,.014,'eb pale fabric')
 if spec.get('quoins'):
  for x in [.13,f.L-.13]:
   for j in range(round((h-3.7)/.42)):f.b(x,3.8+j*.42,.055,.27 if j%2 else .43,.37,.10,spec['trim'])
 if spec.get('roofRail') or spec.get('roofAddition'):
  for j in range(round(f.L/.15)+1):f.line((j*.15,h,.06),(j*.15,h+.70,.06),.009,'eb iron')
  f.line((0,h+.70,.06),(f.L,h+.70,.06),.019,'eb iron')
 if spec.get('garageSpan'):eb_garage(f,spec)
 if spec.get('carriage'):
  # Shallow sloped central cap and the actual stepped side shoulders.
  for a,end,top in [(0,.15,h-.19),(.15,.33,h-.27),(.67,.85,h-.27),(.85,1,h-.19)]:f.b(f.L*(a+end)/2,(h-.64+top)/2,.035,f.L*(end-a),top-(h-.64),.10,r['wall'])
  cap=[f.p(f.L*.33,h-.64,.08),f.p(f.L*.33,h-.22,.08),f.p(f.L*.50,h-.04,.08),f.p(f.L*.67,h-.22,.08),f.p(f.L*.67,h-.64,.08)]
  face(cap,r['wall']);face(cap[::-1],r['wall'])
  for side in [-1,1]:f.line((f.L*.50+side*f.L*.17,h-.22,.13),(f.L*.50,h-.04,.13),.035,'eb gray stone')
  for radius in [.12,.20]:p02_ring(f,f.L*.50,h-.59,radius,radius,.10,'eb buff stone',.025,4)
  # The dentil/zigzag frieze sits BELOW the upper windows.
  for yy in [3.63,3.82]:f.strip(yy,.075,.11,'eb buff stone')
  for j in range(round(f.L/.22)):
   x=(j+.5)*.22;f.b(x,3.53,.07,.10,.14,.14,'eb buff stone')
   for k in range(3):f.b(x+(k-1)*.065,3.94+(1-abs(k-1))*.07,.07,.075,.08,.12,'eb buff stone')
  winright={'at':.89,'width':.18,'bottom':1.52,'height':1.7,'trim':'eb gray metal','frame':'eb gray metal','hood':'none'};fidelity_window(f,winright)
  for at in [.84,.93]:p02_ring(f,f.L*at,.62,.11,.11,.11,'eb iron',.024,20)
  nb_ac(f,f.L*.625,4.16,.57,.38,.05)
 if spec.get('scaffold'):
  # Gray mesh with sparse diagonal structure, explicitly dated 2024 construction.
  for x in [.12,f.L*.34,f.L*.67,f.L-.12]:
   f.line((x,.2,1.35),(x,h+.22,1.35),.026,'eb silver metal')
  for row in range(6):
   yy=2.8+row*2.15;f.line((.12,yy,1.35),(f.L-.12,yy,1.35),.022,'eb silver metal')
   for j in range(3):f.line((f.L*j/3,yy,1.34),(f.L*(j+1)/3,min(h,yy+2.15),1.34),.017,'eb silver metal')
  for j in range(round(f.L/.18)):
   f.line((j*.18,3.0,1.39),(j*.18,h,1.39),.006,'eb gray metal')
  for j in range(round((h-3)/.18)):f.line((0,3+j*.18,1.39),(f.L,3+j*.18,1.39),.006,'eb gray metal')
  eb_panel(f,0,f.L,2.93,.69,'eb green wood',1.5)
  f.b(f.L*.28,3.02,1.62,f.L*.40,.53,.035,'eb white wood');eb_text(f,f.L*.28,3.10,f.L*.36,.13,'DEAN RESTORATION','eb red wood',1.65,'bold')
  eb_text(f,f.L*.28,2.91,f.L*.30,.095,'319 EAST 9TH STREET','eb dark wood',1.65,'condensed')
  f.b(f.L*.75,3.02,1.62,f.L*.39,.53,.035,'eb white wood');eb_text(f,f.L*.75,3.05,f.L*.34,.18,'TOPLINE NYC','eb blue metal',1.65,'bold')
  # Fine dark net strips leave glimpses of the dated scaffold underneath.
  for j in range(round(f.L/.065)):
   f.b(j*.065,(h+3.3)/2,1.41,.037,h-3.3,.012,'eb iron')
  for x in [f.L*.02,f.L*.51,f.L*.98]:f.line((x,3.30,1.45),(x,h,1.45),.014,'eb red wood')
 if spec.get('veselka'):
  for w in r['windows']:
   x=w['at']*f.L;yy=w['bottom']+w['height']+.55
   if w['row']==0:
    f.b(x,w['bottom']+.30,.015,w['width']*f.L-.08,.56,.07,'eb brown metal')
    for col in range(4):
     for row in range(3):
      if (col+row)%2==0:f.b(x+(col-1.5)*.20,yy+(row-1)*.18,.035,.17,.15,.045,'eb white stone')
   else:p02_ring(f,x,h-.65,.14,.14,.05,'eb white stone',.04,4)
  eb_shelter(f,f.L*.025,f.L*.96,'veselka')
 if spec['number'] in ['334','340']:
  # Observed exposed side walls above the two low neighbors.
  s=-.015 if spec['number']=='334' else f.L+.015
  low=8.50 if spec['number']=='334' else 4.83
  dep=min(11.0,b['box'][3]-v['z'])
  pts=[f.p(s,low,0),f.p(s,low,-dep),f.p(s,h,-dep),f.p(s,h,0)]
  mat='eb white stone' if spec['number']=='334' else 'eb pink brick'
  face(pts,mat);face(pts[::-1],mat)
  if spec['number']=='334':f.line((s,low,-.50),(s,h+.70,-.50),.09,'eb silver metal')
 if spec['number']=='307':eb_shelter(f,f.L*.61,f.L*.99,'mud')
 if spec['number']=='146 Second Avenue':
  # The real 2.657 m open-air gap is outside the tall corner footprint.
  # Only its observed low green street wall is present; sky remains above.
  aa=f.L;bb=f.L+2.657;cc=(aa+bb)/2
  f.b(cc,1.35,.035,bb-aa,2.70,.12,'eb green wood')
  for x in [aa+.12,bb-.12]:
   f.b(x,1.53,.12,.20,2.94,.23,'eb green wood')
   for yy in [.28,2.65,2.93]:f.b(x,yy,.17,.31,.12,.29,'eb green wood')
  eb_panel(f,aa,bb,2.91,.28,'eb green wood')
  f.b(cc,1.41,.11,1.93,2.31,.05,'eb gray metal')
  for j in range(30):f.b(cc,.31+j*.075,.15,1.91,.012,.014,'eb iron')
 if spec.get('flag'):
  x=f.L*.72;yy=spec['upperBottom']+spec['step']+.75;f.line((x,yy,.10),(x+.48,yy-.20,1.24),.017,'eb iron')
  for j,mat in enumerate(['eb blue enamel','eb yellow enamel']):face([f.p(x+.16,yy-j*.28,.50),f.p(x+.47,yy-.15-j*.28,1.20),f.p(x+.47,yy-.43-j*.28,1.20),f.p(x+.16,yy-.28-j*.28,.50)],mat)
 for d in r['doors']:
  if d['bottom']<0:continue
  if spec['number']=='327':continue # finished entrance/number remains unobserved
  x=d['at']*f.L;label='303' if spec['number']=='146 Second Avenue' else spec['number'].split(' ')[0].split('–')[0]
  if spec['number'] not in ['338','336','314–316']:eb_text(f,x,d['top']-.19,min(.52,d['width']*f.L*.66),.14,label,'eb gold metal',-.07,'serif')
  if spec['number']=='336':
   f.b(x+.57,2.90,.08,.42,.18,.045,'eb white stone');eb_text(f,x+.57,2.90,.36,.12,'336','eb gray metal',.11,'serif')
  if spec['number']=='314–316':
   f.b(x,1.96,-.09,.34,1.50,.025,'eb white wood')
   for j,t in enumerate('314'):eb_text(f,x,2.4-j*.45,.23,.30,t,'eb dark wood',-.065,'bold')
  f.b(x+d['width']*f.L*.60,1.42,.16,.085,.21,.045,'eb iron')
  for j in range(4):f.b(x+d['width']*f.L*.60,1.36+j*.035,.19,.048,.013,.009,'eb silver metal')
 if spec['number'] in ['331','323','344','320','336']:
  for x in [f.L*.42,f.L*.62] if spec['number']=='344' else [.17,f.L-.17]:eb_lamp(f,x,3.10,.31,'eb white wood')
 for x in [.04,f.L-.04]:f.line((x,3.45,.035),(x,h-.70,.035),.007,'eb iron')
