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
for name,color in [('warm brick',(.40,.18,.10)),('salmon brick',(.44,.24,.17)),('buff brick',(.48,.40,.27)),('charcoal brick',(.18,.17,.15)),('aged brownstone',(.31,.21,.15)),('limestone facade',(.57,.53,.44)),('painted ivory',(.63,.61,.53)),('painted grey',(.36,.37,.34)),('weathered red',(.33,.11,.07))]:
    material(name,color,.86,texture='red_brick_03_diff_1k.jpg' if 'brick' in name or name=='weathered red' else None,normal='red_brick_03_nor_gl_1k.jpg' if 'brick' in name else 'concrete_wall_006_nor_gl_1k.jpg')
    # A tint multiplies the shared brick texture; avoids reusing one identical red.
    if 'brick' in name or name=='weathered red':
        m=MATS[name];bs=m.node_tree.nodes.get('Principled BSDF');link=bs.inputs['Base Color'].links[0]
        mix=m.node_tree.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.72;mix.inputs[2].default_value=(*color,1)
        m.node_tree.links.new(link.from_socket,mix.inputs[1]);m.node_tree.links.new(mix.outputs[0],bs.inputs['Base Color'])
        # glTF exports the base-factor tint with the image; custom nodes are not baked.
        m.node_tree.links.new(link.from_socket,bs.inputs['Base Color']);bs.inputs['Base Color'].default_value=(*color,1)

material('red terra cotta',(.29,.105,.050),.8)
material('cast iron facade',(.08,.095,.091),.50,.40)

def owner(text):ns['OWNER']=text
def clear_meshes():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    ns['BATCHES'].clear();ns['TEXT'].clear()

def wall_mass(b,mat,open_ground=True):
    p=b['p'];h=b['renderHeight']
    area=sum(a[0]*c[1]-c[0]*a[1] for a,c in zip(p,p[1:]+p[:1]))
    if area>0:p=list(reversed(p))
    for a,c in zip(p,p[1:]+p[:1]):
        mid=[(a[0]+c[0])/2,(a[1]+c[1])/2]
        is_front=any(math.hypot(mid[0]-(f['x']+f['rx']*f['length']/2),mid[1]-(f['z']+f['rz']*f['length']/2))<.3 for f in b['frontages'])
        bottom=3.14 if is_front and open_ground and h>5 else .17
        face([(a[0],bottom,a[1]),(c[0],bottom,c[1]),(c[0],h,c[1]),(a[0],h,a[1])],mat)
        length=math.dist(a,c)
        box((a[0]+c[0])/2,h+.09,(a[1]+c[1])/2,length,.18,.16,mat,-math.atan2(c[1]-a[1],c[0]-a[0]))
    verts=[Vector((a[0],h,a[1])) for a in p]
    for tri in tessellate_polygon([verts]):face([verts[v] if isinstance(v,int) else v for v in tri],'roof')

def street_window(f,s,y,w,h,trim,style=0,ac=False):
    # Built reveals, sash, sill and lintel, with actual depth and varied blinds.
    f.b(s,y+h/2,.025,w+.14,h+.13,.13,trim)
    f.b(s,y+h/2,.101,w,h,.022,'window glass')
    for dx in [-w/2,w/2]:f.b(s+dx,y+h/2,.14,.052,h,.10,'window frame')
    for yy in [y+.02,y+h*.49,y+h-.02]:f.b(s,yy,.15,w,.046,.08,'window frame')
    f.b(s,y-.09,.20,w+.25,.12,.35,trim)
    f.b(s,y+h+.105,.15,w+.24,.19,.26,trim)
    pattern=int((s*9+y*3)%7)
    if pattern in [1,3]:
        for dx in [-w*.34,w*.34]:f.b(s+dx,y+h*.5,.125,w*.22,h*.9,.012,'curtain light' if pattern==1 else 'curtain amber')
    elif pattern in [2,5]:
        for j in range(7):f.b(s,y+h-.07-j*.068,.128,w-.1,.038,.012,'curtain')
    if style>=1:
        f.b(s,y+h+.26,.19,w+.38,.09,.39,trim)
        if style>=2:
            for dx in [-.46*w,0,.46*w]:f.b(s+dx,y+h+.29,.25,.15,.19,.17,trim)
    if ac:
        f.b(s,y+.15,.33,w*.67,.38,.51,'air conditioner')
        for j in range(6):f.b(s,y+.01+j*.055,.594,w*.57,.015,.015,'metal')

def doorway(f,s,number,stoop=False,trim='brownstone'):
    rise=.80 if stoop else 0
    f.b(s,1.41+rise,.12,1.19,2.49,.20,trim)
    f.b(s,1.37+rise,.24,.90,2.16,.04,'wood')
    f.b(s,1.70+rise,.27,.66,1.23,.02,'dark glass')
    for dx in [-.44,.44]:f.b(s+dx,1.34+rise,.29,.04,2.15,.08,'black iron')
    f.b(s,2.25+rise,.30,.90,.07,.07,'black iron')
    f.line((s+.3,1.02+rise,.33),(s+.3,1.5+rise,.33),.015,'brass')
    f.b(s+.74,1.43+rise,.23,.16,.31,.07,'metal')
    if number:label(f,s,2.69+rise,1.0,number,'cream stone',.17,.27)
    if stoop:
        for k in range(5):f.b(s,.17+.08*(k+1),1.05-k*.17,1.45,.16*(k+1),.34,trim)
        for dx in [-.72,.72]:
            for k in range(6):f.line((s+dx,.18+k*.13,1.50-k*.22),(s+dx,1.07+k*.13,1.50-k*.22),.018)
            f.line((s+dx,1.07,1.50),(s+dx,1.72,.40),.028)

def render_building(b):
    spec=b.get('facadeSpec',{});photo=bool(spec.get('observed'))
    wall=spec.get('wall','warm brick');trim=spec.get('trim','cream stone')
    h=spec.get('height',b['height']);floors=spec.get('floors',b['floors'])
    b['renderHeight']=h
    title=b['address'] or ('Building '+str(b['id']))
    owner(title+' · '+('reference observed' if photo else 'mapped shape; facade details estimated'))
    if build_landmark(b,spec):return
    wall_mass(b,wall)
    fs=sorted(b['frontages'],key=lambda f:f['length'],reverse=True)
    for fi,v in enumerate(fs):
        f=Facade(v['x'],v['z'],v['rx'],v['rz'],v['length'])
        primary=spec.get('frontStreet',b['address'].split(' ',1)[-1])
        named_primary=(primary.lower().replace('1st','first').replace('2nd','second') in v['street'].lower())
        is_primary=fi==0 if not any(primary.lower().replace('1st','first').replace('2nd','second') in g['street'].lower() for g in fs) else named_primary
        columns=spec.get('bays') if is_primary else None
        if not isinstance(columns,int):columns=max(2,round(f.L/2.65))
        if spec.get('sparseSide') and not is_primary:columns=max(2,round(f.L/7.8))
        columns=max(1,min(40,columns));pitch=f.L/columns
        style=spec.get('ornament',1 if h<26 else 0)
        if spec.get('cornicePlain'):f.strip(h,.20,.20,wall)
        else:cornice(f,h,spec.get('cornice','cornice copper brown'),style>0)
        if floors>1:
            spacing=(h-3.85)/(floors-1)
            for row in range(floors-1):
                y=3.62+row*spacing
                for col in range(columns):
                    ss=spec['bayPositions'][col]*f.L if is_primary and len(spec.get('bayPositions',[]))==columns else (col+.5)*pitch
                    ww=pitch*spec['windowRatio'] if spec.get('windowRatio') else min(1.12,pitch*.49)
                    street_window(f,ss,y,ww,min(2.13,spacing*.68),trim,style,ac=(row*3+col)%13==0)
                    if ww>1.7:
                        for part in range(1,max(2,round(ww/.7))):f.b(ss-ww/2+part*ww/max(2,round(ww/.7)),y+min(2.13,spacing*.68)/2,.16,.055,min(2.13,spacing*.68),.06,'window frame')
                    if spec.get('balconies') and is_primary and col==columns-1 and row>0:
                        f.b(ss,y-.15,.64,2.3,.15,1.3,'brownstone')
                        for j in range(10):f.line((ss-1.08+j*.24,y-.04,1.18),(ss-1.08+j*.24,y+.99,1.18),.015,'metal')
                        f.line((ss-1.15,y+1,1.18),(ss+1.15,y+1,1.18),.026,'metal')
                if spec.get('bands'):f.strip(y-.30,.085,.105,trim)
            # Only add fire escapes when observed; unsurveyed facades avoid inventing them.
            if spec.get('escape') and (is_primary or spec.get('sideEscape')):
                levels=[3.42+row*spacing for row in range(floors-1)]
                positions=spec.get('escapeCenters',[.50]) if is_primary else [.50]
                for center in positions:escape(f,f.L*center,levels,min(3.05,f.L*.60),spec.get('escapeMat','black iron'))
        num=b['address'].split(' ')[0] if b['address'] else ''
        shop=spec.get('business') if is_primary else None
        if shop:
            awning=spec.get('awning');fascia=spec.get('fascia','black iron')
            shop_end=f.L*spec.get('shopFraction',1)-.1
            storefront(f,.10,shop_end,shop,awning,fascia,spec.get('letters','sign white'),closed=spec.get('businessClosed',False),profile=spec.get('profile','cafe'))
            if spec.get('secondarySign'):label(f,(shop_end+.1)/2,2.48,shop_end-.2,spec['secondarySign'],'sign white' if fascia!='sign white' else 'black iron',.14,.46)
            if shop_end<f.L-.2:
                f.b((shop_end+f.L)/2,1.6,.03,f.L-shop_end,2.95,.10,wall);doorway(f,f.L-.8,num,False,trim)
        elif v['street'] in ['First Avenue','Second Avenue','Avenue A'] and b['buildingType'] not in ['church','school','civic']:
            # Unverified shop identity stays blank; small interior rooms are illustrative.
            units=max(1,round(f.L/6.8))
            for j in range(units):
                a=j*f.L/units+.10;end=(j+1)*f.L/units-.10
                storefront(f,a,end,'',None,wall,closed=False)
            doorway(f,f.L-.75,num,False,trim)
        else:
            f.strip(1.65,2.96,.06,wall)
            spacing=f.L/max(2,columns)
            for k in range(max(2,columns)):
                s=(k+.5)*spacing
                if abs(s-f.L*.23)>1:street_window(f,s,.88,min(1.12,spacing*.49),1.7,trim,0)
            doorway(f,max(.9,min(f.L-.9,f.L*.23)),num,spec.get('stoop',False),trim)
        if f.L>4:
            f.b(f.L-.23,2.12,.13,.18,.36,.15,'black iron')
            f.b(f.L-.23,2.17,.22,.10,.15,.03,'opal lamp')
    if b['frontages']:
        roof_details(b,h)

exec(compile((ROOT/'model-source/neighborhood_landmarks.py').read_text(),str(ROOT/'model-source/neighborhood_landmarks.py'),'exec'),globals())

def export_tile(tile):
    clear_meshes()
    for b in DATA['buildings']:
        if b['tile']==tile['id'] and not b['core']:render_building(b)
    # Merge per material inside each tile. Address identity remains in the manifest;
    # hundreds of tiny building draw calls would make the browser needlessly slow.
    merged={}
    for (own,mat),q in ns['BATCHES'].items():
        key=(tile['id']+' · building references in neighborhood.json',mat)
        dest=merged.setdefault(key,{'v':[],'f':[],'uv':[]});offset=len(dest['v'])
        dest['v'].extend(q['v']);dest['uv'].extend(q['uv']);dest['f'].extend(tuple(i+offset for i in f) for f in q['f'])
    ns['BATCHES'].clear();ns['BATCHES'].update(merged)
    flush()
    bpy.ops.object.select_all(action='SELECT')
    target=OUT/(tile['id']+'.glb')
    bpy.ops.export_scene.gltf(filepath=str(target),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_extras=True,export_cameras=False,export_lights=False,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16,export_draco_normal_quantization=9,export_draco_texcoord_quantization=13)
    share_textures(target)
    tile['bytes']=target.stat().st_size
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
        if name in ['buff brick','charcoal brick','painted ivory','painted grey','limestone facade','aged brownstone']:
            pbr.pop('baseColorTexture',None)
            pbr['baseColorFactor']=list(MATS[name].node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value)
        elif name in ['warm brick','salmon brick','weathered red']:
            pbr['baseColorFactor']={'warm brick':[.90,.88,.83,1],'salmon brick':[1,.92,.86,1],'weathered red':[.64,.52,.44,1]}[name]
    doc['buffers']=[{'byteLength':len(packed)}]
    js=json.dumps(doc,separators=(',',':')).encode();js+=b' '*((-len(js))%4);packed.extend(b'\0'*((-len(packed))%4))
    result=struct.pack('<III',0x46546c67,2,28+len(js)+len(packed))+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(packed),0x004e4942)+packed
    path.write_bytes(result)

parser=argparse.ArgumentParser();parser.add_argument('--tile')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
for tile in DATA['tiles']:
    if not args.tile or args.tile==tile['id']:export_tile(tile)
(ROOT/'dist/reconstruction/neighborhood.json').write_text(json.dumps(DATA,separators=(',',':')))
print('NEIGHBORHOOD_COMPLETE',len(DATA['buildings']),flush=True)
