"""Observed frontage components, installed in the neighborhood recipe namespace.

Only explicit storefront-details.json records invoke these components. Sizes,
depths, typeface substitutions and movable-object positions remain estimates.
No reference photographs are copied into textures or into the distributed game.
"""
from mathutils import Matrix

material('neon amber', (1.0,.27,.025), .32, emission=3)
material('neon rose', (1.0,.23,.16), .32, emission=2)
material('lit sign white', (.92,.86,.69), .48, emission=.45)
material('store teal', (.055,.26,.22), .66)
material('neon orange', (.95,.075,.003), .4, emission=.85)
SIGN_FONT = bpy.data.fonts.load(str(ROOT/'model-source/fonts/Damion-Regular.ttf'))

def sign_text(f,s,y,w,text,mat,size=.28,d=.3,style='plain'):
    if not text:return
    if style=='plain':label(f,s,y,w,text,mat,size,d);return
    curve=bpy.data.curves.new('Observed sign lettering','FONT')
    curve.body=text;curve.size=size;curve.align_x='CENTER';curve.align_y='CENTER'
    curve.resolution_u=5;curve.extrude=.002
    if style in ['script','neon-script']:curve.font=SIGN_FONT
    if style in ['outline','neon-script']:
        curve.fill_mode='NONE';curve.bevel_depth=.009;curve.bevel_resolution=2
    obj=bpy.data.objects.new(ns['OWNER']+' / '+text,curve);bpy.context.collection.objects.link(obj)
    x,yy,z=f.p(s,y,d);obj.location=(x,-z,yy)
    obj.rotation_euler=Matrix((Vector((f.rx,-f.rz,0)),Vector((0,0,1)),Vector((f.nx,-f.nz,0)))).transposed().to_euler()
    obj.data.materials.append(MATS[mat]);bpy.context.view_layer.update()
    width=max(v[0] for v in obj.bound_box)-min(v[0] for v in obj.bound_box)
    if width>w:curve.size*=w/width

def sign_panel(f,s,y,w,h,depth,mat,shape='rectangle'):
    if shape=='rectangle':f.b(s,y,depth,w,h,.10,mat);return
    # Elliptic panel and its thickness; same primitive also gives circular blades.
    points=[(s+math.cos(i*math.tau/40)*w/2,y+math.sin(i*math.tau/40)*h/2) for i in range(40)]
    for (x0,y0),(x1,y1) in zip(points,points[1:]+points[:1]):
        face([f.p(s,y,depth+.05),f.p(x0,y0,depth+.05),f.p(x1,y1,depth+.05)],mat)
        face([f.p(x0,y0,depth-.05),f.p(x1,y1,depth-.05),f.p(x1,y1,depth+.05),f.p(x0,y0,depth+.05)],mat)

def observed_sign(f,a,b,sign):
    w=(b-a)*sign.get('width',.94);s=a+(b-a)*sign.get('at',.5)
    y=sign.get('y',2.96);h=sign.get('height',.52);depth=sign.get('depth',.23)
    mat=sign.get('material','black iron');shape=sign.get('shape','rectangle')
    if sign.get('panel',True):sign_panel(f,s,y,w,h,depth,mat,shape)
    for line in sign.get('lines',[]):
        sign_text(f,s+line.get('offset',0)*w,y+line.get('y',0)*h,w*line.get('width',.94),line['text'],
                  line.get('material','sign white'),line.get('size',h*.56),depth+.063,line.get('style','plain'))
    if sign.get('border'):
        if shape=='rectangle':
            for yy in [y-h/2+.035,y+h/2-.035]:f.b(s,yy,depth+.063,w-.07,.025,.012,sign['border'])
        else:
            for k in range(48):
                t=k*math.tau/48;u=(k+1)*math.tau/48
                f.line((s+math.cos(t)*(w/2-.045),y+math.sin(t)*(h/2-.045),depth+.065),(s+math.cos(u)*(w/2-.045),y+math.sin(u)*(h/2-.045),depth+.065),.013,sign['border'])

def projecting_sign(f,a,b,sign):
    s=a+(b-a)*sign.get('at',.90);y=sign.get('y',3.16)
    w=sign.get('width',.78);h=sign.get('height',.78);d=.22+w/2
    for yy in [y-h*.30,y+h*.30]:f.line((s,yy,.03),(s,yy,d),.025)
    x,_,z=f.p(s,y,.22)
    # Local right follows the projection, so each side is visible along the street.
    side=Facade(x,z,f.nx,f.nz,w)
    spec={**sign,'at':.5,'width':1,'depth':0}
    observed_sign(side,0,w,spec)
    x,_,z=f.p(s,y,.22+w)
    other=Facade(x,z,-f.nx,-f.nz,w)
    observed_sign(other,0,w,spec)

def observed_awning(f,a,b,aw):
    a+=(b-a)*aw.get('inset',0);b-=(b-a)*aw.get('inset',0)
    y=aw.get('y',3.10);drop=aw.get('drop',.50);depth=aw.get('depth',1.12);valance=aw.get('valance',.20)
    mat=aw.get('material','awning green');n=max(1,math.ceil((b-a)/aw.get('stripeSpacing',.17)))
    sections=10 if aw.get('shape')=='round' else 1
    for k in range(n):
        l=a+(b-a)*k/n;r=a+(b-a)*(k+1)/n
        sw=min(aw.get('stripeWidth',.012),(r-l)*.20)
        bands=[(l,r,mat)] if not aw.get('stripe') else [(l,l+sw,aw['stripe']),(l+sw,r,mat)]
        for l,r,m in bands:
            for j in range(sections):
                def pt(s,t):
                    if sections>1:return f.p(s,y-drop*(1-math.cos(t*math.pi/2)),.10+depth*math.sin(t*math.pi/2))
                    return f.p(s,y-drop*t,.10+depth*t)
                face([pt(l,j/sections),pt(r,j/sections),pt(r,(j+1)/sections),pt(l,(j+1)/sections)],m)
            f.b((l+r)/2,y-drop-valance/2,.10+depth,r-l,valance,.035,m)
        if aw.get('scalloped'):
            for j in range(6):
                t=j*math.pi/6;u=(j+1)*math.pi/6;c=(l+r)/2;rad=(r-l)/2
                face([f.p(c,y-drop-valance,.12+depth),f.p(c+math.cos(t)*rad,y-drop-valance-math.sin(t)*.06,.12+depth),f.p(c+math.cos(u)*rad,y-drop-valance-math.sin(u)*.06,.12+depth)],m)
    for s in [a+.07,b-.07]:f.line((s,y-.08,.06),(s,y-drop-.06,.08+depth),.016)
    sign_text(f,a+(b-a)*aw.get('textAt',.5),y-drop-valance*.52,(b-a)*aw.get('textWidth',.94),aw.get('text',''),aw.get('letters','sign white'),aw.get('textSize',.23),depth+.135)

def display_board(f,s,d,text='',mat='wood',paper='black iron',height=1.05,width=.57):
    # Hinged A-frame with two leg pairs, frame, panel and hinge hardware.
    for side in [-1,1]:
        for dx in [-width/2,width/2]:f.line((s+dx,.18,d+side*.28),(s+dx,height+.18,d),.023,mat)
        for y in [.35,height+.08]:f.b(s,y,d+side*.06,width,.043,.048,mat)
        f.b(s,height*.56+.18,d+side*.067,width-.065,height*.71,.028,paper)
    f.line((s-width/2,height+.19,d),(s+width/2,height+.19,d),.017,'metal')
    if text:sign_text(f,s,height*.78+.18,width-.11,text,'sign white',.10,d+.089)
    for k in range(4):f.b(s,height*.60+.14-k*.075,d+.089,width*.63,.015,.006,'sign white')

def shop_bench(f,s,d,w,mat='wood'):
    for k in range(4):f.b(s,.62,d+(k-1.5)*.10,w,.055,.086,mat)
    for dx in [-w*.40,w*.40]:
        for dz in [-.15,.15]:f.line((s+dx,.18,d+dz),(s+dx,.59,d+dz),.025,'black iron')

def cafe_table(f,s,d,style='red'):
    mat='theater red' if style=='red' else 'wood'
    # Small folding bistro table and two slatted folding chairs, recorded only
    # where photos actually show seating. Counts/placement remain date-specific.
    if style=='red':
        rod(f.p(s,.875,d),f.p(s,.92,d),.31,mat,24)
    else:f.b(s,.90,d,.58,.045,.58,mat)
    for side in [-1,1]:
        f.line((s-.22,.18,d+side*.20),(s+.22,.89,d+side*.20),.018,mat)
        f.line((s+.22,.18,d+side*.20),(s-.22,.89,d+side*.20),.018,mat)
        cs=s+side*.65
        for k in range(4):f.b(cs,.64,d+(k-1.5)*.085,.38,.025,.069,mat)
        for dd in [-.15,.15]:
            for dx in [-.16,.16]:f.line((cs+dx,.18,d+dd),(cs-dx,.63,d+dd),.012,mat)
        for yy in [.81,.91,1.01]:f.b(cs+side*.18,yy,d,.035,.065,.37,mat)
        for dd in [-.16,.16]:f.line((cs+side*.18,.50,d+dd),(cs+side*.18,1.06,d+dd),.014,mat)

def diamond_grille(f,a,b,low,high,depth,mat='black iron'):
    # Clip diagonal security bars to each window, keeping the doorway open.
    for slope in [-1.65,1.65]:
        for i in range(-30,31):
            intercept=low+i*.38
            pts=[]
            for x in [a,b]:
                y=intercept+slope*(x-a)
                if low<=y<=high:pts.append((x,y,depth))
            for y in [low,high]:
                x=a+(y-intercept)/slope
                if a<x<b:pts.append((x,y,depth))
            if len(pts)==2:f.line(pts[0],pts[1],.012,mat)

def photographed_shop(f,a,b,r):
    spec=r['design'];w=b-a;c=(a+b)/2
    if w<.75:return
    top=spec.get('top',3.3);frame=spec.get('frame','window frame');base=spec.get('base',.40)
    surround=spec.get('surround',frame);head=spec.get('head',2.61);depth=spec.get('recess',.13)
    OPENINGS[frontage_key(f)].append((a,.17,b,top))
    # Separate frame, piers, kick panels, glass and reveals. Unseen interiors
    # use a dark backing instead of borrowing another restaurant's room.
    f.b(c,(top+.17)/2,-.85,w,top-.17,.045,'dark glass')
    f.b(c,top-.11,.04,w,.22,.28,surround)
    for s in [a+.08,b-.08]:f.b(s,(top+.17)/2,.04,.16,top-.17,.30,surround)
    left=a+.16;usable=w-.32
    for kind,fraction in spec['panels']:
        right=left+usable*fraction;ww=right-left;ss=(left+right)/2
        is_door=kind in ['door','double-door']
        bottom=spec.get('doorGlassBottom',.20) if is_door else base
        panel_head=spec.get('doorHead',head) if is_door else head
        panel_mat=spec.get('doorMaterial',surround) if is_door else surround
        dd=-depth if is_door else spec.get('windowDepth',.035)
        for edge in [left,right]:f.b(edge,(panel_head+.20)/2,dd+.025,.065,panel_head-.20,.13,frame)
        f.b(ss,panel_head,dd+.025,ww,.070,.13,frame)
        f.b(ss,(panel_head+bottom)/2,dd-.022,max(.1,ww-.065),panel_head-bottom-.07,.018,'store glass')
        f.b(ss,(bottom+.17)/2,dd+.04,ww,max(.04,bottom-.17),.15,panel_mat)
        if kind in ['door','double-door']:
            f.b(ss,.26,.20,ww,.12,.56,'cream stone')
            doors=2 if kind=='double-door' else 1
            for k in range(doors):
                ds=left+ww*(k+.5)/doors
                if doors==2:f.b(ss,1.42,dd+.045,.065,2.32,.13,frame)
                f.b(ds,.54,dd+.058,ww/doors-.10,.36,.048,panel_mat)
                pull=ds+ww/doors*.30
                f.line((pull,1.06,dd+.15),(pull,1.48,dd+.15),.016,'brass')
                for yy in [.70,2.0]:f.b(ds-ww/doors*.43,yy,dd+.1,.035,.09,.035,'metal')
        if spec.get('smallPanes'):
            for k in range(1,4):f.b(ss,bottom+(head-bottom)*k/4,dd+.075,ww,.035,.045,frame)
            f.b(ss,(head+bottom)/2,dd+.075,.035,head-bottom,.045,frame)
        if spec.get('grille') and kind not in ['door','double-door']:diamond_grille(f,left,right,base,head,dd+.12)
        if spec.get('transom',True):
            f.b(ss,(head+top-.25)/2,dd,ww,max(.08,top-.25-head),.024,'store glass')
            f.b(ss,top-.25,dd+.03,ww,.06,.12,frame)
        elif top>panel_head:
            f.b(ss,(top+panel_head)/2,.045,ww,top-panel_head,.17,panel_mat)
        if spec.get('tileBase') and not is_door:
            for iy in range(max(1,int((base-.17)/.11))):
                yy=.225+iy*.11
                for ix in range(max(1,int(ww/.11))):
                    xx=left+.055+ix*.11
                    f.b(xx,yy,dd+.123,.098,.097,.012,'store teal' if iy in [0,int((base-.17)/.11)-1] else 'shop burgundy')
        left=right
    for sign in spec.get('signs',[]):observed_sign(f,a,b,sign)
    if spec.get('awning'):observed_awning(f,a,b,spec['awning'])
    for sign in spec.get('blades',[]):projecting_sign(f,a,b,sign)
    for item in spec.get('windowText',[]):
        sign_text(f,a+w*item.get('at',.5),item.get('y',1.82),w*item.get('width',.6),item['text'],item.get('material','sign white'),item.get('size',.20),item.get('depth',.09),item.get('style','plain'))
    for at in spec.get('lights',[]):
        s=a+w*at;f.b(s,top+.10,.07,.12,.14,.08,'black iron')
        f.line((s,top+.10,.10),(s,top+.25,.40),.023)
        f.line((s,top+.25,.40),(s,top+.09,.59),.023)
        f.b(s,top+.06,.59,.24,.09,.23,'black iron');f.b(s,top+.01,.59,.19,.025,.18,'opal lamp')
    for board in spec.get('boards',[]):display_board(f,a+w*board['at'],board.get('depth',.95),board.get('text',''),board.get('frame','wood'),height=board.get('height',1.05))
    for bench in spec.get('benches',[]):shop_bench(f,a+w*bench['at'],bench.get('depth',.50),min(bench.get('width',1.3),w*.55),bench.get('material','wood'))
    for table in spec.get('tables',[]):cafe_table(f,a+w*table['at'],table.get('depth',1.05),table.get('style','red'))
    for menu in spec.get('menus',[]):
        s=a+w*menu['at'];ww=min(menu.get('width',.5),w*.27);h=menu.get('height',.70);y=menu.get('y',1.70)
        f.b(s,y,.17,ww+.08,h+.08,.045,frame);f.b(s,y,.20,ww,h,.018,'poster paper')
        for j in range(7):f.b(s,y+h*.36-j*h*.11,.214,ww*.78,.012,.007,'black iron')
    if spec.get('shutter'):
        for yy in [.30+i*.105 for i in range(22)]:
            f.b(c,yy,.20,w-.17,.038,.055,'metal')
            for j in range(int(w/.30)):f.b(a+.17+j*.30,yy+.04,.20,.035,.085,.055,'metal')
