"""Observed Ninth east-block geometry. Only explicit E09East owners dispatch here.

Source photos are never textures. Lettering, relief and murals are reproducible
authored approximations; the ledger separates observed form from estimates.
"""
E09_EAST_IDS={248142661,248142662,248142663,248142664,248142666,248142668,248142669,248142672,248142675,248142676,248142677,248142679,248142681,248142682,248142683,248142684,248142685,248142702,248142710,248142713,248142716,248142921,248142923,248142925,248142926,248142927,248142929,248142930,248142932,248142934,248142936,248142938,248142940,248142942,248142944,248142945,248142947,248142948,248142950,248142955,248142963}
for name,rgb,kind in [('coral',(.58,.34,.29),0),('sage',(.43,.49,.41),0),('pale yellow',(.76,.71,.51),0),('school green',(.35,.43,.31),2),('burgundy',(.28,.105,.13),2),('mauve canvas',(.36,.24,.29),5),('ochre canvas',(.69,.51,.25),5),('green chair',(.16,.37,.21),1),('pink letters',(.85,.39,.62),1),('bright leaf',(.15,.68,.13),1),('red orange',(.75,.21,.075),1),('blue yellow door',(.09,.28,.53),2),('deep blue',(.06,.22,.55),1)]:
 material('ee '+name,rgb,.84)
 if kind:MATS['ee '+name]['storefront09Surface']=kind

material('painted ee white brick',(.86,.87,.84),.9)
SHOP09_FONTS['slab']=SHOP09_FONTS['serif']
SHOP09_FONTS['italic']=SHOP09_FONTS['script']

def ee_ball(f,x,y,d,r,mat):
 for row in range(8):
  for col in range(12):
   points=[]
   for rr,cc in [(row,col),(row+1,col),(row+1,col+1),(row,col+1)]:
    t=-math.pi/2+rr*math.pi/8;u=cc*math.pi/6
    points.append(f.p(x+r*math.cos(t)*math.cos(u),y+r*math.sin(t),d+r*math.cos(t)*math.sin(u)))
   face(points,mat)

def ee_front(points,mat):
 face(points,mat);face(points[::-1],mat)

def ee_mat(name):return name if name.startswith(('ee ','eb ','p02 ','store09 ','painted ee ')) else 'eb '+name
def ee_frame(f,s,y,w,h,d,mat):shop09_frame(f,s,y,w,h,d,mat,.05)
def ee_scroll(f,s,y,scale,mat,d=.20):
 for side in [-1,1]:
  pts=[]
  for j in range(25):
   t=j/24*math.pi*2.2;rr=scale*(1-j/31)
   pts.append((s+side*(scale+rr*math.cos(t)),y+rr*math.sin(t)))
  p02_curve(f,pts,d,mat,.018)
def ee_hood(f,a,b,y,mat='eb gray metal',dep=.45):
 f.b((a+b)/2,y,dep/2,b-a,.16,dep,mat)
 for yy in [y-.09,y+.09]:f.b((a+b)/2,yy,dep-.025,b-a+.03,.025,.07,mat)
def ee_shutter(f,a,b,y= .19,top=2.80,mat='eb silver metal',d=.11):
 f.b((a+b)/2,(y+top)/2,d,b-a,top-y,.035,mat)
 for j in range(int((top-y)/.065)):f.b((a+b)/2,y+j*.065,d+.025,b-a,.012,.014,'eb gray metal')
 for x in [a,b]:f.b(x,(y+top)/2,d+.03,.055,top-y,.07,'eb iron')
def ee_curved(f,a,b,mat,text='',font='serif',y=3.55,drop=.62,dep=.86,letter='store09 paper',scallop=False):
 observed_awning(f,a,b,{'detail09':True,'shape':'round','y':y,'drop':drop,'depth':dep,'valance':.19,'material':mat,'scalloped':scallop,'sidePanels':False})
 # Letters lie on the vertical front valance, with a second larger sign plane
 # on the curved face placed at its actual arc depth rather than behind cloth.
 if text:
  obj=eb_text(f,(a+b)/2,y-drop*.66,(b-a)*.86,.24,text,letter,.10+dep*.94+.025,font)
  if font=='slab' and obj:obj.data.bevel_depth=.012;obj.data.bevel_resolution=0
  if obj:
   bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj;bpy.ops.object.convert(target='MESH');bpy.context.view_layer.update()
   matrix=obj.matrix_world.copy();inverse=matrix.inverted()
   for v in obj.data.vertices:
    world=matrix@v.co;fraction=max(0.,min(1.,(y-world.z)/drop));target=.10+dep*math.sqrt(max(0.,1-(1-fraction)**2))+.026
    old_depth=(world.x-f.x)*f.nx+(-world.y-f.z)*f.nz
    world.x+=f.nx*(target-old_depth);world.y-=f.nz*(target-old_depth);v.co=inverse@world
 for x in [a+.035,b-.035]:
  pts=[f.p(x,y-drop,.105)]+[f.p(x,y-drop*(1-math.cos(j*math.pi/32)),.105+dep*math.sin(j*math.pi/32)) for j in range(17)]
  face(pts,mat);face(pts[::-1],mat)
  for j in range(16):
   t=j*math.pi/32;u=(j+1)*math.pi/32
   f.line((x,y-drop*(1-math.cos(t)),.104+dep*math.sin(t)),(x,y-drop*(1-math.cos(u)),.104+dep*math.sin(u)),.008,mat)
def ee_portrait(f,s,y,w,h,d=.08):
 f.b(s,y,d,w,h,.012,'eb white wood');p02_disc(f,s,y+h*.10,w*.21,h*.24,d+.012,'eb brown stone',16)
 p02_disc(f,s,y-h*.25,w*.37,h*.25,d+.014,'eb charcoal stone',16)
 for dx in [-w*.08,w*.08]:p02_disc(f,s+dx,y+h*.12,.012,.015,d+.020,'eb iron',8)
def ee_round_table(f,s,d):
 rod(f.p(s,.91,d),f.p(s,.97,d),.32,'eb white wood',24)
 f.line((s,.19,d),(s,.91,d),.035,'eb iron')
 for dx,dz in [(.22,.20),(-.22,.20),(0,-.24)]:f.line((s,.27,d),(s+dx,.17,d+dz),.018,'eb iron')
def ee_chair(f,s,d,mat='eb oak wood',woven=False):
 f.b(s,.61,d,.36,.045,.34,mat)
 for dx in [-.15,.15]:
  for dd in [-.14,.14]:f.line((s+dx*1.2,.17,d+dd*1.2),(s+dx,.61,d+dd),.016,mat)
  f.line((s+dx,.61,d-.14),(s+dx,1.02,d-.19),.018,mat)
 for yy in [.73,.88,1.02]:f.line((s-.15,yy,d-.18),(s+.15,yy,d-.18),.015,mat)
 if woven:
  for j in range(9):
   f.line((s-.14+j*.035,.64,d-.14),(s-.14+j*.035,1.0,d-.19),.007,'ee ochre canvas')
   f.line((s-.16,.70+j*.035,d-.18),(s+.16,.70+j*.035,d-.18),.007,'ee ochre canvas')
def ee_star(f,s,y,r,d,mat):
 pts=[f.p(s+math.sin(j*math.pi/5)*r*(1 if j%2==0 else .44),y+math.cos(j*math.pi/5)*r*(1 if j%2==0 else .44),d) for j in range(10)]
 face(pts,mat);face(pts[::-1],mat)
def ee_animal(f,s,y,w,h,mat,d=.10,cat=False):
 p02_disc(f,s,y,w*.25,h*.28,d,mat,24)
 for side in [-1,1]:
  if cat:ee_front([f.p(s+side*w*.1,y+h*.2,d),f.p(s+side*w*.24,y+h*.43,d),f.p(s+side*w*.30,y+h*.12,d)],mat)
  else:p02_disc(f,s+side*w*.25,y+h*.1,w*.09,h*.22,d,mat,16)
 for side in [-1,1]:p02_disc(f,s+side*w*.08,y+h*.03,w*.022,h*.024,d+.01,'eb iron',8)
 p02_disc(f,s,y-h*.09,w*.045,h*.035,d+.012,'eb iron',10)

def ee_escape(f,e):
 if not e.get('balconyOnly'):p02_escape(f,e)
 else:
  a,b=[x*f.L for x in e['span']];mat=e['material']
  for row,y in enumerate(e['levels']):
   for dd in [.08,.90]:f.b((a+b)/2,y,dd,b-a,.065,.065,mat)
   for j in range(max(2,int((b-a)/.09))):f.b(a+j*.09,y+.015,.48,.020,.025,.85,mat)
   for x in [a,b]:
    f.b(x,y,.48,.055,.065,.90,mat);f.line((x,y-.4,.03),(x,y,.90),.022,mat)
    for yy in [y+.13,y+.91]:f.line((x,yy,.04),(x,yy,.9),.018,mat)
   for yy in [y+.13,y+.91]:f.line((a,yy,.91),(b,yy,.91),.019,mat)
   for j in range(max(2,int((b-a)/.15))+1):
    x=a+(b-a)*j/max(2,int((b-a)/.15));f.line((x,y+.04,.91),(x,y+.91,.91),.009,mat)
  if e['levels']:
   x=f.L*e.get('dropAt',.69)
   for xx in [x,x+.32]:f.line((xx,2.55,.92),(xx,e['levels'][0]+.5,.92),.016,mat)
   for j in range(max(1,int((e['levels'][0]-2.1)/.25))):f.line((x,2.55+j*.25,.92),(x+.32,2.55+j*.25,.92),.012,mat)
 if e.get('ornament')!='plain':
  a,b=[x*f.L for x in e['span']]
  for row,y in enumerate(e['levels']):
   if e['ornament']=='spindles' and row==0:continue
   count=max(2,round((b-a)/(.61 if e['ornament']=='circles' else .30)))
   for j in range(count):
    x=a+(j+.5)*(b-a)/count
    if e['ornament']=='circles':
     p02_ring(f,x,y+.52,(b-a)/count*.42,.30,.935,e['material'],.012,20)
     for side in [-1,1]:f.line((x-side*.18,y+.19,.94),(x+side*.18,y+.85,.94),.011,e['material'])
    elif e['ornament']=='spindles':
     # Upper rails have elongated linked diamonds and swollen central collars;
     # the first platform retains its observed plain vertical bars.
     p02_curve(f,[(x,y+.18),(x-.065,y+.36),(x,y+.53),(x+.065,y+.36),(x,y+.18)],.94,e['material'],.013)
     p02_curve(f,[(x,y+.53),(x-.065,y+.69),(x,y+.87),(x+.065,y+.69),(x,y+.53)],.94,e['material'],.013)
     p02_disc(f,x,y+.53,.040,.060,.945,e['material'],10)
    else:ee_scroll(f,x,y+.53,.055,e['material'],.94)

def ee_architecture(f,r,h):
 s=r['e09East'];bridge={**r,'e09Block':s};num=s['number'];mat=s['trim']
 eb_heads(f,bridge);eb_access(f,bridge)
 # Explicit inward-facing linings keep each below-grade well closed from the
 # viewing side after import/backface culling. They stay below the pavement.
 for well in r['observedGround'].get('basementAreaways',[]):
  x=well['at']*f.L;ww=well['width']*f.L;dep=well['depth'];y=-well['depthBelow']+.041
  a=x-ww/2;b=x+ww/2
  ee_front([f.p(a,y,0),f.p(b,y,0),f.p(b,y,dep),f.p(a,y,dep)],mat)
  for lo,hi in [((a,0),(a,dep)),((a,dep),(b,dep)),((b,dep),(b,0)),((b,0),(a,0))]:
   ee_front([f.p(lo[0],y,lo[1]),f.p(hi[0],y,hi[1]),f.p(hi[0],.12,hi[1]),f.p(lo[0],.12,lo[1])],mat)
 if s['cornice']=='school':
  for yy,hh,dep in [(h-.55,.14,.16),(h-.28,.24,.32),(h-.04,.14,.53)]:f.strip(yy,hh,dep,'eb gray stone')
 elif s['cornice']=='rail-blocks':
  f.strip(h-.16,.27,.13,'eb cream stone')
  for x in [.1,f.L*.5,f.L-.1]:f.b(x,h+.19,.05,.28,.65,.14,'eb cream stone')
  for yy in [h+.12,h+.43]:f.line((.1,yy,.06),(f.L-.1,yy,.06),.022,'eb iron')
 else:eb_cornice(f,s.get('streetWallHeight',h),s)
 if s.get('escape'):ee_escape(f,s['escape'])
 for w in r['windows']:
  x=w['at']*f.L;ww=w['width']*f.L;y=w['bottom'];hh=w['height'];top=y+hh
  if [w.get('row',-1),w.get('col',-1)] in s.get('windowAC',[]):nb_ac(f,x,y+.16,min(.65,ww*.73),.35,.15)
  if s.get('school'):
   for side in [-1,1]:
    for j in range(round(hh/.28)):f.b(x+side*(ww/2+.09),y+(j+.5)*hh/round(hh/.28),.07,.22 if j%2 else .32,hh/round(hh/.28)-.025,.14,'eb cream stone')
   for yy in [y-.13,top+.13]:f.b(x,yy,.10,ww+.37,.20,.22,'eb cream stone')
   if w.get('schoolPointed'):
    for side in [-1,1]:f.line((x+side*ww*.62,top+.10,.18),(x,top+.36,.18),.055,'eb cream stone')
  if s.get('head')=='curved-first' and w.get('row')==0:
   eb_arc(f,x,top+.22,ww*.68,.24,.25,.075,mat)
  if s.get('shutters') and 'row' not in w:
   for side in [-1,1]:
    xx=x+side*(ww*.65);f.b(xx,y+hh/2,.09,ww*.28,hh,.10,'eb iron')
    for j in range(int(hh/.09)):f.b(xx,y+.04+j*.09,.16,ww*.27,.025,.025,'eb sash')
 if s.get('edgeTrim'):
  for x in [.08,f.L-.08]:f.b(x,(h+3.6)/2,.04,.17,h-3.6,.08,'eb cream stone')
 if s.get('bands'):
  for row in range(s['rows']):
   yy=s['upperBottom']+row*s['step']-.36;f.strip(yy,.13,.06,'eb brown stone')
 if s.get('roofRail'):
  f.line((0,h+.6,.1),(f.L,h+.6,.1),.02,'eb iron')
  for j in range(round(f.L/.16)+1):f.line((j*.16,h,.1),(j*.16,h+.6,.1),.01,'eb iron')
 if s.get('flag'):
  x=f.L*.8;y=s['upperBottom']+s['step'];f.line((x,y,.10),(x+.4,y-.2,1.1),.018,'eb iron')
  for j,mat in enumerate(['eb blue enamel','eb yellow enamel']):ee_front([f.p(x+.1,y-j*.3,.35),f.p(x+.4,y-.1-j*.3,1.1),f.p(x+.4,y-.4-j*.3,1.1),f.p(x+.1,y-.3-j*.3,.35)],mat)
 for d in r['doors']:
  x=d['at']*f.L;label=d.get('label',num if num.replace('.','').isdigit() else '')
  if label:eb_text(f,x,d['top']-.20,min(.62,d['width']*f.L*.75),.15,label,'eb gold metal',-.07,'serif')
  f.b(x+d['width']*f.L*.62,1.40,.14,.09,.23,.04,'eb iron')
  for j in range(4):f.b(x+d['width']*f.L*.62,1.34+j*.04,.166,.05,.012,.008,'eb silver metal')
 for x in [.035,f.L-.035]:f.line((x,3.4,.03),(x,h-.65,.03),.007,'eb iron')

_ee_previous_shop=photographed_shop
def photographed_shop(f,a,b,r):
 detail=r['design'].get('detailE09East')
 if not detail:return _ee_previous_shop(f,a,b,r)
 k=detail['kind'];spec=r['design'];w=b-a;c=(a+b)/2;head=spec['head'];top=spec['top'];base=spec['base']
 if not spec.get('customShell'):
  rr=deepcopy(r)
  if k in ['fa','chiro','428east']:rr['design']['detail09']['archedPanels']=list(range(len(spec['panels'])-1))
  if k=='thursday':rr['design']['detail09']['panelFrames']={'1':'eb red wood'}
  _ee_previous_shop(f,a,b,rr)
  f.b(c,(head+base)/2,-1.05,w-.10,head-base,.035,'eb cream stone')
  for x in [a+.03,b-.03]:f.b(x,(head+base)/2,-.55,.035,head-base,1.,spec['detail09']['frame'])
 if k in ['411west','411east']:
  eb_panel(f,a,b,3.26,.35,'eb blue metal');eb_canopy(f,a,b,'nb gray canvas',y=3.16,drop=.25,dep=.43)
  for x in [a+.06,b-.06]:
   for yy in [.4,2.72,3.36]:f.b(x,yy,.12,.14,.10,.25,'eb blue metal')
  if k=='411west':nb_grille(f,a+.07,b-.07,.18,2.81,.16)
  else:
   ee_chair(f,a+w*.70,-.30,'eb white wood');eb_plant(f,a+w*.85,.18,-.45,.55)
   ee_frame(f,a+w*.68,1.75,w*.40,1.50,-.90,'eb gold metal')
 elif k=='psychic':
  ee_curved(f,a,b,'ee burgundy','Psychic','script',y=3.6,drop=.60,dep=.85)
  # Side copy on a perpendicular sign plane.
  p=f.p(a,0,.13);side=Facade(p[0],p[2],f.nx,f.nz,.77)
  eb_text(side,.39,3.1,.67,.105,'TAROT CARD','store09 paper',.02,'bold');eb_text(side,.39,2.96,.61,.105,'READING','store09 paper',.02,'bold')
  p02_ring(f,a+w*.85,1.67,w*.095,.52,-.18,'eb iron',.015,28)
  for yy in [1.30,1.65,2.0]:f.line((a+w*.77,yy,-.16),(a+w*.93,yy,-.16),.01,'eb iron')
  ee_chair(f,a+w*.16,.87,'eb silver metal');f.b(a+w*.35,.95,-.5,w*.45,.045,.40,'eb white wood')
 elif k=='katsu':
  eb_panel(f,a,b,3.31,.53,'eb white wood');ee_shutter(f,a+.05,b-.05,top=2.98,mat='eb charcoal stone')
  # Angular joined EK strokes are an authored approximation of the visible mark.
  x=c-.55;y=3.31
  for p,q in [((x,y+.17),(x,y-.17)),((x,y+.17),(x+.23,y+.17)),((x,y),(x+.19,y)),((x,y-.17),(x+.23,y-.17)),((x+.32,y+.17),(x+.32,y-.17)),((x+.32,y),(x+.55,y+.17)),((x+.32,y),(x+.55,y-.17))]:f.line((*p,.265),(*q,.265),.025,'ee deep blue')
  eb_text(f,c+.42,3.31,w*.37,.135,'EVIL KATSU','ee deep blue',.27,'bold')
 elif k=='lafleur':
  eb_panel(f,a,b,3.31,.55,'eb green wood');eb_text(f,a+w*.59,3.32,w*.72,.25,'La Fleur Cafe','ee pink letters',.28,'script')
  for j in range(7):
   ang=-math.pi*.5+j*math.pi/6;f.line((a+w*.13,3.21,.275),(a+w*.13+.23*math.sin(ang),3.21+.26*math.cos(ang),.275),.031,'ee bright leaf')
  nb_grille(f,a+.06,b-.06,.19,2.82,.15);eb_plant(f,a+w*.72,.50,-.45,.70)
 elif k=='throwback':
  eb_panel(f,a,b,3.27,.45)
  text='MR. THROWBACK';step=w*.86/len(text)
  for j,ch in enumerate(text):eb_text(f,a+w*.07+(j+.5)*step,3.29,step*.97,.23,ch,['eb red wood','eb yellow enamel','eb blue enamel'][min(2,j//5)],.27,'bold')
  eb_clothes(f,a+.15,b-.12,2.2)
  for j,number in enumerate(['23','33','1']):eb_text(f,a+w*(.30+j*.23),1.63,.29,.27,number,'store09 paper',-.39,'bold')
  nb_grille(f,a+.06,b-.06,.18,2.81,.15)
 elif k=='barbers':
  ee_curved(f,a,b,'ee ochre canvas','NEIGHBORHOOD','serif',y=3.66,drop=.63,dep=.85)
  eb_text(f,c,2.93,w*.72,.13,'BARBERS','eb dark wood',.98,'bold')
  p02_ring(f,c,3.47,.20,.13,.71,'eb gold metal',.025,24)
  for row in range(3):
   for col in range(3):ee_portrait(f,a+w*(.14+col*.17),.87+row*.43,w*.15,.39)
  for yy in [1.10,1.35,1.60,1.85,2.10]:
   f.b(a-.06,yy,.37,.16,.24,.17,'eb red wood' if round(yy*4)%2 else 'eb white wood')
  for yy in [.96,2.25]:p02_disc(f,a-.06,yy,.11,.08,.48,'eb silver metal',16)
  ee_chair(f,b-.20,.95,'ee green chair');ee_chair(f,b-w*.27,-.55,'eb dark wood')
  ee_frame(f,b-w*.26,1.85,.60,1.32,-.96,'eb gold metal');p02_notice(f,b-.12,1.33,.20,.31,.98)
 elif k in ['439vacant','441vacant']:
  eb_panel(f,a,b,3.26,.38,'eb gray metal' if k=='439vacant' else 'eb dark wood')
  ss=a+w*.63;f.b(ss,1.75,-.13,w*.55,.78,.025,'eb white wood')
  for yy,t in [(1.94,'RETAIL'),(1.70,'FOR LEASE')]:eb_text(f,ss,yy,w*.49,.14,t,'eb dark wood',-.105,'bold')
  if k=='439vacant':nb_grille(f,a+.05,b-.05,.18,2.85,.16);p03_tags(f,a+.15,b-.15,.30,.70,.20,439)
  else:
   for x in [a+w*.30,a+w*.74]:ee_chair(f,x,-.52,'eb red wood')
 elif k=='poke':
  eb_panel(f,a,b,3.30,.51,'eb white wood');eb_text(f,c,3.31,w*.89,.26,'POKE & ROLL','ee deep blue',.28,'bold')
  for j in range(5):
   x=a+w*(.12+j*.19);f.b(x,.77,.10,w*.17,.35,.015,'eb white wood');p02_disc(f,x,.79,.13,.10,.121,'eb oak wood',20)
   for q,mat in enumerate(['eb green wood','eb red wood','eb yellow enamel']):p02_disc(f,x+(q-1)*.05,.81,.04,.04,.13,mat,10)
  eb_blade(f,a+.03,3.46,'POKE','ee deep blue',True)
  for x in [a+w*.2,a+w*.8]:eb_lamp(f,x,3.72,.48)
  f.b(c,1.0,-.5,w*.80,.06,.50,'eb white wood')
 elif k=='socialtees':
  eb_text(f,a+w*.35,2.27,w*.60,.14,'SOCIAL TEES','eb gold metal',.08,'serif');eb_text(f,a+w*.35,2.05,w*.58,.15,'ANIMAL RESCUE','eb gold metal',.08,'serif')
  # Outline head rather than a filled generic retail icon.
  p02_ring(f,a+w*.35,1.56,.25,.29,.08,'eb gold metal',.016,28)
  for side in [-1,1]:p02_ring(f,a+w*.35+side*.24,1.55,.07,.18,.08,'eb gold metal',.014,20)
  for side in [-1,1]:p02_disc(f,a+w*.35+side*.08,1.62,.016,.021,.09,'eb gold metal',10)
  p02_ring(f,a+w*.35,1.46,.12,.08,.09,'eb gold metal',.012,20)
  p02_disc(f,a+w*.35,1.50,.035,.025,.10,'eb gold metal',10)
  for j in range(3):p02_notice(f,b-.27,1.15+j*.30,.23,.21,-.17)
  for yy in [.48,.60,.72]:f.b(a+w*.32,yy,.73,w*.60,.08,.35,'eb oak wood')
  for xx in [a+w*.08,a+w*.55]:f.line((xx,.17,.72),(xx,.75,.72),.028,'eb iron')
 elif k=='yam':
  eb_text(f,a+w*.15,2.59,.36,.12,'EXIT','eb red wood',-.16,'bold')
  p02_disc(f,a+w*.65,1.78,.31,.36,.08,'ee pink letters',28);p02_disc(f,a+w*.66,1.78,.20,.25,.09,'eb yellow enamel',24)
  eb_text(f,a+w*.65,1.25,w*.57,.23,'hello yam','eb yellow enamel',.09,'script')
  f.b(c,1.05,-.60,w*.85,.06,.42,'eb white wood')
  for x in [a+w*.42,a+w*.78]:ee_chair(f,x,-.34,'eb white wood')
 elif k=='creperie':
  observed_awning(f,a,b,{'detail09':True,'y':3.65,'drop':.55,'depth':1.35,'valance':.23,'material':'eb blue canvas','stripe':'ee ochre canvas','stripeSpacing':.31,'stripeWidth':.14,'scalloped':True})
  eb_text(f,c,3.0,w*.9,.18,'VILLAGE CREPERIE','store09 paper',1.49,'serif');eb_blade(f,a+.04,3.39,'CRÊPERIE','eb white wood',True,color='eb oak wood')
  for x in [a+w*.12,a+w*.51,a+w*.89]:
   ee_round_table(f,x,1.83);ee_chair(f,x-.38,1.91,'eb oak wood',True);ee_chair(f,x+.38,1.91,'eb oak wood',True)
  eb_board(f,b-.08,.17,'CREPES|COFFEE|MENU',d=1.04)
  for j in range(9):rod(f.p(a+(j+.5)*w/9,2.89,1.18),f.p(a+(j+.5)*w/9,2.96,1.18),.036,'opal lamp',8)
 elif k=='smoke':
  for j in range(7):f.b(c,3.02+j*.10,.19,w,.083,.10,'eb oak wood')
  for yy,t in [(3.45,'VILLAGER'),(3.16,'SMOKE SHOP')]:
   eb_text(f,c+.01,yy-.015,w*.82,.22,t,'eb red wood',.26,'bold');eb_text(f,c,yy,w*.82,.22,t,'store09 paper',.28,'bold')
  ee_shutter(f,a+.04,b-.04,top=2.85)
  for j,mat in enumerate(['eb green wood','eb purple enamel','eb red wood']):
   x=a+w*(.22+j*.29);p02_ring(f,x,1.25,w*.19,.42,.16,mat,.06,24);p02_ring(f,x+.05,1.17,w*.14,.31,.17,'eb white wood',.012,24)
  eb_text(f,b-.20,3.67,.28,.11,'445','store09 paper',.28,'serif')
 elif k=='tsumiki':
  eb_canopy(f,a,b,'eb black canvas','Tsumiki hair','script',y=3.55,drop=.44,dep=.77,letter='eb gold metal')
  nb_grille(f,a+.05,b-.05,.18,2.80,.15)
  for j in range(3):p02_ring(f,a+w*(.22+j*.28),1.31,w*.16,.49,.17,'ee pink letters',.055,22)
 elif k=='whitmans':
  eb_canopy(f,a,b,'eb black canvas','WHITMANS','sans',y=3.55,drop=.44,dep=.78)
  for j in range(8):
   x=a+(j+.5)*w/8;f.line((x,2.95,.62),(x,2.76,.62),.007,'eb iron');rod(f.p(x,2.73,.62),f.p(x,2.79,.62),.035,'opal lamp',8)
  for x in [a+w*.2,a+w*.78]:ee_chair(f,x,.90,'eb white wood')
  f.b(a+w*.68,.99,-.45,w*.60,.055,.42,'eb oak wood');eb_bottles(f,a+w*.47,b-.12,1.05,rows=1)
  eb_text(f,a+w*.65,.46,w*.49,.12,'WHITMANS','eb dark wood',.13,'bold')
 elif k=='flowerpower':
  for j in range(round(w/.075)):
   x=a+j*.075
   if x<a+w*.06 or x>a+w*.94:f.b(x,1.64,.10,.023,2.94,.027,'eb oak wood')
   else:f.b(x,.36,.10,.023,.37,.027,'eb oak wood')
  eb_panel(f,a,b,3.37,.75,'eb yellow wood')
  eb_text(f,c,3.54,w*.88,.20,'FLOWER POWER','eb blue metal',.28,'script')
  for j in range(13):
   ang=j*math.tau/13;p02_disc(f,c+math.cos(ang)*.21,3.27+math.sin(ang)*.15,.07,.10,.28,'eb yellow enamel',12)
  p02_disc(f,c,3.27,.11,.10,.29,'eb brown stone',20)
  eb_text(f,c,3.13,w*.91,.105,'HERBS AND ROOTS APOTHECARY','eb brown stone',.30,'serif')
  eb_bottles(f,a+.12,a+w*.65,.69,rows=3,colors=['eb oak wood','eb green wood','eb yellow enamel'])
  for x in [a+w*.18,a+w*.48]:eb_plant(f,x,.62,-.35,.6)
  ee_hood(f,a,b,2.93,'eb dark wood',.37)
 elif k=='414basement':
  ee_hood(f,a,b,2.18,'eb dark wood',.40);ee_shutter(f,a+.05,a+w*.75,.19,1.91,'eb charcoal stone')
  for j in range(4):eb_lamp(f,a+(j+.5)*w/4,2.33,.53)
  eb_text(f,b-.17,2.17,.28,.12,'414','eb gold metal',.43,'serif')
 elif k=='412basement':
  ee_hood(f,a,b,2.18,'eb gold metal',.40)
  for x in [a+w*.22,a+w*.75]:eb_lamp(f,x,2.34,.53)
  nb_grille(f,a+.05,b-.05,.18,1.91,.14)
 elif k=='fa':
  ee_hood(f,a,a+w*.69,2.20,'eb dark wood',.45);ee_hood(f,a+w*.70,b,2.25,'eb dark wood',.35)
  # Two actual round display lights within the broad pane, not an undivided box.
  for at in [.175,.515]:eb_arc(f,a+w*at,1.61,w*.16,.31,.09,.035,'eb dark wood')
  for x in [a+w*.12,a+w*.59]:eb_lamp(f,x,2.39,.52,'eb silver metal')
  for j in range(4):ee_scroll(f,a+w*(.73+j*.07),2.43,.035,'eb brown stone',.21)
  for j in range(3):f.b(a+w*.34, .35+j*.22,-.55-j*.10,w*.58,.22,.31,'eb oak wood')
  eb_clothes(f,a+.12,a+w*.58,1.84,-.76);eb_plant(f,a+w*.28,.56,-.22,.55,True)
 elif k=='422basement':
  ee_hood(f,a,a+w*.31,2.19,'eb white wood',.39);ee_hood(f,a+w*.32,b,2.23,'eb white wood',.40)
  for j in range(3):eb_lamp(f,a+w*(.15+j*.34),2.40,.54,'eb silver metal')
  for yy,t in [(1.57,'GOOD'),(1.29,'BEER')]:eb_text(f,a+w*.62,yy,w*.31,.23,t,'eb gold metal',.08,'condensed')
  eb_bottles(f,a+w*.36,b-.12,.40,rows=3)
 elif k=='drgreen':
  ee_hood(f,a,b,2.22,'eb dark wood',.48);p03_tags(f,a+.12,b-.12,2.16,2.28,.51,424)
  p02_disc(f,a+w*.31,1.41,.47,.47,.10,'ee bright leaf',32);ee_animal(f,a+w*.31,1.57,.65,.62,'eb green wood',.12,True)
  eb_text(f,a+w*.31,1.30,w*.55,.20,'Dr.Green','store09 paper',.15,'script');eb_text(f,a+w*.31,1.09,w*.44,.09,'Greenery','store09 paper',.15,'script')
  eb_bottles(f,a+w*.57,b-.10,.43,rows=3);eb_lamp(f,c,2.35,.56,'eb silver metal')
 elif k=='thursday':
  eb_panel(f,a,b,2.23,.32,'eb oak wood')
  for j in range(max(3,round(w/.26))):ee_scroll(f,a+(j+.5)*w/max(3,round(w/.26)),2.30,.063,'eb brown stone',.22)
  # Lit sign sits in front of the projecting fascia molding, never inside it.
  f.b(c,2.03,.36,w*.39,.37,.09,'opal lamp');eb_text(f,c,2.04,w*.34,.23,'Thursday','eb dark wood',.42,'script')
  x=c-w*.24;y=2.04
  for p,q in [((x-.06,y),(x+.06,y)),((x,y+.13),(x,y-.13)),((x,y+.01),(x-.08,y-.11)),((x,y+.01),(x+.08,y-.11))]:f.line((*p,.43),(*q,.43),.013,'eb dark wood')
  eb_lamp(f,c,2.60,.63,'eb silver metal')
  for dx in [-.11,.11]:f.line((c+dx,2.49,.60),(c+dx,2.32,.60),.009,'eb silver metal')
  for xx in [a+w*.2,a+w*.80]:f.b(xx,.86,-.65,w*.25,.05,.48,'eb oak wood')
  for j in range(5):rod(f.p(a+(j+.5)*w/5,1.72,-.65),f.p(a+(j+.5)*w/5,1.82,-.65),.035,'opal lamp',8)
 elif k=='428east':
  eb_panel(f,a,b,3.32,.39,'eb oak wood')
  for j in range(4):ee_scroll(f,a+(j+.5)*w/4,3.32,.07,'eb brown stone',.26)
  diamond_grille(f,a+.05,a+w*.70,.40,2.83,.16,'eb iron')
  for j in range(5):rod(f.p(a+w*(.12+j*.12),.55,-.35),f.p(a+w*(.12+j*.12),.79,-.35),.075,'eb pale fabric',12,r2=.05)
  p03_tags(f,a+.07,a+w*.69,.25,.63,.20,428)
 elif k=='throwback2':
  eb_panel(f,a,b,3.29,.43)
  for j in range(5):p02_ring(f,a+(j+.5)*w/5,3.29,.075,.075,.26,'eb brown stone',.018,20)
  ee_hood(f,a,a+w*.28,2.95,'eb silver metal',.42);ee_hood(f,a+w*.29,b,2.95,'eb silver metal',.42)
  ss=a+w*.64;f.b(ss,2.02,-.12,w*.61,.58,.025,'eb white wood')
  eb_text(f,ss,2.12,w*.55,.25,'THROWBACK','eb red wood',-.09,'condensed');eb_text(f,ss,1.89,w*.54,.10,'428 EAST 9TH ST','eb dark wood',-.09,'sans')
  nb_grille(f,a+.04,b-.04,.18,2.81,.16)
 elif k=='salads':
  eb_panel(f,a,b,2.24,.42,'eb white wood')
  for yy,t in [(2.34,'SALADS'),(2.15,'DAYS')]:eb_text(f,c,yy,w*.58,.17,t,'ee bright leaf',.27,'italic')
  f.b(c,.75,-.52,w*.76,.045,.45,'eb white wood');p02_notice(f,b-.15,1.35,.23,.30,.09)
 elif k=='whiskers':
  f.b(c,2.23,.24,w,.57,.045,'ee red orange');eb_text(f,c,2.38,w*.87,.21,'WHISKERS','eb blue metal',.28,'condensed')
  ee_animal(f,c-.22,2.12,.5,.40,'eb white wood',.28,True);ee_animal(f,c+.18,2.11,.5,.39,'eb green wood',.29)
  eb_canopy(f,a,a+w*.37,'eb red canvas',y=2.25,drop=.25,dep=.42)
  nb_grille(f,a+.05,b-.05,.18,1.96,.14);eb_bottles(f,a+.15,b-.12,.40,rows=3)
 elif k=='chiro':
  eb_panel(f,a,b,3.27,.38,'eb gray stone')
  for j in range(6):
   x=a+w*(j+.5)/6;ee_frame(f,x,.50,w/6-.10,.43,.15,'eb oak wood')
   f.b(x,1.70,-.11,w/6-.13,1.52,.014,'eb pale fabric')
  eb_text(f,b-.28,1.42,.40,.10,'Chiro-Fit','eb gold metal',-.14,'serif')
 elif k=='loveonly':
  ee_curved(f,a,b,'eb black canvas','LOVE ONLY','serif',y=3.70,drop=.70,dep=.83)
  nb_grille(f,a+.05,b-.05,.18,2.85,.15)
 elif k=='434west':
  eb_panel(f,a,b,3.31,.47,'eb gold metal');ee_hood(f,a,b,2.98,'eb gold metal',.40)
  for x in [a+.08,b-.08]:ee_scroll(f,x,3.37,.10,'eb gold metal',.28)
  nb_grille(f,a+.05,b-.05,.18,2.85,.15)
 elif k=='nicebrow':
  eb_panel(f,a,b,3.31,.53,'eb white wood');eb_text(f,c,3.31,w*.92,.32,'Nicebrow','eb gold metal',.29,'serif')
  for j in range(7):f.line((c-.20+j*.065,3.57,.29),(c-.24+j*.08,3.68+.04*math.sin(j*math.pi/6),.29),.015,'eb gold metal')
  nb_grille(f,a+.05,b-.05,.18,2.84,.15);p03_tags(f,a+.08,b-.08,.25,.52,.20,436)
 elif k=='starshop':
  ee_curved(f,a,b,'eb black canvas',y=3.55,drop=.48,dep=.54)
  ee_star(f,c,3.35,.27,.64,'eb white wood');ee_star(f,c,3.35,.21,.65,'eb dark wood')
  nb_grille(f,a+.05,b-.05,.18,2.83,.14);ee_star(f,c,1.62,.78,.16,'eb cyan enamel');ee_star(f,c,1.62,.58,.17,'eb dark wood');ee_star(f,c,1.62,.39,.18,'eb white wood')
  for j in range(4):p02_ring(f,a+(j+.5)*w/4,.44,.25,.16,.19,'eb red wood',.04,20)
 elif k=='murphys':
  eb_canopy(f,a,b,'eb blue canvas',"Murphy’s",'script',y=3.55,drop=.49,dep=.88)
  for j in range(round(w/.045)):f.b(a+j*.045,1.78,.12,.028,1.85,.035,'eb oak wood')
  for x in [a+w*.12,a+w*.82]:eb_plant(f,x,2.41,.43,.32)
  p03_tags(f,a+.08,b-.08,.3,.7,.18,438)
 elif k=='tacos':
  ee_curb_shelter(f,a,b,'tacos')
  eb_panel(f,a,b,3.35,.58,'eb white wood')
  ee_frame(f,c,3.35,w-.06,.57,.27,'eb red wood')
  eb_text(f,c,3.45,w*.92,.20,'TACOS CUAUTLA','eb green wood',.29,'bold');eb_text(f,c,3.24,w*.82,.16,'MORELOS','eb red wood',.29,'bold')
  f.b(c,2.95,.24,w,.15,.12,'eb green wood');eb_text(f,c,3.08,w*.88,.08,'BAR & RESTAURANT','eb red wood',.30,'serif')
  f.b(c,1.0,-.54,w*.80,.05,.43,'eb white wood')
 elif k=='confectionery':
  ee_curved(f,a,b,'eb red canvas','Confectionery','script',y=3.65,drop=.65,dep=.91,letter='eb blue enamel',scallop=True)
  nb_grille(f,a+.05,b-.05,.18,2.84,.15)
 elif k=='monkey':
  eb_canopy(f,a,b,'eb green canvas','MONKEY THRIFT SHOP','serif',y=3.62,drop=.52,dep=.92,letter='ee ochre canvas')
  eb_text(f,c,3.00,w*.84,.13,'UpCycling','ee ochre canvas',1.06,'script')
  eb_text(f,c,1.90,w*.74,.27,'Monkey','eb gold metal',.08,'script');eb_clothes(f,a+.15,b-.12,2.31)
  f.b(c,.45,.10,w-.12,.48,.09,'eb purple enamel');ee_animal(f,a+w*.19,.49,.47,.48,'eb gold metal',.16)
  for side in [-1,1]:p02_disc(f,a+w*.19+side*.15,.51,.08,.085,.18,'eb gold metal',16)
  p02_disc(f,a+w*.19,.46,.10,.07,.19,'eb purple enamel',16)
  p02_curve(f,[(a+w*.27,.35),(a+w*.37,.44),(a+w*.38,.65),(a+w*.32,.68),(a+w*.30,.59)],.18,'eb gold metal',.025)
  nb_grille(f,a+.05,b-.05,.19,2.85,.15)
 else:ee_corner_shop(f,a,b,r)

# Corner shops use bounded openings. Their solid murals / service walls are not
# forced through the full-height glazed-shop primitive.
def ee_corner_shop(f,a,b,r):
 k=r['design']['detailE09East']['kind'];w=b-a;c=(a+b)/2
 def glazing(lo,hi,panels,top=2.90,base=.38,frame='eb oak wood'):
  rr=deepcopy(r);rr['design'].pop('detailE09East',None);rr['design']['panels']=panels
  rr['design'].update(top=top,head=top-.12,base=base)
  rr['design']['detail09'].update(frame=frame,surround=frame)
  _ee_previous_shop(f,lo,hi,rr)
 if k=='ralph':
  # Small inset serving aperture, stainless ledge and illustrated menu surround.
  fidelity_opening(f,c,1.15,w*.39,1.12,mat='eb iron',d=-.18)
  ee_frame(f,c,1.71,w*.39,1.12,.04,'eb silver metal')
  f.b(c,1.15,.28,w*.44,.085,.67,'eb silver metal')
  for x in [c-w*.195,c,c+w*.195]:f.b(x,1.71,.04,.035,1.12,.055,'eb silver metal')
  f.b(c,2.06,-.38,w*.37,.08,.14,'opal lamp')
  for lo,hi in [(a+.10,c-w*.22),(c+w*.22,b-.10)]:
   f.b((lo+hi)/2,1.59,.06,hi-lo,2.45,.04,'eb white wood')
   for row in range(6):
    for col in range(3):
     x=lo+(hi-lo)*(col+.5)/3;yy=.65+row*.33
     p02_disc(f,x,yy,.105,.08,.093,['eb yellow enamel','eb red wood','eb green wood'][(row+col)%3],16)
     f.b(x,yy+.055,.103,.13,.10,.012,'eb pale fabric')
     for j in range(2):f.b(x,yy-.11-j*.027,.095,.17,.008,.008,'eb iron')
  f.b(c,.71,.06,w*.42,.65,.04,'eb white wood')
  for j in range(6):eb_text(f,c,.94-j*.085,w*.38,.045,['ITALIAN ICES','LEMON  CHERRY  BLUE RASPBERRY','MANGO  WATERMELON  ORANGE','CREAM ICES  ICE CREAM','MILKSHAKES  SUNDAES','FAMOUS SINCE 1928'][j],'ee deep blue',.09,'condensed')
  ee_curved(f,a,b,'ee deep blue',y=3.55,drop=.62,dep=.92)
  f.b(c,3.14,1.01,w*.32,.59,.025,'eb white wood')
  eb_text(f,c,3.28,w*.28,.22,"Ralph’s",'eb red wood',1.03,'script')
  eb_text(f,c,3.04,w*.25,.12,'ITALIAN ICES','ee deep blue',1.03,'condensed')
  eb_text(f,c,2.90,w*.24,.10,'ICE CREAM','ee deep blue',1.03,'condensed')
  for x,txt in [(a+w*.16,'ITALIAN ICES'),(b-w*.16,'ICE CREAM')]:
   eb_text(f,x,3.19,w*.25,.15,txt,'store09 paper',1.03,'condensed')
   eb_text(f,x,2.98,w*.24,.08,'SOFT SERVE • SHAKES','eb yellow enamel',1.03,'bold')
  p02_disc(f,c+w*.12,3.28,.09,.12,1.055,'eb yellow enamel',20)
 elif k=='ralphside':
  ee_curved(f,a,b,'ee deep blue','ITALIAN ICES','condensed',y=3.55,drop=.62,dep=.92)
  for x in [a+.18,b-.20]:f.line((x,.22,.08),(x,2.85,.08),.035,'eb silver metal')
  for j in range(3):
   x=a+w*(j+.5)/3;f.b(x,1.8,.08,.36,.46,.02,'eb white wood')
   eb_text(f,x,1.85,.30,.07,'ITALIAN ICES','ee deep blue',.10,'condensed')
 elif k=='docave':
  ee_curved(f,a,b,'ee mauve canvas',"DOC HOLLIDAY’S",'slab',y=3.62,drop=.62,dep=1.04)
  doorx=a+w*.435
  for row in range(6):
   for col in range(2):
    x=doorx+(col-.5)*w*.075;yy=.48+row*.28;f.b(x,yy,-.07,w*.065,.23,.018,['eb white wood','eb red wood','eb yellow enamel'][row%3]);eb_text(f,x,yy,w*.055,.045,['LIVE','NYC','BAR'][row%3],'eb iron',-.055,'condensed')
  for x in [a+w*.17,a+w*.77]:
   p02_ring(f,x,2.15,.43,.26,-.06,'p02 red tube',.012,32);eb_text(f,x,2.15,.70,.13,'BEER','p02 red tube',-.045,'script')
  f.b(a+w*.77,.91,-.49,w*.35,.09,.45,'eb oak wood')
  for x in [a+w*.68,a+w*.86]:ee_chair(f,x,-.45)
 elif k=='docside':
  glazing(a,a+w*.22,[['glass',1]],frame='eb oak wood')
  glazing(a+w*.72,b,[['glass',1]],frame='eb oak wood')
  ee_curved(f,a,a+w*.22,'ee mauve canvas',"DOC HOLLIDAY’S",'slab',y=3.62,drop=.62,dep=1.04)
  lo=a+w*.245;hi=a+w*.695;mc=(lo+hi)/2;mw=hi-lo
  f.b(mc,1.55,.044,mw,2.64,.025,'ee red orange')
  for j in range(4):
   x=lo+mw*(j+.5)/4;yy=2.02
   # Four separately posed painted cowboy figures; simplified authored artwork.
   p02_disc(f,x,yy,.18,.23,.065,'eb brown stone',20)
   p02_disc(f,x,yy+.18,.32,.07,.070,'eb iron',20);f.b(x,yy+.27,.073,.33,.19,.014,'eb iron')
   ee_front([f.p(x-.19,yy-.22,.071),f.p(x+.19,yy-.22,.071),f.p(x+.31,yy-1.18,.071),f.p(x-.31,yy-1.18,.071)],['eb charcoal stone','eb gray metal','eb blue metal','eb iron'][j])
   for side in [-1,1]:
    ee_front([f.p(x+side*.19,yy-.23,.084),f.p(x+side*.05,yy-.22,.084),f.p(x+side*.05,yy-.70,.084)],'eb cream stone')
    f.line((x+side*.25,yy-.32,.08),(x+side*.34,yy-1.03,.08),.045,'eb charcoal stone')
   p02_disc(f,x,yy-.09,.11,.07,.091,'eb iron',12)
   for q in range(3):p02_disc(f,x,yy-.62-q*.15,.016,.018,.092,'eb gold metal',8)
   for dx in [-.10,.10]:f.line((x+dx,yy-.24,.078),(x,yy-.65,.078),.024,'eb cream stone')
   for dx in [-.07,.07]:p02_disc(f,x+dx,yy+.02,.025,.018,.081,'eb iron',8)
   f.line((x-.08,yy-.08,.081),(x+.09,yy-.08,.081),.018,'eb iron')
  eb_text(f,mc,1.06,mw*.96,.48,"DOC HOLLIDAY’S",'ee deep blue',.10,'slab')
  for x in [a+w*.1,a+w*.83]:
   p02_ring(f,x,2.10,.43,.26,-.06,'p02 red tube',.012,32);eb_text(f,x,2.1,.67,.12,'BEER','p02 red tube',-.04,'script')
 elif k=='celeste':
  # The mapped 3.293 m gap has a LOW infill, never a full-height extension.
  f.b(c,1.625,-2.26,w,3.25,4.56,'eb cream stone')
  ee_shutter(f,a+.06,b-.06,.18,2.85,d=.09)
  eb_canopy(f,a,b,'eb black canvas','CELESTE','serif',y=3.20,drop=.42,dep=.66)
  f.b(c,3.25,-1.5,w,.10,3.,'eb gray stone')
  for yy in [3.37,4.18]:f.line((a,yy,.04),(b,yy,.04),.025,'eb iron')
  for j in range(round(w/.14)+1):f.line((a+j*w/round(w/.14),3.29,.04),(a+j*w/round(w/.14),4.18,.04),.012,'eb iron')
  for x in [a,b]:f.line((x,3.27,.04),(x,4.75,.04),.020,'eb iron')
  for j in range(16):
   x0=a+w*j/16;x1=a+w*(j+1)/16;yy=4.7-.30*math.sin(math.pi*j/16);yy2=4.7-.30*math.sin(math.pi*(j+1)/16)
   f.line((x0,yy,.04),(x1,yy2,.04),.008,'eb iron')
   if j%2==0:p02_disc(f,x0,yy-.065,.027,.045,.06,'opal lamp',10)
 elif k=='marketside':
  OPENINGS[frontage_key(f)].append((a,.17,b,3.15))
  ff=FidelityProjectedFacade(f,1.18)
  rr=deepcopy(r);rr['design'].pop('detailE09East',None);rr['design'].update(top=3.14,head=3.05,base=.57,recess=.06)
  rr['design']['detail09'].update(frame='p02 silver frame',surround='p02 market red',frameWidth=.025,molding=False,displayDepth=1.5)
  _ee_previous_shop(ff,a,b,rr)
  observed_awning(f,a,b,{'detail09':True,'y':3.86,'drop':.67,'depth':1.30,'valance':.16,'material':'store09 maroon canvas','text':'','sidePanels':True})
  # One oval identity on the sloping cloth. Project both oval and lettering
  # to the same plane so the lower half cannot sink behind the canopy.
  def cloth_depth(yy):return .10+1.30*(3.86-yy)/.67+.026
  oval=[f.p(c+w*.16*math.cos(j*math.tau/48),3.47+.19*math.sin(j*math.tau/48),cloth_depth(3.47+.19*math.sin(j*math.tau/48))) for j in range(48)]
  ee_front(oval,'eb pale fabric')
  obj=eb_text(f,c,3.47,w*.28,.18,'LIME TREE MARKET','eb green wood',cloth_depth(3.47)+.012,'serif')
  if obj:
   bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj;bpy.ops.object.convert(target='MESH');bpy.context.view_layer.update()
   matrix=obj.matrix_world.copy();inverse=matrix.inverted()
   for v in obj.data.vertices:
    world=matrix@v.co;old=(world.x-f.x)*f.nx+(-world.y-f.z)*f.nz;target=cloth_depth(world.z)+.012
    world.x+=f.nx*(target-old);world.y-=f.nz*(target-old);v.co=inverse@world
  for x in [a,b]:
   for yy in [.18,.57,3.06]:f.line((x,yy,0),(x,yy,1.2),.026,'p02 silver frame')
   pp=[f.p(x,.58,0),f.p(x,.58,1.18),f.p(x,3.06,1.18),f.p(x,3.06,0)];face(pp,'store09 clear glass');face(pp[::-1],'store09 clear glass')
  for j in range(5):
   x=a+w*(j+.5)/5;f.b(x,.90,-.35,w*.17,.10,.65,'eb oak wood')
   for q in range(6):
    p02_disc(f,x+(q-2.5)*w*.022,1.06,.08,.10,-.01,['eb yellow enamel','eb red wood','eb green wood'][j%3],10)
   if j in [1,3]:p02_notice(ff,x,2.03,.50,.67,.04,'store09 paper')
 else:raise ValueError('Unimplemented E09 east shop: '+k)


def ee_school(f,r,h):
 s=r['e09East'];num=s['number']
 for yy,hh,dd in [(5.47,.18,.10),(5.83,.16,.16),(6.17,.18,.12),(11.65,.09,.09),(16.65,.09,.09)]:f.strip(yy,hh,dd,'eb cream stone')
 if num in ['PS122-2','PS122-6']:
  c=f.L/2;w=min(3.0,f.L*.85);y=4.70;peak=6.45
  for x in [c-w/2,c+w/2]:
   f.b(x,2.92,.32,.35,3.85,.64,'eb cream stone')
   for yy in [1.10,4.60]:f.b(x,yy,.35,.49,.18,.73,'eb cream stone')
  # Steep stone gable and real open pointed arch under it.
  ee_front([f.p(c-w*.58,y,.69),f.p(c,peak,.69),f.p(c+w*.58,y,.69)],'eb cream stone')
  for side in [-1,1]:
   f.line((c+side*w*.61,y,.77),(c,peak+.08,.77),.085,'eb gray stone')
   pts=[(c+side*(w*.41)*(1-j/16),3.84+.87*(j/16)**.7) for j in range(17)]
   p02_curve(f,pts,.74,'eb cream stone',.13)
  f.b(c,4.92,.71,.75,.24,.03,'eb cream stone')
  eb_text(f,c,4.92,.65,.12,'P.S. 122','eb gray stone',.74,'serif')
 # Dated green sidewalk shed and cross-braced galvanized scaffold; architecture
 # remains modeled above and behind it, with no opaque full-height fake net.
 f.b(f.L/2,3.02,1.43,f.L,.18,2.65,'eb gray metal')
 eb_panel(f,0,f.L,3.31,.57,'eb green wood',2.73)
 count=max(1,round(f.L/3.2))
 for j in range(count+1):
  x=f.L*j/count
  for dd in [.23,2.68]:f.line((x,.18,dd),(x,3.12,dd),.035,'eb silver metal')
  f.line((x,2.95,.23),(x,2.95,2.68),.023,'eb silver metal')
  if j<count:
   nx=f.L*(j+1)/count
   f.line((x,.36,2.67),(nx,2.90,2.67),.018,'eb silver metal');f.line((x,2.90,2.68),(nx,.36,2.68),.018,'eb silver metal')
 if num in ['PS122-3','PS122-6']:
  f.b(f.L*.5,3.31,2.83,min(3.9,f.L*.88),.45,.035,'eb white wood')
  eb_text(f,f.L*.5,3.36,min(3.5,f.L*.80),.14,'PERFORMANCE SPACE NEW YORK','eb iron',2.86,'condensed')
  eb_text(f,f.L*.5,3.19,min(3.3,f.L*.77),.065,'150 FIRST AVENUE • 122 COMMUNITY CENTER','eb iron',2.86,'condensed')
 if num=='PS122-0':
  # Narrow planted strip between school and 411, independently observed.
  aa=f.L;bb=f.L+1.87
  for yy in [.20,1.50]:f.line((aa,yy,.10),(bb,yy,.10),.023,'eb iron')
  for j in range(13):f.line((aa+j*.15,.16,.10),(aa+j*.15,1.51,.10),.012,'eb iron')
  for x in [aa+.35,aa+1.,aa+1.55]:eb_plant(f,x,.15,-.35,.65)


def ee_relief(f,r,h):
 s=r['e09East'];n=s['number'];mat=s['trim']
 if s.get('school'):ee_school(f,r,h);return
 if n in ['413','417','431','433','402','404','412','418','418.5','426']:
  fidelity_courses(f,min(s['upperBottom']-.30,4.8),ee_mat(s.get('groundPaint','gray stone')),step=.37,bottom=.18,depth=.07)
 if s.get('ornate406'):
  for yy in [3.80,6.55,9.35,12.2,15.0]:
   for offset in [0,.17]:fidelity_clipped_surface(f,0,f.L,yy+offset,yy+offset+.08,.07,.12,mat)
  for yy in [4.55,5.23,5.92,7.4,8.1,8.8]:fidelity_clipped_surface(f,0,f.L,yy,yy+.055,.03,.07,mat)
  for row in range(5):
   wins=[w for w in r['windows'] if w.get('row')==row]
   for j in [0,2,4]:
    a,b=wins[j:j+2];x=(a['at']+b['at'])*f.L/2;ww=(b['at']-a['at'])*f.L+a['width']*f.L;top=a['bottom']+a['height']
    f.b(x,top+.13,.14,ww+.32,.20,.28,mat)
    f.b(x,top+.35,.10,ww*.87,.30,.15,mat)
    for q in range(5):
     xx=x+(q-2)*ww*.15;p02_ring(f,xx,top+.36,.09,.10,.20,'eb charcoal stone',.014,12)
    if row==0:
     ee_front([f.p(x-ww*.45,top+.49,.23),f.p(x,top+.86,.23),f.p(x+ww*.45,top+.49,.23)],mat)
     for side in [-1,1]:f.line((x+side*ww*.45,top+.49,.29),(x,top+.86,.29),.045,mat)
    ee_scroll(f,x,top+.42,.18,mat,.28);p02_ring(f,x,top+.46,.10,.14,.29,mat,.035,20)
    for dx in [-ww*.49,ww*.49]:
     f.b(x+dx,top+.01,.17,.19,.31,.32,mat);ee_scroll(f,x+dx,top+.17,.07,mat,.34)
    f.b(x,a['bottom']-.24,.10,ww+.30,.12,.20,mat)
  for x in [.13,f.L-.13]:
   for j in range(32):f.b(x,3.67+j*.46,.06,.31 if j%2 else .52,.40,.12,mat)
  for x in [f.L*.08,f.L*.92]:
   f.b(x,h+.21,.09,f.L*.16,.50,.18,mat);f.b(x,h+.48,.12,f.L*.17,.10,.28,mat)
 if s.get('ornate431'):
  for row in range(s['rows']):
   yy=s['upperBottom']+row*s['step']
   for offset in [-.30,2.15]:f.strip(yy+offset,.10,.13,mat)
  for x in [.12,f.L-.12]:
   for j in range(round((h-3.8)/.34)):f.b(x,3.9+j*.34,.07,.24 if j%2 else .38,.29,.14,mat)
  for w in r['windows']:
   if 'row' in w:
    x=w['at']*f.L;ww=w['width']*f.L;yy=w['bottom']-.45
    ee_frame(f,x,yy,ww*.94,.35,.13,mat)
    for q in range(4):ee_scroll(f,x+(q-1.5)*ww*.20,yy,.045,mat,.18)
  for x in [f.L*.19,f.L*.81]:
   f.b(x,3.50,.11,1.55,.23,.24,mat);f.b(x,3.35,.15,.21,.36,.22,'eb red wood')
  for w in r['windows']:
   if w.get('row')==1:eb_arc(f,w['at']*f.L,w['bottom']+w['height']+.2,w['width']*f.L*.68,.31,.28,.07,mat)
  x=f.L*.5
  for xx in [x-.8,x+.8]:
   f.b(xx,2.15,.12,.22,2.8,.25,mat);f.b(xx,3.5,.17,.36,.20,.36,'eb red wood')
  f.b(x,3.94,.22,.20,.31,.26,'eb red wood')
  for xx in [x-.77,x+.77]:
   f.b(xx,.57,1.38,.30,.82,.30,mat)
   ee_ball(f,xx,1.08,1.38,.19,mat)
 if n=='421':
  for x in [.05,f.L*.39,f.L*.61,f.L-.05]:
   f.b(x,1.95,.10,.21,3.55,.21,'ee coral');f.b(x,3.67,.14,.39,.19,.29,'ee coral');ee_scroll(f,x,3.51,.085,'ee coral',.27)
  ee_curved(f,f.L*.40,f.L*.60,'ee burgundy','421','serif',y=3.98,drop=.43,dep=.64)
 if n=='429':ee_hood(f,f.L*.39,f.L*.61,3.48,'eb gray metal',.49)
 if n=='433':
  w=next(w for w in r['windows'] if 'row' not in w);x=w['at']*f.L
  f.b(x,w['bottom']+w['height']/2,.10,w['width']*f.L,w['height'],.06,'eb plywood');nb_ac(f,x,w['bottom']+w['height']-.21,.64,.37,.16)
  for xx in [f.L*.1,f.L*.3,f.L*.8]:eb_lamp(f,xx,3.60,.47)
 if n=='427':
  for x in [.12,f.L-.15]:eb_plant(f,x,.20,.43,.70)
  f.b(f.L*.25,1.43,.14,.18,.07,.025,'eb gold metal')
 if n=='418.5':eb_text(f,f.L*.58,1.85,f.L*.46,.26,'418½','eb iron',.10,'serif')
 if n=='424':
  ee_curb_shelter(f,f.L*.03,f.L*.98,'thursday')
  for span,levels in [([.025,.20],[s['upperBottom']+s['step']-.17,s['upperBottom']+3*s['step']-.17]),([.80,.975],[s['upperBottom']+2*s['step']-.17])]:
   ee_escape(f,{'span':span,'levels':levels,'material':'eb iron','balconyOnly':True,'ornament':'plain','dropAt':span[0]})
 if n=='426':
  for w in r['windows']:
   if 'row' not in w:f.b(w['at']*f.L,w['bottom']+w['height']/2,-.04,.06,w['height'],.08,'eb sash')
  for x in [f.L*.40,f.L*.60]:eb_lamp(f,x,3.29,.29)
  for x in [f.L*.34,f.L*.67]:eb_plant(f,x,.22,.43,.45)
 if n=='434':
  x=f.L*.5
  for yy in [.63,1.65,2.51]:ee_frame(f,x,yy,.62,.47,.02,'eb yellow enamel')
 if n=='148-Ninth':
  x=f.L*.33
  ee_front([f.p(x-.85,3.32,.55),f.p(x,3.77,.55),f.p(x+.85,3.32,.55)],'eb gray stone')
  for side in [-1,1]:
   for j in range(7):f.line((x+side*.85*(1-j/7),3.32+.45*j/7,.04),(x+side*.85*(1-j/7),3.32+.45*j/7,.58),.022,'eb charcoal stone')
 if s.get('roofAddition'):
  # Set back from the front wall; does not raise the whole facade to its peak.
  f.b(f.L*.5,10.85,-2.9,f.L-.5,1.30,3.1,'eb cream stone')
  f.b(f.L*.5,11.51,-2.9,f.L-.35,.12,3.25,'eb gray stone')
  for x in [.16,f.L-.16]:f.line((x,10.2,.10),(x,10.95,.10),.015,'eb iron')
  f.line((.16,10.94,.10),(f.L-.16,10.94,.10),.018,'eb iron')
  for j in range(round(f.L/.16)):f.line((j*.16,10.2,.10),(j*.16,10.94,.10),.008,'eb iron')
 if s.get('docSide'):
  for w in s['blindWindows']:
   x=w['at']*f.L;f.b(x,w['bottom']+w['height']/2,.025,w['width'],w['height'],.035,'eb white stone')
   for yy in [w['bottom']-.06,w['bottom']+w['height']+.06]:f.b(x,yy,.10,w['width']+.21,.13,.25,mat)
  # Observed STIK composition: white body, outlined oval head and one raised arm.
  x=f.L*.13;low=4.0;hip=7.4;shoulder=10.2;head=11.1;rx=.74
  body=[f.p(x-rx*.8,hip,.045),f.p(x-rx*.85,shoulder,.045),f.p(x+rx*.70,shoulder,.045),f.p(x+rx,hip,.045)]
  ee_front(body,'eb white wood')
  p02_disc(f,x,head,rx,.62,.05,'eb white wood',40);p02_ring(f,x,head,rx,.62,.065,'eb iron',.027,40)
  for dx in [-.40,.40]:p02_disc(f,x+dx,head-.12,.06,.07,.079,'eb iron',14)
  for pts in [[(x-rx*.8,low),(x-rx*.8,hip),(x-rx*.85,shoulder)],[(x+rx,low),(x+rx,hip),(x+rx*.70,shoulder)],[(x-rx*.8,hip),(x+rx,hip)],[(x-rx*.85,shoulder),(x-1.05,11.6),(x-1.2,13.1)],[(x+rx*.7,shoulder),(x+1.08,9.2),(x+1.15,7.0)]]:p02_curve(f,pts,.075,'eb iron',.034)
 if s.get('ralph'):
  eb_text(f,f.L*.5,h-.52,f.L*.80,.30,'KNOW YOURSELF','eb iron',.065,'script')

_ee_previous_render=render_building
def render_building(b):
 if b['id'] not in E09_EAST_IDS:return _ee_previous_render(b)
 shared=b['id']==248142713
 if shared:_ee_previous_render(b)
 else:owner(str(b['id'])+' E09 east observed block')
 h=b['firstStmarksHeight'];b['renderHeight']=h
 records=[(int(i),r) for i,r in b['firstStmarksArchitecture'].items() if r.get('e09East')]
 if not shared:
  low=next((r['e09East']['streetWallHeight'] for _,r in records if r['e09East'].get('roofAddition')),h)
  wall_mass({**b,'renderHeight':low},records[0][1]['wall'],False)
 for idx,r in records:
  v=b['frontages'][idx];f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']);f.wall=r['wall']
  clean=deepcopy(r);clean['observedGround']['basementAreaways']=[]
  fidelity_elevation({**b,'businesses':[],'seventhArchitecture':clean},f,clean)
  s=r['e09East']
  if paint:=s.get('groundPaint'):shop09_face(f,{'paintSurround':{'bottom':.17,'top':min(3.65,s['upperBottom']-.18),'material':ee_mat(paint)}})
  ee_architecture(f,r,h);ee_relief(f,r,h)


def ee_curb_shelter(f,a,b,kind):
 # Curb-side dining structures: clear pavement behind, open walking ends.
 d=3.40;outer=4.70;w=b-a;count=max(1,round(w/2.0));mat='eb oak wood' if kind=='thursday' else 'eb white wood'
 for j in range(count):
  lo=a+w*j/count;hi=a+w*(j+1)/count;c=(lo+hi)/2
  for x in [lo,hi]:
   for dd in [d,outer]:f.b(x,1.40,dd,.08,2.48,.08,mat)
  for yy in [.32,.53,.74,.95]:f.b(c,yy,outer,hi-lo-.04,.18,.045,mat)
  f.b(c,1.76,outer,hi-lo-.05,1.35,.018,'store09 clear glass')
  f.b(c,2.58,outer,hi-lo,.11,.11,mat)
  for x in [lo,hi]:f.line((x,2.57,d),(x,2.57,outer),.03,mat)
  for q in range(max(1,round((hi-lo)/.12))):
   x=lo+q*.12;roof=[f.p(x,2.73,d-.08),f.p(x+.12,2.73,d-.08),f.p(x+.12,2.61,outer+.08),f.p(x,2.61,outer+.08)]
   face(roof,'eb white wood');face(roof[::-1],'eb white wood');f.line((x,2.74,d-.08),(x,2.62,outer+.08),.012,'eb gray metal')
  if kind=='thursday':p03_tags(f,lo+.07,hi-.07,.32,.93,outer+.03,424+j)
  f.b(c,.91,4.03,.73,.055,.54,'eb oak wood')
  for x in [c-.50,c+.50]:ee_chair(f,x,4.03,'eb oak wood')
 if kind=='tacos':
  for x in [a-.17,b+.17]:
   f.b(x,.20,outer+.12,.31,.045,.31,'ee red orange');rod(f.p(x,.22,outer+.12),f.p(x,.73,outer+.12),.13,'ee red orange',12,r2=.035)
