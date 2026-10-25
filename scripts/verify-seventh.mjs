// Verify the exact shipped engine package, its sources and geographic provenance.
// Actual driving/rendering checks are separate: npm run seventh:review.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {packEntries} from './seventh-package.mjs';
import './verify-seventh-routing.mjs';
const root=fileURLToPath(new URL('../',import.meta.url));
const digest=b=>createHash('sha256').update(b).digest('hex');
const build=JSON.parse(await fs.readFile(path.join(root,'dist/seventh/build.json'),'utf8'));
for(const required of ['index.html','index.js','index.wasm','index.pck','credits.txt','godot-notices.txt','LICENSE.txt','DAMION-OFL.txt','INTER-OFL.txt','InterVariable.woff2','drivearound-logo.png'])assert(build.files[required],required);
for(const [name,record] of Object.entries(build.files)){
  assert(!path.isAbsolute(name)&&!name.split('/').includes('..')&&!name.includes('\\'),'Safe runtime path');
  const data=await fs.readFile(path.join(root,'dist/seventh',name));assert.equal(data.length,record.bytes,name);assert.equal(digest(data),record.sha256,name);
  assert(data.length<100*1024*1024,'Keep every required runtime file below the repository limit');
}
for(const [name,expected] of Object.entries(build.sources))assert.equal(digest(await fs.readFile(path.join(root,name))),expected,'Rebuild after editing '+name);
const wasm=await fs.readFile(path.join(root,'dist/seventh/index.wasm'));assert.equal(wasm.readUInt32LE(0),0x6d736100,'WASM magic');
const pack=await fs.readFile(path.join(root,'dist/seventh/index.pck'));assert.equal(pack.subarray(0,4).toString(),'GDPC','PCK magic');
assert(pack.length<100*1024*1024,'Keep the required pack below the repository file-size limit');
const slice=JSON.parse(await fs.readFile(path.join(root,'engine/first-seventh/assets/slice.json'),'utf8'));
const p02Ids=[248142657,248142658,248142659,248142660,248142713];
const p03Ids=[241822237];
const n01aIds=[247852689,247852690,247852691,247852697];
const n01aFaces=['247852689:0','247852690:0','247852691:1','247852697:0'];
const n01bIds=[247852684,247852685,247852686,247852687];
const n01bFaces=n01bIds.map(id=>id+':0');
const p01Ids=[241822211,241822278,241822304,241822337];
const e09block=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e09-block/schedule.json'),'utf8'));
const e09blockIds=e09block.elevations.map(r=>r.buildingId).sort((a,b)=>a-b);
const e09blockFaces=e09block.elevations.map(r=>r.faceId).sort();
const e09east=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e09-east/schedule.json'),'utf8'));
const e09eastIds=[...new Set(e09east.elevations.map(r=>r.buildingId))].sort((a,b)=>a-b);
const e09eastFaces=e09east.elevations.map(r=>r.faceId).sort();
const tenth=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e10-block/schedule.json'),'utf8'));
const tenthIds=[...new Set(tenth.elevations.map(r=>r.buildingId))].sort((a,b)=>a-b);
const tenthFaces=tenth.elevations.map(r=>r.faceId).sort();
const tenthEast=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e10-east/schedule.json'),'utf8'));
const tenthEastIds=[...new Set(tenthEast.elevations.map(r=>r.buildingId))].sort((a,b)=>a-b);
const tenthEastFaces=tenthEast.elevations.map(r=>r.faceId).sort();
const eleventh=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e11-block/schedule.json'),'utf8'));
const eleventhIds=[...new Set(eleventh.elevations.map(r=>r.buildingId))].sort((a,b)=>a-b);
const eleventhFaces=eleventh.elevations.map(r=>r.faceId).sort();
const core=JSON.parse(await fs.readFile(path.join(root,'engine/first-seventh/assets/protected-core.json'),'utf8'));
const runtimeEntries=[...slice.buildings,...core.buildingOwners,...core.sharedModels];
assert.equal(slice.buildings.length,374);assert.equal(new Set(slice.buildings.map(x=>x.id)).size,374);
assert.equal(core.buildingOwners.length,23);assert.equal(core.sharedModels.length,1);
assert.equal(build.buildings,397);assert.equal(build.modelScenes,398);
assert.equal(new Set(runtimeEntries.map(b=>b.id)).size,398,'Each model has one distinct owner');
assert.equal(digest(await fs.readFile(path.join(root,core.source))),core.sourceSha256,'Original core GLB unchanged');
assert.equal(digest(await fs.readFile(path.join(root,'engine/first-seventh/assets/protected-core.glb'))),core.convertedSha256);
assert.equal(slice.packetScope.id,'01-E11-21');assert.deepEqual(slice.packetScope.buildingIds,eleventhIds);
assert.equal(build.schema,2,'Area-aware export required');
assert.match(build.checkoutCommit,/^[a-f0-9]{40}$/,'Checkout commit separate from geographic baseline');
assert.match(build.areas.manifest,/^areas\/manifest-[a-f0-9]{64}\.json$/);
const areaBytes=await fs.readFile(path.join(root,'dist/seventh',build.areas.manifest));
assert.equal(digest(areaBytes),build.areas.sha256);
assert.equal(build.areas.manifest,`areas/manifest-${digest(areaBytes)}.json`);
assert.equal(digest(await fs.readFile(path.join(root,'engine/first-seventh/assets/area_manifest.json'))),digest(areaBytes));
const areas=JSON.parse(areaBytes);
assert.equal(areas.schema,1);assert.equal(areas.engine,'4.7.2');assert.equal(areas.release,build.areas.release);
assert.deepEqual(areas.originShift,slice.originShift);
assert.deepEqual(Object.keys(areas.assets).sort(),runtimeEntries.map(b=>String(b.id)).sort());
const west=[241833259,241833267,241833274,241833286,241833290,241833291,241833299,241833312,241833322,241845001,241845013,978475216].map(String);
assert.deepEqual([...areas.areas['EVP-WEST']].sort(),west.sort());
assert.equal(areas.areas['EVP-REST'].length,386);
const assigned=Object.values(areas.areas).flat();
assert.equal(new Set(assigned).size,398);assert.equal(assigned.length,398);
assert.deepEqual([...assigned].sort(),Object.keys(areas.assets).sort());
for(const b of runtimeEntries){
  const asset=areas.assets[String(b.id)];assert.equal(asset.id,b.id);assert.equal(asset.glbSha256,b.sha256);
  assert(areas.areas[asset.owner]?.includes(String(b.id)),'Each building has one runtime owner');
  assert.equal(asset.url,`/seventh/areas/assets/${asset.sha256}.scn`);
  const file=asset.url.slice('/seventh/'.length);assert(build.files[file]);
  assert.equal(asset.bytes,build.files[file].bytes);assert.equal(asset.sha256,build.files[file].sha256);
  assert(asset.bytes>0&&asset.bytes<=([247852693,248142953].includes(b.id)?16:8)*1024*1024,'Bounded serialized scene');
  assert.equal(asset.bounds.length,6);assert(asset.bounds.every(Number.isFinite));
  for(let axis=0;axis<3;axis++)assert(asset.bounds[axis]<asset.bounds[axis+3],'Nonempty imported visual bounds');
}
assert(pack.length<=24*1024*1024,'Shared pack including original core texture library');
const entries=packEntries(pack);
assert(!entries.some(e=>/building--?\d+\.glb/.test(e.name)),'No duplicated streamed building payload');
const embedded=entries.find(e=>e.name==='assets/area_manifest.json');assert(embedded);
assert.equal(digest(pack.subarray(embedded.start,embedded.start+embedded.bytes)),digest(areaBytes),'Base pack pins exact external manifest');
async function areaFiles(directory,prefix='areas/'){
 const result=[];for(const entry of await fs.readdir(directory,{withFileTypes:true})){
  if(entry.isDirectory())result.push(...await areaFiles(path.join(directory,entry.name),prefix+entry.name+'/'));
  else result.push(prefix+entry.name);
 }return result;
}
assert.deepEqual((await areaFiles(path.join(root,'dist/seventh/areas'))).sort(),Object.keys(build.files).filter(n=>n.startsWith('areas/')).sort(),'No stale or unverified area files');
const geography=JSON.parse(await fs.readFile(path.join(root,'dist/reconstruction/neighborhood.json'),'utf8'));
const expectedSeventh=geography.buildings.filter(b=>b.frontages.some(f=>f.street==='East 7th Street')).map(b=>b.id).sort((a,b)=>a-b);
assert.equal(expectedSeventh.length,82);
assert.deepEqual([...slice.seventhFrontages].sort((a,b)=>a-b),expectedSeventh,'Every mapped Seventh frontage is included');
assert.deepEqual(slice.reviewFrontages.map(b=>b.id).sort((a,b)=>a-b),expectedSeventh);
for(const frontage of slice.reviewFrontages){
  assert.equal(frontage.height,slice.buildings.find(b=>b.id===frontage.id).height,
    'Review height must match the actual exported model, including cached partial rebuilds: '+frontage.id);
}
const details=JSON.parse(await fs.readFile(path.join(root,'model-source/storefront-details.json'),'utf8'));
const scope=JSON.parse(await fs.readFile(path.join(root,'model-source/first-stmarks-scope-08.json'),'utf8'));
const street=details.firstStmarksEngine;
const expectedFaces=[...scope.frontages,...scope.cornerReturns].filter(f=>!f.protectedCorner).map(f=>f.faceId).sort();
assert.deepEqual(street.elevations.map(r=>r.faceId).sort(),expectedFaces,'Every editable confirmed face has a schedule');
assert.deepEqual(slice.streetReviewFrontages.map(r=>r.faceId).sort(),expectedFaces,'Every scheduled face can be reviewed');
const base=geography.buildings.filter(b=>!b.core&&((b.box[0]+b.box[2])/2>=-268&&(b.box[0]+b.box[2])/2<=77&&(b.box[1]+b.box[3])/2>=121&&(b.box[1]+b.box[3])/2<=283||b.frontages.some(f=>f.street==='East 7th Street'))).map(b=>b.id);
const expectedIds=[...new Set([...base,...scope.frontages.map(f=>f.buildingId),...scope.cornerReturns.map(f=>f.buildingId),...p01Ids,...p02Ids,...p03Ids,...n01aIds,...n01bIds,...e09blockIds,...e09eastIds,...tenthIds,...tenthEastIds,...eleventhIds])].sort((a,b)=>a-b);
assert.deepEqual(slice.buildings.map(b=>b.id).sort((a,b)=>a-b),expectedIds,'Bounded expansion preserves the entire previous slice');
const p01=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-p01/schedule.json'),'utf8'));
assert.deepEqual(p01.elevations.map(r=>r.buildingId).sort((a,b)=>a-b),p01Ids);
assert.deepEqual(slice.packetReviewFrontages.map(r=>r.faceId).sort(),[...[...p01Ids,...p02Ids].map(id=>id+':0'),'241822237:0','241822237:1',...n01aFaces,...n01bFaces,...e09blockFaces,...e09eastFaces,...tenthFaces,...tenthEastFaces,...eleventhFaces].sort());
assert.equal(p01.businesses.length,7);
for(const r of p01.elevations){
  const b=geography.buildings.find(b=>b.id===r.buildingId);
  assert.deepEqual(r.sourceFace,b.frontages[0],'Exact P01 mapped face');
  assert.equal(r.architecture.windows.length,r.buildingId===241822278?20:16,'Observed floor/bay count');
  assert.equal(r.architecture.doors.length,1,'Separate residential entrance');
  assert(!street.elevations.some(old=>old.buildingId===r.buildingId),'New packet cannot rewrite revision09');
  for(const shop of r.architecture.returnShops){
    assert(shop.design.detailP01&&shop.design.detail09.sourceIds.length,'Per-business detail and evidence');
    assert(Math.abs(shop.design.panels.reduce((sum,p)=>sum+p[1],0)-1)<1e-7);
  }
}
const protectedModels=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-p01/protected-models.json'),'utf8'));
assert.equal(protectedModels.models.length,203);
for(const b of protectedModels.models){
  assert.equal(slice.buildings.find(r=>r.id===b.id)?.sha256,b.glbSha256,'Preserve existing GLB '+b.id);
  assert.equal(areas.assets[String(b.id)]?.sha256,b.sceneSha256,'Preserve imported scene '+b.id);
}
const p02=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-p02/schedule.json'),'utf8'));
assert.deepEqual(p02.elevations.map(r=>r.buildingId).sort((a,b)=>a-b),p02Ids);
assert.equal(p02.businesses.length,5);assert.equal(p02.junctions.length,5);
assert.deepEqual(slice.packetScopes.map(p=>p.id),['P01','P02','P03','01-E09-21-N01A','01-E09-21-N01B','01-E09-21','01-E09-1A','01-E10-21','01-E10-1A','01-E11-21']);
for(const r of p02.elevations){
 const b=geography.buildings.find(b=>b.id===r.buildingId),model=slice.buildings.find(b=>b.id===r.buildingId);
 assert.deepEqual(r.sourceFace,b.frontages[0]);assert.deepEqual(model.footprint,b.p.map(p=>[p[0],p[1]-228]),'Keep irregular mapped footprint');
 assert.equal(model.height,b.height);assert.equal(r.architecture.windows.length,({248142657:6,248142658:9,248142659:9,248142660:6,248142713:12})[r.buildingId]);
 assert.equal(r.architecture.doors.length,r.buildingId===248142713?0:1);
 assert(r.architecture.observation.sources.length);assert.equal(r.architecture.returnShops.length,1);
 const shop=r.architecture.returnShops[0];assert(shop.design.detailP02);assert(Math.abs(shop.design.panels.reduce((s,p)=>s+p[1],0)-1)<1e-7);
 assert(!street.elevations.some(old=>old.buildingId===r.buildingId)&&!p01.elevations.some(old=>old.buildingId===r.buildingId));
}
assert.equal(p02.junctions.find(j=>j.northId===248142713).mappedStreetOffsetMetres,.503);
const p02Protected=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-p02/protected-models.json'),'utf8'));
assert.equal(p02Protected.models.length,207);
for(const b of p02Protected.models){assert.equal(slice.buildings.find(r=>r.id===b.id)?.sha256,b.glbSha256,'P02 preserves GLB '+b.id);assert.equal(areas.assets[String(b.id)]?.sha256,b.sceneSha256,'P02 preserves scene '+b.id);}
const p03=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-p03/schedule.json'),'utf8'));
assert.deepEqual(p03.elevations.map(r=>r.faceId).sort(),['241822237:0','241822237:1']);
assert.equal(p03.businesses.length,3);assert.equal(new Set(p03.businesses.map(b=>b.businessId)).size,2);
for(const r of p03.elevations){
 const b=geography.buildings.find(b=>b.id===r.buildingId),model=slice.buildings.find(b=>b.id===r.buildingId);
 assert.deepEqual(r.sourceFace,b.frontages[r.frontageIndex]);assert.deepEqual(model.footprint,b.p.map(p=>[p[0],p[1]-228]));
 assert.equal(model.height,b.height);assert.equal(r.architecture.windows.length,r.frontageIndex===1?16:10);
 assert.equal(r.architecture.doors.length,r.frontageIndex===1?0:1);
 for(const sh of r.architecture.returnShops){assert(sh.design.detailP03);assert(Math.abs(sh.design.panels.reduce((v,p)=>v+p[1],0)-1)<1e-7);}
}
assert.deepEqual(slice.packetScopes.find(p=>p.id==='P03').buildingIds,p03Ids);
assert.deepEqual(slice.packetScope.supportingRoad,{street:'First Avenue connection and Eleventh Second–First; existing Ninth and Tenth retained',northTerminal:-315.3,outerNorthLimit:-320.3,eleventhCenter:-304.3,eleventhWestTerminal:-213,eleventhEastTerminal:13,eleventhOuterWest:-217,eleventhOuterEast:17,tenthCenter:-228,tenthWestTerminal:-213,tenthEastTerminal:207,tenthOuterWest:-217,tenthOuterEast:211,corridorHalfWidth:17,ninthCenter:-154.7,ninthWestTerminal:-213,ninthOuterWest:-217,ninthEastTerminal:207,ninthOuterEast:211,addressPolicy:'Seventh-only HUD; First reaches Eleventh. Eleventh reaches Second and ends at First; Ninth and Tenth retained, other avenue terminals unchanged.'});
const p03Protected=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-p03/protected-models.json'),'utf8'));
assert.equal(p03Protected.models.length,212);
for(const b of p03Protected.models.filter(r=>r.id!==248142713)){assert.equal(slice.buildings.find(r=>r.id===b.id)?.sha256,b.glbSha256,'P03 preserves GLB '+b.id);assert.equal(areas.assets[String(b.id)]?.sha256,b.sceneSha256,'P03 preserves scene '+b.id);}
const n01a=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e09-n01a/schedule.json'),'utf8'));
assert.deepEqual(n01a.elevations.map(r=>r.faceId).sort(),n01aFaces);
assert.equal(n01a.businesses.length,5);assert.equal(new Set(n01a.businesses.map(b=>b.businessId)).size,4);
for(const r of n01a.elevations){
 const b=geography.buildings.find(b=>b.id===r.buildingId),model=slice.buildings.find(b=>b.id===r.buildingId);
 assert.deepEqual(r.sourceFace,b.frontages[r.frontageIndex]);assert.equal(model.height,b.height);
 assert.deepEqual(model.footprint,b.p.map(p=>[p[0],p[1]-228]));
 assert.equal(r.architecture.windows.length,({247852691:21,247852690:12,247852697:14,247852689:19})[r.buildingId]);
 assert(r.architecture.observation.sources.length);
 for(const sh of r.architecture.returnShops){assert(sh.design.detailN01A);assert(Math.abs(sh.design.panels.reduce((v,p)=>v+p[1],0)-1)<1e-7);}
}
const n01aProtected=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e09-n01a/protected-models.json'),'utf8'));
assert.equal(n01aProtected.models.length,213);
for(const b of n01aProtected.models.filter(r=>r.id!==248142713)){assert.equal(slice.buildings.find(r=>r.id===b.id)?.sha256,b.glbSha256,'N01A preserves GLB '+b.id);assert.equal(areas.assets[String(b.id)]?.sha256,b.sceneSha256,'N01A preserves scene '+b.id);}
assert(slice.groundVoids.some(v=>v.faceId==='247852697:0'),'343 observed basement cut');

const n01b=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e09-n01b/schedule.json'),'utf8'));
assert.deepEqual(n01b.elevations.map(r=>r.faceId).sort(),n01bFaces);assert.equal(n01b.businesses.length,6);
for(const r of n01b.elevations){
 const b=geography.buildings.find(b=>b.id===r.buildingId),model=slice.buildings.find(b=>b.id===r.buildingId);
 assert.deepEqual(r.sourceFace,b.frontages[0]);assert.deepEqual(model.footprint,b.p.map(p=>[p[0],p[1]-228]));
 assert.equal(model.height,r.buildingHeight);assert.equal(r.sourceHeight,b.height);
 assert.equal(r.architecture.windows.length,r.buildingId===247852687?22:16);
 assert.equal(r.architecture.doors.length,1);assert(r.architecture.observation.sources.length);
 for(const sh of r.architecture.returnShops){assert(sh.design.detailN01B);assert(Math.abs(sh.design.panels.reduce((v,p)=>v+p[1],0)-1)<1e-7);}
}
assert.equal(n01b.elevations.find(r=>r.buildingId===247852686).buildingHeight,15.9);
assert(slice.groundVoids.some(v=>v.faceId==='247852687:0'));
const n01bProtected=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e09-n01b/protected-models.json'),'utf8'));
assert.equal(n01bProtected.models.length,217);
for(const b of n01bProtected.models.filter(r=>r.id!==248142713)){assert.equal(slice.buildings.find(r=>r.id===b.id)?.sha256,b.glbSha256,'N01B preserves GLB '+b.id);assert.equal(areas.assets[String(b.id)]?.sha256,b.sceneSha256,'N01B preserves scene '+b.id);}

const blockInventory=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e09-block/inventory.json'),'utf8'));
assert.deepEqual(e09blockFaces,[...blockInventory.scope.editableRemainingFaceIds].sort());
assert.equal(e09blockIds.length,34);assert.equal(new Set(e09blockIds).size,34);
for(const r of e09block.elevations){
 const b=geography.buildings.find(b=>b.id===r.buildingId), model=slice.buildings.find(b=>b.id===r.buildingId);
 assert.deepEqual(r.sourceFace,b.frontages[r.frontageIndex]);
 assert.deepEqual(model.footprint,b.p.map(p=>[p[0],p[1]-228]),'Keep mapped polygon '+r.faceId);
 assert.equal(model.height,r.buildingHeight);assert.equal(r.sourceHeight,b.height);
 assert(r.architecture.observation.sources.length,'Inspected source '+r.faceId);
 for(const sh of r.architecture.returnShops){assert(sh.design.detailE09Block);assert(sh.design.detail09.identity);assert(Math.abs(sh.design.panels.reduce((v,p)=>v+p[1],0)-1)<1e-7);}
 for(const well of r.architecture.observedGround.basementAreaways||[])assert(slice.groundVoids.some(v=>v.faceId===r.faceId&&Math.abs(v.worldWidth-well.width*r.sourceFace.length)<.001));
}
const blockProtected=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e09-block/protected-models.json'),'utf8'));
assert.equal(blockProtected.models.length,221);
for(const b of blockProtected.models.filter(r=>r.id!==248142713)){assert(!e09blockIds.includes(b.id));assert.equal(slice.buildings.find(r=>r.id===b.id)?.sha256,b.glbSha256,'Block preserves GLB '+b.id);assert.equal(areas.assets[String(b.id)]?.sha256,b.sceneSha256,'Block preserves SCN '+b.id);}


const eastInventory=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e09-east/inventory.json'),'utf8'));
assert.equal(e09eastIds.length,41);assert.equal(e09eastFaces.length,50);
assert.deepEqual(e09eastFaces,eastInventory.faces.map(r=>r.faceId).sort());
for(const r of e09east.elevations){
 const b=geography.buildings.find(b=>b.id===r.buildingId),model=slice.buildings.find(b=>b.id===r.buildingId);
 assert.deepEqual(r.sourceFace,b.frontages[r.frontageIndex]);assert.equal(model.height,r.buildingHeight);
 assert.deepEqual(model.footprint,b.p.map(p=>[p[0],p[1]-228]));assert(r.architecture.observation.sources.length);
 for(const sh of r.architecture.returnShops){assert(sh.design.detailE09East);assert(sh.design.detail09.identity);assert(Math.abs(sh.design.panels.reduce((v,p)=>v+p[1],0)-1)<1e-7);}
 for(const well of r.architecture.observedGround.basementAreaways||[])assert(slice.groundVoids.some(v=>v.faceId===r.faceId&&Math.abs(v.worldWidth-well.width*r.sourceFace.length)<.001));
}
const eastProtected=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e09-east/protected-models.json'),'utf8'));
assert.equal(eastProtected.models.length,255);
for(const b of eastProtected.models.filter(r=>r.id!==248142713)){assert.equal(slice.buildings.find(r=>r.id===b.id)?.sha256,b.glbSha256,'East block preserves GLB '+b.id);assert.equal(areas.assets[String(b.id)]?.sha256,b.sceneSha256,'East block preserves SCN '+b.id);}
assert.deepEqual(e09east.elevations.filter(r=>r.buildingId===248142713).map(r=>r.faceId),['248142713:1']);
assert.equal(slice.auxiliaryFootprints.length,1);assert.equal(slice.auxiliaryFootprints[0].owner,248142716);assert.equal(slice.auxiliaryFootprints[0].height,3.25);

const tenthInventory=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e10-block/inventory.json'),'utf8'));
assert.equal(tenthIds.length,27);assert.equal(tenthFaces.length,29);
assert.deepEqual(tenthFaces,tenthInventory.faces.map(r=>r.faceId).sort());
for(const r of tenth.elevations){
 const b=geography.buildings.find(b=>b.id===r.buildingId);
 assert.deepEqual(r.sourceFace,b.frontages[r.frontageIndex]);
 assert(!b.core,'Protected core cannot enter ordinary facade generator');
 assert(r.architecture.observation.sources.length);
 for(const shop of r.architecture.returnShops){assert(shop.design.detailE10Block&&shop.design.detail09.identity);assert(Math.abs(shop.design.panels.reduce((v,p)=>v+p[1],0)-1)<1e-7);}
}
const tenthProtected=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e10-block/protected-models.json'),'utf8'));
assert.equal(tenthProtected.models.length,295);
for(const b of tenthProtected.models){assert.equal(slice.buildings.find(r=>r.id===b.id)?.sha256,b.glbSha256);assert.equal(areas.assets[String(b.id)]?.sha256,b.sceneSha256);}
const tenthEastInventory=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e10-east/inventory.json'),'utf8'));
assert.equal(tenthEastIds.length,30);assert.equal(tenthEastFaces.length,36);
assert.deepEqual(tenthEastFaces,tenthEastInventory.faces.map(r=>r.faceId).sort());
for(const r of tenthEast.elevations){
 const b=geography.buildings.find(b=>b.id===r.buildingId);
 assert.deepEqual(r.sourceFace,b.frontages[r.frontageIndex]);assert(!b.core);assert(r.architecture.observation.sources.length);
 for(const sh of r.architecture.returnShops){assert(sh.design.detailE10East&&sh.design.detail09.identity);assert(Math.abs(sh.design.panels.reduce((v,p)=>v+p[1],0)-1)<1e-7);}
}
const tenthEastProtected=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e10-east/protected-models.json'),'utf8'));
assert.equal(tenthEastProtected.models.length,322);
for(const b of tenthEastProtected.models){assert.equal(slice.buildings.find(r=>r.id===b.id)?.sha256,b.glbSha256,'Tenth east preserves GLB '+b.id);assert.equal(areas.assets[String(b.id)]?.sha256,b.sceneSha256,'Tenth east preserves SCN '+b.id);}
assert.equal(Object.keys(tenthEastProtected.coreAssets).length,24);
for(const [id,hash] of Object.entries(tenthEastProtected.coreAssets))assert.equal(areas.assets[id]?.sha256,hash,'Protected core scene '+id);
const imageIndex=JSON.parse(await fs.readFile(path.join(root,'engine/first-seventh/assets/protected-core-textures.json'),'utf8'));
const imageBytes=await fs.readFile(path.join(root,'engine/first-seventh/assets/protected-core-textures.bin'));
assert.equal(digest(imageBytes),imageIndex.sha256);assert.equal(imageIndex.images.length,9);
for(const row of imageIndex.images)assert.equal(digest(imageBytes.subarray(row.offset,row.offset+row.length)),row.sha256);
assert(build.files['NOTOSANSJP-OFL.txt']);
assert(!entries.some(e=>e.name==='assets/protected-core.glb'),'Core geometry stays external');
const encoded=entries.find(e=>e.name==='assets/protected-core-textures.bin');assert(encoded);
assert.equal(digest(pack.subarray(encoded.start,encoded.start+encoded.bytes)),imageIndex.sha256);

for(const r of street.elevations){
 const b=geography.buildings.find(b=>b.id===r.buildingId);
 assert.deepEqual(r.sourceFace,b.frontages[r.frontageIndex],'Stable mapped frontage '+r.faceId);
 assert(r.architecture.observation.sources.length,'Dated source required '+r.faceId);
 assert(![241822226,241829631,248142331,248142404,248142707].includes(r.buildingId));
 assert.notEqual(r.sourceFace.street,'East 7th Street');
}
const schedule=details.seventhEngine;
assert.deepEqual(schedule.elevations.map(b=>b.buildingId).sort((a,b)=>a-b),expectedSeventh);
assert.equal(digest(await fs.readFile(path.join(root,'model-source/storefront-details.json'))),slice.detailSourceSha256);
for(const [name,expected] of Object.entries(slice.recipeHashes))assert.equal(digest(await fs.readFile(path.join(root,name))),expected,'Stale model recipe '+name);
for(const r of [...schedule.elevations,...schedule.frontages]){
  assert(r.sources.length,'Missing source '+r.id);
  for(const id of r.sources)assert(schedule.sources[id],'Missing source record '+id);
}
for(const r of schedule.frontages){
  const b=geography.buildings.find(b=>b.id===r.buildingId),shop=b.businesses.find(s=>s.id===r.businessId);
  const elevation=schedule.elevations.find(e=>e.buildingId===r.buildingId);
  const override=elevation.businessOverrides?.find(o=>o.id===r.businessId);
  if(override){
    assert.equal(override.renderName,true,'Explicit shop activation');
    assert(override.sources?.length,'An engine-only identity change needs its own evidence');
    for(const source of override.sources)assert(schedule.sources[source],'Missing identity source '+source);
  }
  assert(shop && (shop.renderName||override?.renderName) && shop.street==='East 7th Street','Keep mapped shop identity and explicit activation provenance');
  assert(r.span[0]>=0&&r.span[1]<=1&&r.span[0]<r.span[1]);
  assert(Math.abs(r.design.panels.reduce((n,p)=>n+p[1],0)-1)<1e-5);
}
for(const id of [241822226,248142707,241829631,248142331,248142404])assert(slice.buildings.some(x=>x.id===id),'Corner building '+id);
assert.equal(digest(await fs.readFile(path.join(root,'dist/reconstruction/neighborhood.json'))),build.geographySha256);
assert.equal(slice.sourceSha256,build.geographySha256);
const html=await fs.readFile(path.join(root,'dist/seventh/index.html'),'utf8');assert(!html.includes('$GODOT_'),'Unexpanded shell placeholders');
const shellPack=JSON.parse(html.match(/const packRelease = (\{[^\n]+\});/)[1]);
assert.deepEqual(shellPack,{bytes:pack.length,sha256:digest(pack)},'Shell pins its exact pack before startup');
assert(html.includes('"canvasResizePolicy":0'),'CSS-pixel rendering');assert(html.includes('const threaded = false'),'No GPU server or cross-origin threads required');
assert(!/<script[^>]+src=["']https?:/.test(html),'Runtime scripts must be local');

const eleventhInventory=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e11-block/inventory.json'),'utf8'));
assert.equal(eleventhIds.length,22);assert.equal(eleventhFaces.length,26);
assert.deepEqual(eleventhFaces,eleventhInventory.faces.map(r=>r.faceId).sort());
for(const r of eleventh.elevations){
 const b=geography.buildings.find(b=>b.id===r.buildingId),m=slice.buildings.find(b=>b.id===r.buildingId);
 assert.deepEqual(r.sourceFace,b.frontages[r.frontageIndex]);assert.equal(m.height,r.buildingHeight);
 assert.deepEqual(m.footprint,b.p.map(p=>[p[0],p[1]-228]));assert(r.architecture.observation.sources.length);
 for(const sh of r.architecture.returnShops){assert(sh.design.detailE11Block&&sh.design.detail09.identity);assert(Math.abs(sh.design.panels.reduce((v,p)=>v+p[1],0)-1)<1e-7);}
}
const eleventhProtected=JSON.parse(await fs.readFile(path.join(root,'model-source/east-village-e11-block/protected-models.json'),'utf8'));
assert.equal(eleventhProtected.models.length,352);
for(const b of eleventhProtected.models){assert.equal(slice.buildings.find(r=>r.id===b.id)?.sha256,b.glbSha256,'Eleventh preserves GLB '+b.id);assert.equal(areas.assets[String(b.id)]?.sha256,b.sceneSha256,'Eleventh preserves SCN '+b.id);}
assert.equal(Object.keys(eleventhProtected.coreAssets).length,24);
for(const [id,hash] of Object.entries(eleventhProtected.coreAssets))assert.equal(areas.assets[id]?.sha256,hash,'Protected core scene '+id);

console.log(`Verified slice: ${Object.keys(build.files).length} runtime files, ${Object.keys(build.sources).length} source hashes; 397 buildings / 398 model scenes; all352 preceding model pairs and24 core scenes preserved;26 Eleventh planes. Visual/performance review separate.`);
