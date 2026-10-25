"""P01-only observed sign, shop and facade details. Loaded after the 09 kit.

Source photographs are observation references, never embedded textures. Logos,
food/menu art and fonts are authored approximations recorded in the packet.
"""
P01_IDS = {241822278,241822337,241822304,241822211}
for name,color in {
    'p01 137 red brick':(.48,.235,.18),'p01 141 orange brick':(.56,.245,.145),
    'p01 143 red brick':(.47,.205,.15),'painted p01 cobalt':(.075,.23,.47),
    'p01 rose stone':(.53,.22,.24),'p01 brown stone':(.42,.31,.20),
    'p01 dark stone':(.24,.24,.19),'p01 navy cornice':(.055,.115,.20),
    'p01 blue enamel':(.47,.60,.65),'p01 burger orange':(.98,.44,.085),'p01 bronze frame':(.27,.24,.17),
}.items():
    material(name,color,.84)
for name in ['p01 blue enamel','p01 burger orange','p01 bronze frame']:MATS[name]['storefront09Surface']=1
material('p01 blue tube',(.11,.17,.95),.35)
MATS['p01 blue tube'].node_tree.nodes.get('Principled BSDF').inputs['Emission Color'].default_value=(.12,.20,1,1)
MATS['p01 blue tube'].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=1.2
material('p01 violet tube',(.72,.22,.82),.35)
MATS['p01 violet tube'].node_tree.nodes.get('Principled BSDF').inputs['Emission Color'].default_value=(.80,.24,1,1)
MATS['p01 violet tube'].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=1.0
material('p01 green tube',(.10,.80,.25),.35)
MATS['p01 green tube'].node_tree.nodes.get('Principled BSDF').inputs['Emission Color'].default_value=(.15,1,.28,1)
MATS['p01 green tube'].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=1.0

def p01_disc(f,s,y,rx,ry,d,mat,n=28):
    points=[f.p(s+rx*math.cos(k*math.tau/n),y+ry*math.sin(k*math.tau/n),d) for k in range(n)]
    face(points,mat)
    face(list(reversed(points)),mat)

def p01_curve(f,points,d,mat,r=.012):
    for aa,bb in zip(points,points[1:]):f.line((*aa,d),(*bb,d),r,mat)

def p01_food(f,s,y,w,d,kind='burger'):
    # Legible as the observed food illustration family, not invented menu copy.
    if kind=='burger':
        p01_disc(f,s,y+.045,w*.40,w*.20,d,'store09 yellow enamel',18)
        for dy,hh,mat in [(-.012,.045,'store09 bottle green'),(-.055,.05,'store09 red enamel'),(-.095,.055,'store09 dark timber'),(-.135,.055,'store09 yellow enamel')]:
            f.b(s,y+dy,d+.010,w*.78,hh,.012,mat)
    else:
        p01_disc(f,s,y,w*.45,w*.26,d,'store09 paper',18)
        for k in range(5):
            dx=(k-2)*w*.13
            p01_disc(f,s+dx,y+(k%2)*.04,w*.07,w*.10,d+.014,'store09 orange enamel',10)

def p01_notice(f,s,y,w=.12,h=.18,d=.16):
    f.b(s,y,d,w,h,.008,'store09 paper')
    for k in range(4):f.b(s,y+h*.25-k*h*.16,d+.007,w*.70,.007,.006,'store09 gray plaster')

def p01_shop_detail(f,a,b,spec):
    kind=spec['detailP01']['kind'];w=b-a;c=(a+b)/2
    if kind=='spirals':
        # Two lamps above the fascia and three small downlights on a separate black roll housing.
        f.b(c,2.965,.27,w,.18,.25,'store09 dark iron')
        for at in [.04,.5,.96]:
            s=a+w*at
            f.b(s,2.925,.46,.085,.05,.10,'opal lamp')
        for at in [.30,.74]:
            s=a+w*at
            f.line((s,3.77,.07),(s,3.89,.39),.018,'store09 white enamel')
            f.b(s,3.87,.40,.16,.09,.12,'store09 white enamel')
        for yy in [3.055,3.715]:f.b(c,yy,.351,w,.012,.010,'store09 aged brass')
        for ss in [a+.025,b-.025]:f.b(ss,3.38,.351,.012,.66,.010,'store09 aged brass')
        # Spiral above the wordmark's i, tied to the actual sign rather than a generic font swap.
        pts=[]
        for k in range(53):
            t=k*math.tau*1.65/52;r=.007+.040*k/52
            pts.append((c-.23+math.cos(t)*r,3.68+math.sin(t)*r))
        p01_curve(f,pts,.365,'store09 aged brass',.006)
        sign_text(f,a+w*.20,2.47,w*.32,'BABE','store09 paper',.21,.09,'store09:serif')
        sign_text(f,a+w*.20,2.32,w*.32,'ORIGINAL','store09 paper',.067,.09,'store09:serif')
        sign_text(f,a+w*.43,2.44,w*.24,'Spirals','store09 paper',.15,.09,'store09:serif:1.0:0.18')
        # Dated collaboration window's small sprinkle strokes, inside this pane only.
        for k,(xx,yy) in enumerate([(.11,2.14),(.37,2.08),(.22,1.89),(.42,1.73),(.14,1.66),(.30,2.66),(.40,2.59)]):
            f.line((a+w*xx,yy,.105),(a+w*xx+.024,yy+.035,.105),.006,['store09 rose enamel','store09 yellow enamel'][k%2])
        for at in [.17,.34,.51]:
            p01_food(f,a+w*at,1.02,.17,-.28,'roll')
    elif kind=='crispy':
        # Offset name fascia leaves room for the observed chicken medallion.
        s=a+w*.09;y=3.43
        p01_disc(f,s,y,.22,.25,.34,'store09 orange enamel')
        p01_disc(f,s+.012,y-.01,.15,.18,.36,'store09 printed red')
        p01_disc(f,s+.035,y+.07,.087,.10,.38,'store09 paper')
        p01_disc(f,s+.075,y+.085,.013,.014,.397,'store09 dark iron',10)
        face([f.p(s+.103,y+.068,.398),f.p(s+.18,y+.035,.398),f.p(s+.104,y+.013,.398)],'store09 yellow enamel')
        for k in range(3):p01_disc(f,s-.035+k*.042,y+.176,.025,.033,.39,'store09 printed red',12)
        for at in [.04,.47,.96]:
            s=a+w*at
            shop09_frame(f,s,1.73,w*.072,1.42,.19,'p01 burger orange',.023)
            shop09_frame(f,s,.57,w*.072,.30,.19,'p01 burger orange',.020)
        for col in range(2):
            ss=a+w*(.61+col*.24)
            f.b(ss,.78,.075,w*.20,1.02,.018,'store09 printed red')
            for row in range(3):
                yy=.43+row*.31
                p01_food(f,ss,yy+.055,w*.14,.09,'burger' if (row+col)%2==0 else 'chicken')
                f.b(ss,yy-.08,.112,w*.12,.017,.008,'store09 paper')
        s=a+w*.64;y=2.53
        p01_curve(f,[(s+.085*math.cos(k*math.tau/24),y+.085*math.sin(k*math.tau/24)) for k in range(25)],.10,'p01 green tube',.009)
        for yy in [1.25,1.52,2.05]:p01_notice(f,a+w*.47,yy,w*.075,.18)
    elif kind=='vone':
        for at in [.15,.34,.53]:
            s=a+w*at;y=1.12
            p01_disc(f,s,y,w*.080,w*.085,.115,'store09 paper')
            # Loose finger/nail silhouettes inside observed circular service graphics.
            for k in range(4):
                x=s+(k-1.5)*w*.027
                f.line((x,y-.05,.126),(x+.015,y+.06+(k%2)*.018,.126),.017,'store09 pink plaster')
                p01_disc(f,x+.015,y+.065+(k%2)*.018,.013,.024,.15,'store09 rose enamel',10)
        for at in [.20,.47]:
            f.b(a+w*at,.48,-.37,.44,.52,.34,'store09 rose enamel')
            f.b(a+w*at,.70,-.52,.46,.38,.09,'store09 rose enamel')
        p01_notice(f,a+w*.83,1.56,w*.13,.40,.10)
    elif kind=='skwr':
        for yy in [3.44,3.47]:f.b(c,yy,.334,w*.93,.013,.008,'store09 aged brass')
        face([f.p(b-.03,3.455,.339),f.p(b-.25,3.505,.339),f.p(b-.25,3.405,.339)],'store09 aged brass')
        sign_text(f,a+w*.55,2.37,w*.34,'Open','p01 violet tube',.16,.10,'store09:script')
        sign_text(f,a+w*.20,3.135,w*.34,'139 1ST AVENUE','store09 paper',.065,.35,'store09:condensed')
        p01_notice(f,a+w*.12,1.82,w*.13,.24,.10)
    elif kind=='kikoo':
        # Hand-shaped stroke lettering, not the common shop-name font.
        logo_left=a+w*.29;unit=w*.09;y=3.52
        paths=[[(0,-.18),(0,.19)],[(.02,-.01),(.22,.20)],[(.03,-.01),(.25,-.17)],
               [(.42,-.17),(.42,.09)],[(.61,-.18),(.61,.20)],[(.63,-.01),(.84,.19)],[(.63,-.01),(.87,-.17)]]
        for p in paths:p01_curve(f,[(logo_left+xx*unit*2.8,y+yy) for xx,yy in p],.345,'store09 paper',.025)
        p01_disc(f,logo_left+.42*unit*2.8,y+.19,.036,.036,.35,'store09 paper',12)
        for at in [1.13,1.61]:
            s=logo_left+at*unit*2.8
            p01_curve(f,[(s+.13*math.cos(k*math.tau/24),y+.14*math.sin(k*math.tau/24)) for k in range(25)],.35,'store09 paper',.026)
        bowl_s=logo_left+1.13*unit*2.8
        p01_disc(f,bowl_s,y+.06,.10,.04,.38,'store09 printed red')
        for dx in [-.025,.025]:f.line((bowl_s+dx,y+.10,.38),(bowl_s+dx+.09,y+.25,.38),.010,'store09 aged brass')
        f.b(c,3.215,.346,w*.76,.16,.025,'store09 paper')
        sign_text(f,c,3.215,w*.73,'ALL YOU CAN EAT SUSHI SASHIMI','store09 printed red',.16,.368,'store09:condensed')
        for at in [.07,.25,.43,.63,.82]:f.line((a+w*at,1.46,.065),(a+w*at,2.76,.065),.010,'p01 blue tube')
        for col in range(3):
            for row in range(2):p01_food(f,a+w*(.44+col*.11),1.87+row*.27,w*.075,-.115,'sushi')
    elif kind=='paquitos':
        s=a+w*.52;y=3.73
        p01_disc(f,s,y,.25,.05,.35,'store09 yellow enamel')
        p01_disc(f,s,y+.08,.11,.12,.34,'store09 yellow enamel')
        f.b(s,y+.025,.368,.20,.032,.012,'store09 printed red')
        # Front roll shutters have distinct side tracks; no generic fabric awning.
        for edge in [a+.025,b-.025]:
            f.b(edge,1.55,.15,.055,2.75,.10,'store09 brushed steel')
        p01_notice(f,a+w*.94,1.61,w*.075,.25,.11)
    elif kind=='banshee':
        # Two-sided projecting oval with bracket, serif name and a small authored harp.
        ss=b-.16;pos=f.p(ss,0,.20)
        side=Facade(pos[0],pos[2],f.nx,f.nz,.66)
        y=4.19
        for yy in [y-.21,y+.17]:f.line((ss,yy,.02),(ss,yy,.73),.021,'store09 dark iron')
        for reverse in [False,True]:
            pos=f.p(ss,0,.86 if reverse else .20)
            side=Facade(pos[0],pos[2],-f.nx if reverse else f.nx,-f.nz if reverse else f.nz,.66)
            depth=.035
            p01_disc(side,.35,y,.30,.37,depth,'store09 black enamel')
            sign_text(side,.35,y-.07,.55,'GUINNESS','store09 paper',.09,depth+.008,'store09:serif')
            p01_curve(side,[(.22,y+.20),(.40,y+.24),(.38,y+.02),(.29,y+.02),(.22,y+.20)],depth+.014,'store09 aged brass',.012)
            for j in range(5):side.line((.25+j*.026,y+.19,depth+.016),(.29+j*.019,y+.045,depth+.016),.004,'store09 aged brass')
            side.b(.35,y-.25,depth+.010,.18,.026,.009,'store09 printed red')
        f.b(b-.02,3.19,.15,.11,.16,.16,'opal lamp')
        p01_notice(f,a+w*.08,1.43,.10,.24,.16)
        # Burgundy stripe returns on both curved cheeks, authored separately.
        for edge in [a,b]:
            for k in range(8):
                t=(k+.5)/8*math.pi/2;yy=3.79-.73*(1-math.cos(t));dd=.10+1.16*math.sin(t)
                f.line((edge,yy-.02,.10),(edge,yy-.02,dd),.007,'store09 cream canvas')

_p01_previous_shop=photographed_shop
_p01_previous_arch=shop09_arch
_p01_open_door=None
def shop09_arch(f,left,right,bottom,top,d,mat,surround,round_top=False):
    # Only the source-observed open Crispy entrance skips its closed glass plane.
    if _p01_open_door is not None and left<_p01_open_door and mat=='store09 clear glass':return
    return _p01_previous_arch(f,left,right,bottom,top,d,mat,surround,round_top)

def photographed_shop(f,a,b,r):
    global _p01_open_door
    spec=r['design'];p01=spec.get('detailP01')
    if not p01:return _p01_previous_shop(f,a,b,r)
    kind=p01['kind'];w=b-a;detail=spec['detail09']
    # P01 boards have observed paper/menu families instead of generic chalk lines.
    copy=__import__('copy').deepcopy(r);copy['design']['boards']=[]
    _p01_open_door=(a+w*.43) if kind=='crispy' else None
    if kind=='crispy':
        copy['design']['panels'][0][0]='glass'
        copy['design']['base']=.17
    _p01_previous_shop(f,a,b,copy)
    _p01_open_door=None
    for edge in [a+.045,b-.045]:
        f.b(edge,1.61,-.46,.035,2.88,.91,'store09 dark timber')
    for board in spec.get('boards',[]):
        ss=a+w*board['at'];dd=board.get('depth',1);hh=board['height'];ww=board['width']
        paper='store09 paper' if kind=='vone' else 'store09 printed blue' if kind=='paquitos' else 'store09 chalkboard'
        display_board(f,ss,dd,'',board['frame'],paper=paper,height=hh,width=ww)
        # Explicit menu columns preserve density without inventing illegible wording.
        f.b(ss,hh*.56+.18,dd+.108,ww*.88,hh*.75,.012,paper)
        ink='store09 rose enamel' if kind=='vone' else 'store09 paper'
        for row in range(9):
            y=.24+row*hh*.065
            f.b(ss-ww*.07,y,dd+.118,ww*.56,.008,.008,ink)
            f.b(ss+ww*.30,y,dd+.118,ww*.10,.008,.008,ink)
    if kind=='crispy':
        # Open glass leaf turns inward from its left hinge; pull stays attached.
        origin=f.p(a+.20,0,-.12);angle=math.radians(52)
        leaf=Facade(origin[0],origin[2],f.rx*math.cos(angle)-f.nx*math.sin(angle),f.rz*math.cos(angle)-f.nz*math.sin(angle),w*.37)
        ww=w*.37
        shop09_arch(leaf,.025,ww-.025,.22,2.79,0,'store09 clear glass','store09 brushed steel')
        shop09_frame(leaf,ww/2,1.50,ww,2.60,.03,'store09 brushed steel',.028)
        for y in [1.14,1.50]:leaf.line((ww-.13,y,.035),(ww-.13,y,.13),.010,'store09 brushed steel')
        leaf.line((ww-.13,1.14,.13),(ww-.13,1.50,.13),.016,'store09 brushed steel')
    p01_shop_detail(f,a,b,spec)

_p01_previous_render=render_building
def render_building(b):
    _p01_previous_render(b)
    if b['id'] not in P01_IDS:return
    r=b['firstStmarksArchitecture']['0'];v=b['frontages'][0]
    f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length'])
    # Registered openings leave the distinct ground surrounds and piers intact.
    shop09_face(f,{'paintSurround':{'bottom':.17,'top':3.62,'material':'store09 black enamel'}})
    if b['id']==241822337:
        for at in [.015,.985]:f.b(f.L*at,9.36,.065,.10,11.75,.10,'seventh pale limestone')
        f.strip(14.45,.12,.09,'seventh pale limestone')
    if b['id']==241822304:
        s=f.L*.105
        p01_disc(f,s,2.78,.12,.14,.02,'store09 black enamel')
        p01_disc(f,s,2.76,.075,.085,.035,'opal lamp')
    for idx,d in enumerate(r['doors']):
        s=d['at']*f.L;left=s-d['width']*f.L/2
        f.b(left-.10,1.40,.14,.10,.23,.045,'store09 brushed steel')
        for j in range(4):f.b(left-.10,1.34+j*.032,.167,.048,.010,.006,'store09 dark iron')
        if b['id'] in [241822278,241822337]:
            for k in range(11):f.b(s+(k-5)*d['width']*f.L/11,3.09,.08,.020,.24,.040,'store09 dark iron')
        f.b(s,.18,.20,d['width']*f.L+.16,.06,.42,'store09 gray plaster')
    # Observed upper blinds, AC support brackets and thin surface cables.
    # Explicit visible blind groups on 137; depths/drops estimated from the front views.
    blind_drops={0:.58,1:.74,2:.62,5:.53,6:.47,10:.20,11:.46} if b['id']==241822278 else {}
    for i,fraction in blind_drops.items():
        win=r['windows'][i]
        s=f.L*win['at'];ww=f.L*win['width'];high=win['bottom']+win['height']
        drop=fraction*win['height']
        for j in range(max(1,int(drop/.065))):f.b(s,high-.06-j*.065,-.105,ww-.11,.026,.012,'store09 cream canvas')
    if b['id']==241822278:
        f.line((f.L*.965,3.80,.06),(f.L*.965,12.1,.06),.010,'store09 brushed steel')
    if b['id']==241822211:
        # Extra stepped hood relief is visible on 143, unlike the curved 141 hoods.
        for win in r['windows']:
            s=f.L*win['at'];ww=f.L*win['width'];y=win['bottom']+win['height']
            for dy,width,dd in [(.09,ww+.21,.21),(.27,ww+.32,.20),(.33,ww+.37,.25)]:f.b(s,y+dy,dd,width,.065,.14,'p01 dark stone')
