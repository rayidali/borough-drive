"""P02-only mass, facade, shop and material anatomy from its dated ledger.
No source photographic pixels; every relief dimension is an authored estimate.
"""
P02_IDS={248142657,248142658,248142659,248142660,248142713}
for name,rgb in {
 'p02 dark red brick':(.40,.235,.17),'p02 faded pink brick':(.61,.40,.35),
 'p02 red brick':(.47,.235,.18),'p02 fine red brick':(.51,.235,.17),
 'p02 aged cream stucco':(.76,.75,.68),'p02 ivory stone':(.81,.80,.70),
 'p02 dark lintel':(.30,.285,.20),'p02 salmon lintel':(.49,.27,.23),
 'p02 salmon iron':(.47,.27,.23),'p02 olive iron':(.16,.185,.13),
 'p02 olive frame':(.31,.33,.25),'p02 silver frame':(.58,.60,.55),
 'p02 cornice dark':(.33,.32,.23),'p02 cornice salmon':(.56,.295,.23),
 'p02 chair gray':(.24,.28,.26),'p02 pale mortar':(.68,.63,.52),
}.items():material(name,rgb,.87)
for name,rgb,kind in [('p02 green door',(.11,.43,.055),1),('p02 door brown',(.36,.235,.145),2),
 ('p02 laundry red',(.65,.17,.11),1),('p02 market red',(.60,.085,.045),1),
 ('p02 olive canvas',(.28,.28,.195),5),('p02 copper mesh',(.40,.255,.15),6)]:
 material(name,rgb,.83);MATS[name]['storefront09Surface']=kind
for name,rgb in [('p02 red tube',(.98,.05,.025)),('p02 yellow tube',(.9,.75,.03)),('p02 green tube',(.15,.75,.13)),('p02 blue tube',(.04,.21,.85))]:
 material(name,rgb,.35);bs=MATS[name].node_tree.nodes.get('Principled BSDF');bs.inputs['Emission Color'].default_value=(*rgb,1);bs.inputs['Emission Strength'].default_value=.8

def p02_curve(f,pts,d,mat,r=.01):
 for a,b in zip(pts,pts[1:]):f.line((*a,d),(*b,d),r,mat)
def p02_ring(f,s,y,rx,ry,d,mat,r=.01,n=28):
 p02_curve(f,[(s+rx*math.cos(j*math.tau/n),y+ry*math.sin(j*math.tau/n)) for j in range(n+1)],d,mat,r)
def p02_disc(f,s,y,rx,ry,d,mat,n=24):
 pts=[f.p(s+rx*math.cos(j*math.tau/n),y+ry*math.sin(j*math.tau/n),d) for j in range(n)];face(pts,mat);face(list(reversed(pts)),mat)
def p02_notice(f,s,y,w,h,d=.15,mat='store09 paper'):
 f.b(s,y,d,w,h,.008,mat)
 for j in range(4):f.b(s,y+h*.25-j*h*.15,d+.007,w*.72,.009,.004,'store09 gray plaster')

def p02_escape(f,e):
 """Individual open grating, staggered landings, continuous direction flights."""
 mat=e['material'];left,right=[x*f.L for x in e['span']];levels=e['levels'];dep=.93
 for row,y in enumerate(levels):
  aa,bb=[v*f.L for v in e.get('topSpan',e['span'])] if row==len(levels)-1 else (left,right)
  for dd in [.10,dep]:f.b((aa+bb)/2,y,dd,bb-aa,.067,.065,mat)
  for ss in [aa,bb]:
   f.b(ss,y,dep/2,.055,.07,dep,mat)
   f.line((ss,y-.42,.06),(ss,y-.025,dep-.03),.027,mat)
   f.b(ss,y-.12,.03,.13,.28,.025,mat)
   for yy in [y+.12,y+.93]:f.line((ss,yy,.07),(ss,yy,dep),.021,mat)
   for dd in [.18,.34,.50,.66,.82]:f.line((ss,y+.03,dd),(ss,y+.93,dd),.010,mat)
  for j in range(int((bb-aa)/.07)+1):f.b(aa+j*.07,y+.02,dep/2,.018,.026,dep-.04,mat)
  for yy in [y+.12,y+.93]:f.line((aa,yy,dep),(bb,yy,dep),.021,mat)
  for j in range(int((bb-aa)/.14)+1):f.line((aa+j*.14,y+.04,dep),(aa+j*.14,y+.93,dep),.009,mat)
  if row<len(levels)-1:
   low=right-.28 if e.get('reverse') else left+.30
   high=left+.34 if e.get('reverse') else right-.32
   if row==len(levels)-2 and e.get('topSpan'):high=f.L*sum(e['topSpan'])/2
   if e.get('flights'):low,high=[f.L*t for t in e['flights'][row]]
   hi=levels[row+1]
   for dd in [.29,.87]:
    f.line((low,y,.0+dd),(high,hi,dd),.032,mat);f.line((low,y+.83,dd),(high,hi+.83,dd),.019,mat)
   for j in range(15):
    t=j/14;ss=low+(high-low)*t;yy=y+(hi-y)*t
    f.b(ss,yy,.58,.24,.035,.60,mat)
    if j%2==0:
     for dd in [.29,.87]:f.line((ss,yy,dd),(ss,yy+.83,dd),.009,mat)
 if levels:
  x=f.L*e["dropAt"] if e.get("dropAt") is not None else left+.24
  for ss in [x,x+.36]:f.line((ss,2.55,dep),(ss,levels[0]+.66,dep),.018,mat)
  for j in range(max(1,int((levels[0]-2.2)/.26))):f.line((x,2.58+j*.26,dep),(x+.36,2.58+j*.26,dep),.012,mat)

def p02_cornice(f,bid,h):
 if bid==248142713:
  for lo,hi in [(0,.465),(.62,1)]:f.b(f.L*(lo+hi)/2,h-.055,.043,f.L*(hi-lo),.13,.085,'p02 aged cream stucco')
  for ss in [f.L*.465,f.L*.62]:f.line((ss,h-.03,.045),(ss,h+.19,.045),.017,'p02 olive iron')
  f.line((f.L*.465,h+.19,.045),(f.L*.62,h+.19,.045),.019,'p02 olive iron')
  for j in range(9):f.line((f.L*(.465+.155*j/8),h-.02,.045),(f.L*(.465+.155*j/8),h+.18,.045),.010,'p02 olive iron')
  return
 mat='p02 cornice salmon' if bid==248142658 else 'p02 cornice dark'
 for yy,hh,dep in [(h-.62,.14,.19),(h-.39,.26,.22),(h-.16,.13,.40),(h+.015,.13,.50),(h+.115,.065,.54)]:f.strip(yy,hh,dep,mat)
 if bid==248142659:return # broad plain layered cornice, not decorative brackets
 count=8 if bid==248142657 else 9 if bid==248142658 else 8
 for j in range(count):
  s=.20+(f.L-.40)*j/(count-1)
  for yy,ww,dd,hh in [(h-.47,.16,.38,.33),(h-.27,.20,.51,.19),(h-.15,.25,.58,.09)]:f.b(s,yy,dd/2,ww,hh,dd,mat)
  # Bracket scroll and recessed panel relief at visible cornice scale.
  p02_ring(f,s,h-.47,.061,.09,.395,mat,.022,12)
  if j<count-1 and bid in [248142657,248142658]:
   mid=s+(f.L-.4)/(count-1)/2
   shop09_frame(f,mid,h-.59,(f.L-.4)/(count-1)*.61,.16,.24,mat,.02)
   p02_ring(f,mid,h-.59,.053,.045,.27,'p02 dark lintel',.010,12)

_p02_previous_arch=shop09_arch
_p02_open_right=None
def shop09_arch(f,left,right,bottom,top,d,mat,surround,round_top=False):
 if _p02_open_right is not None and left>_p02_open_right and mat=='store09 clear glass':return
 return _p02_previous_arch(f,left,right,bottom,top,d,mat,surround,round_top)

_p02_previous_shop=photographed_shop
def photographed_shop(f,a,b,r):
 global _p02_open_right
 spec=r['design'];detail=spec.get('detailP02')
 if not detail:return _p02_previous_shop(f,a,b,r)
 kind=detail['kind'];w=b-a;c=(a+b)/2;original=f
 if kind=='market':
  OPENINGS[frontage_key(f)].append((a,.17,b,3.15));f=FidelityProjectedFacade(f,1.18)
 clean=__import__('copy').deepcopy(r)
 if kind in ['wines','market']:clean['design']['detail09']['displays']=[x for x in clean['design']['detail09']['displays'] if x['kind']!='poster']
 if kind=='bar':clean['design']['panels'][-1][0]='glass'
 if kind=='laundry':
  clean['design']['panels'][-1][0]='glass';clean['design']['base']=.18;_p02_open_right=a+w*.72
 _p02_previous_shop(f,a,b,clean)
 _p02_open_right=None
 if kind=='laundry':
  ww=(w-.14)*.24;origin=f.p(b-.075-ww,0,-.20);angle=math.radians(62)
  leaf=Facade(origin[0],origin[2],f.rx*math.cos(angle)+f.nx*math.sin(angle),f.rz*math.cos(angle)+f.nz*math.sin(angle),ww)
  shop09_arch(leaf,.02,ww-.02,.20,2.84,0,'store09 clear glass','p02 silver frame')
  shop09_frame(leaf,ww/2,1.52,ww,2.64,.03,'p02 silver frame',.031)
  leaf.line((ww-.11,1.0,.09),(ww-.11,1.40,.09),.015,'store09 brushed steel')
  p02_notice(leaf,ww*.54,1.9,ww*.28,.23,.08)
 # Close shallow-room end walls; open glass never exposes unmodeled sky.
 back=-spec['detail09'].get('displayDepth',1.1)
 for ss in [a+.025,b-.025]:f.b(ss,1.65,back/2,.05,2.95,-back,'store09 dark timber')
 if kind=='wines':
  # Two angled ivory faces share a forward center ridge, not a flat sign rectangle.
  for sa,sb,da,db in [(a,c,.36,.91),(c,b,.91,.36)]:
   aa=f.p(sa,0,da);bb=f.p(sb,0,db);ll=math.hypot(bb[0]-aa[0],bb[2]-aa[2]);ff=Facade(aa[0],aa[2],(bb[0]-aa[0])/ll,(bb[2]-aa[2])/ll,ll)
   ff.b(ll/2,4.01,0,ll,.76,.16,'store09 cream enamel')
   for yy in [3.65,4.37]:ff.b(ll/2,yy,.09,ll,.033,.04,'p02 silver frame')
   for xx in [.035,ll-.035]:ff.b(xx,4.01,.09,.035,.72,.045,'p02 silver frame')
   sign_text(ff,ll*.54,4.16,ll*.84,'EAST VILLAGE','store09 maroon enamel',.30,.101,'store09:condensed')
   sign_text(ff,ll*.54,3.85,ll*.66,'WINES','store09 maroon enamel',.28,.101,'store09:condensed')
   if sa==a:sign_text(ff,ll*.5,3.69,ll*.75,'138 FIRST AVE','store09 gray plaster',.071,.105,'store09:condensed')
   ss=ll*.72;ff.line((ss,4.37,-.02),(ss,4.56,.22),.016,'store09 dark iron');ff.b(ss,4.53,.26,.14,.09,.18,'store09 dark iron')
  # Open neon and the photographed copper screen, not an opaque flat brown pane.
  sign_text(f,a+w*.54,2.67,w*.27,'OPEN','p02 red tube',.21,.12,'store09:condensed')
  ss=a+w*.62
  for y in [1.09,2.12]:
   f.b(ss,y,-.025,w*.205,.83,.022,'p02 copper mesh')
   for j in range(14):f.line((ss-w*.096+j*w*.192/13,y-.39,.005),(ss-w*.096+j*w*.192/13,y+.39,.005),.004,'store09 aged brass')
   for j in range(16):f.line((ss-w*.096,y-.38+j*.05,.008),(ss+w*.096,y-.38+j*.05,.008),.004,'store09 dark iron')
  # Bottle silhouettes on paper. Source copy below them is intentionally not invented.
  f.b(a+w*.24,1.12,.115,w*.35,1.00,.012,'store09 paper')
  for j in range(5):
   ss=a+w*(.105+j*.055);y=.91;hh=.30+(j%3)*.07
   f.b(ss,y,.129,.10,hh,.01,['store09 bottle green','store09 aged brass'][j%2]);f.b(ss,y+hh*.62,.13,.038,.16,.011,'store09 gray plaster')
   f.b(ss,y,.14,.077,.11,.005,'store09 paper')
  for ss,yy,ww,hh,dd,mat in [(.40,.36,.52,.37,.32,'store09 paper'),(.52,.64,.43,.55,.40,'p02 door brown'),(.62,.34,.46,.32,.58,'store09 cream enamel'),(.70,.28,.30,.22,.88,'store09 printed blue'),(.44,.25,.32,.19,1.02,'store09 bottle green')]:
   x=a+w*ss;f.b(x,yy,dd,ww,hh,.30,mat);p02_notice(f,x,yy,ww*.63,hh*.50,dd+.16)
 elif kind=='bar':
  usable=w-2*spec['detail09']['pierWidth'];dc=a+spec['detail09']['pierWidth']+usable*.87
  f.b(dc,1.49,.17,usable*.26-.018,2.61,.09,'p02 green door')
  # Mathematics-inspired circular mark is individually drawn; exact logo remains an approximation.
  ss=a+w*.47;y=1.94;p02_ring(f,ss,y,.46,.49,.10,'store09 paper',.009)
  for pts in [[(-.32,-.34),(-.28,-.26),(-.28,.22),(-.31,.33),(-.12,.32),(-.02,.25),(.00,.12),(-.07,.04),(-.21,.04),(-.05,-.24),(.08,-.31)],[(.015,.24),(.12,.23),(.26,.28),(.31,.37),(.26,.24),(.24,-.26),(.31,-.32)], [(-.25,.20),(-.13,.21),(-.08,.17),(-.10,.11),(-.25,.10)]]:
   p02_curve(f,[(ss+x,y+yy) for x,yy in pts],.112,'store09 paper',.009)
  sign_text(f,ss,1.37,w*.38,'AREA 140 FIRST','store09 paper',.072,.11,'store09:condensed')
  ss=a+w*.19
  for rad,mat in [(.155,'p02 red tube'),(.12,'p02 yellow tube'),(.083,'p02 blue tube')]:
   p02_curve(f,[(ss+rad*math.cos(j*math.pi/16),2.38+rad*math.sin(j*math.pi/16)) for j in range(17)],.14,mat,.009)
  sign_text(f,ss,2.32,.45,'open','p02 green tube',.115,.15,'store09:bold')
  for j in range(8):
   x=a+w*j/7;xx=a+w*(j+1)/7
   if j<7:p02_curve(f,[(x+(xx-x)*k/8,2.94-.10*math.sin(k*math.pi/8)) for k in range(9)],.54,'store09 dark iron',.008)
   f.line((x,2.94,.54),(x,2.78,.54),.007,'store09 dark iron');rod(f.p(x,2.745,.54),f.p(x,2.79,.54),.023,'opal lamp',8)
  # Pressed-sheet folding chairs, with crossed tubular legs and rounded hand-hole backs.
  for at in [.085,.245,.405,.565]:
   ss=a+w*at;dd=.72
   f.b(ss,.64,dd,.46,.045,.42,'p02 chair gray');f.b(ss,.96,dd-.23,.45,.30,.025,'p02 chair gray')
   p02_disc(f,ss,1.005,.063,.021,dd-.209,'store09 black enamel',16)
   for dx in [-.19,.19]:
    f.line((ss+dx,.18,dd-.28),(ss+dx,.77,dd+.18),.012,'p02 chair gray');f.line((ss+dx,.18,dd+.29),(ss+dx,1.11,dd-.25),.012,'p02 chair gray')
  ss=a+w*.34;dd=1.26
  rod(f.p(ss,.57,dd),f.p(ss,.61,dd),.23,'store09 red enamel',24)
  for dx,dz in [(-.18,-.14),(.18,-.14),(0,.20)]:
   f.line((ss+dx,.19,dd+dz),(ss+dx*.75,.57,dd+dz*.75),.010,'store09 red enamel')
  for k in range(24):
   t=k*math.tau/24;u=(k+1)*math.tau/24
   f.line((ss+.21*math.cos(t),.20,dd+.21*math.sin(t)),(ss+.21*math.cos(u),.20,dd+.21*math.sin(u)),.008,'store09 red enamel')
  f.b(dc,2.14,.222,.19,.08,.012,'store09 black enamel')
  f.line((dc-usable*.13+.12,.62,.265),(dc-usable*.13+.12,2.06,.265),.017,'store09 dark iron')
  f.b(a+w*.31,.181,1.0,w*.70,.012,1.25,'store09 black enamel')
 elif kind=='laundry':
  # Bent metal canopy and its sealed ends, distinct from cloth shades.
  for pts in [[(a,3.39,.08),(b,3.39,.08),(b,3.12,.69),(a,3.12,.69)],[(a,3.12,.69),(b,3.12,.69),(b,2.98,.69),(a,2.98,.69)]]:
   pp=[f.p(*p) for p in pts];face(pp,'store09 brushed steel');face(list(reversed(pp)),'store09 brushed steel')
  for xx in [a,b]:face([f.p(xx,3.39,.08),f.p(xx,3.12,.69),f.p(xx,2.98,.69),f.p(xx,2.98,.08)],'store09 brushed steel')
  sign_text(f,a+w*.58,3.08,w*.48,'DROP OFF SERVICE','store09 paper',.115,.71,'store09:condensed')
  f.b(a+w*.17,3.075,.713,w*.24,.17,.011,'store09 paper');sign_text(f,a+w*.17,3.075,w*.21,'WASH DRY FOLD','store09 gray plaster',.068,.724,'store09:condensed')
  sign_text(f,a+w*.07,3.64,w*.21,'COSMOS','p02 laundry red',.18,.35,'store09:condensed')
  for j in range(5):
   ss=a+w*(.01+j*.031);yy=3.85;pts=[]
   for k in range(10):t=math.pi/2+k*math.pi/5;r=.026 if k%2 else .057;pts.append(f.p(ss+r*math.cos(t),yy+r*math.sin(t),.35))
   face(pts,'p02 laundry red')
  for at in [.17,.39,.61,.86]:
   ss=a+w*at;f.b(ss,.78,-.64,.70,1.10,.52,'store09 brushed steel');p02_disc(f,ss,.82,.22,.22,-.365,'store09 dark iron');p02_ring(f,ss,.82,.24,.24,-.35,'p02 silver frame',.028)
   f.b(ss,1.19,-.35,.58,.14,.025,'store09 paper');p02_disc(f,ss+.14,1.20,.035,.035,-.327,'store09 dark iron',12)
  for at in [.02,.36,.72]:f.b(a+w*at,1.51,-.25,.035,2.56,.08,'p02 laundry red')
  for j in range(16):f.line((a+w*(.02+j*.70/15),.38,.19),(a+w*(.02+j*.70/15),1.13,.19),.012,'p02 silver frame')
  f.b(a+w*.37,1.13,.19,w*.72,.035,.055,'p02 silver frame')
  p02_notice(f,a+w*.84,1.73,w*.07,.23,-.07)
 elif kind=='drycleaner':
  for at in [.17,.40,.62]:
   ss=a+w*at;f.b(ss,1.64,-.52,.022,1.88,.04,'store09 aged brass')
   for yy in [.42,2.57]:f.b(ss,yy,-.51,.41,.025,.04,'store09 aged brass')
  f.b(a+w*.24,.89,-.47,w*.38,.30,.21,'p02 door brown')
  ss=b+.025;dd=.56
  f.b(ss,.85,dd,.42,1.36,.46,'store09 sage enamel');f.b(ss,1.59,dd,.54,.10,.53,'store09 sage enamel')
  f.b(ss,1.23,dd+.24,.28,.27,.016,'store09 black enamel');f.b(ss,1.26,dd+.251,.20,.14,.008,'store09 printed blue')
  for j in range(3):
   for k in range(3):f.b(ss-.075+k*.075,.99+j*.052,dd+.249,.028,.019,.009,'store09 brushed steel')
  f.b(ss,.77,dd+.245,.23,.047,.015,'store09 black enamel');p02_notice(f,ss,.47,.27,.26,dd+.246)
  f.b(b-w*.11,3.45,.39,.65,.31,.12,'store09 cream enamel');sign_text(f,b-w*.11,3.49,.54,'ATM','p02 laundry red',.16,.459,'store09:serif');sign_text(f,b-w*.11,3.36,.42,'24/7','store09 gray plaster',.072,.46,'store09:condensed')
 elif kind=='market':
  # Wall setback is retained; only the observed low enclosure projects forward.
  observed_awning(original,a,b,{'detail09':True,'y':3.86,'drop':.67,'depth':1.30,'valance':.16,'material':'store09 maroon canvas','text':'LIME TREE MARKET','textSize':.16,'font':'store09:serif','sidePanels':True})
  obj=sign_text(original,c,3.525,w*.92,'LIME TREE MARKET','store09 paper',.57,.80,'store09:serif')
  if obj:obj.rotation_euler=(obj.rotation_euler.to_matrix() @ Matrix.Rotation(-math.atan2(1.30,.67),3,'X')).to_euler()
  for k,(at,ww,hh) in enumerate([(.22,.065,.58),(.52,.06,.70),(.77,.055,.55)]):
   ss=a+w*at;y=1.57;p02_notice(f,ss,y,w*ww,hh,.105,'store09 printed blue' if k==1 else 'store09 paper')
   f.b(ss,y+hh*.34,.12,w*ww*.9,hh*.18,.01,'store09 printed red')
   for j in range(3):
    p02_disc(f,ss-w*ww*.24+(j%2)*w*ww*.47,y+.05-(j//2)*.17,w*ww*.15,.055,.13,'store09 aged brass',14)
  for ss in [a,b]:
   for yy in [.18,.57,3.06]:original.line((ss,yy,0),(ss,yy,1.20),.026,'p02 silver frame')
   pp=[original.p(ss,.58,0),original.p(ss,.58,1.18),original.p(ss,3.06,1.18),original.p(ss,3.06,0)];face(pp,'store09 clear glass');face(list(reversed(pp)),'store09 clear glass')
   pp=[original.p(ss,.19,0),original.p(ss,.19,1.18),original.p(ss,.56,1.18),original.p(ss,.56,0)];face(pp,'p02 market red');face(list(reversed(pp)),'p02 market red')
  sign_text(f,a+w*.88,2.1,w*.12,'ATM','p02 red tube',.21,.13,'store09:bold')
  for txt,yy in [('DONT POST',1.89),('STICKERS',1.71)]:sign_text(f,a+w*.88,yy,w*.15,txt,'store09 printed red',.10,.14,'store09:bold')
  for at in [.18,.43,.60,.81]:p02_notice(f,a+w*at,2.35,.22,.23,.11,'store09 printed blue' if at==.43 else 'store09 paper')
  # Fluorescent strips behind the glazing and a shallow visible cooler frame.
  for at in [.20,.60,.84]:f.b(a+w*at,2.70,-.55,w*.14,.028,.03,'opal lamp')
  for at in [.08,.43,.95]:shop09_frame(f,a+w*at,1.40,.65,2.13,-.84,'p02 silver frame',.025)

_p02_previous_render=render_building
def render_building(b):
 if b['id'] not in P02_IDS:return _p02_previous_render(b)
 # Direct opt-in model path prevents a guessed Ninth return or roof clutter.
 bid=b['id'];r=b['firstStmarksArchitecture']['0'];b['renderHeight']=b['firstStmarksHeight'];h=b['renderHeight']
 if bid==248142713:OPENINGS[frontage_key(Facade(b['frontages'][0]['x'],b['frontages'][0]['z'],b['frontages'][0]['rx'],b['frontages'][0]['rz'],b['frontages'][0]['length']))].append((b['frontages'][0]['length']*.465,h-.15,b['frontages'][0]['length']*.62,h))
 owner(b['address']+' P02 observed First Avenue face; estimates recorded')
 wall_mass(b,r['wall'],False)
 v=b['frontages'][0];f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']);f.wall=r['wall']
 fidelity_elevation({**b,'businesses':[],'seventhArchitecture':r},f,r)
 shop09_face(f,{'paintSurround':{'bottom':.17,'top':3.62 if bid!=248142713 else 3.14,'material':'store09 black enamel' if bid in [248142657,248142658] else 'store09 white enamel' if bid in [248142659,248142660] else 'p02 market red'}})
 p02_cornice(f,bid,h)
 for e in r['p02Face']['escapeSpecs']:p02_escape(f,e)
 for i,win in enumerate(r['windows']):
  ss=win['at']*f.L;ww=win['width']*f.L;top=win['bottom']+win['height']
  # Fine sash stops, sill ends and observed white blind positions.
  for xx in [ss-ww/2+.065,ss+ww/2-.065]:f.b(xx,win['bottom']+win['height']/2,-.089,.014,win['height']-.12,.016,win['frame'])
  if bid==248142657:
   pts=[(ss-ww*.61,top+.24),(ss+ww*.61,top+.24),(ss+ww*.51,top+.02),(ss-ww*.51,top+.02)]
   face([f.p(x,y,.115) for x,y in pts],'p02 ivory stone');face([f.p(x,y,.115) for x,y in reversed(pts)],'p02 ivory stone');f.b(ss,top+.20,.145,.22,.31,.09,'p02 ivory stone')
   if i<3:
    for dx in [-.36,-.18,0,.18,.36]:f.line((ss+dx,win['bottom'],.19),(ss+dx,win['bottom']+.44,.19),.006,'p02 olive iron')
    f.line((ss-ww/2,win['bottom']+.34,.19),(ss+ww/2,win['bottom']+.34,.19),.010,'p02 olive iron')
  drops={248142657:{0:.75,1:.46,2:.11,3:.25,4:.18},248142658:{0:.70,1:.80,2:.62,5:.35},248142659:{0:.24,2:.36},248142660:{1:.35},248142713:{0:.23,1:.20,6:.30}}[bid]
  if i in drops:
   for j in range(int(win['height']*drops[i]/.065)):f.b(ss,top-.07-j*.065,-.13,ww-.13,.029,.012,'store09 cream canvas')
 if bid==248142657:
  for yy in [6.29,6.43]:
   f.strip(yy,.07,.065,'p02 dark red brick')
   for j in range(int(f.L/.19)):f.b((j+.5)*.19,yy,.10,.095,.065,.065,'p02 pale mortar')
  ss=f.L*.895;ww=f.L*.15
  for j in range(11):f.b(ss-ww*.44+j*ww*.088,1.50,.08,.018,2.45,.025,'store09 cream enamel')
  for yy in [.52,1.23,2.00,2.66]:f.b(ss,yy,.093,ww*.93,.024,.025,'store09 cream enamel')
  for yy in [.80,1.66,2.34]:
   for dx in [-ww*.25,ww*.25]:p02_ring(f,ss+dx,yy,.055,.068,.108,'store09 cream enamel',.009,12)
  p02_notice(f,ss+.15,1.65,.16,.25,.12)
 elif bid==248142658:
  for yy,hh,dd in [(3.62,.13,.20),(3.85,.16,.13),(3.98,.07,.23)]:f.strip(yy,hh,dd,'p02 cornice salmon')
  p02_curve(f,[(f.L*.08,3.74),(f.L*.90,3.74),(f.L*.93,3.68),(f.L*.93,3.55)],.25,'p02 salmon iron',.012)
  ss=f.L*.12
  for yy,ww,dd in [(.21,f.L*.20,.50),(.28,f.L*.185,.34)]:f.b(ss,yy,dd/2,ww,.10,dd,'p02 ivory stone')
  f.b(ss,3.19,.28,.17,.27,.21,'p02 olive iron');rod(f.p(ss,3.10,.39),f.p(ss,3.22,.39),.048,'opal lamp',12)
 elif bid==248142659:
  ss=f.L*.23
  f.b(ss,.56,.10,.28,.48,.11,'store09 black enamel')
  for j in range(6):f.b(ss,.37+j*.072,.167,.28,.027,.023,'store09 white enamel')
  # Ribbed glass and small hood on the separate residential doorway.
  ss=f.L*.115
  for j in range(12):f.b(ss-.39+j*.065,2.12,-.112,.012,.90,.012,'store09 cream enamel')
  f.b(ss,3.14,.27,f.L*.21,.16,.55,'store09 white enamel')
 for d in r['doors']:
  ss=f.L*d['at'];right=ss+f.L*d['width']/2+.065
  f.b(right,1.52,.13,.10,.23,.04,'store09 aged brass')
  for j in range(4):f.b(right,1.45+j*.037,.157,.057,.012,.006,'store09 dark iron')
 # Fixed cable/pipe paths observed at party-wall margins, not random facade clutter.
 if bid in [248142658,248142659,248142660]:
  ss=f.L*(.025 if bid!=248142659 else .985)
  f.line((ss,3.7,.095),(ss,h-.24,.095),.010,'p02 dark lintel')

_p02_original_box=box
def box(x,y,z,w,h,depth,mat,angle=0):
 # The base wall finisher normally emits a continuous coping across each edge.
 # Split this one known edge, leaving all other cap/body geometry untouched.
 if DETAIL_SEED==248142713 and abs(y-13.45)<.001 and abs(h-.18)<.001 and abs(w-10.275)<.002 and x<16:
  rx=math.cos(-angle);rz=math.sin(-angle)
  for lo,hi in [(0,.465),(.62,1)]:
   offset=w*((lo+hi)/2-.5)
   _p02_original_box(x+rx*offset,y,z+rz*offset,w*(hi-lo),h,depth,mat,angle)
  return
 return _p02_original_box(x,y,z,w,h,depth,mat,angle)
