"""Photo-guided exceptions to the regular facade component system.

Loaded by build_neighborhood.py, using that module's mesh primitives. Roof pitches,
recesses and spire heights without measurements are explicit visual estimates.
"""
def arch(f,s,y,w,h,trim='brownstone',pointed=True,glass='window glass'):
    shoulder=y+h-w*(.65 if pointed else .5)
    coords=[(s-w/2,y),(s+w/2,y),(s+w/2,shoulder)]
    if pointed:
        for k in range(1,13):
            t=k/12;coords.append((s+w/2*(1-t),shoulder+(h+y-shoulder)*(1-(1-t)**1.6)))
        for k in range(1,13):
            t=k/12;coords.append((s-w/2*t,shoulder+(h+y-shoulder)*(1-t**1.6)))
    else:
        for k in range(1,21):
            a=k*math.pi/20;coords.append((s+math.cos(a)*w/2,shoulder+math.sin(a)*w/2))
    coords.append((s-w/2,y))
    points=[f.p(a,b,.10) for a,b in coords]
    # Triangulate in the facade's local plane to preserve the arch outline.
    verts=[Vector((a,b,0)) for a,b in coords[:-1]]
    for tri in tessellate_polygon([verts]):
        vv=[verts[k] if isinstance(k,int) else k for k in tri]
        face([f.p(v.x,v.y,.10) for v in vv],glass)
    for a,b in zip(coords,coords[1:]):f.line((a[0],a[1],.18),(b[0],b[1],.18),.095,trim)
    f.b(s,y-.10,.18,w+.26,.14,.29,trim)
    for dx in [-.22*w,.22*w]:f.line((s+dx,y+.06,.14),(s+dx,shoulder+.10,.14),.026,'window frame')
    for yy in [y+h*.32,y+h*.62]:f.b(s,yy,.14,w-.13,.039,.04,'window frame')

def gable(f,base,peak,wall='warm brick',trim='brownstone'):
    face([f.p(0,base,0),f.p(f.L,base,0),f.p(f.L/2,peak,0)],wall)
    f.line((-.12,base+.05,.16),(f.L/2,peak+.15,.16),.11,trim)
    f.line((f.L/2,peak+.15,.16),(f.L+.12,base+.05,.16),.11,trim)

def roof(x0,x1,z0,z1,eave,ridge,axis='x'):
    if axis=='x':
        zm=(z0+z1)/2
        face([(x0,eave,z0),(x1,eave,z0),(x1,ridge,zm),(x0,ridge,zm)],'roof')
        face([(x0,ridge,zm),(x1,ridge,zm),(x1,eave,z1),(x0,eave,z1)],'roof')
    else:
        xm=(x0+x1)/2
        face([(x0,eave,z0),(xm,ridge,z0),(xm,ridge,z1),(x0,eave,z1)],'roof')
        face([(xm,ridge,z0),(x1,eave,z0),(x1,eave,z1),(xm,ridge,z1)],'roof')

def pyramid(x,z,y,width,top,depth=None):
    depth=width if depth is None else depth
    points=[(x-width/2,y,z-depth/2),(x+width/2,y,z-depth/2),(x+width/2,y,z+depth/2),(x-width/2,y,z+depth/2)]
    for a,b in zip(points,points[1:]+points[:1]):face([a,b,(x,top,z)],'roof')
    rod((x,top-.10,z),(x,top+.95,z),.045,'cornice green',8)
    rod((x-.26,top+.65,z),(x+.26,top+.65,z),.034,'cornice green',8)

def main_front(b,street=None):
    fs=[v for v in b['frontages'] if not street or v['street']==street] or b['frontages']
    if not fs:return None
    v=max(fs,key=lambda v:v['length']);return Facade(v['x'],v['z'],v['rx'],v['rz'],v['length'])

def build_landmark(b,spec):
    kind=spec.get('landmark');wall=spec.get('wall','warm brick');bb=b['box'];x0,z0,x1,z1=bb
    special=['st_nicholas','st_stanislaus','st_cyril','st_mary','st_marks_church','joyce','school','east_side_school','ps122','orpheum','ottendorfer','dispensary','village_east','elizabeth','elizabeth_east','ruin','modern_bank','cast_iron']
    if kind not in special:return False
    if kind=='east_side_school':
        # NYC's actual H-shaped outline supplies both recessed courtyards. The
        # archive photograph shows grouped classroom glazing with stone frames.
        wall_mass(b,wall,False);h=b['renderHeight'];step=(h-.65)/5
        for v in b['frontages']:
            f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']);f.wall=wall
            f.window_dressing=False;f.window_frame='white frame'
            groups=max(1,round(f.L/6.0));pitch=f.L/groups
            entrance=f.L-3.8 if f.L>25 and v['street']=='East 12th Street' else None
            for row in range(5):
                y=.85+row*step
                for k in range(groups):
                    ss=(k+.5)*pitch;ww=min(4.1,pitch*.72);hh=step*.67
                    if row==0 and entrance is not None and abs(ss-entrance)<ww/2+1.5:continue
                    street_window(f,ss,y,ww,hh,'cream stone',0)
                    for j in range(1,4):f.b(ss-ww/2+j*ww/4,y+hh/2,.04,.055,hh,.10,'white frame')
                    for yy in [y+hh*.33,y+hh*.67]:f.b(ss,yy,.06,ww,.035,.05,'white frame')
                    if row>0:
                        for dx in [-ww/2-.16,ww/2+.16]:
                            for q in range(5):f.b(ss+dx,y+.25+q*hh/5,.03,.24 if q%2 else .34,.32,.19,'cream stone')
                if row in [0,3]:f.strip(y+step-.30,.12,.18,'cream stone')
            f.strip(h,.20,.30,'cream stone')
            if f.L<12:
                f.b(f.L/2,h+.35,.02,f.L-.45,.70,.20,wall)
                f.b(f.L/2,h+.76,.03,2.6,.60,.24,wall)
                f.strip(h+.73,.13,.26,'cream stone')
            elif entrance is not None:
                # The reference places the red entrance beside the western
                # projecting wing, not in the middle of a classroom window.
                arch(f,entrance,.19,2.2,3.8,'cream stone',False,'dark glass')
                for dx in [-.53,.53]:
                    f.b(entrance+dx,1.30,.23,1.02,2.22,.10,'theater red')
                    f.b(entrance+dx,2.18,.30,.76,.29,.035,'dark glass')
                    f.line((entrance+dx*.28,1.05,.31),(entrance+dx*.28,1.52,.31),.018,'metal')
                for dx in [-1.35,1.35]:
                    f.b(entrance+dx,1.8,.17,.37,3.25,.36,'cream stone')
                    f.b(entrance+dx,3.36,.23,.59,.20,.47,'cream stone')
                f.b(entrance,3.95,.17,3.15,.19,.38,'cream stone')
                label(f,entrance,3.15,1.8,'420','sign white',.20,.23)
                # A small identification plaque is an estimated modern sign.
                f.b(entrance-2.0,1.80,.17,.70,.62,.06,'cream stone')
                label(f,entrance-2.0,1.82,.62,'EAST SIDE','black iron',.095,.22)
                label(f,entrance-2.0,1.63,.62,'SCHOOL','black iron',.095,.22)
        return True
    if kind=='cast_iron':
        wall_mass(b,'cast iron facade');f=main_front(b,'First Avenue');h=b['renderHeight'];step=(h-3.85)/4
        for row in range(4):
            y=3.7+row*step
            for col in range(3):
                ss=(col+.5)*f.L/3;ww=f.L/3*.83
                street_window(f,ss,y,ww,min(2.7,step*.8),'cast iron facade',0)
                for dx in [-ww/6,ww/6]:f.b(ss+dx,y+step*.38,.17,.05,step*.76,.08,'cast iron facade')
            for col in range(4):f.b(col*f.L/3,y+step*.4,.16,.17,step*.82,.23,'cast iron facade')
            f.strip(y-.17,.24,.3,'cast iron facade')
        cornice(f,h,'cast iron facade',True);storefront(f,.1,f.L-.1,'',None,'cast iron facade');return True
    if kind=='st_nicholas':
        b['renderHeight']=16.5;wall_mass(b,'warm brick',False)
        box(189.4,18.55,17.2,13.2,4.1,15.6,'warm brick')
        box(198.65,20.45,13.9,5.7,9.0,7.5,'warm brick')
        roof(x0,182.8,11.5,25.4,16.5,21.0);roof(182.8,196,9.4,25,20.6,25.0,axis='z')
        pyramid(198.65,13.9,24.95,6.4,31.4,8.2)
        f=Facade(201.6,9.35,-1,0,34.1)
        for col in [4.3,8.2,12.9,17.5,21.2,25.3,29.6]:
            for row,y in enumerate([1.8,7.5,13.2]):
                if col>19 and row==2:continue
                local=Facade(f.x,12.20 if col in [12.9,17.5] else f.z,f.rx,f.rz,f.L)
                arch(local,col,y,1.6,3.1 if row<2 else 2.8,'brownstone')
        for y in [5.75,11.7,17.5]:f.strip(y,.16,.15,'brownstone')
        for start,w,eave,peak in [(12.2,13.2,20.6,25.0),(21.1,4.5,16.5,20.9),(28.0,4.4,16.5,20.8)]:
            gf=Facade(*[f.p(start-w/2,0,.05)[i] for i in [0,2]],f.rx,f.rz,w);gable(gf,eave,peak,'warm brick','brownstone');arch(gf,w/2,eave-.5,w*.42,2.5,'brownstone')
        for v in [Facade(201.67,17.2,0,-1,7.5),Facade(201.6,9.35,-1,0,5.7)]:
            for ss in [v.L*.30,v.L*.70]:arch(v,ss,21.5,1.25,2.65,'brownstone',True,'dark glass')
            v.strip(20.9,.24,.22,'brownstone')
        side=Facade(201.72,25.4,0,-1,8.2)
        gable(side,16,23.1,'warm brick','brownstone');arch(side,4.1,2.0,5.0,13.2,'brownstone')
        for xx in [168.3+i*.5 for i in range(65)]:rod((xx,.3,7.6),(xx,1.24,7.6),.025,'black iron',6)
        rod((168,.9,7.6),(201,.9,7.6),.027,'black iron',6)
        b['renderHeight']=31.4;return True
    if kind=='st_stanislaus':
        b['renderHeight']=16.7;wall_mass(b,'limestone facade',False);f=main_front(b,'East 7th Street')
        for ss in [f.L*.19,f.L*.50,f.L*.81]:arch(f,ss,1.15,2.20,4.8,'cream stone',True,'wood')
        for ss in [f.L*.18,f.L*.82]:arch(f,ss,8.0,2.3,6.2,'cream stone')
        arch(f,f.L*.5,7.7,3.6,7.4,'cream stone')
        gable(f,16.7,21.0,'limestone facade','cream stone')
        cx,_,cz=f.p(f.L*.5,0,-2.0);box(cx,22.4,cz,4.9,11.4,5.8,'limestone facade')
        tf=Facade(*[f.p(f.L*.5-2.45,0,.09)[i] for i in [0,2]],f.rx,f.rz,4.9)
        for ss in [1.35,3.55]:arch(tf,ss,22.2,1.2,3.9,'cream stone',True,'dark glass')
        pyramid(cx,cz,28.1,5.25,38,6.2)
        for ss in [.4,f.L-.4]:
            px,_,pz=f.p(ss,0,0);box(px,17.8,pz,.60,3,.60,'cream stone');pyramid(px,pz,19.3,.9,22.3)
        for k in range(6):f.b(f.L/2,.17+.09*k,2.1-k*.28,f.L-.5,.18*(k+1),.50,'cream stone')
        b['renderHeight']=38;return True
    if kind=='st_cyril':
        b['renderHeight']=15.5;wall_mass(b,'warm brick',False);f=main_front(b)
        for ss in [f.L*.17,f.L*.83]:arch(f,ss,.70,1.45,3.65,'cream stone',False,'wood')
        arch(f,f.L*.50,.9,2.12,7.3,'cream stone',False,'blue glass')
        for row,y in enumerate([9.1,12.1]):
            for ss in [.17,.5,.83]:street_window(f,f.L*ss,y,1.05,1.8,'brownstone')
        gable(f,15.5,16.65,'warm brick','brownstone');label(f,f.L*.83,3.35,1.15,'ST CYRIL','sign white',.13,.24)
        return True
    if kind=='st_mary':
        b['renderHeight']=11.9;wall_mass(b,'painted grey',False);f=main_front(b)
        for row,y in enumerate([1.0,4.65,8.0]):
            for ss in [.2,.5,.8]:arch(f,f.L*ss,y,1.15,2.65,'cream stone',False,'wood' if row==0 else 'window glass')
        f.strip(11.7,.3,.35,'cream stone');cx,_,cz=f.p(f.L/2,0,-2.5)
        box(cx,13.2,cz,2.65,3.0,3.3,'painted grey');pyramid(cx,cz,14.7,3.05,18.0,3.7)
        for k in range(5):f.b(f.L/2,.16+.1*k,1.7-k*.25,f.L-.45,.2*(k+1),.40,'cream stone')
        b['renderHeight']=19;return True
    if kind=='st_marks_church':
        b['renderHeight']=13.5;wall_mass(b,'painted grey',False);roof(x0,x1,z0,z1,13.5,19.5,'z')
        f=Facade(x1,z1,-1,0,x1-x0);gable(f,13.5,19.5,'painted grey','cream stone')
        for y in [3,8.2]:
            for ss in [.2,.5,.8]:arch(f,f.L*ss,y,2.4,3.6,'cream stone',False)
        for ss in [f.L*.12,f.L*.37,f.L*.63,f.L*.88]:
            px,_,pz=f.p(ss,0,2.8);rod((px,.2,pz),(px,5.8,pz),.23,'cream stone',12)
        f.b(f.L/2,5.9,1.6,f.L,.34,3.4,'cream stone')
        cx,_,cz=f.p(f.L/2,0,-4);box(cx,21,cz,5.8,7.5,6.5,'cream stone');pyramid(cx,cz,24.7,6.3,40,6.7)
        b['renderHeight']=41;return True
    if kind in ['joyce','school','ps122','modern_bank']:
        wall_mass(b,wall,False);h=b['renderHeight'];floors=spec.get('floors',b['floors'])
        for v in b['frontages']:
            f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']);cols=max(2,round(f.L/(4.6 if kind=='joyce' else 3.8)))
            for row in range(floors):
                y=.7+row*(h-.7)/floors
                for col in range(cols):
                    ss=(col+.5)*f.L/cols;ww=min(2.6,f.L/cols*.61);hh=min(2.3,(h-1)/floors*.62)
                    if kind=='ps122' and row==floors-1:arch(f,ss,y,ww,hh,'brownstone',False)
                    else:street_window(f,ss,y,ww,hh,'painted grey' if kind=='joyce' else 'cream stone',0)
            if kind=='joyce' and v['street']=='Avenue A':
                for ss in [f.L*.60,f.L*.77,f.L*.92]:
                    street_window(f,ss,h-10,1.4,5.0,'painted grey',0)
            if kind=='ps122':cornice(f,h,'brownstone',True)
            else:f.strip(h,.22,.23,wall)
            doorway(f,f.L*.35,b['address'].split(' ')[0],False,'cream stone')
        if kind=='joyce':
            for x in [x0,x1]:
                for z in [z0+i*2 for i in range(max(1,int((z1-z0)/2)))]:rod((x,h,z),(x,h+2.2,z),.028,'metal',6)
                for y in [h+.5,h+1.15,h+2.2]:rod((x,y,z0),(x,y,z1),.018,'metal',6)
        return True
    if kind in ['orpheum','ottendorfer','dispensary','village_east']:
        f=main_front(b,'Second Avenue');h=b['renderHeight'];L=f.L
        if kind=='village_east':
            b['renderHeight']=13.8;wall_mass(b,wall,False)
            # The mapped top is the rear auditorium, not the pale street-front wing.
            box(-269.1,11.95,-129.8,21.3,23.9,22.0,'warm brick')
            f.b(L*.80,15.75,-3.0,8.2,3.9,6.2,'limestone facade')
            for ss in [.075,.20,.325,.45,.95]:
                arch(f,L*ss,.8,2.65,6.1,'cream stone',False,'dark glass')
                for dx in [-.50,.50]:arch(f,L*ss+dx,9.1,.76,2.0,'cream stone',False)
            for ss in [.58,.80]:
                if ss==.58:
                    for dx in [-.5,.5]:arch(f,L*ss+dx,9.1,.76,2,'cream stone',False)
            arch(f,L*.80,7.0,5.8,8.65,'cream stone',False)
            f.strip(6.5,.23,.30,'cream stone')
            f.b(L*.32,13.5,.15,L*.64,.23,.30,'cream stone');f.b(L*.9675,13.5,.15,L*.065,.23,.30,'cream stone')
            storefront(f,L*.62,L*.935,'VILLAGE EAST',None,'black iron')
            f.b(L*.79,4.3,1.25,L*.31,1.7,2.55,'black iron')
            label(f,L*.79,4.4,L*.285,'VILLAGE EAST','sign white',.58,2.55)
            # The cornermost return has two tall arches and paired upper windows.
            side=main_front(b,'East 12th Street')
            for ss in [2.65,6.85]:
                arch(side,ss,.8,2.55,6.1,'cream stone',False,'dark glass')
                for dx in [-.5,.5]:arch(side,ss+dx,9.1,.76,2,'cream stone',False)
            side.strip(6.5,.23,.30,'cream stone');side.strip(13.5,.23,.30,'cream stone')
            blade=Facade(*[f.p(L*.64,0,1.7)[i] for i in [0,2]],f.nx,f.nz,1.9)
            blade.b(.9,5.5,0,1.8,4.5,.22,'black iron')
            back=Facade(*[blade.p(1.9,0,-.13)[i] for i in [0,2]],-blade.rx,-blade.rz,1.9)
            for j,ch in enumerate('VILLAGE'):
                label(blade,.9,7.25-j*.56,1.4,ch,'sign white',.48,.15);label(back,.9,7.25-j*.56,1.4,ch,'sign white',.48,.03)
            b['renderHeight']=23.9;return True
        wall_mass(b,wall,False)
        cols=3 if kind!='dispensary' else 7;floors=2 if kind=='orpheum' else 3
        trim='red terra cotta' if kind!='orpheum' else 'cream stone'
        positions=[.075,.22,.37,.5,.63,.78,.925] if kind=='dispensary' else [(i+.5)/cols for i in range(cols)]
        if kind=='dispensary':
            f.b(L*.5,h*.5,.10,L*.40,h-.3,.19,'weathered red')
            for x in [L*.285,L*.715]:f.b(x,h*.5,.28,.24,h,.36,'red terra cotta')
        for row in range(floors-1):
            for col in range(cols):
                af=f
                if kind=='dispensary' and col in [2,3,4]:af=Facade(f.x+f.nx*.20,f.z+f.nz*.20,f.rx,f.rz,f.L)
                arch(af,positions[col]*L,4.25+row*4.1,min(2.4 if kind=='orpheum' else 1.8,L/cols*.76),4.55 if kind=='orpheum' else 3.1,trim,False)
            f.strip(4.1+row*4.1,.22,.26,trim)
        cornice(f,h,trim,True)
        if kind=='orpheum':
            storefront(f,.1,L-.1,'ORPHEUM',None,'black iron');f.b(L/2,3.35,1.02,L-.15,.65,2.1,'black iron');label(f,L/2,3.4,L-.7,'ORPHEUM','sign white',.48,2.1);gable(f,h,h+1.0,'warm brick','cream stone')
        elif kind=='ottendorfer':arch(f,L*.5,.45,L*.76,3.6,trim,False,'wood');label(f,L/2,3.95,L-.3,'FREIE BIBLIOTHEK','red terra cotta',.29,.30)
        else:arch(f,L*.5,.6,2.8,3.6,trim,False,'wood');label(f,L/2,4.1,L*.7,'GERMAN DISPENSARY','red terra cotta',.24,.32)
        return True
    if kind in ['elizabeth','elizabeth_east']:
        b['renderHeight']=15.0;wall_mass(b,'warm brick',False);f=main_front(b)
        if not f:return True
        for y in [1.2,5.0,8.9]:
            for ss in [.23,.64]:street_window(f,f.L*ss,y,1.45,2.4,'brownstone',1)
        if kind=='elizabeth':
            roof(x0,x1,z0,z1,15,18)
            for ss in [.25,.7]:
                ff=Facade(*[f.p(f.L*ss-.8,0,-.45)[i] for i in [0,2]],f.rx,f.rz,1.6);ff.b(.8,16.1,0,1.7,2.4,1.5,'warm brick');street_window(ff,.8,15.2,1,1.4,'brownstone');gable(ff,17.3,18.1,'warm brick','brownstone')
            box(x1-.4,18.3,z1-2,1,6.6,1.25,'warm brick')
            f.b(f.L-.15,4.5,1.1,3.5,.35,2.4,'brownstone');doorway(f,f.L-.20,'307',True,'brownstone')
            for k in range(10):f.line((f.L-1.7+k*.32,4.6,2.1),(f.L-1.7+k*.32,5.5,2.1),.035,'brownstone')
        else:
            for k in range(4):
                width=f.L-k*1.2;f.b(f.L/2,15.0+k*.72,0,width,.78,.4,'warm brick')
            for ss in [.27,.69]:arch(f,f.L*ss,15.2,1.05,1.65,'brownstone',False)
            b['renderHeight']=18.5
        return True
    if kind=='ruin':
        b['renderHeight']=3.4;wall_mass(b,'weathered red',False)
        for v in b['frontages']:
            f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length']);f.strip(1.4,2.4,.2,'painted grey')
        return True
    return False
