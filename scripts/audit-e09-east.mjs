// Local final-block hosting/preservation evidence. No publication or credentials.
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {seventhHeaders} from './seventh-hosting.mjs';
const out='model-source/east-village-e09-east';
const origin=process.env.BOROUGH_INTEGRATION_ORIGIN||'http://127.0.0.1:5181';
const hash=b=>createHash('sha256').update(b).digest('hex');
const read=async p=>JSON.parse(await fs.readFile(p,'utf8'));
const build=await read('dist/seventh/build.json');
const baseline=await read(out+'/baseline.json');
const report={date:new Date().toISOString(),origin,build,routes:[],runtime:[],privateImages:[],preservedTracked:[],changedTracked:[],limits:'Local HTTP and file checks only; no production/CDN recheck or publication.'};
for(const [file,expected] of Object.entries(baseline.privateImages)){
 const actual=hash(await fs.readFile(file));assert.equal(actual,expected,file);report.privateImages.push({file,sha256:actual});
}
for(const [file,expected] of Object.entries(baseline.trackedHashes)){
 const actual=hash(await fs.readFile(file));(actual===expected?report.preservedTracked:report.changedTracked).push(file);
}
const allowed=new Set(['dist/seventh/build.json','dist/seventh/index.html','dist/seventh/index.pck','engine/first-seventh/assets/slice.json','engine/first-seventh/scripts/minimap.gd','engine/first-seventh/scripts/world.gd','model-source/export_seventh_engine.py','scripts/export-seventh.mjs','scripts/verify-seventh.mjs']);
for(const file of report.changedTracked)assert(file.endsWith('.md')||allowed.has(file),'Unexpected tracked change: '+file);
for(const [url,file] of [['/','seventh/index.html'],['/seventh/','seventh/index.html'],['/index.html','legacy.html'],['/legacy.html','legacy.html']]){
 const response=await fetch(origin+url),body=Buffer.from(await response.arrayBuffer());assert.equal(response.status,200);
 const sha256=hash(body);assert.equal(sha256,hash(await fs.readFile('dist/'+file)));
 assert.equal(response.headers.get('cache-control'),seventhHeaders(url)['Cache-Control']);report.routes.push({url,sha256,bytes:body.length});
}
for(const [file,expected] of Object.entries(build.files)){
 const url='/seventh/'+file,response=await fetch(origin+url),body=Buffer.from(await response.arrayBuffer());assert.equal(response.status,200,url);
 assert.equal(body.length,expected.bytes,url);assert.equal(hash(body),expected.sha256,url);
 assert.equal(response.headers.get('cache-control'),seventhHeaders(url)['Cache-Control'],url);
 report.runtime.push({file,bytes:body.length,sha256:hash(body)});
}
const absent=await fetch(origin+'/seventh/areas/assets/'+'0'.repeat(64)+'.scn');assert.equal(absent.status,404);assert.equal(absent.headers.get('cache-control'),'no-store');
await assert.rejects(fs.access('dist/index.html'));report.complete=true;report.missingScene404NoStore=true;
await fs.writeFile(out+'/hosting-preservation.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({routes:report.routes.length,runtime:report.runtime.length,privateImages:report.privateImages.length,preservedTracked:report.preservedTracked.length,changedTracked:report.changedTracked,complete:true}));
