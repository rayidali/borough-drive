import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {reviewClient,delay} from './browser-review-client.mjs';
const out=path.resolve(process.argv[2]||'model-source/browser-scale-2026-10-25/smoke-01');
const mode=process.argv[3]||'smoke';
const url=process.env.BOROUGH_REVIEW_URL||'http://127.0.0.1:5181/seventh/?review=1';
await fs.mkdir(out,{recursive:true});
const build=JSON.parse(await fs.readFile('dist/seventh/build.json','utf8'));
const report={date:new Date().toISOString(),url,build,mode,errors:[],warnings:[],failedRequests:[],views:[]};
const c=await reviewClient();
c.on('Runtime.exceptionThrown',e=>report.errors.push(e.exceptionDetails));
c.on('Runtime.consoleAPICalled',e=>{if(['error','warning'].includes(e.type))report[e.type==='error'?'errors':'warnings'].push(e.args.map(a=>a.value||a.description||'').join(' '));});
c.on('Network.responseReceived',e=>{if(e.response.status>=400)report.failedRequests.push([e.response.status,e.response.url]);});
async function shot(name){await c.shot(path.join(out,name+'.png'));report.views.push({name,stats:await c.stats()});}
try{
 report.startup=await c.open(url);
 console.log('STARTUP',JSON.stringify(report.startup));
 await c.tap('Enter');await c.until('seventhStats.started');
 while((await c.stats()).weather!==0)await c.tap('t');
 while((await c.stats()).camera!==0)await c.tap('c');
 await c.until('!seventhStats.streaming.cameraHeld && !seventhStats.streaming.held');
 await delay(1500);await shot('seventh-start');
 report.initial=await c.dump();
 assert.equal(report.initial.catalogCount,build.modelScenes);
 assert(report.initial.initialResidentCount<build.modelScenes);
 for(const [name,x,z,yaw] of [['seventh-west',-260,0,-Math.PI/2],['ninth',0,-154.7,0],['tenth-east',155,-228,Math.PI/2],['eleventh',-115,-304.3,Math.PI/2]]){
  await c.command({type:'pose',x,z,yaw});await delay(1200);await shot(name);
 }
 await delay(10000);report.remote=await c.dump();
 await c.tap('r');await c.until('!seventhStats.streaming.cameraHeld && Math.abs(seventhStats.position[2]-8)<.3');await delay(10000);report.reset=await c.dump();await shot('seventh-return');
 assert(report.reset.retirements>0,'Distant assets must retire');
 assert(report.reset.residentCount<report.reset.catalogCount,'Residency must be local');
 for(const record of [report.initial,report.remote,report.reset]){
  assert(record.maxReservedBytes<=32*1024*1024);
  assert.equal(Object.keys(record.treeOwners).length,record.residentCount);
  for(const o of Object.values(record.treeOwners)){assert(o.model);assert.equal(o.collision,o.kind!=='protected-core-details');}
 }
 assert.equal(report.errors.length,0,JSON.stringify(report.errors));assert.equal(report.failedRequests.length,0);
 report.complete=true;console.log('BROWSER_SCALE_PASS',JSON.stringify({readyMs:report.startup.readyMs,initial:report.initial.residentCount,remote:report.remote.residentCount,reset:report.reset.residentCount,retirements:report.reset.retirements}));
}finally{await fs.writeFile(path.join(out,'review.json'),JSON.stringify(report,null,2)+'\n');await c.close();}
