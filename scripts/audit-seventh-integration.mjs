// Offline ownership + local HTTP audit for EV-003. No publication or model export.
// Optional third argument: installed Vercel CLI chunk exporting require_dist
// for @vercel/routing-utils. No package download is performed.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {seventhHeaders,immutableCache,mutableCache} from './seventh-hosting.mjs';
const out=path.resolve(process.argv[2]||'model-source/east-village-ev003');
const origin=process.env.BOROUGH_INTEGRATION_ORIGIN||'http://127.0.0.1:5175';
const read=async p=>JSON.parse(await fs.readFile(p,'utf8'));
const hash=b=>createHash('sha256').update(b).digest('hex');
await fs.mkdir(out,{recursive:true});
const build=await read('dist/seventh/build.json');
const slice=await read('engine/first-seventh/assets/slice.json');
const manifest=await read('dist/seventh/'+build.areas.manifest);
const protectedIds=await read('model-source/east-village-ev000/protected.json');
const packets=await read('model-source/east-village-ev000/next-packets.json');
const geography=await read('dist/reconstruction/neighborhood.json');
const baseline=await read(path.join(out,'baseline.json'));
assert.deepEqual(slice.buildings.map(b=>b.id).sort((a,b)=>a-b),[...protectedIds.runtimeBuildingIds].sort((a,b)=>a-b));
const current=slice.buildings.map(b=>{
  const a=manifest.assets[b.id],old=baseline.areaManifest.assets[b.id];
  assert.deepEqual(a,old,'No ownership/model/bounds changes: '+b.id);
  return {id:b.id,runtimeOwner:a.owner,modelAndCollisionOwner:'Resident_'+b.id,sceneSha256:a.sha256,protectedFaces:protectedIds.faceIds.filter(f=>f.startsWith(b.id+':'))};
});
const faceOwners=new Map(),massOwners=new Map();
const future=packets.map(p=>{
  for(const id of p.massAndRoofOwners){assert(!massOwners.has(id));massOwners.set(id,p.id);}
  return {id:p.id,parent:p.parent,notImplemented:true,faces:p.faces.map(f=>{
    assert(!faceOwners.has(f.faceId));faceOwners.set(f.faceId,p.id);
    assert(!protectedIds.faceIds.includes(f.faceId));assert(!manifest.assets[f.buildingId]);
    const b=geography.buildings.find(b=>b.id===f.buildingId);
    assert.deepEqual(b.frontages[Number(f.faceId.split(':')[1])],f.sourceFace);
    assert(p.massAndRoofOwners.includes(f.buildingId));
    return {faceId:f.faceId,buildingId:f.buildingId,authoringOwner:p.id,geometryOwner:f.geometryOwner,
      engineFrontage:{...f.sourceFace,z:f.sourceFace.z-slice.originShift[2]}};
  })};
});
assert.equal(current.length,203);assert.equal(faceOwners.size,53);
const ownership={schema:1,scope:'Current reviewed slice and nine planned packets; no new runtime geometry',pack:build.files['index.pck'],current,future,
  contract:{runtime:'One compiled scene and collision owner per building; never one duplicate building per frontage.',authoring:'EV-000 exact face and mass owners stay authoritative. Runtime partitions cannot authorize edits.',
    initialGrowth:'P01 may add only its four buildings and observed faces through a bounded adapter, initially retained with existing context. Exact catalog/face assertions must extend by that explicit set; preserve current 203 hashes unless separately assigned.',
    newSpatialArea:'Before another releasable group: generalize readiness over explicit manifest groups; full visual AABB, car/camera/resize coverage, predictive requests, collision ownership and request cancellation must use the same group. No blind copies of global street/prop builders.',
    route:'Keep current origin shift; separately extend street/void/collision/address/minimap bounds only as needed by the assigned packet. Municipal roads are not automatically drivable.',
    gates:'Inspect every new business; rerun affected browser routes and measured startup/frame/resource budget after growth. The 12/191 proof does not establish full-area capacity.'},
  counts:{current:current.length,protectedFaces:protectedIds.faceIds.length,futurePackets:future.length,futureFaces:faceOwners.size,futureMassOwners:massOwners.size}};
await fs.writeFile(path.join(out,'spatial-ownership.json'),JSON.stringify(ownership,null,2)+'\n');
const configBytes=await fs.readFile('vercel.json'),config=JSON.parse(configBytes);
let transformed;
if(process.argv[3]){
  const module=await import(pathToFileURL(path.resolve(process.argv[3])));
  transformed={configSha256:hash(configBytes),compiler:'Installed Vercel CLI @vercel/routing-utils',...module.require_dist().getTransformedRoutes(config)};
  assert.equal(transformed.error,null);
  await fs.writeFile(path.join(out,'hosting-routes.json'),JSON.stringify(transformed,null,2)+'\n');
}else{
  transformed=await read(path.join(out,'hosting-routes.json'));
  assert.equal(transformed.configSha256,hash(configBytes),'Recompile changed config with installed Vercel routing-utils');
}
const cases=['/','/seventh/','/seventh/index.html','/index.html','/legacy.html','/seventh/build.json','/seventh/index.pck','/seventh/index.wasm',
  '/seventh/'+build.areas.manifest,...Object.values(manifest.assets).slice(0,2).map(a=>a.url)];
const results=[];
for(const url of cases){
  const expected=seventhHeaders(url),compiled={};
  for(const route of transformed.routes)if(route.headers&&new RegExp(route.src).test(url))Object.assign(compiled,route.headers);
  assert.equal(compiled['Cache-Control'],expected['Cache-Control'],'Host and dev cache policies agree: '+url);
  const response=await fetch(origin+url),body=Buffer.from(await response.arrayBuffer());
  assert.equal(response.status,200,url);assert.equal(response.headers.get('cache-control'),expected['Cache-Control']);
  if(expected['Content-Type'])assert.equal(response.headers.get('content-type'),expected['Content-Type']);
  const file=url==='/'||url==='/seventh/'?'seventh/index.html':url==='/index.html'?'legacy.html':url.slice(1);
  assert.equal(hash(body),hash(await fs.readFile('dist/'+file)),url);
  const head=await fetch(origin+url,{method:'HEAD'});assert.equal(head.status,200);assert.equal((await head.arrayBuffer()).byteLength,0);
  assert.equal(head.headers.get('content-length'),String(body.length));
  results.push({url,status:response.status,headers:Object.fromEntries(response.headers),bytes:body.length,sha256:hash(body),headPassed:true});
}
const missing='/seventh/areas/assets/'+'0'.repeat(64)+'.scn';
const absent=await fetch(origin+missing);assert.equal(absent.status,404);assert.equal(absent.headers.get('cache-control'),'no-store');
const invalid=['/seventh/areas/assets/unversioned.scn','/seventh/areas/assets/'+'a'.repeat(63)+'.scn','/seventh/areas/manifest-current.json'];
for(const url of invalid){assert.equal(seventhHeaders(url)['Cache-Control'],mutableCache);assert(!transformed.routes.some(r=>r.headers?.['Cache-Control']===immutableCache&&new RegExp(r.src).test(url)));}
assert.deepEqual(config.rewrites,[{source:'/',destination:'/seventh/index.html'},{source:'/index.html',destination:'/legacy.html'}]);
await assert.rejects(fs.access('dist/index.html'));
const report={date:new Date().toISOString(),build,origin,results,missing:{url:missing,status:404,cacheControl:absent.headers.get('cache-control')},invalidNamesRejected:invalid,
  limitations:'Compiled config and actual localhost HTTP checks. Production candidate headers/negative caching require a later authorized deployment check; prior live HEAD evidence is separate. No deployment or credentials used.'};
await fs.writeFile(path.join(out,'hosting.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({ownership:ownership.counts,httpCases:results.length,missing404:true,compiledConfig:true}));
