"""Bounded First Avenue / St. Marks face adapter for the Godot slice only.

Stable building + frontage indices own the schedules. Geometry helpers are
shared with Seventh, but dispatch, observed-ground data and shop ownership are
explicit per face. Legacy and protected Seventh recipes never enter this path.
"""
from copy import deepcopy

material('first warm red brick', (.48,.19,.12), .93)
material('first pale buff brick', (.62,.57,.44), .94)
material('first pink stucco', (.60,.39,.36), .96)
material('first mustard paint', (.64,.43,.11), .88)
material('first teal paint', (.09,.29,.31), .87)
material('first maroon paint', (.30,.07,.065), .89)
material('first olive trim', (.32,.33,.24), .90)
material('first brown molding', (.34,.245,.18), .94)
material('first net veil', (.04,.055,.05), .98)
material('painted sage', (.43,.49,.40), .95)
material('seventh blue gray stone', (.39,.45,.47), .93)
material('stmarks white stucco', (.79,.80,.76), .96)
material('stmarks brown masonry', (.45,.37,.31), .96)
material('stmarks tan canvas', (.62,.51,.35), .96)
MATS['first net veil'].node_tree.nodes.get('Principled BSDF').inputs['Alpha'].default_value = .30

FIRST_STMARKS_PROTECTED = {241822226,241829631,248142331,248142404,248142707}

def apply_first_stmarks_schedule(data, schedule):
    buildings = {b['id']: b for b in data['buildings']}
    seen = set()
    for record in schedule.get('elevations', []):
        key = record['faceId']
        bid, index = map(int, key.split(':'))
        if key in seen or bid in FIRST_STMARKS_PROTECTED:
            raise ValueError('Duplicate/protected First–St. Marks face: '+key)
        seen.add(key)
        b = buildings[bid]
        if b['frontages'][index] != record['sourceFace']:
            raise ValueError('Mapped face changed: '+key)
        if record['sourceFace']['street'] == 'East 7th Street':
            raise ValueError('Seventh must retain its accepted recipe: '+key)
        b.setdefault('firstStmarksArchitecture', {})[str(index)] = deepcopy(record['architecture'])
        spec = b.setdefault('facadeSpec', {})
        spec.setdefault('elevations', {}).setdefault(record['sourceFace']['street'], {})['wall'] = record['architecture']['wall']
        if record.get('buildingHeight') is not None:
            existing = b.get('firstStmarksHeight')
            if existing is not None and existing != record['buildingHeight']:
                raise ValueError('Conflicting corner heights: '+key)
            b['firstStmarksHeight'] = record['buildingHeight']

_first_stmarks_previous_render = render_building

def render_building(b):
    records = b.get('firstStmarksArchitecture')
    if not records:
        return _first_stmarks_previous_render(b)
    if b['id'] in FIRST_STMARKS_PROTECTED or b.get('seventhArchitecture'):
        raise ValueError('New adapter overlaps accepted Seventh: '+str(b['id']))
    fronts = b['frontages']; businesses = b.get('businesses', [])
    remaining = [(i, f) for i, f in enumerate(fronts) if str(i) not in records]
    remap = {old: new for new, (old, _) in enumerate(remaining)}
    b['frontages'] = [f for _, f in remaining]
    b['businesses'] = [{**p, 'frontageIndex': remap[p['frontageIndex']]}
                       for p in businesses if p['frontageIndex'] in remap]
    if 'firstStmarksHeight' in b:
        b['facadeSpec']['height'] = b['firstStmarksHeight']
    # Old generic landmark dispatch cannot recreate an explicitly scheduled
    # bank or house across the same faces. Retain all out-of-scope dispatch.
    landmark = b['facadeSpec'].pop('landmark', None)
    try:
        _first_stmarks_previous_render(b)
    finally:
        b['frontages'] = fronts; b['businesses'] = businesses
        if landmark is not None: b['facadeSpec']['landmark'] = landmark
    if b['id']==241822297:
        # The mapped footprint itself includes the narrow forward projection.
        # Split its mass at the observed join rather than raising it to the
        # mansard house's roof or drawing a floating cornice over empty space.
        PENDING_WALLS[:]=[p for p in PENDING_WALLS if p[0] is not b]
        for index,height,keep_greater in [(0,12.2,True),(1,10.25,False)]:
            polygon=_street_clip_polygon(b['p'],0,-189.4,keep_greater)
            clone={**b,'p':polygon,'frontages':[fronts[index]],'renderHeight':height}
            clone['facadeSpec']=deepcopy(b['facadeSpec'])
            clone['facadeSpec']['elevations']['St. Marks Place']['wall']=records[str(index)]['wall']
            PENDING_WALLS.append((clone,records[str(index)]['wall'],False,height))
    elif any(r.get('setbackMass') for r in records.values()):
        PENDING_WALLS[:]=[p for p in PENDING_WALLS if p[0] is not b]
        for index,r in records.items():
            spec=r.get('setbackMass')
            if not spec:continue
            v=fronts[int(index)];low=r['bodyHeight']
            PENDING_WALLS.append(({**b},r['wall'],False,low))
            z=v['z']+spec['setback']
            polygon=_street_clip_polygon(b['p'],1,z,True)
            vf={**v,'z':z}
            clone={**b,'p':polygon,'frontages':[vf],'renderHeight':spec['height']}
            PENDING_WALLS.append((clone,r['wall'],False,spec['height']))
            ff=Facade(vf['x'],vf['z'],vf['rx'],vf['rz'],vf['length']);ff.wall=r['wall']
            for row in range(spec['rows']):
                for at in [.16,.50,.84]:fidelity_window(ff,{'at':at,'width':.18,'bottom':low+.55+row*2.8,'height':1.85,'trim':'cream stone','frame':'black iron'})
            escape(ff,ff.L*.5,[low+.4+j*2.8 for j in range(3)],ff.L*.58,'black iron')
    for index, architecture in records.items():
        v = fronts[int(index)]
        f = Facade(v['x'], v['z'], v['rx'], v['rz'], v['length'])
        # Ground helpers read this field; a temporary per-face view keeps
        # corner overrides and old Seventh global fallbacks from leaking.
        face_building = {**b, 'businesses': [], 'seventhArchitecture': architecture}
        rendered=deepcopy(architecture)
        rendered['returnShops']=[shop for shop in architecture.get('returnShops',[]) if not shop.get('projection')]
        entry=architecture.get('entryProjection')
        projected_doors=[]
        if entry:
            projected_doors=[door for door in rendered.get('doors',[]) if entry['span'][0]<door['at']<entry['span'][1]]
            rendered['doors']=[door for door in rendered.get('doors',[]) if door not in projected_doors]
        if architecture.get('cornice',{}).get('pedimentAt') is not None:
            rendered['cornice']['pediment']=False
        fidelity_elevation(face_building, f, rendered)
        # Close the underside and retaining faces of new below-grade wells.
        # Thin tread slabs alone expose the sky through their vertical gaps
        # when the shared pavement is correctly cut away.
        for well in architecture.get('observedGround',{}).get('basementAreaways',[]):
            s=well['at']*f.L;width=well['width']*f.L;depth=well['depth'];below=well.get('depthBelow',.48);mat=well.get('material','seventh sandstone')
            f.b(s,-below-.10,depth/2,width,.10,depth,mat)
            for edge in [-1,1]:f.b(s+edge*(width/2-.03),-below/2,depth/2,.06,below+.10,depth,mat)
            f.b(s,-below/2,depth-.03,width,below+.10,.06,mat)
            f.b(s,-below/2,.025,width,below+.10,.05,mat)
            count=well.get('steps',3);floor_depth=max(.18,depth*.24);stair_depth=depth-.06-.04-floor_depth
            for j in range(count):
                top=-below*(j+.5)/count+.04;bottom=-below-.05;d=depth-.06-(j+.5)*stair_depth/count
                f.b(s,(top+bottom)/2,d,width-.12,top-bottom,stair_depth/count+.012,mat)
        if entry:
            a,end=[t*f.L for t in entry['span']];depth=entry['depth'];height=entry['height']
            projected=FidelityProjectedFacade(f,depth)
            for door in projected_doors:
                left=(door['at']-door['width']/2)*f.L;right=(door['at']+door['width']/2)*f.L
                for x1,x2 in [(a,left),(right,end)]:
                    f.b((x1+x2)/2,height/2,depth/2,x2-x1,height,depth,architecture['wall'])
                f.b((left+right)/2,(height+door['top'])/2,depth/2,right-left,height-door['top'],depth,architecture['wall'])
                fidelity_door(projected,door)
            f.b((a+end)/2,height+.06,depth/2,end-a+.13,.12,depth+.14,architecture['wall'])
        c=architecture.get('cornice',{})
        if c.get('pedimentAt') is not None:
            s=f.L*c['pedimentAt'];w=f.L*c.get('pedimentWidth',.20);h=c['y'];mat=c.get('material','cream stone')
            face([f.p(s-w/2,h+.10,.07),f.p(s+w/2,h+.10,.07),f.p(s,h+.72,.07)],mat)
            for side in [-1,1]:f.line((s+side*w/2,h+.13,.18),(s,h+.75,.18),.055,mat)
        for shop in architecture.get('returnShops',[]):
            if not shop.get('projection'):continue
            projected=FidelityProjectedFacade(f,shop['projection'])
            a,end=[t*f.L for t in shop['span']]
            photographed_shop(projected,a,end,shop)
            for s in [a,end]:
                f.b(s,1.5,shop['projection']/2,.08,2.6,shop['projection'],'seventh oak recess')
        if architecture.get('mansard'):
            roof=architecture['mansard'];low,high=roof['bottom'],roof['top']
            face([f.p(0,low,0),f.p(f.L,low,0),f.p(f.L,high,-1.3),f.p(0,high,-1.3)],'seventh slate roof')
            for at in roof['dormers']:
                s=at*f.L
                f.b(s,low+1.1,-.4,1.30,1.9,.8,'first brown molding')
                f.b(s,low+1.1,.035,.84,1.30,.04,'seventh reflective glass')
                f.b(s,low+1.12,.065,.055,1.30,.05,'white frame')
                f.b(s,low+2.08,-.30,1.65,.13,1.05,'seventh slate roof')
        if architecture.get('billboard'):
            r=architecture['billboard'];left,right=[v*f.L for v in r['span']];y=(r['bottom']+r['top'])/2
            f.b((left+right)/2,y,-.2,right-left,r['top']-r['bottom'],.12,'sign white')
            # Observed abstract linked-square artwork, authored geometry.
            for j in range(5):
                x=left+.3+(right-left-.6)*j/4;yy=y+(.48 if j%2 else -.48)
                fidelity_panel(f,x,yy,.30,.24,-.115,'first teal paint')
                if j:f.line((last_x,last_y,-.12),(x,yy,-.12),.023,'first teal paint')
                last_x,last_y=x,yy
        for w in architecture.get('windows', []):
            s=w['at']*f.L; width=w['width']*f.L; top=w['bottom']+w['height']
            if w.get('lowerMullion'):
                f.b(s,w['bottom']+w['height']*.37,-.055,.052,w['height']*.74,.08,w.get('frame','black iron'))
            if w.get('moldedHood'):
                mat=w['trim']
                for y,extra,hh,depth in [(top+.06,.16,.12,.22),(top+.20,.30,.11,.32),(top+.31,.42,.09,.39)]:
                    f.b(s,y,depth/2,width+extra,hh,depth,mat)
                for side in [-1,1]:f.b(s+side*(width/2+.07),top+.05,.12,.13,.32,.25,mat)
                if w.get('hood')=='pediment':
                    face([f.p(s-width/2-.20,top+.29,.205),f.p(s+width/2+.20,top+.29,.205),f.p(s,top+.64,.205)],mat)
                    for side in [-1,1]:f.line((s+side*(width/2+.24),top+.30,.23),(s,top+.69,.23),.052,mat)
        for guard in architecture.get('scaffoldGuards', []):
            low,high=guard['bottom'],guard['top'];depth=guard['depth']
            if guard.get('veil'):
                face([f.p(0,low,depth+.06),f.p(f.L,low,depth+.06),f.p(f.L,high,depth+.06),f.p(0,high,depth+.06)],'first net veil')
            if guard.get('angledSide') is not None:
                x=guard['angledSide']*f.L
                for j in range(4):
                    d=.10+depth*j/3
                    f.line((x,low,d),(x,low+1.30,d-.68),.065,'wood')
                f.line((x,low+1.30,-.58),(x,low+1.30,depth-.68),.08,'wood')
        for blind in architecture.get('shopBlinds', []):
            width=blind['width']*f.L;s=blind['at']*f.L
            for j in range(int(blind['height']/.055)):
                f.b(s,blind['bottom']+j*.055,-.035,width,.034,.026,'wood')
        for bottle in architecture.get('displayBottles', []):
            s=bottle['at']*f.L;y=bottle.get('bottom',.80);d=bottle.get('depth',.14)
            rod(f.p(s,y,d),f.p(s,y+.18,d),.038,bottle.get('material','awning green'),8)
            rod(f.p(s,y+.18,d),f.p(s,y+.26,d),.018,bottle.get('material','awning green'),8)
            f.b(s,y+.10,d+.039,.052,.07,.008,'sign white')
        for shutter in architecture.get('closedShutters', []):
            left,right = [x*f.L for x in shutter['span']]
            low,top = shutter.get('bottom',.2),shutter.get('top',2.9)
            f.b((left+right)/2,(low+top)/2,.07,right-left,top-low,.09,shutter.get('material','metal'))
            for j in range(int((top-low)/.095)):
                f.b((left+right)/2,low+j*.095,.126,right-left,.018,.015,'sill patina')
        if architecture.get('storefront09'):
            shop09_face(f,architecture['storefront09'])

def _street_clip_polygon(polygon,axis,boundary,greater):
    result=[]
    for a,c in zip(polygon,polygon[1:]+polygon[:1]):
        ia=(a[axis]>=boundary) if greater else (a[axis]<=boundary)
        ic=(c[axis]>=boundary) if greater else (c[axis]<=boundary)
        if ia:result.append(a)
        if ia!=ic:
            t=(boundary-a[axis])/(c[axis]-a[axis]);result.append([a[k]+(c[k]-a[k])*t for k in range(2)])
    return result
