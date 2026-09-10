"""First & Seventh pass 08: dated visual observations, authored geometry.

Extends the accepted pass 06 recipe without replacing the First & 10th core.
Dimensions, surface marks, lettering outlines and occluded details are estimates.
No Google photographs are embedded, projected onto geometry or redistributed.
Reference dates and limitations: first-seventh-street-view-08.json.
"""
material('seventh aged olive',(.22,.205,.14),.87)
material('seventh oxidized iron',(.25,.073,.043),.79,.38)
material('seventh garden green',(.16,.35,.036),.68)
material('seventh garden canvas',(.079,.10,.042),.95)
material('seventh blue paint',(.09,.39,.66),.92)
material('seventh sky paint',(.34,.64,.80),.96)
material('seventh chalk paint',(.72,.70,.59),.99)
material('seventh faded green',(.31,.39,.21),.98)
material('seventh faded pink',(.57,.24,.25),.98)
material('seventh hen ochre',(.59,.24,.046),.88)
material('seventh tar paint',(.047,.055,.048),.96)
material('seventh soil sack',(.35,.57,.13),.87)
material('seventh white sack',(.72,.75,.62),.94)
material('seventh curb ramp',(.43,.075,.058),.89)
material('seventh canvas brown',(.092,.069,.051),.97)
material('seventh smoke brick',(.99,.77,.62),.88,texture='red_brick_03_diff_1k.jpg',normal='red_brick_03_nor_gl_1k.jpg')
WALL_MATERIALS['seventh smoke brick']=('red_brick_03',(.99,.77,.62))

_old_fascia=fascia
_old_shop_front=shop_front
_old_tile_front=tile_front
_old_ground_return=ground_return
_old_burger_front=burger_front
_old_yubu_front=yubu_front
_old_corner_streets=corner_streets
_old_saifee_front=saifee_front
_old_cwindow=cwindow
_old_escape=escape


def buff_brickwork(f,low,high):
    """Mortar is a thin surface band, not thousands of raised six-sided bars.

    Preserve the running bond, joint width and all opening exclusions; use two
    triangles per band instead of twelve to offset the new storefront detail.
    """
    openings=OPENINGS[frontage_key(f)];step=.073;width=.225
    def band(a,b,bt,top):
        face([f.p(a,bt,.010),f.p(b,bt,.010),f.p(b,top,.010),f.p(a,top,.010)],'seventh mortar')
    for row in range(int((high-low)/step)+1):
        y=low+row*step;cursor=0
        for a,b in sorted((max(0,l),min(f.L,r)) for l,bt,r,top in openings if bt-.012<y<top+.012)+[(f.L,f.L)]:
            if a>cursor:band(cursor,a,y-.003,y+.003)
            cursor=max(cursor,b)
        offset=(row%2)*width/2
        for j in range(int(f.L/width)+1):
            ss=j*width+offset
            if 0<ss<f.L and not any(l-.012<ss<r+.012 and bt-step<y<top for l,bt,r,top in openings):
                band(ss-.003,ss+.003,y,y+step)


def escape(f,center,levels,width=2.9,mat='black iron',stairs=True):
    if DETAIL_SEED not in CORNER_BUILDINGS:
        return _old_escape(f,center,levels,width,mat,stairs)
    # Open steel grating and angle-iron framing replace solid balcony slabs.
    # Stair runs repeat the same direction, visible in the corner photographs.
    for row,y in enumerate(levels):
        for dd in [.10,1.17]:f.b(center,y,dd,width,.075,.055,mat)
        for ss in [center-width/2,center+width/2]:
            f.b(ss,y,.635,.055,.075,1.13,mat)
            f.b(ss,y-.09,.025,.17,.28,.032,mat)
            for yy in [y-.18,y-.02]:rod(f.p(ss,yy,.046),f.p(ss,yy,.067),.022,'metal',6)
            f.line((ss,y-.52,.045),(ss,y-.04,1.13),.028,mat)
        for j in range(int(width/.065)+1):
            ss=center-width/2+j*.065
            f.b(ss,y+.012,.64,.019,.025,1.08,mat)
        for yy in [y+.17,y+1.04]:
            f.line((center-width/2,yy,1.19),(center+width/2,yy,1.19),.021,mat)
            for ss in [center-width/2,center+width/2]:f.line((ss,yy,.085),(ss,yy,1.19),.022,mat)
        for j in range(int(width/.125)+1):
            ss=center-width/2+j*.125
            f.line((ss,y+.045,1.19),(ss,y+1.05,1.19),.009,mat)
        for ss in [center-width/2,center+width/2]:
            for dd in [.22,.39,.56,.73,.9,1.07]:f.line((ss,y+.045,dd),(ss,y+1.05,dd),.009,mat)
        if row<len(levels)-1 and stairs:
            high=levels[row+1];left=center-width*.34;right=center+width*.34
            for dd in [.52,1.11]:
                f.line((left,y+.04,dd),(right,high+.04,dd),.035,mat)
                f.line((left,y+.88,dd),(right,high+.88,dd),.018,mat)
            for j in range(15):
                t=j/14;ss=left+(right-left)*t;yy=y+(high-y)*t
                f.b(ss,yy+.035,.815,.23,.034,.61,mat)
                for dd in [.55,.66,.77,.88,.99,1.08]:f.b(ss,yy+.055,dd,.23,.004,.012,'seventh tar paint')
                if j%2==0:
                    for dd in [.52,1.11]:f.line((ss,yy+.06,dd),(ss,yy+.88,dd),.008,mat)
    if levels:
        for ss in [center+.42,center+.82]:f.line((ss,2.51,1.18),(ss,levels[0]+.68,1.18),.023,mat)
        for j in range(max(1,int((levels[0]-2.2)/.27))):f.line((center+.42,2.53+j*.27,1.18),(center+.82,2.53+j*.27,1.18),.014,mat)


def cwindow(f,s,y,w,h,spec,row,col):
    _old_cwindow(f,s,y,w,h,spec,row,col)
    # Putty, corner mitres, sash stops and sill end caps stay below 1 cm relief.
    for dx in [-w/2+.067,w/2-.067]:
        f.b(s+dx,y+h/2,-.012,.011,h-.09,.013,'seventh tar paint')
    for yy in [y+.075,y+h-.074]:
        f.b(s,yy,-.013,w-.13,.012,.018,'seventh tar paint')
    for dx in [-w*.44,w*.44]:
        f.b(s+dx,y-.044,.147,.055,.029,.03,spec['trim'])
    if (row+col)%4==1 and h>1:
        # Slightly open sash, seen on several flats; positions are inferred.
        f.b(s,y+h*.50+.073,-.11,w-.16,.075,.016,'recess shadow')


def painted_word(f,s,y,w,text,mat,size,d=.108,outline=False):
    curve=bpy.data.curves.new('Authored painted lettering; outline estimate','FONT')
    curve.body=text;curve.size=size;curve.align_x='CENTER';curve.align_y='CENTER'
    curve.resolution_u=5;curve.extrude=.0005
    if not outline:curve.offset=.09*size
    if outline:curve.fill_mode='NONE';curve.bevel_depth=.014;curve.bevel_resolution=1
    obj=bpy.data.objects.new(ns['OWNER']+' / paint / '+text,curve);bpy.context.collection.objects.link(obj)
    x,yy,z=f.p(s,y,d);obj.location=(x,-z,yy)
    obj.rotation_euler=Matrix((Vector((f.rx,-f.rz,0)),Vector((0,0,1)),Vector((f.nx,-f.nz,0)))).transposed().to_euler()
    obj.data.materials.append(MATS[mat]);bpy.context.view_layer.update()
    measured=max(v[0] for v in obj.bound_box)-min(v[0] for v in obj.bound_box)
    if measured>w:curve.size*=w/measured


def paint_patch(f,s,y,w,h,mat,d=.11,seed=0):
    rng=random.Random(seed+431)
    points=[]
    for i in range(18):
        a=i*math.tau/18;r=rng.uniform(.84,1.0)
        points.append(f.p(s+math.cos(a)*w*.5*r,y+math.sin(a)*h*.5*r,d))
    for a,b in zip(points,points[1:]+points[:1]):face([f.p(s,y,d),a,b],mat)


def ink_path(f,points,mat,width=.015,depth=.12):
    for (x0,y0),(x1,y1) in zip(points,points[1:]):
        length=math.hypot(x1-x0,y1-y0)
        if length<.0001:continue
        dx=-(y1-y0)/length*width;dy=(x1-x0)/length*width
        face([f.p(x0+dx,y0+dy,depth),f.p(x0-dx,y0-dy,depth),f.p(x1-dx,y1-dy,depth),f.p(x1+dx,y1+dy,depth)],mat)


def paint_strokes(f,a,b,low,high,seed,depth=.12,count=13,palette=None):
    """Flat, irregular hand-painted marks; no repeating sinusoidal geometry."""
    rng=random.Random(seed)
    palette=palette or ['seventh chalk paint','seventh faded pink','seventh tar paint']
    paths=[[(0,.1),(.16,1),(.34,-.1),(.58,.87),(.61,.12),(.9,.6)],
           [(0,.66),(.21,.95),(.53,.92),(.61,.70),(.36,.50),(.17,.35),(.32,.08),(.64,.17),(.88,.46)],
           [(.04,.03),(.22,.91),(.59,.76),(.15,.42),(.69,.30),(.50,-.05)],
           [(0,.17),(.24,.83),(.43,.99),(.62,.92),(.43,.41),(.16,.04),(.84,.23)],
           [(0,.44),(.30,.64),(.71,.51),(.45,.39),(.14,.19),(.78,.07)],
           [(0,.84),(.75,.95),(.29,.02),(.23,.88),(.88,.28)]]
    for i in range(max(3,count//3)):
        w=rng.uniform(.32,.80);h=rng.uniform(.29,.68)
        s=rng.uniform(a,max(a,b-w));y=rng.uniform(low,max(low,high-h))
        glyph=paths[rng.randrange(len(paths))]
        points=[(min(b,max(a,s+x*w+yy*w*.14)),min(high,max(low,y+yy*h))) for x,yy in glyph]
        ink_path(f,points,palette[i%len(palette)],rng.uniform(.008,.015),depth)
        if i%4==0:ink_path(f,[(s,y-.035),(min(b,s+w*1.1),y+.026)],palette[i%len(palette)],.008,depth)


def masonry_age(f,low,high,seed=0):
    # Local color loss and water trails have varied lengths instead of one
    # repeating giant stain. The small geometry remains in the tile's batches.
    rng=random.Random(seed+DETAIL_SEED)
    openings=OPENINGS[frontage_key(f)]
    for i in range(int(f.L*8)):
        s=rng.uniform(.06,f.L-.06);y=rng.uniform(low,high)
        if any(l-.1<s<r+.1 and b-.12<y<t+.12 for l,b,r,t in openings):continue
        w=rng.uniform(.017,.13);h=rng.uniform(.025,.17)
        paint_patch(f,s,y,w,h,'sill patina' if i%3 else 'seventh chalk paint',.005,i+seed)
    for s in [.035,f.L-.06]:
        for i in range(12):
            yy=low+(high-low)*i/12
            f.b(s,yy,.019,.029,(high-low)/13,.008,'sill patina')


def fascia(f,a,b,title,style):
    w=b-a;c=(a+b)/2
    if style=='hen':
        f.b(c,3.31,.15,w,.53,.19,'sign white')
        for yy in [3.065,3.555]:f.b(c,yy,.255,w,.024,.015,'seventh aged olive')
        ctext(f,c,3.32,w*.94,'Hen House Nyc','seventh aged olive',.48,.264,'script')
        ctext(f,c,3.33,w*.94,'Hen House Nyc','seventh hen ochre',.48,.268,'script')
        for ss in [a+.15,b-.15]:
            f.line((ss,3.63,.02),(ss,3.63,.38),.011,'metal')
            f.b(ss,3.59,.37,.13,.068,.17,'seventh tar paint')
    elif style=='monkey':
        f.b(c,3.28,.14,w,.45,.23,'seventh red enamel')
        for yy in [3.074,3.488]:f.b(c,yy,.265,w-.045,.022,.019,'sign white')
        # White round monkey mark: geometric approximation, not an exact logo.
        sign_panel(f,a+w*.12,3.29,.37,.34,.267,'sign white','oval')
        for dx in [-.095,.095]:sign_panel(f,a+w*.12+dx,3.30,.075,.11,.323,'seventh tar paint','oval')
        sign_panel(f,a+w*.12,3.24,.18,.095,.324,'seventh tar paint','oval')
        ctext(f,a+w*.59,3.29,w*.76,'MONKEY SUSHI','sign white',.29,.278)
    elif style=='deli':
        _old_fascia(f,a,b,title,style)
        # April sign has a deeper continuous fascia and large readable letters.
        for yy in [3.0,3.83]:f.b(c,yy,.163,w,.030,.26,'seventh tar paint')
    else:_old_fascia(f,a,b,title,style)


def shop_front(f,a,b,design):
    style=design['cornerStyle'];w=b-a;c=(a+b)/2
    if style=='monkey':
        OPENINGS[frontage_key(f)].append((a,.17,b,3.65))
        shop_room(f,a,b,3.60,'monkey')
        for ss in [a+.025,b-.025]:f.b(ss,1.75,.005,.11,3.15,.20,'seventh aged olive')
        glass_opening(f,a+.10,a+w*.40,.27,2.87,'black iron',True,-.19,'black iron')
        glass_opening(f,a+w*.43,b-.09,.28,2.85,'black iron',False,.013,'black iron')
        fascia(f,a,b,'MONKEY SUSHI',style)
        f.b(a+w*.72,1.32,.05,w*.52,.24,.028,'seventh red enamel')
        ctext(f,a+w*.72,1.32,w*.48,'MONKEY SUSHI','sign white',.14,.074)
        for ss,yy,ww,hh in [(a+w*.23,2.24,.23,.37),(a+w*.51,2.52,.25,.31),(a+w*.86,2.61,.28,.18)]:
            framed_notice(f,ss,yy,ww,hh,'',d=.062)
        for j in range(16):f.b(a+w*.72,1.50+j*.079,-.08,w*.43,.017,.012,'interior oak')
        f.b(c,2.98,.06,w-.05,.08,.12,'seventh aged olive')
        # Existing cast-iron capitals and rosettes, visible across all shop bays.
        for ss in [a+.035,b-.035]:
            for yy,ww in [(3.03,.22),(3.65,.25)]:f.b(ss,yy,.07,ww,.07,.23,'seventh aged olive')
            sign_panel(f,ss,2.87,.075,.075,.13,'seventh chalk paint','oval')
    else:
        _old_shop_front(f,a,b,design)
    if style=='deli':
        # Upright beverage coolers and layered decals, rather than only uniform boxes.
        for j in range(3):
            ss=a+w*(.17+.15*j)
            f.b(ss,1.53,-.61,w*.14,2.13,.10,'metal')
            for yy in [.57,1.05,1.53,2.01]:
                f.b(ss,yy,-.48,w*.12,.033,.15,'white frame')
        for j,t in enumerate(['ORGANIC','NATURAL','24 HRS']):
            ctext(f,a+w*(.12+j*.22),2.16,w*.20,t,'sign white',.085,.083)
    elif style=='smoke':
        for j,t in enumerate(['ATM','CIGAR','VAPE','SNACKS','GROCERY','LOTTO']):
            ss=a+w*(.1+(j%3)*.22);yy=.55+(j//3)*1.35
            ctext(f,ss,yy,w*.19,t,'seventh green light' if j%2 else 'yellow paint',.11,.097)
        sign_panel(f,b-.08,3.62,.39,.39,.15,'nishaan blue','oval')
        ctext(f,b-.08,3.62,.31,'113','sign white',.12,.21)
        for j in range(12):food_decal(f,a+w*(.09+(j%6)*.105),.86+(j//6)*.50,.19,.22,.087)
    elif style=='hen':
        for j in range(3):
            s=a+w*(.30+j*.21)
            pot_plant(f,s,.18,.13,.06,.58,221+j)
        for s in [a+.17,b-.15]:f.b(s,2.89,.04,.20,.071,.22,'seventh aged olive')


def tile_front(f,a,b):
    # April view has no pavement tables. Keep the individually authored door,
    # mosaic, shop glass and lights, while suppressing the old furniture calls.
    global cafe_table
    saved=cafe_table
    try:
        cafe_table=lambda *args,**kwargs:None
        _old_tile_front(f,a,b)
    finally:cafe_table=saved
    for yy in [.65,1.7,2.36]:framed_notice(f,a+.065,yy,.13,.18,'',d=.143)


def tile_return(f):
    f.b(f.L/2,1.66,.026,f.L,2.98,.076,'seventh tile paint')
    # One small glazed panel near the corner; long painted wall behind canopy.
    c=f.L-1.48
    OPENINGS[frontage_key(f)].append((c-.53,1.0,c+.53,2.24))
    glass_opening(f,c-.53,c+.53,1.0,2.24,'store teal',False,.10,'seventh tile paint')
    framed_notice(f,c,1.61,.67,.93,'B','black iron','sign white',.174)
    for i in range(7):f.b(c-.44+i*.146,.87,.145,.082,.14,.016,'seventh tile olive')
    doorway(f,.87,'87',False,'seventh dark stone')
    for j in range(2):framed_notice(f,1.67,1.46+j*.37,.12,.29,'',d=.09)
    aw={'material':'seventh blue canvas','stripe':'sign white','y':3.47,'drop':.56,
        'depth':1.17,'valance':.32,'stripeSpacing':.115,'stripeWidth':.008,'text':''}
    observed_awning(f,1.95,f.L+.07,aw)
    for i in range(int((f.L-1.95)/.115)):
        ss=1.95+i*.115+.024
        face([f.p(ss,3.47,.10),f.p(ss+.006,3.47,.10),f.p(ss+.006,2.91,1.27),f.p(ss,2.91,1.27)],'sign white')
        f.b(ss,2.75,1.29,.006,.31,.008,'sign white')
    ctext(f,3.18,2.74,2.13,'TILE BAR','sign white',.27,1.319)
    ctext(f,f.L-1.05,2.74,1.0,'115','sign white',.24,1.319)
    f.b((1.95+f.L)/2,2.635,.67,f.L-1.95,.025,1.07,'poster paper')
    for s in [2.05,5.4,8.8,12.0,f.L-.1]:f.line((s,3.40,.07),(s,2.63,1.23),.012,'metal')
    paint_strokes(f,2.12,f.L-2.4,.50,2.50,1201,.081,48,['seventh chalk paint','seventh faded pink'])
    painted_word(f,f.L*.59,2.31,1.50,'HELP','seventh faded green',.31,.083)
    for ss in [f.L*.59,f.L*.66]:
        f.b(ss,.64,.48,.56,.86,.59,'door enamel')
        f.b(ss,1.085,.48,.60,.035,.64,'black iron')
        for dx in [-.21,.21]:rod(f.p(ss+dx-.035,.23,.65),f.p(ss+dx+.035,.23,.65),.080,'black iron',10)
        ctext(f,ss,.86,.28,'NYC','sign white',.075,.781)
    f.b(f.L*.56,.194,1.19,2.46,.028,.74,'seventh tar paint')
    for j in range(16):f.line((f.L*.56-1.20+j*.15,.213,.86),(f.L*.56-1.20+j*.15,.213,1.51),.004,'metal')
    conduit(f,2.02,.22,12.95,'metal',.15)
    masonry_age(f,3.52,12.97,17)


def saifee_awning(f,main=False):
    observed_awning(f,-.025,f.L+.025,{'material':'seventh canvas brown','y':4.0,'drop':.95,'depth':.90,'valance':.18,'text':''})
    f.b(f.L/2,2.84,.58,f.L,.018,.86,'poster paper')
    if main:
        for t,text,size in [(.24,'SAIFEE',.40),(.49,'hardware',.28),(.72,'& garden',.28)]:canopy_text(f,f.L*.37,t,f.L*.50,text,size)
        canopy_text(f,f.L*.37,.90,f.L*.48,'saifeehardware.com',.098)
        canopy_text(f,f.L*.82,.70,f.L*.27,'California',.16)
        canopy_text(f,f.L*.82,.89,f.L*.25,'PAINTS',.10)
        ctext(f,f.L*.51,2.96,f.L*.98,'ELECTRICAL · PLUMBING · LUMBER · TOOLS · POTS · SOIL','sign white',.081,1.034)
    else:
        canopy_text(f,f.L*.39,.66,f.L*.72,'RALPH LAUREN PAINT',.135)
        canopy_text(f,f.L*.39,.45,f.L*.30,'RL',.16)
        ctext(f,f.L*.22,2.96,f.L*.39,'114 FIRST AVENUE','sign white',.103,1.034)
    for ss in [.18,f.L-.18]:
        f.line((ss,3.91,.08),(ss,3.10,1.03),.013,'metal')
        rod(f.p(ss,3.00,.82),f.p(ss,3.12,.82),.047,'opal lamp',10,r2=.028)


def inventory_bay(f,a,b,kind='plants',d=.25):
    w=b-a;c=(a+b)/2
    f.b(c,1.59,d-.26,w,2.70,.10,'seventh white sack')
    for s in [a,b]:f.b(s,1.58,d,.052,2.78,.47,'seventh garden green')
    if kind=='plants':
        for row,y in enumerate([.33,1.08,1.85]):
            f.b(c,y,d,w,.049,.54,'metal')
            for j in range(max(2,int(w/.33))):
                s=a+.16+j*.33
                pot_plant(f,s,y+.03,d,.085+.012*(j%3),.32+.11*((row+j)%4),820+row*22+j)
    elif kind=='pots':
        for row,y in enumerate([.35,1.12,1.86]):
            f.b(c,y,d,w,.05,.56,'metal')
            for j in range(max(2,int(w/.38))):
                s=a+.19+j*.38;r=.11+(j%2)*.022;h=.24+row*.035
                mat=['seventh chalk paint','seventh tar paint','red terra cotta'][j%3]
                rod(f.p(s,y+.03,d),f.p(s,y+.03+h,d),r*.75,mat,12,r2=r)
                rod(f.p(s,y+h+.031,d),f.p(s,y+h+.036,d),r*.86,'recess shadow',12)
        for row in range(3):
            for j in range(max(2,int(w/.40))):
                ss=a+.22+j*.40
                f.b(ss,.31+row*.13,d+.54,.36,.12,.55,'seventh soil sack' if (row+j)%3 else 'seventh white sack')
                f.b(ss,.374+row*.13,d+.54,.22,.007,.32,'seventh white sack')
                ctext(f,ss,.31+row*.13,.25,'SOIL','seventh garden green',.056,d+.822)
    else:stock_shelves(f,a+.04,b-.04,d,.32,2.35,'mixed')


def little_canopy(f,a,b,lines,mat='seventh garden canvas',top=3.95):
    observed_awning(f,a,b,{'material':mat,'y':top,'drop':.44,'depth':.77,'valance':.13,'text':lines[-1],'textSize':.14})
    for i,t in enumerate(lines[:-1]):ctext(f,(a+b)/2,top-.23-i*.14,b-a-.10,t,'sign white',.15,.50+i*.12)


def saifee_return(f):
    L=f.L
    OPENINGS[frontage_key(f)].append((.025,.17,L-.025,3.80))
    f.b(L/2,1.83,-.76,L,3.31,.04,'interior plaster')
    f.b(L/2,.205,-.22,L,.068,1.05,'interior tile')
    for t in [0,.09,.235,.39,.59,.72,.99]:
        f.b(t*L,1.77,.07,.15,3.20,.31,'seventh garden green')
    # East-end residential/service door and bamboo-blinded hardware window.
    glass_opening(f,.15,L*.087,.31,2.97,'seventh garden green',True,-.12,'seventh garden green')
    ctext(f,L*.042,3.15,L*.065,'90','sign white',.16,.04)
    glass_opening(f,L*.10,L*.232,.36,2.90,'seventh garden green',False,.01,'seventh garden green')
    for j in range(int(L*.132/.038)):
        f.b(L*.10+j*.038,2.05,.067,.027,1.45,.015,'interior oak')
    for s in [L*.11,L*.22]:framed_notice(f,s,1.82,.22,.27,'',d=.093)
    little_canopy(f,L*.10,L*.234,[''],'seventh tar paint',3.27)
    # Open hardware bay, full pot/soil display, candle entrance, corner plants.
    inventory_bay(f,L*.245,L*.382,'hardware',.19)
    little_canopy(f,L*.24,L*.388,['SAIFEE garden','ELECTRIC · PLUMBING · LUMBER'])
    inventory_bay(f,L*.397,L*.58,'pots',.16)
    little_canopy(f,L*.39,L*.592,[''],'seventh tar paint',3.38)
    glass_opening(f,L*.606,L*.708,.29,2.86,'seventh garden green',True,-.14,'seventh garden green')
    for j in range(6):food_decal(f,L*.657,1.15+j*.19,.35,.17,-.052)
    little_canopy(f,L*.596,L*.717,['HOME DECOR','GIFTS','CANDLES'])
    inventory_bay(f,L*.732,L*.97,'plants',.19)
    little_canopy(f,L*.793,L+.02,['VASES + PLANTERS','SAIFEEGARDEN.COM','OPEN 7 DAYS'],'seventh canvas brown')
    # Large weathered side sign spans the hardware and pot bays, as observed.
    a=L*.233;b=L*.59;c=(a+b)/2
    f.b(c,4.10,.12,b-a,.86,.13,'seventh chalk paint')
    ctext(f,c,4.22,b-a-.20,'SAIFEE HARDWARE','seventh faded pink',.50,.194)
    ctext(f,c+.025,4.19,b-a-.20,'SAIFEE HARDWARE','seventh aged olive',.50,.198)
    ctext(f,b-.81,3.86,1.4,'979-6396','seventh aged olive',.13,.20)
    for ss in [a+.12,b-.12]:
        for yy in [3.79,4.43]:rod(f.p(ss,yy,.185),f.p(ss,yy,.201),.018,'metal',8)
    # Waist-high green hardware carts and a narrow permanent threshold rail.
    for ss,ww in [(L*.157,L*.12),(L*.312,L*.12)]:
        f.b(ss,.65,.69,ww,.80,.37,'seventh garden green')
        f.b(ss,1.075,.69,ww+.04,.045,.45,'seventh garden green')
        for j in range(3):f.b(ss-ww*.31+j*ww*.30,.84,.895,ww*.24,.065,.013,'sign white')
    for ss in [L*.602,L*.712]:
        f.line((ss,.23,.59),(ss,1.14,.59),.014,'black iron')
        f.line((ss,1.14,.59),(ss,.84,.13),.014,'black iron')
    for ss in [L*.745,L*.88,L*.97]:pot_plant(f,ss,.18,.88,.17,.72,int(ss*33))
    conduit(f,L*.595,.21,4.54,'black iron',.16)
    masonry_age(f,4.58,12.93,431)


def deli_return(f):
    L=f.L;end=L*.255
    OPENINGS[frontage_key(f)].append((.06,.17,end,3.82))
    shop_room(f,.04,end,3.70,'deli')
    glass_opening(f,.14,end-.07,.39,2.72,'black iron',False,.055,'black iron')
    fascia(f,.01,end,'DELI','deli')
    for i,(text,mat) in enumerate([('DELI','seventh red enamel'),('GRILL','seventh red enamel'),('SALAD','seventh green light'),('24 HOURS','neon orange')]):
        ctext(f,end*.54,2.29-i*.26,end*.65,text,mat,.21,.093,'outline')
    for j in range(6):food_decal(f,.30+j*(end-.50)/6,.79,.28,.36,.092)
    # Broad blue-painted return: hand-authored painted fields and worn strokes.
    # This is a visual approximation of artwork, never a copied reference image.
    # Stop the opaque paint skin before Burger's recessed glazed frontage.
    # Ground-level paint must not cover the separate shop's registered opening.
    a=end;b=L*.728
    f.b((a+b)/2,1.70,.062,b-a,3.04,.065,'seventh blue paint')
    for j in range(28):
        s=a+.22+(b-a-.44)*j/27
        paint_patch(f,s,2.65+.10*math.sin(j*1.1),.95,.24,'seventh sky paint',.102,j)
        if j%2:paint_patch(f,s,2.43+.12*math.sin(j),.69,.12,'seventh chalk paint',.106,j+6)
    for j in range(12):
        s=a+.45+(b-a-.9)*j/11
        paint_patch(f,s,1.35+.11*math.sin(j),1.19,1.32,'seventh chalk paint' if j<7 else 'seventh tar paint',.111,j+72)
    paint_strokes(f,a+.08,b-.08,.29,2.20,819,.121,83)
    for t in [.43,.75]:
        f.line((L*t,.22,.142),(L*t,3.32,.142),.014,'seventh blue paint')
    # Pale upper wall has distinct stacked painted groups and dark lettering.
    w=L*.328;c=L*.168
    for yy,mat,hh in [(12.33,'seventh blue paint',.73),(10.79,'seventh faded pink',.89)]:
        for j in range(4):
            ss=c-w*.33+j*w*.22
            paint_patch(f,ss,yy,w*.26,hh,'seventh chalk paint',.093,92+j)
            paint_patch(f,ss,yy,w*.23,hh*.83,mat,.095,92+j)
            ink_path(f,[(ss-w*.08,yy-hh*.3),(ss-w*.04,yy+hh*.25),(ss+w*.08,yy+hh*.29),(ss+w*.04,yy-hh*.25)],'seventh chalk paint',.024,.098)
    painted_word(f,c,9.10,w*.93,'TARO','seventh tar paint',1.19,.111)
    painted_word(f,c,7.22,w*.96,'BOOP','seventh chalk paint',1.25,.103)
    painted_word(f,c,7.22,w*.90,'BOOP','seventh faded green',1.16,.107)
    painted_word(f,c,7.22,w*.80,'BOOP','seventh tar paint',1.02,.111)
    paint_strokes(f,.13,w-.07,4.04,5.77,717,.103,31,['seventh blue paint','seventh faded pink'])
    paint_strokes(f,L*.71,L*.98,3.81,6.20,127,.023,10,['seventh chalk paint'])
    wear(f,.10,w,3.62,16.25,'sill patina',220,.106,726)
    for ss in [L*.36,L*.60]:conduit(f,ss,3.46,16.17,'black iron',.065)


def ground_return(f,profile):
    if profile=='saifee-corner':saifee_return(f)
    elif profile=='deli':deli_return(f)
    elif profile=='smoke':
        # Short shop return, followed by poster cases, blind mural panel and 86 door.
        end=f.L*.225
        OPENINGS[frontage_key(f)].append((.05,.17,end,3.78))
        shop_room(f,.05,end,3.64,'smoke')
        glass_opening(f,.09,end-.06,.30,2.73,'window frame',False,.02,'black iron',2)
        fascia(f,.02,end,'E SMOKE & CONVENIENCE','smoke')
        for i,t in enumerate(['ICE CREAM','MILK','CIGAR','VAPE','BEER','LOTTO','EGGS']):
            ctext(f,.15+(end-.30)*(i+.5)/7,2.47,(end-.35)/7,t,'sign white',.105,.087)
        for j in range(5):food_decal(f,.37+j*(end-.65)/5,1.30,.32,.48,.085)
        for a,b in [(f.L*.245,f.L*.405),(f.L*.425,f.L*.645)]:
            f.b((a+b)/2,1.64,.021,b-a,2.90,.066,'black iron')
            if a<f.L*.3:
                for i in range(3):framed_notice(f,a+(b-a)*(i+.5)/3,1.63,(b-a)/3-.09,2.10,'',paper=['seventh aged olive','shop burgundy','seventh tar paint'][i],d=.068)
            else:paint_strokes(f,a+.09,b-.09,.32,2.96,737,.067,42,['seventh sky paint','seventh faded pink','seventh chalk paint','seventh tar paint'])
        doorway(f,f.L*.704,'86',False,'black iron')
        conduit(f,f.L*.72,.3,16.4,'black iron',.1)
        masonry_age(f,3.8,16.5,607)
    else:_old_ground_return(f,profile)


def burger_front(f,a,b):
    _old_burger_front(f,a,b)
    projecting_sign(f,a,b,{'at':.11,'y':3.58,'width':.63,'height':.66,'material':'seventh red enamel','lines':[{'text':'7TH','size':.20},{'text':'STREET','y':-.19,'size':.13},{'text':'BURGER','y':-.38,'size':.12}]})
    for s in [a+.03,b-.03]:f.line((s,3.24,.02),(s,3.63,.11),.011,'black iron')
    # Red outdoor dining structure visible in April; fit the observed feature
    # to the retained sidewalk width, keeping a pedestrian gap beside the shop.
    lo=a+.60;hi=b-.40;d=2.45
    for ss in [lo,hi]:
        for dd in [d-.64,d+.64]:f.b(ss,1.06,dd,.062,1.78,.064,'seventh red enamel')
        f.b(ss,.68,d,.065,.95,1.34,'seventh red enamel')
        f.line((ss,1.92,d-.68),(ss,1.92,d+.68),.035,'seventh red enamel')
    f.b((lo+hi)/2,.68,d+.64,hi-lo,.95,.06,'seventh red enamel')
    for yy in [.25,1.14,1.92]:f.b((lo+hi)/2,yy,d+.64,hi-lo+.10,.065,.067,'seventh red enamel')
    for ss in [lo+(hi-lo)/3,lo+2*(hi-lo)/3]:f.b(ss,1.54,d+.64,.055,.76,.055,'seventh red enamel')
    for ss in [lo+(hi-lo)*.27,lo+(hi-lo)*.73]:
        f.b(ss,.86,d,.62,.038,.54,'seventh tar paint')
        for dx in [-.21,.21]:f.line((ss+dx,.20,d),(ss+dx,.84,d),.018,'black iron')
        for dd in [d-.43,d+.40]:
            f.b(ss,.60,dd,.37,.035,.30,'seventh tar paint')
            for dx in [-.14,.14]:f.line((ss+dx,.18,dd),(ss+dx,.59,dd),.014,'black iron')


def yubu_front(f,a,b):
    _old_yubu_front(f,a,b)
    # Only shutter hardware and canopy seams are supported by the newer view;
    # retain the previously observed open-door state with that limit recorded.
    for i in range(8):f.b((a+b)/2,3.24+i*.046,.042,b-a-.07,.024,.16,'metal')
    for ss in [a+.07,b-.07]:f.b(ss,1.65,.073,.034,2.82,.082,'metal')


def corner_streets():
    _old_corner_streets()
    owner('First & Seventh / April 2026 street hardware; positions estimated')
    # Long NYC traffic mast arms, distinct from the small curved lamp brackets.
    for px,pz,direction in [(-11.8,220.9,1),(12.0,235.4,-1)]:
        f=Facade(px,pz,1,0,1)
        mast=[(0,5.25,0),(.38*direction,5.52,0),(1.4*direction,5.61,0),(7.5*direction,5.46,0)]
        for a,b in zip(mast,mast[1:]):f.line(a,b,.044,'metal')
        f.line((.04,5.84,.01),(7.5*direction,5.52,.01),.008,'metal')
        s=7.35*direction
        f.b(s,5.00,.06,.27,.87,.30,'yellow paint')
        for j in range(3):
            yy=5.26-j*.26
            rod(f.p(s,yy,.22),f.p(s,yy,.30),.096,'black iron',12)
            rod(f.p(s,yy,.303),f.p(s,yy,.309),.074,'seventh green light' if j==2 else 'shop burgundy',12)
        f.b(direction*2.0,5.33,.045,1.40,.36,.049,'store teal')
        ctext(f,direction*2.0,5.33,1.22,'E 7 St','sign white',.25,.073)
    # Utility lids, bolt heads and inset grates: flush with the existing surfaces.
    for x,z,r in [(-8.2,222.0,.47),(8.7,235.0,.39),(-5.2,228,.42),(2.2,232,.44)]:
        f=Facade(x,z,1,0,1)
        rod(f.p(0,.003,0),f.p(0,.012,0),r,'seventh oxidized iron',40)
        for k in range(12):
            a=k*math.tau/12;b=(k+1)*math.tau/12
            f.line((math.cos(a)*r*.89,.017,math.sin(a)*r*.89),(math.cos(b)*r*.89,.017,math.sin(b)*r*.89),.007,'metal')
        for i in range(-4,5):
            yy=i*r*.16;length=math.sqrt(max(0,(r*.79)**2-yy*yy))
            if length:f.line((-length,.018,yy),(length,.018,yy),.006,'seventh tar paint')


_unbatched_corner_flush=flush


def flush():
    """Keep opaque paint colors in vertex data rather than extra draw calls.

    Only the authored matte corner paints are combined. Glass, emissive signs,
    metallic iron and photographed generic masonry surface maps remain distinct.
    """
    _unbatched_corner_flush()
    palette={'seventh aged olive','seventh garden green','seventh garden canvas',
             'seventh blue paint','seventh sky paint','seventh chalk paint',
             'seventh faded green','seventh faded pink','seventh tar paint',
             'seventh soil sack','seventh white sack','seventh curb ramp','seventh canvas brown','seventh hen ochre'}
    selected=[]
    for obj in list(bpy.context.scene.objects):
        if obj.type not in ['FONT','MESH'] or not len(obj.data.materials):continue
        source=obj.data.materials[0]
        if source.name not in palette:continue
        color=tuple(source.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value)
        if obj.type=='FONT':
            bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
            bpy.ops.object.convert(target='MESH')
        if not obj.data.loops:continue
        if 'seventh painted color batch' not in MATS:
            material('seventh painted color batch',(1,1,1),.92)
            m=MATS['seventh painted color batch'];v=m.node_tree.nodes.new('ShaderNodeVertexColor');v.layer_name='Color'
            m.node_tree.links.new(v.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
        attr=obj.data.color_attributes.new(name='Color',type='FLOAT_COLOR',domain='CORNER')
        attr.data.foreach_set('color',list(color)*len(attr.data))
        obj.data.materials.clear();obj.data.materials.append(MATS['seventh painted color batch'])
        for polygon in obj.data.polygons:polygon.material_index=0
        selected.append(obj)
    if len(selected)>1:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in selected:obj.select_set(True)
        bpy.context.view_layer.objects.active=selected[0];bpy.ops.object.join()
