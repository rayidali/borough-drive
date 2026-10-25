// P02: five elevations, five businesses and protected neighbors. Capture is not visual acceptance.
// Captures never automatically award photographic or visual acceptance.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const url=process.env.BOROUGH_REVIEW_URL||'http://127.0.0.1:5173/seventh/?review=1';
const out=path.resolve(process.argv[2]||'model-source/east-village-p02/review-01');
const terminalMode=process.argv[3]==='terminal';
const routeMode=process.argv[3]==='routes';
const filter=(routeMode||terminalMode)?null:process.argv[3]?.split(',');
const slice=JSON.parse(await fs.readFile('engine/first-seventh/assets/slice.json','utf8'));
const build=JSON.parse(await fs.readFile('dist/seventh/build.json','utf8'));
const faces=slice.packetReviewFrontages.filter(r=>[248142657,248142658,248142659,248142660,248142713].includes(r.id)&&(!filter||filter.includes(r.faceId)));
const schedule=JSON.parse(await fs.readFile('model-source/east-village-p02/schedule.json','utf8'));
const ledger=schedule;
const elevations=new Map(schedule.elevations.map(r=>[r.faceId,r]));
assert(faces.length,'No scheduled review faces');
if(filter)assert.equal(faces.length,new Set(filter).size,'Unknown review face');
await fs.mkdir(out,{recursive:true});
const report={url,date:new Date().toISOString(),scope:'P02 138–148 First Avenue; protected neighbors read-only',build,viewport:[800,800,1],acceptance:'Capture only; visual review must be recorded separately.',errors:[],warnings:[],failedRequests:[],views:[]};
const tab=await(await fetch('http://127.0.0.1:9222/json/new?about:blank',{method:'PUT'})).json();
const ws=new WebSocket(tab.webSocketDebuggerUrl),pending=new Map();let sequence=0,commandSequence=0;
await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p?.reject(m.error):p?.resolve(m.result);return;}
 if(m.method==='Runtime.exceptionThrown')report.errors.push(m.params.exceptionDetails);
 if(m.method==='Runtime.consoleAPICalled'&&['error','warning'].includes(m.params.type))report[m.params.type==='error'?'errors':'warnings'].push(m.params.args.map(a=>a.value||a.description||'').join(' '));
 if(m.method==='Network.responseReceived'&&m.params.response.status>=400)report.failedRequests.push([m.params.response.status,m.params.response.url]);};
const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++sequence,timer=setTimeout(()=>{pending.delete(id);reject(Error('CDP timeout: '+method));},30000);pending.set(id,{resolve:v=>{clearTimeout(timer);resolve(v);},reject:e=>{clearTimeout(timer);reject(e);}});ws.send(JSON.stringify({id,method,params}));});
const delay=ms=>new Promise(r=>setTimeout(r,ms));
async function evaluate(expression){const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result?.value;}
async function until(expression,timeout=120000){const start=Date.now();while(Date.now()-start<timeout){if(await evaluate(expression))return;await delay(200);}throw Error('Timeout: '+expression);}
async function command(value){const n=++commandSequence;await evaluate('window.seventhReviewCommand='+JSON.stringify({...value,sequence:n}));await until('window.seventhReviewAck==='+n,6000);await delay(450);}
async function capture(name,record,pose){await command(pose);const r=await send('Page.captureScreenshot',{format:'png'});const bytes=Buffer.from(r.data,'base64');await fs.writeFile(path.join(out,name+'.png'),bytes);report.views.push({name,faceId:record.faceId,pose,sha256:createHash('sha256').update(bytes).digest('hex')});}

async function key(value,down){await send('Input.dispatchKeyEvent',{type:down?'keyDown':'keyUp',key:value,code:'Key'+value.toUpperCase(),windowsVirtualKeyCode:value.toUpperCase().charCodeAt(0)});}
async function tap(value){await key(value,true);await key(value,false);await delay(400);}
const stats=()=>evaluate('window.seventhStats');
async function shot(name){const r=await send('Page.captureScreenshot',{format:'png'});await fs.writeFile(path.join(out,name+'.png'),Buffer.from(r.data,'base64'));report.views.push({name,stats:await stats()});}
async function routeReview(){
 report.routes=[];report.boundaries=[];report.cameras=[];
 await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});report.viewport=[1440,1000,1];
 for(const [name,x,z,yaw,end,direction] of [['first-north',0,-88,0,-122,-1],['first-south',0,-134,Math.PI,-87,1],['west-lane-north',-6,-96,0,-122,-1],['east-lane-south',6,-134,Math.PI,-92,1]]){
  await command({type:'pose',x,z,yaw});await delay(500);const before=await stats();
  await evaluate('window.p02Frames=[];window.p02Sampling=true;window.p02Last=performance.now();function p02Tick(t){if(!p02Sampling)return;p02Frames.push(t-p02Last);p02Last=t;requestAnimationFrame(p02Tick)}requestAnimationFrame(p02Tick)');
  await key('w',true);const start=Date.now();
  try{while(direction*((await stats()).position[2]-end)<0){assert(Date.now()-start<25000,'Route stalled '+name);await delay(100);}}
  finally{await key('w',false);await key('s',true);await until('seventhStats.speed<1',7000);await key('s',false);await delay(600);}
  const after=await stats(),frames=await evaluate('p02Sampling=false;p02Frames'),sorted=[...frames].sort((a,b)=>a-b);
  report.currentRoute={name,before,after};assert.equal(after.collisions,before.collisions,name+' contact');assert.equal(after.streaming.holdCount,before.streaming.holdCount,name+' hold');assert.equal(after.addressVisible,false);assert.equal(after.address,'');
  report.routes.push({name,before,after,frames,p95Ms:sorted[Math.ceil(sorted.length*.95)-1],maxMs:sorted.at(-1)});await shot(name);
 }
 // Test the corridor cap north of 148's projecting storefront, not through its building collider.
 for(const [name,x,z,yaw,axis,limit,direction] of [['first-terminal',0,-138,0,2,-145,-1],['second-still-closed',-229,-112,0,2,-119,-1],['avenue-a-still-closed',214,-112,0,2,-119,-1],['east-side-cap',12,-147,-Math.PI/2,0,17,1]]){
  await command({type:'pose',x,z,yaw});const before=await stats();const heldSamples=[];await key('w',true);for(let i=0;i<6;i++){await delay(1000);heldSamples.push(await stats());}await key('w',false);await key('s',true);await delay(500);await key('s',false);const after=await stats();
  report.currentBoundary={name,before,after};assert(direction*(after.position[axis]-limit)<.5,name+' escaped');assert(direction*(heldSamples.at(-1).position[axis]-before.position[axis])>1,name+' must move toward boundary');assert(Math.abs(heldSamples.at(-1).position[axis]-heldSamples.at(-2).position[axis])<.05,name+' must stop under held throttle');assert(Math.abs(heldSamples.at(-1).position[axis]-limit)<3,name+' must reach boundary');report.boundaries.push({name,before,after,heldSamples});await shot(name);
 }
 await command({type:'pose',x:-4,z:-132,yaw:0});
 for(let mode=0;mode<4;mode++){
  while((await stats()).camera!==mode)await tap('c');const before=await stats();
  await send('Input.dispatchMouseEvent',{type:'mousePressed',x:700,y:480,button:'right',buttons:2});await send('Input.dispatchMouseEvent',{type:'mouseMoved',x:880,y:510,button:'right',buttons:2});await send('Input.dispatchMouseEvent',{type:'mouseReleased',x:880,y:510,button:'right',buttons:0});
  await send('Input.dispatchMouseEvent',{type:'mouseWheel',x:700,y:480,deltaY:250,deltaX:0});await delay(650);const after=await stats();
  assert.equal(after.camera,mode);assert(Math.hypot(after.position[0]-before.position[0],after.position[2]-before.position[2])<.01);assert.equal(after.addressVisible,false);assert.notDeepEqual(after.cameraPose,before.cameraPose);report.cameras.push({mode,before,after});await shot('north-camera-'+mode);
 }
 await command({type:'streamingDump'});report.owners=await evaluate('window.seventhStreamDump');
 for(const id of slice.packetScope.buildingIds){const owner=report.owners.treeOwners[id];assert(owner&&owner.model&&owner.collision&&owner.children===2,'P02 model/collision owner '+id);}
 await tap('r');await delay(1000);report.reset=await stats();assert(Math.hypot(report.reset.position[0]+.5,report.reset.position[2]-8)<.2);await shot('reset-seventh');
}
try{
 await send('Runtime.enable');await send('Network.enable');await send('Page.enable');
 await send('Emulation.setDeviceMetricsOverride',{width:800,height:800,deviceScaleFactor:1,mobile:false});
 await send('Emulation.setFocusEmulationEnabled',{enabled:true});await send('Page.bringToFront');
 await send('Page.navigate',{url});
 await until('window.seventhStats?.ready && document.getElementById("loading")?.hidden');
 assert.equal(await evaluate('seventhStats.buildings'),slice.buildings.length);
 await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
 await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});await until('seventhStats.started');
 for(let i=0;i<3&&(await evaluate('seventhStats.weather'))!==0;i++){
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'t',code:'KeyT',windowsVirtualKeyCode:84});await send('Input.dispatchKeyEvent',{type:'keyUp',key:'t',code:'KeyT',windowsVirtualKeyCode:84});await delay(500);
 }
 await delay(1500);
 if(terminalMode){
 await command({type:'reference',x:0,z:-139,height:2.0,heading:29.076863530557524,pitch:0,fov:70});await delay(600);await shot('terminal-facing');report.terminal=await stats();
 }else if(routeMode){
 await routeReview();
 }else{
 for(const record of faces){
  await capture(record.faceId.replaceAll(':','-')+'-elevation',record,{type:'streetFrontage',faceId:record.faceId,close:false});
  for(const [name,along] of [['ground-south',.25],['ground-north',.75]])
   await capture(record.faceId.replaceAll(':','-')+'-'+name,record,{type:'streetFrontage',faceId:record.faceId,close:true,along,span:.65});
 }
 for(const [name,pose] of [
 ['protected-stmarks83',{type:'streetFrontage',faceId:'241822219:0',close:true,along:.5,span:.65}],
 ['protected-first134',{type:'streetFrontage',faceId:'248142711:1',close:true,along:.5,span:.65}],
 ['protected-tilebar',{type:'reference',x:-7,z:-11.85,height:2.1,heading:-60.92313646944248,pitch:0,fov:58}]
 ])await capture(name,{faceId:'protected'},pose);
 for(const business of ledger.businesses){
  const record=faces.find(r=>r.faceId===business.faceId);if(!record)continue;
  const a=elevations.get(record.faceId).architecture;
  const shop=a.returnShops[Number(business.id.split(':').at(-1))];
  const span=shop?.span||[0,1],f=record.frontage,w=f.length*(span[1]-span[0]);
  const count=Math.max(1,Math.ceil(w/7.5));
  for(let j=0;j<count;j++){
   const along=span[0]+(span[1]-span[0])*(j+.5)/count;
   const nx=-f.rz,nz=f.rx,mx=f.x+f.rx*f.length*along,mz=f.z-228+f.rz*f.length*along;
   const distance=Math.max(5.5,Math.min(8.2,(w/count)/(2*Math.tan(31*Math.PI/180))*1.16));
   for(const [view,offset] of [['front',0],['left',-1.8],['right',1.8]]){
    const x=mx+nx*distance+f.rx*offset,z=mz+nz*distance+f.rz*offset;
    const heading=Math.atan2(mx-x,-(mz-z))*180/Math.PI+29.076863530557524;
    const name=business.id.replaceAll(':','-')+'-'+j+'-'+view;
    const pose={type:'reference',x,z,height:2.30,heading,pitch:0,fov:62};
    await capture(name,record,pose);
    report.views.at(-1).businessId=business.id;report.views.at(-1).view=view;
   }
  }
  if(w>7.5){
   const mx=f.x+f.rx*f.length*.5,mz=f.z-228+f.rz*f.length*.5;
   await capture(record.faceId.replaceAll(':','-')+'-shop-complete',record,{type:'reference',x:mx-f.rz*10.5,z:mz+f.rx*10.5,height:2.75,heading:119.07686353055752,pitch:0,fov:62});
  }
  console.log('BUSINESS_CAPTURED',business.id);
  // Upper mass and both junctions must survive perspective review, not only shop crops.
  const mx=f.x+f.rx*f.length*.5,mz=f.z-228+f.rz*f.length*.5;
  for(const [name,offset] of [['mass-north',-5],['mass-south',5]]){
   const x=mx-f.rz*17+f.rx*offset,z=mz+f.rx*17+f.rz*offset;
   const heading=Math.atan2(mx-x,-(mz-z))*180/Math.PI+29.076863530557524;
   await capture(record.faceId.replaceAll(':','-')+'-'+name,record,{type:'reference',x,z,height:5.0,heading,pitch:8,fov:60});
  }

 }
 }
 if(!routeMode&&!terminalMode&&!filter){
  for(let mood=0;mood<3;mood++){
   while((await stats()).weather!==mood)await tap('t');await delay(7000);
   await capture('block-weather-'+mood,{faceId:'P02-block'},{type:'reference',x:-1,z:-127,height:4.2,heading:119.07686353055752,pitch:4,fov:95});
  }
 }
 assert.equal(report.errors.length,0,JSON.stringify(report.errors));assert.equal(report.failedRequests.length,0,JSON.stringify(report.failedRequests));report.complete=true;
}finally{await fs.writeFile(path.join(out,'captures.json'),JSON.stringify(report,null,2)+'\n');await fetch('http://127.0.0.1:9222/json/close/'+tab.id).catch(()=>{});ws.close();}
