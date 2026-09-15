// Reproducible photographic-camera and entrance review. Does not fetch imagery,
// accept a facade, modify the game, or contact a model/paid service.
// Start npm run dev and the isolated Chromium CDP review browser on port 9222.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const out=path.resolve(process.argv[2]||'renders/seventh-engine-03/fidelity');
const filter=process.argv[3]?.split(',').map(Number);
const root=new URL('../',import.meta.url);
const read=async name=>JSON.parse(await fs.readFile(new URL(name,root),'utf8'));
const source=await read('model-source/storefront-details.json');
const geo=await read('dist/reconstruction/neighborhood.json');
const build=await read('dist/seventh/build.json');
const engine=source.seventhEngine;
const calibration=await read('model-source/seventh-fidelity-camera-03.json');
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
await fs.mkdir(out,{recursive:true});
const report={checked:new Date().toISOString(),build,viewport:[640,640,1],
  basis:'Actual engine captures. Panorama latitude/longitude, heading, pitch and horizontal FOV reproduced; camera height estimated at 2.5 m. These do not prove visual or surveyed accuracy.',
  errors:[],warnings:[],failedRequests:[],views:[]};
const tab=await(await fetch('http://127.0.0.1:9222/json/new?about:blank',{method:'PUT'})).json();
const ws=new WebSocket(tab.webSocketDebuggerUrl),pending=new Map();let sequence=0,commandSequence=0;
await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
ws.onmessage=e=>{
  const m=JSON.parse(e.data);
  if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p?.reject(m.error):p?.resolve(m.result);return;}
  if(m.method==='Runtime.exceptionThrown')report.errors.push(m.params.exceptionDetails);
  if(m.method==='Runtime.consoleAPICalled'&&['error','warning'].includes(m.params.type))report[m.params.type==='error'?'errors':'warnings'].push(m.params.args.map(a=>a.value||a.description||'').join(' '));
  if(m.method==='Network.responseReceived'&&m.params.response.status>=400)report.failedRequests.push([m.params.response.status,m.params.response.url]);
};
const send=(method,params={})=>new Promise((resolve,reject)=>{
  const id=++sequence,timer=setTimeout(()=>{pending.delete(id);reject(Error('CDP timeout: '+method));},30000);
  pending.set(id,{resolve:v=>{clearTimeout(timer);resolve(v);},reject:e=>{clearTimeout(timer);reject(e);}});
  ws.send(JSON.stringify({id,method,params}));
});
async function evaluate(expression){const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result?.value;}
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function until(expression,timeout=90000){const start=Date.now();while(Date.now()-start<timeout){if(await evaluate(expression))return;await delay(200);}throw Error('Timeout: '+expression);}
async function command(value){const sequence=++commandSequence;await evaluate('window.seventhReviewCommand='+JSON.stringify({...value,sequence}));await until('window.seventhReviewAck==='+sequence,6000);await delay(350);}
async function capture(name,details){const result=await send('Page.captureScreenshot',{format:'png'});const bytes=Buffer.from(result.data,'base64');await fs.writeFile(path.join(out,name+'.png'),bytes);report.views.push({name,...details,sha256:hash(bytes),stats:await evaluate('window.seventhStats')});}
try{
  await send('Runtime.enable');await send('Network.enable');await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride',{width:640,height:640,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url:'http://127.0.0.1:5173/seventh/?review=1'});
  await until('window.seventhStats?.ready && document.getElementById("loading")?.hidden');
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
  await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
  await until('window.seventhStats?.started');
  // A fixed weather state makes successive model revisions comparable.
  for(let i=0;i<3&&(await evaluate('seventhStats.weather'))!==0;i++){
    await send('Input.dispatchKeyEvent',{type:'keyDown',key:'t',code:'KeyT',windowsVirtualKeyCode:84});
    await send('Input.dispatchKeyEvent',{type:'keyUp',key:'t',code:'KeyT',windowsVirtualKeyCode:84});await delay(500);
  }
  await delay(1500);
  const angle=geo.axis.avenueBearing*Math.PI/180,cs=Math.cos(angle),sn=Math.sin(angle);
  const referenceEntries=Object.entries(engine.sources).filter(([id,r])=>id.startsWith('seventh-03-')&&r.panoramaId&&r.views&&r.location);
  for(const [id,ref] of referenceEntries){
    if(filter && !['seventh-03-streetview-50','seventh-03-streetview-48'].includes(id))continue;
    const e=(ref.location.lon-geo.origin.lon)*111320*Math.cos(geo.origin.lat*Math.PI/180),n=(ref.location.lat-geo.origin.lat)*111320;
    for(let i=0;i<ref.views.length;i++){
      const view=ref.views[i];const pose={type:'reference',x:e*cs-n*sn,z:-e*sn-n*cs-228,height:2.5,...view};
      await command(pose);await capture(`${id}-${i}`,{projection:'perspective',source:id,panoramaId:ref.panoramaId,captureDate:ref.captureDate,pose});
    }
  }
  // Keep the raw metadata captures above. This separately labeled pose fit
  // exposes GPS/camera uncertainty instead of silently moving the reference.
  await command({type:'reference',...calibration.fittedCamera,...calibration.view});
  await capture('church-pose-fit',{projection:'perspective diagnostic pose fit',calibration,
    limitation:'One-view approximate manual landmarks; not independent multi-view acceptance.'});
  for(const r of engine.elevations){
    if(filter&&!filter.includes(r.buildingId))continue;
    const doors=r.architecture?.doors?.length?r.architecture.doors:[{at:.5}];
    for(let i=0;i<doors.length;i++){
      await command({type:'frontage',id:r.buildingId,close:true,along:doors[i].at,span:.46});
      await capture('entry-'+r.buildingId+(i?'-'+i:''),{buildingId:r.buildingId,entranceIndex:i,address:r.address,projection:'perspective frontage closeup; not matched to a photograph'});
    }
  }
  const after=await read('dist/seventh/build.json');assert.equal(after.files['index.pck'].sha256,build.files['index.pck'].sha256,'build changed during capture');
  assert.equal(report.errors.length,0);assert.equal(report.failedRequests.length,0);
  report.completed=true;
}finally{
  await fs.writeFile(path.join(out,'review.json'),JSON.stringify(report,null,2)+'\n');
  await fetch('http://127.0.0.1:9222/json/close/'+tab.id).catch(()=>{});ws.close();
}
console.log('SEVENTH_FIDELITY_CAPTURES',report.views.length);
