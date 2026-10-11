// Real keyboard traversal and perspective review. Start npm run dev and an
// isolated Chromium CDP browser on port 9222, then run:
// node scripts/review-first-stmarks-routes.mjs [output-directory]
// Pose commands set the start; W drives every route through normal physics.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';

const out=path.resolve(process.argv[2]||'renders/first-stmarks-08/routes');
const url=process.env.BOROUGH_REVIEW_URL||'http://127.0.0.1:5173/seventh/?review=1';
const build=JSON.parse(await fs.readFile(new URL('../dist/seventh/build.json',import.meta.url),'utf8'));
const buildHashes={sourceCommit:build.sourceCommit,geographySha256:build.geographySha256,
  files:Object.fromEntries(Object.entries(build.files||{}).map(([name,entry])=>[name,entry.sha256])),sources:build.sources||{}};
await fs.mkdir(out,{recursive:true});

const tab=await(await fetch('http://127.0.0.1:9222/json/new?about:blank',{method:'PUT'})).json();
const ws=new WebSocket(tab.webSocketDebuggerUrl),pending=new Map(),listeners=new Map();
let id=0,commandSequence=0;
await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
ws.onmessage=event=>{
  const message=JSON.parse(event.data);
  if(message.id){const request=pending.get(message.id);pending.delete(message.id);message.error?request?.reject(message.error):request?.resolve(message.result);}
  else for(const listener of listeners.get(message.method)||[])listener(message.params);
};
const on=(method,listener)=>listeners.set(method,[...(listeners.get(method)||[]),listener]);
const send=(method,params={})=>new Promise((resolve,reject)=>{
  const requestId=++id,timeout=setTimeout(()=>{pending.delete(requestId);reject(Error('CDP timeout: '+method));},45000);
  pending.set(requestId,{resolve:value=>{clearTimeout(timeout);resolve(value);},reject:error=>{clearTimeout(timeout);reject(error);}});
  ws.send(JSON.stringify({id:requestId,method,params}));
});
async function evaluate(expression){const result=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(result.exceptionDetails)throw Error(JSON.stringify(result.exceptionDetails));return result.result?.value;}
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function until(expression,timeout=120000){const start=Date.now();while(Date.now()-start<timeout){if(await evaluate(expression))return;await sleep(250);}throw Error('Timeout: '+expression);}
const keycodes={Enter:13};
async function key(value,down){await send('Input.dispatchKeyEvent',{type:down?'keyDown':'keyUp',key:value,code:value.length===1?'Key'+value.toUpperCase():value,windowsVirtualKeyCode:keycodes[value]||value.toUpperCase().charCodeAt(0)});}
async function tap(value){await key(value,true);await sleep(80);await key(value,false);await sleep(350);}
const stats=()=>evaluate('window.seventhStats');
async function command(value){const sequence=++commandSequence;await evaluate('window.seventhReviewCommand='+JSON.stringify({...value,sequence}));await until('window.seventhReviewAck==='+sequence,5000);await sleep(350);}

const viewsOnly=process.env.BOROUGH_REVIEW_VIEWS_ONLY==='1';
const report={date:new Date().toISOString(),viewsOnly,build,buildHashes,errors:[],failedRequests:[],routes:[],views:[]};
on('Runtime.exceptionThrown',e=>report.errors.push(e.exceptionDetails));
on('Runtime.consoleAPICalled',e=>{if(e.type==='error')report.errors.push(e.args.map(a=>a.value||a.description).join(' '));});
on('Network.responseReceived',e=>{if(e.response.status>=400)report.failedRequests.push([e.response.status,e.response.url]);});
async function screenshot(name){const r=await send('Page.captureScreenshot',{format:'png'});await fs.writeFile(path.join(out,name+'.png'),Buffer.from(r.data,'base64'));report.views.push({name,stats:await stats()});}
try{
 await send('Page.enable');await send('Runtime.enable');await send('Network.enable');
 await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
 await send('Emulation.setFocusEmulationEnabled',{enabled:true});await send('Page.bringToFront');
 await send('Page.navigate',{url});await until('window.seventhStats?.ready && document.getElementById("loading").hidden');
 assert.equal((await stats()).buildings,build.buildings);await tap('Enter');
 while((await stats()).camera!==0)await tap('c');
 for(let mood=0;mood<(viewsOnly?0:3);mood++){
  while((await stats()).weather!==mood)await tap('t');
  for(const [name,x,z,yaw,seconds,axis,limit,direction] of [
   ['stmarks-east',-235,-77.9,-Math.PI/2,35,0,225,1],
   ['stmarks-west',225,-77.9,Math.PI/2,35,0,-235,-1],
   ['first-north',0,2,0,12,2,-85,-1],
   ['first-south',0,-85,Math.PI,12,2,2,1],
   ['avenue-a-north',214,4,0,12,2,-85,-1],
   ['seventh-preserved-east',-235,0,-Math.PI/2,35,0,220,1],
  ]){
   await command({type:'pose',x,z,yaw});const before=await stats();
   const started=Date.now();let after;await key('w',true);
   // Capture the crossing in the browser's frame loop. A 250 ms host poll,
   // CDP round trip and extra coast can hit the terminal beyond Avenue A
   // after the assigned route is already complete (the barrier is x=239).
   try{after=await evaluate(`new Promise((resolve,reject)=>{const start=performance.now();function tick(){const s=window.seventhStats;if(s.position[${axis}] ${direction>0?'>':'<'} ${limit}){resolve(JSON.parse(JSON.stringify(s)));return;}if(performance.now()-start>${seconds*1000}){reject(Error('Route crossing timed out'));return;}requestAnimationFrame(tick);}tick();})`);}
   finally{await key('w',false);}
   report.routes.push({weather:mood,name,seconds:(Date.now()-started)/1000,start:before.position,end:after.position,contacts:after.collisions-before.collisions,measurement:'Browser-frame telemetry at endpoint crossing, before post-route coast.'});
   assert.equal(after.collisions,before.collisions,name+' must clear collision');
   assert(direction>0?after.position[axis]>limit:after.position[axis]<limit,name+' must traverse its full segment');
   console.log('ROUTE_PASS',mood,name,after.position);
   // Stop at the measured endpoint for a readable capture; this happens only
   // after the complete keyboard traversal and contact assertions above.
   await command({type:'pose',x:after.position[0],z:after.position[2],yaw});
   await screenshot(name+'-'+mood);
  }
 }
 while((await stats()).weather!==0)await tap('t');
 for(const [name,x,z,yaw] of [
  ['driving-first-north',0,-22,0],
  ['driving-stmarks-west-block',-155,-77.9,-Math.PI/2],
  ['driving-stmarks-east-block',70,-77.9,-Math.PI/2],
 ]){
  await command({type:'pose',x,z,yaw});await sleep(500);await screenshot(name);
 }
 // Actual perspective cameras for corner returns, the two exceptional masses,
 // basement entries, and the painted gap. This is visual evidence, not a fit.
 for(const [name,x,z,heading,pitch,fov] of [
  ['second-north-corner',-229,-77.9,65,15,90],
  ['second-south-corner',-224,-77.9,120,14,90],
  ['39-mansard',-178,-73,325,22,85],
  ['40half-setback',-201,-83,140,22,80],
  ['62-chapel',-110,-77.9,130,14,80],
  ['first-stmarks-intersection',-2,-76,45,10,100],
  ['101-stoop',84,-77.9,335,14,85],
  ['109-entry',117,-77.9,35,18,80],
  ['painted-gap',96,-77.9,180,0,83],
  ['avenue-a-north-corner',214,-77.9,305,12,95],
  ['avenue-a-south-corner',214,-77.9,240,12,95],
 ]){
  await command({type:'reference',x,z,height:2.5,heading:heading+29.076863530557524,pitch,fov});await screenshot(name);
 }
 report.complete=true;assert.equal(report.errors.length,0,JSON.stringify(report.errors));assert.equal(report.failedRequests.length,0);
}finally{await fs.writeFile(path.join(out,'routes.json'),JSON.stringify(report,null,2)+'\n');await fetch('http://127.0.0.1:9222/json/close/'+tab.id).catch(()=>{});ws.close();}
