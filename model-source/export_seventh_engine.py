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
first_stmarks = json.loads((ROOT/'model-source/storefront-details.json').read_text()).get('firstStmarksEngine', {})
p01 = json.loads((ROOT/'model-source/east-village-p01/schedule.json').read_text())
p01_ids = {241822278,241822337,241822304,241822211}
assert {r['buildingId'] for r in p01['elevations']} == p01_ids
assert {r['faceId'] for r in p01['elevations']} == {str(i)+':0' for i in p01_ids}
p02 = json.loads((ROOT/'model-source/east-village-p02/schedule.json').read_text())
p02_ids = {248142657,248142658,248142659,248142660,248142713}
assert {r['buildingId'] for r in p02['elevations']} == p02_ids
assert {r['faceId'] for r in p02['elevations']} == {str(i)+':0' for i in p02_ids}
p03 = json.loads((ROOT/'model-source/east-village-p03/schedule.json').read_text())
p03_ids = {241822237}
assert {r['buildingId'] for r in p03['elevations']} == p03_ids
assert {r['faceId'] for r in p03['elevations']} == {'241822237:0','241822237:1'}
n01a = json.loads((ROOT/'model-source/east-village-e09-n01a/schedule.json').read_text())
n01a_ids = {247852691,247852690,247852697,247852689}
assert {r['buildingId'] for r in n01a['elevations']} == n01a_ids
assert {r['faceId'] for r in n01a['elevations']} == {'247852691:1','247852690:0','247852697:0','247852689:0'}
n01b = json.loads((ROOT/'model-source/east-village-e09-n01b/schedule.json').read_text())
n01b_ids = {247852687,247852686,247852685,247852684}
assert {r['buildingId'] for r in n01b['elevations']} == n01b_ids
assert {r['faceId'] for r in n01b['elevations']} == {str(i)+':0' for i in n01b_ids}
e09block = json.loads((ROOT/'model-source/east-village-e09-block/schedule.json').read_text())
e09block_ids = {r['buildingId'] for r in e09block['elevations']}
assert len(e09block_ids)==34
assert not e09block_ids & {r['id'] for r in json.loads((ROOT/'model-source/east-village-e09-block/protected-models.json').read_text())['models']}
e09east = json.loads((ROOT/'model-source/east-village-e09-east/schedule.json').read_text())
e09east_ids = {r['buildingId'] for r in e09east['elevations']}
assert len(e09east_ids)==41 and len(e09east['elevations'])==50
assert e09east_ids & {r['id'] for r in json.loads((ROOT/'model-source/east-village-e09-east/protected-models.json').read_text())['models']} == {248142713}
e10block = json.loads((ROOT/'model-source/east-village-e10-block/schedule.json').read_text())
e10block_ids = {r['buildingId'] for r in e10block['elevations']}
assert len(e10block_ids)==27 and len(e10block['elevations'])==29
assert not e10block_ids & {r['id'] for r in json.loads((ROOT/'model-source/east-village-e10-block/protected-models.json').read_text())['models']}
e10east = json.loads((ROOT/'model-source/east-village-e10-east/schedule.json').read_text())
e10east_ids = {r['buildingId'] for r in e10east['elevations']}
assert len(e10east_ids)==30 and len(e10east['elevations'])==36
assert not e10east_ids & {r['id'] for r in json.loads((ROOT/'model-source/east-village-e10-east/protected-models.json').read_text())['models']}
e11block=json.loads((ROOT/'model-source/east-village-e11-block/schedule.json').read_text())
e11block_ids={r['buildingId'] for r in e11block['elevations']}
assert len(e11block_ids)==22 and len(e11block['elevations'])==26
assert not e11block_ids & {r['id'] for r in json.loads((ROOT/'model-source/east-village-e11-block/protected-models.json').read_text())['models']}
def canonical_digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
recipe_files=['model-source/export_seventh_engine.py','model-source/seventh_street_kit.py','model-source/seventh_fidelity_kit.py',
    'model-source/build_neighborhood.py','model-source/build_intersection.py',
    'model-source/neighborhood_detail_kit.py','model-source/storefront_detail_kit.py',
    'model-source/neighborhood_landmarks.py','model-source/first_seventh_kit.py',
    'model-source/first_seventh_refinement.py','model-source/first_stmarks_kit.py',
    'model-source/author_first_stmarks_08.py','model-source/author_stmarks_08.py',
    'model-source/storefront_individual_kit.py','model-source/author_storefront_09.py',
    'model-source/storefront-observations-09.json']
recipe_files += sorted(str(p.relative_to(ROOT)) for p in (ROOT/'model-source/fonts/storefront-09').glob('*') if p.is_file())
recipe_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in recipe_files}
# This extension dispatches only the four explicit IDs / detailP01 records.
# Its hashes invalidate those four models; shared-recipe changes still require
# a full export. Both sets are verified before every browser export.
p01_recipe_files=['model-source/author_p01.py','model-source/p01_kit.py',
    'model-source/east-village-p01/schedule.json','model-source/east-village-p01/observations.json']
p01_recipe_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in p01_recipe_files}
p02_recipe_files=['model-source/author_p02.py','model-source/p02_kit.py','model-source/east-village-p02/schedule.json','model-source/east-village-p02/observations.json']
p02_recipe_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in p02_recipe_files}
p03_recipe_files=['model-source/author_p03.py','model-source/p03_kit.py','model-source/east-village-p03/schedule.json','model-source/east-village-p03/observations.json']
p03_recipe_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in p03_recipe_files}
n01a_recipe_files=['model-source/author_e09_n01a.py','model-source/e09_n01a_kit.py','model-source/east-village-e09-n01a/schedule.json','model-source/east-village-e09-n01a/observations.json']
n01a_recipe_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in n01a_recipe_files}
n01b_recipe_files=['model-source/author_e09_n01b.py','model-source/e09_n01b_kit.py','model-source/east-village-e09-n01b/schedule.json','model-source/east-village-e09-n01b/observations.json']
n01b_recipe_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in n01b_recipe_files}
e09block_recipe_files=['model-source/author_e09_block.py','model-source/e09_block_kit.py','model-source/east-village-e09-block/schedule.json','model-source/east-village-e09-block/observations.json']
e09block_recipe_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in e09block_recipe_files}
e09east_recipe_files=['model-source/author_e09_east.py','model-source/e09_east_kit.py','model-source/east-village-e09-east/schedule.json','model-source/east-village-e09-east/observations.json']
e09east_recipe_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in e09east_recipe_files}
e10block_recipe_files=['model-source/author_e10_block.py','model-source/e10_block_kit.py','model-source/east-village-e10-block/schedule.json','model-source/east-village-e10-block/observations.json','model-source/fonts/tenth/NotoSansJP.ttf','model-source/fonts/tenth/OFL.txt']
e10block_recipe_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in e10block_recipe_files}
e10east_recipe_files=['model-source/author_e10_east.py','model-source/e10_east_kit.py','model-source/east-village-e10-east/schedule.json','model-source/east-village-e10-east/observations.json']
e10east_recipe_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in e10east_recipe_files}
e11block_recipe_files=['model-source/author_e11_block.py','model-source/e11_block_kit.py','model-source/east-village-e11-block/schedule.json','model-source/east-village-e11-block/observations.json']
e11block_recipe_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in e11block_recipe_files}
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
first_stmarks_source=ROOT/'model-source/first_stmarks_kit.py'
exec(compile(first_stmarks_source.read_text(),str(first_stmarks_source),'exec'),kit)
kit['apply_first_stmarks_schedule'](data,first_stmarks)
individual_source=ROOT/'model-source/storefront_individual_kit.py'
exec(compile(individual_source.read_text(),str(individual_source),'exec'),kit)
p01_source=ROOT/'model-source/p01_kit.py'
exec(compile(p01_source.read_text(),str(p01_source),'exec'),kit)
kit['apply_first_stmarks_schedule'](data,p01)
p02_source=ROOT/'model-source/p02_kit.py'
exec(compile(p02_source.read_text(),str(p02_source),'exec'),kit)
kit['apply_first_stmarks_schedule'](data,p02)
p03_source=ROOT/'model-source/p03_kit.py'
exec(compile(p03_source.read_text(),str(p03_source),'exec'),kit)
kit['apply_first_stmarks_schedule'](data,p03)
n01a_source=ROOT/'model-source/e09_n01a_kit.py'
exec(compile(n01a_source.read_text(),str(n01a_source),'exec'),kit)
kit['apply_first_stmarks_schedule'](data,n01a)
n01b_source=ROOT/'model-source/e09_n01b_kit.py'
exec(compile(n01b_source.read_text(),str(n01b_source),'exec'),kit)
kit['apply_first_stmarks_schedule'](data,n01b)
e09block_source=ROOT/'model-source/e09_block_kit.py'
exec(compile(e09block_source.read_text(),str(e09block_source),'exec'),kit)
kit['apply_first_stmarks_schedule'](data,e09block)
e09east_source=ROOT/'model-source/e09_east_kit.py'
exec(compile(e09east_source.read_text(),str(e09east_source),'exec'),kit)
kit['apply_first_stmarks_schedule'](data,e09east)
e10block_source=ROOT/'model-source/e10_block_kit.py'
exec(compile(e10block_source.read_text(),str(e10block_source),'exec'),kit)
kit['apply_first_stmarks_schedule'](data,e10block)
e10east_source=ROOT/'model-source/e10_east_kit.py'
exec(compile(e10east_source.read_text(),str(e10east_source),'exec'),kit)
kit['apply_first_stmarks_schedule'](data,e10east)
e11block_source=ROOT/'model-source/e11_block_kit.py'
exec(compile(e11block_source.read_text(),str(e11block_source),'exec'),kit)
kit['apply_first_stmarks_schedule'](data,e11block)
# A complete First/Second/Seventh/St Marks circuit plus the facing street walls.
bounds = [-268, 121, 77, 283]
confirmed_scope=json.loads((ROOT/'model-source/first-stmarks-scope-08.json').read_text())
street_ids={f['buildingId'] for f in confirmed_scope['frontages']+confirmed_scope['cornerReturns']}
selected = [b for b in data['buildings'] if not b['core'] and (
            (bounds[0] <= (b['box'][0]+b['box'][2])/2 <= bounds[2] and
             bounds[1] <= (b['box'][1]+b['box'][3])/2 <= bounds[3]) or
            any(f['street']=='East 7th Street' for f in b['frontages']) or b['id'] in street_ids or b['id'] in p01_ids or b['id'] in p02_ids or b['id'] in p03_ids or b['id'] in n01a_ids or b['id'] in n01b_ids or b['id'] in e09block_ids or b['id'] in e09east_ids or b['id'] in e10block_ids or b['id'] in e10east_ids or b['id'] in e11block_ids)]
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
             'light': plain_material('Lofi / illuminated details', emission=True),
             'shop09': plain_material('Storefront09 / authored surfaces'),
             'shopglass09': plain_material('Storefront09 / clear glass', .18)}

for index, building in enumerate(selected):
    applicable_recipes={**recipe_hashes,**(p01_recipe_hashes if building['id'] in p01_ids else {}),**(p02_recipe_hashes if building['id'] in p02_ids else {}),**(p03_recipe_hashes if building['id'] in p03_ids else {}),**(n01a_recipe_hashes if building['id'] in n01a_ids else {}),**(n01b_recipe_hashes if building['id'] in n01b_ids else {}),**(e09block_recipe_hashes if building['id'] in e09block_ids else {}),**(e09east_recipe_hashes if building['id'] in e09east_ids else {}),**(e10block_recipe_hashes if building['id'] in e10block_ids else {}),**(e10east_recipe_hashes if building['id'] in e10east_ids else {}),**(e11block_recipe_hashes if building['id'] in e11block_ids else {})}
    input_digest=canonical_digest({'recipes':applicable_recipes,'building':building})
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
        if mat.get('storefront09Surface') is not None:kind='shop09'
        elif mat.get('storefront09Glass'):kind='shopglass09'
        mesh = obj.data
        # Material class uses the otherwise unused vertex alpha byte. World-
        # aligned surface coordinates avoid UV/tangent arrays on millions of
        # small architectural vertices, materially reducing browser download.
        surface = float(mat.get('storefront09Surface',0))
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
        if kind not in ('glass','shopglass09'):
            values=[0.0]*(len(colors.data)*4)
            colors.data.foreach_get('color',values)
            for i in range(3,len(values),4): values[i]=surface/(16.0 if kind=='shop09' else 8.0)
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
            if 'painted' in material_name or 'illuminated' in material_name or 'authored surfaces' in material_name:
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

# A partial rebuild does not run the renderer that sets renderHeight for
# cached buildings. Their verified exported records retain the real height.
exported_heights = {record['id']:record['height'] for record in records}
manifest = {'schema':1, 'sourceCommit':'c76dccebc143960498d21eeab8c55c2d0dbcc5ce',
    'sourceSha256':hashlib.sha256((ROOT/'dist/reconstruction/neighborhood.json').read_bytes()).hexdigest(),
    'originShift':[0,0,228], 'bounds':[-306,-107,289,55], 'buildings':records,
    'seventhFrontages':[b['id'] for b in selected if any(f['street']=='East 7th Street' for f in b['frontages'])],
    'detailRevision':schedule.get('revision','04'),
    'detailScheduleSha256':canonical_digest(schedule),
    'firstStmarksScheduleSha256':canonical_digest(first_stmarks),
    'firstStmarksRevision':first_stmarks.get('revision'),
    'streetReviewFrontages':[{'faceId':r['faceId'],'id':r['buildingId'],
        'address':r['address'],'height':exported_heights[r['buildingId']],
        'frontage':r['sourceFace']} for r in first_stmarks.get('elevations',[])],
    'detailSourceSha256':hashlib.sha256((ROOT/'model-source/storefront-details.json').read_bytes()).hexdigest(),
    'recipeHashes':{**recipe_hashes,**p01_recipe_hashes,**p02_recipe_hashes,**p03_recipe_hashes,**n01a_recipe_hashes,**n01b_recipe_hashes,**e09block_recipe_hashes,**e09east_recipe_hashes,**e10block_recipe_hashes,**e10east_recipe_hashes,**e11block_recipe_hashes},
    'packetScope':{'id':'01-E11-21','buildingIds':sorted(e11block_ids),'faceIds':sorted(r['faceId'] for r in e11block['elevations']),
        'supportingRoad':{'street':'First Avenue connection and Eleventh Second–First; existing Ninth and Tenth retained','northTerminal':-315.3,'outerNorthLimit':-320.3,'eleventhCenter':-304.3,'eleventhWestTerminal':-213.0,'eleventhEastTerminal':13.0,'eleventhOuterWest':-217.0,'eleventhOuterEast':17.0,'tenthCenter':-228.0,'tenthWestTerminal':-213.0,'tenthEastTerminal':207.0,'tenthOuterWest':-217.0,'tenthOuterEast':211.0,
            'corridorHalfWidth':17.0,'ninthCenter':-154.7,'ninthWestTerminal':-213.0,'ninthOuterWest':-217.0,'ninthEastTerminal':207.0,'ninthOuterEast':211.0,
            'addressPolicy':'Seventh-only HUD; First reaches Eleventh. Eleventh reaches Second and ends at First; Ninth and Tenth retained, other avenue terminals unchanged.'}},
    'packetScopes':[{'id':packet['id'],'buildingIds':sorted({r['buildingId'] for r in packet['elevations']}),'faceIds':sorted(r['faceId'] for r in packet['elevations'])} for packet in [p01,p02,p03,n01a,n01b,e09block,e09east,e10block,e10east,e11block]],
    'packetReviewFrontages':[{'faceId':r['faceId'],'id':r['buildingId'],'address':r['address'],
        'height':exported_heights[r['buildingId']],'frontage':r.get('effectiveFace',r['sourceFace'])} for packet in [p01,p02,p03,n01a,n01b,e09block,e09east,e10block,e10east,e11block] for r in packet['elevations']],
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
    'reviewFrontages':[{'id':b['id'],'address':b['address'],'height':exported_heights[b['id']],
        'frontage':{**next(f for f in b['frontages'] if f['street']=='East 7th Street')}}
        for b in selected if any(f['street']=='East 7th Street' for f in b['frontages'])],
    'roads':[{'name':r['name'],'a':[r['a'][0],r['a'][1]-228],
              'b':[r['b'][0],r['b'][1]-228], 'halfWidth':r['halfWidth'],
              'oneway':r['oneway']} for r in data['roads']
             if r['name'] in ['First Avenue','Second Avenue','Avenue A','East 7th Street','St. Marks Place']],
    'notes':'Seventh Street from Second Avenue through Avenue A with existing boundary context and the prior return circuit. Dated observation schedules plus authored surface/street detail; not a measured survey. Shared Poly Haven CC0 generic material maps are not scans of these buildings. Original game export is preserved.'}
for record in first_stmarks.get('elevations',[])+n01a['elevations']+n01b['elevations']+e09block['elevations']+e09east['elevations']+e10block['elevations']+e10east['elevations']+e11block['elevations']:
    f=record['sourceFace']
    for well in record['architecture'].get('observedGround',{}).get('basementAreaways',[]):
        at=well.get('at',.5)
        manifest['groundVoids'].append({'buildingId':record['buildingId'],'faceId':record['faceId'],
            'address':record['address'],'worldWidth':well['width']*f['length'],'cutExtent':well['depth'],
            'depthBelow':well.get('depthBelow',.48),'frontage':f,
            'runtimeCenter':[f['x']+f['rx']*f['length']*at,f['z']+f['rz']*f['length']*at-228],
            'runtimeNormal':[-f['rz'],f['rx']],
            'basis':'Explicit dated frontage basement access; dimensions visually estimated.'})
manifest['notes']='Confirmed First Avenue Seventh–St. Marks and St. Marks Second–Avenue A, plus preserved Seventh and prior context. Dated observations and authored estimates; no measured survey or calibrated acceptance. Original game export preserved.'
manifest['notes']+=' P01 adds only 137–143 First Avenue west faces and a bounded First Avenue continuation; Ninth and other avenue ends remain closed.'
manifest['notes']+=' P02 adds five east-side First Avenue faces only; Ninth return is deferred, with its plain shared mass explicit.'
manifest['notes']+=' P03 adds only 145 First Avenue and its complete southwest Ninth return. The supporting Ninth stub ends at x=-40; no other Ninth facade is assigned.'
manifest['notes']+=' N01A supersedes the P03 road stub with access to four north Ninth faces, west terminal x=-69. Unassigned 147 First face and other Ninth faces remain deferred.'
manifest['notes']+=' N01B adds 339–333 Ninth; supporting west terminal x=-99, other street ends unchanged. 337 has explicit engine-only observed-height estimate; source data preserved.'
manifest['notes']+=' E09 complete-block addition owns 34 remaining Ninth faces; 221 prior models preserved. Ninth west terminal x=-213 at Second approach, with other avenue ends unchanged.'
manifest['auxiliaryFootprints']=[{**r,'box':[r['box'][0],r['box'][1]-228,r['box'][2],r['box'][3]-228]} for r in e09east['auxiliaryFootprints']]
manifest['notes']+=' E09 east block supersedes previous road limits: 50 faces across 41 owners, including 148 Ninth return with First face and shared mapped mass protected. Celeste retains its observed low infill/open terrace.'
manifest['notes']+=' Tenth Second–First adds 27 ordinary owners / 29 faces; separate immutable protected core adapter retains 23 original building owners.'
manifest['notes']+=' Tenth First–Avenue A adds 30 ordinary owners / 36 planes, with separate club and church roof profiles and no protected core changes.'
(OUT.parent/'slice.json').write_text(json.dumps(manifest,separators=(',',':'))+'\n')
print('ENGINE_EXPORT_COMPLETE',len(records),sum(r['triangles'] for r in records),flush=True)
