// Run from repository root: BOROUGH_REVIEW_URL=https://www.drivearound.nyc/?review=1 node model-source/publication-review-09/smoke-harness.mjs output-directory
// Real browser controls and rendering review. Start npm run dev and an isolated
// Chromium browser with --remote-debugging-port=9222, then npm run seventh:review.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const out = path.resolve(process.argv[2] || 'renders/seventh-engine/browser-review');
// Resume the independent settings/recovery checks after a completed driving
// pass; retain the earlier report rather than rerunning its long route loop.
const recoveryOnly = process.argv.includes('--recovery-only');
const url = process.env.BOROUGH_REVIEW_URL || 'http://127.0.0.1:5173/seventh/?review=1';
await fs.mkdir(out, {recursive:true});
const tab = await (await fetch('http://127.0.0.1:9222/json/new?about:blank', {method:'PUT'})).json();
const ws = new WebSocket(tab.webSocketDebuggerUrl), pending = new Map(), listeners = new Map();
let id = 0;
await new Promise((resolve,reject) => {ws.onopen=resolve;ws.onerror=reject;});
ws.onmessage = event => {
  const m=JSON.parse(event.data);
  if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p?.reject(m.error):p?.resolve(m.result);}
  else for(const f of listeners.get(m.method)||[]) f(m.params);
};
const on=(name,fn)=>listeners.set(name,[...(listeners.get(name)||[]),fn]);
const send=(method,params={})=>new Promise((resolve,reject)=>{const n=++id;const timer=setTimeout(()=>{pending.delete(n);reject(Error('CDP timeout: '+method));},30000);pending.set(n,{resolve:value=>{clearTimeout(timer);resolve(value);},reject:error=>{clearTimeout(timer);reject(error);}});ws.send(JSON.stringify({id:n,method,params}));});
async function evaluate(expression){const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result?.value;}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function until(expression,timeout=120000){const t=Date.now();while(Date.now()-t<timeout){if(await evaluate(expression))return;await sleep(250);}throw Error('Timeout: '+expression);}
const keycodes={Enter:13,Escape:27,Space:32};
async function key(key,down){await send('Input.dispatchKeyEvent',{type:down?'keyDown':'keyUp',key:key==='Space'?' ':key,code:key.length===1?'Key'+key.toUpperCase():key,windowsVirtualKeyCode:keycodes[key]||key.toUpperCase().charCodeAt(0)});}
async function tap(value){await key(value,true);await sleep(80);await key(value,false);await sleep(350);}
async function hold(value,ms){await key(value,true);await sleep(ms);await key(value,false);await sleep(300);}
const stats=()=>evaluate('window.seventhStats');
let commandSequence=0;
async function command(value){const sequence=++commandSequence;await evaluate('window.seventhReviewCommand='+JSON.stringify({...value,sequence}));await until('window.seventhReviewAck==='+sequence,5000);await sleep(350);}

const report={date:new Date().toISOString(),url,conditions:'Production HTTPS, Apple M1, Chromium, 1440x1000; cache disabled; focused isolated tab.',build:JSON.parse(await fs.readFile('dist/seventh/build.json','utf8')),errors:[],warnings:[],failedRequests:[],checks:{},screenshots:[]};
on('Runtime.exceptionThrown',e=>report.errors.push(e.exceptionDetails));
on('Runtime.consoleAPICalled',e=>{if(['error','warning'].includes(e.type))report[e.type==='error'?'errors':'warnings'].push(e.args.map(a=>a.value||a.description||'').join(' '));});
on('Network.responseReceived',e=>{if(e.response.status>=400)report.failedRequests.push([e.response.status,e.response.url]);});
async function screenshot(name){const r=await send('Page.captureScreenshot',{format:'png'});await fs.writeFile(path.join(out,name+'.png'),Buffer.from(r.data,'base64'));report.screenshots.push({name,stats:await stats()});}
try{
 await send('Page.enable');await send('Runtime.enable');await send('Network.enable');
 await send('Network.setCacheDisabled',{cacheDisabled:true});
 await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
 await send('Emulation.setFocusEmulationEnabled',{enabled:true});await send('Page.bringToFront');await send('Page.navigate',{url});
 await until('window.seventhStats?.ready && document.getElementById("loading").hidden',180000);
 assert.equal((await stats()).buildings,203);report.startup={readyMs:await evaluate('seventhReadyMs'),stats:await stats()};await screenshot('launch');
 await tap('Enter');assert.equal((await stats()).started,true);report.checks.start=true;
 while((await stats()).camera!==0)await tap('c');for(let i=0;i<4;i++){assert.equal((await stats()).camera,i);await tap('c');}report.checks.fourCameras=true;
 while((await stats()).weather!==0)await tap('t');for(let i=0;i<3;i++){assert.equal((await stats()).weather,i);await tap('t');}report.checks.threeWeatherModes=true;
 await tap('r');const before=await stats();await hold('w',2200);const after=await stats();assert(after.position[2]<before.position[2]-3);assert.equal(after.collisions,before.collisions);report.checks.keyboardDrive={before:before.position,after:after.position,contacts:after.collisions-before.collisions};await screenshot('first-avenue-drive');
 await tap('Escape');assert.equal((await stats()).paused,true);await tap('Escape');assert.equal((await stats()).paused,false);report.checks.pauseResume=true;
 await command({type:'pose',x:70,z:-77.9,yaw:-Math.PI/2});await sleep(700);assert((await stats()).drawCalls>0);await screenshot('stmarks-east');
 await command({type:'reference',x:-229,z:-77.9,height:2.5,heading:94.07686353055752,pitch:15,fov:90});await screenshot('maud-corner');
 assert.equal(report.errors.length,0,JSON.stringify(report.errors));assert.equal(report.failedRequests.length,0,JSON.stringify(report.failedRequests));report.complete=true;console.log('PRODUCTION_SMOKE_PASSED',out);
}finally{await fs.writeFile(path.join(out,'smoke.json'),JSON.stringify(report,null,2)+'\n');await fetch('http://127.0.0.1:9222/json/close/'+tab.id).catch(()=>{});ws.close();}
