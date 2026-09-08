"""Street-scale detail shared by every neighborhood section (revision 04).

Executed inside build_neighborhood.py's component namespace. Material depth,
hardware, interiors and weathering are authored estimates. Specific architectural
crown/entry treatments come from the dated observation schedule.
"""
from collections import defaultdict
from mathutils.geometry import delaunay_2d_cdt

_original_storefront = storefront
OPENINGS = defaultdict(list)
SHOP_FRONTAGES = set()
PENDING_WALLS = []
DETAIL_SEED = 0

material('recess shadow', (.028, .036, .036), .96)
material('sill patina', (.25, .245, .215), .98)
material('entry bronze', (.17, .12, .065), .43, .65)
material('door enamel', (.055, .082, .071), .61, .12)

def frontage_key(f):
    return tuple(round(v, 3) for v in (f.x, f.z, f.rx, f.rz, f.L))

def begin_building_detail(b):
    global DETAIL_SEED
    DETAIL_SEED = b['id']
    OPENINGS.clear(); SHOP_FRONTAGES.clear(); PENDING_WALLS.clear()

def wall_mass(b, mat, open_ground=True):
    # Windows register their openings before the wall skin is emitted.
    PENDING_WALLS.append((b, mat, open_ground, b['renderHeight']))

def finish_building_detail():
    for b, mat, open_ground, h in PENDING_WALLS:
        p = b['p']
        if sum(a[0]*c[1]-c[0]*a[1] for a,c in zip(p,p[1:]+p[:1])) > 0:
            p = list(reversed(p))
        emitted=set()
        for a, c in zip(p, p[1:]+p[:1]):
            # A frontage can combine several collinear footprint edges. Match
            # the projected edge span, not its midpoint, and emit it only once.
            def belongs(v):
                positions=[((q[0]-v['x'])*v['rx']+(q[1]-v['z'])*v['rz'], abs(-(q[0]-v['x'])*v['rz']+(q[1]-v['z'])*v['rx'])) for q in [a,c]]
                return all(-.16<=s<=v['length']+.16 and d<.16 for s,d in positions)
            v = next((v for v in b['frontages'] if belongs(v)), None)
            if v:
                f = Facade(v['x'],v['z'],v['rx'],v['rz'],v['length'])
                facade_mat=b.get('facadeSpec',{}).get('elevations',{}).get(v['street'],{}).get('wall',mat)
                key = frontage_key(f)
                if key in emitted:continue
                emitted.add(key)
                low = .17
                openings = [(max(0,l),max(low,bt),min(f.L,r),min(h,top)) for l,bt,r,top in OPENINGS[key]]
                openings = [o for o in openings if o[0]<o[2] and o[1]<o[3]]
                rows = sorted({low,h,*[v for o in openings for v in [o[1],o[3]]]})
                for y0,y1 in zip(rows,rows[1:]):
                    cy = (y0+y1)/2
                    spans = sorted((o[0],o[2]) for o in openings if o[1]<cy<o[3])
                    cursor = 0
                    for left,right in spans+[(f.L,f.L)]:
                        if left>cursor:
                            face([f.p(cursor,y0),f.p(left,y0),f.p(left,y1),f.p(cursor,y1)],facade_mat)
                        cursor = max(cursor,right)
            else:
                face([(a[0],.17,a[1]),(c[0],.17,c[1]),(c[0],h,c[1]),(a[0],h,a[1])],mat)
            length = math.dist(a,c)
            box((a[0]+c[0])/2,h+.09,(a[1]+c[1])/2,length,.18,.16,mat,-math.atan2(c[1]-a[1],c[0]-a[0]))
        holes=b.get('holes',[])
        for ring in holes:
            for a,c in zip(ring,ring[1:]+ring[:1]):face([(a[0],.17,a[1]),(a[0],h,a[1]),(c[0],h,c[1]),(c[0],.17,c[1])],mat)
        if holes:
            coords=[];edges=[]
            for ring in [p,*holes]:
                start=len(coords);coords.extend(Vector(q) for q in ring)
                edges.extend((start+i,start+(i+1)%len(ring)) for i in range(len(ring)))
            vertices,_,triangles,*_=delaunay_2d_cdt(coords,edges,[],0,.00001)
            def inside(q,ring):
                x,z=q;yes=False
                for a,c in zip(ring,ring[1:]+ring[:1]):
                    if (a[1]>z)!=(c[1]>z) and x<(c[0]-a[0])*(z-a[1])/(c[1]-a[1])+a[0]:yes=not yes
                return yes
            for tri in triangles:
                center=sum((vertices[i] for i in tri),Vector((0,0)))/len(tri)
                if inside(center,p) and not any(inside(center,hole) for hole in holes):face([(vertices[i].x,h,vertices[i].y) for i in reversed(tri)],'roof')
        else:
            verts = [Vector((a[0],h,a[1])) for a in p]
            for tri in tessellate_polygon([verts]):face([verts[v] if isinstance(v,int) else v for v in tri],'roof')

def relief(f,s,y,trim):
    # Shallow geometric foliate relief, an interpretation rather than a scan.
    for k in range(8):
        a=k*math.tau/8; b=(k+1)*math.tau/8
        face([f.p(s,y,.30), f.p(s+.10*math.cos(a),y+.10*math.sin(a),.34),
              f.p(s+.10*math.cos(b),y+.10*math.sin(b),.34)],trim)

def window_crown(f,s,top,w,trim):
    for k in range(12):
        a=k*math.pi/12; b=(k+1)*math.pi/12
        face([f.p(s+math.cos(a)*(w*.54),top+math.sin(a)*w*.32,.24),
              f.p(s+math.cos(b)*(w*.54),top+math.sin(b)*w*.32,.24),
              f.p(s+math.cos(b)*(w*.54+.11),top+math.sin(b)*(w*.32+.12),.24),
              f.p(s+math.cos(a)*(w*.54+.11),top+math.sin(a)*(w*.32+.12),.24)],trim)
    f.b(s,top+w*.32+.04,.27,.15,.23,.19,trim)

def street_window(f,s,y,w,h,trim,style=0,ac=False):
    if w <= .15 or h <= .15: return
    if getattr(f,'window_shape','rectangle') in ['round','segmental']:
        shaped_window(f,s,y,w,h,trim,style,getattr(f,'window_shape'));return
    cy=y+h/2
    OPENINGS[frontage_key(f)].append((s-w/2-.025,y-.025,s+w/2+.025,y+h+.025))
    pattern=(DETAIL_SEED+int(s*31+y*13))%11 if getattr(f,'window_dressing',True) else -1
    frame=getattr(f,'window_frame','white frame' if pattern==8 else 'window frame')
    # A deep cavity, four masonry reveals, two nested sash frames and sill drip.
    f.b(s,cy,-.24,w+.06,h+.06,.035,'recess shadow')
    for dx in [-w/2-.045,w/2+.045]:f.b(s+dx,cy,-.065,.11,h+.20,.32,trim)
    for yy in [y-.04,y+h+.04]:f.b(s,yy,-.065,w+.10,.10,.32,trim)
    f.b(s,cy,-.145,w-.035,h-.035,.018,'blue glass' if pattern==6 else 'window glass')
    for dx in [-w/2+.03,w/2-.03]:f.b(s+dx,cy,-.025,.045,h,.08,frame)
    for yy in [y+.02,y+h*.47,y+h-.025]:f.b(s,yy,.015,w,.052,.11,frame)
    f.b(s,y+h*.47+.042,.071,.07,.028,.025,'metal')
    f.b(s,y-.095,.15,w+.28,.13,.43,trim)
    f.b(s,y-.175,.185,w+.14,.022,.22,'sill patina')
    f.b(s,y+h+.10,.11,w+.28,.19,.27,trim)
    # Different curtain openings and blind heights stay deterministic by address.
    if pattern in [1,3,7,9]:
        for side in [-1,1]:
            for pleat in range(4):
                f.b(s+side*(w*.39-pleat*w*.047),cy,-.105+(pleat%2)*.012,w*.050,h*.92,.019,'curtain light' if pattern in [1,7] else 'curtain amber')
    elif pattern in [0,2,5,8]:
        for j in range(5+(pattern%3)*3):f.b(s,y+h-.08-j*.067,-.087,w-.13,.040,.015,'curtain')
        f.line((s+w*.33,y+h-.12,-.055),(s+w*.33,y+h*.50,-.055),.004,'curtain light')
    if style>=1:
        f.b(s,y+h+.25,.18,w+.43,.095,.39,trim)
        for dx in [-w*.44,w*.44]:f.b(s+dx,y-.20,.075,.14,.15,.22,trim)
    if style>=2:
        for dx in [-w*.48,w*.48]:f.b(s+dx,y+h+.04,.15,.12,.31,.25,trim)
        relief(f,s,y+h+.29,trim)
    if getattr(f,'arched_crown',False):window_crown(f,s,y+h+.16,w,trim)
    if ac:
        f.b(s,y+.16,.33,w*.67,.39,.53,'air conditioner')
        for j in range(7):f.b(s,y+.014+j*.045,.603,w*.55,.012,.016,'metal')
        for side in [-1,1]:
            ss=s+side*w*.23
            f.line((ss,y-.29,.015),(ss,y-.065,.55),.014,'metal')
            f.line((ss,y-.065,.015),(ss,y-.065,.55),.014,'metal')
        f.line((s+w*.29,y+.05,.59),(s+w*.35,y-.26,.11),.009,'black iron')

def doorway(f,s,number,stoop=False,trim='brownstone'):
    rise=getattr(f,'entry_rise',.80 if stoop else 0); floor=.19+rise
    OPENINGS[frontage_key(f)].append((s-.50,floor,s+.50,2.71+rise))
    f.b(s,1.47+rise,-.27,1.01,2.57,.06,'recess shadow')
    for dx in [-.59,.59]:
        f.b(s+dx,1.43+rise,.04,.19,2.50,.36,trim)
        f.b(s+dx,.34+rise,.13,.29,.31,.43,trim)
        f.b(s+dx,2.60+rise,.16,.29,.14,.44,trim)
    f.b(s,2.74+rise,.16,1.46,.17,.48,trim)
    f.b(s,2.85+rise,.22,1.61,.09,.58,trim)
    door='door enamel' if DETAIL_SEED%3 else 'wood'
    f.b(s,1.37+rise,-.14,.94,2.25,.07,door)
    for yy in [.61,1.13]:
        f.b(s,yy+rise,-.091,.72,.37,.038,'entry bronze')
        f.b(s,yy+rise,-.064,.61,.27,.024,door)
    f.b(s,1.92+rise,-.093,.71,.83,.025,'dark glass')
    f.b(s,2.51+rise,-.08,.94,.29,.03,'warm glass')
    for dx in [-.44,0,.44]:f.b(s+dx,2.51+rise,-.035,.037,.32,.058,'entry bronze')
    for yy in [2.31,2.70]:f.b(s,yy+rise,-.015,.99,.062,.08,'entry bronze')
    f.line((s+.31,1.08+rise,-.01),(s+.31,1.48+rise,-.01),.015,'brass')
    for yy in [.57,1.47,2.18]:f.b(s-.46,yy+rise,-.007,.043,.092,.035,'metal')
    f.b(s,floor,.23,1.12,.08,.64,trim)
    f.b(s+.78,1.41+rise,.15,.17,.36,.07,'entry bronze')
    for j in range(4):
        f.b(s+.745,1.30+rise+j*.055,.194,.021,.023,.013,'brass')
        f.b(s+.800,1.30+rise+j*.055,.194,.049,.013,.013,'sign white')
    if number:label(f,s,2.51+rise,.76,number,'cream stone',.145,-.01)
    if getattr(f,'detail',{}).get('archedEntry'):window_crown(f,s,2.88+rise,1.27,trim)
    if getattr(f,'detail',{}).get('pedimentEntry'):
        face([f.p(s-.83,2.9+rise,.18),f.p(s+.83,2.9+rise,.18),f.p(s,3.35+rise,.18)],trim)
        for side in [-1,1]:f.line((s+side*.84,2.91+rise,.27),(s,3.37+rise,.27),.065,trim)
    if stoop:
        count=max(1,round(rise/.16));run=count*.25
        for k in range(count):
            step=rise/count*(k+1)
            f.b(s,.17+step/2,run-.25*k,1.46,step,.28,trim)
            f.b(s,.175+step,run-.25*k+.12,1.50,.027,.085,'sill patina')
        for dx in [-.76,.76]:
            for k in range(count+1):f.line((s+dx,.18+rise*k/count,run+.13-.25*k),(s+dx,1.09+rise*k/count,run+.13-.25*k),.018)
            f.line((s+dx,1.09,run+.13),(s+dx,1.09+rise,.13),.029)
            f.b(s+dx,.21,run+.13,.15,.15,.15,trim)

def storefront(f,a,b,name='',awning=None,fascia='shop cream',letter='sign white',closed=False,profile='cafe'):
    if b-a<1.1:return
    SHOP_FRONTAGES.add(frontage_key(f))
    OPENINGS[frontage_key(f)].append((a,.17,b,3.16))
    _original_storefront(f,a,b,name,awning,fascia,letter,closed,profile)
    c=(a+b)/2;w=b-a
    # Roll-up shutter housing, panel joints, wall fixings and glazed transom.
    f.b(c,3.265,.36,w-.20,.14,.26,'window frame')
    for j in range(4):f.b(c,3.217+j*.032,.50,w-.24,.010,.012,'metal')
    for s in [a+.10,b-.10]:
        for yy in [.65,1.90,2.76]:f.b(s,yy,.476,.035,.035,.019,'metal')
    for j in range(1,max(2,round(w/.85))):
        f.b(a+j*w/max(2,round(w/.85)),2.60,.30,.028,.34,.052,'entry bronze')
    if not closed:
        # Small menu/display cards are blank unless the source names the business.
        f.b(b-.36,1.73,.283,.23,.31,.025,'poster paper')
        for k in range(4):f.b(b-.36,1.80-k*.046,.301,.15,.012,.004,'window frame')
        f.b(c,2.94,-.45,max(.35,w*.55),.025,.09,'warm glass')

def detail_frontage(f,spec,h,is_primary):
    if f.L<3 or h<5:return
    detail=spec.get('detail',{}) if is_primary else {}
    # Street-level base joints, exposed pipes and wall anchors use no tenant names.
    for yy in [.40,.78]:
        for s in [.13,f.L-.13]:f.b(s,yy,.055,.16,.026,.065,'sill patina')
    if not spec.get('landmark') and f.L>5:
        s=f.L-.17
        f.line((s,.27,.15),(s,h-.70,.15),.029,'metal')
        for yy in range(1,max(2,int(h)),3):f.b(s,yy,.125,.12,.055,.13,'black iron')
        f.line((s,.40,.15),(s,.24,.37),.035,'metal')
        # Service cable sags slightly between the fixings.
        for k in range(12):
            t=k/12;u=(k+1)/12
            f.line((.2+(f.L-.4)*t,3.30-.15*4*t*(1-t),.13),(.2+(f.L-.4)*u,3.30-.15*4*u*(1-u),.13),.008)
    if detail.get('rusticatedBase'):
        for yy in [.50,.88,1.26,1.64,2.02,2.40,2.78,3.12]:
            for s in [.16,f.L-.16]:f.b(s,yy,.10,.31,.035,.12,'sill patina')
    if detail.get('quoins'):
        for yy in range(4,int(h-1)):
            for s in [.19,f.L-.19]:f.b(s,yy,.08,.48 if yy%2 else .34,.40,.20,spec.get('trim','cream stone'))
    if not spec.get('cornicePlain') and h<30:
        # Dentils and a fine shadow line beneath the existing cornice.
        for j in range(max(1,int(f.L/.31))):f.b(.16+j*.31,h-.69,.17,.09,.115,.24,spec.get('cornice','cornice copper brown'))
    if detail.get('roofRail'):
        for j in range(max(2,int(f.L/.22))):f.line((.12+j*.22,h+.17,-.16),(.12+j*.22,h+.96,-.16),.012)
        f.line((.05,h+.96,-.16),(f.L-.05,h+.96,-.16),.023)
    if detail.get('roofBalustrade'):
        for s in [.15+i*.40 for i in range(int((f.L-.3)/.40))]:
            f.b(s,h+.40,.03,.15,.64,.19,'cream stone')
            f.b(s,h+.38,.03,.23,.22,.23,'cream stone')
        f.strip(h+.76,.13,.32,'cream stone')
    if detail.get('pediment'):
        w=min(2.7,f.L*.4);s=f.L/2;mat=spec.get('cornice','cornice copper brown')
        if detail['pediment']=='triangle':
            face([f.p(s-w/2,h-.16,.08),f.p(s+w/2,h-.16,.08),f.p(s,h+.65,.08)],mat)
            for side in [-1,1]:f.line((s+side*w/2,h-.14,.18),(s,h+.67,.18),.065,mat)
        elif detail['pediment']=='round':window_crown(f,s,h-.16,w,mat)
        else:f.b(s,h+.24,.06,w,.53,.22,mat)
    if detail.get('wovenBrick'):
        # Observed alternating headers; geometry is authored from the pattern,
        # not a copied photographic facade texture.
        key=frontage_key(f)
        for iy in range(max(0,int((h-7)/.17))):
            yy=3.4+iy*.17
            for ix in range(int(f.L/.24)):
                ss=.12+ix*.24
                if (ix+iy)%2 or any(l-.1<ss<r+.1 and bt-.12<yy<top+.12 for l,bt,r,top in OPENINGS[key]):continue
                f.b(ss,yy,.035,.105,.07,.10,'cream stone')

def shaped_window(f,s,y,w,h,trim,style,shape):
    """Curved glazing and masonry spandrels, not a crown over square glass."""
    rise=min(w*.5,h*.35) if shape=='round' else min(w*.19,h*.18)
    shoulder=y+h-rise
    arc=[(s+w/2*math.cos(k*math.pi/16),shoulder+rise*math.sin(k*math.pi/16)) for k in range(17)]
    outline=[(s-w/2,y),(s+w/2,y),*arc]
    OPENINGS[frontage_key(f)].append((s-w/2-.025,y-.025,s+w/2+.025,y+h+.025))
    vertices=[Vector((x,yy,0)) for x,yy in outline]
    for tri in tessellate_polygon([vertices]):
        points=[vertices[v] if isinstance(v,int) else v for v in tri]
        face([f.p(v.x,v.y,-.14) for v in points],'window glass')
    for (x0,y0),(x1,y1) in zip(arc,arc[1:]):
        face([f.p(x0,y0),f.p(x1,y1),f.p(x1,y+h+.03),f.p(x0,y+h+.03)],getattr(f,'wall','warm brick'))
        face([f.p(x0,y0,-.2),f.p(x1,y1,-.2),f.p(x1,y1,.04),f.p(x0,y0,.04)],trim)
        f.line((x0,y0,.075),(x1,y1,.075),.065,trim)
    for side in [-1,1]:
        f.b(s+side*(w/2+.045),(y+shoulder)/2,-.06,.11,shoulder-y,.31,trim)
        f.b(s+side*(w/2-.025),(y+shoulder)/2,.01,.045,shoulder-y,.06,'window frame')
    for yy in [y+.035,y+h*.46,shoulder]:f.b(s,yy,.035,w,.05,.08,'window frame')
    f.b(s,y-.10,.13,w+.26,.14,.40,trim)
    if style>=2:relief(f,s,y+h+.23,trim)

def retail_front(f,a,b,name,fascia,letter,category):
    """A restrained retail unit, with no restaurant counter or invented logo."""
    if b-a<1.15:return
    w=b-a;c=(a+b)/2;OPENINGS[frontage_key(f)].append((a,.17,b,3.15))
    f.b(c,1.53,-1.1,w,2.7,.06,'dark glass')
    for side in [a+.07,b-.07]:f.b(side,1.63,.05,.14,2.92,.31,fascia)
    for yy in [.38,2.54]:f.b(c,yy,.19,w,.09,.20,fascia)
    door=a+min(.65,w*.24)
    for ss in [door-.44,door+.44]:f.b(ss,1.45,.20,.065,2.30,.12,'window frame')
    f.b(c,1.48,.205,w-.20,2.1,.018,'store glass')
    f.b(c,2.86,.18,w,.53,.25,fascia)
    if name:label(f,c,2.86,w-.24,name,letter,min(.27,(w-.24)/max(5,len(name))*1.25),d=.322)
    f.line((door+.28,1.02,.28),(door+.28,1.55,.28),.013,'brass')
    if category in ['books','clothes','second_hand','gift','variety_store']:
        for yy in [.65,1.12,1.58,2.04]:
            f.b(c,yy,-.7,max(.5,w-1.2),.06,.38,'wood')
            for j in range(max(1,int((w-1.3)/.25))):f.b(a+.75+j*.25,yy+.15,-.64,.16,.26,.18,'shop burgundy' if j%3 else 'shop sage')

def basement_shop(f,a,b,name,fascia,letter):
    if b-a<1.15:return
    w=b-a;c=(a+b)/2
    OPENINGS[frontage_key(f)].append((a,.17,b,1.97))
    f.b(c,1.01,-.08,w,1.68,.06,'dark glass')
    for ss in [a+.08,b-.08]:f.b(ss,1.02,.09,.15,1.74,.22,fascia)
    f.b(c,1.91,.12,w,.28,.26,fascia)
    label(f,c,1.92,w-.2,name,letter,min(.20,(w-.2)/max(5,len(name))*1.25),.265)
    f.b(a+.59,1.01,.04,.82,1.60,.045,'wood')
    f.b(a+.59,1.18,.075,.68,1.14,.025,'dark glass')
    f.line((a+.86,.73,.14),(a+.86,1.09,.14),.014,'brass')

def blue_gold_front(f,number):
    a=f.L*.29;b=f.L-.25;c=(a+b)/2;w=b-a
    f.b(c,1.57,.01,w,2.8,.16,'warm brick')
    # Two narrow windows flank the central low entrance; the small sign sits on
    # a green scalloped awning. Source photo upload: May 2022, capture unknown.
    door=c;ww=max(.7,(w-1.65)/2)
    for ss in [a+ww/2+.14,b-ww/2-.14]:
        OPENINGS[frontage_key(f)].append((ss-ww/2,.45,ss+ww/2,2.33))
        f.b(ss,1.39,.11,ww,1.87,.05,'dark glass')
        for yy in [.43,2.35]:f.b(ss,yy,.15,ww+.12,.07,.15,'cornice green')
        for yy in [1.88+i*.095 for i in range(5)]:f.b(ss,yy,.17,ww-.08,.028,.04,'cornice green')
    OPENINGS[frontage_key(f)].append((door-.48,.17,door+.48,2.47))
    f.b(door,1.24,.12,.94,2.45,.08,'black iron');f.b(door,1.62,.17,.77,1.38,.024,'dark glass')
    f.line((door+.29,.9,.23),(door+.29,1.33,.23),.014,'brass')
    for l,r in [(a,door-.48),(door-.48,b)]:
        face([f.p(l,2.65,.05),f.p(r,2.65,.05),f.p(r,2.39,.67),f.p(l,2.39,.67)],'awning green')
        for k in range(max(1,int((r-l)/.19))):
            ss=l+.1+k*.19;f.b(ss,2.35,.67,.17,.10,.035,'awning green')
    f.b(c+.18,2.47,.70,min(2.4,w*.62),.31,.07,'nishaan blue')
    label(f,c+.18,2.48,min(2.22,w*.60),'BLUE & GOLD','yellow paint',.195,.75)
    # A small Ukrainian flag and the observed entrance railing are geometric.
    f.b(b-ww*.45,.76,.18,.42,.15,.023,'nishaan blue');f.b(b-ww*.45,.61,.18,.42,.15,.023,'yellow paint')
    for j in range(max(2,int(w/.28))):f.line((a+.14+j*.28,.19,.86),(a+.14+j*.28,.82,.86),.016,'cornice green')
    f.line((a,.7,.86),(b,.7,.86),.024,'cornice green')
    doorway(f,max(.8,f.L*.14),number,False,'brownstone')

def render_ground(b,f,v,spec,primary,columns,wall,trim):
    f.window_shape='rectangle';f.arched_crown=False
    number=b['address'].split(' ')[0] if b['address'] else ''
    entries=[r for r in b.get('businesses',[]) if r['renderName'] and b['frontages'][r['frontageIndex']] is v]
    use=spec.get('groundUse') if primary else None
    if primary and spec.get('groundProfile')=='blue_gold':blue_gold_front(f,number);return
    entry=max(.85,min(f.L-.85,f.L*spec.get('entryPosition',.23)))
    if use in ['garage','bathhouse']:
        ww=max(1.2,f.L-2.2);center=f.L*.5
        if use=='garage':
            f.b(center,1.47,.04,ww,2.56,.10,'window frame')
            for i in range(23):f.b(center,.25+i*.107,.12,ww-.12,.028,.07,'metal')
            doorway(f,f.L-.75,number,False,trim)
        else:
            doorway(f,entry,number,True,trim)
            for ss in [f.L*.12,f.L*.5,f.L*.85]:
                if abs(ss-entry)>1:street_window(f,ss,1.03,min(1.15,f.L/5),1.55,trim)
            label(f,f.L/2,3.10,f.L-.4,'RUSSIAN & TURKISH BATHS','black iron',.23,.22)
        return
    if entries or use in ['shops','basement_shops'] or (use is None and v['street'] in ['First Avenue','Second Avenue','Avenue A'] and b['buildingType'] not in ['church','school','civic']):
        if entries:
            # Names occupy only their supported approximate unit. The rest of
            # a long elevation must not inherit the nearest shop's identity.
            gaps=[];cursor=.12
            for r in sorted(entries,key=lambda r:r['unit'][0]):
                a,end=r['unit']
                if a-cursor>1.15:gaps.append((cursor,a-.12))
                cursor=max(cursor,end+.12)
            if f.L-.12-cursor>1.15:gaps.append((cursor,f.L-.12))
            entries=list(entries)
            for a,end in gaps:
                count=max(1,math.ceil((end-a)/7))
                for j in range(count):entries.append({'name':'','unit':[a+(end-a)*j/count,a+(end-a)*(j+1)/count-.08],'category':'unknown'})
        if not entries:
            count=max(1,round(f.L/7))
            entries=[{'name':'','unit':[j*f.L/count+.12,(j+1)*f.L/count-.12],'category':'unknown'} for j in range(count)]
        reserve=1.55 if f.L>5 and spec.get('floors',b['floors'])>1 and spec.get('residentialEntry',True) else 0
        for r in entries:
            a,end=r['unit'];name=r['name'].upper();fascia=r.get('fascia','window frame');letters=r.get('letters','sign white')
            if r.get('design'):
                photographed_shop(f,a,end,r)
                continue
            # Keep a residential doorway in tenement shop fronts. The exact
            # boundaries are explicitly estimates until a storefront is observed.
            if reserve and a<entry<end:
                left=entry-a;right=end-entry
                if left>right:end=entry-reserve/2
                else:a=entry+reserve/2
            if spec.get('shopFraction') and len(entries)==1 and primary:end=min(end,f.L*spec['shopFraction'])
            if use=='basement_shops':
                # Low shop opening under the raised residential level.
                basement_shop(f,a,end,name,fascia,letters)
                for k in range(columns):
                    ss=(k+.5)*f.L/columns
                    if abs(ss-entry)>1.1:street_window(f,ss,2.30,min(1.12,f.L/columns*.5),1.5,trim)
                continue
            if r.get('category') in ['clothes','books','gift','hardware','second_hand','hairdresser','beauty','laundry','unknown','chemist','convenience','supermarket','bank','pet']:
                retail_front(f,a,end,name,fascia,letters,r.get('category'))
            else:storefront(f,a,end,name,r.get('awning'),fascia,letters,False,r.get('profile','cafe'))
        if reserve:
            f.entry_rise=1.28 if use=='basement_shops' and spec.get('stoop') else 0
            doorway(f,entry,number,spec.get('stoop',False) and use=='basement_shops',trim)
        return
    basement=primary and spec.get('basement',False)
    f.entry_rise=1.28 if basement and spec.get('stoop') else .8 if spec.get('stoop') else 0
    pitch=f.L/max(2,columns)
    for k in range(max(2,columns)):
        ss=(k+.5)*pitch
        if abs(ss-entry)<1.1:continue
        if basement:
            street_window(f,ss,.40,min(1.15,pitch*.5),.69,trim)
            street_window(f,ss,1.58,min(1.15,pitch*.5),1.98,trim)
            for j in range(6):f.line((ss-.48+j*.19,.27,.27),(ss-.48+j*.19,1.10,.27),.011)
        else:street_window(f,ss,.86,min(1.15,pitch*.49),1.7,trim)
    doorway(f,entry,number,spec.get('stoop',False),trim)
