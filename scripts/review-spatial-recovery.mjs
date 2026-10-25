import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {reviewClient,delay} from './browser-review-client.mjs';
const out=path.resolve(process.argv[2]||'model-source/browser-scale-2026-10-25/recovery-05');await fs.mkdir(out,{recursive:true});
const build=JSON.parse(await fs.readFile('dist/seventh/build.json','utf8'));
const manifest=JSON.parse(await fs.readFile('engine/first-seventh/assets/area_manifest.json','utf8'));
const target='247851937',asset=manifest.assets[target];assert(asset);
const c=await reviewClient();let fault='',held=[],activeCase;
const report={date:new Date().toISOString(),build,target,errors:[],expectedNetworkErrors:[],failedRequests:[],cases:[]};
c.on('Runtime.exceptionThrown',e=>report.errors.push(e.exceptionDetails));
c.on('Runtime.consoleAPICalled',e=>{if(e.type==='error'){const message=e.args.map(a=>a.value||a.description||'').join(' ');if(fault||message.includes('Failed to fetch'))report.expectedNetworkErrors.push(message);else report.errors.push(message);}});
c.on('Network.responseReceived',e=>{if(e.response.status>=400)report.failedRequests.push([e.response.status,e.response.url]);});
c.on('Fetch.requestPaused',e=>{(async()=>{
 activeCase.requests.push({url:e.request.url,headers:e.request.headers,fault});
 if(fault==='delay'){held.push(e.requestId);return;}
 if(fault==='404'){await c.send('Fetch.fulfillRequest',{requestId:e.requestId,responseCode:404,responseHeaders:[{name:'Content-Type',value:'text/plain'},{name:'Content-Length',value:'18'}],body:Buffer.from('missing scene test').toString('base64')});return;}
 if(fault==='offline'){await c.send('Fetch.failRequest',{requestId:e.requestId,errorReason:'InternetDisconnected'});return;}
 if(fault==='corrupt'){const b=await fs.readFile('dist'+asset.url);b[b.length-1]^=1;await c.send('Fetch.fulfillRequest',{requestId:e.requestId,responseCode:200,responseHeaders:[{name:'Content-Type',value:'application/octet-stream'},{name:'Content-Length',value:String(b.length)}],body:b.toString('base64')});return;}
 await c.send('Fetch.continueRequest',{requestId:e.requestId});
 })().catch(e=>report.errors.push(String(e)));});
async function clear(){fault='';for(const id of held)await c.send('Fetch.continueRequest',{requestId:id});held=[];await c.send('Fetch.disable');}
async function absent(x=270,z=0){await c.command({type:'pose',x,z,yaw:Math.PI});await delay(10500);const s=await c.stats();assert(!s.streaming.residentIds.includes(target),'Fault target must actually retire');return s;}
async function intercept(name){fault=name;await c.send('Fetch.enable',{patterns:[{urlPattern:'*'+asset.url,requestStage:'Request'}]});}
try{
 report.startup=await c.open('http://127.0.0.1:5181/seventh/?review=1');await c.tap('Enter');
 for(const kind of (process.argv[3]==='resize'?[]:['delay','404','corrupt','offline'])){
  activeCase={kind,requests:[],before:await absent()};report.cases.push(activeCase);
  await intercept(kind);const sequence=await c.submit({type:'pose',x:-202,z:-304.3,yaw:Math.PI/2});
  const began=Date.now();while(!activeCase.requests.length){assert(Date.now()-began<30000,'Missing intercepted request');await delay(100);}
  await c.key('w',true);await delay(kind==='delay'?12000:1600);activeCase.during=await c.stats();await c.key('w',false);
  assert.equal(activeCase.during.speed,0);assert.deepEqual(activeCase.during.position,activeCase.before.position);
  assert(!activeCase.during.streaming.residentIds.includes(target));
  if(kind!=='delay'){
   await c.until('seventhStats.streaming.terminalFailure',30000);activeCase.failure=await c.stats();assert.equal(activeCase.requests.length,3);
   if(kind==='corrupt')assert.match(activeCase.failure.streaming.lastError,/integrity mismatch/);
  }
  await c.shot(path.join(out,kind+'-held.png'));await clear();if(kind!=='delay')await c.tap('r');
  await c.until('window.seventhReviewAck==='+sequence);await delay(700);activeCase.after=await c.dump();
  assert(activeCase.after.residentIds.includes(target));assert(!activeCase.after.terminalFailure);assert.equal(activeCase.after.lastError,'');
  console.log('RECOVERY_PASS',kind);
  await fs.writeFile(path.join(out,'review.json'),JSON.stringify(report,null,2)+'\n');
 }
 activeCase={kind:'resize-delay',requests:[],before:await absent(0,8)};report.cases.push(activeCase);await intercept('delay');
 activeCase.oldCanvas=await c.evaluate('[document.querySelector("canvas").width,document.querySelector("canvas").height]');
 await c.send('Emulation.setDeviceMetricsOverride',{width:1000,height:780,deviceScaleFactor:1,mobile:false});
 await c.until('seventhStats.streaming.resizePending');
 const requestStart=Date.now();while(!activeCase.requests.length){assert(Date.now()-requestStart<60000,'Resize target request must arrive');await delay(100);}
 await delay(1800);assert(activeCase.requests.length>0);activeCase.pending=await c.stats();
 assert.deepEqual(await c.evaluate('[document.querySelector("canvas").width,document.querySelector("canvas").height]'),activeCase.oldCanvas);
 await c.shot(path.join(out,'resize-held.png'));await clear();await c.until('!seventhStats.streaming.resizePending');await delay(700);
 assert.deepEqual(await c.evaluate('[document.querySelector("canvas").width,document.querySelector("canvas").height]'),[1000,780]);activeCase.after=await c.dump();await c.shot(path.join(out,'resize-complete.png'));
 for(const [width,height] of [[680,800],[620,800],[390,844],[1440,1000]]){
  await c.send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:false});await delay(500);await c.until('!seventhStats.streaming.resizePending');await delay(500);assert.deepEqual(await c.evaluate('[document.querySelector("canvas").width,document.querySelector("canvas").height]'),[width,height]);await c.shot(path.join(out,`viewport-${width}.png`));
 }
 assert.equal(report.errors.length,0,JSON.stringify(report.errors));report.complete=true;console.log('SPATIAL_RECOVERY_COMPLETE');
}finally{await clear().catch(()=>{});await fs.writeFile(path.join(out,'review.json'),JSON.stringify(report,null,2)+'\n');await c.close();}
