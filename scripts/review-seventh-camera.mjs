// Bounded browser review for camera-only inspection controls. Export first,
// then run with npm run dev and an isolated Chromium on port 9222.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';

const out = path.resolve(process.argv[2] || 'renders/seventh-engine/camera-review');
const url = process.env.BOROUGH_REVIEW_URL || 'http://127.0.0.1:5173/seventh/?review=1';
const build = JSON.parse(await fs.readFile(path.resolve('dist/seventh/build.json'),'utf8'));
await fs.mkdir(out, {recursive:true});
const tab = await (await fetch('http://127.0.0.1:9222/json/new?about:blank', {method:'PUT'})).json();
const ws = new WebSocket(tab.webSocketDebuggerUrl), pending = new Map(); let id = 0;
await new Promise((resolve,reject) => {ws.onopen=resolve;ws.onerror=reject;});
ws.onmessage = event => {const m=JSON.parse(event.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p?.reject(m.error):p?.resolve(m.result);}};
const send=(method,params={})=>new Promise((resolve,reject)=>{const n=++id,t=setTimeout(()=>{pending.delete(n);reject(Error('CDP timeout: '+method));},30000);pending.set(n,{resolve:v=>{clearTimeout(t);resolve(v);},reject:e=>{clearTimeout(t);reject(e);}});ws.send(JSON.stringify({id:n,method,params}));});
const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result?.value;};
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const until=async(expression,timeout=120000)=>{const start=Date.now();while(Date.now()-start<timeout){if(await evaluate(expression))return;await sleep(250);}throw Error('Timeout: '+expression);};
const keycodes={Enter:13,Escape:27,Space:32};
async function key(key,down,modifiers=0){await send('Input.dispatchKeyEvent',{type:down?'keyDown':'keyUp',key:key==='Space'?' ':key,code:key.length===1?'Key'+key.toUpperCase():key,modifiers,windowsVirtualKeyCode:keycodes[key]||key.toUpperCase().charCodeAt(0)});}
async function tap(value){await key(value,true);await sleep(70);await key(value,false);await sleep(350);}
async function mouse(type,x,y,button='none',modifiers=0,deltaY=0){
  const event={type,x,y,button,buttons:type==='mouseReleased'?0:(button==='right'?2:button==='middle'?4:0),modifiers};
  if(type==='mouseWheel'){event.deltaX=0;event.deltaY=deltaY;}
  await send('Input.dispatchMouseEvent',event);
}
async function dragBy(button,dx,dy,modifiers=0){await mouse('mousePressed',700,480,button,modifiers);await mouse('mouseMoved',700+dx,480+dy,button,modifiers);await mouse('mouseReleased',700+dx,480+dy,button,modifiers);await sleep(450);}
async function drag(button,modifiers=0){await dragBy(button,60,-50,modifiers);}
async function screenshot(name){const result=await send('Page.captureScreenshot',{format:'png'});await fs.writeFile(path.join(out,name+'.png'),Buffer.from(result.data,'base64'));}
async function panReleaseOverHud(dx=80,dy=-60){
  await mouse('mousePressed',700,480,'middle');
  await mouse('mouseMoved',700+dx,480+dy,'middle');
  // The bottom bar is a Control layer in the exported shell. This release
  // verifies that a consumed release cannot leave camera panning latched.
  await mouse('mouseReleased',720,965,'middle');
  await sleep(450);
}
const stats=()=>evaluate('window.seventhStats');
let sequence=0;
async function command(value){const n=++sequence;await evaluate('window.seventhReviewCommand='+JSON.stringify({...value,sequence:n}));await until('window.seventhReviewAck==='+n,5000);await sleep(300);}
const report={date:new Date().toISOString(),url,build,checks:{},modes:[]};
try {
  await send('Page.enable');await send('Runtime.enable');await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url});await until('window.seventhStats?.ready');
  const label=await evaluate('document.querySelector("#canvas")?.getAttribute("aria-label")||""');
  assert(label.includes('Shift plus right-drag')&&label.includes('mouse wheel')&&label.includes('V recenters'),'Shell must expose camera inspection controls');report.checks.controlLabel=true;
  // Mouse gestures before Start must not alter the camera on the intro menu.
  await drag('right');await mouse('mouseWheel',700,480,'none',0,-120);await tap('Enter');
  let initial=await stats();assert.equal(initial.started,true);assert(Math.abs(initial.cameraPose.yaw)<.001&&Math.abs(initial.cameraPose.pitch)<.001,'Menu input must not capture camera inspection');report.checks.menuInput=true;
  await command({type:'pose',x:-120,z:0,yaw:-Math.PI/2});
  const modes=[];
  for(let i=0;i<4;i++){
    while((await stats()).camera!==i)await tap('c');
    await command({type:'pose',x:-120,z:0,yaw:-Math.PI/2});
    const before=await stats();const carBefore={position:[...before.position],yaw:before.yaw};
    const defaultPose=before.cameraPose;
    await dragBy('right',240,0); // approximately a 70–degree look-around
    await dragBy('right',0,100); // pitch after yaw, including hood/cockpit local-right
    await drag('right',8);await mouse('mouseWheel',700,480,'none',0,-180);await sleep(500);
    const after=await stats();
    assert.equal(after.camera,i,'Camera mode must remain selected during inspection');
    assert.deepEqual(after.position,carBefore.position,'Camera gestures must not move the car');
    assert.equal(after.yaw,carBefore.yaw,'Camera gestures must not rotate the car');
    assert(after.cameraPose.inspecting,'Camera telemetry must expose an active inspection');
    assert(after.cameraPose.zoom<1,'Wheel-up zoom must move toward a closer, narrower view');
    if(i===1||i===2)assert(after.cameraPose.pitch>.05,'Hood/cockpit pitch must work after a large yaw');
    await tap('v');const recentered=await stats();assert.equal(recentered.camera,i);assert.deepEqual(recentered.position,carBefore.position,'V must not move the car');assert.equal(recentered.yaw,carBefore.yaw,'V must not rotate the car');assert(Math.abs(recentered.cameraPose.yaw)<.001&&Math.abs(recentered.cameraPose.pitch)<.001&&Math.abs(recentered.cameraPose.zoom-1)<.001,'V must recenter camera state without changing mode');
    for(let axis=0;axis<3;axis++)assert(Math.abs(recentered.cameraPose.position[axis]-defaultPose.position[axis])<.03,'V must restore the original default camera pose');
    if(i===1||i===2){
      const panBefore=await stats();
      await panReleaseOverHud();
      const panAfter=await stats();
      assert.deepEqual(panAfter.position,carBefore.position,'Pan must not move the car');
      assert.equal(panAfter.yaw,carBefore.yaw,'Pan must not rotate the car');
      assert(panAfter.cameraPose.pan.some(value=>Math.abs(value)>.1),'Hood/cockpit pan must update the inspection offset');
      assert(panAfter.cameraPose.position.some((value,axis)=>Math.abs(value-panBefore.cameraPose.position[axis])>.02),'Pan must move the selected camera');
      await mouse('mouseMoved',1380,965);await sleep(300);
      const released=await stats();
      assert(released.cameraPose.pan.every((value,axis)=>Math.abs(value-panAfter.cameraPose.pan[axis])<.02),'HUD release must clear the pan drag state');
      report.checks.panInspection={modes:[1,2],releaseSurface:'HUD',carTransformStable:true};
      await tap('v');
    }
    modes.push({mode:i,after,recentered});
  }
  report.modes=modes;report.checks.allFourModes=true;report.checks.carTransformStable=true;
  // A large, split middle drag keeps every event inside the viewport while
  // exercising the overhead roof-inspection path at its intended range.
  while((await stats()).camera!==3)await tap('c');
  await command({type:'pose',x:-120,z:0,yaw:-Math.PI/2});
  const roofBefore=await stats();
  await mouse('mousePressed',700,700,'middle');
  await mouse('mouseMoved',700,450,'middle');
  await mouse('mouseMoved',700,200,'middle');
  await mouse('mouseReleased',700,200,'middle');
  await dragBy('right',120,0);
  await sleep(500);
  const roofAfter=await stats();
  assert.deepEqual(roofAfter.position,roofBefore.position,'Roof inspection must not move the car');
  assert.equal(roofAfter.yaw,roofBefore.yaw,'Roof inspection must not rotate the car');
  assert(roofAfter.cameraPose.pan.some(value=>Math.abs(value)>.1),'Overhead roof inspection must pan the camera focus');
  assert(roofAfter.cameraPose.position.some((value,axis)=>Math.abs(value-roofBefore.cameraPose.position[axis])>.02),'Roof inspection must move the overhead camera');
  assert(roofAfter.cameraPose.inspecting,'Roof inspection must expose active camera telemetry');
  await screenshot('roof-inspection');
  report.roofInspection={before:roofBefore,after:roofAfter,dragPixels:-500,orbitPixels:120};
  report.checks.roofInspection=true;
  const pausedBefore=await stats();await tap('Escape');const paused=await stats();assert.equal(paused.paused,true);await drag('right');await mouse('mouseWheel',700,480,'none',0,-180);await sleep(400);const pausedAfter=await stats();assert(Math.abs(pausedAfter.cameraPose.yaw-paused.cameraPose.yaw)<.001&&Math.abs(pausedAfter.cameraPose.zoom-paused.cameraPose.zoom)<.001,'Paused menu must ignore camera mouse input');await tap('Escape');assert.equal((await stats()).paused,false);const resumedBefore=await stats();await drag('right');const resumedAfter=await stats();assert(Math.abs(resumedAfter.cameraPose.yaw-resumedBefore.cameraPose.yaw)>.05,'Camera inspection must resume after unpausing');report.checks.pauseInput={before:pausedBefore.cameraPose,paused:pausedAfter.cameraPose,resumed:resumedAfter.cameraPose};
  // Driving remains real input while the camera is being orbited.
  await command({type:'pose',x:-120,z:0,yaw:-Math.PI/2});await key('w',true);await drag('right');await sleep(850);const moving=await stats();await key('w',false);assert(moving.speed>0.2||moving.position[2]<-0.5,'Held drive input must continue while orbiting camera');report.checks.driveDuringOrbit={speed:moving.speed,position:moving.position};
  await fs.writeFile(path.join(out,'review.json'),JSON.stringify(report,null,2)+'\n');console.log('SEVENTH_CAMERA_BROWSER_REVIEW_COMPLETE',out);
} finally {await fs.writeFile(path.join(out,'review.json'),JSON.stringify(report,null,2)+'\n');await fetch('http://127.0.0.1:9222/json/close/'+tab.id).catch(()=>{});ws.close();}
