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
for(const required of ['index.html','index.js','index.wasm','index.pck','credits.txt','godot-notices.txt','LICENSE.txt','DAMION-OFL.txt'])assert(build.files[required],required);
for(const [name,record] of Object.entries(build.files)){
  const data=await fs.readFile(path.join(root,'dist/seventh',name));assert.equal(data.length,record.bytes,name);assert.equal(digest(data),record.sha256,name);
}
for(const [name,expected] of Object.entries(build.sources))assert.equal(digest(await fs.readFile(path.join(root,name))),expected,'Rebuild after editing '+name);
const wasm=await fs.readFile(path.join(root,'dist/seventh/index.wasm'));assert.equal(wasm.readUInt32LE(0),0x6d736100,'WASM magic');
const pack=await fs.readFile(path.join(root,'dist/seventh/index.pck'));assert.equal(pack.subarray(0,4).toString(),'GDPC','PCK magic');
const slice=JSON.parse(await fs.readFile(path.join(root,'engine/first-seventh/assets/slice.json'),'utf8'));
assert.equal(slice.buildings.length,154);assert.equal(new Set(slice.buildings.map(x=>x.id)).size,154);
for(const id of [241822226,248142707,241829631,248142331,248142404])assert(slice.buildings.some(x=>x.id===id),'Corner building '+id);
assert.equal(digest(await fs.readFile(path.join(root,'dist/reconstruction/neighborhood.json'))),build.geographySha256);
assert.equal(slice.sourceSha256,build.geographySha256);
const html=await fs.readFile(path.join(root,'dist/seventh/index.html'),'utf8');assert(!html.includes('$GODOT_'),'Unexpanded shell placeholders');
assert(html.includes('"canvasResizePolicy":0'),'CSS-pixel rendering');assert(html.includes('const threaded = false'),'No GPU server or cross-origin threads required');
assert(!/<script[^>]+src=["']https?:/.test(html),'Runtime scripts must be local');
console.log(`Verified Seventh: ${Object.keys(build.files).length} package files, ${Object.keys(build.sources).length} source hashes, 154 buildings and original geography.`);
