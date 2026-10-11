// Capture exact building:face records from the bounded revision 08 export.
// Captures never automatically award photographic or visual acceptance.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const out=path.resolve(process.argv[2]||'renders/first-stmarks-08');
const filter=process.argv[3]?.split(',');
const slice=JSON.parse(await fs.readFile('engine/first-seventh/assets/slice.json','utf8'));
const build=JSON.parse(await fs.readFile('dist/seventh/build.json','utf8'));
const faces=slice.streetReviewFrontages.filter(r=>!filter||filter.includes(r.faceId));
assert(faces.length,'No scheduled review faces');
if(filter)assert.equal(faces.length,new Set(filter).size,'Unknown review face');
await fs.mkdir(out,{recursive:true});
const report={date:new Date().toISOString(),scope:'Scheduled First Avenue / St. Marks faces only',build,viewport:[800,800,1],acceptance:'Capture only; visual review must be recorded separately.',errors:[],warnings:[],failedRequests:[],views:[]};
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
try{
 await send('Runtime.enable');await send('Network.enable');await send('Page.enable');
 await send('Emulation.setDeviceMetricsOverride',{width:800,height:800,deviceScaleFactor:1,mobile:false});
 await send('Emulation.setFocusEmulationEnabled',{enabled:true});await send('Page.bringToFront');
 await send('Page.navigate',{url:'http://127.0.0.1:5173/seventh/?review=1'});
 await until('window.seventhStats?.ready && document.getElementById("loading")?.hidden');
 assert.equal(await evaluate('seventhStats.buildings'),slice.buildings.length);
 await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
 await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});await until('seventhStats.started');
 for(let i=0;i<3&&(await evaluate('seventhStats.weather'))!==0;i++){
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'t',code:'KeyT',windowsVirtualKeyCode:84});await send('Input.dispatchKeyEvent',{type:'keyUp',key:'t',code:'KeyT',windowsVirtualKeyCode:84});await delay(500);
 }
 await delay(1500);
 for(const record of faces){
  const name=record.faceId.replace(':','-');
  await capture(name+'-elevation',record,{type:'streetFrontage',faceId:record.faceId});
  const count=Math.max(1,Math.ceil(record.frontage.length/8));
  for(let j=0;j<count;j++)await capture(name+'-ground-'+j,record,{type:'streetFrontage',faceId:record.faceId,close:true,along:(j+.5)/count,span:1/count});
  console.log('STREET_CAPTURED',record.faceId);
 }
 assert.equal(report.errors.length,0,JSON.stringify(report.errors));assert.equal(report.failedRequests.length,0,JSON.stringify(report.failedRequests));report.complete=true;
}finally{await fs.writeFile(path.join(out,'captures.json'),JSON.stringify(report,null,2)+'\n');await fetch('http://127.0.0.1:9222/json/close/'+tab.id).catch(()=>{});ws.close();}
