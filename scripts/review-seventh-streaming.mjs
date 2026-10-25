// EV-002 paired browser evidence. Uses the existing isolated review CDP profile.
// node scripts/review-seventh-streaming.mjs OUT startups|journey|views
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';

const out=path.resolve(process.argv[2]);
const mode=process.argv[3]||'startups';
const url=process.env.BOROUGH_REVIEW_URL||'http://127.0.0.1:5173/seventh/?review=1';
const build=JSON.parse(await fs.readFile(process.env.BOROUGH_REVIEW_BUILD||new URL('../dist/seventh/build.json',import.meta.url),'utf8'));
await fs.mkdir(out,{recursive:true});
const tab=await(await fetch('http://127.0.0.1:9222/json/new?about:blank',{method:'PUT'})).json();
const ws=new WebSocket(tab.webSocketDebuggerUrl),pending=new Map(),listeners=new Map();
let id=0,sequence=0;
await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
ws.onmessage=event=>{const m=JSON.parse(event.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p?.reject(m.error):p?.resolve(m.result);}else for(const fn of listeners.get(m.method)||[])fn(m.params);};
const on=(name,fn)=>listeners.set(name,[...(listeners.get(name)||[]),fn]);
const send=(method,params={})=>new Promise((resolve,reject)=>{const request=++id,t=setTimeout(()=>{pending.delete(request);reject(Error('CDP timeout '+method));},45000);pending.set(request,{resolve:x=>{clearTimeout(t);resolve(x);},reject:x=>{clearTimeout(t);reject(x);}});ws.send(JSON.stringify({id:request,method,params}));});
async function evaluate(expression){const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result?.value;}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function until(expression,timeout=120000){const start=Date.now();while(Date.now()-start<timeout){if(await evaluate(expression))return;await sleep(100);}throw Error('Timeout '+expression);}
async function key(value,down){const code={Enter:13,Escape:27,' ':32}[value]||value.toUpperCase().charCodeAt(0);await send('Input.dispatchKeyEvent',{type:down?'keyDown':'keyUp',key:value,code:value===' '?'Space':value.length===1?'Key'+value.toUpperCase():value,windowsVirtualKeyCode:code});}
async function tap(value){await key(value,true);await sleep(70);await key(value,false);await sleep(300);}
const stats=()=>evaluate('window.seventhStats');
async function command(value){const seq=++sequence;await evaluate('window.seventhReviewCommand='+JSON.stringify({...value,sequence:seq}));await until('window.seventhReviewAck==='+seq);await sleep(350);}
const report={date:new Date().toISOString(),mode,url,build,viewport:{width:1440,height:1000,deviceScaleFactor:1},conditions:'One local game tab; unthrottled CPU/network; focus emulated. Cold means browser network cache disabled, not an OS/GPU/WASM-cache reset. Warm enables browser cache; localhost response headers are recorded. Raw first-drive intervals retained.',errors:[],warnings:[],failedRequests:[],startups:[],legs:[],poses:[],views:[]};
on('Runtime.exceptionThrown',e=>report.errors.push(e.exceptionDetails));
on('Runtime.consoleAPICalled',e=>{
  if(!['error','warning'].includes(e.type))return;
  const message=e.args.map(a=>a.value||a.description||'').join(' ');
  if(fault==='offline' && e.type==='error' && message.startsWith('TypeError: Failed to fetch') && message.includes('_godot_js_fetch_create')){
    report.expectedOfflineErrors??=[];report.expectedOfflineErrors.push(message);
  }else report[e.type==='error'?'errors':'warnings'].push(message);
});
let responses=[],transfers=[];
on('Network.responseReceived',e=>{responses.push({id:e.requestId,url:e.response.url,status:e.response.status,cache:!!e.response.fromDiskCache,mime:e.response.mimeType,headers:e.response.headers});if(e.response.status>=400)report.failedRequests.push([e.response.status,e.response.url]);});
on('Network.loadingFinished',e=>transfers.push({id:e.requestId,encodedBytes:e.encodedDataLength}));
async function open(cacheDisabled){
  await send('Page.navigate',{url:'about:blank'});await sleep(600);
  await send('Network.setCacheDisabled',{cacheDisabled});responses=[];transfers=[];
  const started=Date.now();await send('Page.navigate',{url});
  await until('(window.seventhStats?.ready && document.getElementById("loading").hidden) || document.getElementById("retry")?.hidden === false');
  assert(await evaluate('window.seventhStats?.ready && document.getElementById("loading").hidden'),'Player reports a loading failure');
  return {cacheDisabled,wallReadyMs:Date.now()-started,...await evaluate('({readyMs:window.seventhReadyMs,stats:window.seventhStats,resources:performance.getEntriesByType("resource").map(r=>({path:new URL(r.name).pathname,transferBytes:r.transferSize,encodedBytes:r.encodedBodySize,durationMs:r.duration})),memory:performance.memory?{usedJSHeapSize:performance.memory.usedJSHeapSize,totalJSHeapSize:performance.memory.totalJSHeapSize}:null})'),responses:[...responses],transfers:[...transfers]};
}
async function begin(){await tap('Enter');while((await stats()).weather!==0)await tap('t');while((await stats()).camera!==0)await tap('c');assert.equal((await stats()).started,true);}
async function recordFrames(){await evaluate('window.evFrames=[];window.evSampling=true;window.evLast=performance.now();function evTick(t){if(!window.evSampling)return;evFrames.push([t,t-evLast]);evLast=t;requestAnimationFrame(evTick)}requestAnimationFrame(evTick)');}
async function endFrames(){return evaluate('window.evSampling=false;window.evFrames');}
async function screenshot(name){const p=path.join(out,name+'.png');const r=await send('Page.captureScreenshot',{format:'png'});await fs.writeFile(p,Buffer.from(r.data,'base64'));report.views.push({file:name+'.png',stats:await stats()});}
async function dump(label){if(!(await stats()).streaming)return;await command({type:'streamingDump'});const data=await evaluate('window.seventhStreamDump');assert.equal(Object.keys(data.treeOwners).length,data.residentCount);for(const owner of Object.values(data.treeOwners))assert(owner.model&&owner.collision&&owner.children===2,'Model/collision have one shared owner');report.dumps??=[];report.dumps.push({label,data});}
let fault='',heldRequests=new Set();
async function faultMode(value){
  fault=value;
  if(value){
    const manifest=JSON.parse(await fs.readFile(new URL('../dist/seventh/'+build.areas.manifest,import.meta.url),'utf8'));
    await send('Fetch.enable',{patterns:manifest.areas['EVP-WEST'].map(id=>({urlPattern:'*'+manifest.assets[id].url,requestStage:'Request'}))});
  }else{
    for(const requestId of heldRequests){await send('Fetch.continueRequest',{requestId}).catch(e=>{report.interceptionCancellations??=[];report.interceptionCancellations.push(String(e.message||e));});}
    heldRequests.clear();await send('Fetch.disable');
  }
}
on('Fetch.requestPaused',e=>{if(e.request.url.endsWith('/index.pck'))return;(async()=>{
  report.injected??=[];report.injected.push({kind:fault,url:e.request.url,headers:e.request.headers});
  if(fault==='delay'){heldRequests.add(e.requestId);return;}
  if(fault==='offline'){await send('Fetch.failRequest',{requestId:e.requestId,errorReason:'InternetDisconnected'});return;}
  if(fault==='404'){await send('Fetch.fulfillRequest',{requestId:e.requestId,responseCode:404,body:Buffer.from('test-only missing asset').toString('base64')});return;}
  if(fault==='bad-hash'){
    const name=new URL(e.request.url).pathname;assert.match(name,/^\/seventh\/areas\/assets\/[a-f0-9]{64}\.scn$/);
    const body=await fs.readFile(new URL('../dist'+name,import.meta.url));body[body.length-1]^=1;
    await send('Fetch.fulfillRequest',{requestId:e.requestId,responseCode:200,responseHeaders:[{name:'Content-Type',value:'application/octet-stream'},{name:'Content-Length',value:String(body.length)}],body:body.toString('base64')});return;
  }
  await send('Fetch.continueRequest',{requestId:e.requestId});
})().catch(error=>{report.interceptionErrors??=[];report.interceptionErrors.push(String(error.stack||error));});});
async function eastRetired(){await command({type:'pose',x:260,z:0,yaw:Math.PI/2});await until('seventhStats.streaming.residentCount===191',12000);assert.equal((await stats()).streaming.retiredResourceRefsAlive,0);}
async function resizeCases(){
  report.resizeCases=[];
  const canvasState=()=>evaluate('({width:canvas.width,height:canvas.height,cssWidth:canvas.getBoundingClientRect().width,cssHeight:canvas.getBoundingClientRect().height,viewport:[innerWidth,innerHeight]})');
  const resize=async(width,height)=>{await send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:false});await sleep(550);};
  for(let mode=0;mode<4;mode++){
    while((await stats()).camera!==mode)await tap('c');
    await eastRetired();await faultMode('delay');
    const before=await canvasState(),car=(await stats()).position;
    await resize(680,1040);await resize(1800,700);
    const held=await canvasState(),waiting=await stats();
    assert.equal(held.width,before.width);assert.equal(held.height,before.height);
    assert(Math.abs(held.cssWidth/held.cssHeight-before.width/before.height)<.001,'Held canvas retains aspect');
    assert(waiting.streaming.resizePending&&waiting.streaming.held);assert.deepEqual(waiting.position,car);
    await screenshot('resize-held-'+mode);await faultMode('');
    await until('canvas.width===1800 && canvas.height===700 && !seventhStats.streaming.resizePending',30000);
    const ready=await stats();assert(ready.streaming.westReady);assert.equal(ready.camera,mode);
    await screenshot('resize-ready-'+mode);report.resizeCases.push({mode,before,held,waiting,ready,canvas:await canvasState()});
    await resize(1440,1000);
  }
  while((await stats()).camera!==0)await tap('c');await eastRetired();await faultMode('404');
  const before=await canvasState();await resize(700,1100);
  await until('seventhStats.streaming.terminalFailure',30000);
  const failed=await stats();assert.equal((await canvasState()).width,before.width);
  await screenshot('resize-missing');await faultMode('');await tap('r');
  await until('canvas.width===700 && canvas.height===1100 && !seventhStats.streaming.resizePending',30000);
  const resetView=await stats();
  assert(Math.hypot(resetView.cameraPose.position[0]-resetView.position[0],resetView.cameraPose.position[2]-resetView.position[2])<15,'Retry/reset must snap to its own street, without a camera sweep through buildings');
  await screenshot('resize-retry');report.resizeCases.push({kind:'missing-retry',failed,recovered:await stats()});
  await resize(1440,1000);
}
async function routeCases(){
  report.routeCases=[];
  const legs=[
    ['stmarks-east',-250,-77.9,-Math.PI/2,0,190,1],['stmarks-west',225,-77.9,Math.PI/2,0,-220,-1],
    ...[[-229,'second'],[0,'first'],[214,'avenue-a']].flatMap(([x,n])=>[[n+'-south',x,-105,Math.PI,2,10,1],[n+'-north',x,40,0,2,-73,-1]])
  ];
  for(let index=0;index<legs.length;index++){
    const [name,x,z,yaw,axis,end,direction]=legs[index];
    while((await stats()).camera!==index%4)await tap('c');
    while((await stats()).weather!==index%3)await tap('t');
    await command({type:'pose',x,z,yaw});await sleep(700);
    const before=await stats();await recordFrames();await key('w',true);const started=Date.now();
    try{while(direction*((await stats()).position[axis]-end)<0){assert(Date.now()-started<45000,'Route stalled '+name);await sleep(100);}}
    finally{await key('w',false);await key('s',true);await until('seventhStats.speed<2',10000);await key('s',false);await key(' ',true);await sleep(800);await key(' ',false);await sleep(350);}
    const frames=await endFrames(),after=await stats();
    assert.equal(after.collisions,before.collisions,'No contacts on '+name);
    assert.equal(after.streaming.holdCount,before.streaming.holdCount,'No ordinary-network hold on '+name);
    const gaps=frames.map(x=>x[1]).sort((a,b)=>a-b);
    report.routeCases.push({name,before,after,frames,p95Ms:gaps[Math.ceil(gaps.length*.95)-1],maxMs:gaps.at(-1)});
    await dump(name);await screenshot(name);console.log('ROUTE_PASS',name);
  }
}
async function releaseCases(){
  report.releaseCases=[];
  const oldPack=await fs.readFile(new URL('../model-source/east-village-ev003/fixtures/ev002.pck',import.meta.url));
  let injectedBody=null;
  on('Fetch.requestPaused',e=>{if(!e.request.url.endsWith('/index.pck'))return;(async()=>{
    await send('Fetch.fulfillRequest',{requestId:e.requestId,responseCode:200,responseHeaders:[{name:'Content-Type',value:'application/octet-stream'}],body:injectedBody.toString('base64')});
  })().catch(error=>{report.interceptionErrors??=[];report.interceptionErrors.push(String(error));});});
  for(const kind of ['old-pack','corrupt-pack']){
    injectedBody=kind==='old-pack'?oldPack:await fs.readFile(new URL('../dist/seventh/index.pck',import.meta.url));
    if(kind==='corrupt-pack')injectedBody[injectedBody.length-1]^=1;
    await send('Page.navigate',{url:'about:blank'});await send('Network.setCacheDisabled',{cacheDisabled:true});
    await send('Fetch.enable',{patterns:[{urlPattern:'*/index.pck',requestStage:'Request'}]});
    await send('Page.navigate',{url});await until('document.getElementById("retry")?.hidden===false',30000);
    const result=await evaluate('({status:document.getElementById("status").textContent,ready:!!window.seventhStats?.ready,pinned:window.seventhPinnedPack||null,resources:performance.getEntriesByType("resource").map(r=>r.name)})');
    assert(result.status.includes('updated'));assert.equal(result.ready,false);assert.equal(result.pinned,null);
    assert(!result.resources.some(u=>u.includes('/areas/assets/')),'No model wave starts from a mismatched base pack');
    await screenshot(kind);report.releaseCases.push({kind,result});await send('Fetch.disable');
  }
  report.expectedPackageErrors=report.errors.splice(0);
  assert(report.expectedPackageErrors.every(e=>typeof e==='string'&&e.startsWith('Error: The neighborhood was updated.')));
  const recovered=await open(true);assert.equal(await evaluate('window.seventhPinnedPack'),build.files['index.pck'].sha256);
  report.startups.push(recovered);await begin();
  report.cacheRuns=[];
  for(let i=0;i<2;i++)report.cacheRuns.push(await open(false));
  const cached=report.cacheRuns[1].responses.filter(r=>r.url.includes('/areas/assets/')&&r.cache);
  assert.equal(cached.length,203,'Every immutable scene is served from browser cache on repeat');
  assert(report.cacheRuns[1].responses.filter(r=>r.url.includes('/areas/assets/')).every(r=>r.headers['Cache-Control']?.includes('immutable')));
  report.immutableCachedScenes=cached.length;
}
async function failureCases(){
  report.failureCases=[];
  for(const kind of (process.env.BOROUGH_REVIEW_FAULTS||'404,bad-hash,offline').split(',')){
    await eastRetired();await faultMode(kind);
    const seq=++sequence;await evaluate('window.seventhReviewCommand='+JSON.stringify({type:'pose',x:0,z:0,yaw:0,sequence:seq}));
    await until('seventhStats.streaming.terminalFailure',30000);
    const waiting=await stats();report.currentFault={kind,waiting};assert(waiting.position[0]>250,'Unavailable reset destination must not move car');assert(waiting.streaming.residentCount>=191);assert.equal(waiting.streaming.westReady,false);
    assert(waiting.streaming.lastError.includes(kind==='bad-hash'?'integrity':'HTTP'));
    await faultMode('');await tap('r');await until('window.seventhReviewAck==='+seq,30000);await until('seventhStats.streaming.residentCount===203 && Math.abs(seventhStats.position[0])<.1',5000);
    assert.equal((await stats()).streaming.residentCount,203);assert(Math.abs((await stats()).position[0])<.1);
    report.failureCases.push({kind,waiting,recovered:await stats()});await dump(kind+'-recovered');console.log('FAULT_RECOVERY',kind);
  }
  await eastRetired();await faultMode('delay');
  const retrySeq=++sequence;await evaluate('window.seventhReviewCommand='+JSON.stringify({type:'pose',x:0,z:0,yaw:0,sequence:retrySeq}));
  await until('seventhStats.streaming.pendingRequests===2',10000);await sleep(300);
  const retryBefore=await stats();assert(heldRequests.size>0,'An intercepted request is actually outstanding');
  await tap('r');await until('seventhStats.streaming.cancellations>'+retryBefore.streaming.cancellations,5000);
  await faultMode('');await until('window.seventhReviewAck==='+retrySeq,30000);await until('seventhStats.streaming.residentCount===203',5000);
  assert.equal((await stats()).streaming.residentCount,203);
  report.failureCases.push({kind:'retry-during-delay',before:retryBefore,recovered:await stats()});await dump('inflight-retry-recovered');
  await eastRetired();await faultMode('delay');
  await key('w',true);await until('seventhStats.streaming.pendingRequests>0',10000);await key('w',false);
  await tap('Escape');assert.equal((await stats()).paused,true);
  await send('Emulation.setFocusEmulationEnabled',{enabled:false});
  const other=await(await fetch('http://127.0.0.1:9222/json/new?about:blank',{method:'PUT'})).json();
  await sleep(700);await fetch('http://127.0.0.1:9222/json/close/'+other.id);await send('Page.bringToFront');await send('Emulation.setFocusEmulationEnabled',{enabled:true});await sleep(700);
  const focus=await stats();assert.equal(focus.paused,true);assert.equal(focus.speed,0);
  await faultMode('');assert.equal((await stats()).paused,true);await tap('Escape');await key('w',true);await until('seventhStats.streaming.westReady',30000);await key('w',false);await key(' ',true);await sleep(700);await key(' ',false);
  report.failureCases.push({kind:'delay-pause-focus',focus,recovered:await stats()});await dump('pause-focus-recovered');
  await eastRetired();await faultMode('delay');
  await key('w',true);await until('seventhStats.streaming.pendingRequests>0',10000);await key('w',false);
  const before=await stats();await command({type:'pose',x:260,z:0,yaw:-Math.PI/2});
  await until('seventhStats.streaming.cancellations>'+before.streaming.cancellations,12000);
  await faultMode('');await sleep(1000);const canceled=await stats();
  assert.equal(canceled.streaming.residentCount,191);assert.equal(canceled.streaming.pendingRequests,0);assert.equal(canceled.streaming.stagedBytes,0);
  await command({type:'pose',x:0,z:0,yaw:0});assert.equal((await stats()).streaming.residentCount,203);
  report.failureCases.push({kind:'cancel-and-backtrack',before,canceled,recovered:await stats()});await dump('cancel-recovered');
}
async function drive(direction,cycle){
  const current=await stats(),east=direction==='east',yaw=east?-Math.PI/2:Math.PI/2;
  await command({type:'pose',x:current.position[0],z:0,yaw});
  await recordFrames();await key('w',true);
  const started=Date.now(),positions=[];
  while(true){const s=await stats();positions.push({wallMs:Date.now()-started,...s});if(east?s.position[0]>=238:s.position[0]<=-238)break;assert(Date.now()-started<65000,'Traversal stalled');await sleep(150);}
  await key('w',false);await key('s',true);await until('seventhStats.speed<2',10000);await key('s',false);await key(' ',true);await sleep(600);await key(' ',false);
  const intervals=await endFrames(),sorted=intervals.map(x=>x[1]).sort((a,b)=>a-b);
  const leg={cycle,direction,wallMs:Date.now()-started,positions,intervals,p95Ms:sorted[Math.floor(sorted.length*.95)],maxMs:sorted.at(-1),final:await stats()};report.legs.push(leg);
  assert.equal(leg.final.collisions,0,'Unexpected route contact');
  console.log(JSON.stringify({cycle,direction,p95Ms:leg.p95Ms,maxMs:leg.maxMs,x:leg.final.position[0],resident:leg.final.streaming?.residentCount}));
  await sleep(4200);report.poses.push({cycle,direction,stats:await stats()});
  if((await stats()).streaming){
    const s=await stats();assert.equal(s.streaming.held,false,'Normal-network loading must keep up');
    assert.equal(s.streaming.holdCount,0,'No hidden movement holds on normal travel');
    assert.equal(s.streaming.residentCount,east?191:203,'Expected independent west residency');
    assert.equal(s.streaming.retiredResourceRefsAlive,0,'Retired resources must be released');
    if(east){
      const saved={camera:s.camera,weather:s.weather};
      while((await stats()).camera!==0)await tap('c');while((await stats()).weather!==0)await tap('t');await sleep(3200);
      report.memoryCheckpoints??=[];report.memoryCheckpoints.push({cycle,stats:await stats()});
      while((await stats()).camera!==saved.camera)await tap('c');while((await stats()).weather!==saved.weather)await tap('t');
    }
    await dump('cycle-'+cycle+'-'+direction);
  }
  await fs.writeFile(path.join(out,mode+'.json'),JSON.stringify(report,null,2)+'\n');
}
try{
  await send('Page.enable');await send('Runtime.enable');await send('Network.enable');
  await send('Emulation.setDeviceMetricsOverride',{...report.viewport,mobile:false});
  await send('Emulation.setFocusEmulationEnabled',{enabled:true});await send('Page.bringToFront');
  report.browser=await send('Browser.getVersion');
  if(mode==='release'){
    await releaseCases();
  }else if(mode==='startups'){
    report.preconditioning=await open(true);await begin();await sleep(1000);
    for(const cacheDisabled of [true,false])for(let i=0;i<5;i++){
      const run=await open(cacheDisabled);run.index=i;report.startups.push(run);
      assert.equal(run.stats.buildings,build.buildings);
      console.log(JSON.stringify({cacheDisabled,index:i,readyMs:run.readyMs,wallReadyMs:run.wallReadyMs,encodedBytes:run.transfers.reduce((n,x)=>n+x.encodedBytes,0)}));
      await fs.writeFile(path.join(out,mode+'.json'),JSON.stringify(report,null,2)+'\n');
    }
  }else{
    report.startups.push(await open(true));await begin();
    if(mode==='resize'){
      await resizeCases();
    }else if(mode==='routes'){
      await routeCases();
    }else if(mode==='journey'){
      await command({type:'pose',x:-260,z:0,yaw:-Math.PI/2});
      for(let cycle=0;cycle<10;cycle++){
        while((await stats()).weather!==cycle%3)await tap('t');
        while((await stats()).camera!==cycle%4)await tap('c');
        await sleep(1000);await drive('east',cycle);await drive('west',cycle);
      }
    }else if(mode==='failures'){
      await failureCases();
    }else if(mode==='camera-hold'){
      await eastRetired();await faultMode('delay');
      while((await stats()).camera!==1)await tap('c');
      await send('Input.dispatchMouseEvent',{type:'mouseWheel',x:700,y:480,deltaY:1500,deltaX:0});await sleep(1200);
      let held=null;report.cameraProbe=[];
      for(let step=0;step<12;step++){
        await send('Input.dispatchMouseEvent',{type:'mousePressed',x:700,y:480,button:'right',buttons:2});
        await send('Input.dispatchMouseEvent',{type:'mouseMoved',x:740,y:480,button:'right',buttons:2});
        await send('Input.dispatchMouseEvent',{type:'mouseReleased',x:740,y:480,button:'right',buttons:0});
        await sleep(450);const state=await stats();report.cameraProbe.push(state);
        if(state.streaming.cameraHeld){held=state;break;}
      }
      assert(held,'Wide orbit should request unready west bounds');
      await sleep(600);const still=await stats();assert.deepEqual(still.position,held.position,'Guard keeps the car stopped');
      assert.deepEqual(still.cameraPose.position,held.cameraPose.position,'Unready camera pose stays frozen');
      await screenshot('camera-held');await faultMode('');await until('seventhStats.streaming.westReady && !seventhStats.streaming.cameraHeld',30000);
      await screenshot('camera-released');report.cameraRecovery={held,recovered:await stats()};await dump('camera-released');
    }else if(mode==='probe'){
      await dump('opening');await command({type:'pose',x:260,z:0,yaw:Math.PI/2});await sleep(4500);await dump('east-retired');await screenshot('east');
      assert.equal((await stats()).streaming.residentCount,191);
      await command({type:'pose',x:-260,z:0,yaw:-Math.PI/2});await dump('west-reloaded');await screenshot('west');
      assert.equal((await stats()).streaming.residentCount,203);
    }else if(mode==='details'||mode==='tilebar-entry'){
      for(let weather=0;weather<3;weather++){
        while((await stats()).weather!==weather)await tap('t');await sleep(3000);
        for(const [name,cmd] of (mode==='tilebar-entry' ? [['tilebar-entry',{type:'reference',x:-7,z:-11.85,height:2.1,heading:-60.92313646944248,pitch:0,fov:58}]] : [
          ['tilebar',{type:'frontage',id:241822226,close:true,along:.5,span:.5}],
          ['kinka',{type:'frontage',id:241822202,close:true,along:.55,span:.65}],
          ['stmarks83',{type:'streetFrontage',faceId:'241822219:0',close:true,along:.5,span:.65}],
          ['first134',{type:'streetFrontage',faceId:'248142711:1',close:true,along:.5,span:.65}]
        ])){await command(cmd);await sleep(1200);await screenshot(name+'-'+weather);}
      }
    }else if(mode==='views'){
      for(let weather=0;weather<3;weather++){
        while((await stats()).weather!==weather)await tap('t');await sleep(3000);
        for(const [name,x,yaw] of [['corner',0,Math.PI/2],['seam',-229,-Math.PI/2],['west',-260,Math.PI/2],['east',260,Math.PI/2]]){
          await command({type:'pose',x,z:0,yaw});await sleep(2000);await screenshot(name+'-'+weather);
        }
      }
    }else throw Error('Unknown mode '+mode);
  }
  assert.equal(report.errors.length,0,JSON.stringify(report.errors));
  report.runtimeCatalogRequests=responses.filter(r=>/\/seventh\/(?:build\.json|areas\/manifest-)/.test(r.url));
  assert.equal(report.runtimeCatalogRequests.length,0,'An open player must retain its embedded catalog, without switching releases');
  if(!['failures','resize'].includes(mode))assert.equal(report.failedRequests.length,0,JSON.stringify(report.failedRequests));
  assert.equal(report.interceptionErrors?.length||0,0,JSON.stringify(report.interceptionErrors));report.complete=true;
}catch(error){report.failure=String(error.stack||error);report.failureState=await stats().catch(()=>null);throw error;}
finally{await key('w',false).catch(()=>{});await key('s',false).catch(()=>{});await fs.writeFile(path.join(out,mode+'.json'),JSON.stringify(report,null,2)+'\n');await fetch('http://127.0.0.1:9222/json/close/'+tab.id).catch(()=>{});ws.close();}
