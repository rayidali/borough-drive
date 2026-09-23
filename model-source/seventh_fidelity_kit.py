"""Explicit Seventh elevations, installed only by the Godot exporter.

No door, AC unit, grille, ramp or window subdivision is randomly assigned here.
Positions and profiles are stored with observations in seventhEngine.elevations.
Dimensions inferred from photographs remain estimates in those records.
"""
material('seventh oak door', (.64,.40,.15), .64)
material('seventh oak recess', (.43,.24,.065), .81)
material('seventh oak edge', (.72,.47,.20), .62)
material('seventh reflective glass', (.13,.24,.29), .23, .50)
material('seventh church buff brick', (.43,.365,.27), .94)
material('seventh church limestone', (.80,.755,.65), .95)
material('seventh church dressed stone', (.88,.85,.75), .93)
material('seventh church poster purple', (.20,.10,.47), .97)
material('seventh church granite', (.16,.21,.19), .96)
material('seventh red facade brick', (.47,.125,.075), .92)
material('seventh sandstone', (.32,.21,.145), .93)
material('seventh dark sandstone', (.21,.18,.15), .94)
material('painted terracotta', (.43,.19,.14), .93)
material('seventh grey buff brick', (.53,.505,.44), .94)
material('seventh pale buff brick', (.63,.585,.49), .94)
material('seventh weathered limestone', (.58,.56,.51), .96)
material('seventh pale limestone', (.73,.70,.62), .95)
material('seventh grey painted stone', (.60,.615,.59), .94)
material('seventh cornice recess', (.075,.087,.079), .94)
material('seventh dusty red paint', (.40,.17,.13), .91)
material('seventh ceramic tile', (.63,.61,.53), .94)
material('seventh red door enamel', (.48,.105,.065), .72)
material('seventh charcoal gray paint', (.27,.30,.30), .92)
material('seventh pale church brick', (.67,.66,.60), .95)
material('seventh rough church stone', (.38,.395,.36), .98)
material('seventh slate roof', (.29,.34,.36), .85)
material('seventh worn stair stone', (.40,.39,.35), .96)
material('east7 scaffold blue', (.045,.20,.36), .76)
material('east7 shed green', (.065,.21,.13), .90)
material('east7 plywood', (.48,.25,.11), .97)
material('east7 sage paint', (.34,.43,.34), .87)
material('east7 navy paint', (.075,.13,.19), .87)
material('east7 salmon trim', (.61,.35,.29), .88)
material('east7 bronze', (.17,.19,.12), .69)

_fidelity_photographed_shop = photographed_shop
def photographed_shop(f,a,b,r):
    """Engine-only color split for observed shop plinths; legacy kit is frozen."""
    _fidelity_photographed_shop(f,a,b,r)
    spec=r['design'];mat=spec.get('baseMaterial')
    if not mat or b-a<.75:return
    left=a+.16;usable=b-a-.32;base=spec.get('base',.40)
    for kind,fraction in spec['panels']:
        width=usable*fraction
        if kind not in ['door','double-door']:
            f.b(left+width/2,(base+.17)/2,spec.get('windowDepth',.035)+.13,width,max(.04,base-.17),.03,mat)
        left+=width

class FidelityProjectedFacade:
    def __init__(self,base,depth):self.base=base;self.depth=depth
    def __getattr__(self,key):return getattr(self.base,key)
    def p(self,s,y,d=0):return self.base.p(s,y,d+self.depth)
    def b(self,s,y,d,w,h,depth,mat):self.base.b(s,y,d+self.depth,w,h,depth,mat)
    def line(self,a,b,r,mat='black iron'):rod(self.p(*a),self.p(*b),r,mat)

def fidelity_stroke(f,a,b,r,mat):
    """Two beveled faces for shallow attached carving, not an 8-sided pipe.

    The back is the existing wall. Profile, width and depth remain visible
    from the street while avoiding hidden tube faces at every scroll segment.
    """
    dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy)
    if length<.00001:return
    nx=-dy/length*r;ny=dx/length*r
    def edge(p,side):return f.p(p[0]+nx*side,p[1]+ny*side,p[2]-r*.25)
    aa=f.p(a[0],a[1],a[2]+r*.45);bb=f.p(b[0],b[1],b[2]+r*.45)
    face([edge(a,1),aa,bb,edge(b,1)],mat)
    face([aa,edge(a,-1),edge(b,-1),bb],mat)

def fidelity_arc(f,s,y,rx,ry,depth,thickness,mat,segments=24):
    for j in range(segments):
        a=j*math.pi/segments;b=(j+1)*math.pi/segments
        fidelity_stroke(f,(s+rx*math.cos(a),y+ry*math.sin(a),depth),
                        (s+rx*math.cos(b),y+ry*math.sin(b),depth),thickness,mat)

def fidelity_panel(f,s,y,w,h,d,mat,edge=.035):
    for xx in [s-w/2,s+w/2]:f.b(xx,y,d,edge,h,.035,mat)
    for yy in [y-h/2,y+h/2]:f.b(s,yy,d,w,edge,.035,mat)
    if mat=='seventh oak door':
        f.b(s,y+h/2-edge*.5,d+.022,w-edge,.012,.022,'seventh oak edge')
        f.b(s-w/2+edge*.5,y,d+.022,.012,h-edge,.022,'seventh oak edge')

def fidelity_curve_height(t,shape):
    t=min(1,abs(t))
    if shape=='pointed':return math.sqrt(max(0,4-(t+1)**2))/math.sqrt(3)
    if shape=='ogee':return 1-1.8*t+2.4*t*t-1.6*t*t*t
    return math.sqrt(max(0,1-t*t))

def fidelity_shaped_arc(f,s,y,rx,ry,d,thickness,mat,shape):
    for j in range(32):
        a=1-j/16;b=1-(j+1)/16
        fidelity_stroke(f,(s+rx*a,y+ry*fidelity_curve_height(a,shape),d),
                        (s+rx*b,y+ry*fidelity_curve_height(b,shape),d),thickness,mat)

def fidelity_opening(f,s,bottom,w,h,mat='seventh reflective glass',shape='rectangle',d=-.16):
    """Actual recessed opening, including opaque masonry around an arch."""
    top=bottom+h;left=s-w/2;right=s+w/2
    OPENINGS[frontage_key(f)].append((left,bottom,right,top))
    f.b(s,bottom+h/2,d-.10,w+.025,h+.025,.03,'recess shadow')
    rise=(min(w*.70,h*.38) if shape=='pointed' else min(w*.40,h*.28) if shape=='ogee'
          else w*.5 if shape=='round' else min(w*.20,h*.18) if shape=='segmental' else 0)
    shoulder=top-rise
    coords=[(left,bottom),(right,bottom),(right,shoulder)]
    if shape in ['pointed','ogee']:
        for j in range(1,33):
            t=1-j/16;coords.append((s+t*w/2,shoulder+rise*fidelity_curve_height(t,shape)))
        for (x0,y0),(x1,y1) in zip(coords[2:],coords[3:]):
            face([f.p(x1,y1),f.p(x0,y0),f.p(x0,top),f.p(x1,top)],f.wall)
    elif rise:
        for j in range(1,25):
            t=j*math.pi/24;coords.append((s+math.cos(t)*w/2,shoulder+math.sin(t)*rise))
        # Fill only the two shoulders; do not leave a rectangular hole above
        # the arch or place a solid trim panel across the glazed fanlight.
        for j in range(24):
            a=j*math.pi/24;b=(j+1)*math.pi/24
            x0=s+math.cos(a)*w/2;x1=s+math.cos(b)*w/2
            y0=shoulder+math.sin(a)*rise;y1=shoulder+math.sin(b)*rise
            face([f.p(x1,y1),f.p(x0,y0),f.p(x0,top),f.p(x1,top)],f.wall)
    else:coords.append((left,top))
    coords.append((left,bottom))
    verts=[Vector((x,y,0)) for x,y in coords[:-1]]
    for tri in tessellate_polygon([verts]):
        vv=[verts[k] if isinstance(k,int) else k for k in tri]
        face([f.p(v.x,v.y,d) for v in vv],mat)
    for (x0,y0),(x1,y1) in zip(coords,coords[1:]):
        face([f.p(x0,y0,0),f.p(x1,y1,0),f.p(x1,y1,d-.025),f.p(x0,y0,d-.025)],f.wall)
    return shoulder

def fidelity_window(f,r):
    if r.get('angledBay'):
        # The two white parlor oriels at 112 have glazed angled returns.
        # Explicit opt-in: existing projected windows keep their old geometry.
        s=r['at']*f.L;w=r['width']*f.L;projection=r['projection']
        y=r['bottom'];h=r['height'];front_w=w*r.get('frontFraction',.72)
        fidelity_opening(f,s,y,w,h,d=-.20)
        front=FidelityProjectedFacade(f,projection)
        clean={k:v for k,v in r.items() if k not in ['angledBay','projection','frontFraction']}
        fidelity_window(front,{**clean,'width':front_w/f.L})
        for side in [-1,1]:
            aa=f.p(s+side*w/2,0,.02);bb=f.p(s+side*front_w/2,0,projection)
            if side>0:aa,bb=bb,aa
            length=math.hypot(bb[0]-aa[0],bb[2]-aa[2])
            panel=Facade(aa[0],aa[2],(bb[0]-aa[0])/length,(bb[2]-aa[2])/length,length);panel.wall=r.get('frame','white frame')
            fidelity_window(panel,{**clean,'at':.5,'width':.90,'columns':1,'recess':-.04,'hood':'none'})
        for yy in [y-.08,y+h+.09]:
            points=[f.p(s-w/2-.06,yy,0),f.p(s+w/2+.06,yy,0),f.p(s+front_w/2+.06,yy,projection+.09),f.p(s-front_w/2-.06,yy,projection+.09)]
            face(points,r.get('trim','white frame'))
            for a,b in zip(points,points[1:]+points[:1]):rod(a,b,.06,r.get('trim','white frame'),6)
        return
    if r.get('projection'):
        projection=r['projection'];s=r['at']*f.L;w=r['width']*f.L
        y=r['bottom'];h=r['height'];mat=r.get('frame','black iron')
        # Box-bay returns and top/bottom caps, separate from the window face.
        for x in [s-w/2-.07,s+w/2+.07]:f.b(x,y+h/2,projection/2,.14,h+.12,projection,mat)
        for yy in [y-.07,y+h+.07]:f.b(s,yy,projection/2,w+.28,.14,projection+.08,mat)
        f=FidelityProjectedFacade(f,projection)
    s=r['at']*f.L;w=r['width']*f.L;y=r['bottom'];h=r['height']
    trim=r.get('trim','cream stone');frame=r.get('frame','white frame')
    shape=r.get('shape','rectangle');d=r.get('recess',-.15)
    shoulder=fidelity_opening(f,s,y,w,h,mat=r.get('glassMaterial','seventh reflective glass'),shape=shape,d=d)
    f.b(s,y-.055,.095,w+.20,.11,.31,trim)
    for xx in [s-w/2+.022,s+w/2-.022]:f.b(xx,(y+shoulder)/2,d+.04,.045,shoulder-y,.085,frame)
    f.b(s,y+.022,d+.05,w,.045,.08,frame)
    cols=r.get('columns',1)
    for j in range(1,cols):
        x=s-w/2+w*j/cols;fraction=(x-s)/(w/2)
        high=shoulder+fidelity_curve_height(fraction,shape)*(y+h-shoulder)
        f.b(x,(y+high)/2,d+.07,r.get('mullion',.07),high-y,.14,frame)
    for at in r.get('rails',[.49]):
        yy=y+h*at
        if yy>shoulder:
            ww=w*math.sqrt(max(0,1-((yy-shoulder)/(y+h-shoulder))**2))
        else:ww=w
        f.b(s,yy,d+.07,ww,.045,.10,frame)
    if shape=='rectangle':f.b(s,y+h-.023,d+.06,w,.045,.09,frame)
    elif shape in ['pointed','ogee']:fidelity_shaped_arc(f,s,shoulder,w/2,y+h-shoulder,d+.07,.035,frame,shape)
    else:fidelity_arc(f,s,shoulder,w/2,y+h-shoulder,d+.07,.035,frame)
    hood=r.get('hood','flat')
    if hood=='flat':f.b(s,y+h+.095,.07,w+.21,.16,.20,trim)
    elif hood in ['pointed','ogee']:
        fidelity_shaped_arc(f,s,shoulder,w/2+.13,y+h-shoulder+.13,.14,.085,trim,hood)
    elif hood in ['segmental','round']:
        shaped=shape!='rectangle'
        rise=y+h-shoulder+.12 if shaped else w*(.22 if hood=='segmental' else .50)
        fidelity_arc(f,s,shoulder if shaped else y+h+.06,w*.58,rise,.14,.07,trim)
        if not shaped:f.b(s,y+h+.05,.13,w*1.24,.08,.26,trim)
        if r.get('hoodBacking') and not shaped:
            # Solid carved stone below the curved cap, not an open arch-shaped
            # gap above a rectangular sash. Only explicitly observed hoods.
            center=f.p(s,y+h+.06,.15)
            for j in range(20):
                t=j*math.pi/20;u=(j+1)*math.pi/20
                face([center,f.p(s+math.cos(t)*w*.58,y+h+.06+math.sin(t)*rise,.15),f.p(s+math.cos(u)*w*.58,y+h+.06+math.sin(u)*rise,.15)],trim)
    elif hood=='pediment':
        for side in [-1,1]:f.line((s+side*(w/2+.15),y+h+.09,.18),(s,y+h+.46,.18),.06,trim)
        f.b(s,y+h+.06,.12,w+.34,.10,.28,trim)
    elif hood=='bracketed':
        f.b(s,y+h+.16,.14,w+.36,.14,.32,trim)
        for dx in [-w*.51,w*.51]:f.b(s+dx,y+h+.01,.10,.15,.27,.26,trim)
    if r.get('keystone'):
        f.b(s,y+h+.13,.19,.16,.30,.20,trim)
    if r.get('surround'):
        for xx in [s-w/2-.085,s+w/2+.085]:f.b(xx,(y+shoulder)/2,.055,.14,shoulder-y,.23,trim)
    if r.get('grille'):
        for j in range(max(3,round(w/.17))+1):
            xx=s-w/2+j*w/max(3,round(w/.17));fraction=(xx-s)/(w/2)
            high=shoulder+fidelity_curve_height(fraction,shape)*(y+h-shoulder)
            f.line((xx,y,.17),(xx,high,.17),.008,'black iron')
        for yy in [y+h*.22,y+h*.75]:f.b(s,yy,.17,w,.022,.022,'black iron')
    if r.get('ac'):
        ww=w*.68;yy=y+.18
        f.b(s,yy,.27,ww,.36,.45,'air conditioner')
        for j in range(6):f.b(s,yy-.13+j*.052,.504,ww-.10,.014,.01,'metal')

def fidelity_access(f,s,w,r):
    rise=r.get('rise',0);count=r.get('steps',0);run=r.get('run',count*.28)
    landing=r.get('landing',.32);mat=r.get('material','seventh sandstone')
    if count:
        for j in range(count):
            hh=rise*(j+1)/count;d=landing+run*(1-(j+.5)/count)
            f.b(s,.17+hh/2,d,w,hh,run/count+.012,mat)
            f.b(s,.18+hh,d+run/count*.43,w+.025,.025,.05,r.get('treadEdgeMaterial',mat))
        f.b(s,.17+rise/2,landing/2,w,rise,landing,mat)
        if r.get('stoneCheeks'):
            # Solid sloping stoop cheeks, separately observed from iron rails.
            for side in [-1,1]:
                x=s+side*(w/2+.09);thickness=.18
                outline=[(.17,.02),(.17,landing+run),(.58,landing+run),
                         (.58+rise,landing),(.58+rise,.02)]
                for dx in [-thickness/2,thickness/2]:
                    face([f.p(x+dx,y,d) for y,d in outline],mat)
                for (y0,d0),(y1,d1) in zip(outline,outline[1:]+outline[:1]):
                    face([f.p(x-thickness/2,y0,d0),f.p(x+thickness/2,y0,d0),
                          f.p(x+thickness/2,y1,d1),f.p(x-thickness/2,y1,d1)],mat)
        if r.get('brickLattice'):
            # 98's brick/capped piers and pale diagonal infill are not iron
            # balusters. Heights follow the explicit stair schedule.
            for side in [-1,1]:
                x=s+side*(w/2+.06)
                for dd,yy in [(landing+run,.17),(landing,.17+rise)]:
                    f.b(x,yy+.48,dd,.27,.96,.30,'seventh red facade brick')
                    f.b(x,yy+.99,dd,.36,.12,.40,'seventh worn stair stone')
                for j in range(count):
                    d0=landing+run*(1-j/count);d1=landing+run*(1-(j+1)/count)
                    y0=.28+rise*j/count;y1=.28+rise*(j+1)/count
                    for offset in [.30,.74]:f.line((x,y0+offset,d0),(x,y1+offset,d1),.025,'seventh grey painted stone')
                    f.line((x,y0+.30,d0),(x,y1+.74,d1),.018,'seventh grey painted stone')
                    f.line((x,y0+.74,d0),(x,y1+.30,d1),.018,'seventh grey painted stone')
        if r.get('rails',True):
            rail_mat=r.get('railMaterial','black iron')
            for side in [-1,1]:
                x=s+side*w*.51
                f.line((x,1.1,run+landing),(x,1.1+rise,landing),.025,rail_mat)
                f.line((x,1.1+rise,landing),(x,1.1+rise,.06),.025,rail_mat)
                for j in range(count+1):
                    d=landing+run*(1-j/count);y=.18+rise*j/count
                    f.line((x,y,d),(x,y+.92,d),.012,rail_mat)
    if r.get('ramp'):
        # Explicit start/end endpoints support lateral and outward ramps.
        ramp=r['ramp'];a=ramp['start'];b=ramp['end'];width=ramp['width']
        dx=b[0]-a[0];dz=b[2]-a[2];length=math.hypot(dx,dz);nx=-dz/length*width/2;nz=dx/length*width/2
        points=[(s+a[0]+nx,a[1],a[2]+nz),(s+b[0]+nx,b[1],b[2]+nz),(s+b[0]-nx,b[1],b[2]-nz),(s+a[0]-nx,a[1],a[2]-nz)]
        face([f.p(*p) for p in points],mat)
        for side in [-1,1]:
            p=(s+a[0]+nx*side,a[1]+.92,a[2]+nz*side);q=(s+b[0]+nx*side,b[1]+.92,b[2]+nz*side)
            f.line(p,q,.023,'black iron')
            for j in range(max(2,round(length/.6))+1):
                t=j/max(2,round(length/.6));v=tuple(p[k]+(q[k]-p[k])*t for k in range(3))
                f.line((v[0],v[1]-.92,v[2]),v,.011,'black iron')

def fidelity_door(f,r):
    s=r['at']*f.L;w=r['width']*f.L;bottom=r.get('bottom',.19);top=r['top']
    trim=r.get('trim','cream stone');mat=r.get('material','door enamel');d=-r.get('recess',.18)
    shape=r.get('shape','rectangle');arched_leaves=r.get('archedLeaves',False)
    shoulder=fidelity_opening(f,s,bottom,w,top-bottom,mat if arched_leaves else r.get('openingMaterial','seventh reflective glass'),shape,d-.03)
    arch_rise=top-shoulder;leaves=r.get('leaves',1);leaf_top=r.get('leafTop',min(shoulder,bottom+2.32))
    if arched_leaves:leaf_top=shoulder
    parts=r.get('parts',[{'fraction':1/leaves} for j in range(leaves)])
    for j,part in enumerate(parts):
        x=s-w/2+w*(sum(p['fraction'] for p in parts[:j])+part['fraction']/2) if r.get('parts') else s-w/2+w*(j+.5)/leaves
        ww=w*part['fraction']-.018
        part_mat=part.get('material',mat)
        f.b(x,(bottom+leaf_top)/2,d,ww,leaf_top-bottom,.075,part_mat)
        for p in part.get('panels',r.get('panels',[])):
            cy=bottom+p['y']*(leaf_top-bottom);hh=p['height']*(leaf_top-bottom);pw=ww*p.get('width',.72)
            f.b(x,cy,d+.045,pw,hh,.022,'seventh reflective glass' if p.get('glass') else r.get('panelMaterial',mat))
            fidelity_panel(f,x,cy,pw+.045,hh+.045,d+.07,mat,.038)
            if p.get('columns',1)>1:
                for k in range(1,p['columns']):f.b(x-pw/2+pw*k/p['columns'],cy,d+.08,.028,hh,.025,mat)
            for k in range(1,p.get('rows',1)):f.b(x,cy-hh/2+hh*k/p['rows'],d+.08,pw,.028,.025,mat)
        if arched_leaves:
            l=x-ww/2+.10;rr=x+ww/2-.10;low=bottom+.48
            curve=[(l+(rr-l)*k/16,shoulder+arch_rise*fidelity_curve_height((l+(rr-l)*k/16-s)/(w/2),shape)-.13) for k in range(17)]
            outline=[(l,low),(rr,low),*reversed(curve)]
            verts=[Vector((xx,yy,0)) for xx,yy in outline]
            for tri in tessellate_polygon([verts]):
                vv=[verts[k] if isinstance(k,int) else k for k in tri]
                face([f.p(v.x,v.y,d+.047) for v in vv],'seventh reflective glass')
            for a,b in zip(outline,outline[1:]+outline[:1]):fidelity_stroke(f,(*a,d+.075),(*b,d+.075),.035,mat)
        if r.get('crossPanels'):
            cy=bottom+(leaf_top-bottom)*.66
            f.b(x,cy,d+.09,.065,(leaf_top-bottom)*.36,.07,mat)
            f.b(x,cy+.15,d+.09,ww*.55,.065,.07,mat)
        if r.get('grille'):
            diamond_grille(f,x-ww*.38,x+ww*.38,bottom+.40,leaf_top-.12,d+.11,mat)
        if not part.get('fixed'):
            side=-1 if part.get('handle')=='left' else 1 if part.get('handle')=='right' else 1 if leaves==1 or j%2==0 else -1
            hx=x+ww*.32*side
            f.line((hx,bottom+.92,d+.11),(hx,bottom+1.23,d+.11),.015,r.get('hardware','brass'))
    for xx in [s-w/2-.055,s+w/2+.055]:f.b(xx,(bottom+shoulder)/2,.025,.11,shoulder-bottom,.30,trim)
    if not arched_leaves:f.b(s,leaf_top,d+.075,w,.11,.10,mat)
    if shoulder>leaf_top+.08:
        if r.get('transomMaterial'):f.b(s,(leaf_top+shoulder)/2,d-.015,w,shoulder-leaf_top,.025,r['transomMaterial'])
        for j in range(leaves+1):f.b(s-w/2+j*w/leaves,(leaf_top+shoulder)/2,d+.045,.065,shoulder-leaf_top,.095,mat)
    if arch_rise:
        arch_mat=r.get('archFrameMaterial',mat)
        if shape in ['pointed','ogee']:
            fidelity_shaped_arc(f,s,shoulder,w*.5,arch_rise,d+.06,.055,arch_mat,shape)
            fidelity_shaped_arc(f,s,shoulder,w*.5+.13,arch_rise+.13,.12,.095,trim,shape)
        else:
            fidelity_arc(f,s,shoulder,w*.5,arch_rise,d+.06,.055,arch_mat)
            fidelity_arc(f,s,shoulder,w*.5+.13,arch_rise+.13,.12,.095,trim)
        if r.get('archMullion',True):f.b(s,(top+shoulder)/2,d+.075,.065,arch_rise,.10,arch_mat)
        if not arched_leaves and r.get('shoulderBar',True):f.b(s,shoulder,d+.075,w,.09,.10,arch_mat)
    else:f.b(s,top+.08,.09,w+.25,.16,.34,trim)
    if r.get('hood')=='pediment':
        for side in [-1,1]:f.line((s+side*(w/2+.22),top+.15,.17),(s,top+.55,.17),.07,trim)
    elif r.get('hood')=='stepped':
        for j in range(3):
            inset=j*.07
            f.b(s,top+.10+j*.09,.17,w+.34-inset*2,.09,.28,trim)
    if r.get('portal') in ['pilasters','columns']:
        for side in [-1,1]:
            x=s+side*(w/2+.20)
            if r['portal']=='columns':rod(f.p(x,bottom+.18,.12),f.p(x,shoulder-.18,.12),.13,trim,12)
            else:f.b(x,(bottom+shoulder)/2,.09,.23,shoulder-bottom,.30,trim)
            for yy in [bottom+.12,shoulder-.09]:f.b(x,yy,.14,.35,.20,.41,trim)
        if shape=='rectangle':f.b(s,top+.22,.19,w+.70,.18,.48,trim)
    if r.get('fanlight') and arch_rise:
        for j in range(1,6):
            a=j*math.pi/6
            f.line((s,shoulder,d+.10),(s+math.cos(a)*w*.47,shoulder+math.sin(a)*arch_rise*.93,d+.10),.009,'black iron')
    f.b(s,bottom,.10,w+.14,.06,.52,r.get('thresholdMaterial',trim))
    if r.get('label'):
        label_s=s+w*r.get('labelOffset',0);label_y=r.get('labelY',min(top-.12,leaf_top+.22));label_d=r.get('labelDepth',d+.13)
        if r.get('labelPlate'):
            plate=r['labelPlate'];f.b(label_s,label_y,label_d-.025,plate['width'],plate['height'],.035,plate.get('material','cream stone'))
        sign_text(f,label_s,label_y,w*r.get('labelWidth',.90),r['label'],r.get('labelMaterial','cream stone'),r.get('labelSize',.16),label_d)
    fidelity_access(f,s,w+.28,r.get('access',{}))

def fidelity_courses(f,top,mat,step=.44,bottom=.18,depth=.028):
    """Rusticated blocks, cut around every registered door and window."""
    count=max(1,math.ceil((top-bottom)/step))
    for row in range(count):
        low=bottom+row*step;high=min(top,low+step-.027)
        cuts=sorted({0,f.L,*[v for o in OPENINGS[frontage_key(f)] for v in [max(0,o[0]-.06),min(f.L,o[2]+.06)]]})
        for a,b in zip(cuts,cuts[1:]):
            center=(a+b)/2
            intervals=[(low,high)]
            for l,bt,r,tt in OPENINGS[frontage_key(f)]:
                if not l-.06<center<r+.06:continue
                next_intervals=[]
                for y0,y1 in intervals:
                    if tt<=y0 or bt>=y1:next_intervals.append((y0,y1));continue
                    if bt>y0:next_intervals.append((y0,bt))
                    if tt<y1:next_intervals.append((tt,y1))
                intervals=next_intervals
            for y0,y1 in intervals:
                n=max(1,math.ceil((b-a)/.85))
                for j in range(n):
                    x0=a+(b-a)*j/n;x1=a+(b-a)*(j+1)/n
                    if x1-x0>.035 and y1-y0>.025:f.b((x0+x1)/2,(y0+y1)/2,depth,x1-x0-.016,y1-y0,.12,mat)

def fidelity_clipped_surface(f,left,right,bottom,top,depth,thickness,mat,padding=0):
    """Place a shallow facade surface without covering registered openings."""
    def clamp_x(value):return max(left,min(right,value))
    cuts=sorted({left,right,*[
        value for opening in OPENINGS[frontage_key(f)]
        for value in (clamp_x(opening[0]-padding),clamp_x(opening[2]+padding))
    ]})
    assert all(left-.000001<=value<=right+.000001 for value in cuts),"Clipped surface cut escaped its requested span"
    for a,b in zip(cuts,cuts[1:]):
        if b-a<.004:continue
        center=(a+b)/2;intervals=[(bottom,top)]
        for opening_left,opening_bottom,opening_right,opening_top in OPENINGS[frontage_key(f)]:
            if not opening_left-padding<center<opening_right+padding:continue
            clipped=[]
            for y0,y1 in intervals:
                if opening_top+padding<=y0 or opening_bottom-padding>=y1:
                    clipped.append((y0,y1));continue
                if y0<opening_bottom-padding:clipped.append((y0,opening_bottom-padding))
                if opening_top+padding<y1:clipped.append((opening_top+padding,y1))
            intervals=clipped
        for y0,y1 in intervals:
            if y1-y0>.004:f.b(center,(y0+y1)/2,depth,b-a,y1-y0,thickness,mat)

def fidelity_cornice(f,h,c):
    mat=c['material'];profile=c.get('profile','bracketed' if c.get('ornate',True) else 'plain')
    if profile=='plain':
        f.strip(h-.14,.24,.17,mat);f.strip(h+.02,.075,.27,mat)
    elif profile=='corbelled':
        # Observed pendant arches under the low parapets of 116–122.
        f.strip(h-.11,.14,.13,mat);f.strip(h+.02,.10,.24,mat)
        count=c.get('arches',max(3,round(f.L/.80)))
        spacing=f.L/count
        for j in range(count):
            x=(j+.5)*spacing
            fidelity_arc(f,x,h-.18,spacing*.46,-.22,.10,.055,mat,12)
            f.b(x-spacing*.47,h-.38,.08,.10,.31,.17,mat)
        for j in range(max(2,round(f.L/.19))):
            f.b((j+.5)*f.L/max(2,round(f.L/.19)),h-.045,.20,.065,.06,.12,mat)
    elif profile=='parapet':
        f.strip(h-.28,.54,.10,mat);f.strip(h+.015,.08,.24,mat)
        for at in c.get('piers',[.02,.50,.98]):
            f.b(at*f.L,h-.19,.10,.18,.81,.25,mat)
    else:
        # A deep entablature: separate recesses, projecting brackets and
        # stepped crown. Dark inset faces express actual recesses in shade.
        for yy,hh,dd in [(h-.73,.11,.18),(h-.42,.50,.23),(h-.10,.12,.48),(h+.015,.10,.65),(h+.10,.07,.76)]:f.strip(yy,hh,dd,mat)
        count=c.get('brackets',max(3,round(f.L/.78)))
        spacing=(f.L-.36)/count
        for j in range(count):
            x=.18+spacing*(j+.5)
            f.b(x,h-.42,.239,spacing*.66,.28,.012,'seventh cornice recess')
            fidelity_panel(f,x,h-.42,spacing*.67,.30,.26,mat,.030)
        for j in range(count+1):
            x=.18+spacing*j
            for yy,ww,hh,dd in [(h-.58,.12,.19,.32),(h-.39,.14,.23,.43),(h-.22,.21,.14,.56)]:
                f.b(x,yy,dd/2+.08,ww,hh,dd,mat)
        for j in range(max(2,round(f.L/.24))):
            f.b((j+.5)*f.L/max(2,round(f.L/.24)),h-.76,.18,.09,.12,.23,mat)
    if c.get('pediment'):
        w=f.L*c.get('pedimentWidth',.40);s=f.L*.5
        face([f.p(s-w/2,h+.10,.07),f.p(s+w/2,h+.10,.07),f.p(s,h+.72,.07)],mat)
        for side in [-1,1]:f.line((s+side*w/2,h+.13,.18),(s,h+.75,.18),.055,mat)

def fidelity_relief(f,s,y,w,h,mat,kind):
    if kind=='shell':
        # Fan-shell apron recorded below particular arched windows.
        for j in range(17):
            a=j*math.pi/16
            fidelity_stroke(f,(s,y-h*.46,.14),(s+math.cos(a)*w*.48,y+math.sin(a)*h*.43,.15),.014,mat)
        fidelity_arc(f,s,y,w*.50,h*.46,.15,.027,mat)
    else:
        fidelity_panel(f,s,y,w,h,.13,mat,.035)
        for side in [-1,1]:
            for j in range(20):
                a=j/20*math.tau;bb=(j+1)/20*math.tau
                rr=w*.18*(1-j/27);rr2=w*.18*(1-(j+1)/27)
                fidelity_stroke(f,(s+side*w*.22+math.cos(a)*rr,y+math.sin(a)*rr*.45,.16),
                               (s+side*w*.22+math.cos(bb)*rr2,y+math.sin(bb)*rr2*.45,.16),.014,mat)

def fidelity_church_house(b,r):
    """50 E 7th: current lowered oak entrances and asymmetrical 1892 facade."""
    owner('50 East 7th / April 2026 architecture')
    b['renderHeight']=15.20;wall_mass(b,'seventh church buff brick')
    f=main_front(b,'East 7th Street');f.wall='seventh church buff brick'
    fidelity_elevation(b,f,r)
    stone='seventh church dressed stone';oak='seventh oak door'
    # Engaged columns extend to grade; capitals terminate at the arch spring.
    s=f.L*.768;w=f.L*.232;spring=3.62
    for side in [-1,1]:
        x=s+side*(w/2+.23)
        f.b(x,.47,.15,.46,.58,.51,'seventh church granite')
        for yy,rr,hh in [(.79,.24,.13),(.91,.20,.09),(3.36,.20,.10),(3.49,.25,.16)]:
            rod(f.p(x,yy-hh/2,.15),f.p(x,yy+hh/2,.15),rr,stone,16)
        rod(f.p(x,.95,.15),f.p(x,3.34,.15),.16,stone,16,r2=.185)
        f.b(x,3.50,.16,.49,.25,.43,stone)
        # Twin volutes on each capital, traced as small spiral relief.
        for direction in [-1,1]:
            center=x+direction*.112
            for j in range(22):
                a=j/22*math.tau*1.3;c=(j+1)/22*math.tau*1.3
                ra=.078*(1-j/25);rb=.078*(1-(j+1)/25)
                f.line((center+math.cos(a)*ra,3.53+math.sin(a)*ra,.40),(center+math.cos(c)*rb,3.53+math.sin(c)*rb,.40),.009,stone)
    for offset,thickness,depth in [(.08,.07,.19),(.23,.065,.26),(.35,.075,.16)]:
        fidelity_arc(f,s,spring,w/2+offset,w/2+offset,depth,thickness,stone,36)
    # Dark decorative glazing in the oak semicircular fanlight.
    for j in range(13):
        t=(j+.5)*math.pi/13
        x=s+math.cos(t)*w*.37;y=spring+math.sin(t)*w*.37
        for k in range(8):
            a=k*math.tau/8;c=(k+1)*math.tau/8
            f.line((x+math.cos(a)*.033,y+math.sin(a)*.033,-.09),(x+math.cos(c)*.033,y+math.sin(c)*.033,-.09),.006,'black iron')
    # Lower double doors have four small panels on each leaf, and glass above.
    for j in range(2):
        x=s-w/4+w*j/2
        for dx in [-w*.092,w*.092]:
            for yy in [.49,.91]:
                f.b(x+dx,yy,-.12,w*.14,.25,.028,'seventh oak recess')
                fidelity_panel(f,x+dx,yy,w*.14,.25,-.075,oak)
    left=f.L*.275;lw=f.L*.338
    for j in range(2):
        x=left-lw/4+lw*j/2
        for dx in [-lw*.087,lw*.087]:
            for yy in [.51,.94]:
                f.b(x+dx,yy,-.12,lw*.14,.29,.025,'seventh oak recess')
                fidelity_panel(f,x+dx,yy,lw*.14,.29,-.075,oak)
    # Church-house inscription and the smaller address in the door transom.
    f.b(f.L*.50,4.89,.10,f.L,.27,.23,stone)
    sign_text(f,f.L*.5,4.89,f.L*.96,'M I D D L E   C O L L E G I A T E   C H U R C H','black iron',.17,.235)
    sign_text(f,s,2.71,w*.95,'50 EAST 7TH STREET','black iron',.115,-.025)
    # Historic brass-framed information case on the granite pier.
    x=f.L*.535
    f.b(x,1.69,.15,.66,1.35,.12,'brass')
    f.b(x,1.69,.225,.56,1.22,.015,'black iron')
    f.b(x,1.69,.24,.46,1.10,.015,'seventh church poster purple')
    sign_text(f,x,2.05,.43,'PROJECT','sign white',.056,.255)
    sign_text(f,x,1.96,.43,'SPACE RENTALS','sign white',.050,.255)
    # The changing photographic artwork and fine print are not reproduced.
    for yy,ww in [(1.76,.31),(1.65,.22),(1.50,.36)]:f.b(x,yy,.252,ww,.075,.008,'seventh lilac door')
    # Visible intercom, brass fire-service couplings and paired bowed pulls.
    f.b(f.L*.949,1.24,.10,.19,.38,.10,'black iron')
    for j in range(4):f.b(f.L*.949,1.15+j*.051,.157,.11,.017,.015,'metal')
    for at in [.495,.551]:
        xx=f.L*at
        rod(f.p(xx,.72,.08),f.p(xx,.72,.24),.062,'brass',12)
        for j in range(16):
            t=j*math.tau/16;u=(j+1)*math.tau/16
            f.line((xx+math.cos(t)*.065,.72+math.sin(t)*.065,.26),(xx+math.cos(u)*.065,.72+math.sin(u)*.065,.26),.012,'brass')
    for ss,ww in [(s,w),(f.L*.275,f.L*.338)]:
        for side in [-1,1]:
            for j in range(12):
                t=j/12;u=(j+1)/12
                f.line((ss+side*ww*.065,.99+t*.33,-.018+math.sin(t*math.pi)*.045),
                       (ss+side*ww*.065,.99+u*.33,-.018+math.sin(u*math.pi)*.045),.020,'brass')
    # Three coupled sashes sit beneath a broad arch. The apron carries paired
    # scrolling foliage, not the former row of unrelated circular rosettes.
    c=f.L*.275;ww=f.L*.325
    f.b(c,8.09,.065,ww+.17,.40,.17,stone)
    for side in [-1,1]:
        for j in range(38):
            t=j/37*math.tau*1.30;u=(j+1)/37*math.tau*1.30
            rx=ww*.21*(1-j/46);rx2=ww*.21*(1-(j+1)/46)
            f.line((c+side*ww*.23+math.cos(t)*rx,8.09+math.sin(t)*rx*.24,.17),
                   (c+side*ww*.23+math.cos(u)*rx2,8.09+math.sin(u)*rx2*.24,.17),.018,stone)
    # Low left balustrade, rear dormer and three narrow arched tower lights.
    for yy in [14.91,15.32]:f.b(f.L*.285,yy,-.07,f.L*.57,.13,.29,stone)
    for j in range(17):
        x=f.L*(.024+j*.032)
        rod(f.p(x,14.98,-.07),f.p(x,15.24,-.07),.045,stone,8,r2=.037)
        f.b(x,15.1,-.07,.08,.11,.11,stone)
    f.b(f.L*.755,15.98,-1.10,f.L*.36,2.36,1.42,'seventh church buff brick')
    tower=Facade(f.x,f.z,f.rx,f.rz,f.L);tower.wall='seventh church buff brick'
    for at in [.672,.755,.838]:fidelity_window(tower,{'at':at,'width':.056,'bottom':15.59,'height':.96,'shape':'round','hood':'round','trim':stone,'frame':'white frame','rails':[.38]})
    # Restrict the upper wall to the tower span; surrounding roof remains open.
    for a,c in [(.575,.635),(.709,.727),(.783,.810),(.866,.935)]:
        f.b(f.L*(a+c)/2,15.98,.015,f.L*(c-a),2.36,.10,'seventh church buff brick')
    for yy,hh in [(15.14,.73),(16.90,.49)]:f.b(f.L*.755,yy,.01,f.L*.36,hh,.10,'seventh church buff brick')
    f.b(f.L*.755,17.16,-.08,f.L*.39,.21,.32,stone)
    apex=f.p(f.L*.755,18.08,-1)
    rim=[f.p(f.L*.575,17.25,.10),f.p(f.L*.935,17.25,.10),f.p(f.L*.935,17.25,-2.10),f.p(f.L*.575,17.25,-2.10)]
    for a,c in zip(rim,rim[1:]+rim[:1]):face([a,c,apex],'cornice green')
    for j in range(4):
        yy=17.37+j*.14;ratio=(18.08-yy)/.83
        f.b(f.L*.755,yy,-.03-(1-ratio)*.96,f.L*.36*ratio,.026,.07,'metal')
    f.b(f.L*.275,15.55,-2.35,f.L*.43,1.04,.30,'painted ivory')
    for at in [.12,.22,.32,.42]:f.b(f.L*at,15.55,-2.17,.36,.60,.025,'window glass')
    b['renderHeight']=18.12

def fidelity_bayed_shop(f,a,b,r):
    """Observed pane order and projected returns, with a separate recessed door.

    Path fractions/depths live in the storefront observation. No invented room
    is substituted for the interior; the backing remains explicitly unresolved.
    """
    spec=r['design'];w=b-a;top=spec['top'];base=spec['base'];frame=spec['frame']
    OPENINGS[frontage_key(f)].append((a,.17,b,top+.03))
    f.b((a+b)/2,(top+.17)/2,-.88,w,top-.17,.035,'dark glass')
    path=spec['facadePath']
    for j,((start,d0),(end,d1)) in enumerate(zip(path,path[1:])):
        p=f.p(a+w*start,0,d0);q=f.p(a+w*end,0,d1)
        length=math.hypot(q[0]-p[0],q[2]-p[2]);panel=Facade(p[0],p[2],(q[0]-p[0])/length,(q[2]-p[2])/length,length)
        door=spec['panels'][j][0]=='door';low=.22 if door else base
        head=spec.get('doorHead',2.40) if door else top
        for x in [0,length]:panel.b(x,(top+.17)/2,.015,.075,top-.17,.13,frame)
        for yy in [low,head,top]:panel.b(length/2,yy,.025,length,.072,.14,frame)
        panel.b(length/2,(head+low)/2,-.025,max(.03,length-.075),head-low-.072,.016,'store glass')
        panel.b(length/2,(low+.17)/2,.015,length,max(.025,low-.17),.13,spec['surround'])
        if door:
            panel.b(length/2,(top+head)/2,-.025,length-.075,top-head-.075,.016,'store glass')
            panel.b(length/2,.34,.04,length-.08,.23,.06,frame)
            panel.line((length*.18,.99,.12),(length*.18,1.46,.12),.014,'metal')
            for yy in [.55,2.18]:panel.b(length-.055,yy,.055,.035,.08,.035,'metal')
        # Horizontal bottom and top faces make the bay a solid projection.
        for yy,mat in [(low-.045,spec['surround']),(top+.045,frame)]:
            face([f.p(a+w*start,yy,-.32),f.p(a+w*end,yy,-.32),f.p(a+w*end,yy,d1+.04),f.p(a+w*start,yy,d0+.04)],mat)
    for sign in spec.get('signs',[]):observed_sign(f,a,b,sign)
    for sign in spec.get('blades',[]):projecting_sign(f,a,b,sign)
    for bench in spec.get('benches',[]):
        ss=a+w*bench['at'];ww=bench['width'];dd=bench.get('depth',.90)
        # Open metal slats/curved back observed in the April entrance views.
        for j in range(15):
            x=ss-ww/2+j*ww/14
            for aa,bb in [((x,.46,dd+.22),(x,.46,dd-.13)),((x,.46,dd-.13),(x,.67,dd-.23)),((x,.67,dd-.23),(x,.91,dd-.29))]:f.line(aa,bb,.012,'black iron')
        for yy,zz in [(.46,dd+.22),(.46,dd-.13),(.91,dd-.29)]:f.line((ss-ww/2,yy,zz),(ss+ww/2,yy,zz),.022,'black iron')
        for side in [-1,1]:
            x=ss+side*ww*.37
            for zz in [dd-.13,dd+.17]:f.line((x,.17,zz),(x,.46,zz),.025,'black iron')

OBSERVED_GROUND = globals().get('SEVENTH_GROUND_OVERRIDES',{})

def _observed_scaffold(f, spec):
    """Shallow street-facing scaffold seen in a dated view; no permit text."""
    spans=spec.get('scaffold',[])
    for sc in spans:
        a=sc.get('at',0)*f.L if isinstance(sc.get('at',0),(int,float)) else sc['at'][0]*f.L
        b=sc.get('to',1)*f.L if isinstance(sc.get('to',1),(int,float)) else sc['at'][1]*f.L
        levels=sc.get('levels',[.35,3.45,6.55,9.65,12.75])
        depth=sc.get('depth',.36)
        if sc.get('datedShed'):
            # April 2026 east-block sheds. Separate fascia, posts, braces and
            # upper working decks; opt-in leaves the accepted 66 unchanged.
            canopy=sc.get('canopyY',3.35);mat=sc.get('material','metal')
            count=max(2,round((b-a)/1.8));posts=[a+(b-a)*j/count for j in range(count+1)]
            high=max(levels[-1],canopy)
            for x in posts:
                f.line((x,.18,depth),(x,high,depth),.035,mat)
                f.line((x,canopy,.06),(x,canopy,depth),.035,mat)
                f.b(x,.18,depth,.20,.04,.20,'metal')
            f.b((a+b)/2,canopy,depth/2,b-a,.14,depth,'seventh worn stair stone')
            f.b((a+b)/2,canopy+.42,depth+.03,b-a,.76,.09,'east7 shed green')
            for j,(x0,x1) in enumerate(zip(posts,posts[1:])):
                if j%2==0:
                    f.line((x0,.30,depth),(x1,canopy-.14,depth),.020,mat)
                    f.line((x1,.30,depth),(x0,canopy-.14,depth),.020,mat)
                f.b((x0+x1)/2,canopy-.12,depth*.5,.28,.045,.15,'opal lamp')
                for y0,y1 in zip(levels,levels[1:]):
                    if y0<canopy:continue
                    f.line((x0,y0,depth),(x1,y1,depth),.020,mat)
                    f.line((x1,y0,depth),(x0,y1,depth),.020,mat)
                    for yy in [y0,y0+.95]:f.line((x0,yy,depth),(x1,yy,depth),.025,mat)
                    f.b((x0+x1)/2,y0,depth*.5,x1-x0,.055,depth,'wood')
            if sc.get('net'):
                # Sparse dark mesh geometry avoids transparent overdraw.
                for j in range(max(2,round((b-a)/.16))+1):
                    x=a+(b-a)*j/max(2,round((b-a)/.16))
                    f.b(x,(canopy+high)/2,depth+.07,.013,high-canopy,.012,'black iron')
                for j in range(max(2,round((high-canopy)/.23))+1):
                    yy=canopy+(high-canopy)*j/max(2,round((high-canopy)/.23))
                    f.b((a+b)/2,yy,depth+.075,b-a,.011,.012,'black iron')
                for x in posts:
                    for yy in levels[1:]:f.b(x,yy,depth+.10,.08,.05,.025,'theater red')
            if sc.get('board'):
                observed_sign(f,a,b,{'at':.24,'width':.43,'y':canopy+.44,'height':.53,'depth':depth+.10,'material':'sign white','lines':[{'text':sc['board'],'material':'black iron','size':.12}]})
            continue
        for x in [a,b]:
            f.line((x,.18,depth),(x,levels[-1],depth),.035,'black iron')
        for y in levels:f.line((a,y,depth),(b,y,depth),.028,'black iron')
        # The photographed 66 shed projects across the sidewalk. Its deck and
        # outer poles make a real obstruction instead of thin wall-line art.
        var_canopy_y=sc.get('canopyY',3.40)
        f.b((a+b)/2,var_canopy_y,depth*.5,b-a,.10,depth,'black iron')
        var_poles=max(2,round((b-a)/1.65))
        for j in range(var_poles+1):
            var_x=a+(b-a)*j/var_poles
            f.line((var_x,.18,depth),(var_x,var_canopy_y+.10,depth),.030,'black iron')
            f.line((var_x,var_canopy_y,0.06),(var_x,var_canopy_y,depth),.024,'black iron')
        for y in levels[1:]:
            f.line((a,y,depth),(b,y-.28,depth),.020,'black iron')
            f.line((b,y,depth),(a,y-.28,depth),.020,'black iron')
        for y in levels[:-1]:
            f.b((a+b)/2,y,depth,b-a,.055,.72,'black iron')

def _observed_ground(f,b):
    spec=b.get('seventhArchitecture',{}).get('observedGround',OBSERVED_GROUND.get(str(b['id']),{}))
    if not spec:return
    tile=spec.get('tileGround')
    if tile:
        material_name=tile.get('material','seventh ceramic tile');tile_h=tile.get('height',.92);tile_w=tile.get('width',.18)
        cols=max(1,round(f.L/tile_w));rows=max(1,round(tile_h/tile_w))
    for opening in spec.get('groundOpenings',[]):
        fidelity_window(f,{**opening,'at':opening['at'],'hood':opening.get('hood','none'),
                           'shape':opening.get('shape','rectangle'),'recess':opening.get('recess',-.15),
                           'bottom':opening.get('bottom',.20),'height':opening.get('height',2.0),
                           'frame':opening.get('frame','black iron'),'trim':opening.get('trim','cream stone'),
                           'grille':opening.get('grille',False),'rails':opening.get('rails',[])})
    for door in spec.get('groundDoors',[]):
        fidelity_door(f,door)
    for unit in spec.get('blankGround',[]):
        design=deepcopy(unit['design'])
        photographed_shop(f,unit['span'][0]*f.L,unit['span'][1]*f.L,{'design':design,'name':''})
        aw=unit.get('awning')
        if aw:
            a=unit['span'][0]*f.L;bb=unit['span'][1]*f.L;y=aw.get('y',2.95);drop=aw.get('drop',.35)
            count=max(2,round((bb-a)/.27))
            for j in range(count):
                l=a+(bb-a)*j/count;r=a+(bb-a)*(j+1)/count
                mat=aw.get('material','seventh shop blue') if j%2 else aw.get('stripe','sign white')
                face([f.p(l,y-drop,aw.get('depth',.46)),f.p(r,y-drop,aw.get('depth',.46)),
                      f.p(r,y,.05),f.p(l,y,.05)],mat)
                f.b((l+r)/2,y-drop-aw.get('valance',.14)/2,aw.get('depth',.47),
                    r-l,aw.get('valance',.14),.025,mat)
            if aw.get('topMaterial'):
                f.b((a+bb)/2,y+.025,.06,bb-a,.07,.06,aw['topMaterial'])
            if aw.get('text'):
                sign_text(f,(a+bb)/2,y-drop-aw.get('valance',.14)*.5,bb-a-.12,
                          aw['text'],aw.get('textMaterial','sign white'),aw.get('textSize',.16),
                          aw.get('depth',.46)+.03)
    # These surfaces sit in front of the wall, so every window and door must
    # have registered first.  Split them around the recesses instead of
    # drawing an opaque slab across the newly modeled glass.
    if tile:
        surface_depth=tile.get('depth',.045);surface_thickness=tile.get('thickness',.018)
        grout=tile.get('grout','seventh grey painted stone')
        fidelity_clipped_surface(f,0,f.L,0,tile_h,surface_depth,surface_thickness,material_name)
        for x in range(1,cols):
            xx=f.L*x/cols
            fidelity_clipped_surface(f,xx-.009,xx+.009,0,tile_h,surface_depth+.014,.012,grout)
        for y in range(1,rows):
            yy=tile_h*y/rows
            fidelity_clipped_surface(f,0,f.L,yy-.009,yy+.009,surface_depth+.014,.012,grout)
    for band in spec.get('baseBands',[]):
        width=f.L*band.get('width',1);center=f.L*band.get('at',.5)
        fidelity_clipped_surface(f,center-width/2,center+width/2,
            band.get('y',.55)-band.get('height',.86)/2,
            band.get('y',.55)+band.get('height',.86)/2,
            band.get('depth',.03),band.get('thickness',.08),
            band.get('material','seventh shop blue'),.025)
    awnings=list(spec.get('groundAwnings',[]))
    if spec.get('groundAwning'):awnings.append(spec['groundAwning'])
    for aw in awnings:
        a=(aw.get('at',.5)-aw.get('width',.3)/2)*f.L
        bb=(aw.get('at',.5)+aw.get('width',.3)/2)*f.L
        y=aw.get('y',3.1);drop=aw.get('drop',.35);d=aw.get('depth',.48)
        f.b((a+bb)/2,y-drop/2,d,bb-a,drop,.035,aw.get('material','theater red'))
        f.b((a+bb)/2,y-drop-.08,d,bb-a,.16,.035,aw.get('material','theater red'))
        if aw.get('text'):
            sign_text(f,(a+bb)/2,y-drop-.04,bb-a-.08,aw['text'],
                      aw.get('textMaterial','sign white'),aw.get('textSize',.13),d+.04)
    for at in spec.get('lanterns',[]):
        s=at*f.L
        f.b(s,2.45,.30,.12,.22,.12,'opal lamp')
        f.line((s,2.34,.28),(s,2.63,.28),.018,'black iron')
    for well in spec.get('basementAreaways',[]):
        at=well.get('at',.5)*f.L;width=well.get('width',.34)*f.L;depth=well.get('depth',.92)
        material_name=well.get('material','seventh sandstone')
        below=well.get('depthBelow',.46);rim=.06
        # The well is an open descent: side and street-edge curbs only, with
        # treads falling from the sidewalk toward the facade and a real floor.
        for x in [at-width/2+rim/2,at+width/2-rim/2]:
            f.b(x,.02,depth/2,rim,.12,depth,material_name)
        f.b(at,.02,depth-rim/2,width-rim*2,.12,rim,material_name)
        count=max(0,well.get('steps',2));floor_depth=max(.18,depth*.24)
        inner_edge=.04+floor_depth;stair_depth=max(.04,depth-rim-inner_edge)
        f.b(at,-below,.04+floor_depth/2,width-rim*2,.08,floor_depth,material_name)
        for j in range(count):
            yy=-below*(j+.5)/count
            d=depth-rim-(j+.5)*stair_depth/count
            f.b(at,yy,d,width-rim*2,.08,stair_depth/count+.012,material_name)
        for side in [-1,1]:
            x=at+side*(width/2-.03)
            f.line((x,.12,.10),(x,1.24,depth+.10),.021,'black iron')
            f.line((x,1.24,depth+.10),(x,1.24,.10),.021,'black iron')
            for j in range(4):
                d=.10+(depth-.10)*j/3
                f.line((x,.12,d),(x,1.24,d),.011,'black iron')
        f.line((at-width/2+.03,1.24,depth+.10),(at+width/2-.03,1.24,depth+.10),.021,'black iron')
    for fence in spec.get('groundFences',[]):
        seventh_fence(f,f.L*fence['span'][0],f.L*fence['span'][1],fence.get('depth',.70))
    _observed_scaffold(f,spec)

def fidelity_elevation(b,f,r):
    f.wall=r.get('wall','warm brick');f.detail={};f.window_dressing=False
    ground=r.get('observedGround',OBSERVED_GROUND.get(str(b['id']),{}))
    replace_windows=ground.get('replaceWindows',bool(ground.get('groundOpenings')))
    replace_doors=ground.get('replaceDoors',bool(ground.get('groundDoors')))
    def overlaps_observed_opening(window):
        left=window['at']-window['width']/2;right=window['at']+window['width']/2
        bottom=window.get('bottom',0);top=bottom+window.get('height',0)
        observed_openings=list(ground.get('groundOpenings',[]))+[
            {**door,'height':door['top']-door.get('bottom',.19)} for door in ground.get('groundDoors',[])
        ]
        for observed in observed_openings:
            observed_left=observed['at']-observed['width']/2;observed_right=observed['at']+observed['width']/2
            observed_bottom=observed.get('bottom',.20);observed_top=observed_bottom+observed.get('height',2.0)
            if min(right,observed_right)-max(left,observed_left)>.001 and min(top,observed_top)-max(bottom,observed_bottom)>.001:return True
        return False
    for window in r.get('windows',[]):
        if replace_windows and window.get('bottom',99)<3.55:continue
        if replace_windows and overlaps_observed_opening(window):continue
        fidelity_window(f,window)
    for door in r.get('doors',[]):
        if replace_doors and door.get('bottom',99)<3.55:continue
        fidelity_door(f,door)
    # Register replacement openings before courses, piers and facade bands
    # are emitted, otherwise shallow masonry would close the new recesses.
    _observed_ground(f,b)
    suppressed_businesses=set(ground.get('suppressBusinessExteriorIds',[]))
    for shop in b.get('businesses',[]):
        if shop.get('street')!='East 7th Street' or not shop.get('renderName'):continue
        var_appearance=shop.get('appearance',{})
        if isinstance(var_appearance,dict) and var_appearance.get('record') in suppressed_businesses:continue
        a,end=shop['unit']
        # Keep explicitly scheduled entrances clear, including legacy units
        # whose old geocoded span covered the entire ground floor.
        effective_doors=(list(ground.get('groundDoors',[])) if replace_doors
                         else list(r.get('doors',[]))+list(ground.get('groundDoors',[])))
        for door in effective_doors:
            left=(door['at']-door['width']/2-.025)*f.L
            right=(door['at']+door['width']/2+.025)*f.L
            if a<right and end>left:
                if left-a>end-right:end=left
                else:a=right
        if end-a<.75:continue
        # Retain transparent shop glazing so the separately observed window
        # displays and deep entrances remain visible. Opaque sky-tinted glass
        # is confined to the architectural windows/door panes above.
        if shop.get('design',{}).get('facadePath'):fidelity_bayed_shop(f,a,end,shop)
        elif shop.get('design'):photographed_shop(f,a,end,shop)
        elif r.get('legacyShops',False):storefront(f,a,end,shop['name'].upper(),shop.get('awning'),shop.get('fascia','window frame'),shop.get('letters','sign white'))
    for rail in r.get('rails',[]):
        seventh_fence(f,rail['span'][0]*f.L,rail['span'][1]*f.L,rail.get('depth',1.10),rail.get('material','seventh worn iron'))
    for pier in r.get('piers',[]):
        s=pier['at']*f.L;y=(pier['bottom']+pier['top'])/2;hh=pier['top']-pier['bottom'];w=pier['width']*f.L;mat=pier['material']
        f.b(s,y,.06,w,hh,.16,mat)
        for yy in [pier['bottom']+.06,pier['top']-.06]:f.b(s,yy,.10,w+.09,.12,.24,mat)
        if pier.get('joints'):
            for j in range(1,math.ceil(hh/.48)):
                f.b(s,pier['bottom']+j*.48,.143,w,.015,.012,'sill patina')
    for band in r.get('bands',[]):f.strip(band['y'],band.get('height',.12),band.get('depth',.10),band.get('material','cream stone'))
    for zone in r.get('rustication',[]):fidelity_courses(f,zone['top'],zone['material'],zone.get('step',.44),zone.get('bottom',.18))
    for esc in r.get('escapes',[]):escape(f,esc['at']*f.L,esc['levels'],esc['width']*f.L,esc.get('material','black iron'))
    for balcony in r.get('balconies',[]):
        s=balcony['at']*f.L;w=balcony['width']*f.L;d=balcony['depth'];y=balcony['y']
        mat=balcony.get('material','black iron');height=balcony.get('height',.95)
        f.b(s,y,d/2,w,.14,d,balcony.get('floorMaterial','seventh weathered limestone'))
        for end in [-1,1]:
            x=s+end*w/2
            f.line((x,y,.04),(x,y+height,.04),.022,mat)
            f.line((x,y+height,.04),(x,y+height,d),.022,mat)
        f.line((s-w/2,y+height,d),(s+w/2,y+height,d),.025,mat)
        for j in range(max(2,round(w/.16))+1):
            x=s-w/2+w*j/max(2,round(w/.16))
            f.line((x,y,d),(x,y+height,d),.012,mat)
    for sign in r.get('signs',[]):observed_sign(f,0,f.L,sign)
    for aw in r.get('awnings',[]):observed_awning(f,aw['span'][0]*f.L,aw['span'][1]*f.L,aw)
    for blade in r.get('blades',[]):projecting_sign(f,0,f.L,blade)
    # Small explicitly observed facade fixtures; every coordinate is authored
    # in the record, without an automatic decoration/number-placement rule.
    for item in r.get('detailBoxes',[]):
        f.b(item['at']*f.L,item['y'],item.get('depth',.16),item['width'],item['height'],item.get('thickness',.08),item['material'])
    for item in r.get('detailLines',[]):
        a=item['from'];c=item['to'];f.line((a[0]*f.L,a[1],a[2]),(c[0]*f.L,c[1],c[2]),item.get('radius',.02),item['material'])
    for item in r.get('detailFaces',[]):
        face([f.p(v[0]*f.L,v[1],v[2]) for v in item['vertices']],item['material'])
    for item in r.get('busts',[]):
        # Small faceted bronze silhouette. Portrait likeness is not claimed.
        s=item['at']*f.L;y=item['y'];d=item['depth'];mat='east7 bronze'
        rod(f.p(s,y,d),f.p(s,y+.25,d),.25,mat,12,r2=.15)
        rod(f.p(s,y+.25,d),f.p(s,y+.35,d),.085,mat,10)
        for j in range(7):
            t0=-math.pi/2+j*math.pi/7;t1=-math.pi/2+(j+1)*math.pi/7
            for k in range(12):
                angle_a=k*math.tau/12;angle_b=(k+1)*math.tau/12
                face([f.p(s+math.cos(t)*math.cos(v)*.12,y+.48+math.sin(t)*.17,d+math.cos(t)*math.sin(v)*.12) for t,v in [(t0,angle_a),(t0,angle_b),(t1,angle_b),(t1,angle_a)]],mat)
    if r.get('cornice'):
        c=r['cornice'];fidelity_cornice(f,c.get('y',b['renderHeight']),c)
    for detail in r.get('ornaments',[]):
        s=detail['at']*f.L;y=detail['y'];size=detail.get('size',.16);mat=detail.get('material','cream stone')
        if detail['type']=='diamond':
            face([f.p(s-size,y,.085),f.p(s,y+size,.10),f.p(s+size,y,.085),f.p(s,y-size,.10)],mat)
        elif detail['type']=='panel':fidelity_panel(f,s,y,detail['width']*f.L,detail['height'],.12,mat,.045)
        elif detail['type'] in ['scroll','shell']:fidelity_relief(f,s,y,detail['width']*f.L,detail['height'],mat,detail['type'])
    for shop in r.get('unletteredUnits',[]):
        # Exact panel order may be observed while a present tenant is unknown.
        # A blank panel never acquires a guessed tenant or an archive business.
        photographed_shop(f,shop['span'][0]*f.L,shop['span'][1]*f.L,{'design':shop['design'],'name':''})
    for shop in r.get('returnShops',[]):
        # Avenue-addressed corner businesses can also have a photographed
        # Seventh return. Keep that face explicit rather than duplicating the
        # avenue design over the entire corner parcel.
        photographed_shop(f,shop['span'][0]*f.L,shop['span'][1]*f.L,
                          {'design':shop['design'],'name':shop['name']})
    for zone in r.get('surfaceZones',[]):
        fidelity_clipped_surface(f,zone['span'][0]*f.L,zone['span'][1]*f.L,zone.get('bottom',.18),zone['top'],.025,.022,zone['material'],.015)

_fidelity_previous_render=render_building
_fidelity_previous_detail=add_seventh_detail

def fidelity_tower(f,bottom,top,depth,mat):
    """Tower skin respects its registered openings instead of burying glazing."""
    fidelity_clipped_surface(f,0,f.L,bottom,top,0,.025,mat)
    for at in [0,f.L]:
        face([f.p(at,bottom,0),f.p(at,bottom,-depth),f.p(at,top,-depth),f.p(at,top,0)],mat)
    face([f.p(0,bottom,-depth),f.p(f.L,bottom,-depth),f.p(f.L,top,-depth),f.p(0,top,-depth)],mat)
    face([f.p(0,top,0),f.p(f.L,top,0),f.p(f.L,top,-depth),f.p(0,top,-depth)],mat)

def fidelity_spire(f,s,bottom,width,depth,top,mat='seventh slate roof'):
    corners=[(s-width/2,bottom,0),(s+width/2,bottom,0),
             (s+width/2,bottom,-depth),(s-width/2,bottom,-depth)]
    peak=(s,top,-depth/2)
    for a,c in zip(corners,corners[1:]+corners[:1]):
        face([f.p(*a),f.p(*c),f.p(*peak)],mat)
        f.line(a,peak,.025,'seventh weathered limestone')
    f.line((s,top-.08,-depth/2),(s,top+.68,-depth/2),.03,'brass')
    f.line((s-.22,top+.43,-depth/2),(s+.22,top+.43,-depth/2),.026,'brass')

def fidelity_east_church(b,r):
    owner(r['profile']);b['renderHeight']=r['bodyHeight'];wall_mass(b,r['wall'],False)
    f=main_front(b,'East 7th Street');fidelity_elevation(b,f,r)
    if r['profile']=='east-stanislaus':
        stone='seventh pale limestone';wall=r['wall']
        gable(f,16.7,22.1,wall,stone)
        # Paired upper lancets and three double timber portals are in the
        # explicit schedule. These independent piers continue into the tower.
        for at in [.018,.35,.65,.982]:
            top=23.0 if at in [.35,.65] else 17.0
            f.b(at*f.L,top/2,.15,.32,top,.36,stone)
            for yy in [6.0,13.9,16.6]:f.b(at*f.L,yy,.24,.49,.16,.48,stone)
        for yy in [6.55,6.80]:f.strip(yy,.13,.22,stone)
        for j in range(42):
            x=(j+.5)*f.L/42
            fidelity_relief(f,x,6.67,.23,.19,stone,'shell')
        tower_w=f.L*.31;point=f.p((f.L-tower_w)/2,0,.12)
        tf=Facade(point[0],point[2],f.rx,f.rz,tower_w);tf.wall=wall
        for at in [.27,.73]:
            fidelity_window(tf,{'at':at,'width':.34,'bottom':22.05,'height':4.50,
                'shape':'round','hood':'round','frame':'seventh dark sandstone',
                'trim':stone,'rails':[],'glassMaterial':'recess shadow','recess':-.42})
        fidelity_tower(tf,18.8,28.05,4.8,wall)
        for yy in [20.6,21.05,27.1,27.48,28.0]:tf.strip(yy,.16,.23,stone)
        for at in [.08,.25,.42,.59,.76,.93]:
            fidelity_shaped_arc(tf,at*tower_w,19.15,tower_w*.065,.52,.065,.045,stone,'pointed')
        fidelity_spire(tf,tower_w/2,28.12,tower_w*.92,4.7,37.8)
        for at in [.025,.975]:
            x=at*tower_w;tf.b(x,28.1,.02,.42,1.8,.48,stone)
            fidelity_spire(tf,x,29.0,.65,.70,31.1)
        for at in [.018,.982]:
            x=at*f.L;f.b(x,17.4,.02,.40,1.4,.45,stone)
            fidelity_spire(f,x,18.1,.56,.62,20.3)
        # Shallow peaked portal hood at the central entry, observed separately
        # from the tall pointed fanlight underneath it.
        for side in [-1,1]:f.line((f.L*.5+side*2.05,5.85,.25),(f.L*.5,7.15,.25),.09,stone)
        f.line((f.L*.5,7.10,.28),(f.L*.5,7.75,.28),.045,stone)
        f.line((f.L*.5-.22,7.52,.28),(f.L*.5+.22,7.52,.28),.040,stone)
    else:
        # 121's irregular, exposed stone has short courses; it is not the
        # pale smooth limestone of St Stanislaus. Relief depth is estimated.
        fidelity_courses(f,11.85,r['wall'],.20,.19,.025)
        f.strip(11.78,.16,.19,'seventh weathered limestone')
        tw=f.L*.36;point=f.p((f.L-tw)/2,0,-.10)
        tf=Facade(point[0],point[2],f.rx,f.rz,tw);tf.wall=r['wall']
        fidelity_window(tf,{'at':.5,'width':.47,'bottom':12.18,'height':1.72,
            'shape':'rectangle','hood':'flat','rails':[],'trim':'seventh weathered limestone',
            'frame':'black iron','glassMaterial':'recess shadow','recess':-.23})
        fidelity_tower(tf,11.85,14.7,2.9,r['wall'])
        for y in [12.30+j*.14 for j in range(11)]:tf.b(tw*.5,y,-.13,tw*.45,.035,.09,'seventh dark sandstone')
        for y in [14.44,14.68]:tf.strip(y,.11,.16,'seventh weathered limestone')
        fidelity_spire(tf,tw*.5,14.78,tw+.28,3.25,18.0)
    b['renderHeight']=r['height']

def render_building(b):
    r=b.get('seventhArchitecture')
    if not r or r.get('preserveRecipe'):return _fidelity_previous_render(b)
    if r.get('profile')=='church-house-50':return fidelity_church_house(b,r)
    if r.get('profile') in ['east-stanislaus','east-st-mary']:return fidelity_east_church(b,r)
    # Render other sides through their existing recipes. The deferred wall
    # generator sees the restored full footprint and our registered openings.
    fronts=b['frontages'];businesses=b.get('businesses',[])
    others=[(i,v) for i,v in enumerate(fronts) if v['street']!='East 7th Street']
    indices={old:new for new,(old,_) in enumerate(others)}
    b['frontages']=[v for _,v in others]
    b['businesses']=[{**p,'frontageIndex':indices[p['frontageIndex']]} for p in businesses if p['frontageIndex'] in indices]
    if 'height' in r:b['facadeSpec']['height']=r['height']
    try:_seventh_base_render(b)
    finally:b['frontages']=fronts;b['businesses']=businesses
    for v in fronts:
        if v['street']=='East 7th Street':fidelity_elevation(b,Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']),r)

def add_seventh_detail(b,schedule):
    r=b.get('seventhArchitecture')
    if r and not r.get('preserveRecipe'):
        # Retain separately observed shop-specific details (painted door relief,
        # hats, menu cases, benches); suppress generic residential additions.
        shop_record=deepcopy(next(e for e in schedule['elevations'] if e['buildingId']==b['id']))
        shop_record['features']={}
        temp=deepcopy(b)
        temp['facadeSpec']['elevations']['East 7th Street']['groundUse']='shops'
        _fidelity_previous_detail(temp,{'elevations':[shop_record]})
        return
    _fidelity_previous_detail(b,schedule)
