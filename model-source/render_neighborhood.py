"""Render exported neighborhood geometry for asset review, without a browser.

Run: blender -b -t 6 --python model-source/render_neighborhood.py
The published viewer supplies its own lighting, streaming and postprocessing.
"""
import bpy,math,json,argparse,sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'dist/reconstruction'
ap=argparse.ArgumentParser();ap.add_argument('--output',default='/tmp/borough-neighborhood-renders');args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=Path(args.output);OUT.mkdir(parents=True,exist_ok=True)
data=json.loads((ASSETS/'neighborhood.json').read_text())
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def load(path):
 before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(path));return [o for o in bpy.data.objects if o not in before]
for name in ['block-2-2','block-3-2','block-4-2','block-5-2','edge-east']:
 load(ASSETS/'neighborhood'/f'{name}.glb')
def material(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.9;return m
asphalt=material('Render asphalt',(.095,.109,.105));pavement=material('Render sidewalk',(.39,.39,.34));grass=material('Render park',(.12,.19,.09));white=material('Render paint',(.65,.64,.54))
def box(x,y,z,w,h,d,mat):
 bpy.ops.mesh.primitive_cube_add(size=1,location=(x,-z,y));o=bpy.context.object;o.scale=(w,d,h);o.data.materials.append(mat);return o
box(120,-.15,50,420,.3,530,asphalt)
for lo,hi in [(10.75,204.7),(223.3,272)]:
 for zi in range(len(data['streets'])-1):
  za=data['streets'][zi][1]+4.95;zb=data['streets'][zi+1][1]-4.95;box((lo+hi)/2,.07,(za+zb)/2,hi-lo,.2,zb-za,pavement)
box(228.15,.19,114,9.7,.1,213,pavement);box(252.5,.18,114,39,.1,211,grass)
for x,w in [(0,10.75),(214,9.3)]:
 for _,z in data['streets']:
  for dz in [-7.2,7.2]:
   for k in range(math.ceil(2*w/1.25)):box(x-w+.7+k*1.25,.024,z+dz,.57,.014,2.7,white)
  for side in [-1,1]:
   if x==214 and side>0 and z in [73.3,150.1]:continue
   for k in range(8):box(x+side*(w+2),.024,z-4.1+k*1.18,2.75,.014,.53,white)
def instances(name,placements):
 objects=load(ASSETS/'neighborhood'/name)
 originals=[]
 for o in objects:
  if o.type=='MESH':originals.append((o.data,o.matrix_world.copy()))
 for o in objects:bpy.data.objects.remove(o,do_unlink=True)
 from mathutils import Matrix
 for p in placements:
  if p['x']<95 or p['z']>170:continue
  transform=Matrix.Translation((p['x'],-p['z'],0))@Matrix.Rotation(p.get('angle',0),4,'Z')@Matrix.Scale(p.get('scale',1),4)
  for mesh,matrix in originals:
   o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.matrix_world=transform@matrix
instances('street-tree.glb',data['trees']);instances('parked-car.glb',[p for p in data['parked'] if not p.get('core')]);instances('park-bench.glb',data['benches']);instances('street-furniture.glb',data['furniture'])
world=bpy.data.worlds.new('Warm daylight');world.use_nodes=True;bpy.context.scene.world=world;nodes=world.node_tree.nodes;nodes.clear();sky=nodes.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(29);sky.sun_rotation=math.radians(143);sky.sun_disc=False;bg=nodes.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.32;out=nodes.new('ShaderNodeOutputWorld');world.node_tree.links.new(sky.outputs['Color'],bg.inputs['Color']);world.node_tree.links.new(bg.outputs[0],out.inputs['Surface'])
light=bpy.data.lights.new('Afternoon sun','SUN');light.energy=2.3;light.angle=.08;light.color=(1,.80,.58);ob=bpy.data.objects.new('Afternoon sun',light);bpy.context.collection.objects.link(ob);ob.rotation_euler=Vector((-.32,.81,-.48)).to_track_quat('-Z','Y').to_euler()
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.cycles.max_bounces=4;scene.view_settings.view_transform='AgX';scene.render.resolution_x=1400;scene.render.resolution_y=900;scene.render.resolution_percentage=100
cd=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',cd);bpy.context.collection.objects.link(cam);scene.camera=cam;cd.lens=24
for name,pos,target in [('avenue-a-and-tenth',(223,1.72,-5),(191,13,16)),('avenue-a-storefronts',(215,1.72,197),(193,5.5,175)),('joyce-center',(217,1.72,16),(184,11,-24))]:
 cam.location=(pos[0],-pos[2],pos[1]);look=Vector((target[0],-target[2],target[1]));cam.rotation_euler=(look-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
print('RENDER_COMPLETE',str(OUT),flush=True)
