// Dependency-free client for the existing, isolated local review browser.
import fs from 'node:fs/promises';
export const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
export async function reviewClient(){
 const base=process.env.BOROUGH_CDP||'http://127.0.0.1:9222';
 const tab=await(await fetch(base+'/json/new?about:blank',{method:'PUT'})).json();
 const ws=new WebSocket(tab.webSocketDebuggerUrl),pending=new Map(),listeners=new Map();let sequence=0,commandSequence=0;
 await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p?.reject(m.error):p?.resolve(m.result);}else for(const f of listeners.get(m.method)||[])f(m.params);};
 const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++sequence,timer=setTimeout(()=>{pending.delete(id);reject(Error('CDP timeout: '+method));},30000);pending.set(id,{resolve:v=>{clearTimeout(timer);resolve(v);},reject:e=>{clearTimeout(timer);reject(e);}});ws.send(JSON.stringify({id,method,params}));});
 const on=(name,fn)=>listeners.set(name,[...(listeners.get(name)||[]),fn]);
 async function evaluate(expression){const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result?.value;}
 async function until(expression,timeout=180000){const start=Date.now();while(Date.now()-start<timeout){if(await evaluate(expression))return;await delay(150);}throw Error('Timeout: '+expression);}
 async function key(value,down){await send('Input.dispatchKeyEvent',{type:down?'keyDown':'keyUp',key:value,code:value.length===1?'Key'+value.toUpperCase():value,windowsVirtualKeyCode:value==='Enter'?13:value.toUpperCase().charCodeAt(0)});}
 async function tap(value){await key(value,true);await delay(60);await key(value,false);await delay(400);}
 async function submit(value){const n=++commandSequence;await evaluate('window.seventhReviewCommand='+JSON.stringify({...value,sequence:n}));return n;}
 async function command(value){const n=await submit(value);await until('window.seventhReviewAck==='+n);await delay(400);}
 async function shot(file){const r=await send('Page.captureScreenshot',{format:'png'});await fs.writeFile(file,Buffer.from(r.data,'base64'));}
 async function dump(){await command({type:'streamingDump'});return evaluate('window.seventhStreamDump');}
 async function open(url,width=1440,height=1000,cacheDisabled=true){await send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:false});await send('Network.setCacheDisabled',{cacheDisabled});await send('Page.navigate',{url});await until('window.seventhStats?.ready && document.getElementById("loading")?.hidden');return evaluate('({readyMs:seventhReadyMs,stats:seventhStats})');}
 await send('Runtime.enable');await send('Page.enable');await send('Network.enable');await send('Emulation.setFocusEmulationEnabled',{enabled:true});await send('Page.bringToFront');
 return {send,on,evaluate,until,key,tap,command,submit,shot,dump,open,stats:()=>evaluate('window.seventhStats'),close:async()=>{await fetch(base+'/json/close/'+tab.id).catch(()=>{});ws.close();}};
}
