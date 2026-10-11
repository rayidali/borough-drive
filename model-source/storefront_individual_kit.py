"""Opt-in business detail for First Avenue / St. Marks revision 09.

Installed by the engine exporter after the historical facade kits. Only records
with detail09 use this path; existing Seventh/core/legacy recipes stay unchanged.
All placements come from the authored business packet, never a seeded shop type.
"""
from mathutils import Matrix

SHOP09_MATERIALS = {
    'cream enamel': ((.79,.75,.65),1), 'white enamel': ((.88,.87,.81),1),
    'black enamel': ((.055,.067,.064),1), 'red enamel': ((.48,.055,.035),1),
    'maroon enamel': ((.28,.065,.055),1), 'sage enamel': ((.26,.32,.24),1),
    'teal enamel': ((.035,.22,.24),1), 'navy enamel': ((.035,.08,.12),1),
    'blue enamel': ((.03,.20,.40),1), 'orange enamel': ((.79,.25,.045),1),
    'oak timber': ((.33,.23,.14),2), 'honey timber': ((.46,.34,.23),2),
    'dark timber': ((.16,.105,.065),2), 'white tile': ((.85,.84,.77),3),
    'green tile': ((.075,.24,.18),3), 'red tile': ((.43,.10,.055),3),
    'black tile': ((.045,.055,.047),3), 'pink plaster': ((.63,.49,.41),4),
    'gray plaster': ((.34,.35,.32),4), 'linen canvas': ((.69,.64,.51),5),
    'cream canvas': ((.82,.79,.69),5), 'black canvas': ((.055,.065,.05),5),
    'olive canvas': ((.20,.22,.13),5), 'maroon canvas': ((.34,.045,.05),5),
    'orange canvas': ((.91,.40,.09),5), 'red canvas': ((.55,.07,.045),5),
    'brushed steel': ((.43,.47,.47),6), 'aged brass': ((.52,.38,.16),6),
    'dark iron': ((.055,.065,.058),6), 'chalkboard': ((.025,.04,.035),7),
    'paper': ((.87,.83,.70),8), 'printed red': ((.55,.06,.045),8),
    'printed blue': ((.055,.17,.32),8), 'printed green': ((.17,.36,.14),8),
    'warm white': ((.92,.84,.64),8), 'bottle green': ((.065,.21,.08),1),
    'purple canvas': ((.27,.12,.31),5), 'green enamel': ((.075,.24,.18),1),
    'lime enamel': ((.35,.64,.10),1),
    'yellow enamel': ((.85,.66,.17),1), 'rose enamel': ((.63,.38,.43),1),
}
for key,(color,surface) in SHOP09_MATERIALS.items():
    name='store09 '+key
    material(name,color,.65 if surface in [1,3] else .90)
    MATS[name]['storefront09Surface']=surface
material('store09 clear glass',(.83,.88,.85),.19)
MATS['store09 clear glass'].node_tree.nodes.get('Principled BSDF').inputs['Alpha'].default_value=.18
MATS['store09 clear glass']['storefront09Glass']=True

SHOP09_FONTS={
 'condensed':bpy.data.fonts.load(str(ROOT/'model-source/fonts/storefront-09/BarlowCondensed-SemiBold.ttf')),
 'narrow':bpy.data.fonts.load(str(ROOT/'model-source/fonts/storefront-09/BebasNeue-Regular.ttf')),
 'serif':bpy.data.fonts.load(str(ROOT/'model-source/fonts/storefront-09/BoroughStoreSerif.ttf')),
 'bold':bpy.data.fonts.load(str(ROOT/'model-source/fonts/storefront-09/BoroughStoreSans.ttf')),
 'script':SIGN_FONT,
}

_shop09_sign_text=sign_text
def sign_text(f,s,y,w,text,mat,size=.28,d=.3,style='plain'):
    if not style.startswith('store09:'):
        return _shop09_sign_text(f,s,y,w,text,mat,size,d,style)
    if not text:return
    parts=style.split(':');font=parts[1]
    curve=bpy.data.curves.new('Individual business lettering','FONT')
    curve.body=text;curve.font=SHOP09_FONTS[font];curve.size=size
    curve.align_x='CENTER';curve.align_y='CENTER';curve.resolution_u=3;curve.extrude=.0015
    curve.space_character=float(parts[2]) if len(parts)>2 else 1.0
    if len(parts)>3:curve.shear=float(parts[3])
    obj=bpy.data.objects.new(ns['OWNER']+' / business lettering / '+text,curve)
    bpy.context.collection.objects.link(obj)
    x,yy,z=f.p(s,y,d);obj.location=(x,-z,yy)
    obj.rotation_euler=Matrix((Vector((f.rx,-f.rz,0)),Vector((0,0,1)),Vector((f.nx,-f.nz,0)))).transposed().to_euler()
    obj.data.materials.append(MATS[mat]);bpy.context.view_layer.update()
    width=max(v[0] for v in obj.bound_box)-min(v[0] for v in obj.bound_box)
    if width>w and width>0:curve.size*=w/width
    return obj

_shop09_sign_panel=sign_panel
def sign_panel(f,s,y,w,h,depth,mat,shape='rectangle'):
    if shape!='store09-arch':return _shop09_sign_panel(f,s,y,w,h,depth,mat,shape)
    spring=y-h*.06
    pts=[(s-w/2,y-h/2),(s+w/2,y-h/2),(s+w/2,spring)]
    pts.extend((s+w/2*math.cos(j*math.pi/24),spring+h*.62*math.sin(j*math.pi/24)) for j in range(1,25))
    face([f.p(x,yy,depth+.05) for x,yy in pts],mat)
    for aa,bb in zip(pts,pts[1:]+pts[:1]):
        face([f.p(*aa,depth-.05),f.p(*bb,depth-.05),f.p(*bb,depth+.05),f.p(*aa,depth+.05)],mat)
        f.line((*aa,depth+.06),(*bb,depth+.06),.018,'store09 aged brass')

def shop09_frame(f,s,y,w,h,d,mat,rail=.045):
    for x in [s-w/2,s+w/2]:f.b(x,y,d,rail,h+rail,.065,mat)
    for yy in [y-h/2,y+h/2]:f.b(s,yy,d,w,rail,.065,mat)

def shop09_arch(f,left,right,bottom,top,d,mat,surround,round_top=False):
    w=right-left;s=(left+right)/2
    if not round_top:
        f.b(s,(bottom+top)/2,d,w,top-bottom,.018,mat)
        return
    rise=min(w*.5,(top-bottom)*.34);spring=top-rise
    pts=[f.p(left,bottom,d),f.p(right,bottom,d),f.p(right,spring,d)]
    for j in range(1,25):
        t=j*math.pi/24;pts.append(f.p(s+w/2*math.cos(t),spring+rise*math.sin(t),d))
    face(pts,mat)
    for j in range(24):
        ta=j*math.pi/24;tb=(j+1)*math.pi/24
        aa=(s+w/2*math.cos(ta),spring+rise*math.sin(ta));bb=(s+w/2*math.cos(tb),spring+rise*math.sin(tb))
        face([f.p(*aa,d+.04),f.p(*bb,d+.04),f.p(bb[0],top+.025,d+.04),f.p(aa[0],top+.025,d+.04)],surround)
        f.line((*aa,d+.07),(*bb,d+.07),.034,surround)

def shop09_furniture(f,s,d,item):
    """Furniture anatomy is selected explicitly per observed placement."""
    kind=item['kind'];mat=item.get('material','store09 oak timber')
    floor=item.get('floor',.17);height=item.get('height',.72)+floor
    if kind in ['round-table','square-table','high-table']:
        width=item.get('width',.58)
        if kind=='round-table':rod(f.p(s,height-.035,d),f.p(s,height,d),width/2,mat,20)
        else:f.b(s,height-.02,d,width,.045,item.get('length',width),mat)
        leg=item.get('legs','pedestal')
        if leg=='pedestal':
            f.line((s,floor+.04,d),(s,height-.04,d),.037,'store09 dark iron')
            for ds,dd in [(-.24,0),(.24,0),(0,-.24),(0,.24)]:f.line((s,floor+.075,d),(s+ds,floor+.035,d+dd),.025,'store09 dark iron')
        else:
            for side in [-1,1]:
                f.line((s-.23,floor,d+side*.20),(s+.23,height,d+side*.20),.015,'store09 dark iron')
                f.line((s+.23,floor,d+side*.20),(s-.23,height,d+side*.20),.015,'store09 dark iron')
    elif kind in ['chair','stool']:
        yaw=item.get('yaw',0);ca=math.cos(yaw);sa=math.sin(yaw)
        def p(x,y,z):return (s+x*ca+z*sa,y,d-x*sa+z*ca)
        seat=floor+item.get('seat',.45)
        for k in range(5):
            aa=p(-.19,seat,(k-2)*.075);bb=p(.19,seat,(k-2)*.075)
            f.line(aa,bb,.022,mat)
        for x in [-.16,.16]:
            for z in [-.16,.16]:f.line(p(x*1.12,floor,z*1.12),p(x,seat,z),.016,mat)
        if kind=='chair':
            profile=item.get('profile','slat')
            for x in [-.17,.17]:f.line(p(x,seat,-.17),p(x,seat+.43,-.23),.017,mat)
            if profile=='wishbone':
                for j in range(14):
                    a=math.pi*j/14;b=math.pi*(j+1)/14
                    f.line(p(.24*math.cos(a),seat+.32,-.08-.20*math.sin(a)),p(.24*math.cos(b),seat+.32,-.08-.20*math.sin(b)),.020,mat)
                for side in [-1,1]:f.line(p(0,seat+.04,-.18),p(side*.12,seat+.32,-.24),.014,mat)
            elif profile=='mesh':
                for j in range(7):f.line(p(-.18+j*.06,seat+.08,-.20),p(-.18+j*.06,seat+.38,-.23),.007,mat)
                for j in range(6):f.line(p(-.18,seat+.08+j*.06,-.20),p(.18,seat+.08+j*.06,-.20),.007,mat)
            else:
                for yy in [.22,.34]:f.line(p(-.19,seat+yy,-.22),p(.19,seat+yy,-.22),.027,mat)
    elif kind=='bench':
        width=item.get('width',1.25)
        for j in range(4):f.b(s,floor+.44,d+(j-1.5)*.10,width,.04,.085,mat)
        for x in [-width*.4,width*.4]:
            for z in [-.14,.14]:f.line((s+x,floor,d+z),(s+x,floor+.42,d+z),.025,'store09 dark iron')
        if item.get('back'):
            for y in [.69,.81,.93]:f.b(s,floor+y,d-.20,width,.07,.04,mat)
    elif kind in ['umbrella','closed-umbrella']:
        height=floor+item.get('height',2.4);rad=item.get('radius',1.0)
        rod(f.p(s,floor,d),f.p(s,floor+.06,d),.25,'store09 dark iron',16)
        f.line((s,floor,d),(s,height+.13,d),.025,item.get('pole','store09 dark iron'))
        if kind=='closed-umbrella':
            for j in range(12):
                a=j*math.tau/12;b=(j+1)*math.tau/12
                face([f.p(s,height+.10,d),f.p(s+.12*math.cos(a),height-.35,d+.12*math.sin(a)),f.p(s+.12*math.cos(b),height-.35,d+.12*math.sin(b))],mat)
                face([f.p(s+.12*math.cos(a),height-.35,d+.12*math.sin(a)),f.p(s+.07*math.cos(a),height-1.10,d+.07*math.sin(a)),f.p(s+.07*math.cos(b),height-1.10,d+.07*math.sin(b)),f.p(s+.12*math.cos(b),height-.35,d+.12*math.sin(b))],mat)
        else:
            for j in range(8):
                a=j*math.tau/8;b=(j+1)*math.tau/8
                aa=(s+rad*math.cos(a),height-.30,d+rad*math.sin(a));bb=(s+rad*math.cos(b),height-.30,d+rad*math.sin(b))
                face([f.p(s,height,d),f.p(*aa),f.p(*bb)],mat)
                f.line((s,height-.014,d),aa,.009,'store09 aged brass')
    elif kind in ['planter','barrel']:
        width=item.get('width',.50);height=item.get('height',.45)
        if kind=='barrel':
            rod(f.p(s,floor,d),f.p(s,floor+height,d),width/2,mat,16)
            for yy in [floor+.08,floor+height-.08]:
                for j in range(16):
                    a=j*math.tau/16;b=(j+1)*math.tau/16
                    f.line((s+width/2*math.cos(a),yy,d+width/2*math.sin(a)),(s+width/2*math.cos(b),yy,d+width/2*math.sin(b)),.016,'store09 dark iron')
        else:
            f.b(s,floor+height/2,d,width,height,item.get('length',width),mat)
            f.b(s,floor+height+.01,d,width+.04,.035,item.get('length',width)+.04,mat)
        # Explicit planter location; foliage is an estimated surface silhouette.
        for j in range(item.get('stems',9)):
            angle=j*2.399;x=math.cos(angle)*width*.37;z=math.sin(angle)*width*.37;h=.24+(j%3)*.10
            f.line((s,floor+height,d),(s+x,floor+height+h,d+z),.008,'store09 bottle green')
            for side in [-1,1]:
                face([f.p(s+x,floor+height+h*.5,d+z),f.p(s+x+side*.10,floor+height+h*.72,d+z+.04),f.p(s+x,floor+height+h,d+z)],'store09 bottle green')

def shop09_display(f,a,b,low,top,item):
    s=a+(b-a)*item.get('at',.5);w=(b-a)*item.get('width',.65)
    y=item.get('y',1.25);d=item.get('depth',-.28);kind=item['kind']
    if kind in ['books','bottles','jars','produce','optical','laundry','shelves']:
        rows=item.get('rows',2);count=item.get('count',6);step=item.get('rowStep',.37)
        for row in range(rows):
            yy=y+row*step
            f.b(s,yy-.035,d,w,.045,.25,item.get('shelf','store09 honey timber'))
            for k in range(count):
                x=s-w*.45+w*.9*(k+.5)/count
                color=item.get('colors',['store09 printed green','store09 paper','store09 printed red'])[k%len(item.get('colors',['store09 printed green','store09 paper','store09 printed red']))]
                if kind=='books':
                    hh=.18+.045*(k%3);ww=min(.07,w/count*.64)
                    f.b(x,yy+hh/2,d+.045,ww,hh,.13,color)
                    f.b(x,yy+hh*.66,d+.116,ww*.7,.012,.005,'store09 paper')
                elif kind in ['bottles','jars']:
                    hh=.17 if kind=='bottles' else .13
                    rod(f.p(x,yy,d),f.p(x,yy+hh,d),.035,color,8)
                    rod(f.p(x,yy+hh,d),f.p(x,yy+hh+(.065 if kind=='bottles' else .018),d),.016 if kind=='bottles' else .039,color,8)
                    f.b(x,yy+hh*.5,d+.037,.045,.07,.006,'store09 paper')
                elif kind=='produce':
                    f.b(x,yy+.09,d,.16,.16,.19,color)
                    f.b(x,yy+.02,d+.12,.18,.03,.03,'store09 honey timber')
                elif kind=='optical':
                    for dx in [-.04,.04]:
                        for j in range(12):
                            t=j*math.tau/12;u=(j+1)*math.tau/12
                            f.line((x+dx+.033*math.cos(t),yy+.08+.025*math.sin(t),d+.07),(x+dx+.033*math.cos(u),yy+.08+.025*math.sin(u),d+.07),.005,'store09 dark iron')
                    f.line((x-.012,yy+.08,d+.07),(x+.012,yy+.08,d+.07),.005,'store09 dark iron')
                elif kind=='laundry':
                    f.b(x,yy+.35,d,.52,.65,.40,'store09 white enamel')
                    rod(f.p(x,yy+.35,d+.208),f.p(x,yy+.35,d+.245),.20,'store09 brushed steel',20)
                    rod(f.p(x,yy+.35,d+.25),f.p(x,yy+.35,d+.258),.145,'dark glass',20)
    elif kind=='poster':
        height=item.get('height',.52);paper=item.get('material','store09 paper')
        f.b(s,y,d,w,height,.012,paper)
        if item.get('text'):sign_text(f,s,y+height*.24,w*.86,item['text'],item.get('ink','store09 printed blue'),min(.13,height*.16),d+.009,item.get('font','store09:condensed'))
        if item.get('layout','lines')=='grid':
            for row in range(4):
                for col in range(3):f.b(s+(col-1)*w*.27,y+height*.22-row*height*.16,d+.010,w*.21,height*.12,.004,['store09 printed red','store09 printed green','store09 printed blue'][(row+col)%3])
        else:
            for j in range(5):f.b(s,y+height*.06-j*height*.105,d+.010,w*(.62 if j%2 else .78),.010,.004,item.get('ink','store09 printed blue'))
    elif kind=='blind':
        height=item.get('height',1.5)
        for j in range(int(height/.045)):f.b(s,y+height/2-j*.045,d,w,.028,.03,item.get('material','store09 honey timber'))
        for dx in [-w*.28,w*.28]:f.b(s+dx,y,d+.02,.008,height,.006,'store09 cream canvas')
    elif kind=='pendant':
        f.line((s,top-.05,d),(s,y+.12,d),.008,'store09 dark iron')
        rod(f.p(s,y-.06,d),f.p(s,y+.10,d),.09,item.get('material','opal lamp'),12)
    elif kind=='counter':
        f.b(s,y-.08,d,w,.13,item.get('depthSize',.40),item.get('material','store09 dark timber'))
    elif kind=='cloth':
        height=item.get('height',1.2)
        for j in range(10):f.b(s-w/2+w*(j+.5)/10,y,d+.015*(j%2),w/10+.005,height,.024,item.get('material','store09 red canvas'))

def shop09_ink(f,a,b,low,high,ink,depth=.23,variant='outline',color=None,fill=None):
    # Separate interpretations of the observed mark families. These contours
    # deliberately do not spell invented tags; exact artwork remains uncertain.
    paths={
      'vacant-outline':[
        [(0,.10),(.03,.66),(.12,.93),(.20,.85),(.23,.54),(.17,.24),(.12,.12),(.06,.22),(.10,.67),(.28,.72)],
        [(.23,.15),(.33,.80),(.41,.94),(.48,.85),(.44,.28),(.34,.05),(.31,.24),(.52,.32)],
        [(.50,.08),(.56,.88),(.65,.77),(.61,.41),(.74,.92),(.80,.79),(.77,.30),(.69,.11)],
        [(.76,.13),(.81,.65),(.91,.89),(.98,.68),(.95,.34),(.84,.13),(.78,.15)],
      ],
      'bubble':[
        [(.01,.28),(.04,.64),(.13,.89),(.23,.94),(.27,.78),(.24,.41),(.18,.15),(.06,.06),(.01,.28)],
        [(.23,.22),(.28,.69),(.36,.85),(.46,.76),(.46,.48),(.41,.37),(.48,.24),(.43,.05),(.29,.04),(.23,.22)],
        [(.44,.23),(.51,.77),(.58,.94),(.63,.87),(.64,.50),(.73,.84),(.80,.90),(.83,.72),(.76,.15),(.66,.06),(.60,.25),(.53,.05),(.44,.23)],
        [(.77,.17),(.83,.70),(.91,.94),(.97,.88),(1,.66),(.94,.41),(.86,.31),(.97,.24),(.92,.06),(.77,.17)],
      ],
      'ghost':[
        [(.07,.20),(.13,.75),(.24,.84),(.27,.67),(.18,.44),(.37,.43),(.32,.18)],
        [(.31,.31),(.43,.69),(.50,.58),(.46,.24),(.60,.59),(.68,.60),(.60,.31),(.78,.30),(.86,.61)],
        [(.07,.09),(.80,.06),(.91,.17)],
      ],
      'collage':[
        [(.01,.12),(.09,.89),(.18,.81),(.12,.46),(.24,.52),(.27,.20),(.12,.09),(.10,.32),(.31,.63)],
        [(.18,.89),(.35,.96),(.40,.82),(.29,.78),(.25,.51),(.38,.42),(.42,.18),(.30,.04)],
        [(.38,.24),(.46,.77),(.54,.93),(.57,.58),(.51,.20),(.46,.23),(.52,.62),(.67,.76),(.70,.53),(.58,.16)],
        [(.65,.06),(.72,.94),(.76,.50),(.89,.93),(.93,.72),(.85,.21),(.80,.14),(.91,.08)],
        [(.01,.70),(.22,.73),(.30,.64),(.38,.72),(.62,.87),(.72,.86),(.83,.64),(1,.67)],
      ]}
    paths=paths.get(variant,paths['bubble'])
    # Smooth the curved shutter tags; keep the vacant angular strokes crisp.
    for j,pts in enumerate(paths):
        if variant in ['bubble','outline']:
            for _ in range(2):
                smooth=[]
                for p,q in zip(pts,pts[1:]):smooth.extend([(.75*p[0]+.25*q[0],.75*p[1]+.25*q[1]),(.25*p[0]+.75*q[0],.25*p[1]+.75*q[1])])
                pts=[pts[0],*smooth,pts[-1]]
        mat=ink if not color or j%2 else color
        if variant=='collage':
            # Interleaved broad silver/blue paint, thin dark outlines and drips.
            mat=['store09 paper','store09 printed blue','store09 black enamel','store09 printed red','store09 paper'][j]
        radius=.020 if variant in ['bubble','vacant-outline'] else .007 if variant=='ghost' else .023
        if fill:face([f.p(a+p[0]*(b-a),low+p[1]*(high-low),depth+.015+j*.001) for p in pts],fill)
        for p,q in zip(pts,pts[1:]):
            aa=(a+p[0]*(b-a),low+p[1]*(high-low),depth+.018+j*.001)
            bb=(a+q[0]*(b-a),low+q[1]*(high-low),depth+.018+j*.001)
            f.line(aa,bb,radius,mat)
        if variant=='collage':
            for k,p in enumerate(pts[1::2]):
                xx=a+p[0]*(b-a);yy=low+p[1]*(high-low)
                f.line((xx,yy,depth+.022),(xx+.02,yy-.06-(k%3)*.027,depth+.022),.006,mat)

def shop09_special(f,a,b,low,top,detail):
    w=b-a
    if detail.get('corrugatedSides'):
        for l,r in [(a,a+w*.32),(a+w*.62,b)]:
            f.b((l+r)/2,(low+2.65)/2,.13,r-l,2.65-low,.045,'store09 brushed steel')
            for j in range(int((2.65-low)/.065)):f.b((l+r)/2,low+j*.065,.167,r-l,.018,.018,'store09 gray plaster')
    if detail.get('lattice'):
        # Diamond trellis above each projecting timber display.
        l=a+.09;r=b-.09;y0=1.72;y1=2.62
        for slope in [-1,1]:
            for j in range(int((r-l+y1-y0)/.18)+1):
                x=l-(y1-y0)+j*.18
                pts=[]
                for yy in [y0,y1]:
                    xx=x+(yy-y0)*slope
                    if l<=xx<=r:pts.append((xx,yy,.19))
                for xx in [l,r]:
                    yy=y0+(xx-x)/slope
                    if y0<yy<y1:pts.append((xx,yy,.19))
                if len(pts)>=2:f.line(pts[0],pts[1],.010,'store09 honey timber')
        for at in [.18,.78]:shop09_furniture(f,a+w*at,.29,{'kind':'planter','floor':1.23,'height':.18,'width':.42,'length':.26,'material':'store09 dark timber','stems':6})
    if g:=detail.get('graffiti'):
        lo,hi=g['band'];shop09_ink(f,a+.10,b-.10,lo,hi,g['ink'],variant=g.get('variant','collage' if g.get('fascia') else 'outline'),color=g.get('color'))
        if g.get('fascia'):shop09_ink(f,a,b,top-.25,top+.20,g['ink'],depth=.31,variant='collage',color=g.get('color'))
    for layer in detail.get('paintLayers',[]):
        lo,hi=layer['band'];left,right=layer['span']
        shop09_ink(f,a+w*left,a+w*right,lo,hi,layer['ink'],depth=layer.get('depth',.23),variant=layer['variant'],fill=layer.get('fill'))
    if detail.get('checkerPiers'):
        for edge in [a+.085,b-.085]:
            for j in range(int((top-low)/.23)):f.b(edge,low+.115+j*.23,.23,.17,.22,.025,['store09 printed green','store09 paper','store09 printed red','store09 blue enamel'][j%4])
        for j in range(int(w/.24)):f.b(a+.12+j*.24,low+.18,.23,.23,.28,.025,['store09 printed green','store09 paper','store09 printed red'][j%3])
    for star in detail.get('crifStars',[]):
        ss=a+w*star['at'];yy=star['y'];rad=star['radius'];dd=star['depth']
        pts=[f.p(ss+rad*(1 if k%2==0 else .42)*math.sin(k*math.pi/5),yy+rad*(1 if k%2==0 else .42)*math.cos(k*math.pi/5),dd) for k in range(10)]
        face(pts,'store09 warm white')
    if detail.get('paintedLeaves'):
        for at,lean in [(.12,.16),(.29,-.10),(.69,.12),(.85,-.14)]:
            ss=a+w*at
            f.line((ss,.25,.22),(ss+lean,.69,.22),.007,'store09 sage enamel')
            for j in range(4):
                yy=.32+j*.085;xx=ss+lean*(yy-.25)/.44
                for side in [-1,1]:
                    face([f.p(xx,yy,.225),f.p(xx+side*.11,yy+.02,.225),f.p(xx+side*.16,yy+.12,.225),f.p(xx+side*.04,yy+.07,.225)],'store09 sage enamel')
    if detail.get('dumplingLogo'):
        # Plump cream dumpling silhouette and folded crown on the projecting sign.
        at=a+w*.86;y=2.38
        f.line((at,y+.25,.08),(at,y+.25,.85),.022,'store09 dark iron')
        side=Facade(*[v for v in (f.p(at,0,.18)[0],f.p(at,0,.18)[2],f.nx,f.nz,.72)])
        for normal in [.04,-.04]:
            points=[side.p(.36+.30*math.cos(j*math.tau/32),y+.23*math.sin(j*math.tau/32),normal) for j in range(32)]
            face(points,'store09 paper')
            for eye in [.26,.46]:rod(side.p(eye,y+.03,normal),side.p(eye,y+.03,normal+(.015 if normal>0 else -.015)),.021,'store09 black enamel',10)
            for j in range(5):side.line((.18+j*.09,y+.12,normal),(.21+j*.075,y+.22,normal),.012,'store09 printed red')
    if detail.get('romeoGraphics'):
        red='store09 printed red'
        # Red fluted column drawings in the cream piers.
        for at in [.03,.35,.96]:
            s=a+w*at
            for dx in [-.07,-.023,.023,.07]:f.line((s+dx,.35,.24),(s+dx,2.62,.24),.009,red)
            for yy in [.33,.43,2.57,2.67]:f.b(s,yy,.241,.23,.012,.008,red)
        for at in [.15,.77]:
            s=a+w*at;y=.56
            cat=[(-.24,-.06),(-.15,.10),(-.20,.36),(-.11,.28),(.02,.34),(.10,.46),(.12,.23),(.21,.09),(.22,-.06),(-.24,-.06)]
            for p,q in zip(cat,cat[1:]):f.line((s+p[0],y+p[1],.23),(s+q[0],y+q[1],.23),.011,red)
        for at in [.20,.62,.85]:
            s=a+w*at;y=3.10
            pts=[(0,-.12),(-.11,.01),(-.10,.09),(-.035,.105),(0,.05),(.035,.105),(.10,.09),(.11,.01),(0,-.12)]
            for p,q in zip(pts,pts[1:]):f.line((s+p[0],y+p[1],.33),(s+q[0],y+q[1],.33),.010,red)

_shop09_previous_awning=observed_awning
def observed_awning(f,a,b,aw):
    if not aw.get('detail09'):return _shop09_previous_awning(f,a,b,aw)
    aw=dict(aw);text=aw.pop('text','');style=aw.pop('font','store09:condensed')
    y=aw.get('y',3.10);drop=aw.get('drop',.50);depth=aw.get('depth',1.12);valance=aw.get('valance',.20)
    mat=aw.get('material','store09 black canvas');inset=(b-a)*aw.get('inset',0);a+=inset;b-=inset
    sections=16 if aw.get('shape')=='round' else 1
    def pt(s,t):
        if sections>1:return f.p(s,y-drop*(1-math.cos(t*math.pi/2)),.10+depth*math.sin(t*math.pi/2))
        return f.p(s,y-drop*t,.10+depth*t)
    if aw.get('horizontalStripes'):
        for j in range(9):face([pt(a,(j+1)/9),pt(b,(j+1)/9),pt(b,j/9),pt(a,j/9)],'store09 cream canvas' if j%2 else mat)
        f.b((a+b)/2,y-drop-valance/2,.10+depth,b-a,valance,.032,mat)
    else:
        count=max(1,math.ceil((b-a)/aw.get('stripeSpacing',.24)))
        for k in range(count):
            l=a+(b-a)*k/count;r=a+(b-a)*(k+1)/count
            sw=min(aw.get('stripeWidth',.06),(r-l)*.95)
            bands=[(l,r,mat)] if not aw.get('stripe') else [(l,l+sw,aw['stripe']),(l+sw,r,mat)]
            for left,right,color in bands:
                for j in range(sections):face([pt(left,(j+1)/sections),pt(right,(j+1)/sections),pt(right,j/sections),pt(left,j/sections)],color)
                f.b((left+right)/2,y-drop-valance/2,.10+depth,right-left,valance,.032,color)
    if aw.get('scalloped'):
        count=max(1,round((b-a)/.22))
        for k in range(count):
            center=a+(b-a)*(k+.5)/count;radius=(b-a)/count/2
            for j in range(8):
                t=j*math.pi/8;u=(j+1)*math.pi/8
                face([f.p(center,y-drop-valance,.12+depth),f.p(center+math.cos(t)*radius,y-drop-valance-.055*math.sin(t),.12+depth),f.p(center+math.cos(u)*radius,y-drop-valance-.055*math.sin(u),.12+depth)],mat)
    for edge in [a,b]:
        if aw.get('sidePanels',True):face([f.p(edge,y,.10),f.p(edge,y-drop,.10+depth),f.p(edge,y-drop,.10)],mat)
        for u,v in [((edge+.015,y-.02,.10),(edge+.015,y-drop-.04,.10+depth)),((edge+.015,y-.35,.10),(edge+.015,y-drop-.04,.10+depth))]:f.line(u,v,.017,'store09 dark iron')
    f.line((a,y-drop-.03,.10+depth),(b,y-drop-.03,.10+depth),.020,'store09 dark iron')
    sign_text(f,a+(b-a)*aw.get('textAt',.5),y-drop-valance*.50,(b-a)*aw.get('textWidth',.92),text,aw.get('letters','store09 warm white'),aw.get('textSize',.21),depth+.137,style)
    if aw.get('topText'):
        angle=math.pi/3 if sections>1 else math.atan2(depth,drop)
        dd=.10+depth*(math.sin(angle) if sections>1 else .50)+.025
        obj=sign_text(f,(a+b)/2,y-drop*.50,(b-a)*.75,aw['topText'],aw.get('letters','store09 warm white'),aw.get('topTextSize',.22),dd,style)
        if obj:obj.rotation_euler=(obj.rotation_euler.to_matrix() @ Matrix.Rotation(angle-math.pi/2,3,'X')).to_euler()

_shop09_previous_shop=photographed_shop
def photographed_shop(f,a,b,r):
    spec=r['design'];detail=spec.get('detail09')
    if not detail:return _shop09_previous_shop(f,a,b,r)
    w=b-a;c=(a+b)/2
    if w<.75:return
    top=spec.get('top',3.3);head=spec.get('head',2.61);base=spec.get('base',.40)
    floor=detail.get('floor',-.46 if base<0 else .17)
    frame=detail.get('frame',spec.get('frame','store09 black enamel'))
    surround=detail.get('surround',frame);base_mat=detail.get('baseMaterial',surround)
    fw=detail.get('frameWidth',.06);pier=detail.get('pierWidth',.13);recess=spec.get('recess',.18)
    OPENINGS[frontage_key(f)].append((a,floor,b,top))
    # A shallow room shell only where visible cues exist; no unobserved room plan.
    back=-detail.get('displayDepth',.80)
    f.b(c,(top+floor)/2,back-.025,w,top-floor,.05,detail.get('backing','dark glass'))
    f.b(c,floor+.01,back/2,w,.045,-back,'store09 gray plaster')
    f.b(c,top-.04,back/2,w,.08,-back,surround)
    for edge in [a+pier/2,b-pier/2]:f.b(edge,(top+floor)/2,-.04,pier,top-floor,.34,surround)
    f.b(c,top-.09,.03,w,.18,.28,surround)
    for yy in [top-.015,top-.17]:f.b(c,yy,.205,w+.035,.025,.035,detail.get('trim',frame))
    left=a+pier;usable=w-2*pier
    for idx,(kind,fraction) in enumerate(spec['panels']):
        frame=detail.get('panelFrames',{}).get(str(idx),detail.get('frame',spec.get('frame','store09 black enamel')))
        right=left+usable*fraction;ww=right-left;ss=(left+right)/2
        door=kind in ['door','double-door'];dd=-recess if door else spec.get('windowDepth',.035)
        bottom=detail.get('doorSolidTop',floor+.55) if door else max(base,floor+.08)
        panel_head=spec.get('doorHead',head) if door else head
        round_top=idx in detail.get('archedPanels',[])
        glass_left=left+fw/2;glass_right=right-fw/2
        shop09_arch(f,glass_left,glass_right,bottom,panel_head,dd-.012,'store09 clear glass',surround,round_top)
        for edge in [left,right]:
            f.b(edge,(panel_head+floor)/2,dd+.035,fw,panel_head-floor,.13,frame)
            if detail.get('molding',True):f.b(edge-fw*.28,(panel_head+floor)/2,dd+.105,fw*.22,panel_head-floor,.025,detail.get('trim',frame))
        for yy in [bottom,panel_head]:f.b(ss,yy,dd+.035,ww,fw,.13,frame)
        f.b(ss,(bottom+floor)/2,dd+.035,ww,bottom-floor,.13,detail.get('doorMaterial',base_mat) if door else base_mat)
        if bottom-floor>.23 and detail.get('recessedBase',True):shop09_frame(f,ss,(bottom+floor)/2,ww-.15,bottom-floor-.14,dd+.115,frame,.022)
        if spec.get('transom',True) and top-panel_head>.18:
            f.b(ss,(top-.18+panel_head)/2,dd,ww,top-.18-panel_head,.014,'store09 clear glass')
            for y in [panel_head,top-.19]:f.b(ss,y,dd+.06,ww,fw,.10,frame)
        elif top>panel_head:f.b(ss,(top+panel_head)/2,dd+.035,ww,top-panel_head,.10,surround)
        for split in detail.get('rails',[]):f.b(ss,bottom+(panel_head-bottom)*split,dd+.06,ww,.035,.07,frame)
        if spec.get('smallPanes'):
            for j in range(1,4):f.b(ss,bottom+(panel_head-bottom)*j/4,dd+.06,ww,.032,.055,frame)
            f.b(ss,(panel_head+bottom)/2,dd+.06,.032,panel_head-bottom,.055,frame)
        if door:
            n=2 if kind=='double-door' else 1
            if n==2:f.b(ss,(panel_head+floor)/2,dd+.05,fw,panel_head-floor,.10,frame)
            for j in range(n):
                x=left+ww*(j+.5)/n;pull=x+ww/n*.30
                if detail.get('handle','pull')=='pull':
                    for yy in [floor+.89,floor+1.24]:f.line((pull,yy,dd+.07),(pull,yy,dd+.17),.012,detail.get('hardware','store09 brushed steel'))
                    f.line((pull,floor+.89,dd+.17),(pull,floor+1.24,dd+.17),.016,detail.get('hardware','store09 brushed steel'))
                else:rod(f.p(pull,floor+1.02,dd+.07),f.p(pull,floor+1.02,dd+.16),.028,detail.get('hardware','store09 aged brass'),12)
                for yy in [floor+.25,panel_head-.25]:f.b(x-ww/n*.44,yy,dd+.09,.03,.10,.026,'store09 brushed steel')
                if detail.get('kickplate'):f.b(x,floor+.12,dd+.12,ww/n-.10,.17,.025,'store09 brushed steel')
            f.b(ss,floor+.015,.12,ww,.055,.44,detail.get('threshold','store09 gray plaster'))
        else:
            f.b(ss,bottom-.035,.14,ww+.03,.07,.29,frame)
        if spec.get('grille') and not door:diamond_grille(f,left,right,bottom,panel_head,dd+.13)
        left=right
    for sign in spec.get('signs',[]):observed_sign(f,a,b,sign)
    if spec.get('awning'):observed_awning(f,a,b,spec['awning'])
    for sign in spec.get('blades',[]):projecting_sign(f,a,b,sign)
    for item in spec.get('windowText',[]):sign_text(f,a+w*item.get('at',.5),item.get('y',1.82),w*item.get('width',.6),item['text'],item.get('material','store09 warm white'),item.get('size',.20),item.get('depth',.13),item.get('style','store09:condensed'))
    for item in detail.get('displays',[]):shop09_display(f,a,b,floor,top,item)
    for item in detail.get('furniture',[]):shop09_furniture(f,a+w*item['at']+item.get('offset',0),item.get('depth',.95),item)
    for board in spec.get('boards',[]):display_board(f,a+w*board['at'],board.get('depth',.95),board.get('text',''),board.get('frame','store09 oak timber'),paper='store09 chalkboard',height=board.get('height',1.05),width=board.get('width',.57))
    for at in spec.get('lights',[]):
        s=a+w*at
        f.b(s,top+.10,.04,.12,.14,.06,'store09 dark iron')
        for u,v in [((s,top+.10,.07),(s,top+.28,.25)),((s,top+.28,.25),(s,top+.16,.49))]:f.line(u,v,.019,'store09 dark iron')
        rod(f.p(s,top+.11,.49),f.p(s,top+.17,.49),.12,'store09 dark iron',12)
        rod(f.p(s,top+.104,.49),f.p(s,top+.111,.49),.09,'opal lamp',12)
    for bench in spec.get('benches',[]):shop09_furniture(f,a+w*bench['at'],bench.get('depth',.5),{'kind':'bench',**bench})
    for menu in spec.get('menus',[]):
        item={'kind':'poster','depth':.20,**menu,'width':menu.get('width',.5)/w}
        shop09_display(f,a,b,floor,top,item)
    if detail.get('closedShutter'):
        for j in range(int((head-floor)/.075)):f.b(c,floor+(j+.5)*.075,.17,w-.15,.068,.028,detail.get('shutterMaterial','store09 brushed steel'))
    shop09_special(f,a,b,floor,top,detail)

def shop09_face(f,record):
    if paint:=record.get('paintSurround'):
        low,high=paint.get('bottom',.22),paint.get('top',3.55)
        holes=[h for h in OPENINGS[frontage_key(f)] if h[1]<high and h[3]>low]
        ys=sorted({low,high,*[max(low,min(high,h[k])) for h in holes for k in [1,3]]})
        for y0,y1 in zip(ys,ys[1:]):
            cuts=sorted([(max(0,h[0]),min(f.L,h[2])) for h in holes if h[1]<(y0+y1)/2<h[3]])
            x=0
            for l,r in cuts+[(f.L,f.L)]:
                if l>x:f.b((x+l)/2,(y0+y1)/2,.012,l-x,y1-y0,.035,paint['material'])
                x=max(x,r)
    for item in record.get('signs',[]):observed_sign(f,0,f.L,item)
    for item in record.get('displays',[]):shop09_display(f,0,f.L,.17,3.50,item)
    for item in record.get('furniture',[]):shop09_furniture(f,f.L*item['at'],item.get('depth',.95),item)
    if record.get('augursEyes'):
        for at in [.24,.75]:
            s=f.L*at;ww=f.L*.17;y=1.90
            for j in range(24):
                x0=-1+2*j/24;x1=-1+2*(j+1)/24
                for side in [-1,1]:f.line((s+x0*ww,y+side*.30*math.sin((x0+1)*math.pi/2),.18),(s+x1*ww,y+side*.30*math.sin((x1+1)*math.pi/2),.18),.015,'store09 black enamel')
            rod(f.p(s,y,.18),f.p(s,y,.20),.19,'store09 black enamel',24)
        shop09_ink(f,.08*f.L,.42*f.L,.4,1.3,'store09 paper',depth=.19,variant='ghost')
        shop09_ink(f,.58*f.L,.94*f.L,.4,1.3,'store09 purple canvas',depth=.19,variant='bubble')
