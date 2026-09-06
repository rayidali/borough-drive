"""Reusable representative NYC street props, metres, game Y-up.

Run: blender -b -t 6 --python build_street_props.py
Outputs are Draco-compressed GLBs next to this script. No external inputs.
Palette and mesh batching follow Borough Drive's reconstruction helper kit.
Street furniture is illustrative seasonal dressing, not a surveyed location.
"""
import bpy, bmesh, math, random, json
from pathlib import Path
from mathutils import Vector

OUT = Path(__file__).resolve().parents[1] / 'dist/reconstruction/neighborhood'
OUT.mkdir(exist_ok=True)
MATS, BATCHES = {}, {}

def clear():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    BATCHES.clear()

def material(name, color, rough=.8, metal=0, double_sided=False):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*color, 1)
    shader.inputs['Roughness'].default_value = rough
    shader.inputs['Metallic'].default_value = metal
    mat.use_backface_culling = not double_sided
    MATS[name] = mat

material('black iron', (.026,.029,.028), .60, .58)
material('wood', (.16,.066,.028), .86)
material('soil', (.052,.041,.023), 1)
material('tree bark', (.14,.105,.06), .98)
for i,c in enumerate([(.072,.16,.032),(.09,.20,.04),(.12,.24,.052),(.17,.26,.068)]):
    material('leaf '+str(i), c, .92, double_sided=True)

def face(points, mat):
    q = BATCHES.setdefault(mat, {'v': [], 'f': []})
    start = len(q['v'])
    q['v'].extend([tuple(p) for p in points])
    q['f'].append(tuple(range(start, start+len(points))))

def box(x,y,z,w,h,d,mat):
    ps=[(x+a*w/2,y+b*h/2,z+c*d/2) for a,b,c in
        [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
    for ids in [(0,3,2,1),(4,5,6,7),(0,4,7,3),(1,2,6,5),(3,7,6,2),(0,1,5,4)]:
        face([ps[i] for i in ids], mat)

def rod(a,b,r,mat,sides=8,r2=None):
    a,b=Vector(a),Vector(b)
    n=(b-a).normalized()
    t=n.cross(Vector((0,1,0)))
    if t.length<.001: t=n.cross(Vector((1,0,0)))
    t.normalize(); s=n.cross(t); r2=r if r2 is None else r2
    pa=[a+r*(t*math.cos(i*math.tau/sides)+s*math.sin(i*math.tau/sides)) for i in range(sides)]
    pb=[b+r2*(t*math.cos(i*math.tau/sides)+s*math.sin(i*math.tau/sides)) for i in range(sides)]
    for i in range(sides):
        j=(i+1)%sides; face([pa[i],pa[j],pb[j],pb[i]],mat)
    face(list(reversed(pa)),mat);face(pb,mat)

def path(points, radii, mat, sides=8):
    # Joined rings avoid exposed tube caps at bends in trunks and ironwork.
    points=list(map(Vector,points)); rings=[]; tangent=None
    for i,p in enumerate(points):
        n=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized()
        if tangent is None:
            tangent=n.cross(Vector((0,1,0)))
            if tangent.length<.001: tangent=n.cross(Vector((1,0,0)))
        else: tangent=tangent-n*tangent.dot(n)
        tangent.normalize(); bitangent=n.cross(tangent)
        rings.append([p+radii[i]*(tangent*math.cos(j*math.tau/sides)+bitangent*math.sin(j*math.tau/sides)) for j in range(sides)])
    for i in range(len(rings)-1):
        for j in range(sides):
            k=(j+1)%sides;face([rings[i][j],rings[i][k],rings[i+1][k],rings[i+1][j]],mat)
    face(list(reversed(rings[0])),mat);face(rings[-1],mat)

def leaf(center, length, angle, pitch, mat, rng):
    # A pointed folded diamond: crisp leaf silhouette and subtle ridge shading.
    t=Vector((math.cos(angle)*math.cos(pitch),math.sin(pitch),math.sin(angle)*math.cos(pitch)))
    v=Vector((-math.sin(angle),rng.uniform(-.30,.30),math.cos(angle))).normalized()
    n=t.cross(v).normalized()
    c=Vector(center); w=length*rng.uniform(.35,.47)
    points=[c-t*length,c-v*w,c+n*length*.11,c+v*w,c+t*length]
    for ids in [(0,1,2),(0,2,3),(1,4,2),(2,4,3)]: face([points[i] for i in ids],mat)

def tree():
    rng=random.Random(52210)
    # Narrow pedestrian-compatible tree well and guard, 1.40 by 1.68 m.
    box(0,.018,0,1.36,.036,1.64,'soil')
    for x in [-.70,.70]: box(x,.038,0,.05,.075,1.72,'black iron')
    for z in [-.84,.84]: box(0,.038,z,1.44,.075,.05,'black iron')
    for x in [-.69,.69]:
        for z in [-.83,.83]:
            rod((x,.035,z),(x,.64,z),.021,'black iron',8)
            rod((x,.64,z),(x,.68,z),.028,'black iron',8,.006)
        for y in [.12,.56]: rod((x,y,-.83),(x,y,.83),.014,'black iron',6)
        for j in range(7):
            z=-.66+j*.22
            rod((x,.12,z),(x,.56,z),.009,'black iron',6)
    for z in [-.83,.83]:
        for y in [.12,.56]: rod((-.69,y,z),(.69,y,z),.014,'black iron',6)
        for j in range(5):
            x=-.48+j*.24
            rod((x,.12,z),(x,.56,z),.009,'black iron',6)
    # Slight lean and uneven taper remain visible between foliage lobes.
    trunk=[(0,.025,0),(.055,1.05,.045),(-.045,2.32,.035),(.11,3.52,.14),(.04,4.70,.17),(.22,5.80,.08),(.10,6.95,.19)]
    path(trunk,[.205,.18,.153,.126,.094,.067,.029],'tree bark',12)
    for i in range(7):
        a=i*math.tau/7+.13
        path([(.40*math.cos(a),.018,.40*math.sin(a)),(.20*math.cos(a),.10,.20*math.sin(a)),(.08, .50,.035)], [.025,.055,.08], 'tree bark',7)
    tips=[]
    for i in range(9):
        a=i*2.399963+rng.uniform(-.21,.21)
        base=Vector((.06,3.0+(i%4)*.57,.10))
        reach=rng.uniform(1.55,2.36)
        end=Vector((math.cos(a)*reach,5.55+(i%3)*.51+rng.uniform(-.18,.18),math.sin(a)*reach))
        bend=base.lerp(end,.48)+Vector((rng.uniform(-.12,.12),.13,rng.uniform(-.12,.12)))
        path([base,bend,end],[.080 if i<5 else .065,.048,.024],'tree bark',8)
        for j in range(3):
            b=a+(j-1)*.68+rng.uniform(-.13,.13)
            tip=end+Vector((math.cos(b)*rng.uniform(.40,.85),rng.uniform(.45,1.10),math.sin(b)*rng.uniform(.40,.85)))
            joint=end.lerp(tip,.54)+Vector((0,.11,0))
            path([end,joint,tip],[.025,.015,.005],'tree bark',7)
            tips.append((tip,rng.uniform(.49,.70),rng.uniform(.41,.60)))
            for k in range(2):
                twig=joint+Vector((math.cos(b+k*1.25)*.35,.23,math.sin(b+k*1.25)*.35))
                rod(joint,twig,.008,'tree bark',5,.002)
    for i in range(3):
        a=i*math.tau/3+.5
        tip=Vector((math.cos(a)*.62,7.80+i*.12,math.sin(a)*.62))
        path([trunk[-2],trunk[-1],tip],[.043,.028,.004],'tree bark',8)
        tips.append((tip,.56,.51))
    # Individually oriented leaves gather around twig ends; clear gaps reveal
    # the branching silhouette. No sphere meshes or opaque canopy envelopes.
    for tip, spread, vertical in tips:
        for i in range(136):
            while True:
                dx,dy,dz=[rng.uniform(-1,1) for _ in range(3)]
                if dx*dx+dy*dy+dz*dz<=1: break
            center=tip+Vector((dx*spread,dy*vertical,dz*spread))
            leaf(center,rng.uniform(.125,.205),rng.uniform(0,math.tau),rng.uniform(-.77,.72),'leaf '+str(rng.choices(range(4),[3,5,5,2])[0]),rng)
    # Preserve metric height explicitly across seeded variations.
    tallest=max(p[1] for q in BATCHES.values() for p in q['v'])
    factor=(8.65-2.8)/(tallest-2.8)
    for mat,q in BATCHES.items():
        if mat=='tree bark' or mat.startswith('leaf '):
            q['v']=[(x,2.8+(y-2.8)*factor if y>2.8 else y,z) for x,y,z in q['v']]

def bench():
    # Bench length 1.94 m; seat 0.47 m above ground, front toward +Z.
    for i in range(5): box(0,.465,.215-i*.105,1.94,.044,.084,'wood')
    # Back slats recede gently as they rise, with open spaces between them.
    for i in range(4):
        y=.615+i*.106; z=-.30-(y-.55)*.21
        box(0,y,z,1.94,.084,.044,'wood')
    for x in [-.78,.78]:
        # Cast-iron leg profile, curved seat carrier, back rise, and armrest.
        path([(x,.035,.28),(x,.21,.20),(x,.40,.16),(x,.425,.04),(x,.425,-.20),(x,.51,-.28),(x,.72,-.32),(x,.995,-.40)],
             [.035,.030,.029,.033,.034,.031,.028,.024],'black iron',10)
        path([(x,.425,-.19),(x,.24,-.21),(x,.035,-.36)],[.031,.029,.038],'black iron',10)
        for z in [.28,-.36]: box(x,.018,z,.16,.036,.115,'black iron')
        # Smoothly bent arm running from the front support to the back frame.
        points=[(x,.43,.195),(x,.57,.22),(x,.645,.19),(x,.675,.11),(x,.68,-.04),(x,.685,-.18),(x,.72,-.32)]
        path(points,[.020]*len(points),'black iron',10)
        # Seat and back fasteners are small visible iron disks.
        for i in range(5): rod((x,.487,.215-i*.105),(x,.493,.215-i*.105),.0085,'black iron',8)
        for i in range(4):
            y=.615+i*.106; z=-.30-(y-.55)*.21
            rod((x,y,z+.022),(x,y,z+.028),.0085,'black iron',8)
    rod((-.78,.24,-.20),(.78,.24,-.20),.019,'black iron',10)

def export(name, description):
    owner=name.replace('-',' ').title()
    parent=bpy.data.objects.new(owner,None)
    bpy.context.collection.objects.link(parent)
    parent['description']=description
    parent['units']='metres'
    parent['coordinates']='Y-up; origin on ground at center'
    for mat,q in BATCHES.items():
        mesh=bpy.data.meshes.new(owner+' / '+mat)
        mesh.from_pydata([(x,-z,y) for x,y,z in q['v']],[],q['f']);mesh.update()
        if mat=='wood':
            bm=bmesh.new();bm.from_mesh(mesh)
            bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001)
            bm.to_mesh(mesh);bm.free();mesh.update()
        obj=bpy.data.objects.new(owner+' / '+mat,mesh)
        bpy.context.collection.objects.link(obj)
        obj.data.materials.append(MATS[mat]);obj.parent=parent
        if mat=='wood':
            bevel=obj.modifiers.new('Soft slat edges','BEVEL');bevel.width=.006;bevel.segments=2
            bevel.limit_method='ANGLE'
            weighted=obj.modifiers.new('Weighted wood normals','WEIGHTED_NORMAL');weighted.keep_sharp=True
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(filepath=str(OUT/(name+'.glb')),export_format='GLB',use_selection=True,
        export_apply=True,export_yup=True,export_extras=True,export_cameras=False,export_lights=False,
        export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=8,
        export_draco_position_quantization=15,export_draco_normal_quantization=10)
    deps=bpy.context.evaluated_depsgraph_get()
    triangles=0
    for obj in bpy.context.scene.objects:
        if obj.type=='MESH':
            ev=obj.evaluated_get(deps); mesh=ev.to_mesh(); mesh.calc_loop_triangles()
            triangles+=len(mesh.loop_triangles);ev.to_mesh_clear()
    vertices=[p for q in BATCHES.values() for p in q['v']]
    bounds=[[round(min(p[i] for p in vertices),4) for i in range(3)], [round(max(p[i] for p in vertices),4) for i in range(3)]]
    return {'file':name+'.glb','triangles':triangles,'meshes':len(BATCHES),'bytes':(OUT/(name+'.glb')).stat().st_size,'boundsXYZ':bounds,'description':description}

if __name__=='__main__':
    clear();tree()
    infos=[export('street-tree','Mature 8.65 m street tree with irregular branches, individual folded leaves, soil well and narrow black iron guard. Representative seasonal dressing.')]
    clear();bench()
    infos.append(export('park-bench','Slatted wood park bench with black cast-iron frame, armrests, feet and visible fasteners. Faces +Z. Representative street dressing.'))
    (OUT/'prop-info.json').write_text(json.dumps({'units':'metres','upAxis':'Y','props':infos},indent=2))
    print(json.dumps(infos,indent=2))
