"""Individual First & Seventh elevations and retail interiors visible from outside.

Executed by build_neighborhood.py. The five building records in
first-and-seventh.json replace the shared tenement recipe at this intersection.
Photographs are observation only; geometry, wear, lettering and plants are
authored here. All dimensions are estimates unless the source record says more.
"""
CORNER_SOURCE = json.loads((ROOT/'model-source/first-and-seventh.json').read_text())
CORNER_BUILDINGS = {v['id']: v for v in CORNER_SOURCE['buildings']}

for name,surface,tint in [
    ('seventh red brick','red_brick_03',(.98,.82,.70)),
    ('seventh buff brick','white_bricks',(.89,.79,.62)),
]:
    material(name,tint,.87,texture=surface+'_diff_1k.jpg',normal=surface+'_nor_gl_1k.jpg')
    WALL_MATERIALS[name]=(surface,tint)
# Saifee has clean buff running-bond brick, not the heavily plastered
# white_bricks surface used for some distant buildings. Joints are geometry.
material('seventh buff brick',(.68,.62,.49),.90)
WALL_MATERIALS.pop('seventh buff brick',None)
material('seventh mortar',(.43,.415,.36),.96)
material('seventh tile paint',(.60,.052,.016),.88,normal='concrete_wall_006_nor_gl_1k.jpg')
material('seventh red plaster',(.40,.115,.069),.90,normal='red_brick_03_nor_gl_1k.jpg')
material('seventh dark stone',(.14,.105,.082),.85,normal='concrete_wall_006_nor_gl_1k.jpg')
material('seventh blue canvas',(.009,.18,.49),.91)
material('seventh tile olive',(.31,.39,.19),.33)
material('seventh tile plum',(.21,.125,.15),.37)
material('seventh red enamel',(.66,.027,.014),.45)
material('seventh leaf light',(.18,.32,.039),.83)
material('seventh leaf dark',(.035,.14,.024),.87)
material('seventh green light',(.035,.73,.08),.3,emission=1.6)
material('seventh glass',(.73,.81,.84),.095,.70)
MATS['seventh glass'].node_tree.nodes.get('Principled BSDF').inputs['Alpha'].default_value=.23
MATS['seventh glass'].surface_render_method='DITHERED'


def ctext(f,s,y,w,text,mat='sign white',size=.22,d=.12,style='plain'):
    sign_text(f,s,y,w,text,mat,size,d,'block' if style=='plain' else style)


def wear(f,a,b,low,high,mat='sill patina',count=28,depth=.009,seed=0):
    """Small paint losses, not a fabricated readable graffiti tag."""
    rng=random.Random(DETAIL_SEED+seed+int(a*413))
    openings=OPENINGS[frontage_key(f)]
    for i in range(count):
        s=rng.uniform(a,b);y=rng.uniform(low,high)
        w=rng.uniform(.016,.070);h=rng.uniform(.007,.035)
        if any(l-w<s<r+w and bt-h<y<top+h for l,bt,r,top in openings):continue
        face([f.p(s-w,y,depth),f.p(s-w*.44,y+h,depth),f.p(s+w,y+h*.35,depth),
              f.p(s+w*.4,y-h,depth),f.p(s-w*.55,y-h*.48,depth)],mat)


def framed_notice(f,s,y,w,h,title='',paper='poster paper',ink='black iron',d=.13):
    f.b(s,y,d-.012,w+.023,h+.023,.017,'window frame')
    f.b(s,y,d,w,h,.008,paper)
    if title:ctext(f,s,y+h*.29,w*.90,title,ink,min(.10,h*.24),d+.007)
    for j in range(5):f.b(s,y+h*.07-j*h*.105,d+.007,w*(.68 if j%3 else .48),.008,.004,ink)


def ac_unit(f,s,y,w=.72,d=.37):
    f.b(s,y,d,w,.45,.60,'air conditioner')
    f.b(s-w*.27,y,d+.313,w*.29,.35,.018,'window frame')
    for i in range(9):f.b(s+w*.08,y-.172+i*.042,d+.314,w*.56,.013,.014,'metal')
    for dx in [-w*.37,w*.37]:
        f.line((s+dx,y-.33,.02),(s+dx,y-.23,d+.27),.015,'metal')
        f.line((s+dx,y-.23,.02),(s+dx,y-.23,d+.27),.015,'metal')
    for dx in [-w*.44,w*.44]:
        for yy in [y-.17,y+.17]:f.b(s+dx,yy,d+.319,.015,.015,.012,'metal')


def grille(f,s,bottom,w,h,depth=.07):
    for yy in [bottom+.03,bottom+h-.02]:f.b(s,yy,depth,w,.027,.045,'black iron')
    for dx in [-w*.47,-w*.23,0,w*.23,w*.47]:
        f.line((s+dx,bottom,depth),(s+dx,bottom+h,depth),.010,'black iron')
    for side in [-1,1]:
        for cy in [bottom+h*.31,bottom+h*.73]:
            for j in range(18):
                a=j*math.tau/18;b=(j+1)*math.tau/18
                f.line((s+side*w*.23+math.cos(a)*w*.15,cy+math.sin(a)*h*.17,depth+.012),
                       (s+side*w*.23+math.cos(b)*w*.15,cy+math.sin(b)*h*.17,depth+.012),.007,'black iron')


def cwindow(f,s,y,w,h,spec,row,col):
    """Thin sash/reveals and the actual lintel type, without generic stone boxes."""
    trim=spec['trim'];key=frontage_key(f)
    OPENINGS[key].append((s-w/2,y,s+w/2,y+h))
    f.b(s,y+h/2,-.36,w,h,.025,'recess shadow')
    for dx in [-w/2,w/2]:f.b(s+dx,y+h/2,-.14,.085,h+.10,.32,trim)
    f.b(s,y+h/2,-.20,w-.10,h-.10,.015,'window glass')
    for dx in [-w/2+.035,w/2-.035]:f.b(s+dx,y+h/2,-.04,.045,h,.075,'window frame')
    for yy in [y+.026,y+h*.48,y+h-.025]:f.b(s,yy,-.02,w,.055,.09,'window frame')
    f.b(s,y+h*.49+.012,.035,w-.08,.025,.07,'window frame')
    # Small latch, weather seals and a projecting sill with an underside drip.
    f.b(s,y+h*.48+.036,.042,.072,.026,.030,'metal')
    f.b(s,y-.062,.057,w+.20,.103,.29,trim)
    f.b(s,y-.125,.115,w+.10,.018,.053,'sill patina')
    kind=spec.get('lintel','stone')
    if kind=='tapered':
        face([f.p(s-w*.66,y+h+.25,.105),f.p(s+w*.66,y+h+.25,.105),
              f.p(s+w*.55,y+h+.04,.105),f.p(s-w*.55,y+h+.04,.105)],trim)
        f.b(s,y+h+.15,.055,w*1.12,.17,.10,trim)
    elif kind=='brick':
        for j in range(10):f.b(s-w*.54+j*w*.12,y+h+.12,.016,w*.108,.21,.068,trim)
    else:f.b(s,y+h+.092,.068,w+.23,.13,.23,trim)
    if spec.get('ornament')=='hood':
        f.b(s,y+h+.207,.105,w+.34,.065,.31,trim)
        for dx in [-w*.40,w*.40]:f.b(s+dx,y-.17,.05,.12,.15,.17,trim)
    pattern=(row*7+col*3+DETAIL_SEED)%9
    if pattern in [0,1,2,4,6,8]:
        length=h*([.18,.39,.59][pattern%3])
        for j in range(max(2,int(length/.075))):f.b(s,y+h-.075-j*.075,-.14,w-.14,.052,.010,'curtain' if pattern%2 else 'curtain light')
        f.line((s+w*.33,y+h-.05,-.115),(s+w*.33,y+h-length-.18,-.115),.003,'curtain light')
    elif pattern in [3,5]:
        for side in [-1,1]:
            for j in range(5):f.b(s+side*(w*.39-j*.033),y+h/2,-.14+(j%2)*.01,.030,h-.13,.02,'curtain light')
    if spec.get('grilles'):grille(f,s,y+.03,w-.07,h*.45,.058)
    if [row,col] in spec.get('ac',[]):ac_unit(f,s,y+.23,w*.74,.34)
    # Mineral staining confined to narrow strips below real sills.
    for dx in [-w*.31,w*.36]:
        f.b(s+dx,y-.22,.006,.028,.20,.006,'sill patina')


def buff_brickwork(f,low,high):
    openings=OPENINGS[frontage_key(f)];step=.073;width=.225
    def spans(y):
        cursor=0
        for a,b in sorted((max(0,l),min(f.L,r)) for l,bt,r,top in openings if bt-.012<y<top+.012)+[(f.L,f.L)]:
            if a>cursor:yield cursor,a
            cursor=max(cursor,b)
    for row in range(int((high-low)/step)+1):
        y=low+row*step
        for a,b in spans(y):f.b((a+b)/2,y,.010,b-a,.006,.008,'seventh mortar')
        offset=(row%2)*width/2
        for j in range(int(f.L/width)+1):
            ss=j*width+offset
            if 0<ss<f.L and not any(l-.012<ss<r+.012 and bt-step<y<top for l,bt,r,top in openings):
                f.b(ss,y+step/2,.010,.006,step,.008,'seventh mortar')


def cornice_corner(f,h,kind):
    if kind=='stepped-red-cornice':
        for yy,hh,dd in [(h-.31,.24,.15),(h-.13,.08,.25),(h+.035,.11,.36)]:f.strip(yy,hh,dd,'cornice copper brown')
    elif kind=='bracketed-cornice':
        for yy,hh,dd in [(h-.46,.18,.18),(h-.20,.12,.35),(h+.04,.16,.53),(h+.18,.07,.58)]:f.strip(yy,hh,dd,'black iron')
        for i in range(max(2,round(f.L/1.2))):
            s=(i+.5)*f.L/max(2,round(f.L/1.2))
            for yy,ww,dd in [(h-.44,.12,.19),(h-.33,.14,.29),(h-.18,.19,.41)]:f.b(s,yy,dd/2,ww,.17,dd,'black iron')
    else:
        f.strip(h+.025,.09,.18,'seventh dark stone' if kind=='plain' else 'sill patina')
        f.strip(h-.075,.085,.12,getattr(f,'wall','seventh red brick'))


def conduit(f,s,low,high,mat='metal',d=.09):
    f.line((s,low,d),(s,high,d),.017,mat)
    for y in [low+.3,low+1.8,high-.25]:f.b(s,y,d-.007,.072,.045,.08,mat)


def threshold(f,a,b,depth=.37,mat='sill patina'):
    f.b((a+b)/2,.205,depth/2,b-a,.067,depth,mat)
    for j in range(max(2,round((b-a)/.19))):f.b(a+.09+j*.18,.242,depth/2,.005,.005,depth-.04,'metal')


def glass_opening(f,a,b,low,high,frame='black iron',door=False,d=-.06,base='black iron',panes=1):
    s=(a+b)/2;w=b-a
    for edge in [a,b]:f.b(edge,(high+.18)/2,d+.025,.057,high-.18,.105,frame)
    for yy in [low,high]:f.b(s,yy,d+.02,w,.055,.095,frame)
    face([f.p(a+.03,low+.03,d),f.p(b-.03,low+.03,d),f.p(b-.03,high-.03,d),f.p(a+.03,high-.03,d)],'seventh glass')
    for j in range(1,panes):f.b(a+w*j/panes,(high+low)/2,d+.025,.034,high-low,.085,frame)
    if low>.22:f.b(s,(low+.18)/2,d+.04,w,low-.18,.13,base)
    if door:
        f.b(s,.31,d+.049,w-.03,.22,.035,'metal' if frame=='white frame' else base)
        pull=b-.13
        f.line((pull,1.04,d+.13),(pull,1.39,d+.13),.012,'metal')
        for yy in [1.04,1.39]:f.line((pull,yy,d+.045),(pull,yy,d+.13),.012,'metal')
        for yy in [.64,1.79,2.30]:f.b(a+.02,yy,d+.07,.021,.084,.024,'metal')
        f.b(s,high-.12,d+.08,.30,.054,.05,'metal')
        f.line((s+.07,high-.09,d+.09),(s+.27,high-.17,d+.12),.009,'metal')
        threshold(f,a,b,.32)


def shop_room(f,a,b,top,style):
    """Shallow observed display zone; no invented traversable full interior."""
    w=b-a;c=(a+b)/2;depth=2.6 if style in ['smoke','deli','saifee'] else 2.0
    f.b(c,1.62,-depth,w,2.90,.04,'interior plaster' if style in ['hen','burger','saifee','smoke','deli'] else 'interior oak')
    f.b(c,.17,-depth/2,w,.04,depth,'interior tile')
    f.b(c,top-.25,-depth/2,w,.055,depth,'interior plaster')
    # The two street-facing rooms share their corner: an opaque side at the
    # frontage endpoint otherwise hides the perpendicular recessed door.
    for ss in [a,b]:
        if .20<ss<f.L-.20:f.b(ss,1.63,-depth/2,.05,2.9,depth,'interior plaster')
    for dd in [-.66,-1.66]:
        f.b(c,top-.29,dd,w*.68,.033,.09,'white frame')
        f.b(c,top-.313,dd,w*.65,.010,.065,'lit sign white')
    if style in ['smoke','deli']:
        stock_shelves(f,a+.12,b-.12,-.43,.30,2.38,'bottle' if style=='smoke' else 'mixed')
    elif style=='saifee':
        stock_shelves(f,a+.12,b-.12,-.70,.33,2.45,'pots')
    elif style=='hen':
        f.b(c,1.05,-1.3,w*.83,.86,.55,'interior oak')
        f.b(c,1.51,-1.3,w*.86,.075,.63,'cream stone')
        for ss in [a+w*.26,a+w*.58,a+w*.86]:
            f.b(ss,2.08,-1.97,w*.20,.66,.04,'wood')
            f.b(ss,2.08,-1.94,w*.18,.59,.02,'poster paper')
            for k in range(7):f.b(ss,2.28-k*.071,-1.925,w*.12,.009,.006,'seventh dark stone')
        # Dark speckled tile seen through the doorway in the sign photograph.
        for row in range(14):
            for col in range(max(1,int(w/.16))):
                if (row*7+col*3)%5==0:f.b(a+.1+col*.16,.35+row*.16,-depth+.025,.028,.019,.007,'nishaan blue')
    elif style=='burger':
        f.b(c,1.14,-1.50,w*.85,.77,.48,'white frame')
        f.b(c,1.56,-1.50,w*.87,.075,.53,'metal')
        for ss in [a+w*.28,a+w*.72]:
            f.line((ss,top-.33,-.83),(ss,2.49,-.83),.009,'black iron')
            rod(f.p(ss,2.35,-.83),f.p(ss,2.51,-.83),.21,'sign white',20,r2=.07)
        f.b(c,2.16,-depth+.10,.22,.22,.10,'air conditioner')


def stock_shelves(f,a,b,d,low,high,kind='mixed'):
    rng=random.Random(DETAIL_SEED+int(a*153));w=b-a;levels=5
    palette=['theater red','wood','nishaan blue','sign white','yellow paint','store teal']
    for i in range(levels):
        y=low+i*(high-low)/(levels-1)
        f.b((a+b)/2,y,d,w,.038,.25,'metal')
        f.b((a+b)/2,y-.025,d+.137,w,.048,.018,'white frame')
        count=max(3,int(w/(.16 if kind!='pots' else .23)))
        for j in range(count):
            s=a+(j+.52)*w/count
            h=rng.uniform(.13,.26);mat=palette[(j//3+i*2)%len(palette)]
            if kind=='pots':
                rod(f.p(s,y+.035,d),f.p(s,y+.16,d),.067,mat,10,r2=.083)
                rod(f.p(s,y+.161,d),f.p(s,y+.168,d),.068,'recess shadow',10)
            elif (j+i)%3 and kind!='mixed':
                rod(f.p(s,y+.03,d),f.p(s,y+h,d),.034,mat,8)
                rod(f.p(s,y+h,d),f.p(s,y+h+.055,d),.016,mat,8)
                f.b(s,y+h*.53,d+.034,.059,h*.34,.006,'poster paper')
            else:
                f.b(s,y+h/2+.025,d,.095,h,.105,mat)
                f.b(s,y+h*.60,d+.056,.072,h*.36,.007,'poster paper')
                f.b(s,y+h*.57,d+.061,.050,.018,.004,mat)
            if j%3==0:f.b(s,y-.024,d+.15,.055,.024,.005,'poster paper')


def food_decal(f,s,y,w=.42,h=.50,d=.09):
    f.b(s,y,d,w,h,.008,'poster paper')
    # Geometric food illustrations establish the observed decal density. Their
    # artwork/wording is an approximation, explicitly recorded in the source.
    for dx,yy,scale in [(-.18,.10,.33),(.19,-.05,.32)]:
        sign_panel(f,s+dx*w,y+yy*h,w*scale,h*.27,d+.012,'yellow paint','oval')
        f.b(s+dx*w,y+yy*h,d+.068,w*scale*.85,h*.039,.006,'store teal')
        f.b(s+dx*w,y+yy*h-.027,d+.071,w*scale*.84,h*.037,.006,'theater red')
    for j in range(2):f.b(s,y-h*.30-j*.033,d+.013,w*.75,.008,.007,'black iron')


def leaf(f,s,y,d,length,width,angle,mat):
    ds=math.sin(angle)*length;dy=math.cos(angle)*length
    pts=[f.p(s,y,d),f.p(s+ds*.44-width*.46,y+dy*.44,d+.025),
         f.p(s+ds*.58,y+dy*.58,d+.062),f.p(s+ds,y+dy,d),
         f.p(s+ds*.44+width*.46,y+dy*.44,d+.025)]
    for tri in [(0,1,2),(1,3,2),(2,3,4),(0,2,4)]:
        face([pts[i] for i in tri],mat);face([pts[i] for i in reversed(tri)],mat)


def pot_plant(f,s,y,d,r=.15,height=.57,seed=0,hang=False):
    rng=random.Random(DETAIL_SEED+seed+int(s*473+d*47))
    ph=r*1.35
    rod(f.p(s,y,d),f.p(s,y+ph,d),r*.75,'wood' if hang else 'red terra cotta',14,r2=r)
    rod(f.p(s,y+ph*.85,d),f.p(s,y+ph,d),r*1.065,'wood' if hang else 'red terra cotta',14)
    rod(f.p(s,y+ph+.003,d),f.p(s,y+ph+.008,d),r*.91,'recess shadow',14)
    if hang:
        for dx in [-r*.88,r*.88]:f.line((s+dx,y+ph,d),(s,y+ph+.40,d),.008,'black iron')
        f.line((s,y+ph+.40,d),(s,y+ph+.55,d),.007,'black iron')
    for branch in range(7 if height>.6 else 5):
        a=rng.uniform(-1.5,1.5);size=height*rng.uniform(.5,1)
        if hang:
            ex=s+math.sin(a)*r*2;ey=y-size
        else:ex=s+math.sin(a)*r*1.7;ey=y+ph+size*.7
        dd=d+rng.uniform(-r,r)
        f.line((s,y+ph,d),(ex,ey,dd),.004,'seventh leaf dark')
        for j in range(3 if height<.4 else 7):
            t=(j+1)/(4 if height<.4 else 8);ss=s+(ex-s)*t;yy=y+ph+(ey-y-ph)*t
            for side in [-1,1]:leaf(f,ss,yy,dd,.09+height*.11,r*.58,side*(1.0+j*.17)+(math.pi if hang else 0),'seventh leaf light' if (j+branch)%3 else 'seventh leaf dark')


def plant_rack(f,s,d,w=1.3,height=1.78,seed=0):
    for dx in [-w/2,w/2]:
        for dd in [d-.22,d+.22]:
            f.b(s+dx,height/2+.23,dd,.032,height,.034,'metal')
            rod(f.p(s+dx-.04,.235,dd),f.p(s+dx+.04,.235,dd),.071,'black iron',12)
    for row in range(6):
        y=.37+row*(height-.15)/5
        f.b(s,y,d,w+.045,.036,.51,'nishaan blue' if row in [0,5] else 'metal')
        for j in range(6):
            ss=s-w*.41+j*w*.164
            pot_plant(f,ss,y+.03,d,.062,.20+(row+j)%3*.035,seed+row*7+j)
    for y in [.52,1.44]:framed_notice(f,s+w*.3,y,.11,.09,'',d=d+.263)


def fascia(f,a,b,title,style):
    c=(a+b)/2;w=b-a
    if style=='smoke':
        f.b(c,3.36,.50,w+.14,.62,.18,'sign white')
        f.b(c,2.96,.51,w+.14,.18,.21,'seventh red enamel')
        ctext(f,c,3.38,w-.10,title,'black iron',.34,.615)
        ctext(f,c,3.40,w-.10,title,'seventh red enamel',.34,.638)
        ctext(f,c,2.97,w-.13,'BEER · BEVERAGE · LOTTO · VAPE · CIGAR · SNACK · GROCERY','sign white',.12,.63)
        f.b(c,2.84,.25,w,.07,.85,'sign white')
        for j in range(max(1,int(w/.15))):f.b(a+j*.15,2.792,.25,.012,.012,.79,'metal')
    elif style=='deli':
        for row in range(7):f.b(c,3.03+row*.119,.15,w,.095,.23,'black iron')
        ctext(f,a+w*.095,3.40,w*.19,'E','seventh red enamel',.42,.285)
        ctext(f,a+w*.14,3.28,w*.17,'7','seventh green light',.38,.297)
        ctext(f,a+w*.105,3.10,w*.20,'east seven','sign white',.067,.285)
        ctext(f,a+w*.605,3.43,w*.76,title,'sign white',.41,.285)
        f.b(c,2.94,.29,w,.31,.58,'black iron')
        ctext(f,c,2.97,w*.94,'SALAD BAR   JUICE BAR   ORGANIC   NATURAL   24 HRS. GRILL','sign white',.085,.593)
    elif style=='hen':
        f.b(c,3.31,.15,w,.51,.19,'black iron')
        ctext(f,c,3.33,w*.94,'Hen House NYC','neon orange',.52,.265,'script')
        projecting_sign(f,a,b,{'at':.96,'y':3.35,'width':.66,'height':.66,'shape':'oval','material':'painted blue','lines':[{'text':'HEN HOUSE','size':.13},{'text':'NYC','size':.12,'y':-.24}]})
    elif style=='burger':
        f.b(c,3.29,.14,w+.12,.63,.26,'black iron')
        f.b(c,2.93,.32,w,.06,.12,'shop burgundy')
        for ss in [a+.12,b-.12]:
            f.line((ss,3.38,.07),(ss,3.00,.76),.012,'black iron')
            f.line((ss,3.0,.76),(ss,2.97,.10),.012,'black iron')
        f.b(c,2.98,.18,w-.12,.065,.19,'white frame')
        f.b(c,2.934,.22,w-.27,.020,.044,'lit sign white')
    else:f.b(c,3.30,.10,w,.44,.16,'black iron')


def shop_front(f,a,b,design):
    style=design['cornerStyle'];w=b-a;c=(a+b)/2
    top=design.get('top',3.7);frame=design.get('frame','black iron')
    OPENINGS[frontage_key(f)].append((a,.17,b,top))
    shop_room(f,a,b,top,style)
    for ss in [a+.035,b-.035]:f.b(ss,1.76,.035,.105,3.17,.25,frame)
    cursor=a+.085;available=w-.17
    panels=design['panels'];positions=[]
    for kind,fraction in panels:
        end=cursor+available*fraction
        low=.26 if kind=='door' else design.get('base',.48)
        d=-.24 if kind=='door' else .035
        glass_opening(f,cursor,end,low,design.get('head',2.74),frame,kind=='door',d,frame)
        positions.append((kind,cursor,end,d));cursor=end
    f.b(c,2.81,.025,w,.085,.14,frame)
    fascia(f,a,b,'DELI & CAFE' if style=='deli' else 'E SMOKE & CONVENIENCE',style)
    if style=='deli':
        # Shop door sits back inside the striped/chevron reveal.
        da,db=positions[-1][1:3]
        for side in [da+.065,db-.065]:
            for j in range(11):f.b(side,.33+j*.222,-.12,.085,.105,.29,'sign white')
        for j in range(5):food_decal(f,a+w*(.10+j*.103),1.06+(j%2)*.40,.29,.39,.082)
        framed_notice(f,db-.20,1.61,.20,.30,'A','sign white','nishaan blue',-.17)
        ctext(f,db-.24,2.88,.53,'118','sign white',.13,.597)
        display_board(f,a+w*.24,.96,'PLANT BASED','black iron','black iron',.99,.55)
    elif style=='hen':
        # Light transom, door header/address, menu easel, camera and sign conduit.
        f.b(c,2.99,-.12,w-.20,.27,.023,'seventh glass')
        ctext(f,b-.57,2.99,1.02,'120 1ST AVE','black iron',.105,-.09)
        framed_notice(f,b-.26,1.64,.25,.34,'A','sign white','nishaan blue',-.17)
        for j in range(2):framed_notice(f,a+w*(.20+j*.23),1.47,.41,.62,'MENU',d=.084)
        ac_unit(f,a+.24,3.82,.40,.19)
        f.b(b-.11,2.98,.29,.12,.17,.18,'white frame')
        conduit(f,b-.085,2.2,3.6,'black iron',.10)
    elif style=='monkey':
        # June 2025 still shows Unique's small window notice and grey fish noren;
        # a new giant Monkey fascia is not supported by this photograph.
        for ss in [a+w*.18,b-w*.15]:
            f.line((ss,3.50,.11),(ss,3.14,.35),.009,'metal')
            rod(f.p(ss,2.85,.35),f.p(ss,3.19,.35),.10,'brass',16)
            for j in range(9):f.b(ss-.07+j*.017,3.02,.443,.005,.28,.007,'black iron')
        for j in range(3):
            ss=a+w*(.22+j*.27)
            f.b(ss,2.90,.14,w*.265,.73,.013,'curtain shadow')
            for k in range(7):f.b(ss-w*.11+k*w*.032,2.90,.15,w*.018,.72,.005,'curtain')
            sign_panel(f,ss,2.78,w*.14,.17,.16,'nishaan blue','oval')
            face([f.p(ss+w*.06,2.79,.221),f.p(ss+w*.14,2.91,.221),f.p(ss+w*.13,2.66,.221)],'nishaan blue')
            f.b(ss-w*.034,2.82,.225,.019,.018,.006,'sign white')
        for j in range(23):f.b(a+w*.72,1.02+j*.061,-.06,w*.43,.047,.009,'interior oak')
        framed_notice(f,a+w*.52,1.47,.29,.46,'UNIQUE','black iron','sign white',.087)
        framed_notice(f,a+w*.50,1.15,.24,.13,'SUSHI','yellow paint','black iron',.09)
        ctext(f,a+w*.16,2.80,w*.24,'120','sign white',.16,-.08)
        f.b(a+w*.72,.98,-.25,w*.41,.04,.30,'interior oak')
        for ss in [a+w*.56,b-w*.12]:f.b(ss,.59,-.29,.048,.75,.052,'interior oak')
    elif style=='smoke':
        for i in range(4):framed_notice(f,a+w*.14+i*.24,1.29,.16,.23,'',d=.079)
        framed_notice(f,a+.25,2.39,.32,.40,'A','sign white','nishaan blue',.08)
        ctext(f,b-.42,2.29,.58,'OPEN','seventh green light',.19,-.13,'outline')
        for yy in [.45,.99]:f.line((b-.17,yy,.47),(b-.17,yy,1.03),.014,'black iron')
        f.line((b-.17,.19,1.03),(b-.17,1.00,1.03),.015,'black iron')
    elif style=='saifee':
        pass  # Joined awning and individually placed inventory follow below.
    wear(f,a,b,.2,3.4,count=36,depth=.078,seed=31)


def tile_mosaic(f,a,b,low,high,kind='base'):
    step=.088
    for ix in range(max(1,int((b-a)/step))):
        s=a+(ix+.5)*step
        for iy in range(max(1,int((high-low)/step))):
            y=low+(iy+.5)*step
            mat='seventh tile plum'
            if kind=='edge' or iy in [1,2]:mat='seventh tile olive'
            elif (ix//4+iy//3)%7==0:mat='seventh dark stone'
            elif (ix*19+iy*7)%53==0:mat='sill patina'
            f.b(s,y,.165,step-.006,step-.006,.020,mat)


def corner_canopy(f,y,drop,depth,valance,mat,stripe=None):
    # Hip joins the two perpendicular canopies across the outside corner.
    reach=depth+.10;bottom=y-drop
    a=(0,y,.10);b=(0,bottom,reach);c=(-reach,bottom,reach);d=(-reach,bottom,.10)
    face([f.p(*a),f.p(*b),f.p(*c)],mat);face([f.p(*a),f.p(*c),f.p(*d)],mat)
    for l,r in [(b,c),(c,d)]:
        face([f.p(*l),f.p(*r),f.p(r[0],bottom-valance,r[2]),f.p(l[0],bottom-valance,l[2])],mat)
        f.line(l,r,.012,'metal')
    if stripe:
        for i in range(1,int(reach/.115)+1):
            for off in [0,.024]:
                t=min(.98,(i*.115+off)/reach);ss=-reach*t;dd=.10+depth*t;high=y-drop*t
                face([f.p(ss,high+.005,dd),f.p(ss+.006,high+.005,dd),f.p(ss+.006,bottom+.005,reach),f.p(ss,bottom+.005,reach)],stripe)
                f.b(ss,bottom-valance/2,reach+.008,.006,valance,.008,stripe)
                face([f.p(-reach*t,high+.005,dd),f.p(-reach*t,high+.005,dd+.006),f.p(-reach,bottom+.005,dd+.006),f.p(-reach,bottom+.005,dd)],stripe)
                face([f.p(-reach-.006,bottom,dd),f.p(-reach-.006,bottom,dd+.006),f.p(-reach-.006,bottom-valance,dd+.006),f.p(-reach-.006,bottom-valance,dd)],stripe)


def tile_front(f,a,b):
    w=b-a;door_a=a+w*.12;door_b=a+w*.35;win_a=a+w*.43;win_b=b-.10
    OPENINGS[frontage_key(f)].append((a,.17,b,3.50))
    shop_room(f,a,b,3.45,'tile')
    # True voids through the ground wall, composed from separate piers/spandrels.
    for l,r in [(a,door_a),(door_b,win_a),(win_b,b)]:f.b((l+r)/2,1.82,.01,r-l,3.28,.19,'seventh tile paint')
    f.b((win_a+win_b)/2,.68,.015,win_b-win_a,.99,.19,'seventh tile paint')
    f.b((win_a+win_b)/2,2.94,.015,win_b-win_a,1.15,.19,'seventh tile paint')
    f.b((door_a+door_b)/2,3.15,.015,door_b-door_a,.60,.19,'store teal')
    # Door frame and painted green slab, deeply recessed; old metal kick plate.
    for ss in [door_a,door_b]:f.b(ss,1.57,-.03,.091,2.77,.22,'store teal')
    f.b((door_a+door_b)/2,.61,-.22,door_b-door_a-.10,.83,.08,'store teal')
    f.b((door_a+door_b)/2,2.70,-.22,door_b-door_a-.10,.24,.08,'store teal')
    for ss in [door_a+.105,door_b-.105]:f.b(ss,1.79,-.22,.12,1.61,.08,'store teal')
    glass_opening(f,door_a+.055,door_b-.055,1.02,2.58,'store teal',False,-.158,'store teal')
    f.b((door_a+door_b)/2,.38,-.028,door_b-door_a-.12,.31,.025,'brass')
    f.b(door_b-.11,1.05,-.028,.060,.31,.025,'brass')
    f.line((door_b-.11,1.02,.009),(door_b-.11,1.15,.009),.014,'brass')
    ctext(f,(door_a+door_b)/2,.91,door_b-door_a-.10,'115','yellow paint',.25,-.028)
    threshold(f,door_a-.05,door_b+.05,.59,'cream stone')
    glass_opening(f,win_a,win_b,1.11,2.28,'seventh tile plum',False,.035,'seventh tile paint',2)
    # Sill tiles, checker patch and irregular stair-step edges around the door.
    tile_mosaic(f,win_a-.08,win_a+.92,.18,1.04)
    tile_mosaic(f,win_a-.08,win_b+.02,.18,.36)
    tile_mosaic(f,win_a-.08,win_b+.02,.44,.54,'edge')
    tile_mosaic(f,win_a-.08,win_b+.02,1.055,1.155,'edge')
    tile_mosaic(f,win_a-.08,win_a+.025,1.14,2.39,'edge')
    tile_mosaic(f,win_b-.04,win_b+.06,1.14,2.39,'edge')
    for side in [-1,1]:
        edge=door_a-.05 if side<0 else door_b+.05
        for j in range(5):
            ss=edge+side*j*.09;top=1.4-j*.22
            tile_mosaic(f,ss-.042,ss+.045,.18,max(.27,top),'edge' if j==0 else 'base')
    for i in range(6):
        for j in range(4):f.b(win_a+.34+i*.045,.91+j*.045,.180,.041,.041,.012,'sign white' if (i+j)%2 else 'seventh tile plum')
    # Same stripes on both return and avenue; opaque soffit and real support ribs.
    aw={'material':'seventh blue canvas','stripe':'sign white','y':3.47,'drop':.56,'depth':1.17,'valance':.32,'stripeSpacing':.115,'stripeWidth':.008,'text':'','textAt':.78,'textWidth':.40,'textSize':.29}
    observed_awning(f,a-.04,b+.05,aw)
    corner_canopy(f,3.47,.56,1.17,.32,'seventh blue canvas','sign white')
    ctext(f,a+w*.79,2.745,w*.41,'TILE BAR','sign white',.33,1.319)
    # Paired pinstripes are visible in the official exterior photograph.
    for i in range(int(w/.115)):
        ss=a+i*.115+.024
        face([f.p(ss,3.47,.10),f.p(ss+.006,3.47,.10),f.p(ss+.006,2.91,1.27),f.p(ss,2.91,1.27)],'sign white')
        f.b(ss,2.75,1.29,.005,.31,.007,'sign white')
    f.b((a+b)/2,2.635,.67,w+.1,.025,1.07,'poster paper')
    for ss in [a+.04,a+w*.33,a+w*.66,b-.03]:f.line((ss,3.36,.07),(ss,2.65,1.20),.012,'metal')
    ctext(f,win_a+(win_b-win_a)*.70,2.01,(win_b-win_a)*.40,'Shiner','neon amber',.26,.064,'neon-script')
    ctext(f,win_a+(win_b-win_a)*.22,2.03,(win_b-win_a)*.38,'Heineken','seventh green light',.13,.066,'outline')
    framed_notice(f,win_a+.23,1.32,.30,.38,'A','sign white','nishaan blue',.089)
    stock_shelves(f,win_a+.10,win_b-.10,-.78,1.04,1.75,'bottle')
    for ss in [win_a+.42,win_b-.43]:cafe_table(f,ss,1.15,'red')
    display_board(f,a+.18,1.20,'WELCOME TO','wood','black iron',1.08,.62)
    ctext(f,a+.18,.92,.48,'TILE BAR','sign white',.11,1.29,'script')
    pot_plant(f,b-.03,.18,.81,.17,1.13,50)
    # Weathered paint chips stay below the canopy, with no synthetic tags.
    wear(f,a,b,.25,2.61,'seventh tile olive',100,.119,91)


def tile_return(f):
    # Most of the return is masonry; the shared generic residential windows at
    # pavement level were wrong. Small corner window, side door and poster cases.
    f.b(f.L/2,1.57,.027,f.L,2.79,.075,'seventh tile paint')
    c=f.L-1.48
    OPENINGS[frontage_key(f)].append((c-.70,1.15,c+.70,2.25))
    f.b(c,1.69,.08,1.51,1.22,.19,'seventh tile plum')
    f.b(c,1.69,.19,1.31,1.00,.025,'dark glass')
    for ss in [c-.66,c+.66]:f.b(ss,1.7,.215,.045,1.09,.058,'store teal')
    tile_mosaic(f,c-.77,c+.77,.18,.69)
    tile_mosaic(f,c-.77,c+.77,1.09,1.20,'edge')
    observed_awning(f,f.L-3.10,f.L+.07,{'material':'seventh blue canvas','stripe':'sign white','y':3.47,'drop':.56,'depth':1.17,'valance':.32,'stripeSpacing':.115,'stripeWidth':.008,'text':'115','textAt':.80,'textSize':.25})
    # Far end's recessed residential doorway and mail slots.
    doorway(f,.84,'87',False,'seventh dark stone')
    for j in range(2):
        f.b(4.2+j*1.55,1.65,.12,1.41,1.76,.07,'black iron')
        for row in range(2):
            for col in range(3):framed_notice(f,3.76+j*1.55+col*.43,1.23+row*.77,.39,.67,'',d=.163)
    conduit(f,2.03,.22,12.95,'metal',.15)
    for yy in [3.21,3.32]:f.line((1.4,yy,.085),(f.L-.1,yy,.085),.009,'black iron')
    wear(f,1.8,f.L,.25,3.0,count=80,depth=.077,seed=29)


def canopy_text(f,s,t,w,text,size=.24):
    top=4.0;drop=.95;depth=.90;length=math.hypot(drop,depth)
    curve=bpy.data.curves.new('Saifee fabric lettering','FONT')
    curve.body=text;curve.size=size;curve.align_x='CENTER';curve.align_y='CENTER';curve.resolution_u=5;curve.extrude=.001
    obj=bpy.data.objects.new(ns['OWNER']+' / canopy / '+text,curve);bpy.context.collection.objects.link(obj)
    x,y,z=f.p(s,top-drop*t+.012,.10+depth*t+.02);obj.location=(x,-z,y)
    right=Vector((f.rx,-f.rz,0));up=Vector((-f.nx*depth/length,f.nz*depth/length,drop/length))
    obj.rotation_euler=Matrix((right,up,right.cross(up))).transposed().to_euler()
    obj.data.materials.append(MATS['sign white']);bpy.context.view_layer.update()
    width=max(v[0] for v in obj.bound_box)-min(v[0] for v in obj.bound_box)
    if width>w:curve.size*=w/width


def saifee_awning(f,main=False):
    observed_awning(f,-.025,f.L+.025,{'material':'awning brown','y':4.0,'drop':.95,'depth':.90,'valance':.18,'text':''})
    f.b(f.L/2,2.84,.58,f.L,.018,.86,'poster paper')
    if main:
        for t,text,size in [(.34,'SAIFEE',.36),(.59,'hardware',.27),(.81,'& garden',.25)]:canopy_text(f,f.L*.36,t,f.L*.49,text,size)
        canopy_text(f,f.L*.83,.68,f.L*.25,'California',.16)
        canopy_text(f,f.L*.83,.87,f.L*.25,'Paints',.12)
        ctext(f,f.L*.50,2.96,f.L*.95,'ELECTRICAL · PLUMBING · LUMBER · POTS · SOIL','sign white',.093,1.034)
    else:
        canopy_text(f,f.L*.37,.70,f.L*.75,'RALPH LAUREN PAINT',.15)
        canopy_text(f,f.L*.37,.43,f.L*.24,'RL',.17)
        ctext(f,f.L*.23,2.96,f.L*.40,'114 FIRST AVENUE','sign white',.12,1.034)
    for ss in [.18,f.L-.18]:
        f.line((ss,3.91,.08),(ss,3.10,1.03),.013,'metal')
        rod(f.p(ss,3.00,.82),f.p(ss,3.12,.82),.047,'opal lamp',10,r2=.028)


def string_lights(f,points,step=.20):
    for (s0,y0,d0),(s1,y1,d1) in zip(points,points[1:]):
        length=math.dist((s0,y0,d0),(s1,y1,d1));n=max(1,int(length/step))
        f.line((s0,y0,d0),(s1,y1,d1),.0035,'black iron')
        for i in range(n):
            t=(i+.5)/n;s=s0+(s1-s0)*t;y=y0+(y1-y0)*t;d=d0+(d1-d0)*t
            f.b(s,y,d,.018,.034,.022,'neon amber')


def saifee_front(f,main):
    design={'cornerStyle':'saifee','top':3.80,'frame':'white frame','base':.28,'head':2.99,'panels':[['window',.78],['door',.22]] if main else [['door',.27],['window',.73]]}
    shop_front(f,.035,f.L-.04,design)
    saifee_awning(f,main)
    if not main:corner_canopy(f,4.0,.95,.90,.18,'awning brown')
    for i in range(5):f.b(f.L/2,3.015+i*.036,.13,f.L-.08,.020,.18,'metal')
    if main:
        plant_rack(f,f.L*.28,.56,1.42,1.72,10)
        plant_rack(f,f.L*.59,.56,1.29,1.75,40)
        for s in [f.L*.15,f.L*.39,f.L*.63]:pot_plant(f,s,2.45,.76,.14,1.16,int(s*22),True)
        pot_plant(f,f.L-.04,.18,.59,.23,1.35,19)
        ctext(f,f.L*.84,2.13,.57,'OPEN','seventh green light',.19,.087,'outline')
        framed_notice(f,f.L*.86,1.57,.33,.60,'HOURS','sign white','black iron',.09)
    else:
        plant_rack(f,f.L*.48,.55,1.29,1.63,80)
        plant_rack(f,f.L*.83,.55,1.07,1.67,100)
        for s in [f.L*.36,f.L*.62,f.L*.88]:pot_plant(f,s,2.48,.80,.13,.87,int(s*11),True)
        ctext(f,f.L*.15,2.14,.50,'OPEN','neon orange',.14,-.13,'outline')
    for s in [f.L*.35,f.L*.65]:pot_plant(f,s,.18,1.02,.125,.40,int(s*400))
    # Cables remain in daylight; lit bulbs follow the September 2025 image.
    h=17.68 if main else 13.15
    for t in ([.04,.77,.97] if main else [.18,.38,.59,.81]):
        string_lights(f,[(f.L*t,h+.06,.16),(f.L*t-.22,h*.69,.17),(f.L*t-.39,4.03,.28)])
    if main:
        string_lights(f,[(.05,h+.9,.15),(f.L-.07,h+.9,.15)])
        string_lights(f,[(f.L*.45,15.75,.97),(f.L*.12,5.25,1.13),(f.L*.89,5.25,1.13),(f.L*.45,15.75,.97)])


def yubu_front(f,a,b):
    w=b-a
    OPENINGS[frontage_key(f)].append((a,.17,b,3.88))
    shop_room(f,a,b,3.80,'yubu')
    for ss in [a+.05,b-.05]:f.b(ss,1.81,.035,.15,3.30,.28,'cream stone')
    door=a+w*.40
    glass_opening(f,a+.10,door,.31,2.66,'wood',True,-.13,'wood')
    glass_opening(f,door+.08,b-.12,.69,2.66,'wood',False,.0,'wood',2)
    f.b((a+b)/2,3.1,.025,w-.12,.65,.15,'cream stone')
    ac_unit(f,a+w*.19,2.75,.49,.33)
    observed_awning(f,a,b,{'material':'seventh red enamel','y':3.91,'drop':.24,'depth':.72,'valance':.17,'text':'YUBU','textSize':.21})
    ctext(f,a+w*.22,1.73,w*.33,'YUBU','sign white',.105,-.043)
    framed_notice(f,door-.14,1.02,.15,.23,'',d=-.038)
    for j in range(5):food_decal(f,b-.13,1.00+j*.21,.12,.18,.21)
    # Photographed slatted folding wood table, red metal crossed legs.
    s=a+w*.63;d=.88
    for j in range(7):f.b(s,.89,d+(j-3)*.057,.59,.029,.046,'interior oak')
    for dd in [d-.18,d+.18]:
        f.line((s-.22,.18,dd),(s+.22,.87,dd),.013,'seventh red enamel')
        f.line((s+.22,.18,dd),(s-.22,.87,dd),.013,'seventh red enamel')
    threshold(f,a,door,.41)


def burger_front(f,a,b):
    w=b-a;c=(a+b)/2
    OPENINGS[frontage_key(f)].append((a,.17,b,3.65));shop_room(f,a,b,3.55,'burger')
    # Central doorway between projecting wood display bays, not a white shop kit.
    for l,r in [(a+.09,a+w*.39),(a+w*.64,b-.08)]:
        glass_opening(f,l,r,.56,2.91,'wood',False,.30,'wood')
        for ss in [l,r]:
            f.b(ss,1.67,.29,.075,2.64,.20,'wood')
            for yy in [2.48,2.61,2.78]:f.b(ss,yy,.37,.095,.085,.17,'wood')
        for yy in [.41,.56,2.87]:f.b((l+r)/2,yy,.38,r-l+.12,.07,.21,'wood')
        for ss in [l+.05,r-.05]:f.b(ss,.34,.40,.065,.30,.064,'wood')
    glass_opening(f,a+w*.40,a+w*.64,.27,2.70,'wood',True,-.19,'wood')
    for l,r in [(a+.09,a+w*.39),(a+w*.64,b-.08)]:
        for ss in [l,r]:
            face([f.p(ss,.56,-.035),f.p(ss,2.89,-.035),f.p(ss,2.89,.30),f.p(ss,.56,.30)],'seventh glass')
            f.b(ss,1.67,.12,.053,2.63,.36,'wood')
    # Worn black and yellow diagonal cellar-hatch edging.
    ha=a+w*.64;hb=b-.02
    f.b((ha+hb)/2,.195,.70,hb-ha,.028,.90,'black iron')
    for i in range(int((hb-ha)/.19)):
        ss=ha+i*.19
        face([f.p(ss,.211,.26),f.p(min(ss+.065,hb),.211,.26),f.p(min(ss+.40,hb),.211,1.12),f.p(min(ss+.33,hb),.211,1.12)],'yellow paint')
    fascia(f,a,b,'','burger')
    ctext(f,a+w*.235,1.79,w*.30,'7TH STREET','seventh red enamel',.22,.32)
    ctext(f,a+w*.235,1.56,w*.30,'BURGER','seventh red enamel',.23,.32)
    framed_notice(f,a+w*.815,1.16,w*.23,.90,'CHEESEBURGER','sign white','black iron',.333)
    for i,t in enumerate(['DOUBLE','IMPOSSIBLE','FRIES','MEXICAN COKE','WATER']):ctext(f,a+w*.815,1.32-i*.103,w*.20,t,'black iron',.065,.350)
    ac_unit(f,b-.14,2.43,.53,.45)
    conduit(f,b-.015,.2,4.13,'black iron',.16)
    wear(f,a,b,.2,3.55,'sill patina',50,.409,51)


def ground_return(f,profile):
    if profile=='deli':
        end=f.L*.46
        # Return has one corner display and masonry further east; no repeating
        # residential kit under the uninterrupted deli sign.
        OPENINGS[frontage_key(f)].append((.06,.17,end,3.80))
        shop_room(f,.04,end,3.70,'deli')
        f.b((end+2.23)/2,1.47,.015,end-2.23,2.60,.09,'black iron')
        glass_opening(f,.16,min(2.16,end-.1),.86,2.71,'black iron',False,.105,'black iron')
        for i in range(4):food_decal(f,.39+i*.43,1.20,.36,.37,.151)
        fascia(f,.01,end,'DELI & CAFE','deli')
        # Blue-painted return artwork is deliberately not replaced with invented
        # mural lettering. Color field/paint edges only; artwork remains a gap.
        f.b((end+2.40)/2,1.61,.063,end-2.40,2.86,.065,'painted blue')
        # Only the visible blue field is established; the occluded mural is
        # documented as incomplete instead of inventing a repeated motif.
        doorway(f,f.L*.655,'91',False,'seventh dark stone')
        conduit(f,f.L*.606,.2,4.3,'black iron',.12)
    elif profile=='smoke':
        end=f.L*.40
        OPENINGS[frontage_key(f)].append((.05,.17,end,3.74))
        shop_room(f,.05,end,3.62,'smoke')
        for j in range(3):glass_opening(f,.09+j*(end-.18)/3,.09+(j+1)*(end-.18)/3,.44,2.72,'window frame',False,.02,'black iron')
        fascia(f,.02,end,'E SMOKE & CONVENIENCE','smoke')
        # Intermediate return openings are separately composed from the older
        # Yubu photo. Uncorroborated neighboring business name stays off the sign.
        f.b((end+f.L*.60)/2,1.8,.022,f.L*.60-end,3.26,.055,'seventh red plaster')
        doorway(f,f.L*.56,'86',False,'seventh dark stone')
        a=f.L*.64;b=f.L*.835
        OPENINGS[frontage_key(f)].append((a,.17,b,3.6))
        shop_room(f,a,b,3.5,'jewelry')
        glass_opening(f,a+.10,b-.11,.69,2.80,'white frame',False,-.05,'seventh red brick')
        f.b((a+b)/2,3.12,.14,b-a,.35,.33,'white frame')
        framed_notice(f,a+.22,1.75,.31,.41,'',d=.027)
    elif profile=='saifee-corner':
        # The green side paint and service entrance are visible in dated side
        # photographs. Upper-return window spacing remains recorded inference.
        f.b(f.L/2,1.55,.022,f.L,2.75,.054,'awning green')
        for s in [f.L*.22,f.L*.49]:
            f.b(s,1.37,.08,1.09,2.41,.10,'door enamel')
            f.b(s,2.09,.14,.84,.70,.022,'dark glass')
            f.b(s+.35,1.09,.17,.035,.21,.026,'brass')
        for i in range(5):
            s=f.L*.65+i*.83
            pot_plant(f,s,.18,.50,.16,.54,300+i)
        observed_awning(f,f.L-5.35,f.L+.02,{'material':'awning brown','y':4.0,'drop':.95,'depth':.90,'valance':.18,'text':'HARDWARE & GARDEN','textSize':.21})
        conduit(f,f.L*.57,.18,3.65,'metal',.10)


def corner_roof(b,profile):
    h=profile['height'];x0,z0,x1,z1=b['box']
    if profile['roof']=='antenna-rack':
        f=next(Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']) for v in b['frontages'] if v['street']=='First Avenue')
        for y in [h+.65,h+1.64]:f.line((.6,y,-1.4),(f.L-.5,y,-1.4),.033,'metal')
        for i in range(4):
            s=.65+i*(f.L-1.25)/3
            f.line((s,h+.03,-1.4),(s,h+2.02,-1.4),.038,'metal')
            f.b(s,h+1.60,-1.43,.24,.91,.15,'air conditioner')
            f.line((s,h+.7,-1.42),(s,h+.2,-2.2),.025,'metal')
        box(x0+2.3,h+.48,z0+2,1.0,.95,.95,'seventh red brick')
        rod((x0+2.3,h+.95,z0+2),(x0+2.3,h+1.45,z0+2),.14,'metal',12)
    if profile['roof']=='railing-and-plants':
        v=next(v for v in b['frontages'] if v['street']=='First Avenue');f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length'])
        for y in [h+.06,h+.94]:f.line((0,y,-.13),(f.L,y,-.13),.023,'black iron')
        for i in range(int(f.L/.12)):f.line((i*.12,h+.04,-.13),(i*.12,h+1.03,-.13),.009,'black iron')
        for i in range(7):pot_plant(f,.35+i*(f.L-.7)/7,h+.10,-.72,.12,.37,i+500)


def corner_streets():
    owner('First & Seventh / photographed streetscape; positions estimated')
    for px,pz in CORNER_SOURCE['streetFurniture']['signals']:
        f=Facade(px,pz,1,0,1)
        # Cast base, bolted access plate, galvanized shaft and curved mast.
        f.b(0,.23,0,.40,.12,.40,'metal')
        rod(f.p(0,.23,0),f.p(0,.85,0),.15,'metal',16,r2=.095)
        rod(f.p(0,.85,0),f.p(0,4.78,0),.065,'metal',16,r2=.052)
        for dx in [-.14,.14]:
            for dd in [-.14,.14]:rod(f.p(dx,.293,dd),f.p(dx,.32,dd),.029,'black iron',6)
        f.b(0,.61,.147,.10,.23,.027,'sill patina')
        direction=1 if px<0 else -1
        curve=[(0,4.70,0),(.03*direction,5.17,0),(.18*direction,5.57,0),(.44*direction,5.88,0),(.83*direction,6.09,0),(1.40*direction,6.18,0),(1.80*direction,6.16,0)]
        for a,b in zip(curve,curve[1:]):f.line(a,b,.043,'metal')
        f.b(direction*1.75,6.12,0,.48,.15,.21,'metal')
        f.b(direction*1.75,6.04,.03,.37,.035,.13,'opal lamp')
        f.line((0,4.74,0),(direction*.77,4.74,0),.031,'metal')
        for ss in [.16*direction,.70*direction]:
            f.b(ss,4.87,.12,.25,.85,.25,'yellow paint')
            for i in range(3):
                yy=5.13-i*.26
                rod(f.p(ss,yy,.25),f.p(ss,yy,.345),.090,'black iron',16)
                rod(f.p(ss,yy,.347),f.p(ss,yy,.354),.073,'seventh green light' if i==2 else 'shop burgundy',16)
                # Hood shading makes the unlit bulbs read as dark lenses.
                for j in range(9):
                    a=j*math.pi/9;b=(j+1)*math.pi/9
                    face([f.p(ss+.091*math.cos(a),yy+.091*math.sin(a),.24),f.p(ss+.091*math.cos(b),yy+.091*math.sin(b),.24),f.p(ss+.091*math.cos(b),yy+.091*math.sin(b),.41),f.p(ss+.091*math.cos(a),yy+.091*math.sin(a),.41)],'black iron')
        f.b(0,2.48,.11,.44,.49,.24,'yellow paint');f.b(0,2.48,.24,.35,.40,.021,'black iron')
        # Pixel-shaped pedestrian hand in the observed yellow signal housing.
        for x,y,w,h in [(-.03,2.45,.12,.15),(-.087,2.52,.028,.12),(-.047,2.55,.026,.13),(-.007,2.55,.026,.13),(.032,2.52,.026,.11),(.071,2.43,.08,.041)]:
            f.b(x,y,.258,w,h,.010,'neon orange')
        for yy in [3.38,3.74,4.08]:rod(f.p(0,yy-.027,0),f.p(0,yy+.027,0),.081,'metal',16)
        f.b(.22,3.68,.08,1.10,.28,.05,'sign white')
        f.b(.22,3.68,.111,1.01,.213,.012,'black iron')
        ctext(f,.18,3.68,.75,'ONE WAY','sign white',.125,.122)
        face([f.p(-.26,3.67,.132),f.p(-.12,3.77,.132),f.p(-.12,3.57,.132)],'sign white')
        for angle,name,y in [(0,'E 7 St',3.98),(math.pi/2,'1 AV',4.23)]:
            for reverse in [0,math.pi]:
                rx,rz=math.cos(angle+reverse),math.sin(angle+reverse)
                sf=Facade(px-rx*.45,pz-rz*.45,rx,rz,.90)
                sf.b(.45,y,.033,.95,.22,.030,'store teal')
                ctext(sf,.45,y,.84,name,'sign white',.135,.053)
        for j in range(7):framed_notice(f,0,.98+j*.147,.093,.10,'',d=.080)
    for px,pz in CORNER_SOURCE['streetFurniture']['mailboxes']:
        f=Facade(px,pz,1,0,1)
        for ss in [-.23,.23]:
            for dd in [-.23,.23]:f.b(ss,.38,dd,.06,.39,.07,'black iron')
        f.b(0,.76,0,.61,.58,.58,'door enamel')
        # Curved collection-box roof along its depth; separately visible seam.
        for i in range(18):
            a=i*math.pi/18;b=(i+1)*math.pi/18
            for side in [-1,1]:
                face([f.p(side*.305,1.02,0),f.p(side*.305,1.02+math.sin(a)*.29,math.cos(a)*.29),f.p(side*.305,1.02+math.sin(b)*.29,math.cos(b)*.29)],'door enamel')
            face([f.p(-.305,1.02+math.sin(a)*.29,math.cos(a)*.29),f.p(.305,1.02+math.sin(a)*.29,math.cos(a)*.29),f.p(.305,1.02+math.sin(b)*.29,math.cos(b)*.29),f.p(-.305,1.02+math.sin(b)*.29,math.cos(b)*.29)],'door enamel')
        f.b(0,1.00,.30,.45,.045,.06,'black iron')
        f.b(0,.955,.345,.32,.034,.045,'metal')
        framed_notice(f,0,.70,.29,.28,'U.S. MAIL','sign white','nishaan blue',.307)
        for j in range(9):framed_notice(f,-.21+(j%3)*.18,.40+(j//3)*.18,.11,.083,'',d=.312)
        wear(f,-.28,.28,.48,1.06,'sign white',30,.327,709)
    for px,pz in CORNER_SOURCE['streetFurniture']['bins']:
        f=Facade(px,pz,1,0,1)
        for i in range(28):
            a=i*math.tau/28;ss=math.cos(a)*.255;d=math.sin(a)*.255
            f.line((ss,.21,d),(ss,1.02,d),.013,'door enamel')
        for y in [.22,.43,.81,1.02]:
            for i in range(32):
                a=i*math.tau/32;b=(i+1)*math.tau/32
                f.line((math.cos(a)*.264,y,math.sin(a)*.264),(math.cos(b)*.264,y,math.sin(b)*.264),.022,'door enamel')
        rod(f.p(0,.22,0),f.p(0,.25,0),.25,'black iron',24)
        framed_notice(f,0,.67,.19,.22,'NYC','store teal','sign white',.27)


def build_first_seventh(b):
    profile=CORNER_BUILDINGS.get(b['id'])
    if not profile:return False
    h=profile['height'];b['renderHeight']=h
    owner(profile['address']+' / First & Seventh photographic benchmark')
    wall_mass(b,profile['wall'])
    for v in b['frontages']:
        spec=profile['elevations'].get(v['street'])
        if not spec:continue
        f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']);f.wall=profile['wall']
        for row,(bottom,wh) in enumerate(spec['rows']):
            for col,t in enumerate(spec['bays']):
                w=spec.get('widths',[spec['width']]*len(spec['bays']))[col]
                individual=spec.get('windowOverrides',{}).get(f'{row}:{col}',{})
                cwindow(f,t*f.L,individual.get('bottom',bottom),w,individual.get('height',wh),spec,row,col)
        if spec.get('blindPanel'):
            a,end=spec['blindPanel'];low=3.50
            f.b((a+end)*f.L/2,(low+h-.28)/2,.032,(end-a)*f.L,h-.28-low,.090,'painted ivory')
            for s in [a*f.L,end*f.L]:f.b(s,(h+low)/2,.09,.055,h-low,.042,'sill patina')
        if spec.get('redBand'):
            low=spec['redBand'];f.b(f.L/2,(low+h)/2,.005,f.L,h-low,.055,'seventh red brick')
        if profile['profile']=='saifee-corner':buff_brickwork(f,3.48,spec.get('redBand',h-.17))
        cornice_corner(f,h,profile['roof'])
        if spec.get('escape'):
            e=spec['escape'];escape(f,e['center']*f.L,[r[0]-.22 for r in spec['rows']],e['width'],e['material'])
        for e in spec.get('escapes',[]):
            escape(f,e['center']*f.L,[r[0]-.22 for r in spec['rows']],e['width'],e['material'])
        kind=profile['profile'];street=v['street']
        if kind=='tile':
            if street=='First Avenue':tile_front(f,.10,f.L-.08)
            else:tile_return(f)
        elif kind in ['saifee-corner','saifee-main'] and street=='First Avenue':saifee_front(f,kind=='saifee-main')
        else:
            if street=='East 7th Street':ground_return(f,kind)
            if kind=='deli' and street=='First Avenue':doorway(f,f.L*.425,'120',False,'seventh dark stone')
            for r in b.get('businesses',[]):
                if not r.get('renderName') or r['street']!=street or not r.get('design',{}).get('cornerStyle'):continue
                a,end=r['unit'];style=r['design']['cornerStyle']
                if style=='yubu':yubu_front(f,a,end)
                elif style=='burger':burger_front(f,a,end)
                else:shop_front(f,a,end,r['design'])
        # Small utility and masonry details follow known building-specific types.
        wear(f,.14,f.L-.14,3.7,h-.3,'sill patina',int(f.L*9),.008,34)
        if kind in ['tile','deli']:
            conduit(f,f.L-.17,3.60,h-.35,'black iron',.08)
    corner_roof(b,profile)
    if profile['profile']=='saifee-corner':corner_streets()
    return True


# The current, bounded refinement extends this accepted recipe. Its file is
# included in the corner-only export signatures, leaving other tiles intact.
exec(compile((ROOT/'model-source/first_seventh_refinement.py').read_text(),str(ROOT/'model-source/first_seventh_refinement.py'),'exec'),globals())
