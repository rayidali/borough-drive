import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
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
// Every visual section must carry the current detail export, with bounded draw
// calls and the surface maps needed to show masonry at street level.
assert.equal(data.detailSummary.revision,'04');
assert.equal(data.detailSummary.buildings,data.buildings.filter(b=>!b.core).length);
let largestMaterialBatchCount=0;
for(const tile of data.tiles){
 assert.equal(tile.detailRevision,data.detailSummary.revision,`Stale detail export: ${tile.id}`);
 assert.equal(tile.detailBuildings,data.buildings.filter(b=>!b.core&&b.tile===tile.id).length);
 const buf=fs.readFileSync(path.join(root,tile.url));
 const doc=JSON.parse(buf.subarray(20,20+buf.readUInt32LE(12)));
 largestMaterialBatchCount=Math.max(largestMaterialBatchCount,doc.meshes.length);
 assert(doc.meshes.length<=64,`Section needs material batching: ${tile.id}`);
 for(const m of doc.materials){
  if(['warm brick','salmon brick','weathered red','buff brick','charcoal brick','aged brownstone','limestone facade'].includes(m.name)){
   assert(m.pbrMetallicRoughness.baseColorTexture,`Lost masonry color texture: ${m.name}`);
  }
  if(['warm brick','buff brick','painted ivory','painted grey','limestone facade'].includes(m.name)){
   assert(m.normalTexture&&m.pbrMetallicRoughness.metallicRoughnessTexture,`Lost masonry surface detail: ${m.name}`);
  }
 }
}
let streetObjects=0;
assert.equal(data.detailProps.length,5);
for(const group of data.detailProps){
 const file=path.resolve(root,group.url);
 assert(file.startsWith(root+path.sep),'Street detail assets stay in reconstruction/');
 const buf=fs.readFileSync(file);assert.equal(buf.readUInt32LE(0),0x46546c67);assert.equal(buf.readUInt32LE(8),buf.length);
 const doc=JSON.parse(buf.subarray(20,20+buf.readUInt32LE(12)));
 assert(doc.meshes.length>0&&doc.extensionsRequired.includes('KHR_draco_mesh_compression'));
 for(const p of group.placements){
  assert([p.x,p.z,p.angle].every(Number.isFinite),'Street objects have valid poses');
  assert(p.x>=data.extent[0]&&p.x<=data.extent[2]&&p.z>=data.extent[1]&&p.z<=data.extent[3]);
  assert(!(Math.abs(p.x)<72&&Math.abs(p.z)<75),'New furniture must preserve the accepted core');
  assert(!world.buildingAt(p.x,p.z),'Street objects must not be inside mapped buildings');
  if(!/utility-cover|drain-grate/.test(group.url))assert(!world.roadAt(p.x,p.z),'Upright street furniture belongs on the sidewalk');
  streetObjects++;
 }
}
assert.equal(streetObjects,data.detailSummary.streetObjects);
// Municipal additions must survive the complete prepare/compile/export chain,
// including the courtyard opening used by collision and distant geometry.
const corrections=JSON.parse(fs.readFileSync(path.resolve(root,'../../model-source/geography-corrections.json')));
const municipal=JSON.parse(fs.readFileSync(path.resolve(root,'../../source-data/nyc-buildings-2026-09-06.geojson')));
const byId=new Map(data.buildings.map(b=>[b.id,b]));
assert.equal(new Set(corrections.municipalMatches.map(r=>r.doittId)).size,municipal.features.length);
for(const r of corrections.municipalMatches)assert(byId.has(r.buildingId),'Municipal record has a modeled building');
for(const addition of corrections.addBuildings){
 const b=byId.get(addition.id);
 assert(b&&!b.core&&b.frontages.length,'Restored building has a street frontage');
 assert.equal(b.bin,String(addition.bin));
 assert(b.geometrySource&&b.height>3&&b.p.length>=4);
 assert(data.tiles.some(t=>t.id===b.tile),'Restored building belongs to an exported section');
}
const school=byId.get(-449265);
assert.equal(school.name,'East Side Community School');
for(const hole of school.holes){
 const x=hole.reduce((sum,p)=>sum+p[0],0)/hole.length,z=hole.reduce((sum,p)=>sum+p[1],0)/hole.length;
 assert(!world.buildingAt(x,z),'School courtyard must stay open');
}
let namedPlaces=0;
for(const b of data.buildings){
 const units=new Map();
 for(const p of b.businesses||[]){
  if(!p.renderName)continue;
  namedPlaces++;
  const f=b.frontages[p.frontageIndex];
  assert(f&&p.street===f.street,'Business belongs to its selected street frontage');
  assert.equal(p.buildingId,b.id);
  assert(p.sources.some(s=>s.publisher!=='OpenStreetMap contributors'&&(s.url||Object.keys(s.record||{}).length)),'Named business needs independent dated evidence');
  assert(p.unit?.every(Number.isFinite)&&p.unit[0]>=0&&p.unit[1]<=f.length&&p.unit[1]>p.unit[0],'Shop partition stays within its building');
  if(!units.has(p.frontageIndex))units.set(p.frontageIndex,[]);
  units.get(p.frontageIndex).push(p.unit);
 }
 for(const group of units.values()){
  group.sort((a,b)=>a[0]-b[0]);
  for(let i=1;i<group.length;i++)assert(group[i][0]>=group[i-1][1]-.001,'Named shop partitions must not overlap');
 }
}
assert.equal(namedPlaces,data.businessSummary.namedPlaces);
for(const [id,name,street] of [[241822336,'BLUE & GOLD','East 7th Street'],[-177966,'BIG BAR','East 7th Street'],[241822329,'ABRAÇO','East 7th Street']]){
 assert(byId.get(id).businesses.some(p=>p.renderName&&p.name===name&&p.street===street),'Seventh Street place must survive compilation: '+name);
}
assert.equal(byId.get(241822336).facadeSpec.groundProfile,'blue_gold');
// The beginning and reset share a safe northbound pose at First & Seventh.
const start=world.start();
assert.equal(start.x,data.avenues.find(a=>a[0]==='First Avenue')[1]);
assert.equal(start.z,data.streets.find(s=>s[0]==='East 7th Street')[1]);
assert.equal(start.yaw,0);assert(world.walkable(start.x,start.z));
assert(!world.carCollides(start.x,start.z,start.yaw));
const startingCar=createVehicle(start);
for(let i=0;i<240;i++){const result=stepVehicle(startingCar,{throttle:1},1/120,world,data.driveBounds);assert(!result.edge&&!result.collision);}
assert(startingCar.z<start.z-.5,'The start permits driving north into the neighborhood');
// Each individually observed storefront has a supported identity, source,
// selected elevation and current exported mesh. Observations are not occupancy.
const storefronts=JSON.parse(fs.readFileSync(path.resolve(root,'../../model-source/storefront-details.json')));
assert.equal(storefronts.frontages.length,data.storefrontDetailSummary.frontages);
assert.equal(new Set(storefronts.elevations.map(r=>r.buildingId+':'+r.street)).size,storefronts.elevations.length,'One schedule per elevation');
for(const r of [...storefronts.frontages,...storefronts.elevations]){
 assert(byId.has(r.buildingId)&&!byId.get(r.buildingId).core,'Storefront work preserves the core');
 assert(r.sources.length&&r.sources.every(id=>storefronts.sources[id]),'An observed detail has a source record');
 assert(r.limits,'Dimensions and capture-date limitations remain explicit');
}
for(const r of storefronts.frontages){
 const b=byId.get(r.buildingId),p=b.businesses.find(p=>p.id===r.businessId);
 assert(p?.renderName&&p.street===r.street&&p.design,'Design reaches its supported business on the correct street');
 assert(Math.abs(p.design.panels.reduce((s,p)=>s+p[1],0)-1)<.00001);
 assert.equal(p.appearance.record,r.id);
}
const recipeHash=crypto.createHash('sha256');for(const name of data.storefrontDetailSummary.recipeFiles)recipeHash.update(fs.readFileSync(path.resolve(root,'../..',name)));
assert.equal(recipeHash.digest('hex'),data.storefrontDetailSummary.recipeHash,'Compile and rebuild after changing model recipes');
const corner=JSON.parse(fs.readFileSync(path.resolve(root,'../../model-source/first-and-seventh.json')));
const cornerHash=crypto.createHash('sha256');for(const name of data.storefrontDetailSummary.cornerRecipeFiles)cornerHash.update(fs.readFileSync(path.resolve(root,'../..',name)));
assert.equal(cornerHash.digest('hex'),data.storefrontDetailSummary.cornerRecipeHash,'Recompile and rebuild after editing the First & 7th kit');
assert.deepEqual(corner.buildings.map(b=>b.id).sort(),[241822226,241829631,248142331,248142404,248142707].sort(),'Bounded four-corner benchmark');
assert.equal(data.cornerDetailSummary.elevations,9);
assert.equal(data.cornerDetailSummary.streetViewVerified,false,'Photographic comparison must not claim inaccessible Street View verification');
for(const profile of corner.buildings){
 const b=byId.get(profile.id);assert(!b.core);assert.equal(b.cornerReconstruction.profile,profile.profile);
 assert.equal(b.renderHeight,profile.height,'Export uses the individually observed corner height');
 assert(profile.sources.length&&profile.sources.every(id=>corner.sources[id]));assert(profile.limits);
 for(const [street,spec] of Object.entries(profile.elevations)){
  const face=b.frontages.find(f=>f.street===street);assert(face);
  assert.deepEqual(b.facadeSpec.elevations[street].cornerSchedule,spec);
  assert.equal(spec.rows.length,profile.floors-1);
  for(const [bottom,height] of spec.rows)assert(bottom>=3.5&&bottom+height<profile.height,'Residential openings remain above shop signage and below the roof');
  for(let i=0;i<spec.bays.length;i++){
   const center=spec.bays[i]*face.length,width=spec.widths?.[i]||spec.width;
   assert(center-width/2>0&&center+width/2<face.length,'Individual windows fit the mapped elevation');
  }
 }
}
assert(byId.get(248142404).renderHeight<byId.get(248142331).renderHeight-3,'Saifee corner stays distinctly lower than 114 First');
const seventhNames=corner.buildings.flatMap(p=>byId.get(p.id).businesses).filter(b=>b.renderName).map(b=>b.name);
for(const name of ['E7 Deli & Cafe','Monkey Sushi','Saifee Hardware & Garden'])assert(seventhNames.includes(name),'Supported corner tenant: '+name);
for(const [tile,signature] of Object.entries(data.storefrontDetailSummary.tileSignatures)){
 const entry=data.tiles.find(t=>t.id===tile),buf=fs.readFileSync(path.join(root,entry.url));
 const gltf=JSON.parse(buf.subarray(20,20+buf.readUInt32LE(12)));
 assert.equal(entry.storefrontSignature,signature,'Stale storefront manifest: '+tile);
 assert.equal(gltf.asset.extras?.storefrontSignature,signature,'Stale storefront mesh: '+tile);
}
for(const p of data.storefrontObstacles){
 assert(!world.walkable(p.x,p.z),'Walking must not pass through observed seating or boards');
 for(const a of [-p.halfWidth,p.halfWidth])for(const b of [-p.halfDepth,p.halfDepth]){
  const x=p.x+p.rx*a-p.rz*b,z=p.z+p.rz*a+p.rx*b;
  assert(!world.roadAt(x,z),'Observed street object must stay on the sidewalk: '+p.record);
  assert(!world.buildingAt(x,z),'Observed street object must stay outside building: '+p.record);
 }
}
for(const name of ['RALPH\'S ITALIAN ICES','DANNY & COOP\'S'])assert.equal(data.buildings.flatMap(b=>b.businesses).filter(p=>p.renderName&&p.name===name).length,1,'One supported shop after identity correction');
console.log(JSON.stringify({blocks:10,tiles:data.tiles.length,mappedBuildings:data.buildings.length,photoObserved:data.referenceSummary.newObservedBuildings,municipalBuildings:municipal.features.length,restoredBuildings:corrections.addBuildings.length,namedPlaces,roadSamples,detailMeshMB:+(bytes/1048576).toFixed(2),detailTriangles:triangles,detailBuildings:data.detailSummary.buildings,streetObjects,largestMaterialBatchCount,validBoundaryDriving:true,validMapSpawns:true,parkDeadEnds:true},null,2));
