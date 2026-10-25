// Full Eleventh west block: independent elevations, shopfronts, access and junctions. Capture is not visual acceptance.
// Captures never automatically award photographic or visual acceptance.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const cdp=process.env.BOROUGH_CDP||'http://127.0.0.1:9222';
const url=process.env.BOROUGH_REVIEW_URL||'http://127.0.0.1:5181/seventh/?review=1';
const out=path.resolve(process.argv[2]||'model-source/east-village-e11-block/review-01');
const routeMode=process.argv[3]==='routes';
const filter=routeMode?null:process.argv[3]?.split(',');
const slice=JSON.parse(await fs.readFile('engine/first-seventh/assets/slice.json','utf8'));
const build=JSON.parse(await fs.readFile('dist/seventh/build.json','utf8'));
const faces=slice.packetReviewFrontages.filter(r=>slice.packetScope.faceIds.includes(r.faceId)&&(!filter||filter.includes(r.faceId)));
const schedule=JSON.parse(await fs.readFile('model-source/east-village-e11-block/schedule.json','utf8'));
const ledger=schedule;
const elevations=new Map(schedule.elevations.map(r=>[r.faceId,r]));
assert(faces.length,'No scheduled review faces');
if(filter)assert.equal(faces.length,new Set(filter).size,'Unknown review face');
await fs.mkdir(out,{recursive:true});
const report={url,date:new Date().toISOString(),scope:'26 Eleventh west planes, preserved 23-owner core, and full block integration',build,viewport:[800,800,1],imageEncoding:'JPEG quality 96; original viewport 800 x 800',acceptance:'Capture only; visual review must be recorded separately.',errors:[],warnings:[],failedRequests:[],views:[]};
const tab=await(await fetch(`${cdp}/json/new?about:blank`,{method:'PUT'})).json();
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
async function command(value){const n=++commandSequence;await evaluate('window.seventhReviewCommand='+JSON.stringify({...value,sequence:n}));await until('window.seventhReviewAck==='+n,180000);await delay(450);}
async function capture(name,record,pose){const existing=await fs.readFile(path.join(out,name+'.jpg')).catch(()=>null);if(existing){report.views.push({name,faceId:record.faceId,pose,sha256:createHash('sha256').update(existing).digest('hex'),recoveredSameBuildCapture:true});return;}await command(pose);const r=await send('Page.captureScreenshot',{format:'jpeg',quality:96});const bytes=Buffer.from(r.data,'base64');await fs.writeFile(path.join(out,name+'.jpg'),bytes);report.views.push({name,faceId:record.faceId,pose,sha256:createHash('sha256').update(bytes).digest('hex')});await fs.writeFile(path.join(out,'captures.json'),JSON.stringify(report,null,2)+'\n');}

async function key(value,down){await send('Input.dispatchKeyEvent',{type:down?'keyDown':'keyUp',key:value,code:'Key'+value.toUpperCase(),windowsVirtualKeyCode:value.toUpperCase().charCodeAt(0)});}
async function tap(value){await key(value,true);await key(value,false);await delay(400);}
const stats=()=>evaluate('window.seventhStats');
async function shot(name){const r=await send('Page.captureScreenshot',{format:'jpeg',quality:96});await fs.writeFile(path.join(out,name+'.jpg'),Buffer.from(r.data,'base64'));report.views.push({name,stats:await stats()});await fs.writeFile(path.join(out,'captures.json'),JSON.stringify(report,null,2)+'\n');}
async function routeReview(){
 report.routes=[];report.boundaries=[];report.cameras=[];
 await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});report.viewport=[1440,1000,1];
 while((await stats()).camera!==0)await tap('c');
 for(const [name,x,z,yaw,end,direction,axis] of [
  // Browser polling adds travel before braking; leave six more meters than
  // frame-exact native endpoints, while still traversing the street junctions.
  ['first-connection-north',0,-159,0,-285,-1,2],['first-connection-south',0,-310,Math.PI,-177,1,2],
  ['eleventh-west',0,-304.3,Math.PI/2,-182,-1,0],['eleventh-east',-202,-304.3,-Math.PI/2,-18,1,0],
  ['tenth-whole-west',198,-228,Math.PI/2,-172,-1,0],['tenth-whole-east',-202,-228,-Math.PI/2,178,1,0],
  ['ninth-through-first-west',45,-154.7,Math.PI/2,-45,-1,0],['ninth-through-first-east',-45,-154.7,-Math.PI/2,45,1,0],
  ['west-first-lane-north',-6,-160,0,-285,-1,2],['east-first-lane-south',6,-309,Math.PI,-178,1,2]
 ]){
  if(process.env.BOROUGH_ROUTE_ONLY&&name!==process.env.BOROUGH_ROUTE_ONLY)continue;
  await command({type:'pose',x,z,yaw});await delay(500);const before=await stats();
  await evaluate('window.e10Frames=[];window.e10Sampling=true;window.e10Last=performance.now();function e10Tick(t){if(!e10Sampling)return;e10Frames.push(t-e10Last);e10Last=t;requestAnimationFrame(e10Tick)}requestAnimationFrame(e10Tick)');
  await key('w',true);const start=Date.now();
  try{while(direction*((await stats()).position[axis]-end)<0){if(Date.now()-start>=25000){report.failedRoute={name,before,after:await stats()};await shot('failed-'+name);throw Error('Route stalled '+name+' at '+JSON.stringify(report.failedRoute.after.position));}await delay(100);}}
  finally{await key('w',false);await key('s',true);await until('seventhStats.speed<1',7000);await key('s',false);await delay(600);}
  const after=await stats(),frames=await evaluate('e10Sampling=false;e10Frames'),sorted=[...frames].sort((a,b)=>a-b);
  report.currentRoute={name,before,after};assert.equal(after.collisions,before.collisions,name+' contact');assert.equal(after.streaming.holdCount,before.streaming.holdCount,name+' hold');assert.equal(after.addressVisible,false);assert.equal(after.address,'');
  report.routes.push({name,before,after,frames,p95Ms:sorted[Math.ceil(sorted.length*.95)-1],maxMs:sorted.at(-1)});await shot(name);
 }
 for(const [name,x,z,yaw,axis,limit,direction] of [
  ['first-terminal',0,-307,0,2,-315.3,-1],['second-still-closed',-229,-112,0,2,-119,-1],['avenue-a-still-closed',214,-112,0,2,-119,-1],
  ['tenth-west-terminal',-205,-228,Math.PI/2,0,-213,-1],['tenth-east-terminal',199,-228,-Math.PI/2,0,207,1],
  ['ninth-west-terminal',-205,-154.7,Math.PI/2,0,-213,-1],['ninth-east-terminal',199,-154.7,-Math.PI/2,0,207,1],
  ['eleventh-west-terminal',-205,-304.3,Math.PI/2,0,-213,-1],['eleventh-east-terminal',5,-304.3,-Math.PI/2,0,13,1],
  ['first-outer-north',0,-318,0,2,-320.3,-1]
 ]){
  await command({type:'pose',x,z,yaw});const before=await stats(),heldSamples=[];
  await key('w',true);for(let i=0;i<6;i++){await delay(1000);heldSamples.push(await stats());}await key('w',false);await key('s',true);await delay(500);await key('s',false);const after=await stats();
  report.currentBoundary={name,before,after,heldSamples};assert(direction*(after.position[axis]-limit)<.5,name+' escaped');assert(Math.abs(heldSamples.at(-1).position[axis]-heldSamples.at(-2).position[axis])<.05,name+' must stop under held throttle');
  if(name!=='first-outer-north'){assert(direction*(heldSamples.at(-1).position[axis]-before.position[axis])>1,name+' must approach boundary');assert(Math.abs(heldSamples.at(-1).position[axis]-limit)<3,name+' must reach boundary');}
  report.boundaries.push({name,before,after,heldSamples});await shot(name);
 }
 await command({type:'pose',x:-120,z:-304.3,yaw:0});
 for(let mode=0;mode<4;mode++){
  while((await stats()).camera!==mode)await tap('c');const before=await stats();
  await send('Input.dispatchMouseEvent',{type:'mousePressed',x:700,y:480,button:'right',buttons:2});await send('Input.dispatchMouseEvent',{type:'mouseMoved',x:880,y:510,button:'right',buttons:2});await send('Input.dispatchMouseEvent',{type:'mouseReleased',x:880,y:510,button:'right',buttons:0});
  await send('Input.dispatchMouseEvent',{type:'mouseWheel',x:700,y:480,deltaY:250,deltaX:0});await delay(650);const after=await stats();
  assert.equal(after.camera,mode);assert(Math.hypot(after.position[0]-before.position[0],after.position[2]-before.position[2])<.01);assert.equal(after.addressVisible,false);assert.notDeepEqual(after.cameraPose,before.cameraPose);report.cameras.push({mode,before,after});await shot('eleventh-camera-'+mode);
 }
 await command({type:'streamingDump'});report.owners=await evaluate('window.seventhStreamDump');
 for(const id of slice.packetScope.buildingIds){const o=report.owners.treeOwners[id];assert(o&&o.model&&o.collision&&o.children===2,'New model/collision owner '+id);}
 const core=JSON.parse(await fs.readFile('engine/first-seventh/assets/protected-core.json','utf8'));
 for(const [id,o] of Object.entries(report.owners.treeOwners)){assert(o.model);assert.equal(o.collision,o.kind!=='protected-core-details');const r=[...core.buildingOwners,...core.sharedModels].find(r=>String(r.id)===id);if(r)assert.equal(o.kind,r.kind);}
 assert.equal(report.owners.catalogCount,build.modelScenes); // Full catalog; active owners depend on the current camera.
 await tap('r');await until('!seventhStats.relocating && !seventhStats.streaming.cameraHeld && Math.abs(seventhStats.position[0]+.5)<.2 && Math.abs(seventhStats.position[2]-8)<.2',180000);await delay(450);report.reset=await stats();assert(Math.hypot(report.reset.position[0]+.5,report.reset.position[2]-8)<.2);await shot('reset-seventh');
}
try{
 await send('Runtime.enable');await send('Network.enable');await send('Page.enable');
 await send('Emulation.setDeviceMetricsOverride',{width:800,height:800,deviceScaleFactor:1,mobile:false});await send('Emulation.setFocusEmulationEnabled',{enabled:true});await send('Page.bringToFront');await send('Page.navigate',{url});
 await until('window.seventhStats?.ready && document.getElementById("loading")?.hidden',180000);
 assert.equal(await evaluate('seventhStats.buildings'),build.buildings);
 await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});await until('seventhStats.started');
 for(let i=0;i<3&&(await stats()).weather!==0;i++)await tap('t');await delay(1500);
 if(routeMode)await routeReview();
 else{
  for(const record of (process.env.BOROUGH_WELL_ONLY?[]:faces)){
   const id=record.faceId,stem=id.replaceAll(':','-'),f=record.frontage,a=elevations.get(id).architecture;
   await capture(stem+'-elevation',record,{type:'streetFrontage',faceId:id,close:false});
   for(const [label,along,span] of f.length>18?[['ground-west',.20,.40],['ground-middle',.5,.40],['ground-east',.80,.40]]:[['ground',.5,.90]])await capture(stem+'-'+label,record,{type:'streetFrontage',faceId:id,close:true,along,span});
   const mx=f.x+f.rx*f.length*.5,mz=f.z-228+f.rz*f.length*.5;
   if(id==='247851932:0'){
    const x=mx-f.rz*6,z=mz+f.rx*6;
    await capture(stem+'-crest-close',record,{type:'reference',x,z,height:record.height-.10,heading:Math.atan2(mx-x,-(mz-z))*180/Math.PI+29.076863530557524,pitch:0,fov:60});
   }
   for(const [label,offset] of [['mass-left',-5],['mass-right',5]]){
    const distance=14,x=mx-f.rz*distance+f.rx*offset,z=mz+f.rx*distance+f.rz*offset;
    await capture(stem+'-'+label,record,{type:'reference',x,z,height:record.height*.45,heading:Math.atan2(mx-x,-(mz-z))*180/Math.PI+29.076863530557524,pitch:4,fov:78});
   }
   for(const [i,well] of (a.observedGround.basementAreaways||[]).entries()){
    const mx=f.x+f.rx*f.length*well.at,mz=f.z-228+f.rz*f.length*well.at,x=mx-f.rz*3.6,z=mz+f.rx*3.6;
    await capture(stem+'-well-'+i,record,{type:'reference',x,z,height:2.3,heading:Math.atan2(mx-x,-(mz-z))*180/Math.PI+29.076863530557524,pitch:-20,fov:75});
   }
   if(!a.returnShops.length && !id.startsWith('248142975:')){
    for(const [label,offset] of [['access-left',-1.6],['access-right',1.6]]){
     const distance=id==='248142900:0'?7.0:5.8,x=mx-f.rz*distance+f.rx*offset,z=mz+f.rx*distance+f.rz*offset;
     await capture(stem+'-'+label,record,{type:'reference',x,z,height:id==='248142900:0'?3.7:2.7,heading:Math.atan2(mx-x,-(mz-z))*180/Math.PI+29.076863530557524,pitch:-3,fov:83});
    }
   }
   if(id==='248142888:0'){
    const x=mx-f.rz*2.3,z=mz+f.rx*2.3;
    await capture(stem+'-entry-inside-tree',record,{type:'reference',x,z,height:2.0,heading:Math.atan2(mx-x,-(mz-z))*180/Math.PI+29.076863530557524,pitch:0,fov:93});
   }
   if(id==='248142892:0'){
    const px=f.x+f.rx*f.length*.22,pz=f.z-228+f.rz*f.length*.22,x=px-f.rz*2.5,z=pz+f.rx*2.5;
    await capture(stem+'-board',record,{type:'reference',x,z,height:1.1,heading:Math.atan2(px-x,-(pz-z))*180/Math.PI+29.076863530557524,pitch:-10,fov:80});
   }
   if(id==='248142975:1'){
    for(const [label,at] of [['service',.25],['entry',.65],['identity',.84]]){
     const px=f.x+f.rx*f.length*at,pz=f.z-228+f.rz*f.length*at;
     for(const [view,offset] of [['front',0],['left',-1.4],['right',1.4]]){
      const x=px-f.rz*7+f.rx*offset,z=pz+f.rx*7+f.rz*offset;
      await capture(stem+'-'+label+'-'+view,record,{type:'reference',x,z,height:3.5,heading:Math.atan2(px-x,-(pz-z))*180/Math.PI+29.076863530557524,pitch:0,fov:75});
     }
    }
   }
   // Explicit long-facade entries and overlapping upper bays need readable views.
   if(f.length>18){
    for(const [i,entry] of a.doors.entries()){
     const px=f.x+f.rx*f.length*entry.at,pz=f.z-228+f.rz*f.length*entry.at;
     for(const [view,off] of [['front',0],['oblique',1.8]]){
      const x=px-f.rz*5+f.rx*off,z=pz+f.rx*5+f.rz*off;
      await capture(stem+'-entrance-'+i+'-'+view,record,{type:'reference',x,z,height:2.3,heading:Math.atan2(px-x,-(pz-z))*180/Math.PI+29.076863530557524,pitch:0,fov:74});
     }
    }
    for(const along of [.20,.50,.80]){
     const px=f.x+f.rx*f.length*along,pz=f.z-228+f.rz*f.length*along,x=px-f.rz*10,z=pz+f.rx*10;
     await capture(stem+'-upper-'+along,record,{type:'reference',x,z,height:Math.min(12,record.height*.50),heading:Math.atan2(px-x,-(pz-z))*180/Math.PI+29.076863530557524,pitch:10,fov:80});
    }
   }
   console.log('FACADE_CAPTURED',id);
  }
  for(const business of ledger.businesses){
   const record=faces.find(r=>r.faceId===business.faceId);if(!record)continue;
   const f=record.frontage,span=business.span,w=f.length*(span[1]-span[0]),count=Math.max(1,Math.ceil(w/7.5));
   for(let j=0;j<count;j++){
    const along=span[0]+(span[1]-span[0])*(j+.5)/count,mx=f.x+f.rx*f.length*along,mz=f.z-228+f.rz*f.length*along;
    const community=false,inside=['247851924:0','247851927:0','247851930:0'].includes(record.faceId);
    const bowprint=business.businessId==='bowprint';
    const distance=bowprint?2.3:inside?2.4:Math.max(4,Math.min(7.5,(w/count)/(2*Math.tan(34*Math.PI/180))*1.1));
    for(const [view,offset] of [['front',0],['left',-1.3],['right',1.3]]){
     const alongOffset=inside?offset*.35:offset,x=mx-f.rz*distance+f.rx*alongOffset,z=mz+f.rx*distance+f.rz*alongOffset;
     await capture(business.id.replaceAll(':','-')+'-'+j+'-'+view,record,{type:'reference',x,z,height:bowprint?2.9:community?3.5:1.9,heading:Math.atan2(mx-x,-(mz-z))*180/Math.PI+29.076863530557524,pitch:0,fov:bowprint?115:inside?100:72});
     report.views.at(-1).businessId=business.id;
    }
   }
  }

  if(!filter){
   const siteRecord={faceId:'site-01-E11-21'};
   for(const [name,x,z,height,tx,tz,pitch,fov] of [
    ['324-lot-front',-103.2,-302,3,-103.2,-287,0,88],
    ['324-lot-east-oblique',-96.2,-302,3,-103.2,-285,5,88],
    ['324-lot-west-oblique',-111.2,-302,3,-103.2,-285,5,88],
    ['300-304-passage',-176,-301.5,2.5,-176,-285,0,72],
    ['schoolyard-west',-130,-304.3,3,-105,-329,0,88],
    ['schoolyard-east',-63,-304.3,3,-93,-330,0,88],
    ['schoolyard-interior',-100,-319,4,-100,-340,0,88],
    ['school-bike-row',-40,-304,1.8,-40,-311,0,80],
    ['177-mural-oblique',-7,-302,7,-24,-295,8,80],
    ['342-neon-oblique',-48,-303,5,-39,-295,10,75]
   ])await capture(name,siteRecord,{type:'reference',x,z,height,heading:Math.atan2(tx-x,-(tz-z))*180/Math.PI+29.076863530557524,pitch,fov});
  }

 }
 assert.equal(new Set(report.views.map(v=>v.name)).size,report.views.length,'Unique captures');assert.equal(report.errors.length,0,JSON.stringify(report.errors));assert.equal(report.failedRequests.length,0,JSON.stringify(report.failedRequests));report.complete=true;
}finally{await fs.writeFile(path.join(out,'captures.json'),JSON.stringify(report,null,2)+'\n');await fetch(`${cdp}/json/close/`+tab.id).catch(()=>{});ws.close();}
