import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createNeighborhoodWorld} from '../dist/reconstruction/neighborhood-world.js';
import {createVehicle,stepVehicle} from '../dist/reconstruction/vehicle.js';
const root=path.resolve(import.meta.dirname,'../dist/reconstruction');
const data=JSON.parse(fs.readFileSync(path.join(root,'neighborhood.json'))),world=createNeighborhoodWorld(data);
assert.equal(data.tiles.filter(t=>t.id.startsWith('block-')).length,10);
assert.equal(new Set(data.buildings.map(b=>b.id)).size,data.buildings.length);
let roadSamples=0;
for(const road of data.roads){
 const len=Math.hypot(road.b[0]-road.a[0],road.b[1]-road.a[1]),yaw=road.axis==='avenue'?0:Math.PI/2;
 for(let dist=4;dist<len-4;dist+=2){const t=dist/len,x=road.a[0]+(road.b[0]-road.a[0])*t,z=road.a[1]+(road.b[1]-road.a[1])*t;assert(!world.carCollides(x,z,yaw),`Blocked road centerline: ${road.name} at ${x},${z}`);roadSamples++;}
}
for(const pose of [{x:-234,z:100,yaw:Math.PI},{x:218,z:100,yaw:0},{x:50,z:-160,yaw:Math.PI/2},{x:0,z:-170,yaw:Math.PI}]){
 const car=createVehicle(pose);for(let i=0;i<60;i++){const step=stepVehicle(car,{throttle:1},1/120,world,data.driveBounds);assert(!step.edge&&!step.collision,'Valid boundary lane should allow movement');}assert(Math.hypot(car.x-pose.x,car.z-pose.z)>.02);
}
for(const x of [-1000,-244,-229,0,214,230,1000])for(const z of [-1000,-174,-157.8,0,150.1,228,244,1000]){const p=world.spawn(x,z),b=data.driveBounds;assert(p.x>=b[0]&&p.x<=b[2]&&p.z>=b[1]&&p.z<=b[3]);assert(!world.carCollides(p.x,p.z,p.yaw),'Map destination must spawn a usable car');}
for(const z of [73.3,150.1]){assert(!world.roadAt(235,z),'Side streets must stop before Tompkins Square Park');assert(world.carCollides(235,z,Math.PI/2));}
assert(world.buildingAt(...data.buildings.find(b=>b.address==='163 1st Avenue').center),'Building collision must survive unloading visual tiles');
let bytes=0,triangles=0;
for(const tile of data.tiles){const file=path.join(root,tile.url),buf=fs.readFileSync(file);bytes+=buf.length;assert(buf.length<25*1024*1024);assert.equal(buf.readUInt32LE(0),0x46546c67);assert.equal(buf.readUInt32LE(8),buf.length);const jl=buf.readUInt32LE(12),doc=JSON.parse(buf.subarray(20,20+jl));assert(doc.meshes.length>0);assert(doc.extensionsRequired.includes('KHR_draco_mesh_compression'));const binLength=buf.readUInt32LE(20+jl);for(const v of doc.bufferViews)assert((v.byteOffset||0)+v.byteLength<=binLength,'Buffer view lies inside binary chunk');for(const m of doc.meshes)for(const p of m.primitives){const draco=p.extensions.KHR_draco_mesh_compression;assert(doc.bufferViews[draco.bufferView]);triangles+=(doc.accessors[p.indices]?.count||0)/3;}for(const image of doc.images||[]){assert(image.uri&&!image.uri.includes('..'));const img=fs.readFileSync(path.resolve(path.dirname(file),image.uri));assert(img.length>100);}assert.equal(tile.bytes,buf.length);}
const html=fs.readFileSync(path.join(root,'../index.html'),'utf8'),ids=new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]));
for(const name of ['neighborhood-map.js','neighborhood-render.js']){const source=fs.readFileSync(path.join(root,name),'utf8');for(const m of source.matchAll(/querySelector\('#([^']+)'\)/g))assert(ids.has(m[1]),'Map controls must exist: '+m[1]);for(const m of source.matchAll(/instanceAsset\('([^']+)'/g))assert(fs.existsSync(path.join(root,m[1])));}
console.log(JSON.stringify({blocks:10,tiles:data.tiles.length,mappedBuildings:data.buildings.length,photoObserved:data.referenceSummary.newObservedBuildings,roadSamples,detailMeshMB:+(bytes/1048576).toFixed(2),detailTriangles:triangles,validBoundaryDriving:true,validMapSpawns:true,parkDeadEnds:true},null,2));
