// Fast reproducible runtime-performance pass. Start npm run dev and an
// isolated Chromium CDP browser on port 9222, then run:
// node scripts/review-seventh-performance.mjs [output-directory]
// This deliberately uses the same nine weather/route samples as
// review-seventh.mjs, but does not capture images or exercise controls,
// persistence, recovery, or download behavior.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';

const out=path.resolve(process.argv[2]||'renders/seventh-engine-04/performance');
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
  const requestId=++id,timeout=setTimeout(()=>{pending.delete(requestId);reject(Error('CDP timeout: '+method));},30000);
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

const report={
  date:new Date().toISOString(),url,viewport:{width:1440,height:1000,deviceScaleFactor:1},build,buildHashes,
  conditions:'Local HTTP, Apple M1, unthrottled CPU/network; browser cache disabled for startup. Same routes, weather transitions, reset behavior, and warm intervals as review-seventh.mjs; no screenshots or control/recovery checks.',
  routeConfig:{northbound:{seconds:5,warmAfterResetMs:5500},seventhEast:{pose:{x:-260,z:0,yaw:-Math.PI/2},seconds:8,weatherSettleMs:5000},seventhWest:{pose:{x:258,z:0,yaw:Math.PI/2},seconds:8,weatherSettleMs:5000}},
  errors:[],warnings:[],failedRequests:[],samples:[]
};
on('Runtime.exceptionThrown',event=>report.errors.push(event.exceptionDetails));
on('Runtime.consoleAPICalled',event=>{if(['error','warning'].includes(event.type))report[event.type==='error'?'errors':'warnings'].push(event.args.map(arg=>arg.value||arg.description||'').join(' '));});
on('Network.responseReceived',event=>{if(event.response.status>=400)report.failedRequests.push([event.response.status,event.response.url]);});
async function sample(name,seconds){
  const value=await evaluate(`new Promise(resolve=>{const start=performance.now(),first=seventhStats.frames,firstTick=seventhStats.tickMs,times=[],counts=[];let last;function tick(t){if(last)times.push(t-last);last=t;counts.push({...seventhStats});if(t-start<${seconds*1000})requestAnimationFrame(tick);else{times.sort((a,b)=>a-b);resolve({name:${JSON.stringify(name)},seconds:(t-start)/1000,frames:seventhStats.frames-first,counterMs:seventhStats.tickMs-firstTick,rafFps:times.length*1000/(t-start),p95Ms:times[Math.floor(times.length*.95)],drawCalls:counts.reduce((sum,current)=>sum+current.drawCalls,0)/counts.length,triangles:counts.reduce((sum,current)=>sum+current.triangles,0)/counts.length,final:{...seventhStats}})}}requestAnimationFrame(tick)})`);
  value.renderFps=value.frames*1000/value.counterMs;
  report.samples.push(value);console.log(JSON.stringify(value));
}

try{
  await send('Page.enable');await send('Runtime.enable');await send('Network.enable');
  await send('Network.setCacheDisabled',{cacheDisabled:true});
  await send('Emulation.setDeviceMetricsOverride',{...report.viewport,mobile:false});
  await send('Page.navigate',{url});
  await until('window.seventhStats?.ready && document.getElementById("loading").hidden');
  report.startup=await evaluate('({readyMs:seventhReadyMs,resources:performance.getEntriesByType("resource").map(resource=>({path:new URL(resource.name).pathname,bytes:resource.transferSize,durationMs:resource.duration})),stats:seventhStats})');
  assert.equal((await stats()).buildings,182);
  await tap('Enter');assert.equal((await stats()).started,true);
  while((await stats()).weather!==0)await tap('t');
  while((await stats()).camera!==0)await tap('c');
  // Exact northbound loop from review-seventh.mjs: reset, 5.5 s warmup,
  // then five seconds of normal W-key driving in each weather state.
  for(let mood=0;mood<3;mood++){
    await tap('r');await sleep(5500);
    await key('w',true);await sample(`weather-${mood}-northbound`,5);await key('w',false);
    assert((await stats()).position[2]<-20);
    if(mood<2)await tap('t');
  }
  // Exact Seventh east/west pose and duration loop from review-seventh.mjs.
  for(let mood=0;mood<3;mood++){
    while((await stats()).weather!==mood)await tap('t');await sleep(5000);
    await command({type:'pose',x:-260,z:0,yaw:-Math.PI/2});
    await key('w',true);await sample(`weather-${mood}-seventh-east`,8);await key('w',false);
    await command({type:'pose',x:258,z:0,yaw:Math.PI/2});
    await key('w',true);await sample(`weather-${mood}-seventh-west`,8);await key('w',false);
  }
  await tap('r');
  assert.equal(report.samples.length,9);
  assert.equal(report.errors.length,0,JSON.stringify(report.errors));
  assert.equal(report.failedRequests.length,0,JSON.stringify(report.failedRequests));
  report.complete=true;
  console.log('SEVENTH_PERFORMANCE_PASSED',out);
}finally{
  await fs.writeFile(path.join(out,'performance.json'),JSON.stringify(report,null,2)+'\n');
  await fetch('http://127.0.0.1:9222/json/close/'+tab.id).catch(()=>{});
  ws.close();
}
