"""Reusable Borough Drive extra props. Outputs Draco GLBs beside this script.

Run with Blender:
  blender -b -t 6 --python build_extra_props.py -- --kit /path/to/build_intersection.py

Only the helper prefix before the source's main-build marker is evaluated;
the original scene, full core model, and export/render entry point never run.
The source kit is read-only. Its existing palette and car are reused.
"""
import argparse, math, json, sys, bpy
from pathlib import Path
from mathutils import Vector

OUT=Path(__file__).resolve().parents[1]/'dist/reconstruction/neighborhood'
args=argparse.ArgumentParser()
args.add_argument('--kit',default=str(Path(__file__).resolve().with_name('build_intersection.py')))
opt=args.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
kit_path=Path(opt.kit).resolve()
source=kit_path.read_text()
marker="print('Building individual facades'"
if marker not in source: raise RuntimeError('Required helper/main boundary is absent from kit')
kit={'__file__':str(kit_path),'__name__':'borough_drive_prop_helper'}
exec(compile(source.split(marker,1)[0],str(kit_path),'exec'),kit)
MATS=kit['MATS'];BATCHES=kit['BATCHES'];face=kit['face'];rod=kit['rod'];box=kit['box']

def clear(owner):
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    BATCHES.clear();kit['TEXT'].clear();kit['OWNER']=owner

def tube(points,radii,mat,sides=10):
    points=list(map(Vector,points));rings=[];t=None
    for i,p in enumerate(points):
        n=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized()
        if t is None:
            t=n.cross(Vector((0,1,0)))
            if t.length<.001:t=n.cross(Vector((1,0,0)))
        else:t=t-n*t.dot(n)
        t.normalize();s=n.cross(t)
        rings.append([p+radii[i]*(t*math.cos(j*math.tau/sides)+s*math.sin(j*math.tau/sides)) for j in range(sides)])
    for i in range(len(rings)-1):
        for j in range(sides):
            k=(j+1)%sides;face([rings[i][j],rings[i][k],rings[i+1][k],rings[i+1][j]],mat)
    face(list(reversed(rings[0])),mat);face(rings[-1],mat)

def consolidate(remap):
    combined={}
    for (owner,mat),q in BATCHES.items():
        target=combined.setdefault((owner,remap.get(mat,mat)),{'v':[],'f':[],'uv':[]})
        offset=len(target['v']);target['v'].extend(q['v']);target['uv'].extend(q['uv'])
        target['f'].extend(tuple(i+offset for i in f) for f in q['f'])
    BATCHES.clear();BATCHES.update(combined)

def ground_center():
    vertices=[p for q in BATCHES.values() for p in q['v']]
    low=[min(p[i] for p in vertices) for i in range(3)]
    high=[max(p[i] for p in vertices) for i in range(3)]
    shift=((low[0]+high[0])*.5,low[1],(low[2]+high[2])*.5)
    for q in BATCHES.values():q['v']=[tuple(p[i]-shift[i] for i in range(3)) for p in q['v']]

def parked_car():
    clear('Parked Car')
    kit['material']('sage car paint',(.245,.315,.265),.29,.46)
    kit['car'](0,0,'sage car paint',0)
    # Keep the kit body, lamp, wheel and trim geometry, reducing material changes.
    consolidate({'blue glass':'dark glass','black iron':'rubber','yellow paint':'sign white'})
    ground_center()

def lamppost():
    clear('Street Lamppost')
    kit['material']('lamp diffuser',(.74,.79,.68),.36,.15,emission=.16)
    # Ground-centered pole; the curved arm and cobra-style head extend toward +X.
    rod((0,0,0),(0,.15,0),.22,'metal',8)
    rod((0,.15,0),(0,.52,0),.145,'metal',10,.103)
    rod((0,.52,0),(0,7.30,0),.084,'metal',12,.048)
    for x in [-.135,.135]:
        for z in [-.135,.135]:rod((x,.11,z),(x,.18,z),.022,'black iron',6)
    box(0,.57,.091,.09,.23,.013,'black iron')
    rod((0,.70,.10),(0,.715,.10),.016,'metal',6)
    points=[]
    for i in range(13):
        a=(math.pi/2)*(i/12)
        points.append((1.1-1.1*math.cos(a),7.23+.76*math.sin(a),0))
    points.extend([(1.47,7.99,0),(1.79,7.99,0)])
    tube(points,[.048-i*.00075 for i in range(len(points))],'metal',10)
    rod((0,7.09,0),(.10,7.38,0),.060,'metal',10)
    # Tapered luminaire body, with its actual down-facing light panel recessed.
    rings=[(1.54,7.99,.11),(1.75,8.05,.19),(2.13,8.025,.17),(2.26,7.975,.09)]
    for i in range(len(rings)-1):
        x,y,w=rings[i];u,v,d=rings[i+1]
        face([(x,y,-w),(u,v,-d),(u,v,d),(x,y,w)],'metal')
        for sign in [-1,1]:face([(x,y,sign*w),(x,7.86,sign*w),(u,7.86,sign*d),(u,v,sign*d)],'metal')
        face([(x,7.86,-w),(x,7.86,w),(u,7.86,d),(u,7.86,-d)],'lamp diffuser')
    for x,y,w in [rings[0],rings[-1]]:face([(x,7.86,-w),(x,y,-w),(x,y,w),(x,7.86,w)],'metal')
    box(1.91,7.849,0,.43,.018,.22,'lamp diffuser')

def traffic_signal():
    clear('Traffic Signal')
    kit['material']('unlit red lens',(.20,.020,.012),.28,.08)
    kit['material']('unlit amber lens',(.20,.075,.007),.32,.08)
    kit['material']('active green lens',(.07,.56,.21),.28,.08,emission=1.4)
    rod((0,0,0),(0,.14,0),.20,'black iron',8)
    rod((0,.14,0),(0,.49,0),.108,'black iron',10,.080)
    rod((0,.49,0),(0,4.72,0),.058,'black iron',10,.039)
    for x in [-.115,.115]:
        for z in [-.115,.115]:rod((x,.10,z),(x,.165,z),.018,'metal',6)
    tube([(0,4.58,0),(.07,4.70,0),(.25,4.76,0),(1.04,4.76,0),(1.17,4.68,0),(1.17,4.47,0)], [.039]*6,'black iron',10)
    box(1.17,3.88,0,.40,1.13,.26,'signal yellow')
    box(1.17,3.88,.141,.32,1.04,.034,'black iron')
    for cy,mat in [(4.21,'unlit red lens'),(3.88,'unlit amber lens'),(3.55,'active green lens')]:
        rod((1.17,cy,.158),(1.17,cy,.180),.11,'black iron',20)
        rod((1.17,cy,.181),(1.17,cy,.189),.092,mat,20)
        for i in range(12):
            a=i*math.pi/12;b=(i+1)*math.pi/12
            face([(1.17+.118*math.cos(a),cy+.118*math.sin(a),.16),
                  (1.17+.118*math.cos(b),cy+.118*math.sin(b),.16),
                  (1.17+.118*math.cos(b),cy+.118*math.sin(b),.35),
                  (1.17+.118*math.cos(a),cy+.118*math.sin(a),.35)],'black iron')
    consolidate({'metal':'black iron'})

def export(name,description):
    parent=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(parent)
    parent['units']='metres';parent['upAxis']='Y';parent['description']=description
    for (owner,mat),q in BATCHES.items():
        mesh=bpy.data.meshes.new(name+' / '+mat)
        mesh.from_pydata([(p[0],-p[2],p[1]) for p in q['v']],[],q['f']);mesh.update()
        obj=bpy.data.objects.new(name+' / '+mat,mesh);bpy.context.collection.objects.link(obj)
        obj.data.materials.append(MATS[mat]);obj.parent=parent
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(filepath=str(OUT/(name+'.glb')),export_format='GLB',use_selection=True,
        export_apply=True,export_yup=True,export_extras=True,export_cameras=False,export_lights=False,
        export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=8,
        export_draco_position_quantization=15,export_draco_normal_quantization=10)
    vertices=[p for q in BATCHES.values() for p in q['v']]
    info={'file':name+'.glb','bytes':(OUT/(name+'.glb')).stat().st_size,
        'triangles':sum(len(f)-2 for q in BATCHES.values() for f in q['f']),'meshes':len(BATCHES),
        'boundsXYZ':[[round(min(p[i] for p in vertices),4) for i in range(3)], [round(max(p[i] for p in vertices),4) for i in range(3)]],
        'description':description}
    return info

infos=[]
parked_car();infos.append(export('parked-car','Original helper kit car in neutral sage. Front points -Z; XZ bounds centered, tires touch Y=0.'))
lamppost();infos.append(export('street-furniture','Representative 8.05 m NYC curved-arm streetlamp. Origin at pole ground center; lamp arm extends +X.'))
traffic_signal();infos.append(export('traffic-signal','Representative single vertical three-lens traffic signal. Pole-centered ground origin, head on +X arm, front faces +Z. Only green lens illuminated.'))
(OUT/'extra-prop-info.json').write_text(json.dumps({'kitSource':str(kit_path),'units':'metres','upAxis':'Y','props':infos},indent=2))
print(json.dumps(infos,indent=2))
# Test each compressed asset by importing through Blender's Draco decoder.
for info in infos:
    clear('verify')
    bpy.ops.import_scene.gltf(filepath=str(OUT/info['file']))
    imported=[o for o in bpy.context.scene.objects if o.type=='MESH']
    if len(imported)!=info['meshes']:raise RuntimeError('Unexpected imported mesh count for '+info['file'])
    print('VERIFIED IMPORT',info['file'],len(imported),'meshes')
