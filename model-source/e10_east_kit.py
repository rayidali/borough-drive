"""Individual Tenth east facades. Only the thirty assigned owners dispatch here.

Photos remain private references. Reproducible lettering, carvings and material
geometry are authored approximations; dimensions beyond footprints are estimated.
"""
E10_EAST_IDS={-577810,248142887,248142888,248142890,248142891,248142892,248142893,248142894,248142895,248142896,248142897,248142898,248142899,248142900,248142901,248142902,248142903,248142904,248142905,248142906,248142907,248142908,248142909,248142910,248142911,248142912,248142913,248142914,248142953,248142975}
material('te pale buff brick',(.69,.63,.49),.90)
material('te pale limestone',(.81,.80,.72),.90)
material('te rose ashlar',(.62,.47,.42),.90)
material('te gray painted brick',(.43,.43,.43),.90)
material('te lime letters',(.50,.86,.10),.72)
material('te cyan board',(.23,.69,.72),.83)
material('te orange board',(.88,.37,.14),.83)
material('te club lower paint',(.49,.50,.39),.88)
material('te blue entry',(.18,.27,.30),.86)
MATS['te blue entry']['storefront09Surface']=2
for name,rgb,kind in [('charcoal brick',(.19,.20,.20),0),('church brick',(.47,.24,.18),0),('church trim',(.39,.19,.13),0),('copper roof',(.19,.29,.25),6),('slate roof',(.27,.29,.27),0),('peach canvas',(.76,.51,.39),5),('pink curtain',(.72,.45,.49),5),('cream paint',(.83,.80,.66),2),('sage bench',(.57,.67,.53),6),('maroon canvas',(.31,.065,.10),5),('club blue',(.08,.25,.38),6),('glass block',(.61,.70,.66),6),('green porthole',(.09,.22,.17),2),('yellow paint',(.76,.57,.17),2)]:
 material('te '+name,rgb,.84)
 if kind:MATS['te '+name]['storefront09Surface']=kind

def te_curtain(f,a,b,y=.60,top=2.68,d=-.56,mat='te pink curtain'):
 f.b((a+b)/2,(y+top)/2,d,b-a,top-y,.035,mat)
 for j in range(max(2,round((b-a)/.075))):
  x=a+(j+.5)*(b-a)/max(2,round((b-a)/.075));f.b(x,(y+top)/2,d+.045,.045,top-y,.07,mat)

def te_mask(f,x,y,scale,mat):
 # Same source-inspired outline and projecting profile as the masonry masks;
 # attached scrolls omit hidden tube backs, never free-standing ironwork.
 relief=EtCarvedRelief(f)
 p02_disc(f,x,y,.10*scale,.13*scale,.21,mat,12)
 for side in [-1,1]:
  p02_ring(relief,x+side*.055*scale,y+.025*scale,.025*scale,.025*scale,.235,mat,.01*scale,10)
  ee_scroll(relief,x+side*.16*scale,y,.055*scale,mat,.18)
 f.b(x,y-.035*scale,.25,.032*scale,.080*scale,.04,mat)

def te_bench(f,x,d,w,mat,back=True):
 for j in range(4):f.b(x,.61,d+(j-1.5)*.075,w,.045,.065,mat)
 for side in [-1,1]:
  xx=x+side*w*.37
  for dd in [-.11,.12]:f.line((xx,.18,d+dd),(xx,.61,d+dd),.022,mat)
  if back:f.line((xx,.61,d-.14),(xx,1.1,d-.18),.025,mat)
 if back:
  for yy in [.78,.92,1.06]:f.b(x,yy,d-.17,w,.065,.035,mat)

def te_bistro_chair(f,x,d):
 mat='eb white wood';f.b(x,.60,d,.34,.025,.33,mat)
 for side in [-1,1]:
  xx=x+side*.16
  f.line((xx,.17,d-.20),(xx,.62,d+.16),.013,mat);f.line((xx,.17,d+.20),(xx,.62,d-.16),.013,mat)
  f.line((xx,.60,d-.16),(xx,1.06,d-.21),.014,mat)
 p02_ring(f,x,.95,.15,.18,d-.21,mat,.012,28)
 ee_scroll(f,x,.95,.044,mat,d-.20)

def te_books(f,a,b,y,d=-.55):
 for j in range(max(2,round((b-a)/.13))):
  x=a+(j+.5)*(b-a)/max(2,round((b-a)/.13));hh=.17+(j%3)*.045
  f.b(x,y+hh/2,d,.075,hh,.10,['eb white wood','ee pale yellow','eb green wood','eb pink enamel'][j%4])
  f.b(x,y+hh*.65,d+.054,.047,.023,.008,'store09 paper')

def te_slope_word(f,x,y,w,h,text,mat,y0,drop,dep,font='sans'):
 d=.10+(y0-y)/drop*dep+.032
 obj=et_text(f,x,y,w,h,text,mat,d,font)
 if not obj:return
 slope=math.atan2(drop,dep);cs=math.cos(slope);sn=math.sin(slope)
 obj.rotation_euler=Matrix((Vector((f.rx,-f.rz,0)),Vector((-f.nx*cs,f.nz*cs,sn)),Vector((f.nx*sn,-f.nz*sn,cs)))).transposed().to_euler()
 obj.scale.y/=sn;n01_center_text(obj,f,x,y,d)

def te_flat_hatch(f,a,b,d=.18,depth=.90):
 ee_front([f.p(a,.185,d),f.p(b,.185,d),f.p(b,.185,d+depth),f.p(a,.185,d+depth)],'eb iron')
 for x in [a,(a+b)/2,b]:f.line((x,.195,d),(x,.195,d+depth),.009,'eb gray metal')
 f.b((a+b)/2,.205,d+depth*.55,.18,.025,.025,'eb gray metal')

def te_grid_glass(f,x,low,top,w,d=-.12,cols=2,rows=3,mat='eb iron'):
 f.b(x,(low+top)/2,d-.025,w,top-low,.025,'seventh reflective glass')
 shop09_frame(f,x,(low+top)/2,w,top-low,d,mat,.035)
 for j in range(1,cols):f.b(x-w/2+w*j/cols,(low+top)/2,d,.035,top-low,.04,mat)
 for j in range(1,rows):f.b(x,low+(top-low)*j/rows,d,w,.035,.04,mat)

def te_lancet(f,x,low,top,ww,mat='te church trim',depth=.18):
 shoulder=top-min(ww*.70,(top-low)*.38)
 for off,rr in [(.10,.055),(.22,.055),(.34,.065)]:
  fidelity_shaped_arc(f,x,shoulder,ww/2+off,top-shoulder+off,depth+off*.15,rr,mat,'pointed')
  for side in [-1,1]:f.line((x+side*(ww/2+off),low,depth+off*.15),(x+side*(ww/2+off),shoulder,depth+off*.15),rr,mat)
 f.b(x,low-.08,depth,ww+.7,.16,.34,mat)

def te_fence(f,a,b,d=.80,top=1.50,circles=False):
 for y in [.28,top-.20]:f.line((a,y,d),(b,y,d),.022,'eb iron')
 count=max(2,round((b-a)/.15))
 for j in range(count+1):
  x=a+(b-a)*j/count;f.line((x,.17,d),(x,top,d),.012,'eb iron')
  if circles:p02_ring(f,x,top-.22,.060,.070,d,'eb iron',.010)

def te_dining(f):
 # The dated curb enclosure partly conceals 259; preserve its open sidewalk.
 a=.12;b=f.L-.12;d=3.45;dep=1.35;n=4
 for j in range(n):
  x0=a+(b-a)*j/n;x1=a+(b-a)*(j+1)/n;c=(x0+x1)/2
  f.b(c,.65,d+dep/2,x1-x0-.04,.93,.07,'eb plywood')
  for x in [x0,x1]:
   f.b(x,1.48,d,.075,2.62,.075,'eb oak wood');f.b(x,1.48,d+dep/2,.075,2.62,.075,'eb oak wood')
  f.line((x0,.25,d+dep/2+.04),(x1,2.75,d+dep/2+.04),.035,'eb oak wood')
  f.b(c,2.74,d+dep/2,x1-x0,.10,.09,'eb oak wood')
  ee_front([f.p(x0,1.12,d+dep/2),f.p(x1,1.12,d+dep/2),f.p(x1,2.67,d+dep/2),f.p(x0,2.67,d+dep/2)],'store09 clear glass')
  ee_front([f.p(x0,2.78,d-.65),f.p(x1,2.78,d-.65),f.p(x1,2.70,d+.72),f.p(x0,2.70,d+.72)],'eb taupe canvas')
  p03_tags(f,x0+.05,x1-.05,.35,.97,d+dep/2+.05,259+j)

_te_previous_shop=photographed_shop
def photographed_shop(f,a,b,r):
 detail=r['design'].get('detailE10East')
 if not detail:return _te_previous_shop(f,a,b,r)
 k=detail['kind'];w=b-a;c=(a+b)/2;design=r['design'];frame=design['detail09']['frame']
 _te_previous_shop(f,a,b,r)
 # Every new display has a closed shallow shell, including its oblique ends.
 low=design['base'];top=design['head']
 f.b(c,(low+top)/2,-1.06,w,top-low,.055,'recess shadow')
 for xx in [a+.025,b-.025]:f.b(xx,(low+top)/2,-.51,.05,top-low,1.10,frame)
 for yy in [low,top]:f.b(c,yy,-.51,w,.045,1.10,frame)
 if k=='lephin':
  for x in [a+.09,b-.09]:
   f.b(x,1.7,.11,.17,3.0,.24,'te cream paint');f.b(x,2.98,.16,.28,.18,.33,'te cream paint')
   for off in [-.04,.04]:f.line((x+off,.30,.25),(x+off,2.88,.25),.013,'te cream paint')
  eb_panel(f,a,b,3.20,.28,'te cream paint');et_foliage(f,a+.10,b-.10,3.20,'te cream paint',.23)
  te_curtain(f,a+.15,a+w*.56,mat='te yellow paint',d=-.82)
  et_text(f,a+w*.32,2.17,w*.46,.22,'Lê','store09 paper',.045,'serif');et_text(f,a+w*.32,1.88,w*.46,.24,'Phin','store09 paper',.045,'serif')
  for yy in [.81,1.25]:
   f.b(a+w*.30,yy,-.65,w*.49,.045,.28,'eb oak wood')
   for j in range(4):
    xx=a+w*(.10+j*.11);rod(f.p(xx,yy+.03,-.61),f.p(xx,yy+.17,-.61),.065,'eb silver metal',20)
    rod(f.p(xx,yy+.17,-.61),f.p(xx,yy+.19,-.61),.09,'eb silver metal',20)
  bx=a+w*.55;eb_board(f,bx,.17,'',d=1.0)
  f.b(bx,.69,1.035,.52,.75,.012,'te cream paint')
  et_text(f,bx,.91,.40,.14,'Lê','eb iron',1.052,'serif');et_text(f,bx,.74,.40,.14,'Phin','eb iron',1.052,'serif')
  eb_arc(f,bx,.39,.15,.19,1.054,.025,'te cyan board')
  for xx in [bx-.15,bx+.15]:f.line((xx,.30,1.054),(xx,.39,1.054),.025,'te cyan board')
  ee_scroll(f,bx,.47,.068,'te orange board',1.063)
 elif k=='halfmoon':
  eb_panel(f,a,b,3.28,.52,'eb iron');et_text(f,c,3.29,w*.94,.24,'Half moon convenience','store09 paper',.27,'italic')
  nb_ac(f,a+w*.18,2.54,.66,.34,.18)
  eb_bottles(f,a+w*.36,b-.08,.82,rows=3)
  for j in range(6):f.b(a+w*(.39+j*.085),.59,-.48,.18,.29,.18,['eb yellow enamel','eb red wood','eb blue enamel'][j%3])
 elif k=='kavasutra':
  et_canopy(f,a,b,'eb blue canvas',y=3.53,drop=.49,dep=1.05)
  for yy in [3.22,3.33]:
   dd=.10+(3.53-yy)/.49*1.05+.022
   f.line((a,yy,dd),(b,yy,dd),.045,'store09 paper')
  et_text(f,b-w*.17,2.99,w*.24,.08,'KAVA BAR','store09 paper',1.18,'condensed')
  et_text(f,a+w*.34,2.06,w*.56,.17,'KAVASUTRA','te cream paint',.055,'condensed:1:0.15')
  et_text(f,a+w*.34,1.88,w*.43,.10,'KAVA BAR','te cream paint',.055,'condensed')
  f.line((a+w*.10,1.77,.06),(a+w*.58,1.77,.06),.007,'te cream paint')
  te_bench(f,a+w*.32,-.62,w*.57,'eb red wood');f.b(a+w*.31,.73,.26,w*.57,.10,.50,'eb oak wood')
 elif k=='livelive':
  for yy,hh in [(3.22,.25),(.40,.16)]:eb_panel(f,a,b,yy,hh,'et pale blue')
  for xx in [a+.07,b-.07]:
   f.b(xx,1.8,.10,.14,2.8,.22,'et pale blue')
   for dx in [-.035,.035]:f.line((xx+dx,.40,.23),(xx+dx,2.9,.23),.010,'et pale blue')
  et_foliage(f,a+.12,b-.12,3.22,'et pale blue',.23)
  nb_ac(f,a+w*.16,2.68,.66,.30,.19)
  eb_bottles(f,a+w*.42,b-.10,.69,rows=1,colors=['eb oak wood','eb white wood'])
  for yy in [.75,1.18,1.63]:f.b(a+w*.68,yy,-.83,w*.55,.045,.25,'eb oak wood')
 elif k=='lucie':
  # The header rolls outward in depth; it is not a triangular facade pediment.
  ee_curved(f,a,b,'te yellow paint',y=3.29,drop=.26,dep=.19)
  for xx in [a+.07,b-.07]:f.b(xx,1.7,.13,.14,2.9,.22,'te yellow paint')
  te_curtain(f,a+.12,a+w*.66,y=.56,top=1.08,d=.005)
  et_text(f,a+w*.34,1.28,w*.54,.13,'FROM LUCIE','store09 paper',.075,'serif')
  for yy in [1.08,1.75,2.42]:f.b(a+w*.85,yy,-.15,w*.27,.035,.08,'te yellow paint')
  f.b(c,1.59,-1.02,w-.10,2.45,.035,'eb white wood')
  f.b(a+w*.34,.88,-.30,w*.57,.055,.42,'eb white wood')
  for j in range(5):
   x=a+w*(.11+j*.11);ee_ball(f,x,.99,-.27,.09,'eb buff stone');p02_disc(f,x,1.03,.04,.025,-.17,'eb pink enamel',12)
  eb_plant(f,b-.13,.17,.76,.45)
  tx=a+w*.30;td=1.08;rod(f.p(tx,.91,td),f.p(tx,.96,td),.31,'eb white wood',28)
  for dx in [-.18,.18]:
   for sign in [-1,1]:f.line((tx+dx,.17,td+sign*.24),(tx+dx,.91,td-sign*.21),.013,'eb white wood')
  for xx in [a+w*.30-.48,a+w*.30+.48]:te_bistro_chair(f,xx,1.05)
 elif k=='niconeco':
  eb_panel(f,a,b,3.17,.31,'te cream paint')
  x=a+w*.66
  for j,ch in enumerate('niconeco'):
   t=(j-3.5)/3.5;et_text(f,x+t*w*.18,1.91+.11*(1-t*t),w*.06,.12,ch,'store09 paper',.045,'serif')
  et_text(f,x,1.73,w*.38,.11,'zakkaya','store09 paper',.045,'serif')
  for side in [-1,1]:
   ee_front([f.p(x,1.48,.05),f.p(x+side*.22,1.54,.05),f.p(x+side*.22,1.32,.05),f.p(x,1.27,.05)],'store09 paper')
   for j in range(3):f.line((x+side*.04,1.34+j*.04,.065),(x+side*.19,1.39+j*.04,.065),.004,'eb oak wood')
   for j in range(6):
    yy=1.24+j*.09;xx=x+side*(.33+.06*math.sin(j));f.line((xx,yy,.06),(xx+side*.04,yy+.08,.06),.006,'store09 paper');p02_disc(f,xx+side*.04,yy+.06,.025,.035,.06,'store09 paper',10)
  for yy in [.73,1.08]:f.b(x,yy,-.54,w*.57,.04,.30,'eb oak wood');te_books(f,a+w*.37,b-.12,yy+.03)
  for xx in [a+w*.51,a+w*.85]:
   f.line((xx,2.8,-.54),(xx,2.43,-.54),.009,'eb iron');ee_ball(f,xx,2.34,-.54,.16,'eb pale fabric')
  eb_plant(f,b-.11,.17,.77,.47)
 elif k=='porthole':
  # Solid opaque composition with a single octagonal opening.
  f.b(c,1.61,.06,w,2.90,.14,'te green porthole')
  x=a+w*.34;p02_disc(f,x,1.98,.52,.52,.145,'store09 paper',8);p02_disc(f,x,1.98,.43,.43,.157,'seventh reflective glass',8)
  for yy in [.43,2.85]:f.b(c,yy,.15,w,.09,.07,'te green porthole')
  xx=a+w*.83;shop09_frame(f,xx,1.55,w*.24,2.58,.17,'eb green wood',.06);f.b(xx,1.70,.18,w*.14,1.71,.025,'seventh reflective glass')
  f.b(xx-w*.06,1.27,.22,.03,.25,.04,'eb gold metal');nb_ac(f,a+w*.82,2.77,.73,.32,.20)
 elif k=='eastsidestory':
  eb_panel(f,a,b,3.25,.38,'eb white wood')
  for x in [a+.10,b-.10]:
   f.b(x,1.70,.15,.21,2.87,.27,'eb white wood');f.b(x,2.94,.18,.35,.22,.35,'eb white wood')
   for dx in [-.06,0,.06]:f.line((x+dx,.44,.30),(x+dx,2.8,.30),.012,'eb white wood')
  for side in [-1,1]:
   xx=c+side*w*.17
   f.b(xx,1.63,-.03,w*.33,2.60,.08,'eb white wood')
   shop09_frame(f,xx,.66,w*.25,.51,.09,'eb white wood',.04)
   te_grid_glass(f,xx,1.00,2.53,w*.19,.065,1,1,'eb white wood')
   f.b(c+side*.035,1.29,.13,.018,.22,.04,'eb gray metal')
  te_grid_glass(f,c,2.62,2.96,w*.82,.065,2,1,'eb white wood')
  et_text(f,c,2.83,w*.78,.09,'EASTSIDE STORY','eb iron',.105,'serif')
 elif k=='whistle':
  et_canopy(f,a,b,'eb black canvas',y=3.68,drop=.65,dep=.92)
  cy=3.36;rr=.20;pts=[]
  for j in range(40):
   ang=j*math.tau/40;xx=c+rr*math.cos(ang);yy=cy+rr*math.sin(ang);pts.append(f.p(xx,yy,.10+(3.68-yy)/.65*.92+.03))
  ee_front(pts,'store09 paper');te_slope_word(f,c,cy,.30,.075,'whistle','eb iron',3.68,.65,.92)
  et_text(f,c,2.96,w*.52,.13,'whistle','store09 paper',1.05,'italic')
  bx=a+w*.43;bw=w*.70;te_bench(f,bx,.82,bw,'te sage bench',False)
  for yy in [.73,1.10]:f.line((bx-bw/2,yy,.64),(bx+bw/2,yy,.64),.021,'te sage bench')
  count=round(bw/.18)
  for j in range(count):
   xx=bx-bw/2+j*bw/count;dx=bw/count
   for yy in [.73,.915]:
    f.line((xx,yy,.64),(xx+dx,yy+.185,.64),.010,'te sage bench')
    f.line((xx,yy+.185,.64),(xx+dx,yy,.64),.010,'te sage bench')
  for xx in [bx-bw/2,bx+bw/2]:
   f.line((xx,.60,.95),(xx,.81,.95),.018,'te sage bench');f.line((xx,.81,.95),(xx,1.04,.65),.018,'te sage bench')
  for yy in [.81,1.34]:
   f.b(a+w*.33,yy,-.53,w*.57,.045,.31,'eb oak wood')
   for j in range(4):
    xx=a+w*(.12+j*.13)
    if j%2:rod(f.p(xx,yy+.03,-.51),f.p(xx,yy+.20,-.51),.065,'eb pale fabric',16)
    else:f.b(xx,yy+.12,-.51,.15,.20,.12,'eb blue enamel' if j==0 else 'ee pale yellow')
 elif k=='bleach':
  count=max(8,round(w/.24))
  for j in range(count):et_canopy(f,a+w*j/count,a+w*(j+1)/count,'eb white canvas' if j%2 else 'eb black canvas',y=3.68,drop=.65,dep=.95)
  for row,col in enumerate(['eb yellow enamel','eb blue enamel','eb pink enamel','te lime letters']):et_text(f,a+w*.64,1.96-row*.13,w*.40,.085,'1-900-BLEACH ME',col,.05,'sans')
  for row in range(3):
   for col in range(3):
    xx=a+w*(.44+col*.17);yy=2.63-row*.20;p02_ring(f,xx,yy,.080,.080,-.11,'eb silver metal',.012,24)
    p02_disc(f,xx,yy,.069,.069,-.105,['seventh reflective glass','te glass block','eb gray metal'][(row+col)%3],24)
  te_bench(f,a+w*.65,.90,w*.60,'eb red metal')
 elif k=='alterations':
  te_curtain(f,a+.10,a+w*.63,mat='eb pale fabric')
  f.b(a+w*.34,.39,.08,w*.61,.46,.06,'eb iron')
  xx=a+w*.84;f.b(xx,1.57,.02,w*.29,2.72,.06,'eb iron')
  shop09_frame(f,xx,1.60,w*.27,2.51,.08,'eb iron',.045)
  shop09_frame(f,xx,1.65,w*.22,1.53,.11,'eb charcoal stone',.035)
  for yy in [.30,.38,.46]:f.b(xx,yy,.11,w*.22,.035,.05,'eb charcoal stone')
  f.b(xx+w*.11,1.27,.15,.025,.26,.07,'eb gold metal')
  eb_blade(f,b-.04,3.05,'ALTERATIONS','eb white wood',color='eb iron')
  for xx in [a+.05,a+w*.65,b-.05]:f.b(xx,1.65,.12,.08,2.9,.17,'eb iron')
 elif k=='271closed':
  eb_panel(f,a,b,3.20,.37,'eb gray stone');et_foliage(f,a+.07,b-.07,3.20,'eb gray stone',.27)
  for xx in [a+w*.25,a+w*.58,a+w*.87]:te_grid_glass(f,xx,.30,2.94,w*.27,-.10,1,3,'eb white wood')
  nb_grille(f,a+.06,b-.06,.26,2.95,.16)
  ee_shutter(f,a+.06,b-.06,.21,.51,d=.18)
 elif k=='clash':
  ee_curved(f,a,b,'eb red canvas',y=3.49,drop=.58,dep=.81)
  f.b(a+w*.35,.70,.09,w*.68,1.03,.06,'eb red wood');nb_grille(f,a+.07,a+w*.67,1.19,2.77,.14)
  for row,word in enumerate(['CLASH','CITY','TATTOO']):
   yy=.99-row*.26;step=w*.60/len(word)
   for j,ch in enumerate(word):
    xx=a+w*.35+(j-(len(word)-1)/2)*step;off=[.015,-.018,.025,-.01][j%4]
    for dx,dy in [(-.012,0),(.012,0),(0,-.012),(0,.012)]:et_text(f,xx+dx,yy+off+dy,step*.97,.23,ch,'store09 paper',.135,'sans')
    et_text(f,xx,yy+off,step*.92,.22,ch,'eb iron',.149,'sans')
 elif k=='273east':
  for row in range(5):
   y=3.44-row*.085;d=.12+row*.13
   for col in range(max(3,round(w/.27))):
    n=max(3,round(w/.27));x=a+w*(col+.5)/n
    ee_front([f.p(x-w/n*.48,y+.07,d-.065),f.p(x+w/n*.48,y+.07,d-.065),f.p(x+w/n*.48,y-.07,d+.075),f.p(x-w/n*.48,y-.07,d+.075)],'eb gray metal')
  for x in [a+.05,b-.05]:
   f.line((x,3.51,.10),(x,3.03,.76),.07,'eb gray metal');p02_ring(f,x,3.06,.08,.08,.79,'eb gray metal',.025,20)
  te_curtain(f,a+w*.38,b-.08,y=.48,top=.99)
  for xx in [a+w*.53,a+w*.73]:f.b(xx,1.72,.06,.035,2.1,.06,'eb oak wood')
  for yy in [1.24,1.94]:f.b(a+w*.67,yy,.06,w*.61,.035,.06,'eb oak wood')
  p02_notice(f,a+w*.17,1.72,.25,.34,.06)
  for xx,yy in [(a+w*.45,1.15),(a+w*.70,1.44),(a+w*.85,.81)]:p02_notice(f,xx,yy,.22,.25,.07)
 elif k=='foxtail':
  eb_panel(f,a,b,3.18,.30,'eb iron');et_text(f,a+w*.34,2.13,w*.40,.11,'FOXTAIL','store09 paper',.06,'serif')
  f.b(c,1.80,-1.015,w-.10,1.75,.025,'eb oak wood')
  for yy in [.88,1.40,2.00]:f.b(a+w*.34,yy,-.82,w*.61,.05,.23,'eb oak wood')
  for j in range(3):
   bx=a+w*(.16+j*.20);rod(f.p(bx,.89,-.52),f.p(bx,1.16,-.52),.13,'eb pale fabric',20)
   for q in range(5):
    xx=bx+(q-2)*.10;yy=1.56+(.15 if q%2 else 0)
    f.line((bx,1.04,-.51),(xx,yy,-.50),.007,'eb buff stone')
    for k2 in range(7):
     for side in [-1,1]:f.line((xx,yy-.20+k2*.04,-.50),(xx+side*.055,yy-.15+k2*.04,-.49),.006,'eb pale fabric')
  et_text(f,a+w*.34,1.99,w*.32,.055,'EAST VILLAGE','store09 paper',.06,'serif')
 elif k=='277lease':
  for j in range(3):f.b(c,3.08+j*.15,.12,w,.14,.20,'eb oak wood')
  for xx in [a+.05,b-.05]:f.b(xx,1.69,.11,.15,2.96,.20,'eb oak wood')
  x=a+w*.51;f.b(x,1.80,.07,w*.25,1.35,.025,'ee deep blue')
  for yy,txt in [(2.22,'RESTAURANT'),(2.05,'AVAILABLE'),(1.88,'FOR LEASE')]:et_text(f,x,yy,w*.23,.07,txt,'store09 paper',.09,'condensed')
 elif k=='crops':
  for aa,bb in [(a+.10,a+w*.25),(a+w*.51,a+w*.66)]:te_curtain(f,aa,bb,y=.82,top=2.73)
  f.b(a+w*.38,1.76,-1.015,w*.51,1.9,.025,'eb pale fabric')
  for yy,txt in [(2.21,'CROPS'),(2.02,'FOR'),(1.83,'GIRLS'),(1.60,'SALE')]:et_text(f,a+w*.36,yy,w*.35,.15,txt,'eb iron' if txt=='SALE' else 'ee pink letters',.06,'serif')
  ee_shutter(f,a+w*.70,b-.05,2.45,3.14,d=.13);eb_plant(f,a+w*.21,.17,.72,.47)
 elif k=='dogwash':
  x=a+w*.66;cy=1.95;p02_ring(f,x,cy,w*.22,w*.22,.07,'store09 paper',.012,48)
  et_text(f,x,1.99,w*.41,.09,'NOW YOU’RE CLEAN','store09 paper',.08,'sans')
  et_text(f,x,1.86,w*.41,.055,'SELF-SERVICE DOG WASH','store09 paper',.08,'sans')
  # Dated glass has two side-profile dogs; simple silhouettes, not an invented mascot face.
  for xx,yy,flip in [(x-.28,2.34,1),(x+.16,1.53,-1)]:
   p02_disc(f,xx,yy,.21,.09,.075,'store09 paper',20);p02_disc(f,xx+flip*.23,yy+.09,.09,.09,.075,'store09 paper',16)
   for dx in [-.13,.13]:f.line((xx+dx,yy-.04,.075),(xx+dx,yy-.22,.075),.022,'store09 paper')
   f.line((xx-flip*.17,yy+.02,.075),(xx-flip*.30,yy+.18,.075),.022,'store09 paper')
  eb_bottles(f,a+w*.39,b-.12,.87,rows=1)
  te_bench(f,a+w*.65,.91,w*.65,'eb oak wood',False);eb_board(f,b+.16,.17,'',d=.95)
 elif k=='body':
  et_canopy(f,a,b,'te peach canvas',y=3.62,drop=.62,dep=.99)
  for xx,ww,hh,txt in [(a+w*.17,w*.23,.31,'be.'),(a+w*.65,w*.59,.19,'body evolutions')]:
   yy=3.29;dd=.10+(3.62-yy)/.62*.99+.03
   obj=et_text(f,xx,yy,ww,hh,txt,'store09 paper',dd,'italic')
   slope=math.atan2(.62,.99);cs=math.cos(slope);sn=math.sin(slope)
   obj.rotation_euler=Matrix((Vector((f.rx,-f.rz,0)),Vector((-f.nx*cs,f.nz*cs,sn)),Vector((f.nx*sn,-f.nz*sn,cs)))).transposed().to_euler();obj.scale.y/=sn;n01_center_text(obj,f,xx,yy,dd)
  for xx in [a+w*.18,a+w*.36,a+w*.54]:f.b(xx,1.65,.07,.055,2.4,.08,'eb white wood')
  for yy in [.99,1.66,2.33]:f.b(a+w*.37,yy,.07,w*.71,.055,.08,'eb white wood')
  f.b(a+w*.36,.46,.65,w*.69,.42,.35,'eb white wood')
  for j in range(6):eb_plant(f,a+w*(.07+j*.12),.61,.65,.24)
  te_fence(f,a+.03,a+w*.72,.92,1.05)
  for xx in [a+w*.84]:te_grid_glass(f,xx,.37,2.76,w*.23,.08,1,4,'eb white wood')
  p02_disc(f,b-.10,2.0,.17,.17,.15,'eb yellow enamel',28)
  for sign in [-1,1]:f.line((b-.22,2.0-sign*.12,.17),(b+.02,2.0+sign*.12,.17),.015,'eb iron')
  p02_notice(f,a+w*.83,1.91,.22,.30,.08)
 elif k in ['280lease','280dark']:
  eb_panel(f,a,b,3.18,.38,'eb iron');et_foliage(f,a+.07,b-.07,3.18,'eb iron',.24)
  if k=='280lease':
   f.b(a+w*.36,1.95,.06,w*.42,1.21,.02,'eb iron')
   for j,word in enumerate(['RETAIL','FOR','LEASE']):et_text(f,a+w*.36,2.30-j*.24,w*.39,.19,word,'store09 paper',.08,'sans')
   p03_tags(f,a+.08,b-.08,.85,1.60,.12,280)
  else:
   f.line((a+w*.65,2.8,-.57),(a+w*.65,2.39,-.57),.01,'eb iron');p02_disc(f,a+w*.65,2.23,.30,.17,-.54,'eb pale fabric',32)
   f.b(a+w*.65,.81,-.55,w*.54,.07,.40,'eb white wood');f.b(c,1.75,-1.015,w-.13,1.77,.025,'eb pale fabric')
 elif k=='physical':
  ee_hood(f,a,b,3.10,'eb silver metal',.48);nb_ac(f,a+w*.84,2.65,.57,.32,.16)
  et_text(f,a+w*.37,2.58,w*.43,.10,'PHYSICAL','eb iron',.06,'sans');et_text(f,a+w*.37,2.44,w*.43,.10,'THERAPY','eb iron',.06,'sans')
  f.b(a+w*.075,2.51,.06,.26,.29,.025,'eb iron');et_text(f,a+w*.075,2.51,.23,.13,'PT','eb gold metal',.08,'serif')
  for aa,bb in [(a+.08,a+w*.19),(a+w*.60,a+w*.70)]:te_curtain(f,aa,bb,y=.82,top=2.74,mat='eb pale fabric',d=-.17)
  for j in range(10):
   yy=.90+j*.16
   for xx in [a+w*.12,a+w*.65]:ee_scroll(f,xx,yy,.035,'eb gray metal',-.10)
  f.b(c,1.8,-1.015,w-.10,1.95,.025,'eb pale fabric')
 elif k=='queencity':
  et_canopy(f,a,b,'eb black canvas',y=3.50,drop=.47,dep=.71)
  count=round(w/.14)
  for j in range(count):p02_disc(f,a+w*(j+.5)/count,2.81,w/count*.52,.075,.83,'eb black canvas',16)
  et_text(f,a+w*.66,2.49,w*.59,.16,'Queen City Group','eb gold metal',.06,'script')
  for row in range(4):
   for col in range(3):
    x=a+w*(.43+col*.18);yy=2.14-row*.36;f.b(x,yy,.055,w*.15,.29,.018,'store09 paper')
    f.b(x,yy+.045,.071,w*.12,.12,.007,'et pale blue');f.b(x,yy-.076,.073,w*.10,.011,.009,'eb iron')
 elif k=='laundromat':
  ee_curved(f,a,b,'te maroon canvas',y=3.53,drop=.64,dep=.97)
  # Broad rounded vertical sign face with separately composed icon / wording.
  et_text(f,a+w*.56,3.17,w*.83,.25,'TEN ST. LAUNDROMAT','store09 paper',1.045,'condensed')
  et_text(f,a+w*.58,2.91,w*.78,.10,'DROP OFF SERVICE  *  DRY CLEAN  *  ALTERATION  *  FREE PICK UP & DELIVERY','eb yellow enamel',1.12,'condensed')
  xx=a+w*.065;shop09_frame(f,xx,3.16,.28,.32,1.055,'store09 paper',.018);p02_ring(f,xx,3.12,.08,.08,1.075,'store09 paper',.012,24)
  for dx,dy in [(-.10,.27),(.02,.26),(.12,.22),(-.03,.38)]:p02_disc(f,xx+dx,3.16+dy,.028,.028,1.06,'store09 paper',16)
  for aa,bb in [(a,a+w*.33),(a+w*.55,b)]:
   f.b((aa+bb)/2,.49,.09,bb-aa,.61,.08,'eb iron')
   for yy in [.29,.40,.51,.62]:f.b((aa+bb)/2,yy,.14,(bb-aa)*.80,.025,.03,'eb gray metal')
  f.b(c,1.72,-1.015,w-.10,1.99,.025,'eb pale fabric')
  eb_clothes(f,a+w*.62,b-.10,2.30,d=-.65)
  te_grid_glass(f,a+w*.44,.26,2.67,w*.21,.07,1,2,'eb iron')
  p02_notice(f,a+w*.25,1.34,.24,.36,.08)
  et_text(f,a+w*.13,1.64,w*.18,.09,'Alterations','eb iron',.07,'serif');et_text(f,a+w*.13,1.51,w*.18,.085,'& Repairs','eb iron',.07,'serif')
  ee_chair(f,b-.80,1.05,'eb gray metal');f.b(b-.80,.62,1.05,.39,.09,.37,'eb red wood');f.b(b-.80,.95,.87,.38,.29,.07,'eb red wood')
  xx=b-.31;dd=1.03;f.b(xx,.61,dd,.34,.035,.34,'eb white wood')
  for side in [-1,1]:
   px=xx+side*.16;f.line((px,.17,dd-.20),(px,.65,dd+.17),.014,'eb white wood');f.line((px,.17,dd+.20),(px,1.02,dd-.21),.014,'eb white wood')
  f.b(xx,.96,dd-.20,.34,.20,.035,'eb white wood');te_flat_hatch(f,a+w*.57,b-.12)

def te_architecture(f,r,h):
 s=r['e10East'];n=s['number'];mat=s['trim']
 mechanics={**s}
 if s.get('curvedCrown'):mechanics['cornice']='carriage'
 if n=='280':mechanics['escapes']=[]
 et_architecture(f,{**r,'e10Block':mechanics},h)
 if n=='280':
  for span in s['escapes']:ee_escape(f,{'span':span,'levels':[s['upperBottom']-.17+i*s['step'] for i in range(s['rows'])],'material':'eb iron','dropAt':span[1]-.03,'ornament':'scroll'})
 if s.get('curvedCrown'):
  cm='eb brown stone' if n=='271' else 'eb iron';radius=f.L*.25;cy=h-.28;rise=.77
  for lo,hi in [(0,.25),(.75,1)]:
   p=f.p(lo*f.L,0,0);sub=Facade(p[0],p[2],f.rx,f.rz,(hi-lo)*f.L);eb_cornice(sub,h,{**s,'cornice':'brackets','corniceColor':'brown stone' if n=='271' else 'iron'})
  f.b(f.L*.5,h-.44,.18,radius*2,.43,.32,cm)
  et_fan(f,f.L*.5,cy,radius,rise,cm,.26)
  if n=='275':et_fan(f,f.L*.5,cy+.06,radius*.83,rise*.61,'eb gray stone',.35)
  for j in range(9):
   x=f.L*.5-radius*.92+j*radius*1.84/8;yy=cy+rise*math.sqrt(max(0,1-((x-f.L*.5)/radius)**2))
   for off in [.0,-.13]:f.b(x,yy+off,.38,.11,.14,.25,cm)
  for off in [.05,.18]:eb_arc(f,f.L*.5,cy+off,radius+off*.25,rise,.45,.045,cm,40)
 if n=='271':
  for row in range(round((h-3.65)/.52)):
   yy=3.65+row*.52;fidelity_clipped_surface(f,0,f.L,yy,yy+.018,.045,.02,'eb brown stone')
   for j in range(7):
    xx=(j+(.5 if row%2 else 0))*f.L/6
    fidelity_clipped_surface(f,xx,xx+.018,yy,yy+.52,.045,.02,'eb brown stone')
 if n in ['259','261']:
  # The lowest upper storey has coursed masonry, above the shop lintel.
  for j in range(9):
   yy=3.70+j*.29;fidelity_clipped_surface(f,0,f.L,yy,yy+.065,.08,.09,'eb red brick')
 if n=='261':
  for at in [.015,.255,.5,.745,.985]:
   x=at*f.L;f.b(x,(h+6.15)/2,.07,.18,h-6.15,.14,'eb red brick')
   for row in range(1,4):
    yy=s['upperBottom']+row*s['step']-.33
    f.b(x,yy,.13,.31,.19,.24,'eb red brick')
  for j in range(round(f.L/.20)):f.b((j+.5)*.20,6.30,.12,.09,.15,.22,'eb red brick')
 if s.get('redQuoins'):
  for x in [.14,f.L-.14]:
   for j in range(round((h-3.7)/.33)):f.b(x,3.8+j*.33,.10,.35 if j%2 else .50,.29,.20,'eb red brick')
 for w in r['windows']:
  x=w['at']*f.L;ww=w['width']*f.L;y=w['bottom'];top=y+w['height'];row=w.get('row',-1);col=w.get('col',-1)
  if s.get('pairedAprons') and row>0 and col in [1,2]:
   shop09_frame(f,x,y-.48,ww,.36,.12,mat,.04);te_mask(f,x,y-.48,.8,mat)
  if s.get('carvedPanels') and row>=0:
   et_foliage(f,x-ww*.48,x+ww*.48,top+.15,mat,.24)
   for side in [-1,1]:
    xx=x+side*(ww/2+.10);f.b(xx,y-.15,.17,.14,.32,.32,mat);p02_ring(f,xx,y-.10,.06,.09,.34,mat,.018,16)
  if n=='253' and row==3 and col in [1,2]:et_foliage(f,x-ww*.5,x+ww*.5,top+.20,mat,.21)
  if n=='255' and row==3:eb_arc(f,x,top-ww*.50,ww*.61,ww*.61,.19,.09,mat)
  if n=='265' and row==0:te_mask(f,x,top+.38,.65,mat)
  if n in ['265','269','275','277'] and row>=0:
   for side in [-1,1]:
    xx=x+side*(ww*.5+.08)
    f.b(xx,top-.06,.14,.12,.36,.28,mat);ee_scroll(f,xx,top+.015,.06,mat,.31)
    f.b(xx,y-.13,.15,.13,.25,.28,mat)
   if n=='275':eb_arc(f,x,top+.16,ww*.69,.24,.27,.055,mat,28)
  if n=='257' and row==-1:
   f.b(x,top+.17,.31,ww*1.45,.12,.35,mat)
   ee_front([f.p(x-ww*.66,top+.23,.32),f.p(x,top+.60,.32),f.p(x+ww*.66,top+.23,.32)],mat)
   for side in [-1,1]:f.line((x+side*ww*.66,top+.23,.36),(x,top+.60,.36),.055,mat)
  if n=='257' and row==1:
   eb_arc(f,x,top-ww*.5,ww*.65,ww*.65,.18,.10,'eb red brick')
   for side in [-1,1]:
    for j in range(9):f.b(x+side*(ww*.5+.13),y+j*.24,.07,.27 if j%2 else .38,.21,.12,'eb red brick')
   shop09_frame(f,x,y-.46,ww*.95,.49,.10,mat,.045)
  if s.get('brickPanels') and row in [1,2]:
   shop09_frame(f,x,y-.48,ww*.8,.36,.10,'eb red brick',.06)
   for j in range(4):f.b(x+(j-1.5)*ww*.17,y-.48,.14,ww*.11,.23,.08,'eb dark red brick')
  if s.get('pilasterBands') and row>=0:
   for yy in [y-.21,top+.23]:fidelity_clipped_surface(f,0,f.L,yy,yy+.10,.065,.13,'eb brown stone')
  if s.get('carvedKeystones') and row>=0:
   ee_front([f.p(x-.17,top+.37,.21),f.p(x+.17,top+.37,.21),f.p(x+.10,top-.02,.21),f.p(x-.10,top-.02,.21)],mat)
   for side in [-1,1]:ee_scroll(f,x+side*.28,top+.16,.055,mat,.24)
  if s.get('starTies') and row in [0,2]:
   if col<2:ee_star(f,x+f.L/6,y+w['height']*.45,.12,.14,'eb iron')
  if s.get('glassBlock') or w.get('glassBlock'):
   f.b(x,y+w['height']/2,-.06,ww,w['height'],.04,'te glass block')
   for j in range(round(ww/.20)+1):f.b(x-ww/2+j*ww/round(ww/.20),y+w['height']/2,-.025,.015,w['height'],.02,'eb gray metal')
   for j in range(round(w['height']/.20)+1):f.b(x,y+j*w['height']/round(w['height']/.20),-.025,ww,.015,.02,'eb gray metal')
 if s.get('splitPaint'):fidelity_clipped_surface(f,f.L*.50,f.L,3.63,h-.74,.025,.035,'te gray painted brick')
 if s.get('stripedAshlar'):
  for j in range(round((h-3.72)/.60)):
   yy=3.72+j*.60;fidelity_clipped_surface(f,0,f.L,yy,yy+.18,.06,.08,'eb gray stone')
  # The source has one broad paired blind arch and a raised central crown.
  top=s['upperBottom']+3*s['step']+1.8
  et_fan(f,f.L*.5,top+.06,f.L*.24,.59,mat,.23)
  f.b(f.L*.5,h+.18,.13,f.L*.39,.43,.28,'eb iron');et_fan(f,f.L*.5,h+.36,f.L*.20,.62,'eb iron',.25)
  p02_ring(f,f.L*.5,h+.55,.11,.13,.34,mat,.025,24)
  for yy in [3.65,s['upperBottom']+s['step']-.6]:
   f.strip(yy,.18,.27,mat);et_foliage(f,.05,f.L-.05,yy,mat,.29)
 if n=='251':
  for row in [1,2,3]:
   yy=s['upperBottom']+row*s['step']-.55;shop09_frame(f,f.L*.5,yy,f.L*.43,.48,.12,mat,.045)
   et_foliage(f,f.L*.30,f.L*.70,yy,mat,.18)
 if n=='255':
  for yy,ww in [(h-1.15,f.L*.24),(h-2.37,f.L*.38)]:f.b(f.L*.5,yy,.025,ww,.22,.04,'eb buff stone')
 if s.get('diaper'):
  # Diagonal red brick diamonds in the buff field, clipped around windows.
  for row in range(21):
   yy=6.9+row*.46
   if yy>h-.8:break
   for col in range(round(f.L/.46)):
    x=(col+.5)*.46
    if (col+row)%4 in [0,1]:fidelity_clipped_surface(f,x-.20,x+.20,yy,yy+.09,.05,.04,'eb red brick')
  for side in [-1,1]:f.line((f.L*.5,h+.14,.10),(f.L*(.5+side*.49),h-.05,.10),.045,'eb cream stone')
 if s.get('rustication'):
  for yy in [s['upperBottom']-.35,7.10,10.15,13.15,16.15]:fidelity_courses(f,yy+.30,mat,step=.26,bottom=yy,depth=.05)
 if s.get('brickBands'):
  for j in range(s['rows']):
   yy=s['upperBottom']+j*s['step']-.37;f.strip(yy,.10,.11,'eb pink brick')
   for q in range(round(f.L/.17)):f.b((q+.5)*.17,yy-.13,.075,.085,.11,.14,'eb pink brick')
 if s.get('corniceMedallions') or n=='251':
  for at in [.15,.50,.85]:p02_ring(f,at*f.L,h-.45,.22,.12,.34,'eb gray stone' if n=='251' else 'eb iron',.025,28)
 if s.get('balconies'):
  for row in range(s['rows']):
   yy=s['upperBottom']+row*s['step']-.12
   f.b(f.L*.5,yy-.09,.60,f.L*.94,.22,1.20,'eb cream stone')
   for y in [yy+.10,yy+1.03]:f.line((f.L*.03,y,1.18),(f.L*.97,y,1.18),.021,'eb gray metal')
   for j in range(round(f.L*.94/.15)+1):
    xx=f.L*.03+j*f.L*.94/round(f.L*.94/.15);f.line((xx,yy+.03,1.18),(xx,yy+1.03,1.18),.012,'eb gray metal')
   for xx in [f.L*.03,f.L*.97]:
    for y in [yy+.10,yy+1.03]:f.line((xx,y,.04),(xx,y,1.18),.021,'eb gray metal')
 if s.get('sideBalconies'):
  for span in [[.035,.24],[.78,.98]]:ee_escape(f,{'span':span,'levels':[s['upperBottom']+row*s['step']-.14 for row in range(s['rows'])],'material':'eb iron','balconyOnly':True,'ornament':'plain','dropAt':span[1]})
 if s.get('entryBalcony') or n=='257':
  ee_escape(f,{'span':[.68,.98],'levels':[4.9 if n=='276' else 3.85],'material':'eb iron','balconyOnly':True,'ornament':'plain','dropAt':.94})
 for d in r['doors']:
  x=d['at']*f.L;ww=d['width']*f.L;top=d['top'];low=d['bottom']
  if n in ['251','253']:
   et_foliage(f,x-ww*.63,x+ww*.63,top+.28,mat,.35)
  if n=='256':
   # Raised shield and scrolls are a separate pale carving over the rose portal.
   pp=[(-.40,.22),(-.37,-.12),(0,-.39),(.37,-.12),(.40,.22),(0,.15)]
   ee_front([f.p(x+dx,top+.45+dy,.40) for dx,dy in pp],mat)
   for (dx,dy),(ex,ey) in zip(pp,pp[1:]+pp[:1]):f.line((x+dx,top+.45+dy,.45),(x+ex,top+.45+ey,.45),.035,mat)
   for side in [-1,1]:
    xx=x+side*(ww*.5+.20);et_foliage(f,xx-.09,xx+.09,(top+low)/2,'te rose ashlar',.33)
    for yy in [low+.15,top-.06]:f.b(xx,yy,.23,.42,.22,.43,'te rose ashlar')
   for side in [-1,1]:ee_scroll(f,x+side*ww*.73,top+.60,.20,mat,.25)
  if n=='260':
   for off in [.13,.25,.36]:eb_arc(f,x,top-.31,ww*.5+off,.49,.14+off*.2,.075,'eb red wood')
   for side in [-1,1]:
    xx=x+side*(ww*.5+.19);f.b(xx,(top+low)/2,.14,.23,top-low,.26,'eb red wood')
    et_foliage(f,xx-.07,xx+.07,(top+low)/2,'eb red wood',.30)
   for xx in [x-ww*.23,x+ww*.23]:
    f.b(xx,low+1.30,-.12,ww*.32,1.35,.025,'eb pale fabric')
    shop09_frame(f,xx,low+1.30,ww*.36,1.43,-.08,'eb iron',.04)
  if n=='257':
   ee_front([f.p(x-ww*.66,top+.20,.18),f.p(x,top+.48,.18),f.p(x+ww*.66,top+.20,.18)],mat)
   for side in [-1,1]:f.line((x+side*ww*.66,top+.20,.23),(x,top+.48,.23),.045,mat)
  if n=='272':
   for xx in [x-ww*.64,x+ww*.64]:f.b(xx,(top+low)/2,.16,.22,top-low,.30,mat)
   ee_front([f.p(x-ww*.80,top+.12,.21),f.p(x,top+.58,.21),f.p(x+ww*.80,top+.12,.21)],mat);eb_lamp(f,x,top+.70,.35)
  if n in ['278','284']:f.b(x,top+.12,.13,ww+.44,.23,.24,'eb cream stone')
  if n=='276' and low>1:
   f.b(x-ww*.75,2.85,.28,.30,.24,.045,'eb gray stone');et_text(f,x-ww*.75,2.85,.25,.13,'276','eb iron',.32,'serif')
 if n=='251':
  et_closed_box(f,f.L*.71,f.L*.99,251)
  for j in range(6):f.b(f.L*.19,.10-(j+1)*.15,1.04-(j+.5)*.17,f.L*.32,.09,.17,'eb gray stone')
 if n=='255':te_fence(f,.08,f.L*.70,.60,1.0,True)
 if n=='257':
  eb_panel(f,f.L*.43,f.L*.93,3.57,.46,'eb white wood');et_text(f,f.L*.68,3.69,f.L*.43,.10,'The Tenth Street','eb blue enamel',.27,'sans');et_text(f,f.L*.68,3.50,f.L*.43,.16,'Church of Christ','eb blue enamel',.27,'sans')
  for x in [f.L*.12,f.L*.55,f.L*.94]:f.line((x,3.52,.06),(x,3.09,.83),.018,'eb iron')
  f.line((f.L*.10,3.09,.83),(f.L*.96,3.09,.83),.055,'eb iron');eb_lamp(f,f.L*.59,4.01,.68)
  for d in r['doors']:
   x=d['at']*f.L;ww=d['width']*f.L
   f.b(x,d['bottom']+.12,-.14,ww*.90,.22,.035,'eb gold metal')
   nb_grille(f,x-ww*.40,x+ww*.40,d['top']-.95,d['top']-.35,-.13)
 if n=='259':te_dining(f)
 if n=='256':
  fidelity_clipped_surface(f,0,f.L,.17,7.91,.018,.028,'te rose ashlar')
  for row in range(17):
   yy=.19+row*.46;fidelity_clipped_surface(f,0,f.L,yy,yy+.025,.065,.025,'eb brown stone')
   for col in range(10):
    xx=(col+(.5 if row%2 else 0))*f.L/9
    fidelity_clipped_surface(f,xx,xx+.023,yy,yy+.46,.065,.025,'eb brown stone')
  for a,b in [(.02,.48),(.78,.98)]:
   te_fence(f,a*f.L,b*f.L,1.43,1.46,True)
   for j in range(7):ee_scroll(f,(a+(b-a)*(j+.5)/7)*f.L,.88,.08,'eb iron',1.44)
 if n=='264':
  x=f.L*.36;ww=3.30;lo=.65;hi=2.20
  points=[(x-ww/2,.04),(x-ww*.30,.64),(x+ww*.30,.64),(x+ww/2,.04)]
  for (a,da),(b,db) in zip(points,points[1:]):
   ee_front([f.p(a,lo,da),f.p(b,lo,db),f.p(b,hi,db),f.p(a,hi,da)],'seventh reflective glass')
   for yy in [lo,lo+.66,hi]:f.line((a,yy,da+.03),(b,yy,db+.03),.035,'eb iron')
  for xx,dd in points:f.line((xx,lo,dd+.03),(xx,hi,dd+.03),.035,'eb iron')
  for (a,da),(b,db) in zip(points,points[1:]):
   ee_front([f.p(a,hi+.06,da+.10),f.p(b,hi+.06,db+.10),f.p(x+(b-x)*.78,hi+.52,.04),f.p(x+(a-x)*.78,hi+.52,.04)],'eb iron')
  f.b(x,.38,.38,ww+.13,.41,.80,'eb red brick');f.b(x,.60,.45,ww+.21,.10,.88,'eb gray stone')
  te_bench(f,x,1.0,2.6,'eb oak wood',False)
  f.line((f.L*.74,.19,.13),(f.L*.74,3.50,.13),.035,'eb gray metal')
 if n=='269':
  for j in range(round(f.L/.22)):f.b((j+.5)*.22,3.45,.12,.11,.14,.22,'eb charcoal stone')
 if n=='275':
  fidelity_clipped_surface(f,0,f.L,.17,1.20,.07,.08,'eb dark red brick')
  for d in r['doors']:
   x=d['at']*f.L;ww=d['width']*f.L
   for side in [-1,1]:
    xx=x+side*(ww*.5+.15);f.b(xx,1.70,.15,.20,2.95,.28,'eb gray stone');ee_scroll(f,xx,2.93,.09,'eb gray stone',.31)
 if n=='268':
  fidelity_courses(f,6.36,'eb white stone',step=.52,bottom=.17,depth=.06)
  for row in range(11):
   yy=.35+row*.52;fidelity_clipped_surface(f,0,f.L,yy,yy+.025,.14,.015,'eb gray stone')
   for col in range(5):
    xx=(col+(.5 if row%2 else 0))*f.L/4
    if .02<xx<f.L-.02:fidelity_clipped_surface(f,xx-.012,xx+.012,yy,yy+.52,.14,.015,'eb gray stone')
  eb_panel(f,.02,f.L-.02,6.13,.43,'eb white wood');et_text(f,f.L*.41,6.13,f.L*.79,.26,'RUSSIAN & TURKISH BATHS','eb gray metal',.29,'sans')
  et_text(f,f.L*.91,6.13,f.L*.16,.14,'Since 1892','eb gray metal',.29,'serif')
  x=f.L*.81;et_text(f,x,5.38,1.0,.24,'268','eb iron',.21,'serif');eb_blade(f,f.L-.04,5.0,'BATHS','eb white wood',color='eb iron')
  # Source gate is chain-link, separate from the stair handrail.
  aa=f.L*.04;bb=f.L*.60;dep=1.37
  for yy in [.23,1.30]:f.line((aa,yy,dep),(bb,yy,dep),.025,'eb gray metal')
  for xx in [aa,bb]:f.line((xx,.17,dep),(xx,1.45,dep),.03,'eb gray metal')
  for j in range(round((bb-aa)/.10)):
   xx=aa+j*.10
   for yy in [.30,.50,.70,.90,1.10]:
    for side in [-1,1]:f.line((xx,yy,dep),(min(bb,xx+.10),yy+side*.10,dep),.005,'eb gray metal')
  for j in range(11):
   t=j/10;xx=x-.86;ee_scroll(f,xx,2.93*(1-t)+1.0*t,.07,'eb iron',.08+3.15*t)
  for xx in [f.L*.12,f.L*.39]:
   f.b(xx,.78,.11,.50,.31,.09,'eb iron')
   for q in range(6):f.b(xx,.66+q*.045,.165,.44,.013,.015,'eb gray metal')
  f.b(f.L*.58,4.95,.13,.27,.16,.10,'eb white wood')
 if n in ['269','270']:
  for yy in [.36,.85,1.34,1.83,2.32,2.81,3.30]:fidelity_clipped_surface(f,0,f.L,yy,yy+.025,.095,.025,'eb charcoal stone' if n=='269' else 'eb gray stone')
 if n=='270':
  for at in [.18,.50,.82]:
   x=at*f.L;ww=1.1 if at==.5 else 1.4;top=3.6;yy=top+.12
   ee_front([f.p(x-.16,yy+.32,.16),f.p(x+.16,yy+.32,.16),f.p(x+.10,yy-.05,.16),f.p(x-.10,yy-.05,.16)],'eb white stone')
   for side in [-1,1]:f.line((x+side*.15,yy+.31,.19),(x+side*.09,yy+.02,.19),.012,'eb gray stone')
  for x in [f.L*.18,f.L*.82]:
   for side in [-1,1]:
    ee_scroll(f,x+side*.15,.80,.13,'eb iron',1.28)
   fidelity_opening(f,x,-.54,1.15,1.13,'eb iron','round',.112)
 if n=='272':
  te_fence(f,.04,f.L-.04,1.48,1.80)
  for j in range(round((f.L-.08)/.15)+1):
   xx=.04+j*(f.L-.08)/round((f.L-.08)/.15)
   ee_front([f.p(xx-.035,1.78,1.48),f.p(xx,1.91,1.48),f.p(xx+.035,1.78,1.48)],'eb iron')
  for xx in [f.L*.63,f.L*.95]:
   f.b(xx,.48,.68,.47,.62,.47,'eb white wood')
   # One pale planter with a tall stem/crown; no repeated pot bodies.
   f.line((xx,.73,.68),(xx,1.72,.68),.024,'eb oak wood')
   for j in range(16):
    angle=j*2.4;yy=1.10+(j%5)*.14;px=xx+math.cos(angle)*.22;dd=.68+math.sin(angle)*.19
    f.line((xx,yy-.13,.68),(px,yy,dd),.009,'store09 bottle green')
    p02_disc(f,px,yy,.12,.07,dd,'store09 bottle green',9)
  x=f.L*.82;ww=1.2
  for side in [-1,1]:
   xx=x+side*ww*.72;f.b(xx,1.70,.20,.30,3.04,.37,'eb gray stone')
   f.line((x+side*ww*.90,3.43,.39),(x,4.04,.39),.055,'eb charcoal stone')
   eb_lamp(f,xx,2.67,.43)
  f.b(x,3.36,.22,ww*1.84,.18,.42,'eb gray stone')
 if n=='274':te_fence(f,.03,f.L*.98,.88,1.70,True)
 if n=='276':
  # Sparse source-observed flaking patches; not randomized grunge.
  for at,yy,ww,hh in [(.10,.56,.55,.35),(.34,.91,.72,.27),(.57,.48,.43,.25)]:fidelity_clipped_surface(f,at*f.L-ww/2,at*f.L+ww/2,yy-hh/2,yy+hh/2,.06,.025,'eb gray stone')
  for x in [f.L*.12,f.L*.48]:eb_plant(f,x,-.22,.56,.35)
  # Curved outer rails and the distinct cellar entrance under the raised parlor.
  x=f.L*.81;dep=2.25
  for side in [-1,1]:
   xx=x+side*.91
   for j in range(10):
    t=j/10;u=(j+1)/10
    f.line((xx,1.0+1.50*(1-t),dep*t),(xx,1.0+1.50*(1-u),dep*u),.035,'eb green wood')
   for j in range(9):ee_scroll(f,xx,1.05+1.45*(1-j/8),.08,'eb green wood',dep*j/8)
 if n=='275':te_flat_hatch(f,f.L*.02,f.L*.28)
 if n=='273':
  for a,b in [(.05,.35),(.67,.96)]:
   ee_front([f.p(a*f.L,.18,.17),f.p(b*f.L,.18,.17),f.p(b*f.L,.18,1.05),f.p(a*f.L,.18,1.05)],'eb iron')
 if n=='284':
  for a,b in [(.02,.29),(.36,.63)]:
   x=f.L*(a+b)/2;ww=(b-a)*f.L;f.b(x,.64,.65,ww,.93,.82,'eb iron');f.b(x,1.13,.65,ww+.05,.055,.90,'eb iron')
   f.line((x,.20,1.07),(x,1.10,1.07),.012,'eb gray metal');p02_notice(f,x,1.17,ww*.34,.11,.69)
   for j in range(4):ee_scroll(f,x+(j-1.5)*ww*.16,.70,.10,'store09 paper',1.08)
  te_flat_hatch(f,f.L*.66,f.L*.82)
 if n in ['278','284']:te_fence(f,.02,f.L*.70,.65,.80)

 # Individual entry numbers replace the inherited automatic gold plate.
 main=r['doors'][0] if r['doors'] else None
 number_places={'261':(2.34,.18,'eb gray metal'), '263':(2.97,.18,'eb iron'),
  '265':(2.61,.13,'store09 paper'),'269':(2.76,.13,'store09 paper'),
  '270':(3.20,.14,'store09 paper'),'273':(2.68,.095,'eb gold metal'),
  '275':(2.91,.11,'eb gold metal'),'277':(2.95,.18,'eb gray metal'),
  '279':(2.49,.21,'store09 paper'),'266':(3.09,.13,'store09 paper'),
  '278':(2.78,.105,'eb gold metal')}
 if main and n in number_places:
  yy,hh,col=number_places[n];et_text(f,main['at']*f.L,yy,.46,hh,n,col,.025,'serif')
 if n=='264':et_text(f,f.L*.84,2.62,.26,.08,'262','eb gold metal',-.11,'serif')
 if n=='266' and main:te_grid_glass(f,main['at']*f.L,1.0,2.92,main['width']*f.L*.76,-.065,2,4,'eb white wood')
 if n in ['263','265','273','275','277','279'] and main:
  x=main['at']*f.L;ww=main['width']*f.L
  te_grid_glass(f,x,main['bottom']+.70,2.62,ww*.67,-.065,2 if n in ['275','277','279'] else 1,3 if n in ['275','277'] else 2,main['material'])
 if n=='265':
  f.strip(3.37,.18,.34,'eb white wood');f.strip(3.55,.08,.43,'eb white wood')
  for xx in [f.L*.425,f.L*.575]:
   f.b(xx,1.74,.17,.20,2.96,.28,'eb white wood')
   for dx in [-.055,0,.055]:f.line((xx+dx,.32,.32),(xx+dx,3.10,.32),.012,'eb white wood')
  f.b(.09,1.78,.16,.17,3.18,.25,'te green porthole')
 if n=='269':
  x=f.L*.5;ww=main['width']*f.L
  eb_arc(f,x,2.82,ww*.62,.63,.16,.09,'eb charcoal stone')
  for side in [-1,1]:f.b(x+side*ww*.63,1.59,.14,.15,2.45,.26,'eb charcoal stone')
  te_grid_glass(f,x,.45,2.72,ww*.80,-.07,2,4,'eb iron')
  for yy in [.90,1.44,2.05]:ee_scroll(f,x,yy,.11,'eb iron',.04)
 if n in ['256','260','269']:
  for w in r['windows']:
   if 'row' in w:continue
   x=w['at']*f.L;ww=w['width']*f.L;lo=w['bottom'];top=lo+w['height']
   if w['height']<1 or (n!='269' and lo<1):continue
   col='eb white wood' if n=='269' else 'eb iron';dep=.38
   for yy in [lo,lo+.32,top]:f.line((x-ww/2,yy,dep),(x+ww/2,yy,dep),.022,col)
   for j in range(round(ww/.13)+1):
    xx=x-ww/2+j*ww/round(ww/.13);f.line((xx,lo,dep),(xx,top,dep),.011,col)
   for xx in [x-ww/2,x+ww/2]:
    for yy in [lo,top]:f.line((xx,yy,.05),(xx,yy,dep),.018,col)
   if n=='260':
    eb_arc(f,x,top-.12,ww*.60,.30,.20,.07,'eb red wood');et_foliage(f,x-ww*.46,x+ww*.46,top+.06,'eb red wood',.28)
   if n=='269':
    for xx in [x-ww*.28,x+ww*.28]:ee_scroll(f,xx,lo+.26,.07,col,dep)
 if n=='256':
  x=main['at']*f.L;ww=main['width']*f.L
  for side in [-1,1]:
   xx=x+side*(ww*.5+.18);f.b(xx,2.94,.17,.29,3.31,.30,'te rose ashlar')
   for yy in [1.41,4.53]:f.b(xx,yy,.20,.46,.19,.43,'te rose ashlar')
   et_foliage(f,xx-.08,xx+.08,2.95,'te rose ashlar',.36)
  te_grid_glass(f,x,1.49,3.94,ww*.83,-.06,4,4,'eb iron');te_grid_glass(f,x,4.03,4.49,ww*.91,-.06,1,1,'eb iron')
 if n=='264':
  for j in range(19):
   xx=f.L*.36-1.50+j*3/18;f.line((xx,.65,.69),(xx,2.19,.69),.010,'eb gray metal')
  f.b(f.L*.36,.53,1.02,3.40,.71,.25,'eb red brick');f.b(f.L*.36,.91,1.02,3.48,.08,.30,'eb cream stone')
  te_bench(f,f.L*.36,1.34,2.55,'eb oak wood',False)
  for xx in [f.L*.69,f.L*.77]:p02_disc(f,xx,2.52,.08,.10,.15,'eb gray metal',16)
 if n=='276':
  for w in r['windows']:
   if 'row' not in w and w['bottom']>1:
    x=w['at']*f.L;ww=w['width']*f.L;yy=w['bottom']+w['height']
    for off,width in [(0,ww+.25),(.13,ww+.41)]:f.b(x,yy+off,.13,width,.13,.27,'eb brown stone')
  for xx in [f.L*.68,f.L*.94]:
   f.b(xx,3.19,.09,.19,3.29,.16,'eb white stucco')
   for j in range(6):f.b(xx,1.9+j*.48,.18,.21,.11,.025,'eb red brick')
  # Source flaking boundaries are irregular, with an estimated local silhouette.
  for xx,yy,ww,hh in [(f.L*.15,.52,.85,.65),(f.L*.40,1.10,1.05,.58),(f.L*.62,.56,.72,.58)]:
   poly=[(-.5,-.4),(-.34,.08),(-.5,.43),(-.05,.29),(.28,.5),(.50,.14),(.30,-.20),(.48,-.45),(0,-.33)]
   ee_front([f.p(xx+dx*ww,yy+dy*hh,.09) for dx,dy in poly],'eb gray stone')
  for j in range(4):f.b(f.L*.53,.12-(j+1)*.16,1.08-(j+.5)*.24,.95,.08,.24,'eb gray stone')
 if n in ['278','284']:
  x=main['at']*f.L;ww=main['width']*f.L
  f.b(x,3.17,.20,ww+.58,.25,.43,'eb cream stone');te_mask(f,x,3.29,.60,'eb cream stone')
  te_grid_glass(f,x,.26,2.66,ww*.81,-.06,2,4,'eb iron')
  for at in [.35,.57]:nb_ac(f,f.L*at,.57,.60,.32,.17)
  f.line((f.L*.1,3.46,.12),(f.L*.96,3.46,.12),.014,'eb gray metal')
  if n=='284':
   for j,ch in enumerate('284'):et_text(f,x,3.27-j*.075,.13,.065,ch,'eb gray metal',.44,'serif')
 if n=='280':
  f.strip(3.72,.31,.24,'eb iron');x=main['at']*f.L
  te_grid_glass(f,x,.85,3.01,1.08,-.05,3,5,'eb iron')
  f.b(x,3.28,-.10,1.14,.35,.03,'eb pale fabric');et_text(f,x,3.28,.53,.16,'280','eb iron',-.07,'serif')
  for side in [-1,1]:f.b(x+side*.91,.51,.65,.24,.70,1.42,'eb iron')
  for w in r['windows']:
   if w.get('row',-1)>=0:te_mask(f,w['at']*f.L,w['bottom']+w['height']+.22,1.0,'eb cream stone')
 if n=='286':
  for w in r['windows']:
   if w.get('row',-1)>=0:
    xx=w['at']*f.L;ww=w['width']*f.L;yy=w['bottom']+w['height']
    for off in [.09,.21]:eb_arc(f,xx,yy+.08,ww*.62,.22+off,.23+off*.2,.045,'eb cream stone')
    for side in [-1,1]:te_mask(f,xx+side*ww*.43,w['bottom']-.23,.65,'eb cream stone')
  te_grid_glass(f,main['at']*f.L,.80,2.72,main['width']*f.L*.75,-.06,3,4,'eb oak wood')
 # Contrasting shallow stone nosings articulate actual steps from street height.
 if entry:=s.get('access'):
  rise=entry['rise'];dep=entry['depth'];count=max(1,round(max(0,rise-.16)/.17))
  if rise>.35:
   for j in range(count):
    yy=.17+(rise-.17)*(j+1)/count;dd=dep*(count-j)/count
    f.b(entry['at']*f.L,yy+.009,dd-.025,entry['width'],.025,.10,'eb cream stone' if n in ['268','276'] else 'eb gray stone')

def te_profile_skin(f,profile,mat):
 """Cut every registered opening out of an arbitrary piecewise-linear roofline."""
 cuts=sorted({0.,f.L,*[x for x,y in profile],*[max(0.,min(f.L,x)) for o in OPENINGS[frontage_key(f)] for x in [o[0],o[2]]]})
 def roof(x,mid):
  for (a,ha),(b,hb) in zip(profile,profile[1:]):
   if a-.00001<=mid<=b+.00001 and b-a>.00001:return ha+(hb-ha)*(x-a)/(b-a)
  raise ValueError('Uncovered roof profile')
 def clip(poly,y,keep_above):
  out=[]
  for p,q in zip(poly,poly[1:]+poly[:1]):
   ip=p[1]>=y if keep_above else p[1]<=y;iq=q[1]>=y if keep_above else q[1]<=y
   if ip:out.append(p)
   if ip!=iq:
    t=(y-p[1])/(q[1]-p[1]);out.append((p[0]+t*(q[0]-p[0]),y))
  return out
 for a,b in zip(cuts,cuts[1:]):
  if b-a<.0001:continue
  mid=(a+b)/2;ha=roof(a,mid);hb=roof(b,mid);top=max(ha,hb);intervals=[(.17,top)]
  for l,bt,rr,tt in OPENINGS[frontage_key(f)]:
   if not l<mid<rr:continue
   remaining=[]
   for lo,hi in intervals:
    if tt<=lo or bt>=hi:remaining.append((lo,hi));continue
    if lo<bt:remaining.append((lo,bt))
    if tt<hi:remaining.append((tt,hi))
   intervals=remaining
  for lo,hi in intervals:
   poly=clip(clip([(a,.17),(b,.17),(b,hb),(a,ha)],lo,True),hi,False)
   if len(poly)>=3:ee_front([f.p(x,y,0) for x,y in poly],mat)

def te_gabled_piece(f,eave,ridge,depth,mat='te church brick',roof='te slate roof',close_sides=True):
 profile=[(0,eave),(f.L/2,ridge),(f.L,eave)];te_profile_skin(f,profile,mat)
 for a,b in zip(profile,profile[1:]):
  ee_front([f.p(a[0],a[1],0),f.p(b[0],b[1],0),f.p(b[0],b[1],-depth),f.p(a[0],a[1],-depth)],roof)
  f.line((a[0],a[1],.09),(b[0],b[1],.09),.10,'te church trim')
  # Roof courses run along the actual slope rather than a flat cap.
  for j in range(1,max(2,round(math.dist(a,b)/.36))):
   t=j/max(2,round(math.dist(a,b)/.36));x=a[0]+t*(b[0]-a[0]);y=a[1]+t*(b[1]-a[1])
   f.line((x,y+.018,-.08),(x,y+.018,-depth),.009,roof)
 if close_sides:
  for x in [0,f.L]:ee_front([f.p(x,.17,0),f.p(x,.17,-depth),f.p(x,eave,-depth),f.p(x,eave,0)],mat)
 ee_front([f.p(0,.17,-depth),f.p(f.L,.17,-depth),f.p(f.L,eave,-depth),f.p(f.L/2,ridge,-depth),f.p(0,eave,-depth)],mat)

def te_cross(f,x,y,d,size=.65):
 f.line((x,y-size*.5,d),(x,y+size*.8,d),.055,'te copper roof')
 f.line((x-size*.45,y+size*.35,d),(x+size*.45,y+size*.35,d),.05,'te copper roof')
 f.line((x-size*.30,y+size*.64,d),(x+size*.30,y+size*.64,d),.04,'te copper roof')
 f.line((x-size*.25,y-size*.15,d),(x+size*.25,y-size*.02,d),.04,'te copper roof')

def te_church(b,records):
 faces={}
 for idx,r in records:
  v=b['frontages'][idx];f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']);f.wall=r['wall'];faces[idx]=(f,r)
  clean=deepcopy(r);clean['observedGround']['basementAreaways']=[]
  fidelity_elevation({**b,'businesses':[],'seventhArchitecture':clean},f,clean)
  for w in r['windows']:
   if w.get('shape')=='pointed':
    xx=w['at']*f.L;ww=w['width']*f.L;yy=w['bottom'];hh=w['height']
    te_lancet(f,xx,yy,yy+hh,ww)
    for t in ([j/12 for j in range(1,12)] if idx==1 else w.get('rails',[.49])):f.line((xx-ww*.47,yy+hh*t,.025),(xx+ww*.47,yy+hh*t,.025),.022,'eb iron')
    for side in [-1,1]:te_mask(f,xx+side*(ww*.5+.22),yy+hh-min(ww*.7,hh*.38),.45,'te church trim')
    if idx in [4,5] and yy>7:
     et_foliage(f,xx-ww*.5,xx+ww*.5,yy-.40,'te church trim',.24)
  for yy in [1.9,6.35]:fidelity_clipped_surface(f,0,f.L,yy,yy+.15,.07,.15,'te church trim')
  if idx!=2:te_fence(f,.02,f.L-.02,.82,1.70,True)
  else:
   te_fence(f,.02,f.L*.27,.82,1.70,True);te_fence(f,f.L*.73,f.L-.02,.82,1.70,True)
  for j,xx in enumerate([.09,f.L-.09]):
   end=[5.8,18.4,13.6,26.5,18.1,12.2 if j==0 else 18.1][idx]
   f.line((xx,1.8,.12),(xx,end,.12),.045,'eb gray metal')
 # Low western wing, nave, recessed porch, tower and corner rectory retain
 # separate tops. Their unseen roof depths remain explicit visual estimates.
 f,r=faces[0];te_gabled_piece(f,6.0,7.8,9.0);te_cross(f,f.L*.5,8.0,.04,.35)
 f,r=faces[1];te_gabled_piece(f,18.6,23.8,16.0);te_cross(f,f.L*.5,24.0,.05,.75)
 for xx in [f.L*.43,f.L*.50,f.L*.57]:et_foliage(f,xx-.35,xx+.35,22.8-abs(xx/f.L-.5)*12,'te church trim',.18)
 for j in range(9):
  x=f.L*.25+j*f.L*.0625;y=18.6+(1-abs(x/f.L-.5)*2)*(23.8-18.6)-.62
  f.b(x,y,.15,.17,.30,.25,'te church trim')
 f,r=faces[2];te_profile_skin(f,[(0,13.8),(f.L,13.8)],r['wall'])
 ee_front([f.p(0,13.8,0),f.p(f.L,13.8,0),f.p(f.L,14.0,-10),f.p(0,14.0,-10)],'te slate roof')
 for xx in [0,f.L]:ee_front([f.p(xx,.17,0),f.p(xx,.17,-10),f.p(xx,14,-10),f.p(xx,13.8,0)],r['wall'])
 x=f.L*.5;ww=3.1;low=1.7;top=7.6
 eb_access(f,{**r,'e09Block':{**r['e10East'],'trim':'eb gray stone'}})
 # Slate shoulders below the high clerestory are visible beside the porch gable.
 for a,bb in [(0,f.L*.26),(f.L*.74,f.L)]:
  ee_front([f.p(a,6.65,.28),f.p(bb,6.65,.28),f.p(bb,9.25,-1.6),f.p(a,9.25,-1.6)],'te slate roof')
  for j in range(1,11):
   t=j/11;f.line((a,6.65+2.60*t+.015,.28-1.88*t),(bb,6.65+2.60*t+.015,.28-1.88*t),.009,'te church trim')
 for j in range(9):f.b(x,.17+(j+1)*1.53/9+.012,2.5*(9-j)/9-.025,3.2,.027,.10,'eb pale fabric')
 # Deep nested entrance moldings and six round column shafts.
 shoulder=top-min(ww*.70,(top-low)*.38)
 for j in range(6):
  off=.12+j*.105;dd=.18+j*.065
  fidelity_shaped_arc(f,x,shoulder,ww/2+off,top-shoulder+off,dd,.045,'te church trim','pointed')
  for side in [-1,1]:
   xx=x+side*(ww/2+off);f.line((xx,low,dd),(xx,shoulder,dd),.065,'te church trim')
   f.b(xx,shoulder-.08,dd,.20,.21,.23,'te church trim');te_mask(f,xx,shoulder-.08,.7,'te church trim')
 # Projecting steep porch gable; fill only masonry outside the arch.
 for side in [-1,1]:
  pts=[(x+side*2.40,7.10),(x,10.45),(x,8.48),(x+side*1.80,6.2)]
  ee_front([f.p(xx,yy,.57) for xx,yy in pts],'te church brick')
  f.line((x+side*2.40,7.10,.63),(x,10.45,.63),.11,'te church trim')
  for j in range(1,7):
   t=j/7;xx=x+side*2.40*(1-t);yy=7.10+3.35*t;te_mask(f,xx,yy+.10,.7,'te church trim')
 p02_ring(f,x,9.18,.30,.35,.66,'te church trim',.045,36);et_text(f,x,9.18,.50,.30,'IHS','te church trim',.70,'serif')
 te_cross(f,x,10.62,.58,.46)
 # Pointed transom with five unequal lancets and fine diagonal leadwork.
 for dx,hh in [(-1.20,.38),(-.72,1.20),(0,1.76),(.72,1.20),(1.20,.38)]:
  w=.58 if dx else .68;lo=5.49;hi=lo+hh
  fidelity_shaped_arc(f,x+dx,hi-w*.62,w*.5,w*.62,-.11,.035,'eb iron','pointed')
  for side in [-1,1]:f.line((x+dx+side*w*.5,lo,-.11),(x+dx+side*w*.5,hi-w*.62,-.11),.025,'eb iron')
  for j in range(round(hh/.14)):
   yy=lo+j*.14
   if yy+.2<hi-w*.62:
    for side in [-1,1]:f.line((x+dx-w*.40,yy+(.18 if side<0 else 0),-.12),(x+dx+w*.40,yy+(0 if side<0 else .18),-.12),.007,'eb gray metal')
 # Iron scrollwork is arranged in distinct upper and lower door panels.
 for side in [-1,1]:
  xx=x+side*.73
  for lo,hi in [(1.87,3.0),(4.20,5.28)]:
   shop09_frame(f,xx,(lo+hi)/2,1.29,hi-lo,-.11,'eb brown metal',.025)
   for yy in [lo+.29,hi-.29]:
    for dx in [-.29,.29]:
     ee_scroll(f,xx+dx,yy,.23,'eb iron',-.075)
     f.line((xx+dx-.12,yy-.16,-.075),(xx+dx+.12,yy+.16,-.075),.015,'eb brown metal')
  for j in range(8):f.line((xx-.61+j*.17,3.06,-.17),(xx-.61+j*.17,4.15,-.17),.010,'eb brown metal')
  gx=x+side*1.63;eb_arc(f,gx,2.28,.38,.60,2.48,.055,'eb iron')
  for xx2 in [gx-.38,gx+.38]:f.line((xx2,.17,2.48),(xx2,2.28,2.48),.036,'eb iron')
  f.line((gx,1.80,2.48),(gx,2.72,2.48),.035,'eb iron');f.line((gx-.20,2.39,2.48),(gx+.20,2.39,2.48),.035,'eb iron')
 et_text(f,x+.78,3.72,.35,.12,'288A','eb gold metal',-.075,'serif')
 f.b(x-2.72,3.95,.30,.65,.92,.09,'eb gold metal');f.b(x-2.72,3.95,.36,.53,.80,.025,'eb charcoal stone')
 et_text(f,x-2.72,4.17,.44,.065,'ST NICHOLAS','eb gold metal',.38,'serif');et_text(f,x-2.72,4.04,.44,.055,'ORTHODOX CHURCH','eb gold metal',.38,'serif')
 for j in range(4):f.b(x-2.72,3.91-j*.075,.38,.32-j*.025,.012,.012,'eb gold metal')
 f,r=faces[3];te_profile_skin(f,[(0,26.7),(f.L,26.7)],r['wall']);depth=7.6
 ee_front([f.p(f.L,.17,0),f.p(f.L,.17,-depth),f.p(f.L,26.7,-depth),f.p(f.L,26.7,0)],r['wall'])
 # East belfry return remains exposed above the lower rectory roof.
 side=Facade(f.x,f.z+depth,0,-1,depth);side.wall=r['wall']
 for yy,hh in [(18.0,2.4),(23.5,2.7)]:
  fidelity_window(side,{'at':.5,'width':1.4/depth,'bottom':yy,'height':hh,'shape':'pointed','frame':'eb brown metal','trim':'te church trim','hood':'none'})
  te_lancet(side,depth*.5,yy,yy+hh,1.4)
  for j in range(8):side.b(depth*.5,yy+.12+j*.27,-.05,1.27,.12,.13,'eb brown metal')
 te_profile_skin(side,[(0,26.7),(depth,26.7)],r['wall'])
 for yy in [22.7,26.5]:side.strip(yy,.19,.22,'te church trim')
 ee_front([f.p(0,.17,-depth),f.p(f.L,.17,-depth),f.p(f.L,26.7,-depth),f.p(0,26.7,-depth)],r['wall'])
 center=f.p(f.L*.5,30.7,-depth*.5)
 ring=[f.p(0,26.7,0),f.p(f.L,26.7,0),f.p(f.L,26.7,-depth),f.p(0,26.7,-depth)]
 for p,q in zip(ring,ring[1:]+ring[:1]):ee_front([p,q,center],'te copper roof')
 te_cross(f,f.L*.5,31.0,-depth*.5,.55)
 for yy in [6.5,12.0,16.8,22.7,26.5]:f.strip(yy,.18,.20,'te church trim')
 for xx in [.12,f.L-.12]:
  f.b(xx,10.3,.25,.36,20.2,.60,r['wall'])
  f.b(xx,20.6,.17,.36,.35,.43,'te church trim')
 for yy in [18.15,23.95]:
  for j in range(7):f.b(f.L*.5,yy+j*.23,-.04,1.03,.12,.15,'eb brown metal')
 f4,r4=faces[4];te_profile_skin(f4,[(0,18.3),(f4.L/2,22.5),(f4.L,18.3)],r4['wall'])
 # Joined cross-gable roof: one continuous surface, avoiding intersecting caps.
 # Roof heights between public views remain estimates, recorded in the mass ledger.
 width=f4.L;depth=7.10;steps=16
 def roof(u,v):return 18.3+4.2*max(1-abs(u/width-.5)*2,1-abs(v/depth-.5)*2)
 for i in range(steps):
  for j in range(steps):
   a=i*width/steps;bb=(i+1)*width/steps;c=j*depth/steps;d=(j+1)*depth/steps
   verts=[f4.p(a,roof(a,c),-c),f4.p(bb,roof(bb,c),-c),f4.p(bb,roof(bb,d),-d),f4.p(a,roof(a,d),-d)]
   ee_front(verts[:3],'te slate roof');ee_front([verts[0],verts[2],verts[3]],'te slate roof')
 # West closure only: the Avenue side is already cut by its window skin.
 for side in [width]:
  ee_front([f4.p(side,.17,0),f4.p(side,.17,-depth),f4.p(side,18.3,-depth),f4.p(side,22.5,-depth/2),f4.p(side,18.3,0)],r4['wall'])
 # Avenue: low pitched range with two projecting dormers and high rectory gable.
 f,r=faces[5];p=[(0,12.4),(.05*f.L,12.4),(.13*f.L,17.0),(.21*f.L,12.4),(.30*f.L,12.4),(.38*f.L,17.0),(.46*f.L,12.4),(.54*f.L,12.4),(.54*f.L,18.3),(.60*f.L,18.3),(.77*f.L,22.5),(f.L,18.3)]
 te_profile_skin(f,p,r['wall'])
 # Broad sloping roof supports the two observed dormers, not a vertical black cap.
 ee_front([f.p(0,12.4,0),f.p(.54*f.L,12.4,0),f.p(.54*f.L,17.0,-3.0),f.p(0,17.0,-3.0)],'te slate roof')
 ee_front([f.p(0,17.0,-3.0),f.p(.54*f.L,17.0,-3.0),f.p(.54*f.L,12.4,-6.85),f.p(0,12.4,-6.85)],'te slate roof')
 for a,peak,bb in [(.05,.13,.21),(.30,.38,.46)]:
  for u,v,hu,hv in [(a,peak,12.4,17),(peak,bb,17,12.4)]:
   ee_front([f.p(u*f.L,hu,0),f.p(v*f.L,hv,0),f.p(peak*f.L,17,-3.0)],'te slate roof')
 for (a,ha),(bb,hb) in zip(p,p[1:]):
  if bb-a>.001:f.line((a,ha,.12),(bb,hb,.12),.09,'te church trim')
 for yy in [6.5,12.0,18.1]:
  aa=0 if yy<18 else .54*f.L
  f.b((aa+f.L)/2,yy,.09,f.L-aa,.16,.17,'te church trim')
  for j in range(round((f.L-aa)/.24)):
   xx=aa+(j+.5)*(f.L-aa)/round((f.L-aa)/.24);f.b(xx,yy-.17,.12,.12,.17,.21,'te church trim')
 for w in r['windows']:
  if w['bottom']>13:
   xx=w['at']*f.L;yy=w['bottom']+w['height'];et_foliage(f,xx-.35,xx+.35,yy-.30,'te church trim',.23)
 # July 2022 Avenue view: carved circular field above the triple attic lights,
 # with a raised gable border and individual crockets. Relief is an approximation.
 cx=.80*f.L;cy=21.03
 p02_disc(f,cx,cy,.48,.49,.13,'te church trim',28)
 p02_ring(EtCarvedRelief(f),cx,cy,.50,.51,.24,'te church trim',.045,28)
 for j in range(8):
  t=j*math.tau/8
  ee_scroll(EtCarvedRelief(f),cx+math.cos(t)*.27,cy+math.sin(t)*.27,.12,'te church brick',.25)
 for a,bb,ha,hb in [(.60,.77,18.3,22.5),(.77,1.,22.5,18.3)]:
  f.line((a*f.L,ha,.24),(bb*f.L,hb,.24),.11,'te church trim')
  for j in range(1,7):
   t=j/7;xx=(a+(bb-a)*t)*f.L;yy=ha+(hb-ha)*t
   f.b(xx,yy+.15,.22,.13,.26,.23,'te church trim')

def te_club(b,records):
 mat='painted ee white brick'
 # Mapped footprint is retained; only its documented rear upper mass lowers.
 for idx,r in records:
  v=b['frontages'][idx];f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']);f.wall=mat;s=r['e10East']
  clean=deepcopy(r);clean['observedGround']['basementAreaways']=[]
  fidelity_elevation({**b,'businesses':[],'seventhArchitecture':clean},f,clean)
  if idx==1:profile=[(0,27.1),(f.L,27.1)]
  else:
   step=9.0;profile=[(0,27.1),(step,27.1),(step,22.7),(f.L,22.7)]
  te_profile_skin(f,profile,mat)
  te_architecture(f,r,27.1 if idx==1 else 22.7)
  fidelity_clipped_surface(f,0,f.L,.17,3.0,.03,.05,'te club lower paint')
  if idx==1:
   et_text(f,f.L*.83,5.75,f.L*.31,.38,'THE BOYS’ CLUB OF NEW YORK','eb gold metal',.14,'sans')
   for at in [.15,.26,.37]:
    x=at*f.L
    for j in range(6):f.b(x,6.16-j*.15,.22,2.6,.075,.45,'eb gray stone')
   for at in [.04,.25]:
    x=at*f.L;f.b(x,1.6,.04,1.03 if at==.04 else 2.22,2.8,.10,'te club blue')
    f.b(x,1.30,.11,.50,.035,.07,'eb silver metal')
    if at==.25:
     f.line((x,.24,.11),(x,3.,.11),.018,'eb iron')
     for dx in [-.13,.13]:f.b(x+dx,1.50,.15,.032,.30,.07,'eb silver metal')
     p02_notice(f,x+.35,1.98,.24,.29,.15)
   x=f.L*.65;f.b(x,4.88,.30,3.28,.23,.64,'te club blue')
   nb_grille(f,x-1.35,x+1.35,1.0,4.65,-.13)
   # Source bubble-outline graffiti is geometry; its fine lettering is uncertain.
   for j,(dx,ww,hh) in enumerate([(-1.15,.66,.66),(-.33,.56,.76),(.46,.61,.69),(1.15,.46,.56)]):
    p02_ring(f,x+dx,6.03,ww,hh,.11,'eb charcoal stone',.015,34)
    ee_scroll(f,x+dx,6.03+hh,.12,'eb charcoal stone',.12)
   for j in range(5):f.b(x,.17+(j+1)*.83/5+.012,1.7*(5-j)/5-.025,3.1,.030,.10,'eb gray metal')
   for side in [-1,1]:
    xx=x+side*1.43;col='te club blue' if side<0 else 'eb silver metal'
    f.line((xx,1.85,.18),(xx,1.05,1.65),.034,col)
    for dd in [.18,1.65]:f.line((xx,.2,dd),(xx,1.85-.80*dd/1.65,dd),.025,col)
   for xx in [x-3.4,x+3.6]:
    f.b(xx,4.72,.13,.8,.42,.09,'eb iron')
    for j in range(7):f.b(xx,4.55+j*.055,.19,.74,.020,.04,'eb gray metal')
   f.b(x+3.6,2.17,.16,.76,.75,.07,'eb charcoal stone')
   for j in range(6):f.b(x+3.6,2.42-j*.10,.21,.56,.016,.02,'eb gray metal')
   for xx in [x-5.2,x+4.6]:eb_lamp(f,xx,3.40,.22)
   for xx in [x-1.77,x+1.77]:f.b(xx,2.6,.10,.45,.55,.06,'eb gray metal')
   for w in r['windows']:
    if w.get('row')==4 and w.get('col') in [5,6,7,8]:
     xx=w['at']*f.L;ww=w['width']*f.L;top=w['bottom']+w['height']
     f.b(xx,top+.15,.42,ww+.34,.27,.95,'eb gray stone')
     for side in [-1,1]:f.b(xx+side*(ww*.5+.07),top-.26,.19,.15,.59,.40,'eb gray stone')
  else:
   et_text(f,f.L*.22,5.72,f.L*.42,.31,'THE BOYS’ CLUB OF NEW YORK','eb gold metal',.13,'sans')
   for xx in [f.L*.12,f.L*.48]:
    f.b(xx,1.7,.11,.7,.52,.12,'eb iron')
    for j in range(8):f.b(xx,1.49+j*.057,.18,.64,.022,.022,'eb gray metal')
   for j in range(14):
    x=9.1+(f.L-9.1)*j/13;f.line((x,22.7,.02),(x,25.1,.02),.018,'eb iron')
   for yy in [22.8,23.95,25.1]:f.line((9.1,yy,.02),(f.L,yy,.02),.018,'eb iron')
 # Remaining mapped edges; back parapet and two distinct flat roof surfaces.
 p=b['p']
 for a,c in zip(p,p[1:]+p[:1]):
  if abs(a[0]-202)<.2 and abs(c[0]-202)<.2:continue
  if abs(a[1]+9.24)<.10 and abs(c[1]+9.24)<.10:continue
  ha=27.1 if a[1]>-18.24 else 22.7;hc=27.1 if c[1]>-18.24 else 22.7
  ee_front([(a[0],.17,a[1]),(c[0],.17,c[1]),(c[0],hc,c[1]),(a[0],ha,a[1])],mat)
 for x0,x1,z0,z1,hh in [(165.72,202.00,-18.24,-9.24,27.1),(167.70,201.94,-30.52,-18.24,22.7)]:
  ee_front([(x0,hh,z0),(x1,hh,z0),(x1,hh,z1),(x0,hh,z1)],'roof')
 ee_front([(165.72,22.7,-18.24),(202.,22.7,-18.24),(202.,27.1,-18.24),(165.72,27.1,-18.24)],mat)

_te_previous_render=render_building
def render_building(b):
 if b['id'] not in E10_EAST_IDS:return _te_previous_render(b)
 owner(str(b['id'])+' Tenth east individually observed');h=b['firstStmarksHeight'];b['renderHeight']=h
 records=[(int(i),r) for i,r in b['firstStmarksArchitecture'].items() if r.get('e10East')]
 if b['id']==248142953:return te_church(b,records)
 if b['id']==248142975:return te_club(b,records)
 wall_mass(b,records[0][1]['wall'],False)
 for idx,r in records:
  v=b['frontages'][idx];f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']);f.wall=r['wall'];s=r['e10East']
  clean=deepcopy(r);clean['observedGround']['basementAreaways']=[]
  fidelity_elevation({**b,'businesses':[],'seventhArchitecture':clean},f,clean)
  if paint:=s.get('groundPaint'):
   top={'256':5.0,'257':6.90,'260':4.91,'266':6.95,'268':6.5,'274':3.0,'276':1.52}.get(s['number'],3.65)
   shop09_face(f,{'paintSurround':{'bottom':.17,'top':top,'material':'eb '+paint}})
  te_architecture(f,r,h)
