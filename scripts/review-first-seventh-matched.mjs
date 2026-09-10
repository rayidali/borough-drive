// Actual local game views at the reference panorama locations/headings/FOVs.
// Google image pixels/keys never enter this tool or the generated game captures.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const out=path.resolve(process.argv[2]||'renders/first-seventh-matched');
await fs.mkdir(out,{recursive:true});
const model=JSON.parse(await fs.readFile(new URL('../dist/reconstruction/neighborhood.json',import.meta.url)));
const sources=JSON.parse(await fs.readFile(new URL('../model-source/first-seventh-street-view-08.json',import.meta.url))).sources;
const views=[
 ['tile-corner','sv08-west-corner',335,12,78],['smoke-corner','sv08-west-corner',245,12,78],
 ['saifee-corner','sv08-west-corner',135,14,80],['deli-first','sv08-first-north',112,10,88],
 ['deli-return','sv08-seventh-middle',29,20,100],['saifee-return','sv08-seventh-middle',209,20,100],
 ['saifee-shop','sv08-west-corner',142,2,48],['tile-return','sv08-west-corner',340,2,48],
 ['monkey-and-hen','sv08-first-north',115,0,58],['e7-deli','sv08-east-corner',29.72,5,90],
 ['yubu-obscured-reference','sv08-yubu',170,3,80],
];
const report={checkedAt:new Date().toISOString(),viewport:{width:900,height:900,deviceScaleFactor:1},
 cameraHeight:2.50,cameraHeightBasis:'estimated Street View capture height; no survey',
 comparison:'Same reported panorama GPS, compass heading, pitch and horizontal field of view; independent game lighting and estimated camera height.',
 errors:[],failedRequests:[],views:[]};
const tab=await(await fetch('http://127.0.0.1:9222/json/new?about:blank',{method:'PUT'})).json();
const ws=new WebSocket(tab.webSocketDebuggerUrl),pending=new Map(),listeners=new Map();let id=0;
await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result);}else for(const f of listeners.get(m.method)||[])f(m.params);};
const on=(name,f)=>listeners.set(name,[...(listeners.get(name)||[]),f]);
const send=(method,params={})=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params}));});
async function evaluate(expression){const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(r.exceptionDetails.text);return r.result?.value;}
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function until(expression){const start=Date.now();while(Date.now()-start<90000){if(await evaluate(expression))return;await delay(250);}throw Error('Matched review timed out');}
on('Runtime.exceptionThrown',e=>report.errors.push(e.exceptionDetails.text));
on('Network.responseReceived',e=>{if(e.response.status>=400)report.failedRequests.push([e.response.status,e.response.url]);});
try{
 for(const method of ['Page.enable','Runtime.enable','Network.enable','Debugger.enable'])await send(method);
 await send('Emulation.setDeviceMetricsOverride',{...report.viewport,mobile:false});
 const source=await fs.readFile(new URL('../dist/reconstruction/viewer.js',import.meta.url),'utf8');
 const lineNumber=source.split('\n').findIndex(s=>s.includes('ready=true;returnToStart()'));assert(lineNumber>0);
 await send('Debugger.setBreakpointByUrl',{urlRegex:'/reconstruction/viewer\\.js$',lineNumber});
 on('Debugger.paused',async e=>{try{await send('Debugger.evaluateOnCallFrame',{callFrameId:e.callFrames[0].callFrameId,expression:`
  globalThis.__matched={pose:()=>({ready,x:camera.position.x,y:camera.position.y,z:camera.position.z,yaw,pitch,fov:camera.fov,pending:[...neighborhood.states.values()].some(s=>s.promise)}),
   view:(x,z,h,p,f)=>{setMode('walk',false);travel(x,z);camera.position.set(x,2.50,z);yaw=targetYaw=(h-${model.axis.avenueBearing})*Math.PI/180;pitch=targetPitch=p*Math.PI/180;camera.fov=f;camera.updateProjectionMatrix();renderDirty=true;neighborhood.update(x,z,performance.now());}};
  walk=()=>{};
 `});}finally{await send('Debugger.resume');}});
 await send('Page.navigate',{url:'http://127.0.0.1:5173'});
 await until('globalThis.__matched?.pose().ready && document.querySelector("#loading").hidden');
 await send('Debugger.disable');
 await evaluate(`document.querySelector('#quality').value='detail';document.querySelector('#quality').dispatchEvent(new Event('change'));const style=document.createElement('style');style.textContent='#app > :not(#world){visibility:hidden!important}';document.head.append(style);`);
 const angle=model.axis.avenueBearing*Math.PI/180,cs=Math.cos(angle),sn=Math.sin(angle);
 for(const [name,key,heading,pitch,fov] of views){
  const ref=sources[key],e=(ref.location.lon-model.origin.lon)*111320*Math.cos(model.origin.lat*Math.PI/180),n=(ref.location.lat-model.origin.lat)*111320;
  const x=e*cs-n*sn,z=-e*sn-n*cs;
  await evaluate(`__matched.view(${x},${z},${heading},${pitch},${fov})`);
  await until('!__matched.pose().pending');await delay(1100);
  const screenshot=await send('Page.captureScreenshot',{format:'png'});
  await fs.writeFile(path.join(out,name+'.png'),Buffer.from(screenshot.data,'base64'));
  report.views.push({name,source:key,imageryDate:ref.captureDate,heading,pitch,fov,pose:await evaluate('__matched.pose()')});
  console.log('MATCHED_VIEW',name);
 }
 await fs.writeFile(path.join(out,'review.json'),JSON.stringify(report,null,2)+'\n');
 assert.equal(report.errors.length,0);assert.equal(report.failedRequests.length,0);
}finally{await fetch('http://127.0.0.1:9222/json/close/'+tab.id).catch(()=>{});ws.close();}
