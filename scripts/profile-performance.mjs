// Chrome CDP benchmark. Run npm run dev and an isolated Chrome on port 9222.
// node scripts/profile-performance.mjs [output directory] [--diagnose] [--automatic]
// Instrumentation is injected into this review tab only, never into the game.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const out=path.resolve(process.argv[2]||'renders/performance');
const diagnose=process.argv.includes('--diagnose');
const automatic=process.argv.includes('--automatic');
await fs.mkdir(out,{recursive:true});
const url=process.env.BOROUGH_REVIEW_URL||'http://127.0.0.1:5173';
const tab=await(await fetch('http://127.0.0.1:9222/json/new?about:blank',{method:'PUT'})).json();
const ws=new WebSocket(tab.webSocketDebuggerUrl),pending=new Map(),listeners=new Map();let id=0;
await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p?.reject(m.error):p?.resolve(m.result);}else for(const f of listeners.get(m.method)||[])f(m.params);};
const on=(name,fn)=>listeners.set(name,[...(listeners.get(name)||[]),fn]);
function send(method,params={}){return new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params}));});}
async function evaluate(expression){const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result?.value;}
async function until(expression,timeout=120000){const start=Date.now();while(Date.now()-start<timeout){if(await evaluate(expression))return;await new Promise(r=>setTimeout(r,250));}throw Error('Timed out: '+expression);}
const pause=ms=>new Promise(r=>setTimeout(r,ms));
const report={date:new Date().toISOString(),url,viewport:{width:1440,height:1000,deviceScaleFactor:1},cache:'disabled; local HTTP, unthrottled CPU/network',errors:[],consoleErrors:[],warnings:[],failedRequests:[],samples:[],screenshots:[]};
on('Runtime.exceptionThrown',e=>report.errors.push(e.exceptionDetails));
on('Runtime.consoleAPICalled',e=>{if(['error','warning'].includes(e.type))report[e.type==='error'?'consoleErrors':'warnings'].push(e.args.map(a=>a.value||a.description||'').join(' '));});
on('Network.responseReceived',e=>{if(e.response.status>=400)report.failedRequests.push([e.response.status,e.response.url]);});
try{
 await send('Page.enable');await send('Runtime.enable');await send('Network.enable');await send('Debugger.enable');
 await send('Network.setCacheDisabled',{cacheDisabled:true});
 await send('Emulation.setDeviceMetricsOverride',{...report.viewport,mobile:false});
 await send('Page.addScriptToEvaluateOnNewDocument',{source:`localStorage.setItem('borough.graphics','detail');globalThis.__longTasks=[];new PerformanceObserver(list=>__longTasks.push(...list.getEntries().map(e=>({start:e.startTime,duration:e.duration})))).observe({type:'longtask',buffered:true});`});
 const source=await fs.readFile(new URL('../dist/reconstruction/viewer.js',import.meta.url),'utf8');
 const lineNumber=source.split('\n').findIndex(s=>s.includes('ready=true;returnToStart()'));assert(lineNumber>0);
 await send('Debugger.setBreakpointByUrl',{urlRegex:'/reconstruction/viewer\\.js$',lineNumber});
 on('Debugger.paused',async e=>{try{await send('Debugger.evaluateOnCallFrame',{callFrameId:e.callFrames[0].callFrameId,expression:`
  globalThis.__perf={renderer,scene,camera,composer,ao,neighborhood,readyAt:performance.now(),frames:[],
   pose:()=>({x:camera.position.x,z:camera.position.z,yaw,mode,ready,tiles:[...neighborhood.states.values()].filter(s=>s.root).map(s=>s.tile.id),coreLoaded:neighborhood.coreLoaded,corePending:neighborhood.corePending,pending:[...neighborhood.states.values()].filter(s=>s.promise).length+(neighborhood.corePending?1:0)}),
   graphics:()=>({renderer:renderer.getContext().getParameter(renderer.getContext().getExtension('WEBGL_debug_renderer_info').UNMASKED_RENDERER_WEBGL),pixelRatio:renderer.getPixelRatio(),ao:ao.enabled,quality,samples:composer.renderTarget1.samples,transmissionScale:renderer.transmissionResolutionScale,memory:{...renderer.info.memory}}),
   travel:(x,z)=>travel(x,z),
   busy:false,
   motion:()=>{if(__perf.busy){yaw=targetYaw=yaw+.000001;requestAnimationFrame(__perf.motion);}}
  };
  const render=composer.render.bind(composer);composer.render=(...args)=>{renderer.info.autoReset=false;renderer.info.reset();const begin=performance.now();render(...args);__perf.frames.push({time:begin,cpuMs:performance.now()-begin,calls:renderer.info.render.calls,triangles:renderer.info.render.triangles});};
 `});}finally{await send('Debugger.resume');}});
 await send('Page.navigate',{url});
 await until('globalThis.__perf?.pose().ready && document.querySelector("#loading").hidden');
 await send('Debugger.disable');
 report.startup=await evaluate('({readyMs:__perf.readyAt,firstFrameMs:__perf.frames[0]?.time,overlayHiddenMs:performance.now(),pose:__perf.pose()})');
 await until('["block-5-1","block-5-2","edge-south"].every(id=>__perf.pose().tiles.includes(id)) && !__perf.pose().pending');
 await evaluate('__perf.neighborhood.props');await pause(1800);
 report.startup.settledMs=await evaluate('performance.now()');
 report.startup.resources=await evaluate('performance.getEntriesByType("resource").map(e=>({path:new URL(e.name).pathname,startMs:e.startTime,endMs:e.responseEnd,bytes:e.transferSize})).filter(e=>e.path.includes("reconstruction/"))');
 report.startup.longTasks=await evaluate('__longTasks');
 report.graphics=await evaluate('__perf.graphics()');
 assert(Math.abs(report.startup.pose.x)<.01&&Math.abs(report.startup.pose.z-228)<.01);
 async function screenshot(name){await pause(500);const r=await send('Page.captureScreenshot',{format:'png'});await fs.writeFile(path.join(out,name+'.png'),Buffer.from(r.data,'base64'));report.screenshots.push({name,pose:await evaluate('__perf.pose()')});}
 async function sample(name,{busy=true,frames=180}={}){
  await evaluate(`__perf.frames=[];__perf.busy=${busy};if(__perf.busy)requestAnimationFrame(__perf.motion)`);
  const timing=await evaluate(`new Promise(resolve=>{const times=[];function tick(t){times.push(t);if(times.length===${frames+1})resolve(times);else requestAnimationFrame(tick)}requestAnimationFrame(tick)})`);
  const rendered=await evaluate('__perf.busy=false;__perf.frames');
  const sorted=timing.slice(1).map((t,i)=>t-timing[i]).sort((a,b)=>a-b),seconds=(timing.at(-1)-timing[0])/1000;
  const mean=key=>rendered.reduce((sum,f)=>sum+f[key],0)/Math.max(1,rendered.length);
  const result={name,seconds,rafFrames:frames,rafFps:frames/seconds,renderFrames:rendered.length,renderFps:rendered.length/seconds,frameMsP50:sorted[Math.floor(sorted.length*.5)],frameMsP95:sorted[Math.floor(sorted.length*.95)],meanRenderCpuMs:mean('cpuMs'),meanDrawCalls:mean('calls'),meanTriangles:mean('triangles'),pose:await evaluate('__perf.pose()'),graphics:await evaluate('__perf.graphics()')};
  const tail=rendered.slice(-120);result.tailRenderFps=tail.length>1?(tail.length-1)*1000/(tail.at(-1).time-tail[0].time):null;
  report.samples.push(result);console.log(JSON.stringify(result));
 }
 for(const corner of ['nw','ne','sw','se']){await evaluate(`document.querySelector('[data-seventh=${corner}]').click()`);await pause(700);await screenshot('seventh-'+corner);if(corner==='se')await sample('seventh-se-detail');}
 if(diagnose){
  await evaluate('__perf.renderer.transmissionResolutionScale=.5');await sample('diagnostic-transmission-half',{frames:120});await evaluate('__perf.renderer.transmissionResolutionScale=1');
  await evaluate('__perf.ao.enabled=false');await sample('diagnostic-no-ao',{frames:120});await evaluate('__perf.ao.enabled=true');
  await evaluate('__perf.scene.children.filter(o=>o.isPointLight).forEach(o=>o.visible=false)');await sample('diagnostic-no-point-lights',{frames:120});await evaluate('__perf.scene.children.filter(o=>o.isPointLight).forEach(o=>o.visible=true)');
 }
 await pause(1200);await sample('seventh-se-idle',{busy:false});
 await evaluate('document.querySelector("#quality").value="fast";document.querySelector("#quality").dispatchEvent(new Event("change"))');await pause(700);await sample('seventh-se-fast');
 await evaluate('document.querySelector("#quality").value="detail";document.querySelector("#quality").dispatchEvent(new Event("change"));document.querySelector("#reset-button").click();document.querySelector("#drive-button").click()');await pause(900);
 await send('Input.dispatchKeyEvent',{type:'keyDown',key:'w',code:'KeyW'});await sample('northbound-drive-detail',{busy:false,frames:240});await send('Input.dispatchKeyEvent',{type:'keyUp',key:'w',code:'KeyW'});
 assert((await evaluate('__perf.pose()')).z<220,'Drive north from First & 7th');
 await evaluate('document.querySelector("[data-corner=se]").click()');await until('!__perf.pose().pending');await pause(2200);await screenshot('first-tenth-se');await sample('first-tenth-se-detail');
 // Cross-map travel exercises queue reprioritization, unloading and return.
 await evaluate('__perf.travel(210,-145)');await pause(9500);await until('!__perf.pose().pending');report.farTravel=await evaluate('__perf.pose()');await screenshot('avenue-a-twelfth');
 await evaluate('document.querySelector("#reset-button").click()');await until('["block-5-1","block-5-2","edge-south"].every(id=>__perf.pose().tiles.includes(id)) && !__perf.pose().pending');await pause(1000);report.returned=await evaluate('__perf.pose()');assert(Math.abs(report.returned.z-228)<.01);await screenshot('returned-seventh');
 if(automatic){
  report.automaticConditions='Additional warm-cache tests after cross-map travel; not a cold-drive comparison.';
  await evaluate('document.querySelector("#quality").value="auto";document.querySelector("#quality").dispatchEvent(new Event("change"));document.querySelector("[data-seventh=se]").click()');
  await sample('seventh-se-auto-adapting',{frames:240});await sample('seventh-se-auto-settled-rate');
  assert((await evaluate('__perf.graphics()')).pixelRatio>=.7);
  await pause(2000);
  assert.equal((await evaluate('__perf.graphics()')).pixelRatio,1,'Idle automatic inspection restores CSS-pixel resolution.');
  assert.equal((await evaluate('__perf.graphics()')).ao,true,'Idle inspection restores ambient shading.');
  await sample('seventh-se-auto-idle',{busy:false,frames:120});
  assert.equal(report.samples.at(-1).renderFrames,0,'Automatic idle restoration must settle without a render loop.');
  await screenshot('seventh-se-auto-restored');
  await evaluate('document.querySelector("#reset-button").click();document.querySelector("#drive-button").click()');
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'w',code:'KeyW'});await sample('northbound-drive-auto-warm',{busy:false,frames:480});await send('Input.dispatchKeyEvent',{type:'keyUp',key:'w',code:'KeyW'});
  await screenshot('automatic-drive');
  await evaluate('document.querySelector("#reset-button").click();document.querySelector("#walk-button").click()');
  await pause(2000);
  assert.equal((await evaluate('__perf.graphics()')).pixelRatio,1);assert.equal((await evaluate('__perf.graphics()')).ao,true);
  await send('Emulation.setDeviceMetricsOverride',{width:1100,height:800,deviceScaleFactor:2,mobile:false});await pause(600);
  assert.equal((await evaluate('__perf.graphics()')).pixelRatio,1,'Automatic does not blindly render at high device pixel ratio.');
  await send('Emulation.setDeviceMetricsOverride',{...report.viewport,mobile:false});
  report.automaticIdleAndResizePassed=true;
 }
 report.runtime={};for(const filename of ['viewer.js','neighborhood-render.js']){const buffer=await fs.readFile(new URL('../dist/reconstruction/'+filename,import.meta.url));report.runtime[filename]=createHash('sha256').update(buffer).digest('hex');}
 await fs.writeFile(path.join(out,'profile.json'),JSON.stringify(report,null,2)+'\n');
 assert.equal(report.errors.length,0);assert.equal(report.consoleErrors.length,0);assert.equal(report.failedRequests.length,0);
 console.log('PROFILE_COMPLETE',out,JSON.stringify({readyMs:report.startup.readyMs,settledMs:report.startup.settledMs,initialReconstructionBytes:report.startup.resources.reduce((n,r)=>n+r.bytes,0)}));
}finally{await fetch('http://127.0.0.1:9222/json/close/'+tab.id).catch(()=>{});ws.close();}
