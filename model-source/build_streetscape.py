"""Reproducible small street objects for all ten blocks; illustrative placement.

Run: blender --background -t 6 --python-exit-code 1 --python model-source/build_streetscape.py
No photographs or unverified business identities are used by this recipe.
"""
import bpy, math, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist/reconstruction/neighborhood'
kit=ROOT/'model-source/build_intersection.py'
ns={'__file__':str(kit),'__name__':'street_detail_components'}
exec(compile(kit.read_text().split("print('Building individual facades'")[0],str(kit),'exec'),ns)
box,rod,face,material=[ns[k] for k in ['box','rod','face','material']]
material('hydrant enamel',(.22,.245,.21),.55,.45)
material('street bin green',(.035,.09,.065),.7,.45)
material('bicycle enamel',(.14,.24,.21),.46,.35)

def bicycle():
    for cx in [-.54,.54]:
        for k in range(28):
            a=k*math.tau/28;b=(k+1)*math.tau/28
            for r,t,mat in [(.33,.020,'rubber'),(.299,.007,'metal')]:
                rod((cx+r*math.cos(a),.55+r*math.sin(a),0),(cx+r*math.cos(b),.55+r*math.sin(b),0),t,mat,6)
            if k%2==0:rod((cx,.55,0),(cx+.30*math.cos(a),.55+.30*math.sin(a),0),.003,'metal',4)
        rod((cx,.55,-.045),(cx,.55,.045),.035,'metal',8)
    for a,b in [((-.54,.55),(-.19,1.04)),((-.19,1.04),(.40,1.06)),((.40,1.06),(.54,.55)),((-.54,.55),(.04,.56)),((.04,.56),(-.19,1.04)),((.04,.56),(.40,1.06))]:
        rod((*a,0),(*b,0),.022,'bicycle enamel',8)
    rod((-.19,1.04,0),(-.21,1.16,0),.016,'metal',8)
    box(-.24,1.17,0,.27,.060,.16,'rubber')
    rod((.40,1.06,0),(.44,1.24,0),.016,'metal',8)
    rod((.44,1.24,-.21),(.44,1.24,.21),.018,'metal',8)
    for z in [-.19,.19]:box(.44,1.24,z,.032,.036,.12,'rubber')
    rod((.04,.56,-.14),(.04,.56,.14),.015,'metal',8)
    for z,y in [(-.14,.44),(.14,.68)]:
        rod((.04,.56,z),(.15,y,z),.014,'metal',6);box(.15,y,z,.10,.03,.08,'rubber')
    rod((-.03,.56,.025),(-.12,.19,.23),.012,'metal',6)
    # Compact U-lock and rear reflector.
    box(-.43,.95,0,.15,.038,.25,'metal');box(-.58,.93,.02,.043,.07,.07,'tail lamp')

def hydrant():
    for y,h,r in [(.23,.10,.20),(.47,.42,.13),(.70,.10,.18),(.82,.15,.14)]:
        rod((0,y-h/2,0),(0,y+h/2,0),r,'hydrant enamel',16)
    rod((0,.89,0),(0,.99,0),.14,'hydrant enamel',16,.06)
    rod((0,.98,0),(0,1.035,0),.048,'metal',6)
    for side in [-1,1]:
        rod((0,.62,0),(side*.24,.62,0),.088,'hydrant enamel',12)
        rod((side*.23,.62,0),(side*.27,.62,0),.063,'metal',6)
    rod((0,.55,0),(0,.55,.22),.10,'hydrant enamel',12)
    rod((0,.55,.22),(0,.55,.245),.072,'metal',6)
    for k in range(10):
        a=k*math.pi/10;b=(k+1)*math.pi/10
        rod((-.24+.24*k/10,.62-.17*math.sin(a),.10),(-.24+.24*(k+1)/10,.62-.17*math.sin(b),.10),.006,'metal',4)
    for x in [-.14,.14]:
        for z in [-.14,.14]:rod((x,.25,z),(x,.29,z),.021,'metal',6)

def litter_bin():
    rod((0,.19,0),(0,.26,0),.265,'street bin green',20)
    rod((0,.96,0),(0,1.04,0),.305,'street bin green',24)
    # An open top, dark liner and individually spaced steel ribs.
    rod((0,.28,0),(0,.82,0),.225,'rubber',20,.245)
    for k in range(28):
        a=k*math.tau/28
        rod((.24*math.cos(a),.26,.24*math.sin(a)),(.285*math.cos(a),.99,.285*math.sin(a)),.012,'street bin green',6)
    box(0,.67,.28,.23,.14,.025,'street bin green')
    for k in range(3):box(0,.705-k*.035,.297,.14,.012,.008,'sign white')

def utility_cover():
    rod((0,.006,0),(0,.020,0),.39,'black iron',40)
    rod((0,.021,0),(0,.028,0),.345,'metal',40)
    for k in range(-5,6):
        z=k*.051;w=2*math.sqrt(max(0,.32**2-z*z))
        box(0,.032,z,w,.008,.017,'black iron')
    for x in [-.20,.20]:box(x,.034,0,.043,.012,.079,'black iron')

def drain_grate():
    box(0,.010,0,.48,.024,.81,'black iron')
    for z in [-.37,.37]:box(0,.027,z,.48,.016,.045,'metal')
    for x in [-.21,.21]:box(x,.027,0,.045,.016,.80,'metal')
    for k in range(9):box(0,.029,-.32+k*.08,.42,.015,.026,'metal')

records=[]
for name,build in [('bicycle-detail',bicycle),('hydrant',hydrant),('litter-bin',litter_bin),('utility-cover',utility_cover),('drain-grate',drain_grate)]:
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    ns['BATCHES'].clear();ns['TEXT'].clear();ns['OWNER']=name+' · illustrative street object'
    build();ns['flush']()
    bpy.ops.object.select_all(action='SELECT')
    target=OUT/(name+'.glb')
    bpy.ops.export_scene.gltf(filepath=str(target),export_format='GLB',use_selection=True,export_yup=True,export_extras=True,export_cameras=False,export_lights=False,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=15)
    records.append({'url':'neighborhood/'+name+'.glb','bytes':target.stat().st_size,'triangles':sum(len(f)-2 for q in ns['BATCHES'].values() for f in q['f'])})
(OUT/'streetscape-info.json').write_text(json.dumps({'revision':'03','recipe':'model-source/build_streetscape.py','placement':'Illustrative, deterministic street dressing; no measured furniture survey.','assets':records},indent=2)+'\n')
print('STREETSCAPE_COMPLETE',json.dumps(records),flush=True)
