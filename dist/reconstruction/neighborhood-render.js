import * as THREE from 'three';
import {mergeGeometries} from 'three/addons/utils/BufferGeometryUtils.js';

const COLORS={'seventh red brick':0x875440,'seventh buff brick':0xb4a387,'seventh red plaster':0x973b28,'painted blue':0x2b6888,'painted ochre':0xc49a34,'warm brick':0x825944,'salmon brick':0x9c7162,'buff brick':0xb1a080,'charcoal brick':0x575653,'aged brownstone':0x796050,'limestone facade':0xb6af9c,'painted ivory':0xc7c4b7,'painted grey':0x858880,'weathered red':0x7e4d3b,'red brick':0x875440,'dark red brick':0x754736,'pale render':0xb8b5a7,'cream stone':0xb6aa89,'ochre brick':0x927454,'orange stucco':0xa86243};
export async function createNeighborhoodRenderer({scene,loader,renderer,data,core,asset,onChange,onStatus}){
 const materialCache=new Map(),textureCache=new Map(),proxyGroups=new Map(),states=new Map();
 const materialVariants=new Map();
 // Core and neighborhood recipes can use the same human-readable name with
 // different paint colors or textures. Share only equivalent materials.
 const materialKey=m=>JSON.stringify([m.name,m.color?.toArray(),m.roughness,m.metalness,m.opacity,m.side,m.emissive?.toArray(),m.emissiveIntensity,...['map','normalMap','roughnessMap','metalnessMap'].map(k=>m[k]?.name||null)]);
 const maxAniso=Math.min(8,renderer.capabilities.getMaxAnisotropy());
 core.traverse(o=>{if(!o.isMesh)return;const ms=Array.isArray(o.material)?o.material:[o.material];for(const m of ms){if(!materialCache.has(m.name))materialCache.set(m.name,m);for(const field of ['map','normalMap','roughnessMap','metalnessMap'])if(m[field]&&m[field].name)textureCache.set(field+':'+m[field].name,m[field]);}if(o.name.startsWith('Streets'))o.visible=false;});
 core.traverse(o=>{if(o.isMesh)for(const m of Array.isArray(o.material)?o.material:[o.material])materialVariants.set(materialKey(m),m);});
 // Preserve the authored core, batching its static meshes by material for driving.
 core.updateMatrixWorld(true);const coreBatches=new Map();
 core.traverse(o=>{if(!o.isMesh||!o.visible||Array.isArray(o.material))return;const g=o.geometry.clone();g.applyMatrix4(o.matrixWorld);for(const name of Object.keys(g.attributes))if(!['position','normal','uv'].includes(name))g.deleteAttribute(name);if(!g.attributes.normal)g.computeVertexNormals();if(!g.attributes.uv)g.setAttribute('uv',new THREE.BufferAttribute(new Float32Array(g.attributes.position.count*2),2));if(!g.index)g.setIndex(Array.from({length:g.attributes.position.count},(_,i)=>i));if(!coreBatches.has(o.material))coreBatches.set(o.material,[]);coreBatches.get(o.material).push(g);});
 const original=[];core.traverse(o=>{if(o.isMesh)original.push(o.geometry);});core.clear();original.forEach(g=>g.dispose());
 for(const [m,gs] of coreBatches){const mesh=new THREE.Mesh(mergeGeometries(gs,false),m);mesh.name='First and Tenth · '+m.name;mesh.castShadow=m.name!=='store glass';mesh.receiveShadow=true;core.add(mesh);gs.forEach(g=>g.dispose());}
 const mat=(name,color,roughness=.85)=>{if(materialCache.has(name))return materialCache.get(name);const m=new THREE.MeshStandardMaterial({name,color,roughness});materialCache.set(name,m);return m;};
 const batches=new Map();
 function geometry(g,m){g=g.toNonIndexed();if(g.getAttribute('uv')===undefined)g.setAttribute('uv',new THREE.BufferAttribute(new Float32Array(g.getAttribute('position').count*2),2));if(!batches.has(m))batches.set(m,[]);batches.get(m).push(g);}
 function box(x,y,z,w,h,d,m,angle=0){
  const g=new THREE.BoxGeometry(w,h,d);g.rotateY(angle);g.translate(x,y,z);
  // Use metre-scale surface coordinates: default cube UVs stretch one asphalt
  // image across the entire neighborhood and smear pavement normal maps.
  if(m.map||m.normalMap){const p=g.attributes.position,n=g.attributes.normal,uv=g.attributes.uv;for(let i=0;i<p.count;i++){const nx=Math.abs(n.getX(i)),ny=Math.abs(n.getY(i)),nz=Math.abs(n.getZ(i));if(ny>=nx&&ny>=nz)uv.setXY(i,p.getX(i)/3,p.getZ(i)/3);else if(nx>nz)uv.setXY(i,p.getZ(i)/1.3,p.getY(i)/.9);else uv.setXY(i,p.getX(i)/1.3,p.getY(i)/.9);}}
  geometry(g,m);
 }
 const asphalt=mat('asphalt',0x404441),pavement=mat('sidewalk',0x9b9a8c),curb=mat('curb granite',0xa9aaa1),seam=mat('concrete seam',0x64665f),white=mat('road paint',0xd4d0b7),green=mat('bike green',0x41694f),yellow=mat('yellow paint',0xcda651),busRed=mat('bus lane red',0x854b3d);
 const ext=data.extent,avs=data.avenues,sts=data.streets;
 box((ext[0]+ext[2])/2,-.14,(ext[1]+ext[3])/2,ext[2]-ext[0],.28,ext[3]-ext[1],asphalt);
 const xcuts=[ext[0],...avs.map(a=>a[1]),ext[2]],zcuts=[ext[1],...sts.map(s=>s[1]),ext[3]];
 for(let xi=0;xi<xcuts.length-1;xi++)for(let zi=0;zi<zcuts.length-1;zi++){
  const x0=xcuts[xi]+(xi?avs[xi-1][2]:0),x1=xcuts[xi+1]-(xi<avs.length?avs[xi][2]:0),z0=zcuts[zi]+(zi?4.95:0),z1=zcuts[zi+1]-(zi<sts.length?4.95:0);
  box((x0+x1)/2,.07,(z0+z1)/2,x1-x0,.20,z1-z0,pavement);
  for(const x of [x0,x1])box(x,.07,(z0+z1)/2,.19,.24,z1-z0,curb);
  for(const z of [z0,z1])box((x0+x1)/2,.07,z,x1-x0,.24,.19,curb);
  for(let z=Math.ceil(z0/2.1)*2.1;z<z1;z+=2.1)for(const x of [x0+2.1,x1-2.1])box(x,.174,z,4.15,.004,.018,seam);
  for(let x=Math.ceil(x0/2.1)*2.1;x<x1;x+=2.1)for(const z of [z0+2.1,z1-2.1])box(x,.174,z,.018,.004,4.1,seam);
 }
 // Park-side pavement and planted ground continue past the dead-end side streets.
 const lawn=mat('park lawn',0x596b3c),earth=mat('park path',0x9c9279);
 box(252.5,.18,114,39,.10,211,lawn);box(228.15,.19,114,9.7,.10,213,pavement);box(244,.24,114,3,.025,209,earth);
 for(const z of [73.3,150.1])box(239,.235,z,24,.02,3.2,earth);
 for(const r of data.roads){
  if(r.axis==='avenue'){
   const x=r.a[0];for(let zi=0;zi<sts.length-1;zi++){
    const z0=sts[zi][1]+12,z1=sts[zi+1][1]-12;if(z1<=z0)continue;
    const facility=r.facilities;
    if(facility){
     for(const side of facility.sides){
      const bike=x+side*facility.offset,w=facility.width;
      // Full green for protected tracks; conventional lanes retain asphalt
      // between the small green conflict-area panels.
      if(facility.bike==='track')box(bike,.008,(z0+z1)/2,w,.009,z1-z0,green);
      else for(const z of [z0+3,z1-3])box(bike,.009,z,w,.009,5,green);
      for(const dx of [-w/2,w/2])box(bike+dx,.016,(z0+z1)/2,.10,.008,z1-z0,white);
      if(facility.bike==='track')for(let z=z0;z<z1;z+=4.2)box(x+side*6.6,.021,z,1.7,.006,.10,white,.36*side);
      const direction=r.name==='Avenue A'?-side:side;
      for(let z=z0+10;z<z1-5;z+=27){box(bike,.022,z,.09,.008,2,white);box(bike-.24,.022,z+direction*.67,.72,.008,.09,white,-direction*.8);box(bike+.24,.022,z+direction*.67,.72,.008,.09,white,direction*.8);}
     }
     if(facility.busSide){const bx=x+facility.busSide*(r.halfWidth-facility.busWidth/2);box(bx,.009,(z0+z1)/2,facility.busWidth,.009,z1-z0,busRed);box(bx-facility.busSide*facility.busWidth/2,.019,(z0+z1)/2,.12,.008,z1-z0,white);}
    }
    for(let z=z0;z<z1;z+=8.5){
     for(const dx of r.name==='Avenue A'?[0]:[-1.8,1.5,4.6])box(x+dx,.019,z,.11,.008,2.9,r.name==='Avenue A'?yellow:white);
    }
   }
  }else{
   for(let xi=0;xi<avs.length-1;xi++){
    const x0=avs[xi][1]+16,x1=avs[xi+1][1]-16,z=r.a[1];
    const facility=r.facilities;
    if(facility){
     const bz=z+facility.side*facility.offset,w=facility.width;
     if(facility.bike==='track')box((x0+x1)/2,.009,bz,x1-x0,.009,w,green);
     else for(const x of [x0+3,x1-3])box(x,.009,bz,5,.009,w,green);
     for(const dz of [-w/2,w/2])box((x0+x1)/2,.018,bz+dz,x1-x0,.008,.10,white);
     for(let x=x0+12;x<x1-8;x+=42){box(x,.022,bz,1.8,.008,.09,white);for(const side of [-1,1])box(x+r.oneway*.64,.022,bz+side*.23,.74,.008,.09,white,-r.oneway*side*.75);}
    }
    for(const x of [x0+26,x1-26]){
     const dir=r.oneway;box(x,.019,z,2.6,.012,.14,white);
     box(x+dir*.90,.019,z-.34,1.0,.012,.12,white,dir*.74);box(x+dir*.90,.019,z+.34,1.0,.012,.12,white,-dir*.74);
    }
   }
  }
 }
 for(const [avenue,x,width] of avs)for(const [street,z] of sts){
  for(const dz of [-7.2,7.2])for(let dx=-width+.7;dx<width;dx+=1.25)box(x+dx,.024,z+dz,.57,.014,2.7,white);
  for(const dx of [-width-2,width+2]){
   if(avenue==='Avenue A'&&dx>0&&['East 9th Street','St. Marks Place'].includes(street))continue;
   for(let dz=-4.1;dz<4.2;dz+=1.18)box(x+dx,.024,z+dz,2.75,.014,.53,white);
  }
  for(const sx of [-1,1])for(const sz of [-1,1]){
   box(x+sx*(width+1.2),.18,z+sz*6.3,1.24,.035,1.2,yellow);
   for(let k=0;k<6;k++)box(x+sx*(width+1.2),.205,z+sz*6.3+(k-2.5)*.16,1.1,.006,.03,curb);
  }
 }
 const ground=new THREE.Group();ground.name='Connected streets and sidewalks';scene.add(ground);
 for(const [m,gs] of batches){const merged=mergeGeometries(gs,false);const mesh=new THREE.Mesh(merged,m);mesh.receiveShadow=true;ground.add(mesh);gs.forEach(g=>g.dispose());}batches.clear();

 // Lightweight silhouettes and window planes keep distant streets continuous.
 for(const tile of data.tiles){
  const group=new THREE.Group();group.name='Distant '+tile.id;scene.add(group);proxyGroups.set(tile.id,group);
  const shapes=new Map(),windows=[];
  for(const b of data.buildings.filter(b=>b.tile===tile.id&&!b.core)){
   const spec=b.facadeSpec||{},color=COLORS[spec.wall]||COLORS['warm brick'];
   const shape=new THREE.Shape(b.p.map(p=>new THREE.Vector2(p[0],-p[1])));for(const hole of b.holes||[])shape.holes.push(new THREE.Path(hole.map(p=>new THREE.Vector2(p[0],-p[1]))));
   const g=new THREE.ExtrudeGeometry(shape,{depth:b.renderHeight||spec.height||b.height,bevelEnabled:false,steps:1});g.rotateX(-Math.PI/2);g.translate(0,.17,0);
   if(!shapes.has(color))shapes.set(color,[]);shapes.get(color).push(g);
   if(!spec.landmark)for(const f of b.frontages){const floors=spec.floors||b.floors,cols=Math.max(2,Math.round(f.length/2.65)),h=spec.height||b.height,step=(h-3.85)/Math.max(1,floors-1),theta=-Math.atan2(f.rz,f.rx);for(let row=0;row<floors-1;row++)for(let col=0;col<cols;col++){const s=(col+.5)*f.length/cols;windows.push({x:f.x+f.rx*s-f.rz*.14,y:3.65+row*step+Math.min(2.1,step*.68)/2,z:f.z+f.rz*s+f.rx*.14,h:Math.min(2.1,step*.68),angle:theta});}}
  }
  for(const [color,gs] of shapes){const g=mergeGeometries(gs,false),m=new THREE.MeshStandardMaterial({color,roughness:.95});group.add(new THREE.Mesh(g,m));gs.forEach(g=>g.dispose());}
  if(windows.length){const geo=new THREE.PlaneGeometry(1.08,1),mesh=new THREE.InstancedMesh(geo,new THREE.MeshStandardMaterial({color:0x33403e,roughness:.4,metalness:.2,side:THREE.DoubleSide}),windows.length),dummy=new THREE.Object3D();windows.forEach((w,i)=>{dummy.position.set(w.x,w.y,w.z);dummy.rotation.y=w.angle;dummy.scale.set(1,w.h,1);dummy.updateMatrix();mesh.setMatrixAt(i,dummy.matrix);});mesh.instanceMatrix.needsUpdate=true;group.add(mesh);}
  states.set(tile.id,{tile,root:null,promise:null,lastNeeded:0,failedAt:0});
 }
 let detailedGlass=true;
 function styleGlass(m){m.transmission=detailedGlass?.96:0;m.opacity=detailedGlass?1:.18;m.transparent=!detailedGlass;m.depthWrite=detailedGlass;m.metalness=detailedGlass?0:.5;m.color.set(detailedGlass?0xffffff:0x91a6ac);m.needsUpdate=true;}
 function prepare(root){root.traverse(o=>{if(!o.isMesh)return;o.castShadow=true;o.receiveShadow=true;const materials=Array.isArray(o.material)?o.material:[o.material];o.material=materials.map(m=>{if(m.name==='seventh glass'){const source=m;m=new THREE.MeshPhysicalMaterial({name:source.name,color:0xffffff,roughness:.008,metalness:0,transmission:.96,ior:1.5,thickness:.006,envMapIntensity:.9,side:THREE.FrontSide});source.dispose();}const key=materialKey(m);if(materialVariants.has(key)){const known=materialVariants.get(key);if(m!==known)m.dispose();return known;}for(const field of ['map','normalMap','roughnessMap','metalnessMap'])if(m[field]){const t=m[field],k=field+':'+t.name;if(t.name&&textureCache.has(k)){m[field]=textureCache.get(k);t.dispose();}else if(t.name)textureCache.set(k,t);}m.envMapIntensity=.75;if(m.map)m.map.anisotropy=maxAniso;if(m.normalMap)m.normalScale.set(.35,.35);if(m.name==='seventh glass')styleGlass(m);materialVariants.set(key,m);return m;});if(!Array.isArray(o.material)||o.material.length===1)o.material=o.material[0];const ms=Array.isArray(o.material)?o.material:[o.material];if(ms.every(m=>m.name==='store glass'||m.name==='seventh glass'))o.castShadow=false;});return root;}
 const distance=(x,z,b)=>Math.hypot(Math.max(b[0]-x,0,x-b[2]),Math.max(b[1]-z,0,z-b[3]));
 let queue=[],active=0,alive=true,cornerEnvironment;
 function reflectCorner(){
  if(cornerEnvironment||!['block-5-1','block-5-2','edge-south'].every(id=>states.get(id)?.root))return;
  const hidden=[];scene.traverse(o=>{if(o.isMesh&&o.material?.name==='seventh glass'&&o.visible){o.visible=false;hidden.push(o);}});
  const target=new THREE.WebGLCubeRenderTarget(256,{type:THREE.HalfFloatType}),probe=new THREE.CubeCamera(.15,190,target);probe.position.set(0,2.2,228);
  try{probe.update(renderer,scene);const pmrem=new THREE.PMREMGenerator(renderer);cornerEnvironment=pmrem.fromCubemap(target.texture);pmrem.dispose();for(const material of materialVariants.values())if(material.name==='seventh glass'){material.envMap=cornerEnvironment.texture;material.envMapIntensity=1.25;material.needsUpdate=true;}}finally{for(const mesh of hidden)mesh.visible=true;target.dispose();}
 }
 function pump(){while(alive&&active<2&&queue.length){const s=queue.shift();if(s.root||s.promise)continue;active++;onStatus?.('Loading nearby streets…');s.promise=loader.loadAsync(asset(s.tile.url)).then(g=>{s.root=prepare(g.scene);scene.add(s.root);proxyGroups.get(s.tile.id).visible=false;reflectCorner();onChange?.();}).catch(error=>{s.failedAt=performance.now();console.warn('Neighborhood section unavailable',s.tile.id,error);onStatus?.('Some street details could not load. They will retry.');}).finally(()=>{s.promise=null;active--;if(!active&&!queue.length)onStatus?.('');pump();});}}
 function update(x,z,now){
  const ordered=[...states.values()].sort((a,b)=>distance(x,z,a.tile.bounds)-distance(x,z,b.tile.bounds));
  queue=[];
  for(const s of ordered){const d=distance(x,z,s.tile.bounds);if(d<116){s.lastNeeded=now;if(!s.root&&!s.promise&&(!s.failedAt||now-s.failedAt>12000))queue.push(s);}else if(s.root&&d>205&&now-s.lastNeeded>6500){scene.remove(s.root);s.root.traverse(o=>{if(o.isMesh)o.geometry.dispose();});s.root=null;proxyGroups.get(s.tile.id).visible=true;onChange?.();}}
  pump();
  const coreDistance=Math.hypot(Math.max(Math.abs(x)-65,0),Math.max(Math.abs(z)-70,0));core.visible=coreDistance<230;
 }
 // Reusable prop meshes are instanced, sharing geometry and materials.
 async function instanceAsset(url,placements,name){if(!placements.length)return;const gltf=await loader.loadAsync(asset(url));prepare(gltf.scene);gltf.scene.updateMatrixWorld(true);const cells=new Map();for(const p of placements){const k=Math.floor(p.x/80)+','+Math.floor(p.z/80);if(!cells.has(k))cells.set(k,[]);cells.get(k).push(p);}const root=new THREE.Group();root.name=name;const transform=new THREE.Matrix4(),dummy=new THREE.Object3D();gltf.scene.traverse(o=>{if(!o.isMesh)return;for(const group of cells.values()){const mesh=new THREE.InstancedMesh(o.geometry,o.material,group.length);group.forEach((p,i)=>{dummy.position.set(p.x,0,p.z);dummy.rotation.set(0,p.angle||0,0);dummy.scale.setScalar(p.scale||1);dummy.updateMatrix();transform.multiplyMatrices(dummy.matrix,o.matrixWorld);mesh.setMatrixAt(i,transform);});mesh.instanceMatrix.needsUpdate=true;mesh.computeBoundingSphere();mesh.castShadow=true;mesh.receiveShadow=true;root.add(mesh);}});scene.add(root);onChange?.();}
 const signals=[];const signs=new THREE.Group();signs.name='Street name signs';scene.add(signs);
 const signMaterials=new Map();function streetSign(name,x,z,y,angle){if(!signMaterials.has(name)){const c=document.createElement('canvas');c.width=512;c.height=96;const ctx=c.getContext('2d');ctx.fillStyle='#285348';ctx.fillRect(0,0,512,96);ctx.strokeStyle='#d8dfce';ctx.lineWidth=3;ctx.strokeRect(5,5,502,86);ctx.fillStyle='#f4eee1';ctx.font='500 49px Arial';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(name,256,49,466);const texture=new THREE.CanvasTexture(c);texture.colorSpace=THREE.SRGBColorSpace;texture.anisotropy=maxAniso;signMaterials.set(name,new THREE.MeshStandardMaterial({map:texture,roughness:.7,side:THREE.DoubleSide}));}const mesh=new THREE.Mesh(new THREE.PlaneGeometry(1.82,.34),signMaterials.get(name));mesh.position.set(x,y,z);mesh.rotation.y=angle;signs.add(mesh);}
 for(const [avenue,x,width] of avs)for(const [street,z] of sts){if(avenue==='First Avenue'&&['East 10th Street','East 7th Street'].includes(street))continue;for(const side of [-1,1]){const px=x+side*(width+.75),pz=z+side*6.2;signals.push({x:px,z:pz,angle:side<0?0:Math.PI});streetSign(street.replace('East ','E ').replace('Street','St'),px,pz,3.55,0);streetSign(avenue.replace('Avenue','Ave'),px,pz,3.95,Math.PI/2);}}
 const props=Promise.allSettled([...(data.detailProps||[]).map(group=>instanceAsset(group.url,group.placements,group.name)),instanceAsset('neighborhood/street-tree.glb',data.trees||[],'Street trees'),instanceAsset('neighborhood/park-bench.glb',data.benches||[],'Park benches'),instanceAsset('neighborhood/parked-car.glb',data.parked?.filter(p=>!p.core)||[],'Parked cars'),instanceAsset('neighborhood/street-furniture.glb',data.furniture||[],'Street furniture'),instanceAsset('neighborhood/traffic-signal.glb',signals,'Traffic signals')]);
 props.then(results=>{if(results.some(r=>r.status==='rejected'))onStatus?.('Some street furniture could not load.');});
 return {update,setQuality(value){detailedGlass=value!=='fast';for(const m of materialVariants.values())if(m.name==='seventh glass')styleGlass(m);},dispose(){alive=false;cornerEnvironment?.dispose();},states,props};
}
