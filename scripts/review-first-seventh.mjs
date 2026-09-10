// Actual-browser review using a separate Chrome instance with remote debugging.
// No dependency installation or instrumentation in the published game.
// Start npm run dev and Chrome with --remote-debugging-port=9222 and a temporary
// --user-data-dir, then: node scripts/review-first-seventh.mjs [output directory]
import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const out=path.resolve(process.argv[2]||'renders/first-seventh-review');
const freshDefault=process.argv.includes('--fresh-default');
await fs.mkdir(out,{recursive:true});
const tab=await (await fetch('http://127.0.0.1:9222/json/new?about:blank',{method:'PUT'})).json();
const ws=new WebSocket(tab.webSocketDebuggerUrl),pending=new Map(),listeners=new Map();let id=0;
await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p?.reject(m.error):p?.resolve(m.result);}else for(const f of listeners.get(m.method)||[])f(m.params);};
const on=(name,fn)=>listeners.set(name,[...(listeners.get(name)||[]),fn]);
function send(method,params={}){return new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params}));});}
async function evaluate(expression){const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result?.value;}
const report={date:new Date().toISOString(),url:'http://127.0.0.1:5173',errors:[],consoleErrors:[],warnings:[],failedRequests:[],viewport:{width:1440,height:1000,deviceScaleFactor:1},screenshots:[]};
let bootstrapFailureExpected=false;
report.expectedFailures=[];
on('Runtime.exceptionThrown',e=>report.errors.push(e.exceptionDetails.text));
on('Runtime.consoleAPICalled',e=>{if(['error','warning'].includes(e.type)){const message=e.args.map(a=>a.value||a.description||'').join(' ');if(bootstrapFailureExpected&&e.type==='error'&&message.includes('Failed to fetch'))report.expectedFailures.push({kind:'bootstrap error',message});else report[e.type==='error'?'consoleErrors':'warnings'].push(message);}});
on('Network.responseReceived',e=>{if(e.response.status>=400)report.failedRequests.push([e.response.status,e.response.url]);});
await send('Page.enable');await send('Runtime.enable');await send('Network.enable');await send('Debugger.enable');
await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
const source=await fs.readFile(new URL('../dist/reconstruction/viewer.js',import.meta.url),'utf8');
const lineNumber=source.split('\n').findIndex(s=>s.includes('ready=true;returnToStart()'));
assert(lineNumber>0);
await send('Debugger.setBreakpointByUrl',{urlRegex:'/reconstruction/viewer\\.js$',lineNumber});
on('Debugger.paused',async e=>{
 try{await send('Debugger.evaluateOnCallFrame',{callFrameId:e.callFrames[0].callFrameId,expression:`globalThis.__boroughReview={
  pose:()=>({x:camera.position.x,z:camera.position.z,yaw,mode,ready,coreLoaded:neighborhood.coreLoaded,corePending:neighborhood.corePending,tiles:[...neighborhood.states.values()].filter(s=>s.root).map(s=>s.tile.id)}),
  look:(x,z,tx,ty,tz)=>{setMode('walk',false);travel(x,z);camera.position.set(x,1.72,z);yaw=targetYaw=Math.atan2(tx-x,-(tz-z));pitch=targetPitch=Math.atan2(ty-1.72,Math.hypot(tx-x,tz-z));},
  glass:()=>{const seen=new Set();for(const state of neighborhood.states.values())state.root?.traverse(o=>{if(o.material?.name==='seventh glass')seen.add(o.material.userData.paneTransmission.value);});return [...seen];},
  renders:0,
  graphics:()=>({renderer:renderer.getContext().getParameter(renderer.getContext().getExtension('WEBGL_debug_renderer_info').UNMASKED_RENDERER_WEBGL),pixelRatio:renderer.getPixelRatio(),ao:ao.enabled,quality,samples:composer.renderTarget1.samples})
 };const actualRender=composer.render.bind(composer);composer.render=(...args)=>{__boroughReview.renders++;return actualRender(...args);}`});}finally{await send('Debugger.resume');}
});
if(freshDefault)await send('Page.addScriptToEvaluateOnNewDocument',{source:"localStorage.removeItem('borough.graphics');"});
await send('Page.navigate',{url:report.url});
async function until(expression,timeout=120000){const start=Date.now();while(Date.now()-start<timeout){if(await evaluate(expression))return;await new Promise(r=>setTimeout(r,300));}throw Error('Browser condition timed out: '+expression);}
await until('globalThis.__boroughReview?.pose().ready && document.querySelector("#loading").hidden');
if(freshDefault){assert.equal(await evaluate('document.querySelector("#quality").value'),'auto');report.freshAutomaticDefaultPassed=true;}
await send('Debugger.disable');
await evaluate('document.querySelector("#quality").value="detail";document.querySelector("#quality").dispatchEvent(new Event("change"))');
await until('__boroughReview.pose().tiles.includes("block-5-1") && __boroughReview.pose().tiles.includes("block-5-2") && __boroughReview.pose().tiles.includes("edge-south")');
report.initial=await evaluate('__boroughReview.pose()');
assert(Math.abs(report.initial.x)<.01&&Math.abs(report.initial.z-228)<.01&&Math.abs(report.initial.yaw)<.01,'Initial pose is First & 7th, northbound');
async function screenshot(name){await new Promise(r=>setTimeout(r,800));const r=await send('Page.captureScreenshot',{format:'png'});await fs.writeFile(path.join(out,name+'.png'),Buffer.from(r.data,'base64'));report.screenshots.push({name,pose:await evaluate('__boroughReview.pose()')});console.log('VIEW',name);}
await screenshot('first-and-seventh-start');
await evaluate('document.querySelector("#drive-button").click()');
await send('Input.dispatchKeyEvent',{type:'keyDown',key:'w',code:'KeyW'});await new Promise(r=>setTimeout(r,1200));await send('Input.dispatchKeyEvent',{type:'keyUp',key:'w',code:'KeyW'});
report.driven=await evaluate('__boroughReview.pose()');assert(report.driven.z<227.8,'Driving proceeds north into map');
await send('Input.dispatchKeyEvent',{type:'keyDown',key:'r',code:'KeyR'});await send('Input.dispatchKeyEvent',{type:'keyUp',key:'r',code:'KeyR'});
await new Promise(r=>setTimeout(r,400));report.driveReset=await evaluate('__boroughReview.pose()');assert(Math.abs(report.driveReset.z-228)<.02&&report.driveReset.mode==='drive');
await evaluate('document.querySelector("#walk-button").click();document.querySelector("[data-corner=se]").click();document.querySelector("#reset-button").click()');
report.walkReset=await evaluate('__boroughReview.pose()');assert(Math.abs(report.walkReset.z-228)<.02&&report.walkReset.mode==='walk');
for(const corner of ['nw','ne','sw','se']){
 await evaluate(`document.querySelector('[data-seventh="${corner}"]').click()`);
 assert(await evaluate(`document.querySelector('[data-seventh="${corner}"]').getAttribute('aria-pressed')==='true'`));
 await screenshot('seventh-'+corner);
}
const data=JSON.parse(await fs.readFile(new URL('../dist/reconstruction/neighborhood.json',import.meta.url)));
const schedule=JSON.parse(await fs.readFile(new URL('../model-source/storefront-details.json',import.meta.url)));
const corner=JSON.parse(await fs.readFile(new URL('../model-source/first-and-seventh.json',import.meta.url)));
const ids=new Set(corner.buildings.map(b=>b.id));
for(const entry of schedule.frontages.filter(e=>ids.has(e.buildingId))){
 const b=data.buildings.find(b=>b.id===entry.buildingId),r=b.businesses.find(r=>r.id===entry.businessId),f=b.frontages[r.frontageIndex];
 const s=(r.unit[0]+r.unit[1])/2,tx=f.x+f.rx*s,tz=f.z+f.rz*s,d=entry.reviewDistance||9;
 await evaluate(`__boroughReview.look(${tx-f.rz*d},${tz+f.rx*d},${tx},2.6,${tz})`);
 await until(`__boroughReview.pose().tiles.includes(${JSON.stringify(b.tile)})`);
 await screenshot(entry.id);
 if(false && entry.design.blades?.length){
  await evaluate(`__boroughReview.look(${tx-f.rz*d+f.rx*6},${tz+f.rx*d+f.rz*6},${tx},3.1,${tz})`);
  await screenshot(entry.id+'-blade');
 }
}
for(const profile of corner.buildings){
 const b=data.buildings.find(b=>b.id===profile.id);
 for(const street of Object.keys(profile.elevations)){
  const f=b.frontages.find(f=>f.street===street);
  const tx=f.x+f.rx*f.length/2,tz=f.z+f.rz*f.length/2,h=b.renderHeight||b.height,d=Math.max(16,Math.min(24,h*1.04));
  await evaluate(`__boroughReview.look(${tx-f.rz*d},${tz+f.rx*d},${tx},${h*.49},${tz})`);
  await screenshot('elevation-'+profile.profile+'-'+(street==='First Avenue'?'first':'seventh'));
 }
}
report.assets={};
for(const tile of data.tiles.filter(t=>['block-5-1','block-5-2','edge-south'].includes(t.id))){
 const buffer=await fs.readFile(new URL('../dist/reconstruction/'+tile.url,import.meta.url));
 report.assets[tile.id]={bytes:buffer.length,sha256:createHash('sha256').update(buffer).digest('hex'),signature:tile.storefrontSignature};
}
await evaluate('document.querySelector("[data-seventh=se]").click()');
// A settled view intentionally does not redraw. RAF callbacks measure browser
// responsiveness here; use profile-performance.mjs for active rendering FPS.
report.rafResponsiveness=[];
for(const quality of ['detail','fast']){
 await evaluate(`document.querySelector('#quality').value='${quality}';document.querySelector('#quality').dispatchEvent(new Event('change'))`);
 await new Promise(r=>setTimeout(r,1000));
 const sample=await evaluate(`new Promise(resolve=>{let n=0,first;const initialRenders=__boroughReview.renders;function step(t){if(!n)first=t;if(++n===121)resolve({rafFrames:120,seconds:(t-first)/1000,rafFps:120000/(t-first),sceneRedraws:__boroughReview.renders-initialRenders});else requestAnimationFrame(step)}requestAnimationFrame(step)})`);
 const transmission=await evaluate('__boroughReview.glass()');assert.deepEqual(transmission,[.96]);
 assert.equal(await evaluate('localStorage.getItem("borough.graphics")'),quality);
 report.rafResponsiveness.push({...sample,...await evaluate('__boroughReview.graphics()'),glassModel:'thin pane',paneTransmission:transmission});
}
await evaluate('document.querySelector("#quality").value="detail";document.querySelector("#quality").dispatchEvent(new Event("change"))');
report.graphics=await evaluate('__boroughReview.graphics()');
await new Promise(r=>setTimeout(r,1000));
const settled=await evaluate('__boroughReview.renders');await new Promise(r=>setTimeout(r,700));
assert.equal(await evaluate('__boroughReview.renders'),settled,'Settled scene must stop redrawing.');
await send('Emulation.setDeviceMetricsOverride',{width:1100,height:800,deviceScaleFactor:1,mobile:false});
await until(`__boroughReview.renders>${settled}`);report.resizeResumedRendering=true;
await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
const beforeLook=await evaluate('__boroughReview.renders');
await send('Input.dispatchMouseEvent',{type:'mousePressed',x:700,y:400,button:'left',clickCount:1});
await send('Input.dispatchMouseEvent',{type:'mouseMoved',x:750,y:390,button:'left',buttons:1});
await send('Input.dispatchMouseEvent',{type:'mouseReleased',x:750,y:390,button:'left',clickCount:1});
await until(`__boroughReview.renders>${beforeLook}`);report.dragResumedRendering=true;
// Fail one deferred core request, then let the real 12-second retry complete.
let coreFailures=0,bootstrapFailures=0;
on('Fetch.requestPaused',async e=>{if(e.request.url.endsWith('first-and-10th.glb')&&coreFailures++===0){report.expectedFailures.push({kind:'deferred core connection failure'});await send('Fetch.failRequest',{requestId:e.requestId,errorReason:'Failed'});}else if(e.request.url.endsWith('street-materials.glb')&&bootstrapFailureExpected&&bootstrapFailures++===0){report.expectedFailures.push({kind:'bootstrap connection failure'});await send('Fetch.failRequest',{requestId:e.requestId,errorReason:'Failed'});}else await send('Fetch.continueRequest',{requestId:e.requestId});});
await send('Fetch.enable',{patterns:[{urlPattern:'*first-and-10th.glb'},{urlPattern:'*street-materials.glb'}]});
assert.equal(await evaluate('__boroughReview.pose().coreLoaded'),false);
await evaluate('document.querySelector("[data-corner=se]").click()');
await until('__boroughReview.pose().coreLoaded',45000);assert.equal(coreFailures,2,'Failed core request must retry once and load.');
report.coreRetryPassed=true;
for(const corner of ['nw','ne','sw','se']){await evaluate(`document.querySelector('[data-corner=${corner}]').click()`);await screenshot('first-tenth-'+corner);}
await evaluate('document.querySelector("#reset-button").click()');
// Startup failure retains the fallback photograph; Retry opens a working game.
bootstrapFailureExpected=true;await send('Page.reload',{ignoreCache:true});
await until('!document.querySelector("#fallback").hidden && document.querySelector("#fallback img").complete && document.querySelector("#fallback img").naturalWidth>0');
assert.equal(bootstrapFailures,1);report.bootstrapFallbackPassed=true;
bootstrapFailureExpected=false;await evaluate('document.querySelector("#retry-button").click()');
await until('document.querySelector("#loading").hidden && document.querySelector("#fallback").hidden');report.bootstrapRetryPassed=true;
await send('Fetch.disable');
await fs.writeFile(path.join(out,'review.json'),JSON.stringify(report,null,2)+'\n');
await fetch('http://127.0.0.1:9222/json/close/'+tab.id);ws.close();assert.equal(report.errors.length,0);assert.equal(report.consoleErrors.length,0);assert.equal(report.failedRequests.length,0);
console.log('REVIEW_COMPLETE',out,report.screenshots.length);
