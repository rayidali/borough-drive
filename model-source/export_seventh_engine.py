"""Export a bounded Godot slice from the existing, evidence-linked recipes.

blender -b -t 4 --python-exit-code 1 --python model-source/export_seventh_engine.py
Does not compile data, overwrite the browser, or alter source observations.
Geometry is retained; flat vertex colors are a separate authored lofi treatment.
"""
import bpy
import json
import hashlib
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'engine/first-seventh/assets/neighborhood'
OUT.mkdir(parents=True, exist_ok=True)
source = ROOT / 'model-source/build_neighborhood.py'
kit = {'__file__': str(source), '__name__': 'seventh_engine_export'}
exec(compile(source.read_text().split('parser=argparse.ArgumentParser()')[0], str(source), 'exec'), kit)
data = kit['DATA']
# A complete First/Second/Seventh/St Marks circuit plus the facing street walls.
bounds = [-268, 121, 77, 283]
selected = [b for b in data['buildings'] if not b['core'] and
            bounds[0] <= (b['box'][0]+b['box'][2])/2 <= bounds[2] and
            bounds[1] <= (b['box'][1]+b['box'][3])/2 <= bounds[3]]
records = []

def plain_material(name, alpha=1.0, emission=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bs = m.node_tree.nodes.get('Principled BSDF')
    color = m.node_tree.nodes.new('ShaderNodeVertexColor')
    color.layer_name = 'Color'
    m.node_tree.links.new(color.outputs['Color'], bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value = .82
    if emission:
        m.node_tree.links.new(color.outputs['Color'], bs.inputs['Emission Color'])
        bs.inputs['Emission Strength'].default_value = .8
    if alpha < 1:
        bs.inputs['Alpha'].default_value = alpha
        m.surface_render_method = 'DITHERED'
    return m

materials = {'paint': plain_material('Lofi / painted surfaces'),
             'glass': plain_material('Lofi / glass', .30),
             'light': plain_material('Lofi / illuminated details', emission=True)}

for index, building in enumerate(selected):
    kit['clear_meshes']()
    kit['begin_building_detail'](building)
    kit['render_building'](building)
    kit['finish_building_detail']()
    kit['flush']()
    center = Vector(((building['box'][0]+building['box'][2])/2,
                     -(building['box'][1]+building['box'][3])/2, 0))
    groups = {}
    for obj in list(bpy.context.scene.objects):
        if obj.type not in ('FONT', 'MESH'): continue
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        if obj.type == 'FONT': bpy.ops.object.convert(target='MESH')
        if not obj.data.materials: continue
        mat = obj.data.materials[0]
        bs = mat.node_tree.nodes.get('Principled BSDF') if mat.use_nodes else None
        rgb = list(bs.inputs['Base Color'].default_value[:3] if bs else mat.diffuse_color[:3])
        name = mat.name.lower()
        # Representative original paint/brick colors, deliberately not a new scan.
        if name in kit['WALL_MATERIALS']:
            rgb = list(kit['WALL_MATERIALS'][name][1])
            if not name.startswith('painted'):
                base = (.48,.24,.17) if 'brick' in name and 'buff' not in name else (.72,.61,.43)
                rgb = [rgb[i]*base[i] for i in range(3)]
        alpha = bs.inputs['Alpha'].default_value if bs else 1.0
        transmission = bs.inputs['Transmission Weight'].default_value if bs else 0
        emissive = bs and bs.inputs['Emission Strength'].default_value > 0
        kind = 'glass' if transmission > .1 or alpha < .9 or name in ('glass','shop glass') else 'light' if emissive else 'paint'
        mesh = obj.data
        colors = mesh.color_attributes.get('Color')
        if colors is None:
            colors = mesh.color_attributes.new(name='Color', type='FLOAT_COLOR', domain='CORNER')
            colors.data.foreach_set('color', [*rgb,1.0]*len(mesh.loops))
        mesh.materials.clear()
        mesh.materials.append(materials[kind])
        for polygon in mesh.polygons: polygon.material_index = 0
        obj.location -= center
        groups.setdefault(kind, []).append(obj)
    triangles = 0
    for kind, objects in groups.items():
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects: obj.select_set(True)
        bpy.context.view_layer.objects.active = objects[0]
        if len(objects) > 1: bpy.ops.object.join()
        obj = bpy.context.view_layer.objects.active
        obj.name = kind
        obj.data.calc_loop_triangles()
        triangles += len(obj.data.loop_triangles)
    bpy.ops.object.select_all(action='SELECT')
    target = OUT / f"building-{building['id']}.glb"
    bpy.ops.export_scene.gltf(filepath=str(target), export_format='GLB',
        use_selection=True, export_apply=True, export_yup=True,
        export_extras=False, export_cameras=False, export_lights=False,
        export_draco_mesh_compression_enable=False, export_texcoords=False,
        export_normals=True, export_attributes=False)
    records.append({'id':building['id'], 'address':building['address'],
        'asset':f'res://assets/neighborhood/{target.name}',
        'position':[center.x, 0, -center.y-228],
        'footprint':[[p[0],p[1]-228] for p in building['p']],
        'height':building.get('renderHeight',building['height']),
        'box':[building['box'][0],building['box'][1]-228,building['box'][2],building['box'][3]-228],
        'triangles':triangles, 'bytes':target.stat().st_size,
        'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    print('ENGINE_BUILDING',index+1,len(selected),building['id'],triangles,flush=True)

manifest = {'schema':1, 'sourceCommit':'c76dccebc143960498d21eeab8c55c2d0dbcc5ce',
    'sourceSha256':hashlib.sha256((ROOT/'dist/reconstruction/neighborhood.json').read_bytes()).hexdigest(),
    'originShift':[0,0,228], 'bounds':[-268,-107,77,55], 'buildings':records,
    'roads':[{'name':r['name'],'a':[r['a'][0],r['a'][1]-228],
              'b':[r['b'][0],r['b'][1]-228], 'halfWidth':r['halfWidth'],
              'oneway':r['oneway']} for r in data['roads']
             if r['name'] in ['First Avenue','Second Avenue','East 7th Street','St. Marks Place']],
    'notes':'Existing geometry; authored vertex-color lofi materials. Source imagery, measurements and hidden-surface limitations remain in the parent source records. No new photographic observations.'}
(OUT.parent/'slice.json').write_text(json.dumps(manifest,separators=(',',':'))+'\n')
print('ENGINE_EXPORT_COMPLETE',len(records),sum(r['triangles'] for r in records),flush=True)
