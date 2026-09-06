import * as THREE from './vendor/three.module.js';
import {mergeGeometries} from './vendor/BufferGeometryUtils.js';
import {inPolygon} from './physics.js';
const rand=n=>{let x=Math.sin(n*127.1+311.7)*43758.5453;return x-Math.floor(x);};
function color(c){return new THREE.Color(c);}
function mesh(geo,mat,scene){const m=new THREE.Mesh(geo,mat);scene.add(m);return m;}
function batchBox(list,x,y,z,w,h,d,angle=0){const g=new THREE.BoxGeometry(w,h,d);g.rotateY(angle);g.translate(x,y,z);list.push(g);}
function batchStrip(list,a,b,w,y,h=.035){const dx=b[0]-a[0],dz=b[1]-a[1],l=Math.hypot(dx,dz);if(l<.01)return;batchBox(list,(a[0]+b[0])/2,y,(a[1]+b[1])/2,w,h,l,Math.atan2(dx,dz));}
function flush(list,mat,scene,shadows=false){if(!list.length)return;const merged=mergeGeometries(list,false);list.forEach(g=>g.dispose());const m=mesh(merged,mat,scene);m.receiveShadow=true;m.castShadow=shadows;return m;}
function polygon(points,y){const shape=new THREE.Shape(points.map(p=>new THREE.Vector2(p[0],-p[1])));const g=new THREE.ShapeGeometry(shape);g.rotateX(-Math.PI/2);g.translate(0,y,0);return g;}
export function createCity(scene,data,world){
 const groundMat=new THREE.MeshStandardMaterial({color:0xb6b3a8,roughness:1});const ground=mesh(new THREE.PlaneGeometry(12000,12000),groundMat,scene);ground.rotation.x=-Math.PI/2;ground.position.y=-.06;ground.receiveShadow=true;
 const sidewalks=[],asphalt=[],white=[],yellow=[],paths=[],grass=[];
 const roadMat=new THREE.MeshStandardMaterial({color:0x666a69,roughness:.98});const sideMat=new THREE.MeshStandardMaterial({color:0xbfbdb1,roughness:1});const whiteMat=new THREE.MeshStandardMaterial({color:0xd8d5c5,roughness:1});const yellowMat=new THREE.MeshStandardMaterial({color:0xd6b574,roughness:1});
 const inter=new Map();
 for(const r of data.roads){
  for(let i=0;i<r.p.length;i++){const k=r.nodes[i];if(!inter.has(k))inter.set(k,{p:r.p[i],roads:[],w:r.w});const n=inter.get(k);if(!n.roads.some(x=>x.id===r.id))n.roads.push(r);n.w=Math.max(n.w,r.w);}
  for(let i=1;i<r.p.length;i++){const a=r.p[i-1],b=r.p[i];const mid=[(a[0]+b[0])/2,(a[1]+b[1])/2];if(mid[0]<data.bounds[0]-100||mid[0]>data.bounds[2]+100||mid[1]<data.bounds[1]-100||mid[1]>data.bounds[3]+100)continue;batchStrip(sidewalks,a,b,r.w+6.5,.005,.09);batchStrip(asphalt,a,b,r.w,.069,.025);
   const dx=b[0]-a[0],dz=b[1]-a[1],l=Math.hypot(dx,dz);if(l<.5)continue;const ux=dx/l,uz=dz/l;
   if(!r.oneway&&r.w>9){for(const off of [-.14,.14])batchStrip(yellow,[a[0]-uz*off,a[1]+ux*off],[b[0]-uz*off,b[1]+ux*off],.075,.087,.006);}
   else if(r.w>13){for(let t=1;t<l-4;t+=12)batchStrip(white,[a[0]+ux*t,a[1]+uz*t],[a[0]+ux*(t+4),a[1]+uz*(t+4)],.09,.087,.006);}
  }
 }
 // Rounded joins keep the exact polyline road network drivable.
 for(const n of inter.values()){if(n.p[0]<data.bounds[0]-30||n.p[0]>data.bounds[2]+30||n.p[1]<data.bounds[1]-30||n.p[1]>data.bounds[3]+30)continue;
  for(const [arr,radius,y] of [[sidewalks,n.w/2+3.2,.049],[asphalt,n.w/2,.084]]){const g=new THREE.CircleGeometry(radius,12);g.rotateX(-Math.PI/2);g.translate(n.p[0],y,n.p[1]); // Match box attributes for merging.
   const boxCompatible=g.toNonIndexed();g.dispose();arr.push(boxCompatible);}
 }
 // Use separate batches for indexed/nonindexed road pieces.
 function flushMixed(arr,mat){const converted=arr.map(g=>g.index?g.toNonIndexed():g);const m=flush(converted,mat,scene);arr.forEach((g,i)=>{if(converted[i]!==g)g.dispose();});return m;}
 flushMixed(sidewalks,sideMat);flushMixed(asphalt,roadMat);
 // Crosswalk stripes use actual shared street nodes, with duplicates removed.
 const crossings=[];
 for(const n of inter.values()){const names=new Set(n.roads.map(r=>r.name));if(names.size<2)continue;if(crossings.some(p=>Math.hypot(p[0]-n.p[0],p[1]-n.p[1])<15))continue;crossings.push(n.p);
  for(const r of n.roads){const idx=r.p.findIndex(p=>Math.hypot(p[0]-n.p[0],p[1]-n.p[1])<.1);for(const j of [idx-1,idx+1]){if(j<0||j>=r.p.length)continue;let next=r.p[j],dx=next[0]-n.p[0],dz=next[1]-n.p[1],l=Math.hypot(dx,dz);if(l<.1)continue;dx/=l;dz/=l;const dist=n.w/2+2.8;for(let off=-r.w/2+1;off<r.w/2-1;off+=1.5){const x=n.p[0]+dx*dist-dz*off,z=n.p[1]+dz*dist+dx*off;batchStrip(white,[x-dx*1.7,z-dz*1.7],[x+dx*1.7,z+dz*1.7],.7,.099,.009);}}}
 }
 flush(white,whiteMat,scene);flush(yellow,yellowMat,scene);
 for(const p of data.parks){grass.push(polygon(p.p,.13));}
 flush(grass,new THREE.MeshStandardMaterial({color:0x82916c,roughness:1}),scene);
 // A world-unit façade shader creates window bays without thousands of meshes.
 const buildingMat=new THREE.MeshStandardMaterial({vertexColors:true,roughness:.91});
 buildingMat.onBeforeCompile=shader=>{
  shader.uniforms.uNight={value:0};buildingMat.userData.shader=shader;
  shader.vertexShader=shader.vertexShader.replace('#include <common>','#include <common>\nattribute float facade; varying float vFacade; varying vec2 vCityUv;').replace('#include <begin_vertex>','#include <begin_vertex>\nvFacade=facade;vCityUv=uv;');
  shader.fragmentShader=shader.fragmentShader.replace('#include <common>','#include <common>\nvarying float vFacade;varying vec2 vCityUv;uniform float uNight;');
  shader.fragmentShader=shader.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
  if(vFacade>0.5){
   vec2 cell=vec2(fract(vCityUv.x/3.1),fract((vCityUv.y-.9)/3.25));
   float window=step(.27,cell.x)*step(cell.x,.72)*step(.22,cell.y)*step(cell.y,.76)*step(3.7,vCityUv.y);
   float trim=step(.23,cell.x)*step(cell.x,.76)*step(.17,cell.y)*step(cell.y,.80)*step(3.7,vCityUv.y);
   vec2 bay=floor(vec2(vCityUv.x/3.1,(vCityUv.y-.9)/3.25));
   float lit=step(.69,fract(sin(dot(bay,vec2(12.9898,78.233)))*43758.5453));
   vec3 glass=mix(vec3(.16,.23,.25),vec3(.9,.62,.24),lit*uNight);
   glass+=step(.6,cell.y)*.018;
   diffuseColor.rgb=mix(diffuseColor.rgb,diffuseColor.rgb*.75,trim);
   diffuseColor.rgb=mix(diffuseColor.rgb,glass,window);
   float sill=step(.15,cell.y)*step(cell.y,.2)*step(.21,cell.x)*step(cell.x,.78)*step(3.7,vCityUv.y);
   diffuseColor.rgb=mix(diffuseColor.rgb,diffuseColor.rgb*1.24,sill);
   float band=step(fract((vCityUv.y-.3)/3.25),.021)*step(3.7,vCityUv.y);
   diffuseColor.rgb*=1.-band*.1;
   if(vCityUv.y<3.7){float shop=step(.12,fract(vCityUv.x/4.5))*step(fract(vCityUv.x/4.5),.87)*step(.45,vCityUv.y)*step(vCityUv.y,2.8);diffuseColor.rgb=mix(diffuseColor.rgb*.79,vec3(.14,.21,.21),shop*.88);}
  }`);
 };
 const palettes=['#a1846b','#b8a38a','#947567','#b4967b','#aab1ad','#c4bcb0','#887b71','#b9b7a6','#8e7770','#bca38a','#a89988'];
 const chunks=new Map();
 for(const b of data.buildings){const key=Math.floor(b.c[0]/220)+','+Math.floor(b.c[1]/220);if(!chunks.has(key))chunks.set(key,{pos:[],uv:[],col:[],fac:[]});const buf=chunks.get(key);const c=color(palettes[Math.floor(rand(b.id)*palettes.length)]);const roofColor=c.clone().multiplyScalar(.81);let offset=rand(b.id+1)*200;
  function tri(a,bp,cp,uv,c,face){for(let i=0;i<3;i++){const p=[a,bp,cp][i];buf.pos.push(...p);buf.uv.push(...uv[i]);buf.col.push(c.r,c.g,c.b);buf.fac.push(face);}}
  for(let i=1;i<b.p.length;i++){const a=b.p[i-1],p=b.p[i],l=Math.hypot(p[0]-a[0],p[1]-a[1]);if(l<.1)continue;const low=b.base,high=b.h;
   tri([a[0],low,a[1]],[p[0],high,p[1]],[p[0],low,p[1]],[[offset,low],[offset+l,high],[offset+l,low]],c,1);
   tri([a[0],low,a[1]],[a[0],high,a[1]],[p[0],high,p[1]],[[offset,low],[offset,high],[offset+l,high]],c,1);offset+=l;
  }
  const shape=new THREE.Shape(b.p.map(p=>new THREE.Vector2(p[0],-p[1])));const g=new THREE.ShapeGeometry(shape);const positions=g.getAttribute('position');const indices=g.index.array;
  for(let i=0;i<indices.length;i+=3){const t=[];for(let j=0;j<3;j++){const k=indices[i+j];t.push([positions.getX(k),b.h,-positions.getY(k)]);}tri(t[0],t[1],t[2],[[0,0],[0,0],[0,0]],roofColor,0);}g.dispose();
 }
 const buildingMeshes=[];buildingMat.side=THREE.DoubleSide;
 for(const buf of chunks.values()){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(buf.pos,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(buf.uv,2));g.setAttribute('color',new THREE.Float32BufferAttribute(buf.col,3));g.setAttribute('facade',new THREE.Float32BufferAttribute(buf.fac,1));g.computeVertexNormals();g.computeBoundingSphere();const m=mesh(g,buildingMat,scene);m.castShadow=true;m.receiveShadow=true;buildingMeshes.push(m);}
 // Cornices, rooftop equipment and occasional tanks enrich the silhouette.
 const cornices=[],roofboxes=[],tanks=[],tanklegs=[],awnings=[];
 for(const b of data.buildings){if(b.base>0)continue;for(let i=1;i<b.p.length;i++){const a=b.p[i-1],p=b.p[i];batchStrip(cornices,a,p,.32,b.h+.14,.34);}
  if(rand(b.id+8)>.62&&inPolygon(b.c[0],b.c[1],b.p)){batchBox(roofboxes,b.c[0],b.h+.65,b.c[1],2.5,1.3,2.8,rand(b.id));}
  if(rand(b.id+23)>.965&&b.h>16&&inPolygon(b.c[0],b.c[1],b.p)){const g=new THREE.CylinderGeometry(1.5,1.5,3.5,10);g.translate(b.c[0],b.h+4.3,b.c[1]);tanks.push(g);const top=new THREE.ConeGeometry(1.65,.85,10);top.translate(b.c[0],b.h+6.48,b.c[1]);tanks.push(top);for(const x of [-1,1])for(const z of [-1,1])batchBox(tanklegs,b.c[0]+x,b.h+1.5,b.c[1]+z,.13,3,.13);}
  if(rand(b.id+31)>.63){let best=null;for(let i=1;i<b.p.length;i++){const a=b.p[i-1],p=b.p[i],mid=[(a[0]+p[0])/2,(a[1]+p[1])/2],l=Math.hypot(p[0]-a[0],p[1]-a[1]);if(l<4||l>35)continue;const n=world.nearest(...mid);if(n.d<24&&(!best||n.d<best.n.d))best={a,p,n,l,mid};}if(best){let {a,p,n,l,mid}=best;let dx=n.x-mid[0],dz=n.z-mid[1],len=Math.hypot(dx,dz);if(len){dx/=len;dz/=len;batchBox(awnings,mid[0]+dx*.55,3.3,mid[1]+dz*.55,Math.min(l-1,11),.23,1.25,Math.atan2(-(p[1]-a[1]),p[0]-a[0]));}}}
 }
 flush(cornices,new THREE.MeshStandardMaterial({color:0xc9c2b3,roughness:1}),scene,true);flush(roofboxes,new THREE.MeshStandardMaterial({color:0x93978f,roughness:1}),scene,true);flush(tanks,new THREE.MeshStandardMaterial({color:0x78685a,roughness:1}),scene,true);flush(tanklegs,new THREE.MeshStandardMaterial({color:0x4e5551,roughness:1}),scene);flush(awnings,new THREE.MeshStandardMaterial({color:0x486f65,roughness:1}),scene,true);
 const treeLocations=[];const treeCells=new Set();function addTree(x,z,seed){const key=Math.round(x/8)+','+Math.round(z/8);if(treeCells.has(key)||world.solid(x,z))return;treeCells.add(key);treeLocations.push([x,z,seed]);}
 for(const r of data.roads){let acc=0;for(let i=1;i<r.p.length;i++){const a=r.p[i-1],b=r.p[i],l=Math.hypot(b[0]-a[0],b[1]-a[1]);if(l<.1)continue;const dx=(b[0]-a[0])/l,dz=(b[1]-a[1])/l;for(let s=(25-acc%25);s<l;s+=25){if(rand(r.id+s)>.55)continue;for(const side of [-1,1]){const off=(r.w/2+1.7)*side;const x=a[0]+dx*s-dz*off,z=a[1]+dz*s+dx*off;if(x<data.bounds[0]||x>data.bounds[2]||z<data.bounds[1]||z>data.bounds[3])continue;addTree(x,z,r.id+s+side);}}acc+=l;}}
 for(const p of data.parks){const xs=p.p.map(a=>a[0]),zs=p.p.map(a=>a[1]);const minX=Math.max(data.bounds[0],Math.min(...xs)),maxX=Math.min(data.bounds[2],Math.max(...xs)),minZ=Math.max(data.bounds[1],Math.min(...zs)),maxZ=Math.min(data.bounds[3],Math.max(...zs));for(let x=minX+6;x<maxX;x+=13)for(let z=minZ+6;z<maxZ;z+=13){const px=x+rand(x+z)*7,pz=z+rand(x-z)*7;if(inPolygon(px,pz,p.p)&&world.nearest(px,pz).d>15)addTree(px,pz,x*2+z);}}
 const dummy=new THREE.Object3D();const trunks=new THREE.InstancedMesh(new THREE.CylinderGeometry(.14,.23,3.8,5),new THREE.MeshStandardMaterial({color:0x7c7460,roughness:1}),treeLocations.length);const leaves=new THREE.InstancedMesh(new THREE.IcosahedronGeometry(2.65,1),new THREE.MeshStandardMaterial({color:0xffffff,roughness:1,flatShading:true}),treeLocations.length*2);
 treeLocations.forEach(([x,z,s],i)=>{const scale=.8+rand(s)*.65;dummy.position.set(x,1.9*scale,z);dummy.scale.set(scale,scale,scale);dummy.updateMatrix();trunks.setMatrixAt(i,dummy.matrix);for(let j=0;j<2;j++){dummy.position.set(x+(j?1.2:-.5)*scale,(j?5:4.5)*scale,z+(j?.4:-.5));dummy.scale.set(scale*(j?.8:1),scale*(j?1.1:1.25),scale);dummy.rotation.y=rand(s)*6;dummy.updateMatrix();leaves.setMatrixAt(i*2+j,dummy.matrix);leaves.setColorAt(i*2+j,color(['#879567','#6e8965','#91a072','#788d6b'][Math.floor(rand(s+j)*4)]));}});trunks.castShadow=true;leaves.castShadow=true;leaves.receiveShadow=true;scene.add(trunks,leaves);
 const poles=[],lamps=[],signposts=[],signpanels=[];
 for(let i=0;i<crossings.length;i++){const p=crossings[i];const s=world.nearest(...p),dx=s.dx/Math.hypot(s.dx,s.dz),dz=s.dz/Math.hypot(s.dx,s.dz);const x=p[0]-dz*(s.road.w/2+1.5)+dx*10,z=p[1]+dx*(s.road.w/2+1.5)+dz*10;if(world.solid(x,z))continue;batchBox(poles,x,3.5,z,.16,7,.16);batchBox(poles,x+dz*.9,6.85,z-dx*.9,.12,.12,2,Math.atan2(-dx,dz));batchBox(lamps,x+dz*1.7,6.75,z-dx*1.7,.7,.16,.45);batchBox(signposts,x,3.8,z,2,.38,.1,Math.atan2(dx,dz));}
 flush(poles,new THREE.MeshStandardMaterial({color:0x525e57,roughness:1}),scene);const lampMat=new THREE.MeshStandardMaterial({color:0xffe4a1,emissive:0xffd080,emissiveIntensity:.35});flush(lamps,lampMat,scene);flush(signposts,new THREE.MeshStandardMaterial({color:0x386957,roughness:1}),scene);
 return {buildingMat,buildingMeshes,lampMat,roadMat,groundMat,trees:treeLocations.length};
}
export function createCar(scene){
 const car=new THREE.Group();scene.add(car);const paint=new THREE.MeshStandardMaterial({color:0xf5b83f,metalness:.18,roughness:.42});const trim=new THREE.MeshStandardMaterial({color:0x293b40,roughness:.65});const glass=new THREE.MeshStandardMaterial({color:0x3e6874,metalness:.12,roughness:.2});const chrome=new THREE.MeshStandardMaterial({color:0xc3ccc5,metalness:.6,roughness:.35});const rubber=new THREE.MeshStandardMaterial({color:0x263033,roughness:.95});
 function box(x,y,z,w,h,d,mat,rot=0){const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);m.position.set(x,y,z);m.rotation.x=rot;m.castShadow=true;car.add(m);return m;}
 box(0,.62,0,1.82,.58,4.02,paint);box(0,.79,-1.25,1.72,.22,1.5,paint);box(0,.83,1.5,1.76,.18,.82,paint);box(0,1.13,.13,1.58,.72,1.86,glass);box(0,1.52,.14,1.65,.08,1.73,paint);box(0,.45,-2.04,1.78,.12,.13,chrome);box(0,.46,2.04,1.78,.12,.13,chrome);box(0,.54,-2.12,.7,.15,.02,trim);
 for(const x of [-.81,.81]){box(x,1.16,.9,.08,.72,.08,paint);box(x,1.16,-.66,.08,.72,.08,paint);box(x,1.17,.1,.055,.70,.06,paint);box(x*1.19,1.01,-.48,.22,.12,.17,paint);box(x,1.05,.52,.025,.035,.2,chrome);}
 const headMat=new THREE.MeshStandardMaterial({color:0xfff4c9,emissive:0xffe3a0,emissiveIntensity:.45});const tailMat=new THREE.MeshStandardMaterial({color:0xda5840,emissive:0xff4422,emissiveIntensity:.6});for(const x of [-.63,.63]){box(x,.73,-2.035,.4,.16,.04,headMat);box(x,.73,2.035,.37,.14,.04,tailMat);}box(0,.52,2.071,.35,.12,.012,new THREE.MeshStandardMaterial({color:0xffd16e}));
 const wheels=[];for(const x of [-.9,.9])for(const z of [-1.27,1.24]){const group=new THREE.Group();group.position.set(x,.41,z);car.add(group);const tire=new THREE.Mesh(new THREE.CylinderGeometry(.39,.39,.23,16),rubber);tire.rotation.z=Math.PI/2;tire.castShadow=true;group.add(tire);const hub=new THREE.Mesh(new THREE.CylinderGeometry(.22,.22,.242,10),chrome);hub.rotation.z=Math.PI/2;group.add(hub);wheels.push({group,tire,hub,front:z<0});}
 const shadowCanvas=document.createElement('canvas');shadowCanvas.width=64;shadowCanvas.height=128;const ctx=shadowCanvas.getContext('2d');const grd=ctx.createRadialGradient(32,64,10,32,64,64);grd.addColorStop(0,'rgba(8,23,29,.4)');grd.addColorStop(1,'rgba(8,23,29,0)');ctx.fillStyle=grd;ctx.fillRect(0,0,64,128);const shadow=new THREE.Mesh(new THREE.PlaneGeometry(3.2,5.8),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(shadowCanvas),transparent:true,depthWrite:false}));shadow.rotation.x=-Math.PI/2;shadow.position.y=.105;car.add(shadow);
 return {group:car,wheels,tailMat,headMat};
}
