"""First Avenue / East 10th Street: editable, metre-scale reconstruction.

Run with Blender 4.3+: blender -b -t 6 --python model-source/build_intersection.py
Coordinates follow the survey extract: x east across First, z south down First.
Facade schedules are authored from the photographs in references.json, not random.
Secondary street furniture and hidden surfaces are explicitly unsurveyed.
"""
import bpy, math, json, random, sys
import numpy as np
from pathlib import Path
from collections import defaultdict
from mathutils import Vector
from mathutils.geometry import tessellate_polygon

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist/reconstruction'
ASSETS = OUT / 'assets'
BASE = json.loads((ROOT/'model-source/intersection-base.json').read_text())
BUILDINGS = {b['id']: b for b in BASE['buildings']}
random.seed(110)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
MATS, BATCHES = {}, {}
OWNER = 'street'

def material(name, color, rough=.8, metal=0, texture=None, normal=None, emission=0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    bs = m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*color, 1)
    bs.inputs['Roughness'].default_value = rough
    bs.inputs['Metallic'].default_value = metal
    if texture and (ASSETS/texture).exists():
        tex = m.node_tree.nodes.new('ShaderNodeTexImage')
        tex.image = bpy.data.images.load(str(ASSETS/texture), check_existing=True)
        m.node_tree.links.new(tex.outputs['Color'], bs.inputs['Base Color'])
        rough_path=ASSETS/texture.replace('_diff_', '_rough_')
        if '_diff_' in texture and rough_path.exists():
            rr=m.node_tree.nodes.new('ShaderNodeTexImage')
            rr.image=bpy.data.images.load(str(rough_path),check_existing=True)
            rr.image.colorspace_settings.name='Non-Color'
            m.node_tree.links.new(rr.outputs['Color'],bs.inputs['Roughness'])
    if normal and (ASSETS/normal).exists():
        tex = m.node_tree.nodes.new('ShaderNodeTexImage')
        tex.image = bpy.data.images.load(str(ASSETS/normal), check_existing=True)
        tex.image.colorspace_settings.name = 'Non-Color'
        nm = m.node_tree.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = .32
        m.node_tree.links.new(tex.outputs['Color'], nm.inputs['Color'])
        m.node_tree.links.new(nm.outputs['Normal'], bs.inputs['Normal'])
    if emission:
        bs.inputs['Emission Color'].default_value = (*color,1)
        bs.inputs['Emission Strength'].default_value = emission
    MATS[name]=m
    return name

material('red brick', (.46,.15,.075), texture='red_brick_03_diff_1k.jpg', normal='red_brick_03_nor_gl_1k.jpg')
material('pale brick', (.62,.61,.54), texture='../references/sw-159-first-2021-09-06.jpg')
material('ochre brick', (.40,.26,.12), texture='brown_brick_02_diff_1k.jpg', normal='brown_brick_02_nor_gl_1k.jpg')
material('orange stucco', (.48,.155,.09), normal='concrete_wall_006_nor_gl_1k.jpg')
material('dark red brick', (.29,.07,.043), normal='red_brick_03_nor_gl_1k.jpg')
material('pale render', (.50,.49,.42), normal='concrete_wall_006_nor_gl_1k.jpg')
material('cream stone', (.63,.58,.44), normal='concrete_wall_006_nor_gl_1k.jpg')
material('light limestone', (.67,.65,.56), normal='concrete_wall_006_nor_gl_1k.jpg')
material('brownstone', (.40,.265,.135), normal='concrete_wall_006_nor_gl_1k.jpg')
material('cornice copper brown', (.27,.096,.036), .65)
material('cornice green', (.045,.16,.13), .55, .15)
material('black iron', (.026,.029,.028), .6, .58)
material('red iron', (.26,.055,.035), .62, .4)
material('window frame', (.023,.028,.026), .49, .3)
material('white frame', (.65,.67,.65), .54, .35)
material('window glass', (.075,.14,.17), .19, .48)
material('dark glass', (.015,.026,.03), .28, .28)
material('blue glass', (.09,.17,.23), .16, .58)
material('curtain', (.41,.42,.38), .94)
material('curtain light', (.68,.67,.58), .96)
material('curtain shadow', (.15,.17,.16), .94)
material('roof', (.06,.062,.06), .98)
material('metal', (.37,.40,.39), .45, .75)
material('air conditioner', (.50,.51,.48), .63, .4)
material('asphalt', (.07,.08,.08), .94, texture='asphalt_02_diff_1k.jpg', normal='asphalt_02_nor_gl_1k.jpg')
material('sidewalk', (.38,.39,.36), .91, normal='concrete_wall_006_nor_gl_1k.jpg')
material('curb granite', (.44,.46,.45), .9, normal='concrete_wall_006_nor_gl_1k.jpg')
material('concrete seam', (.13,.14,.13), .95)
material('road paint', (.72,.72,.63), .91)
material('yellow paint', (.72,.49,.035), .87)
material('bike green', (.105,.26,.17), .95)
material('signal yellow', (.75,.39,.025), .43, .15)
material('red signal', (.75,.018,.008), .35, emission=1.5)
material('green signal', (.13,.65,.28), .3, emission=1.5)
material('amber signal', (.95,.31,.015), .3, emission=1.2)
material('sign green', (.012,.17,.12), .7)
material('sign white', (.82,.83,.77), .67)
material('shop cream', (.66,.60,.43), .8)
material('awning brown', (.115,.066,.033), .92)
material('awning green', (.048,.24,.14), .9)
material('wood', (.16,.066,.028), .9)
material('shop green letters', (.20,.51,.22), .55)
material('soil', (.052,.041,.023), 1)
material('tree bark', (.14,.105,.06), .98, normal='concrete_wall_006_nor_gl_1k.jpg')
for i,c in enumerate([(.072,.16,.032),(.09,.20,.04),(.12,.24,.052),(.17,.26,.068)]): material('leaf '+str(i),c,.92)
for i,c in enumerate([(.075,.085,.09),(.40,.42,.40),(.015,.024,.028),(.65,.66,.62),(.07,.12,.18)]): material('car paint '+str(i),c,.24,.55)
material('rubber',(.014,.017,.018),.96)
material('tail lamp',(.35,.012,.009),.3,.25)
material('Beron murals · photo Eden Janine Jim 2025 · CC BY 2.0',(.5,.5,.5),.87,texture='../references/ne-beron-beron-2025-05-16.jpg')
material('interior plaster',(.37,.29,.20),.96)
material('interior tile',(.44,.43,.35),.73)
material('interior oak',(.23,.115,.046),.76)
material('warm glass',(.32,.21,.105),.28,.15,emission=.18)
material('opal lamp',(.96,.66,.32),.38,emission=2.5)
material('brass',(.40,.26,.095),.34,.78)
material('shop sage',(.19,.28,.20),.83)
material('shop burgundy',(.19,.025,.032),.71)
material('theater red',(.57,.016,.021),.75)
material('poster paper',(.75,.68,.49),.93)
material('poster blue',(.045,.105,.18),.91)
material('mortar joint',(.30,.265,.22),.98)
material('stone weathering',(.34,.33,.28),.99)
material('gelato yellow',(.64,.42,.067),.65)
material('gelato pink',(.59,.034,.18),.62)
material('nishaan blue',(.014,.054,.35),.82)
material('nishaan coral',(.82,.16,.16),.73)
material('hags chartreuse',(.54,.59,.17),.63)
material('curtain amber',(.53,.36,.17),.99,emission=.15)
material('store glass',(.21,.29,.30),.14,.25)
gb=MATS['store glass'].node_tree.nodes.get('Principled BSDF')
gb.inputs['Alpha'].default_value=.18
MATS['store glass'].surface_render_method='DITHERED'

def batch(mat):
    k=(OWNER,mat)
    if k not in BATCHES: BATCHES[k]={'v':[],'f':[],'uv':[]}
    return BATCHES[k]

def face(points,mat,uv=None):
    if mat=='pale brick' and uv is None and len(points)==4:
        # A small unobstructed masonry patch from the actual SW facade. The source
        # photograph remains unchanged; the crop and repetition are mesh UVs.
        a,b,c,d=map(Vector,points);e1=b-a;e2=d-a
        vertical=abs(e1.y)>abs(e1.x)+abs(e1.z)
        n1=max(1,math.ceil(e1.length/(.50 if vertical else .56)))
        n2=max(1,math.ceil(e2.length/(.56 if vertical else .50)))
        def brick_uv(u,v):
            if vertical:u,v=v,u
            return ((451+u*22)/1368,1-(1105-v*24)/1824)
        for i in range(n1):
            for j in range(n2):
                corners=[(i/n1,j/n2),((i+1)/n1,j/n2),((i+1)/n1,(j+1)/n2),(i/n1,(j+1)/n2)]
                face([a+e1*u+e2*v for u,v in corners],mat,[brick_uv(u,v) for u,v in [(0,0),(1,0),(1,1),(0,1)]])
        return
    q=batch(mat);start=len(q['v']);q['v'].extend(points)
    q['f'].append(tuple(range(start,start+len(points))))
    if uv is None:
        a,b,c=map(Vector,points[:3]); n=(b-a).cross(c-a)
        axis=max(range(3),key=lambda i:abs(n[i]))
        # Physical brick scale: about 7.5 cm per course on the source material.
        if axis==0: uv=[(p[2]/1.3,p[1]/.9) for p in points]
        elif axis==2: uv=[(p[0]/1.3,p[1]/.9) for p in points]
        else: uv=[(p[0]/3,p[2]/3) for p in points]
    q['uv'].extend(uv)

def box(x,y,z,w,h,d,mat,angle=0):
    if mat in ['road paint','bike green','concrete seam'] and y<.05:
        y=.0025;h=.0015
    ca,sa=math.cos(angle),math.sin(angle)
    ps=[]
    for a,b,c in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:
        u,v=a*w/2,c*d/2;ps.append((x+ca*u+sa*v,y+b*h/2,z-sa*u+ca*v))
    for idx in [(0,3,2,1),(4,5,6,7),(0,4,7,3),(1,2,6,5),(3,7,6,2),(0,1,5,4)]:face([ps[i] for i in idx],mat)

def rod(a,b,r,mat,sides=8,r2=None):
    a,b=Vector(a),Vector(b);delta=b-a
    if delta.length<.0001:return
    n=delta.normalized();t=n.cross(Vector((0,1,0)))
    if t.length<.001:t=n.cross(Vector((1,0,0)))
    t.normalize();s=n.cross(t);r2=r if r2 is None else r2
    pa=[a+r*(t*math.cos(i*math.tau/sides)+s*math.sin(i*math.tau/sides)) for i in range(sides)]
    pb=[b+r2*(t*math.cos(i*math.tau/sides)+s*math.sin(i*math.tau/sides)) for i in range(sides)]
    for i in range(sides):j=(i+1)%sides;face([pa[i],pa[j],pb[j],pb[i]],mat)
    face(list(reversed(pa)),mat);face(pb,mat)

def mass(poly,h,mat,open_ground=False):
    p=poly[:-1] if poly[0]==poly[-1] else poly
    # OSM may use either winding; normalize so facade normals point outwards.
    area=sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p)))
    if area>0:p=list(reversed(p))
    for i,a in enumerate(p):
        b=p[(i+1)%len(p)]
        # Street-facing retail openings are real holes. Back/party walls stay closed.
        mx,mz=(a[0]+b[0])/2,(a[1]+b[1])/2
        street_edge=(abs(mx)<17.8 and abs(b[0]-a[0])<.9) or (abs(mz)<10.2 and abs(b[1]-a[1])<.9)
        low=3.18 if open_ground and street_edge else .17
        face([(a[0],low,a[1]),(b[0],low,b[1]),(b[0],h,b[1]),(a[0],h,a[1])],mat)
    verts=[Vector((a[0],h,a[1])) for a in p]
    for tri in tessellate_polygon([verts]):
        face([verts[v] if isinstance(v,int) else v for v in tri],'roof')
    for i,a in enumerate(p):
        b=p[(i+1)%len(p)];d=math.hypot(b[0]-a[0],b[1]-a[1])
        box((a[0]+b[0])/2,h+.13,(a[1]+b[1])/2,d,.26,.18,mat,-math.atan2(b[1]-a[1],b[0]-a[0]))

class Facade:
    def __init__(self,x,z,rx,rz,length):
        self.x=x;self.z=z;self.rx=rx;self.rz=rz;self.nx=-rz;self.nz=rx;self.L=length
        self.angle=-math.atan2(rz,rx)
    def p(self,s,y,d=0):return (self.x+self.rx*s+self.nx*d,y,self.z+self.rz*s+self.nz*d)
    def b(self,s,y,d,w,h,depth,mat):box(*self.p(s,y,d),w,h,depth,mat,self.angle)
    def line(self,a,b,r,mat='black iron'):rod(self.p(*a),self.p(*b),r,mat)
    def strip(self,y,h,depth,mat):self.b(self.L/2,y,depth/2,self.L+.08,h,depth,mat)
    def quad(self,s,y,w,h,d,mat):
        face([self.p(s-w/2,y-h/2,d),self.p(s+w/2,y-h/2,d),self.p(s+w/2,y+h/2,d),self.p(s-w/2,y+h/2,d)],mat,[(0,0),(1,0),(1,1),(0,1)])

def window(f,s,bottom,w=1.0,h=1.9,trim='light limestone',parts=1,arch=False,blind=False,ac=False,ornate=False):
    cy=bottom+h/2
    f.b(s,cy,.035,w+.15,h+.12,.11,'window frame' if not blind else trim)
    if blind:
        f.b(s,cy,.10,w-.05,h-.08,.04,'pale brick' if trim=='light limestone' else 'dark red brick')
    else:
        # Glass is set back within a built frame; the narrow reveal is actual geometry.
        f.b(s,cy,.09,w,h,.035,'window glass')
        pattern=int((s*7+bottom*11)%7)
        curtain=['curtain shadow','curtain','curtain light','curtain shadow','curtain amber','curtain','curtain shadow'][pattern]
        widths=[.24*w,.52*w,.24*w] if parts==3 else [w/parts]*parts
        edges=[s-w/2]
        for pw in widths:
            sx=edges[-1]+pw/2
            if pattern in [1,2,4]:
                # Parted pleated curtains leave glass visible, with unequal opening heights.
                for side in [-1,1]:
                    for pleat in range(4):
                        ss=sx+side*(pw*.32-pleat*pw*.032)
                        f.b(ss,cy+.035,.112+(pleat%2)*.014,pw*.037,h*.85,.016,curtain)
            elif pattern in [0,5]:
                for slat in range(8 if pattern==0 else 15):
                    f.b(sx,bottom+h-.09-slat*.061,.112,pw-.1,.045,.018,curtain)
            f.b(sx,cy-h*.18,.13,pw-.065,.038,.048,'window frame')
            f.b(sx,cy+h*.46,.13,pw,.055,.055,'window frame')
            edges.append(edges[-1]+pw)
        for sx in edges:f.b(sx,cy,.15,.055,h,.11,'window frame')
        f.b(s,bottom+.025,.15,w+.04,.055,.11,'window frame')
    f.b(s,bottom-.10,.19,w+.27,.12,.32,trim)
    f.b(s,bottom+h+.11,.16,w+.26,.18,.27,trim)
    if ornate:
        f.b(s,bottom+h+.26,.21,w+.40,.10,.40,trim)
        for sx in [s-w*.49,s+w*.49]:f.b(sx,bottom+h+.03,.2,.12,.34,.26,trim)
        f.b(s,bottom+h+.31,.24,.20,.20,.21,trim)
        # Raised central flower and paired scrolls, visible on the ornate stonework.
        for dx in [-.31,0,.31]:
            for k in range(8):
                a=k*math.tau/8
                rod(f.p(s+dx+.061*math.cos(a),bottom+h+.31+.061*math.sin(a),.275),f.p(s+dx+.061*math.cos(a),bottom+h+.31+.061*math.sin(a),.31),.027,trim,6)
        for side in [-1,1]:
            f.line((s,bottom+h+.52,.23),(s+side*w*.50,bottom+h+.30,.23),.031,trim)
    elif trim=='light limestone':
        # Separate voussoir-like, splayed lintel stones on the pale corner tenement.
        for k in range(7):
            u=(k-3)/7
            ps=[f.p(s+u*w*1.1-w*.062,bottom+h+.02,.31),f.p(s+u*w*1.1+w*.062,bottom+h+.02,.31),f.p(s+u*w*1.30+w*.07,bottom+h+.29,.31),f.p(s+u*w*1.30-w*.07,bottom+h+.29,.31)]
            face(ps,trim)
    if arch:
        for j in range(14):
            a=j*math.pi/14;b=(j+1)*math.pi/14
            f.line((s+math.cos(a)*w*.55,bottom+h+.05+math.sin(a)*w*.42,.16),(s+math.cos(b)*w*.55,bottom+h+.05+math.sin(b)*w*.42,.16),.085,trim)
    if ac:
        f.b(s+w*.13,bottom+.13,.37,w*.60,.37,.55,'air conditioner')
        for j in range(7):f.b(s+w*.13,bottom-.015+j*.044,.66,w*.51,.014,.014,'metal')
        for side in [-1,1]:
            ss=s+w*.13+side*w*.22
            f.line((ss,bottom-.1,.18),(ss,bottom-.1,.62),.015,'metal')
            f.line((ss,bottom-.32,.04),(ss,bottom-.1,.62),.015,'metal')
        f.line((s+w*.4,bottom-.04,.64),(s+w*.4,bottom-.38,.12),.011,'black iron')

def cornice(f,h,mat,ornate=True):
    for y,hh,d in [(h-.68,.19,.20),(h-.39,.42,.22),(h-.11,.14,.48),(h+.05,.16,.70),(h+.17,.075,.78)]:f.strip(y,hh,d,mat)
    if ornate:
        for s in [i*.63+.28 for i in range(int(f.L/.63))]:
            f.b(s,h-.31,.31,.14,.47,.42,mat)
            f.b(s,h-.12,.40,.22,.12,.50,mat)
            f.b(s,h-.45,.18,.24,.10,.20,mat)

def escape(f,center,levels,width=2.9,mat='black iron',stairs=True):
    for n,y in enumerate(levels):
        f.b(center,y, .62,width,.10,1.20,mat)
        # Balcony deck grating and railings are separate open steel members.
        for k in range(int(width/.16)+1):
            s=center-width/2+k*.16
            f.line((s,y+.09,1.18),(s,y+1.01,1.18),.017,mat)
            f.line((s,y+.02,.06),(s,y+.02,1.18),.016,mat)
        for d in [.14,1.18]:f.line((center-width/2,y+1.02,d),(center+width/2,y+1.02,d),.026,mat)
        for s in [center-width/2,center+width/2]:
            f.line((s,y+1.02,.10),(s,y+1.02,1.18),.026,mat)
            f.line((s,y-.48,.02),(s,y,1.05),.037,mat)
        if n<len(levels)-1 and stairs:
            yy=levels[n+1];sa=center-width*.36;sb=center+width*.36
            if n%2:sa,sb=sb,sa
            for d in [.55,1.08]:
                f.line((sa,y+.08,d),(sb,yy+.08,d),.035,mat)
                f.line((sa,y+.87,d),(sb,yy+.87,d),.021,mat)
            for j in range(12):
                t=j/11;s=sa+(sb-sa)*t
                f.b(s,y+(yy-y)*t+.08,.81,.32,.047,.60,mat)
    if levels:
        y=levels[0]
        for s in [center+.55,center+.99]:f.line((s,2.35,1.03),(s,y+.80,1.03),.028,mat)
        for j in range(max(1,int((y-2.05)/.3))):f.line((center+.55,2.4+j*.30,1.03),(center+.99,2.4+j*.30,1.03),.019,mat)

TEXT=[]
def label(f,s,y,w,text,color='sign white',size=.3,d=.24):
    TEXT.append((f,s,y,w,text,color,size,d,OWNER))

def storefront(f,a,b,name='',awning=None,fascia='shop cream',letter='sign white',closed=False,profile='cafe'):
    w=b-a;c=(a+b)/2
    frame='wood' if awning=='awning brown' else 'window frame'
    # Actual room volume behind the glazing, no image billboard or painted interior.
    f.b(c,.205,-1.12,w,.07,2.65,'interior tile')
    f.b(c,3.05,-1.12,w,.10,2.65,'interior plaster')
    f.b(c,1.62,-2.36,w,2.9,.10,'interior plaster' if not closed else 'dark glass')
    for s in [a+.08,b-.08]:
        f.b(s,1.62,-1.1,.16,2.94,2.66,fascia)
        f.b(s,1.61,.30,.17,2.92,.32,fascia)
        f.b(s,.30,.32,.24,.23,.35,'light limestone')
    if not closed:
        # Furnishings are representative; occupancy and street-facing signs are sourced.
        if profile=='optical':
            for yy in [.95,1.38,1.81,2.24]:
                f.b(c,yy,-1.99,w-.6,.065,.50,'interior oak')
                for k in range(max(2,int(w/.42))):
                    ss=a+.4+k*.42
                    for dx in [-.045,.045]:
                        rod(f.p(ss+dx,yy+.085,-1.70),f.p(ss+dx,yy+.085,-1.68),.035,'black iron',10)
                    f.line((ss-.018,yy+.085,-1.68),(ss+.018,yy+.085,-1.68),.007,'black iron')
        else:
            f.b(c+.35,.73,-1.56,max(.8,w-1.7),1.0,.63,'interior oak')
            f.b(c+.35,1.255,-1.55,max(.9,w-1.6),.065,.77,'cream stone')
            for k in range(max(2,int(w/1.2))):
                ss=a+.7+k*1.05
                f.b(ss,2.13,-2.21,.75,.06,.32,'wood')
                for j in range(4):
                    rod(f.p(ss-.24+j*.14,2.17,-2.14),f.p(ss-.24+j*.14,2.40,-2.14),.033,'shop sage' if j%2 else 'brass',8)
            if profile=='gelato':
                f.b(c+.4,1.43,-1.17,max(.8,w-1.9),.35,.28,'store glass')
                for k in range(6):
                    f.b(c-.65+k*.36,1.29,-1.31,.28,.025,.30,'metal')
            elif profile=='bakery':
                for k in range(10):
                    ss=a+1.3+(k%5)*.35; yy=1.32+(k//5)*.18
                    rod(f.p(ss,yy,-1.20),f.p(ss,yy+.06,-1.20),.10,'shop cream',12)
        for s in [a+w*.31,a+w*.70]:
            f.line((s,3.02,-.83),(s,2.43,-.83),.011,'black iron')
            rod(f.p(s,2.45,-.83),f.p(s,2.31,-.83),.17,'brass',16,r2=.22)
            rod(f.p(s,2.31,-.83),f.p(s,2.295,-.83),.20,'opal lamp',16)
    # A distinct door with transom, hinges, threshold, kickplate and tubular pull.
    door=a+min(1.04,w*.24);door_w=min(.94,w*.30)
    divs=[a+.17,door-door_w/2,door+door_w/2,b-.17]
    if w>5.2:divs.append(c+.65)
    for s in sorted(set(divs)):
        f.b(s,1.50,.27,.065,2.59,.13,frame)
    f.b(c,2.58,.27,w-.22,.065,.13,frame)
    f.b(c,.38,.24,w-.3,.26,.17,frame)
    f.b(c,1.50,.253,w-.36,2.30,.016,'store glass' if not closed else 'dark glass')
    f.b(door,.205,.36,door_w+.12,.09,.38,'light limestone')
    f.b(door,.44,.31,door_w-.07,.29,.026,'metal')
    f.b(door,2.22,.29,door_w,.055,.12,frame)
    for y in [.6,1.8]:f.b(door-door_w/2+.035,y,.36,.035,.12,.035,'metal')
    s=door+door_w*.28
    f.line((s,1.04,.37),(s,1.59,.37),.015,'brass')
    for y in [1.04,1.59]:f.line((s,y,.30),(s,y,.37),.013,'brass')
    if closed:
        for y in [.5+i*.08 for i in range(25)]:f.b(c,y,.35,w-.32,.014,.025,'metal')
    f.b(c,2.79,.25,w-.04,.36,.34,fascia)
    f.b(c,3.08,.18,w,.20,.25,fascia)
    f.b(c,2.995,.35,w,.025,.08,'brass' if profile=='cafe' else 'metal')
    if name:label(f,c,2.79,w-.35,name,letter,min(.34,(w-.35)/max(4,len(name))*1.45),d=.434)
    if awning:
        face([f.p(a,2.66,.22),f.p(b,2.66,.22),f.p(b,2.23,1.27),f.p(a,2.23,1.27)],awning)
        f.b(c,2.17,1.27,w,.16,.035,awning)
        for s in [a+.12,b-.12]:
            f.line((s,2.55,.20),(s,2.18,1.27),.014,frame)
        if name:label(f,c,2.17,w-.15,name,letter,min(.145,w/max(4,len(name))*1.2),d=1.30)

def photo_panel(f,s,bottom,w,h,pixels,mat,image_size=(4032,2268)):
    """Project original image coordinates onto a subdivided flat sign mesh.

    No photographic pixels are synthesized or modified. The four picked corners
    are bottom-left, bottom-right, top-right, top-left in source pixel space.
    """
    A=[];B=[]
    for (u,v),(x,y) in zip([(0,0),(1,0),(1,1),(0,1)],pixels):
        A += [[u,v,1,0,0,0,-u*x,-v*x],[0,0,0,u,v,1,-u*y,-v*y]];B += [x,y]
    H=np.append(np.linalg.solve(np.array(A),np.array(B)),1).reshape(3,3)
    def uv(u,v):
        p=H@np.array([u,v,1]);return (float(p[0]/p[2]/image_size[0]),1-float(p[1]/p[2]/image_size[1]))
    for i in range(6):
        for j in range(10):
            u,v=i/6,j/10;du,dv=1/6,1/10
            coords=[(u,v),(u+du,v),(u+du,v+dv),(u,v+dv)]
            face([f.p(s-w/2+a*w,bottom+b*h,.20) for a,b in coords],mat,[uv(a,b) for a,b in coords])

def capsule(f,s,cy,w,h,d,mat):
    radius=w/2;straight=(h-w)/2;points=[]
    for k in range(41):
        a=k*math.tau/40
        points.append(f.p(s+radius*math.cos(a),cy+radius*math.sin(a)+(straight if math.sin(a)>=0 else -straight),d))
    face(points[:-1],mat)

def roof_details(b,h):
    p=b['p'];xs=[v[0] for v in p];zs=[v[1] for v in p]
    x=sum(xs)/len(xs);z=sum(zs)/len(zs)
    box(x,h+.34,z,1.2,.68,.8,'metal')
    for dz in [-.22,0,.22]:box(x,h+.35,z+dz,1.04,.02,.025,'black iron')
    box(max(xs)-.6,h+.6,min(zs)+.7,.52,1.2,.5,'dark red brick')

def build_corners():
    global OWNER
    OWNER='163 First Avenue · northwest · photograph-based'
    b=BUILDINGS[247851944];mass(b['p'],10.40,'orange stucco',True)
    nw=Facade(-15.35,-9.55,0,-1,8.10);nws=Facade(-45.60,-9.51,1,0,30.25)
    for f in [nw,nws]:
        for y in [3.28,6.60,9.68,10.48]:
            f.strip(y,.095,.14,'cornice green')
            if y in [3.28,9.68]:f.strip(y+.095,.04,.18,'cornice green')
        # The first residential storey has shallow horizontal rustication.
        for y in [3.65,4.12,4.59,5.06,5.53,6.0,6.47]:f.strip(y,.014,.015,'cornice copper brown')
    for y in [3.84,7.09]:
        for s in [2.03,6.04]:window(nw,s,y,2.40,2.03,'orange stucco',parts=3,ac=(y>6 and s>5))
        for s in [1.65,5.25,8.9,12.55,16.2,19.85,23.5]:window(nws,s,y,2.18,1.97,'orange stucco',parts=3,ac=(s==16.2))
        window(nws,28.18,y,.89,1.96,'orange stucco')
    storefront(nw,.08,4.15,'GELATOVILLE',None,'shop sage','sign white',profile='gelato')
    storefront(nw,4.15,8.08,'',None,'black iron','sign white')
    nw.b(6.11,1.60,.45,3.90,2.86,.08,'black iron')
    # HAGS has a rounded chartreuse door and oval window, not a conventional fascia.
    capsule(nw,5.27,1.50,1.08,2.55,.505,'hags chartreuse')
    nw.b(5.27,.71,.51,1.08,1.04,.018,'hags chartreuse')
    capsule(nw,5.27,1.72,.62,1.30,.525,'blue glass')
    capsule(nw,7.02,1.88,1.0,1.66,.505,'hags chartreuse')
    capsule(nw,7.02,1.88,.90,1.53,.525,'blue glass')
    nw.line((5.65,.93,.58),(5.65,1.41,.58),.018,'brass')
    nw.b(5.27,.32,.54,.99,.22,.035,'metal')
    nw.b(6.06,1.66,.55,.31,.38,.055,'brass')
    nw.b(6.06,1.66,.583,.25,.30,.02,'poster paper')
    rod(nw.p(6.07,2.07,.49),nw.p(6.07,2.07,.63),.075,'opal lamp',16)
    label(nw,5.27,2.92,.40,'163','brass',.14,d=.53)
    label(nw,5.27,1.81,.50,'HAGS','black iron',.15,d=.541)
    for yy in [2.62+i*.065 for i in range(5)]:nw.b(7.03,yy,.53,.91,.023,.06,'metal')
    for a,bx in [(14.4,20.3),(20.3,25.7),(25.7,30.1)]:
        storefront(nws,a,bx,'GELATOVILLE' if a==25.7 else '',None,'shop sage',profile='gelato')
    storefront(nws,.2,5.0,'NOT AS BITTER',None,'shop cream','black iron')
    storefront(nws,5.0,10.0,'TO EAT SUSHI',None,'black iron','sign white')
    storefront(nws,10.0,14.4,'',None,'shop cream',closed=True)
    for f,a,bx in [(nw,.15,4.10),(nws,25.78,30.1)]:
        for ss in [a,a+(bx-a)*.37,bx]:f.b(ss,1.5,.36,.12,2.6,.18,'gelato yellow')
        for yy in [.36,2.28,2.57]:f.b((a+bx)/2,yy,.36,bx-a,.12,.18,'gelato yellow')
    nw.b(.05,1.55,.32,.17,2.80,.22,'gelato pink')
    escape(nws,11.0,[6.80,10.42],1.0,'red iron',False)
    roof_details(b,10.45)

    OWNER='159–161 First Avenue · southwest · photograph-based'
    b=BUILDINGS[247852692];mass(b['p'],18.40,'pale brick',True)
    sw=Facade(-15.32,23.22,0,-1,14.24);sws=Facade(-15.38,8.97,-1,0,21.9)
    for f in [sw,sws]:
        cornice(f,18.48,'cornice copper brown')
        for y in [3.51,6.40,12.30,15.35]:f.strip(y,.075,.09,'light limestone')
        for i in range(int(f.L/1.35)):
            s=.68+i*1.35
            for j in range(12):
                a=math.pi+j*math.pi/12;b=math.pi+(j+1)*math.pi/12
                f.line((s+.45*math.cos(a),17.81+.19*math.sin(a),.24),(s+.45*math.cos(b),17.81+.19*math.sin(b),.24),.021,'cornice copper brown')
    levels=[3.86,6.78,9.70,12.62,15.54]
    # Front sequence includes the blind bay beside the corner, visible in the source.
    for i,y in enumerate(levels):
        for s,w,parts,blind in [(1.46,1.55,2,False),(3.29,1.0,1,False),(5.25,1.88,2,False),(9.05,1.84,2,False),(12.38,.94,1,True)]:
            window(sw,s,y,w,1.90,'light limestone',parts=parts,blind=blind,ac=(i in [1,3] and s==5.25),ornate=i in [1,2])
        for k,s in enumerate([1.02,3.55,6.09,8.61,11.16,13.68,16.19,18.71,20.65]):
            window(sws,s,y,.94 if k!=5 else 1.25,1.91,'light limestone',ac=((i+k)%9==0),ornate=i in [1,2])
    escape(sw,3.3,[3.64,6.56,9.48,12.4,15.32],3.75)
    escape(sws,12.30,[3.64,6.56,9.48,12.4,15.32],3.25)
    storefront(sw,.1,7.2,'eye & health',None,'pale render','shop green letters',profile='optical')
    storefront(sw,7.2,14.1,'eye & health',None,'pale render','shop green letters',profile='optical')
    storefront(sws,.1,7.4,'eye & health',None,'pale render','shop green letters',profile='optical')
    storefront(sws,7.4,10.0,'DENTIST',None,'pale brick')
    storefront(sws,10,16.0,'Apollo Bagels','theater red','sign white','sign white',profile='bakery')
    for s in [10.25,10.50,10.75,11.0,15.05,15.30,15.55,15.8]:sws.b(s,1.42,.34,.064,2.10,.18,'white frame')
    for s in [11.1,14.9]:
        sws.line((s,3.05,.25),(s,3.18,.80),.018,'white frame')
        rod(sws.p(s,3.18,.80),sws.p(s,3.10,.80),.09,'white frame',12,r2=.12)
    label(sws,10.4,2.18,.50,'242','sign white',.13,d=1.305)
    storefront(sws,16,21.8,'',None,'pale brick')
    # Retracted shop security grilles show the optical displays through glazing.
    for f,a,bb in [(sw,.2,14.0),(sws,.2,7.3)]:
        f.b((a+bb)/2,2.50,.34,bb-a,.18,.22,'metal')
        for y in [2.44,2.48,2.52,2.56]:f.line((a,y,.46),(bb,y,.46),.008,'black iron')
    roof_details(BUILDINGS[247852692],18.5)

    OWNER='164 First Avenue · northeast · photograph-based'
    b=BUILDINGS[248142962];mass(b['p'],13.28,'red brick',True)
    ne=Facade(16.06,-16.44,0,1,7.36);nes=Facade(16.11,-9.06,1,0,15.17)
    cornice(ne,13.40,'metal',False);nes.strip(13.32,.18,.23,'metal')
    ne.strip(3.56,.24,.40,'brownstone');ne.strip(6.69,.10,.08,'light limestone')
    for y in [3.85,7.01,10.17]:
        for s in [1.26,3.68,6.08]:window(ne,s,y,1.16,2.02,'metal' if y>6 else 'light limestone',ac=(s!=6.08))
    ne.strip(5.13,3.10,.014,'black iron');nes.strip(5.13,3.10,.014,'black iron')
    for y in [3.85,7.01,10.17]:
        for s,w in [(2.22,1.30),(7.33,1.1),(9.31,.78),(11.74,1.15)]:
            window(nes,s,y,w,1.94,'metal',blind=(s==2.22 and y>6))
        window(nes,14.20,y,.9,1.90,'metal')
    escape(nes,11.55,[3.61,6.77,9.93],3.20)
    nes.b(13.13,7.10,.50,.73,12.40,.78,'cream stone')
    for s in [9.77,9.89,10.01]:
        nes.line((s,10.1,.16),(s,13.6,.16),.025)
        nes.line((s,10.1,.16),(8.62+(s-9.77),9.90,.16),.025)
        nes.line((8.62+(s-9.77),9.90,.16),(8.62+(s-9.77),3.1,.16),.025)
    storefront(ne,.1,7.27,'BERON BERON',None,'black iron',closed=True)
    storefront(nes,.1,5.2,'BERON BERON',None,'black iron',closed=True)
    for aa,bb in [(5.2,9.8),(9.8,15.1)]:storefront(nes,aa,bb,'',None,'dark red brick',closed=True)
    # The two actual Japanese art panels, preserved from the licensed May 2025 photograph.
    mural='Beron murals · photo Eden Janine Jim 2025 · CC BY 2.0'
    photo_panel(ne,2.47,3.82,.93,2.37,[(155,1380),(752,1390),(923,485),(445,443)],mural)
    photo_panel(ne,4.90,3.82,.93,2.37,[(1510,1427),(2017,1444),(2015,537),(1575,522)],mural)
    for s in [.60+i*.68 for i in range(10)]:
        ne.b(s,2.66,.54,.035,.49,.035,'wood')
        rod(ne.p(s,2.30,.56),ne.p(s,2.55,.56),.16,'shop cream',12)
    for y in [4.75,8.09,11.25]:
        for s in [1.26,3.68]:
            ne.b(s,y-.93,.49,1.25,.055,.62,'black iron')
            for ss in [s-.59,s+.59]:ne.line((ss,y-.93,.73),(ss,y-.32,.73),.018)
            ne.line((s-.6,y-.30,.73),(s+.6,y-.30,.73),.018)
    # Distinctive roof antenna rack. Eave and antenna heights are separated.
    for x in [17.0,18.9,21.0]:
        for z in [-10.2,-13.9]:
            rod((x,13.4,z),(x,15.35,z),.035,'metal')
            box(x,14.85,z,.24,1.78,.16,'white frame')
    for z in [-10.2,-13.9]:rod((16.65,13.85,z),(22.0,13.85,z),.04,'metal')
    for x in [17.0,21.0]:rod((x,13.8,-10.2),(x,13.8,-13.9),.04,'metal')
    roof_details(b,13.3)

    OWNER='162 First Avenue · southeast · photograph-based'
    b=BUILDINGS[248142976];mass(b['p'],14.15,'red brick',True)
    se=Facade(15.32,9.20,0,1,6.89);ses=Facade(31.74,9.11,-1,0,16.39)
    for f in [se,ses]:
        f.strip(13.85,.18,.22,'cornice copper brown');f.strip(14.24,.13,.19,'cornice copper brown')
        f.strip(3.2,.12,.13,'cornice copper brown')
    for y in [3.98,7.24,10.50]:
        for s in [1.13,3.45,5.68]:window(se,s,y,.93,1.93,'cornice copper brown',ac=(s==3.45 and y>6))
        for s in [1.76,5.28,8.76,12.05,14.80]:window(ses,s,y,1.03,1.89,'cornice copper brown',blind=(s in [5.28,12.05,14.80]))
    escape(se,3.4,[3.62,6.88,10.14],4.30,'red iron')
    storefront(se,.10,6.78,'',None,'shop cream',closed=True)
    storefront(ses,8.5,16.27,'',None,'shop cream',closed=True)
    for a,bb in [(.1,4.3),(4.3,8.5)]:storefront(ses,a,bb,'',None,'dark red brick')
    face([se.p(.05,2.72,.4),se.p(6.84,2.72,.4),se.p(6.84,2.15,1.2),se.p(.05,2.15,1.2)],'shop cream')
    # The prominent high bulkhead in the photograph belongs to neighboring 160.
    for x in [17.5,20.0]:
        rod((x,14.25,14.8),(x,15.4,14.8),.03,'metal')

def build_tower():
    global OWNER
    OWNER='Theater and tower · footprint subdivision estimated from references'
    # The OSM outline is a combined podium; extruding all of it to 51.5 m was incorrect.
    b=BUILDINGS[247852695];mass(b['p'],4.3,'pale render',True)
    box(-56.0,10.30,23.20,36.7,12.0,27.6,'pale render')
    f=Facade(-37.4,9.03,-1,0,39.0)
    # This side wing has no modeled retail openings: keep its street-level wall closed.
    f.strip(1.66,3.05,.06,'pale render')
    for yy in [5.0,8.2,11.4]:
        for s in [2.4+i*4.4 for i in range(8)]:window(f,s,yy,2.9,1.58,'pale render',parts=2)
    theatre=Facade(-15.30,37.27,0,-1,14.03)
    # The theater's actual red/white diagonal front, three OPEN doors and poster cases.
    theatre.strip(1.61,2.87,.13,'sign white')
    for s in [0,3.1,6.2,9.3,12.4]:
        face([theatre.p(s,.19,.145),theatre.p(min(s+1.10,14),.19,.145),theatre.p(min(s+2.30,14),3.04,.145),theatre.p(min(s+1.2,14),3.04,.145)],'theater red')
    theatre.strip(3.15,.33,.21,'theater red')
    label(theatre,7.0,3.16,13.55,'THEATER FOR THE NEW CITY','sign white',.43,d=.23)
    for s in [2.10,3.45,4.80]:
        theatre.b(s,1.57,.20,1.26,2.68,.16,'theater red')
        theatre.b(s,2.13,.30,1.05,1.19,.026,'dark glass')
        for yy in [1.52,2.74]:theatre.b(s,yy,.34,1.14,.058,.11,'black iron')
        theatre.line((s+.43,1.20,.38),(s+.43,1.55,.38),.018,'metal')
    label(theatre,3.45,.94,3.80,'OPEN','sign white',1.25,d=.325)
    for s,w,title in [(7.16,1.68,'DREAM UP FESTIVAL'),(10.35,1.32,'THE ROOT OF IT ALL'),(.45,.65,'TNC')]:
        theatre.b(s,1.92,.26,w,1.52,.19,'black iron')
        theatre.b(s,1.92,.365,w-.11,1.39,.025,'poster paper')
        label(theatre,s,2.47,w-.15,'THEATER FOR THE NEW CITY','black iron',.07,d=.39)
        theatre.b(s,2.01,.39,w-.23,.53,.01,'poster blue')
        label(theatre,s,2.10,w-.33,title,'sign white',.11,d=.405)
        label(theatre,s,1.87,w-.30,'2026','sign white',.13,d=.405)
        label(theatre,s,1.55,w-.22,'AUG 23 — SEP 13' if s==7.16 else 'SUMMER THEATER','black iron',.085,d=.39)
    for s in [6.1,6.5]:
        rod(theatre.p(s,.83,.13),theatre.p(s,.83,.41),.075,'metal',12)
    for s in [.50+i*1.85 for i in range(8)]:
        theatre.b(s,3.78,.09,1.74,.77,.06,'dark glass')
        theatre.b(s-.85,3.78,.15,.055,.80,.11,'metal')
    # Separate tower inset behind the tenement, with an elevated balcony stack.
    x0,x1,z0,z1=-38.0,-19.1,24.0,37.25
    mass([[x0,z0],[x1,z0],[x1,z1],[x0,z1]],49.9,'cream stone')
    ft=Facade(x1,z1,0,-1,z1-z0);fs=Facade(x1,z0,-1,0,x1-x0)
    for f in [ft,fs]:
        for yy in [4.7+i*3.08 for i in range(15)]:
            f.strip(yy-.36,.06,.019,'brownstone')
        for s in [i*1.45 for i in range(int(f.L/1.45)+1)]:f.b(s,27.0,.014,.016,43,.018,'brownstone')
    for i in range(14):
        y=5.1+i*3.08
        for s in [2.0,4.8,7.2]:window(ft,s,y,2.22,1.56,'cream stone',parts=2)
        ft.b(10.70,y-.26,.95,4.0,.18,1.75,'cream stone')
        ft.line((8.75,y+.71,1.78),(12.65,y+.71,1.78),.029,'white frame')
        for k in range(24):
            s=8.80+k*.165;ft.line((s,y-.18,1.78),(s,y+.71,1.78),.018,'white frame')
        for s in [8.75,12.65]:ft.line((s,y+.71,.12),(s,y+.71,1.78),.028,'white frame')
        for s in [2.3,5.3,12.0,15.0]:window(fs,s,y,1.85,1.55,'cream stone',parts=2)
    box(-29.0,28.2,23.58,3.4,46.6,1.7,'cream stone')
    rod((-29.1,9.0,22.69),(-29.1,51.3,22.69),.12,'metal')
    box(-33.8,50.9,31.6,6.4,2.0,7.2,'cream stone')

def build_neighbors():
    global OWNER
    # Individual facade schedules for immediately adjacent visible buildings.
    schedules=[
        (247851882,16.65,'red brick','cream stone',5,[1.2,3.4,5.6], 'Pasta de Pasta'),
        (247851883,17.05,'red brick','cream stone',5,[1.2,3.6,6.0], ''),
        (247851884,8.05,'dark red brick','black iron',2,[1.2,3.5,5.8], ''),
        (247851885,19.4,'red brick','brownstone',6,[1.1,3.5,5.8], 'MOMOFUKU NOODLE BAR'),
        (248142864,17.05,'red brick','brownstone',5,[1.2,3.55,5.9], 'Country Buffet'),
        (248142866,17.5,'red brick','black iron',5,[1.3,3.7,6.1], ''),
        (248142868,17.15,'pale brick','light limestone',5,[1.2,3.55,5.9], ''),
        (248142862,21.45,'ochre brick','brownstone',6,[1.30,3.87,6.42], 'NISHAAN'),
        (248142861,20.95,'dark red brick','brownstone',6,[1.25,4.55], ''),
        (248142860,20.6,'pale render','cream stone',5,[1.45,3.85,6.15], ''),
        (247852655,14.8,'red brick','cream stone',4,[1.15,3.6,6.0], ''),
        (247852701,16.8,'red brick','light limestone',5,[1.15,3.4,5.65], ''),
    ]
    for ident,h,wall,trim,floors,bays,shop in schedules:
        b=BUILDINGS[ident];OWNER=b['address']+' · adjacent facade reference'
        mass(b['p'],h,wall,True);zs=[p[1] for p in b['p']];xs=[p[0] for p in b['p']]
        west=sum(xs)<0;length=max(zs)-min(zs)
        if west:f=Facade(max(xs)+.012,max(zs),0,-1,length)
        else:f=Facade(min(xs)-.012,min(zs),0,1,length)
        cornice(f,h,trim)
        step=(h-4.0)/(floors-1)
        for i in range(floors-1):
            for s in bays:
                window(f,s,3.75+i*step,1.08,min(2.28,step*.69),trim,arch=(ident==248142862 and i in [1,4]),ornate=ident==248142862,ac=(int(s*7+i)%7==0))
            if ident==248142862:f.strip(3.51+i*step,.13,.15,trim)
        if ident not in [247851884,248142864,248142866]:escape(f,length*.51,[3.53+i*step for i in range(floors-1)],min(3.2,length*.68),'red iron' if west else 'black iron')
        if ident==247851882:
            storefront(f,.1,length-.1,shop,'awning green','sign white','cornice green')
            f.b(length*.50,2.69,.442,length*.68,.035,.02,'cornice green')
            f.b(length*.30,2.69,.453,length*.21,.035,.025,'theater red')
            for s in [.18,length*.36,length-.18]:f.b(s,1.4,.35,.10,2.3,.15,'white frame')
            for k in range(max(1,int(length*.53/.065))):f.b(length*.4+k*.065,.80,.32,.037,.69,.11,'interior oak')
            rod(f.p(length*.60,1.21,-.38),f.p(length*.60,1.43,-.38),.29,'shop cream',24)
        elif ident==248142862:
            storefront(f,.1,length-.1,'',None,'brownstone')
            a,bx=1.25,length-.15;c=(a+bx)/2
            for s in [a+.13,a+(bx-a)*.36,a+(bx-a)*.58,a+(bx-a)*.80,bx-.12]:
                f.b(s,1.38,.41,.075,2.30,.18,'nishaan blue')
            for yy in [.27,1.99,2.43]:f.b(c,yy,.41,bx-a-.11,.072,.18,'nishaan blue')
            face([f.p(a,3.1,.27),f.p(bx,3.1,.27),f.p(bx,2.42,1.18),f.p(a,2.42,1.18)],'nishaan blue')
            for s in [a,bx]:face([f.p(s,2.42,.25),f.p(s,3.1,.25),f.p(s,2.42,1.18)],'nishaan blue')
            f.b(c,2.32,1.18,bx-a,.21,.035,'nishaan blue')
            # Lettering is modeled on the blue sign, without copying photographic pixels.
            f.b(c,2.68,.845,(bx-a)*.62,.35,.035,'nishaan blue')
            label(f,c,2.68,(bx-a)*.59,'NISHAAN','nishaan coral',.30,d=.875)
            label(f,c,2.33,bx-a-.2,'HOME OF THE PAKISTANI CHOPPED CHEESE','sign white',.105,d=1.205)
            blade=Facade(*[f.p(bx-.18,0,1.10)[i] for i in [0,2]],f.nx,f.nz,1.1)
            blade.b(.45,3.7,0,1.38,.69,.09,'nishaan blue')
            blade.b(.45,3.7,.055,1.21,.50,.018,'sign white')
            label(blade,.45,3.78,1.11,'SANDWICHES','theater red',.12,d=.071)
            label(blade,.45,3.59,1.10,'CHOPPED · MELTED · LOADED','black iron',.055,d=.071)
            f.line((bx-.18,4.15,.07),(bx-.18,4.15,2.30),.035,'black iron')
        elif ident==248142864:
            storefront(f,.1,length-.1,'',None,'light limestone',closed=True)
            f.b(length/2,2.88,.40,length-.25,.60,.16,'sign white')
            f.b(.63,2.88,.49,.59,.50,.025,'theater red')
            for k in range(12):
                a=k*math.tau/12
                f.line((.63+.17*math.sin(a),2.88+.17*math.cos(a),.515),(.63+.21*math.sin(a),2.88+.21*math.cos(a),.515),.009,'sign white')
            f.line((.63,2.88,.53),(.73,3.04,.53),.017,'black iron')
            f.line((.63,2.88,.53),(.79,2.82,.53),.014,'black iron')
            label(f,1.42,2.99,.85,'GOOD','black iron',.18,d=.51)
            label(f,1.42,2.76,.85,'TIME','black iron',.19,d=.51)
            label(f,(length+2)/2,2.86,length-2.3,'Country Buffet','awning brown',.35,d=.51)
            # The right entrance is separate from the broad left security grille.
            door=length*.85
            f.b(door,1.45,.46,length*.21,2.5,.09,'light limestone')
            f.b(door,1.68,.52,length*.15,1.60,.025,'dark glass')
            for sx in [-1,1]:f.b(door+sx*length*.045,1.68,.56,.035,1.65,.07,'white frame')
            for yy in [.92,1.08,2.26,2.46]:f.b(door,yy,.56,length*.16,.035,.07,'white frame')
            f.b(door,.52,.54,length*.17,.53,.045,'white frame')
            f.line((door-length*.073,1.16,.63),(door-length*.073,1.68,.63),.015,'brass')
        else:storefront(f,.1,length-.1,shop,None,'black iron',closed=not bool(shop))
        roof_details(b,h)
        if ident==248142862:
            box(min(xs)+2.0,h+1.4,min(zs)+2.4,2.9,2.8,3.8,'pale render')
            for x in [min(xs)+.4,min(xs)+2.2]:
                rod((x,h,min(zs)+1.4),(x,h+3.7,min(zs)+1.4),.03,'metal')
                box(x,h+2.5,min(zs)+1.4,.3,1.4,.18,'air conditioner')
    # East 10th Street elevations continue only a short distance from each corner.
    for ident,h,wall,floors in [(248142883,16.5,'red brick',5),(248142885,18.7,'red brick',5),(248142884,10.5,'red brick',3),(248142886,10.7,'red brick',3),(248142889,17.4,'dark red brick',5),(247851912,17.3,'pale render',5)]:
        b=BUILDINGS[ident];OWNER=b['address']+' · side street reference'
        mass(b['p'],h,wall,True);xs=[p[0] for p in b['p']];zs=[p[1] for p in b['p']]
        north=sum(zs)<0;L=max(xs)-min(xs)
        f=Facade(min(xs),max(zs)+.013,1,0,L) if north else Facade(max(xs),min(zs)-.013,-1,0,L)
        cornice(f,h,'cornice copper brown',ident not in [248142884,248142886])
        cols=max(2,round(L/2.7));step=(h-3.7)/(floors-1)
        for i in range(floors-1):
            for k in range(cols):window(f,(k+.5)*L/cols,3.65+i*step,1.02,min(2.05,step*.68),'cream stone')
        escape(f,L*.52,[3.5+i*step for i in range(floors-1)],min(L*.65,3.1))
        storefront(f,.1,L-.1,'CRYSTALS GARDEN' if ident==248142883 else '',None,'shop sage' if ident==248142883 else wall,closed=ident!=248142883)
        if ident==248142883:label(f,L/2,2.51,L-.4,'HEALING CRYSTALS · GEM STONES','sign white',.11,d=.43)
        roof_details(b,h)

def build_road():
    global OWNER
    OWNER='Streets · mapped alignment · curb widths estimated from photographs'
    box(0,-.13,0,135,.26,155,'asphalt')
    # Raised sidewalks with open intersecting roads. Four tapered ramp approaches.
    for sx in [-1,1]:
        for sz in [-1,1]:
            x=sx*(10.75+(67.5-10.75)/2);z=sz*(4.95+(77.5-4.95)/2)
            box(x,.065,z,67.5-10.75,.20,77.5-4.95,'sidewalk')
            box(sx*10.82,.04,sz*41.4,.24,.30,72.1,'curb granite')
            box(sx*39.2,.04,sz*5.03,56.3,.30,.24,'curb granite')
            for y in range(8,77,2):box(sx*13.0,.172,sz*y,4.2,.004,.014,'concrete seam')
            for x0 in range(14,67,2):box(sx*x0,.172,sz*7.2,.014,.004,4.05,'concrete seam')
            box(sx*12.02,.177,sz*6.1,1.28,.028,1.10,'cream stone')
            for a in range(9):
                for b in range(6):box(sx*(11.52+a*.12),.20,sz*(5.67+b*.14),.032,.026,.032,'yellow paint')
    # Zebra crossings, set outside the vehicle conflict area.
    for zz in [-7.15,7.15]:
        for x in [-10+i*1.25 for i in range(17)]:box(x,.012,zz,.56,.018,2.7,'road paint')
    for xx in [-12.8,12.8]:
        for z in [-4.2+i*1.2 for i in range(8)]:box(xx,.014,z,2.85,.018,.50,'road paint')
    # First Avenue is northbound. West-side protected bicycle lane and buffer.
    for zz,dep in [(-43.1,64.5),(43.1,64.5)]:
        box(-9.25,.010,zz,2.50,.012,dep,'bike green')
        for xx in [-10.55,-7.85,-5.15]:box(xx,.02,zz,.11,.012,dep,'road paint')
    for z in range(-73,75,4):
        if abs(z)<12:continue
        box(-6.49,.023,z,2.64,.015,.11,'road paint',-.36)
    for xx in [-1.94,1.26,4.46]:
        for z in range(-75,76,9):
            if abs(z)<14:continue
            box(xx,.023,z,.115,.015,3.0,'road paint')
    for z in range(-4,5):box(-9.25,.018,z*1.20,.25,.016,.5,'road paint')
    for x,z in [(-3,17),(3,-18),(2,52),(-3,-50)]:
        box(x,.026,z,.17,.018,2.9,'road paint')
        for sign in [-1,1]:box(x+sign*.43,.026,z-1.14,1.15,.018,.17,'road paint',sign*.74)
    for x,z in [(2.6,4.0),(-2.8,-4.1),(-31.0,.2),(34,1.0),(3,-30)]:
        rod((x,.015,z),(x,.028,z),.48,'metal',32)
        for k in range(9):box(x,.043,z+(k-4)*.078,.68,.012,.012,'black iron')
    # Stop lines and longitudinal utility trench seams.
    box(.55,.03,10.45,13.0,.017,.30,'road paint')
    box(-16.25,.025,0,.27,.015,8.5,'road paint')
    for x in [-3.52,5.8]:box(x,.018,0,.032,.008,150,'concrete seam')

def traffic_pole(x,z,dx,dz):
    rod((x,.17,z),(x,6.05,z),.105,'metal',12)
    box(x,.34,z,.35,.35,.35,'metal')
    # Supported diagonal arm, characteristic NYC signal assembly.
    rod((x,5.30,z),(x+dx*5.8,5.86,z+dz*5.8),.068,'metal',10)
    rod((x,5.98,z),(x+dx*5.8,5.86,z+dz*5.8),.041,'metal',10)
    sx,sz=x+dx*5.45,z+dz*5.45
    f=Facade(sx,sz,-dz,dx,1)
    f.b(0,5.28,.0,.40,1.09,.32,'signal yellow')
    for i in range(3):
        cy=5.64-i*.34
        rod(f.p(0,cy,.17),f.p(0,cy,.24),.127,'black iron',16)
        rod(f.p(0,cy,.244),f.p(0,cy,.25),.097,'green signal' if i==2 else 'black iron',16)
    # Pedestrian signal and exact street labels.
    f=Facade(x,z,1,0,1)
    f.b(.31,2.69,.0,.55,.52,.29,'signal yellow')
    f.b(.31,2.69,.157,.42,.39,.025,'black iron')
    for yy in [2.67,2.78]:f.b(.31,yy,.176,.19,.06,.017,'amber signal')
    sign=Facade(x-.7,z-.08,1,0,1.4)
    sign.b(.7,3.73,0,1.55,.36,.06,'sign green');label(sign,.7,3.73,1.42,'E 10 ST',size=.22,d=.043)
    other=Facade(x+.06,z-.8,0,1,1.6)
    other.b(.8,4.16,0,1.52,.37,.06,'sign green');label(other,.8,4.16,1.40,'1 AV',size=.24,d=.043)
    sign.b(.7,3.22,0,1.08,.25,.05,'sign white');label(sign,.7,3.22,.97,'ONE WAY',color='black iron',size=.13,d=.039)

def street_details():
    global OWNER
    OWNER='Street furniture · positions inferred from reference views'
    for args in [(-11.3,-5.5,1,0),(11.3,5.5,-1,0),(-11.3,5.65,0,-1),(11.3,-5.65,0,1)]:traffic_pole(*args)
    for x,z in [(-11.1,-34),(11.1,-33),(-11.1,32),(11.1,35),(-37,-5.5),(39,5.5)]:
        rod((x,.15,z),(x,7.6,z),.064,'metal',10)
        sx=-1 if x>0 else 1
        rod((x,7.6,z),(x+sx*.6,8.4,z),.055,'metal',10)
        rod((x+sx*.6,8.4,z),(x+sx*2.1,8.63,z),.045,'metal',10)
        box(x+sx*2.25,8.60,z,.61,.18,.30,'metal')
        box(x+sx*2.25,8.48,z,.50,.03,.24,'sign white')
    for x,z in [(-11.55,12.3),(11.62,-11.9),(-29.0,-5.6),(28.8,5.5)]:
        rod((x,.17,z),(x,.76,z),.18,'red iron',12)
        rod((x,.72,z),(x,.92,z),.15,'red iron',12,r2=.05)
        rod((x-.29,.56,z),(x+.29,.56,z),.095,'red iron',10)
        box(x,.25,z,.46,.12,.42,'black iron')
    for x,z in [(-12.1,-7.6),(12.0,7.6),(-12.0,7.6),(12.1,-7.6),(-29,-6.8),(13,-23)]:
        rod((x,.17,z),(x,1.10,z),.27,'black iron',16)
        rod((x,1.11,z),(x,1.13,z),.31,'metal',16)
        for i in range(12):
            a=i*math.tau/12;rod((x+math.sin(a)*.273,.28,z+math.cos(a)*.273),(x+math.sin(a)*.273,1.02,z+math.cos(a)*.273),.013,'metal',5)
    for x,z in [(-26,6.7),(12,-18),(-12,-28)]:
        for dz in [-.64,.64]:rod((x,.18,z+dz),(x,1.03,z+dz),.022,'metal')
        rod((x,1.03,z-.64),(x,1.03,z+.64),.022,'metal')
    for x,z in [(-11.5,40),(11.5,-39),(-43,-5.8)]:
        rod((x,.18,z),(x,3.22,z),.029,'metal')
        f=Facade(x-.34,z,1,0,.68);f.b(.34,2.65,0,.65,.93,.036,'sign white')
        label(f,.34,2.91,.58,'SPEED',color='black iron',size=.13,d=.026)
        label(f,.34,2.71,.58,'LIMIT',color='black iron',size=.13,d=.026)
        label(f,.34,2.39,.58,'25',color='black iron',size=.32,d=.026)

def tree(x,z,height,seed):
    global OWNER
    OWNER='Trees · approximate seasonal dressing'
    r=random.Random(seed)
    box(x,.18,z,2.05,.05,2.1,'soil')
    for dx in [-1.03,1.03]:box(x+dx,.26,z,.06,.14,2.15,'black iron')
    for dz in [-1.05,1.05]:box(x,.26,z+dz,2.1,.14,.06,'black iron')
    top=(x+.10,height*.41,z+.13)
    rod((x,.19,z),top,.17,'tree bark',10,r2=.09)
    tips=[]
    for i in range(8):
        a=i*math.tau/8+r.random()*.4
        end=(x+math.cos(a)*r.uniform(1.5,2.7),height*r.uniform(.51,.85),z+math.sin(a)*r.uniform(1.5,2.7))
        rod(top,end,.065,'tree bark',7,r2=.020)
        for j in range(3):
            tip=(end[0]+r.uniform(-1,1),end[1]+r.uniform(.3,1.6),end[2]+r.uniform(-1,1))
            rod(end,tip,.023,'tree bark',6,r2=.006);tips.append(tip)
    for tip in tips:
        for i in range(255):
            xx=tip[0]+r.gauss(0,.66);yy=tip[1]+r.gauss(0,.50);zz=tip[2]+r.gauss(0,.66)
            length=r.uniform(.105,.22);width=length*.46;a=r.random()*math.tau
            v=Vector((math.cos(a)*width,r.uniform(-.035,.045),math.sin(a)*width))
            t=Vector((-math.sin(a)*length,r.uniform(-.08,.09),math.cos(a)*length))
            c=Vector((xx,yy,zz));pts=[c-t,c-v,c+Vector((0,.035,0)),c+v,c+t]
            mat='leaf '+str(r.randrange(4))
            for inds in [(0,1,2),(0,2,3),(1,4,2),(2,4,3)]:
                ps=[pts[k] for k in inds];face(ps,mat);face(list(reversed(ps)),mat)

def car(x,z,color,angle=0):
    global OWNER
    OWNER='Parked vehicles · illustrative dressing'
    ca,sa=math.cos(angle),math.sin(angle)
    def p(u,y,v):return (x+u*ca+v*sa,y,z-u*sa+v*ca)
    # Smoothly tapered automobile surfaces, with separate glazing and wheel geometry.
    rings=[(-2.22,.69,.54),(-1.82,.86,.78),(-.90,.91,.82),(.82,.90,.79),(1.91,.81,.68),(2.15,.67,.52)]
    # Hull quad strips in local z; upper shoulders and wheel sills.
    for i in range(len(rings)-1):
        a,ww,hh=rings[i];b,vv,jj=rings[i+1]
        face([p(-ww,hh,a),p(ww,hh,a),p(vv,jj,b),p(-vv,jj,b)],color)
        for sign in [-1,1]:face([p(sign*ww,.36,a),p(sign*vv,.36,b),p(sign*vv,jj,b),p(sign*ww,hh,a)],color)
    for v,w,h in [rings[0],rings[-1]]:face([p(-w,.36,v),p(w,.36,v),p(w,h,v),p(-w,h,v)],color)
    # Cabin lower corners / roof corners.
    for sign in [-1,1]:
        face([p(sign*.80,.79,-1.10),p(sign*.79,.79,1.06),p(sign*.65,1.39,.66),p(sign*.65,1.39,-.57)],'dark glass')
        rod(p(sign*.80,.79,-1.10),p(sign*.65,1.39,-.57),.035,color)
        rod(p(sign*.79,.79,1.06),p(sign*.65,1.39,.66),.045,color)
        rod(p(sign*.73,.80,.10),p(sign*.65,1.39,.10),.037,'black iron')
        rod(p(sign*.82,.76,-1.2),p(sign*.82,.76,1.16),.016,'metal')
        for v in [-1.40,1.37]:
            rod(p(sign*.79,.40,v),p(sign*.96,.40,v),.33,'rubber',20)
            rod(p(sign*.97,.40,v),p(sign*.98,.40,v),.205,'metal',16)
            for k in range(5):
                a=k*math.tau/5
                rod(p(sign*.991,.40,v),p(sign*.991,.40+math.cos(a)*.18,v+math.sin(a)*.18),.025,'black iron',5)
    face([p(-.80,.79,-1.10),p(.80,.79,-1.10),p(.65,1.39,-.57),p(-.65,1.39,-.57)],'blue glass')
    face([p(-.79,.79,1.06),p(-.65,1.39,.66),p(.65,1.39,.66),p(.79,.79,1.06)],'dark glass')
    face([p(-.65,1.39,-.57),p(.65,1.39,-.57),p(.65,1.39,.66),p(-.65,1.39,.66)],color)
    for sign in [-1,1]:
        box(*p(sign*.91,.98,-.63),.19,.13,.24,color,angle)
        box(*p(sign*.52,.57,-2.18),.43,.17,.08,'sign white',angle)
        box(*p(sign*.5,.55,2.10),.34,.13,.07,'tail lamp',angle)
    box(*p(0,.48,-2.21),.64,.13,.04,'black iron',angle)
    box(*p(0,.45,2.15),.32,.13,.015,'yellow paint',angle)
    for sign in [-1,1]:
        # Door shut lines, handles, tire sidewalls and lamp surrounds catch the low sun.
        for v in [-.94,.13,1.03]:rod(p(sign*.907,.41,v),p(sign*.907,.75,v),.006,'black iron',5)
        for v in [-.25,.72]:box(*p(sign*.913,.70,v),.027,.035,.16,'metal',angle)
        for v in [-1.4,1.37]:
            for k in range(24):
                aa=k*math.tau/24;bb=(k+1)*math.tau/24
                rod(p(sign*.984,.40+math.cos(aa)*.275,v+math.sin(aa)*.275),p(sign*.984,.40+math.cos(bb)*.275,v+math.sin(bb)*.275),.012,'rubber',5)
        box(*p(sign*.70,.59,-2.16),.095,.13,.055,'amber signal',angle)
    for u in [-.22,-.11,0,.11,.22]:box(*p(u,.48,-2.235),.015,.11,.016,'metal',angle)
    for u in [-.23,.23]:rod(p(u,.855,-.95),p(u+.26,.85,-1.0),.009,'black iron',5)

def close_details():
    global OWNER
    OWNER='Architectural detail · visible elements interpreted from dated references'
    # Recessed entry surrounds and their small, recognizable hardware.
    for f,s,number in [(Facade(-15.35,-9.55,0,-1,8.1),4.1,'163'),(Facade(-15.32,23.22,0,-1,14.24),7.18,'159'),(Facade(16.06,-16.44,0,1,7.36),.20,'164'),(Facade(15.32,9.20,0,1,6.89),.29,'162'),(Facade(-15.38,8.97,-1,0,21.9),9.27,'242')]:
        label(f,s,3.01,.49,number,'black iron',.16,d=.43)
        f.b(s,1.43,.36,.13,.33,.048,'metal')
        for yy in [1.33,1.4,1.47]:
            f.b(s,yy,.391,.062,.013,.009,'black iron')
        f.b(s,2.30,.33,.13,.06,.065,'black iron')
        f.line((s+.07,.27,.27),(s+.07,2.22,.27),.008,'metal')
    # Cables are continuous catenaries with wall fixings, rather than straight decorations.
    for f,ends,height in [(Facade(-45.60,-9.51,1,0,30.25),(1.4,29),6.5),(Facade(16.11,-9.06,1,0,15.17),(.7,12.7),6.45),(Facade(31.74,9.11,-1,0,16.39),(1.4,15.7),6.97)]:
        a,b=ends
        for j in range(24):
            t=j/24;u=(j+1)/24
            f.line((a+(b-a)*t,height-.42*4*t*(1-t),.21),(a+(b-a)*u,height-.42*4*u*(1-u),.21),.011,'black iron')
        for s in [a,b]:f.b(s,height,.17,.07,.11,.12,'metal')
    # Masonry corner seams and sill weathering respect the existing bay schedules.
    for f,ys in [(Facade(-15.32,23.22,0,-1,14.24),[3.86,6.78,9.70,12.62,15.54]),(Facade(-15.38,8.97,-1,0,21.9),[3.86,6.78,9.70,12.62,15.54])]:
        for y in ys:
            for s in [.08,f.L-.08]:
                f.b(s,y+.60,.041,.08,1.48,.014,'stone weathering')
        for s in [.38+i*.63 for i in range(int(f.L/.63))]:
            for y in [18.29,18.58]:rod(f.p(s,y,.35),f.p(s,y,.38),.026,'brass',8)
    OWNER='Street surface detail · representative wear and utility furniture'
    r=random.Random(410)
    for sx in [-1,1]:
        for zz in range(-63,66,3):
            if abs(zz)<10:continue
            box(sx*10.815,.194,zz,.245,.005,.023,'concrete seam')
            # Tiny chipped curb edges and stains, with deterministic variation.
            for j in range(4):
                z=zz+r.uniform(-1.2,1.2)
                box(sx*10.69,.142,z,.032,r.uniform(.013,.04),r.uniform(.045,.17),'stone weathering')
        for zz in [-15,15,-42,41]:
            box(sx*10.37,.01,zz,.49,.02,.83,'black iron')
            for j in range(9):box(sx*10.37,.025,zz-.35+j*.082,.47,.011,.025,'metal')
    for x,z,w,d in [(2.6,4.0,1.72,1.53),(-2.8,-4.1,1.82,1.74),(-31,.2,1.5,1.6),(34,1,1.7,1.5)]:
        # Resurfaced rings around utilities keep the circular covers exposed.
        for side in [-1,1]:
            box(x+side*w*.40,.001,z,w*.2,.001,d,'concrete seam')
            box(x,.001,z+side*d*.4,w,.001,d*.2,'concrete seam')
    for x,z in [(-14.6,-22),(14.6,19),(-25,8.35),(31,-8.0)]:
        box(x,.182,z,1.30,.026,.78,'metal')
        for xx in [-.60+i*.10 for i in range(13)]:
            for zz in [-.31+i*.10 for i in range(7)]:
                box(x+xx,.200,z+zz,.052,.009,.009,'black iron',.65)
        for xx in [-.38,.38]:box(x+xx,.211,z,.12,.01,.06,'black iron')
    # Real street-scale fallen leaves, restrained and concentrated at the curb.
    for k in range(210):
        sx=r.choice([-1,1]);x=sx*r.uniform(10.95,11.55);z=r.uniform(-57,57)
        if abs(z)<9:continue
        a=r.random()*math.tau;w=r.uniform(.025,.045);h=r.uniform(.045,.09)
        c=Vector((x,.17,z));v=Vector((math.cos(a)*w,0,math.sin(a)*w));t=Vector((-math.sin(a)*h,.008,math.cos(a)*h))
        face([c-t,c+v,c+t,c-v],'shop cream' if k%3 else 'leaf 2')

    OWNER='Bicycles · illustrative parked street dressing'
    for x,z,angle in [(-12.1,-28,.08),(-26,6.7,1.57),(12,-18,-.05)]:
        ca,sa=math.cos(angle),math.sin(angle)
        def p(a,y,b=0):return (x+a*ca+b*sa,y,z-a*sa+b*ca)
        for cx in [-.53,.53]:
            for k in range(28):
                aa=k*math.tau/28;bb=(k+1)*math.tau/28
                rod(p(cx+.32*math.cos(aa),.52+.32*math.sin(aa)),p(cx+.32*math.cos(bb),.52+.32*math.sin(bb)),.022,'rubber',6)
                rod(p(cx,.52),p(cx+.30*math.cos(aa),.52+.30*math.sin(aa)),.0025,'metal',4)
        for a,b in [((-.53,.52),(-.19,1.02)),((-.19,1.02),(.42,1.04)),((.42,1.04),(.53,.52)),((-.53,.52),(.05,.53)),((.05,.53),(-.19,1.02)),((.05,.53),(.42,1.04))]:rod(p(*a),p(*b),.022,'cornice green',8)
        rod(p(-.19,1.02),p(-.22,1.14),.016,'metal',8)
        box(*p(-.24,1.15),.26,.065,.16,'rubber',angle)
        rod(p(.42,1.04),p(.43,1.20),.015,'metal',8)
        rod(p(.43,1.20,-.19),p(.43,1.20,.19),.017,'metal',8)

def flush():
    for (owner,mat),q in BATCHES.items():
        mesh=bpy.data.meshes.new(owner+' / '+mat)
        # Blender Z-up -> glTF Y-up yields original game coordinates on export.
        mesh.from_pydata([(p[0],-p[2],p[1]) for p in q['v']],[],q['f']);mesh.update()
        uv=mesh.uv_layers.new(name='UVMap')
        for poly in mesh.polygons:
            for li in poly.loop_indices:uv.data[li].uv=q['uv'][mesh.loops[li].vertex_index]
        obj=bpy.data.objects.new(owner+' / '+mat,mesh);bpy.context.collection.objects.link(obj)
        obj.data.materials.append(MATS[mat]);obj['provenance']=owner
        if owner.startswith('Parked vehicles') and (mat.startswith('car paint') or mat=='metal'):
            bevel=obj.modifiers.new('Soft manufactured edges','BEVEL');bevel.width=.025;bevel.segments=2
            bevel.limit_method='ANGLE'
            weighted=obj.modifiers.new('Weighted panel normals','WEIGHTED_NORMAL');weighted.keep_sharp=True
    for f,s,y,w,text,col,size,d,owner in TEXT:
        curve=bpy.data.curves.new(text,'FONT');curve.body=text;curve.size=size;curve.align_x='CENTER';curve.align_y='CENTER';curve.extrude=.001
        curve.resolution_u=3
        obj=bpy.data.objects.new(owner+' / '+text,curve);bpy.context.collection.objects.link(obj)
        xx,yy,zz=f.p(s,y,d);obj.location=(xx,-zz,yy)
        # Text plane XY, local +Z faces outward. Local +Y points up.
        from mathutils import Matrix
        right=Vector((f.rx,-f.rz,0));up=Vector((0,0,1));normal=Vector((f.nx,-f.nz,0))
        obj.rotation_euler=Matrix((right,up,normal)).transposed().to_euler()
        obj.data.materials.append(MATS[col]);bpy.context.view_layer.update()
        local_width=max(v[0] for v in obj.bound_box)-min(v[0] for v in obj.bound_box)
        if local_width>w and local_width>0:curve.size*=w/local_width

def lighting():
    world=bpy.data.worlds.new('Warm late afternoon');world.use_nodes=True;bpy.context.scene.world=world
    nodes=world.node_tree.nodes;nodes.clear()
    bg=nodes.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.38
    sky=nodes.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(26);sky.sun_rotation=math.radians(143);sky.sun_disc=False
    world.node_tree.links.new(sky.outputs['Color'],bg.inputs['Color'])
    output=nodes.new('ShaderNodeOutputWorld');world.node_tree.links.new(bg.outputs['Background'],output.inputs['Surface'])
    light=bpy.data.lights.new('Afternoon sun','SUN');light.energy=2.3;light.angle=.07;light.color=(1.0,.79,.55)
    ob=bpy.data.objects.new('Afternoon sun',light);bpy.context.collection.objects.link(ob);ob.rotation_euler=Vector((-.32,.81,-.48)).to_track_quat('-Z','Y').to_euler()
    for x,z in [(-16.4,-11.8),(-29.8,10.3),(-16.4,-21.3),(16.4,19.6),(-17.0,16.1)]:
        ll=bpy.data.lights.new('Shop interior glow','POINT');ll.energy=32;ll.color=(1,.61,.28);ll.shadow_soft_size=.65
        oo=bpy.data.objects.new('Shop interior glow',ll);bpy.context.collection.objects.link(oo);oo.location=(x,-z,2.25)
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
    scene.cycles.max_bounces=5;scene.cycles.diffuse_bounces=3;scene.cycles.glossy_bounces=3
    scene.view_settings.view_transform='AgX';scene.render.resolution_x=1600;scene.render.resolution_y=1000;scene.render.resolution_percentage=100

def export_and_render():
    scene=bpy.context.scene
    bpy.ops.object.select_all(action='DESELECT')
    for ob in scene.objects:
        if ob.type in ['MESH','FONT']:ob.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(OUT/'first-and-10th.glb'),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_extras=True,export_cameras=False,export_lights=False,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=8,export_draco_position_quantization=15,export_draco_normal_quantization=10,export_draco_texcoord_quantization=14)
    info={'origin':BASE['origin'],'units':'metres','bounds':[-60,-66,60,66],'coreBuildings':4,'objects':len(BATCHES),'triangles':sum(sum(len(f)-2 for f in q['f']) for q in BATCHES.values()),'revision':'02','referenceYears':'2021–2026','businessesChecked':'2026-09-06','notes':'Photo-guided reconstruction with current occupancy checks; not a survey or current-day capture. Interior layouts, shop partition widths, street furniture and hidden geometry remain estimates. Closed or unconfirmed businesses are identified in businesses.json.'}
    (OUT/'model-info.json').write_text(json.dumps(info,indent=2))
    lighting()
    cam_data=bpy.data.cameras.new('street-height camera');cam=bpy.data.objects.new('street-height camera',cam_data);bpy.context.collection.objects.link(cam);scene.camera=cam;cam_data.lens=25
    # Render the actual authored mesh, not an AI concept or browser screenshot.
    def shot(name,pos,target):
        cam.location=(pos[0],-pos[2],pos[1]);look=Vector((target[0],-target[2],target[1]));cam.rotation_euler=(look-cam.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
    shot('intersection-render',(6,1.72,22),(-16,6.2,-10))
    shot('southwest-render',(10,1.72,-13),(-20,9.4,18))
    # The recipe and GLB are the editable deliverable; keep bulky Blender internals out of the website.
    print('RECONSTRUCTION_COMPLETE',json.dumps(info),flush=True)

print('Building individual facades',flush=True)
build_corners();build_tower();build_neighbors();build_road();street_details();close_details()
for args in [(-12.8,18.7,9.6,42),(-33,6.6,8.0,11),(-33,-6.8,8.4,15),(12.5,-23.4,9.0,71),(12.7,33.6,8.2,17),(41,6.9,8.1,22),(-13,-40.1,8.7,63),(39,-6.8,7.8,29)]:tree(*args)
for i,(x,z,a) in enumerate([(8.90,19,0),(8.90,25,0),(8.90,-19,0),(8.9,-26,0),(8.9,42,0),(-4.4,-24,0),(-4.4,34,0),(-23,3.65,math.pi/2),(-29,3.65,math.pi/2),(25,-3.6,-math.pi/2),(32,-3.6,-math.pi/2)]):car(x,z,'car paint '+str(i%5),a)
print('Constructing mesh batches',flush=True)
flush();export_and_render()
