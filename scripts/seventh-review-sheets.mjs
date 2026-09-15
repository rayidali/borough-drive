// Contact sheets of actual game elevation captures; no reference-photo pixels.
// Run after native --facade-review, while no browser performance test is active.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const folder=path.resolve(process.argv[2]||'renders/seventh-engine-03/elevations-optimized');
const slice=JSON.parse(await fs.readFile(new URL('../engine/first-seventh/assets/slice.json',import.meta.url),'utf8'));
const escape=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
const tab=await(await fetch('http://127.0.0.1:9222/json/new?about:blank',{method:'PUT'})).json();
const ws=new WebSocket(tab.webSocketDebuggerUrl),pending=new Map();let seq=0;
await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p?.reject(m.error):p?.resolve(m.result);}};
const send=(method,params={})=>new Promise((resolve,reject)=>{
  const id=++seq,timer=setTimeout(()=>{pending.delete(id);reject(Error('CDP timeout: '+method));},30000);
  pending.set(id,{resolve:r=>{clearTimeout(timer);resolve(r);},reject:e=>{clearTimeout(timer);reject(e);}});ws.send(JSON.stringify({id,method,params}));
});
try{
  await send('Page.enable');await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride',{width:2100,height:990,deviceScaleFactor:1,mobile:false});
  for(let i=0;i<slice.reviewFrontages.length;i+=6){
    const entries=slice.reviewFrontages.slice(i,i+6),file=path.join(folder,`sheet-${i/6}.html`);
    for(const e of entries)await fs.access(path.join(folder,`facade-${e.id}.png`));
    await fs.writeFile(file,'<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#f1efeb;display:grid;grid-template-columns:repeat(3,700px);font:18px system-ui}figure{margin:4px;height:482px}figcaption{height:24px}img{width:692px;height:452px;object-fit:contain}</style>'+entries.map(e=>`<figure><figcaption>${escape(e.address)} · ${e.id}</figcaption><img src="facade-${e.id}.png"></figure>`).join(''));
    await send('Page.navigate',{url:pathToFileURL(file).href});
    let ready=false;
    for(let attempt=0;attempt<100;attempt++){
      const r=await send('Runtime.evaluate',{expression:`location.href===${JSON.stringify(pathToFileURL(file).href)} && document.images.length===${entries.length} && [...document.images].every(i=>i.complete && i.naturalWidth>0)`,returnByValue:true});
      if(r.result?.value){ready=true;break;}await new Promise(r=>setTimeout(r,100));
    }
    if(!ready)throw Error('Images not loaded: '+file);
    const r=await send('Page.captureScreenshot',{format:'webp',quality:92});
    await fs.writeFile(path.join(folder,`sheet-${i/6}.webp`),Buffer.from(r.data,'base64'));
  }
}finally{await fetch('http://127.0.0.1:9222/json/close/'+tab.id).catch(()=>{});ws.close();}
console.log('SEVENTH_REVIEW_SHEETS',Math.ceil(slice.reviewFrontages.length/6));
