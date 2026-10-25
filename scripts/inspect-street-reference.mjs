// Inspect ordinary browser reference pages; source screenshots stay local.
import fs from 'node:fs/promises';
import path from 'node:path';
const [input] = process.argv.slice(2);
if (!input) throw Error('Usage: node scripts/inspect-street-reference.mjs <local-request.json>');
const requests = JSON.parse(await fs.readFile(input, 'utf8'));
for (const request of Array.isArray(requests) ? requests : [requests]) {
const output = path.resolve(request.output);
const allowed = path.resolve('.tools/street-references') + path.sep;
if (!output.startsWith(allowed)) throw Error('Reference pixels must remain under .tools/street-references/');
const base = 'http://127.0.0.1:9222';
const tab = await (await fetch(base + '/json/new?about:blank', {method:'PUT'})).json();
const ws = new WebSocket(tab.webSocketDebuggerUrl), pending = new Map(); let id = 0;
await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
ws.onmessage = e => {const m=JSON.parse(e.data); if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p?.reject(m.error):p?.resolve(m.result);}};
const send = (method,params={}) => new Promise((resolve,reject)=>{const n=++id,t=setTimeout(()=>{pending.delete(n);reject(Error(method+' timed out'));},30000);pending.set(n,{resolve:v=>{clearTimeout(t);resolve(v);},reject:e=>{clearTimeout(t);reject(e);}});ws.send(JSON.stringify({id:n,method,params}));});
try {
 await send('Page.enable'); await send('Runtime.enable');
 await send('Emulation.setDeviceMetricsOverride',{width:request.width||1600,height:request.height||1100,deviceScaleFactor:1,mobile:false});
 await send('Page.bringToFront'); await send('Page.navigate',{url:request.url});
 await new Promise(r=>setTimeout(r,request.waitMs||13000));
 for (const point of request.clickPoints || []) {
  await send('Input.dispatchMouseEvent',{type:'mousePressed',x:point[0],y:point[1],button:'left',clickCount:1});
  await send('Input.dispatchMouseEvent',{type:'mouseReleased',x:point[0],y:point[1],button:'left',clickCount:1});
  await new Promise(r=>setTimeout(r,3500));
 }
 for (const label of request.clickTexts || []) {
  const expression=`(()=>{const el=[...document.querySelectorAll('button,a')].find(e=>e.innerText.trim()===${JSON.stringify(label)});if(!el)throw Error('Missing visible control');el.click();return el.innerText;})()`;
  const result=await send('Runtime.evaluate',{expression,returnByValue:true});
  if(result.exceptionDetails) throw Error('Reference control unavailable: '+label);
  await new Promise(r=>setTimeout(r,2500));
 }
 if (request.keys?.length) {
  await send('Runtime.evaluate',{expression:'document.activeElement?.blur(); const s=document.querySelector(".widget-scene")||document.body; s.tabIndex=0; s.focus();'});
 }
 for (const key of request.keys || []) {
  const code=key.length===1?'Key'+key.toUpperCase():key;
  const keyCode={ArrowUp:38,ArrowDown:40,ArrowLeft:37,ArrowRight:39}[key] || key.toUpperCase().charCodeAt(0);
  await send('Input.dispatchKeyEvent',{type:'rawKeyDown',key,code,windowsVirtualKeyCode:keyCode});
  await send('Input.dispatchKeyEvent',{type:'keyUp',key,code,windowsVirtualKeyCode:keyCode});
  await new Promise(r=>setTimeout(r,2400));
 }
 const info = await send('Runtime.evaluate',{expression:'({title:document.title,url:location.href,text:document.body.innerText.slice(0,10000),canvasCount:document.querySelectorAll("canvas").length})',returnByValue:true});
 const shot = await send('Page.captureScreenshot',{format:'jpeg',quality:94});
 await fs.mkdir(path.dirname(output),{recursive:true});
 await fs.writeFile(output+'.jpg',Buffer.from(shot.data,'base64'));
 const report={inspectedAt:new Date().toISOString(),requestedUrl:request.url,...info.result.value,image:output+'.jpg',state:'captured; visual inspection pending'};
 await fs.writeFile(output+'.json',JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({image:report.image,title:report.title,url:report.url,state:report.state}));
} finally {
 ws.close();
 await fetch(base+'/json/close/'+tab.id).catch(()=>{});
}
}
