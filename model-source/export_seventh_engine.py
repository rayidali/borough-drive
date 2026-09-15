"""Export a bounded Godot slice from the existing, evidence-linked recipes.

blender -b -t 4 --python-exit-code 1 --python model-source/export_seventh_engine.py
Does not compile data, overwrite the browser, or alter source observations.
Geometry is retained; flat vertex colors are a separate authored lofi treatment.
"""
import bpy
import json
import hashlib
import argparse
import sys
import shutil
import struct
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'engine/first-seventh/assets/neighborhood'
OUT.mkdir(parents=True, exist_ok=True)
source = ROOT / 'model-source/build_neighborhood.py'
kit = {'__file__': str(source), '__name__': 'seventh_engine_export'}
exec(compile(source.read_text().split('parser=argparse.ArgumentParser()')[0], str(source), 'exec'), kit)
data = kit['DATA']
parser = argparse.ArgumentParser()
parser.add_argument('--only', action='append', type=int, help='Rebuild only these building IDs; other cached exports must exist.')
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
# Engine-only schedules reuse the original observed components while leaving the
# accepted ten-block export and its source signatures byte-for-byte unchanged.
schedule = json.loads((ROOT/'model-source/storefront-details.json').read_text()).get('seventhEngine', {})
def canonical_digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
recipe_files=['model-source/export_seventh_engine.py','model-source/seventh_street_kit.py','model-source/seventh_fidelity_kit.py',
    'model-source/build_neighborhood.py','model-source/build_intersection.py',
    'model-source/neighborhood_detail_kit.py','model-source/storefront_detail_kit.py',
    'model-source/neighborhood_landmarks.py','model-source/first_seventh_kit.py',
    'model-source/first_seventh_refinement.py']
recipe_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in recipe_files}
detail_source = ROOT/'model-source/seventh_street_kit.py'
if detail_source.exists():
    exec(compile(detail_source.read_text(),str(detail_source),'exec'),kit)
    kit['apply_seventh_schedule'](data,schedule)
    fidelity_source=ROOT/'model-source/seventh_fidelity_kit.py'
    exec(compile(fidelity_source.read_text(),str(fidelity_source),'exec'),kit)
    by_id={b['id']:b for b in data['buildings']}
    for record in schedule.get('elevations',[]):
        if record.get('architecture'):
            building=by_id[record['buildingId']]
            building['seventhArchitecture']=record['architecture']
            if record['architecture'].get('wall'):
                building['facadeSpec']['elevations']['East 7th Street']['wall']=record['architecture']['wall']
# A complete First/Second/Seventh/St Marks circuit plus the facing street walls.
bounds = [-268, 121, 77, 283]
selected = [b for b in data['buildings'] if not b['core'] and (
            (bounds[0] <= (b['box'][0]+b['box'][2])/2 <= bounds[2] and
             bounds[1] <= (b['box'][1]+b['box'][3])/2 <= bounds[3]) or
            any(f['street']=='East 7th Street' for f in b['frontages']))]
records = []
old_manifest = json.loads((OUT.parent/'slice.json').read_text())
old_records = {b['id']:b for b in old_manifest['buildings']}
surfaces = OUT.parent/'surfaces'
surfaces.mkdir(exist_ok=True)
for surface in ['red_brick_03','white_bricks','concrete_wall_006']:
    for kind in ['diff','nor_gl']:
        filename = f'{surface}_{kind}_1k.jpg'
        shutil.copy2(ROOT/'dist/reconstruction/assets'/filename,surfaces/filename)

def plain_material(name, alpha=1.0, emission=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bs = m.node_tree.nodes.get('Principled BSDF')
    color = m.node_tree.nodes.new('ShaderNodeVertexColor')
    color.layer_name = 'Color'
    m.node_tree.links.new(color.outputs['Color'], bs.inputs['Base Color'])
    if alpha==1.0:
        # Blender otherwise exports RGB only, dropping our semantic alpha byte.
        # The Godot paint shader deliberately ignores opacity and reads the tag.
        m.node_tree.links.new(color.outputs['Alpha'],bs.inputs['Alpha'])
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
    input_digest=canonical_digest({'recipes':recipe_hashes,'building':building})
    if args.only and building['id'] not in args.only:
        previous = old_records.get(building['id'])
        if not previous or not (OUT/Path(previous['asset']).name).exists():
            raise ValueError('Missing previously exported building '+str(building['id']))
        if previous.get('inputSha256')!=input_digest:
            raise ValueError('Stale cached recipe for '+str(building['id'])+'; rebuild without --only.')
        records.append(previous)
        continue
    kit['clear_meshes']()
    kit['begin_building_detail'](building)
    kit['render_building'](building)
    if 'add_seventh_detail' in kit: kit['add_seventh_detail'](building,schedule)
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
        kind = 'glass' if transmission > .1 or alpha < .9 or name in ('glass','shop glass','store glass') else 'light' if emissive else 'paint'
        mesh = obj.data
        # Material class uses the otherwise unused vertex alpha byte. World-
        # aligned surface coordinates avoid UV/tangent arrays on millions of
        # small architectural vertices, materially reducing browser download.
        surface = 0.0
        if kind == 'paint':
            if name=='seventh reflective glass':
                surface = 6.0
            elif 'brick' in name or name.startswith('painted '):
                surface = 3.0 if name.startswith('painted ') else 2.0 if any(t in name for t in ['buff','white','pale','smoke']) else 1.0
            elif any(t in name for t in ['stone','limestone','terra cotta','concrete','stucco','plaster']):
                surface = 4.0
            elif name in ['wood','seventh canvas brown','seventh oak door','seventh oak recess','seventh oak edge']:
                surface = 5.0
        for layer in list(mesh.uv_layers): mesh.uv_layers.remove(layer)
        colors = mesh.color_attributes.get('Color')
        if colors is None:
            colors = mesh.color_attributes.new(name='Color', type='FLOAT_COLOR', domain='CORNER')
            colors.data.foreach_set('color', [*rgb,1.0]*len(mesh.loops))
        if kind!='glass':
            values=[0.0]*(len(colors.data)*4)
            colors.data.foreach_get('color',values)
            for i in range(3,len(values),4): values[i]=surface/8.0
            colors.data.foreach_set('color',values)
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
    raw=target.read_bytes()
    gltf=json.loads(raw[20:20+struct.unpack_from('<I',raw,12)[0]])
    for mesh in gltf['meshes']:
        for primitive in mesh['primitives']:
            material_name=gltf['materials'][primitive['material']]['name']
            if 'painted' in material_name or 'illuminated' in material_name:
                colors=gltf['accessors'][primitive['attributes']['COLOR_0']]
                if colors['type']!='VEC4':
                    raise ValueError('GLB dropped the surface semantic alpha channel: '+str(building['id']))
    records.append({'id':building['id'], 'address':building['address'],
        'asset':f'res://assets/neighborhood/{target.name}',
        'position':[center.x, 0, -center.y-228],
        'footprint':[[p[0],p[1]-228] for p in building['p']],
        'height':building.get('renderHeight',building['height']),
        'box':[building['box'][0],building['box'][1]-228,building['box'][2],building['box'][3]-228],
        'triangles':triangles, 'bytes':target.stat().st_size,
        'inputSha256':input_digest,
        'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    print('ENGINE_BUILDING',index+1,len(selected),building['id'],triangles,flush=True)

manifest = {'schema':1, 'sourceCommit':'c76dccebc143960498d21eeab8c55c2d0dbcc5ce',
    'sourceSha256':hashlib.sha256((ROOT/'dist/reconstruction/neighborhood.json').read_bytes()).hexdigest(),
    'originShift':[0,0,228], 'bounds':[-306,-107,289,55], 'buildings':records,
    'seventhFrontages':[b['id'] for b in selected if any(f['street']=='East 7th Street' for f in b['frontages'])],
    'detailRevision':'04',
    'detailScheduleSha256':canonical_digest(schedule),
    'detailSourceSha256':hashlib.sha256((ROOT/'model-source/storefront-details.json').read_bytes()).hexdigest(),
    'recipeHashes':recipe_hashes,
    # Export only the explicit areaways recorded in revision 04.  The runtime
    # can use these records to cut matching sidewalk/solid planes; no generic
    # basement openings are inferred from building type or address.
    'groundVoids':[
        {
            'buildingId':building_id,
            'address':by_id[int(building_id)]['address'],
            'at':well.get('at',.5),
            'width':well.get('width',.34),
            'worldWidth':well.get('width',.34)*next(f for f in by_id[int(building_id)]['frontages'] if f['street']=='East 7th Street')['length'],
            'depth':well.get('depth',.92),
            'cutExtent':well.get('depth',.92),
            'stepsTowardFacade':True,
            'depthBelow':well.get('depthBelow',.30),
            'runtimeCenter':[
                (lambda f:f['x']+f['rx']*f['length']*well.get('at',.5))(next(f for f in by_id[int(building_id)]['frontages'] if f['street']=='East 7th Street')),
                (lambda f:f['z']+f['rz']*f['length']*well.get('at',.5)-228)(next(f for f in by_id[int(building_id)]['frontages'] if f['street']=='East 7th Street'))
            ],
            'runtimeNormal':[
                (lambda f:-f['rz'])(next(f for f in by_id[int(building_id)]['frontages'] if f['street']=='East 7th Street')),
                (lambda f:f['rx'])(next(f for f in by_id[int(building_id)]['frontages'] if f['street']=='East 7th Street'))
            ],
            'frontage':{**next(f for f in by_id[int(building_id)]['frontages'] if f['street']=='East 7th Street')},
            'basis':'Explicit observedGroundCorrections basementAreaway; below-grade depth is an authored cut envelope pending measurement.'
        }
        for building_id,spec in schedule.get('observedGroundCorrections',{}).items()
        if int(building_id) in by_id
        for well in spec.get('basementAreaways',[])
        if well.get('depth',0)>0
    ],
    'reviewFrontages':[{'id':b['id'],'address':b['address'],'height':b['renderHeight'],
        'frontage':{**next(f for f in b['frontages'] if f['street']=='East 7th Street')}}
        for b in selected if any(f['street']=='East 7th Street' for f in b['frontages'])],
    'roads':[{'name':r['name'],'a':[r['a'][0],r['a'][1]-228],
              'b':[r['b'][0],r['b'][1]-228], 'halfWidth':r['halfWidth'],
              'oneway':r['oneway']} for r in data['roads']
             if r['name'] in ['First Avenue','Second Avenue','Avenue A','East 7th Street','St. Marks Place']],
    'notes':'Seventh Street from Second Avenue through Avenue A with existing boundary context and the prior return circuit. Dated observation schedules plus authored surface/street detail; not a measured survey. Shared Poly Haven CC0 generic material maps are not scans of these buildings. Original game export is preserved.'}
(OUT.parent/'slice.json').write_text(json.dumps(manifest,separators=(',',':'))+'\n')
print('ENGINE_EXPORT_COMPLETE',len(records),sum(r['triangles'] for r in records),flush=True)
