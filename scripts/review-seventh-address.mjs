// Focused browser check for the bounded Seventh Street address HUD.
// Export first, then run with npm run dev and an isolated Chromium on port 9222.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';

const out=path.resolve(process.argv[2]||'renders/seventh-engine/address-review');
const url=process.env.BOROUGH_REVIEW_URL||'http://127.0.0.1:5173/seventh/?review=1';
await fs.mkdir(out,{recursive:true});
const tab=await(await fetch('http://127.0.0.1:9222/json/new?about:blank',{method:'PUT'})).json();
const ws=new WebSocket(tab.webSocketDebuggerUrl),pending=new Map(),listeners=new Map();let id=0;
await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p?.reject(m.error):p?.resolve(m.result);}else for(const f of listeners.get(m.method)||[])f(m.params);};
const send=(method,params={})=>new Promise((resolve,reject)=>{const n=++id,t=setTimeout(()=>{pending.delete(n);reject(Error('CDP timeout: '+method));},30000);pending.set(n,{resolve:v=>{clearTimeout(t);resolve(v);},reject:e=>{clearTimeout(t);reject(e);}});ws.send(JSON.stringify({id:n,method,params}));});
const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result?.value;};
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const until=async(expression,timeout=120000)=>{const start=Date.now();while(Date.now()-start<timeout){if(await evaluate(expression))return;await sleep(250);}throw Error('Timeout: '+expression);};
let sequence=0;
async function command(value){const n=++sequence;await evaluate('window.seventhReviewCommand='+JSON.stringify({...value,sequence:n}));await until('window.seventhReviewAck==='+n,5000);await sleep(450);}
async function screenshot(name){const r=await send('Page.captureScreenshot',{format:'png'});await fs.writeFile(path.join(out,name+'.png'),Buffer.from(r.data,'base64'));}

const cases=[
  {name:'second-corner',x:-219,z:-9,yaw:-Math.PI/2,address:'118 2ND AVE'},
  {name:'half-address',x:-180,z:9,yaw:-Math.PI/2,address:'48 1/2 E 7TH ST'},
  {name:'south-property',x:-170,z:9,yaw:-Math.PI/2,address:'50 E 7TH ST'},
  {name:'north-property',x:-170,z:-9,yaw:-Math.PI/2,address:'49 E 7TH ST'},
  {name:'big-bar',x:-75,z:-5,yaw:-Math.PI/2,address:'73-75 E 7TH ST'},
  {name:'first-corner',x:-10,z:-9,yaw:-Math.PI/2,address:'115 1ST AVE'},
  {name:'second-edge',x:-226,z:0,yaw:-Math.PI/2,address:''},
  {name:'first-edge',x:-3,z:0,yaw:-Math.PI/2,address:''},
  {name:'east-first-edge',x:3,z:0,yaw:-Math.PI/2,address:''},
  {name:'east-north',x:39,z:-9,yaw:-Math.PI/2,address:'93 E 7TH ST'},
  {name:'east-corrected-109',x:98,z:-9,yaw:-Math.PI/2,address:'109 E 7TH ST'},
  {name:'east-corrected-116',x:130,z:9,yaw:-Math.PI/2,address:'116 E 7TH ST'},
  {name:'east-mckinley',x:113,z:-9,yaw:-Math.PI/2,address:'111–115 E 7TH ST'},
  {name:'east-avenue-a-return',x:195,z:-9,yaw:-Math.PI/2,address:'111 AVE A'},
  {name:'avenue-a-edge',x:212,z:0,yaw:-Math.PI/2,address:''},
  {name:'beyond-avenue-a',x:237,z:0,yaw:-Math.PI/2,address:''},
  {name:'st-marks',x:-170,z:-77.9,yaw:-Math.PI/2,address:''},
];
const report={date:new Date().toISOString(),url,cases:[],branding:{}};
try{
  await send('Page.enable');await send('Page.bringToFront');await send('Runtime.enable');await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url});await until('window.seventhStats?.ready && document.getElementById("loading").hidden');
  report.branding=await evaluate('({title:document.title,description:document.querySelector("meta[name=description]")?.content,canvasLabel:document.querySelector("#canvas")?.getAttribute("aria-label")})');
  assert(report.branding.title.includes('DriveAround.nyc'),'Seventh title should use the DriveAround.nyc brand');
  await evaluate('window.seventhReviewCommand={type:"pose",x:-12,z:0,yaw:-Math.PI/2,sequence:1}');await until('window.seventhReviewAck===1');
  await evaluate('document.querySelector("#canvas").focus()');await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});await sleep(500);
  for(const c of cases){await command({type:'pose',x:c.x,z:c.z,yaw:c.yaw});const stats=await evaluate('window.seventhStats');assert.equal(stats.address,c.address,c.name+' address');assert.equal(stats.addressVisible,c.address!=='',c.name+' visibility');if(c.address)assert.notEqual(stats.addressId,0,c.name+' mapped address id');else assert.equal(stats.addressId,0,c.name+' address id reset');await screenshot(c.name);report.cases.push({name:c.name,expected:c.address,stats});}
  await fs.writeFile(path.join(out,'review.json'),JSON.stringify(report,null,2)+'\n');console.log('SEVENTH_ADDRESS_BROWSER_REVIEW_COMPLETE',out);
}finally{await fs.writeFile(path.join(out,'review.json'),JSON.stringify(report,null,2)+'\n');await fetch('http://127.0.0.1:9222/json/close/'+tab.id).catch(()=>{});ws.close();}
