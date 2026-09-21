// Verify the exact shipped engine package, its sources and geographic provenance.
// Actual driving/rendering checks are separate: npm run seventh:review.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const root=fileURLToPath(new URL('../',import.meta.url));
const digest=b=>createHash('sha256').update(b).digest('hex');
const build=JSON.parse(await fs.readFile(path.join(root,'dist/seventh/build.json'),'utf8'));
for(const required of ['index.html','index.js','index.wasm','index.pck','credits.txt','godot-notices.txt','LICENSE.txt','DAMION-OFL.txt','INTER-OFL.txt','InterVariable.woff2','drivearound-logo.png'])assert(build.files[required],required);
for(const [name,record] of Object.entries(build.files)){
  const data=await fs.readFile(path.join(root,'dist/seventh',name));assert.equal(data.length,record.bytes,name);assert.equal(digest(data),record.sha256,name);
}
for(const [name,expected] of Object.entries(build.sources))assert.equal(digest(await fs.readFile(path.join(root,name))),expected,'Rebuild after editing '+name);
const wasm=await fs.readFile(path.join(root,'dist/seventh/index.wasm'));assert.equal(wasm.readUInt32LE(0),0x6d736100,'WASM magic');
const pack=await fs.readFile(path.join(root,'dist/seventh/index.pck'));assert.equal(pack.subarray(0,4).toString(),'GDPC','PCK magic');
assert(pack.length<100*1024*1024,'Keep the required pack below the repository file-size limit');
const slice=JSON.parse(await fs.readFile(path.join(root,'engine/first-seventh/assets/slice.json'),'utf8'));
assert.equal(slice.buildings.length,182);assert.equal(new Set(slice.buildings.map(x=>x.id)).size,182);
const geography=JSON.parse(await fs.readFile(path.join(root,'dist/reconstruction/neighborhood.json'),'utf8'));
const expectedSeventh=geography.buildings.filter(b=>b.frontages.some(f=>f.street==='East 7th Street')).map(b=>b.id).sort((a,b)=>a-b);
assert.equal(expectedSeventh.length,82);
assert.deepEqual([...slice.seventhFrontages].sort((a,b)=>a-b),expectedSeventh,'Every mapped Seventh frontage is included');
assert.deepEqual(slice.reviewFrontages.map(b=>b.id).sort((a,b)=>a-b),expectedSeventh);
const details=JSON.parse(await fs.readFile(path.join(root,'model-source/storefront-details.json'),'utf8'));
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
  assert(shop.renderName&&shop.street==='East 7th Street','Keep shop identity provenance');
  assert(r.span[0]>=0&&r.span[1]<=1&&r.span[0]<r.span[1]);
  assert(Math.abs(r.design.panels.reduce((n,p)=>n+p[1],0)-1)<1e-5);
}
for(const id of [241822226,248142707,241829631,248142331,248142404])assert(slice.buildings.some(x=>x.id===id),'Corner building '+id);
assert.equal(digest(await fs.readFile(path.join(root,'dist/reconstruction/neighborhood.json'))),build.geographySha256);
assert.equal(slice.sourceSha256,build.geographySha256);
const html=await fs.readFile(path.join(root,'dist/seventh/index.html'),'utf8');assert(!html.includes('$GODOT_'),'Unexpanded shell placeholders');
assert(html.includes('"canvasResizePolicy":0'),'CSS-pixel rendering');assert(html.includes('const threaded = false'),'No GPU server or cross-origin threads required');
assert(!/<script[^>]+src=["']https?:/.test(html),'Runtime scripts must be local');
console.log(`Verified Seventh: ${Object.keys(build.files).length} package files, ${Object.keys(build.sources).length} source hashes, 182 buildings, all 82 Seventh frontages and original geography.`);
await import('./verify-seventh-architecture.mjs');
