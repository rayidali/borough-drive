// Real browser controls and rendering review. Start npm run dev and an isolated
// Chromium browser with --remote-debugging-port=9222, then npm run seventh:review.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const out = path.resolve(process.argv[2] || 'renders/seventh-engine/browser-review');
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
const report={date:new Date().toISOString(),url,viewport:{width:1440,height:1000,deviceScaleFactor:1},conditions:'Local HTTP, Apple M1, unthrottled CPU/network; browser cache disabled for startup. Render counters from the actual engine; subsequent samples warmed.',errors:[],warnings:[],failedRequests:[],samples:[],checks:{},screenshots:[]};
report.build=JSON.parse(await fs.readFile(new URL('../dist/seventh/build.json',import.meta.url),'utf8'));
let faultPhase=false;
report.recovery={errors:[],warnings:[],failedRequests:[],checks:{}};
const log=()=>faultPhase?report.recovery:report;
on('Runtime.exceptionThrown',e=>log().errors.push(e.exceptionDetails));
on('Runtime.consoleAPICalled',e=>{if(['error','warning'].includes(e.type))log()[e.type==='error'?'errors':'warnings'].push(e.args.map(a=>a.value||a.description||'').join(' '));});
on('Network.responseReceived',e=>{if(e.response.status>=400)log().failedRequests.push([e.response.status,e.response.url]);});
async function screenshot(name){const r=await send('Page.captureScreenshot',{format:'png'});await fs.writeFile(path.join(out,name+'.png'),Buffer.from(r.data,'base64'));report.screenshots.push({name,stats:await stats()});}
async function sample(name,seconds=5){
  const value=await evaluate(`new Promise(resolve=>{const start=performance.now(),first=seventhStats.frames,firstTick=seventhStats.tickMs,times=[],counts=[];let last;function tick(t){if(last)times.push(t-last);last=t;counts.push({...seventhStats});if(t-start<${seconds*1000})requestAnimationFrame(tick);else{times.sort((a,b)=>a-b);resolve({name:${JSON.stringify(name)},seconds:(t-start)/1000,frames:seventhStats.frames-first,counterMs:seventhStats.tickMs-firstTick,rafFps:times.length*1000/(t-start),p95Ms:times[Math.floor(times.length*.95)],drawCalls:counts.reduce((s,x)=>s+x.drawCalls,0)/counts.length,triangles:counts.reduce((s,x)=>s+x.triangles,0)/counts.length,final:{...seventhStats}})}}requestAnimationFrame(tick)})`);
  value.renderFps=value.frames*1000/value.counterMs;report.samples.push(value);console.log(JSON.stringify(value));
}
try {
  await send('Page.enable');await send('Runtime.enable');await send('Network.enable');
  await send('Network.setCacheDisabled',{cacheDisabled:true});
  await send('Emulation.setDeviceMetricsOverride',{...report.viewport,mobile:false});
  await send('Page.navigate',{url});
  await until('window.seventhStats?.ready && document.getElementById("loading").hidden');
  report.startup=await evaluate('({readyMs:seventhReadyMs,resources:performance.getEntriesByType("resource").map(r=>({path:new URL(r.name).pathname,bytes:r.transferSize,durationMs:r.duration})),stats:seventhStats})');
  assert.equal((await stats()).buildings,182);
  await screenshot('title');
  await tap('Enter');assert.equal((await stats()).started,true);
  // Normalize to golden hour/chase through actual controls, including saved settings.
  while((await stats()).weather!==0)await tap('t');
  while((await stats()).camera!==0)await tap('c');
  for(let mood=0;mood<3;mood++){
    await tap('r');await sleep(5500);
    for(let view=0;view<4;view++){
      assert.equal((await stats()).camera,view);await screenshot(`weather-${mood}-camera-${view}`);await tap('c');
    }
    await tap('r');await key('w',true);await sample(`weather-${mood}-northbound`,5);await key('w',false);
    assert((await stats()).position[2]<-20);await screenshot(`weather-${mood}-drive`);
    if(mood<2)await tap('t');
  }
  report.checks.camerasAndWeather=12;
  await tap('r');await hold('s',1600);assert((await stats()).position[2]>10);report.checks.reverse=true;
  await tap('r');await hold('w',1600);const beforeBrake=(await stats()).speed;await hold('s',450);assert((await stats()).speed<beforeBrake-4,'S brakes before reversing');report.checks.brake=true;
  // Actual input on Seventh: accelerate, steer and pull the handbrake, then
  // release both. Pose selection only places the car; it cannot inject motion.
  while((await stats()).weather!==0)await tap('t');await sleep(5000);
  await command({type:'pose',x:-229,z:18,yaw:0});
  const driftContacts=(await stats()).collisions;
  await key('w',true);await sleep(2100);await key('a',true);await key('Space',true);
  // Telemetry updates at 4 Hz; observe the actual slip rather than sampling
  // a stale quarter-second record at one fragile wall-clock instant.
  let drift;const driftStarted=Date.now();
  while(Date.now()-driftStarted<1200){drift=await stats();if(Math.abs(drift.slipDegrees)>18)break;await sleep(35);}
  await key('Space',false);await key('a',false);await key('w',false);
  await screenshot('handbrake-drift');
  await key('d',true);await sleep(320);await key('d',false);
  await sleep(350);const recovered=await stats();
  assert(Math.abs(drift.slipDegrees)>15&&drift.tireScrub>.2,'Actual handbrake must release grip');
  assert(Math.abs(recovered.slipDegrees)<10,'Released drift regains grip');
  assert.equal(recovered.collisions,driftContacts,'Countersteered drift clears the real intersection');
  report.checks.drift={during:drift,after:recovered,countersteerMs:320,wallContacts:recovered.collisions-driftContacts};
  await tap('r'); // Stop coasting before the next weather settles.
  // Samples down the full street expose more of the scene than the old
  // northbound-only benchmark. All movement uses the normal keyboard control.
  for(let mood=0;mood<3;mood++){
    while((await stats()).weather!==mood)await tap('t');await sleep(5000);
    await command({type:'pose',x:-260,z:0,yaw:-Math.PI/2});
    await key('w',true);await sample(`weather-${mood}-seventh-east`,8);await key('w',false);
    await screenshot(`seventh-east-${mood}`);
    await command({type:'pose',x:258,z:0,yaw:Math.PI/2});
    await key('w',true);await sample(`weather-${mood}-seventh-west`,8);await key('w',false);
    await screenshot(`seventh-west-${mood}`);
  }
  await tap('r');
  await tap('Escape');const stopped=await stats();await hold('w',800);assert.equal((await stats()).paused,true);assert(Math.hypot((await stats()).position[0]-stopped.position[0],(await stats()).position[2]-stopped.position[2])<.1);await screenshot('pause');await tap('Escape');report.checks.pause=true;
  await tap('r');await sleep(500);assert(Math.abs((await stats()).speed)<.1);assert(Math.abs((await stats()).position[2]-8)<.1);report.checks.reset=true;
  await hold('a',600);await key('a',true);await hold('w',900);await key('a',false);assert((await stats()).yaw>.1);report.checks.steering=true;
  await tap('r');await tap('c');await tap('m');await sleep(2000);
  const saved=await stats();report.settingsBeforeReload=saved;
  await send('Page.reload');await until('window.seventhStats?.ready && document.getElementById("loading").hidden');
  const restored=await stats();for(const k of ['camera','weather','sound'])assert.equal(restored[k],saved[k],k+' persists across reload');report.checks.settingsReload=true;
  await tap('Enter');if((await stats()).sound)await tap('m');while((await stats()).camera!==0)await tap('c');while((await stats()).weather!==0)await tap('t');
  await send('Emulation.setDeviceMetricsOverride',{width:1100,height:800,deviceScaleFactor:2,mobile:false});await sleep(900);await screenshot('retina-resize');
  report.retinaCanvas=await evaluate('({width:canvas.width,height:canvas.height,css:[innerWidth,innerHeight]})');
  assert.equal(report.retinaCanvas.width,1100,'Retina must not multiply rendering resolution');
  assert.equal(report.retinaCanvas.height,800);
  await send('Emulation.setDeviceMetricsOverride',{...report.viewport,mobile:false});
  report.checks.resize=true;
  const elsewhere=await send('Target.createTarget',{url:'about:blank'});
  await send('Target.activateTarget',{targetId:elsewhere.targetId});await sleep(600);
  await send('Target.activateTarget',{targetId:tab.id});await sleep(600);
  assert.equal((await stats()).paused,true,'Switching tabs safely pauses driving');
  await send('Target.closeTarget',{targetId:elsewhere.targetId});await tap('Escape');
  report.checks.focusLoss=true;
  const downloads=path.join(out,'postcards');await fs.mkdir(downloads,{recursive:true});
  await send('Browser.setDownloadBehavior',{behavior:'allow',downloadPath:downloads});
  const beforeDownload=new Set(await fs.readdir(downloads));await tap('p');
  let postcard;
  for(let i=0;i<50;i++){postcard=(await fs.readdir(downloads)).find(x=>x.endsWith('.png')&&!beforeDownload.has(x));if(postcard)break;await sleep(200);}
  assert(postcard,'Postcard should download');assert((await fs.stat(path.join(downloads,postcard))).size>100000,'Postcard contains the actual scene');report.checks.postcard=true;
  while((await stats()).weather!==0)await tap('t');await sleep(5000);
  const details=JSON.parse(await fs.readFile(new URL('../model-source/storefront-details.json',import.meta.url),'utf8')).seventhEngine;
  for(const shop of details.frontages){
    await command({type:'frontage',id:shop.buildingId,close:true,along:(shop.span[0]+shop.span[1])/2,span:shop.span[1]-shop.span[0]});
    await screenshot('shop-'+shop.businessId.replace('osm-node-',''));
  }
  report.checks.perspectiveShopCaptures=details.frontages.length;
  await tap('r');
  assert.equal(report.errors.length,0,JSON.stringify(report.errors));assert.equal(report.failedRequests.length,0,JSON.stringify(report.failedRequests));
  await fs.writeFile(path.join(out,'review.json'),JSON.stringify(report,null,2)+'\n');
  console.log('SEVENTH_CONTROLS_PASSED');
  // Fault injection is deliberately separate from the healthy runtime evidence.
  faultPhase=true;
  on('Fetch.requestPaused',event=>{send('Fetch.fulfillRequest',{requestId:event.requestId,responseCode:503,responseHeaders:[{name:'Content-Type',value:'text/plain'}],body:Buffer.from('Intentional review failure').toString('base64')}).catch(()=>{});});
  await send('Fetch.enable',{patterns:[{urlPattern:'*/seventh/index.pck',requestStage:'Request'}]});
  await send('Page.reload');await until('document.getElementById("retry")?.hidden === false');await screenshot('download-recovery');
  console.log('SEVENTH_DOWNLOAD_FAILURE_VISIBLE');
  await send('Fetch.disable');await evaluate('setTimeout(()=>document.getElementById("retry").click(),0)');
  await until('window.seventhStats?.ready && document.getElementById("loading")?.hidden === true');report.recovery.checks.missingPackRetry=true;
  await fs.writeFile(path.join(out,'review.json'),JSON.stringify(report,null,2)+'\n');
  console.log('SEVENTH_DOWNLOAD_RETRY_PASSED');
  await evaluate('canvas.getContext("webgl2").getExtension("WEBGL_lose_context").loseContext()');
  await until('document.getElementById("retry")?.hidden === false');assert((await evaluate('document.getElementById("status").textContent')).includes('graphics paused'));await screenshot('graphics-recovery');
  await evaluate('setTimeout(()=>document.getElementById("retry").click(),0)');await until('window.seventhStats?.ready && document.getElementById("loading")?.hidden === true');report.recovery.checks.contextLossRetry=true;
  await fs.writeFile(path.join(out,'review.json'),JSON.stringify(report,null,2)+'\n');
  assert.equal(report.errors.length,0,JSON.stringify(report.errors));assert.equal(report.failedRequests.length,0,JSON.stringify(report.failedRequests));
  console.log('SEVENTH_BROWSER_REVIEW_COMPLETE',out);
}finally{
  await fs.writeFile(path.join(out,'review.json'),JSON.stringify(report,null,2)+'\n');
  await fetch('http://127.0.0.1:9222/json/close/'+tab.id).catch(()=>{});ws.close();
}
