"""Detailed, streamed neighborhood meshes sharing the First & 10th component kit.

Run: blender -b -t 6 --python-exit-code 1 --python model-source/build_neighborhood.py
Optional arguments after --: --tile block-1-1 (rebuild a single block).
Architectural observations are separate editable records; unobserved elevations
use explicitly estimated component layouts, never an invented tenant identity.
"""
import bpy, json, math, random, sys, argparse, struct, hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import tessellate_polygon

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'dist/reconstruction/neighborhood.json').read_text())
OUT=ROOT/'dist/reconstruction/neighborhood'
OUT.mkdir(exist_ok=True)
# Import definitions only, without running or replacing the original corner model.
KIT=ROOT/'model-source/build_intersection.py'
ns={'__file__':str(KIT),'__name__':'neighborhood_component_kit'}
exec(compile(KIT.read_text().split("print('Building individual facades'")[0],str(KIT),'exec'),ns)
for name in ['Facade','face','box','rod','cornice','escape','storefront','label','roof_details','car','flush','material']:
    globals()[name]=ns[name]
MATS=ns['MATS']
# Preserve brick/stone surface maps; painted masonry uses a solid paint coat
# over brick roughness/normal maps so grey facades do not turn exposed brown.
# Tint factors below are explicitly applied to glTF; source photographs are not
# synthesized or repurposed as facade textures.
WALL_MATERIALS = {
    'warm brick': ('red_brick_03', (.90,.88,.83)),
    'salmon brick': ('red_brick_03', (1.0,.94,.89)),
    'weathered red': ('red_brick_03', (.67,.60,.53)),
    'buff brick': ('white_bricks', (.74,.62,.43)),
    'charcoal brick': ('white_bricks', (.16,.18,.17)),
    'painted ivory': ('white_bricks', (.63,.61,.53)),
    'painted grey': ('white_bricks', (.36,.37,.34)),
    'painted blue': ('white_bricks', (.065,.22,.34)),
    'painted ochre': ('white_bricks', (.64,.40,.045)),
    'aged brownstone': ('concrete_wall_006', (.53,.32,.20)),
    'limestone facade': ('concrete_wall_006', (.85,.80,.67)),
}
for name,(surface,tint) in WALL_MATERIALS.items():
    material(name,tint,.86,texture=surface+'_diff_1k.jpg',normal=surface+'_nor_gl_1k.jpg')
    if name.startswith('painted '):
        m=MATS[name];bs=m.node_tree.nodes.get('Principled BSDF')
        for link in list(bs.inputs['Base Color'].links):m.node_tree.links.remove(link)

material('red terra cotta',(.29,.105,.050),.8)
material('cast iron facade',(.08,.095,.091),.50,.40)

def owner(text):ns['OWNER']=text
def clear_meshes():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    ns['BATCHES'].clear();ns['TEXT'].clear()
    for collection in [bpy.data.meshes,bpy.data.curves]:
        for item in list(collection):
            if item.users==0:collection.remove(item)

# Install the higher-detail components without editing the accepted core kit.
exec(compile((ROOT/'model-source/neighborhood_detail_kit.py').read_text(),str(ROOT/'model-source/neighborhood_detail_kit.py'),'exec'),globals())

def render_building(b):
    spec=b.get('facadeSpec',{});photo=bool(spec.get('observed'))
    wall=spec.get('wall','warm brick');trim=spec.get('trim','cream stone')
    h=spec.get('height',b['height']);floors=spec.get('floors',b['floors'])
    b['renderHeight']=h
    title=b['address'] or ('Building '+str(b['id']))
    owner(title+' · '+('reference observed' if photo else 'mapped shape; facade details estimated'))
    if build_landmark(b,spec):
        for v in b['frontages']:
            f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length'])
            detail_frontage(f,spec,b['renderHeight'],True)
        return
    wall_mass(b,wall)
    fs=sorted(b['frontages'],key=lambda f:f['length'],reverse=True)
    for fi,v in enumerate(fs):
        f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length'])
        primary=spec.get('frontStreet',b['address'].split(' ',1)[-1])
        named_primary=(primary.lower().replace('1st','first').replace('2nd','second') in v['street'].lower())
        is_primary=fi==0 if not any(primary.lower().replace('1st','first').replace('2nd','second') in g['street'].lower() for g in fs) else named_primary
        f.detail=spec.get('detail',{}) if is_primary else {}
        f.wall=wall
        columns=spec.get('bays') if is_primary else None
        if not isinstance(columns,int):columns=max(2,round(f.L/2.65))
        if spec.get('sparseSide') and not is_primary:columns=max(2,round(f.L/7.8))
        columns=max(1,min(40,columns));pitch=f.L/columns
        style=spec.get('ornament',1 if h<26 else 0)
        if spec.get('cornicePlain'):f.strip(h,.20,.20,wall)
        else:cornice(f,h,spec.get('cornice','cornice copper brown'),style>0)
        basement=bool(spec.get('basement')) and is_primary
        ground_top=4.35 if basement else 3.62
        if floors>1:
            spacing=(h-ground_top-.23)/(floors-1)
            for row in range(floors-1):
                y=ground_top+row*spacing
                row_spec=(spec.get('windowRows',[])[row] if is_primary and row<len(spec.get('windowRows',[])) else {})
                row_columns=row_spec.get('bays',columns)
                row_pitch=f.L/row_columns
                round_rows=[r if r>=0 else floors-1+r for r in f.detail.get('roundWindowRows',[])]
                f.window_shape=row_spec.get('shape','round' if row in round_rows else spec.get('windowShape','rectangle') if is_primary else 'rectangle')
                crowns=f.detail.get('archedWindowRows',[])
                f.arched_crown=(row in [(r if r>=0 else floors-1+r) for r in crowns])
                for col in range(row_columns):
                    ss=spec['bayPositions'][col]*f.L if is_primary and len(spec.get('bayPositions',[]))==row_columns else (col+.5)*row_pitch
                    ratio=row_spec.get('windowRatio',spec.get('windowRatio'))
                    ww=row_pitch*ratio if ratio else min(1.18,row_pitch*.49)
                    wh=min(2.20,spacing*.69)*row_spec.get('heightRatio',1)
                    window_style=style if 'hoodedWindowRows' not in f.detail or row in f.detail['hoodedWindowRows'] else 0
                    street_window(f,ss,y,ww,wh,trim,window_style,ac=(row*3+col)%13==0)
                    if ww>1.7:
                        for part in range(1,max(2,round(ww/.7))):f.b(ss-ww/2+part*ww/max(2,round(ww/.7)),y+min(2.13,spacing*.68)/2,.16,.055,min(2.13,spacing*.68),.06,'window frame')
                    if spec.get('balconies') and is_primary and col==columns-1 and row>0:
                        f.b(ss,y-.15,.64,2.3,.15,1.3,'brownstone')
                        for j in range(10):f.line((ss-1.08+j*.24,y-.04,1.18),(ss-1.08+j*.24,y+.99,1.18),.015,'metal')
                        f.line((ss-1.15,y+1,1.18),(ss+1.15,y+1,1.18),.026,'metal')
                if spec.get('bands'):f.strip(y-.30,.085,.105,trim)
            # Observed escape layouts are retained; inferred layouts stay flagged in the manifest.
            if spec.get('escape') and (is_primary or spec.get('sideEscape')):
                levels=[ground_top-.20+row*spacing for row in range(floors-1)]
                positions=spec.get('escapeCenters',[.50]) if is_primary else [.50]
                for center in positions:escape(f,f.L*center,levels,min(3.05,f.L*.60),spec.get('escapeMat','black iron'))
        render_ground(b,f,v,spec,is_primary,columns,wall,trim)
        if f.L>4:
            f.b(f.L-.23,2.12,.13,.18,.36,.15,'black iron')
            f.b(f.L-.23,2.17,.22,.10,.15,.03,'opal lamp')
        detail_frontage(f,spec,h,is_primary)
    if b['frontages']:
        roof_details(b,h)
    if spec.get('roofSetback'):
        r=spec['roofSetback'];x0,z0,x1,z1=b['box'];i=r['inset']
        box((x0+x1)/2,h+r['height']/2,(z0+z1)/2,max(1,x1-x0-2*i),r['height'],max(1,z1-z0-2*i),wall)

exec(compile((ROOT/'model-source/neighborhood_landmarks.py').read_text(),str(ROOT/'model-source/neighborhood_landmarks.py'),'exec'),globals())

def export_tile(tile):
    clear_meshes()
    for b in DATA['buildings']:
        if b['tile']==tile['id'] and not b['core']:
            begin_building_detail(b)
            render_building(b)
            finish_building_detail()
    # Merge per material inside each tile. Address identity remains in the manifest;
    # hundreds of tiny building draw calls would make the browser needlessly slow.
    merged={}
    for (own,mat),q in ns['BATCHES'].items():
        key=(tile['id']+' · building references in neighborhood.json',mat)
        dest=merged.setdefault(key,{'v':[],'f':[],'uv':[]});offset=len(dest['v'])
        dest['v'].extend(q['v']);dest['uv'].extend(q['uv']);dest['f'].extend(tuple(i+offset for i in f) for f in q['f'])
    ns['BATCHES'].clear();ns['BATCHES'].update(merged)
    flush()
    # Include the address/sign glyphs in the material batches as well.
    for obj in list(bpy.context.scene.objects):
        if obj.type=='FONT':
            bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
            bpy.ops.object.convert(target='MESH')
    material_objects={}
    for obj in bpy.context.scene.objects:
        if obj.type=='MESH':material_objects.setdefault(obj.data.materials[0].name,[]).append(obj)
    for objects in material_objects.values():
        if len(objects)<2:continue
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:obj.select_set(True)
        bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join()
    bpy.ops.object.select_all(action='SELECT')
    target=OUT/(tile['id']+'.glb')
    bpy.ops.export_scene.gltf(filepath=str(target),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_extras=True,export_cameras=False,export_lights=False,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16,export_draco_normal_quantization=9,export_draco_texcoord_quantization=13)
    share_textures(target)
    tile['bytes']=target.stat().st_size
    tile['detailRevision']='04'
    tile['detailBuildings']=sum(b['tile']==tile['id'] and not b['core'] for b in DATA['buildings'])
    tile['triangles']=sum(sum(len(f)-2 for f in q['f']) for q in ns['BATCHES'].values())
    print('TILE_DONE',tile['id'],tile['bytes'],tile['triangles'],flush=True)

def share_textures(path):
    """Keep one content-addressed texture copy instead of embedding it in every tile."""
    raw=path.read_bytes();jl=struct.unpack_from('<I',raw,12)[0];doc=json.loads(raw[20:20+jl]);binary=raw[28+jl:]
    views=doc.get('bufferViews',[]);image_views=set();textures=OUT/'textures';textures.mkdir(exist_ok=True)
    for img in doc.get('images',[]):
        if 'bufferView' not in img:continue
        index=img.pop('bufferView');image_views.add(index);v=views[index];chunk=binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']]
        suffix='.jpg' if img.get('mimeType')=='image/jpeg' else '.png';name=hashlib.sha256(chunk).hexdigest()[:20]+suffix
        target=textures/name
        if not target.exists():target.write_bytes(chunk)
        img['uri']='textures/'+name
    new_views=[];packed=bytearray();remap={}
    for index,v in enumerate(views):
        if index in image_views:continue
        while len(packed)%4:packed.append(0)
        nv=dict(v);nv['byteOffset']=len(packed);nv['buffer']=0
        packed.extend(binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']]);remap[index]=len(new_views);new_views.append(nv)
    def replace(obj):
        if isinstance(obj,dict):
            for k,v in obj.items():
                if k=='bufferView':obj[k]=remap[v]
                else:replace(v)
        elif isinstance(obj,list):
            for item in obj:replace(item)
    replace(doc);doc['bufferViews']=new_views
    for m in doc.get('materials',[]):
        name=m.get('name');pbr=m.setdefault('pbrMetallicRoughness',{})
        if name in WALL_MATERIALS:
            pbr['baseColorFactor']=[*WALL_MATERIALS[name][1],1]
    doc['buffers']=[{'byteLength':len(packed)}]
    js=json.dumps(doc,separators=(',',':')).encode();js+=b' '*((-len(js))%4);packed.extend(b'\0'*((-len(packed))%4))
    result=struct.pack('<III',0x46546c67,2,28+len(js)+len(packed))+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(packed),0x004e4942)+packed
    path.write_bytes(result)

parser=argparse.ArgumentParser();parser.add_argument('--tile',action='append',choices=[t['id'] for t in DATA['tiles']])
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
for tile in DATA['tiles']:
    if not args.tile or tile['id'] in args.tile:export_tile(tile)
(ROOT/'dist/reconstruction/neighborhood.json').write_text(json.dumps(DATA,separators=(',',':')))
print('NEIGHBORHOOD_COMPLETE',len(DATA['buildings']),flush=True)
