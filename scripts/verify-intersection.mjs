import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createVehicle,stepVehicle,createFixedStepper} from '../dist/reconstruction/vehicle.js';

const root=path.resolve(import.meta.dirname,'../dist');
const world={carCollides:()=>false};
function simulate(fps,turn=0){
 const car=createVehicle({x:0,z:0,yaw:0});let time=0;
 const fixed=createFixedStepper(dt=>{stepVehicle(car,{throttle:time<4?1:0,brake:time>=4?1:0,steer:time<3?turn:0},dt,world);time+=dt;});
 for(let i=0;i<fps*7;i++)fixed.advance(1/fps);
 assert(Object.values(car).filter(v=>typeof v==='number').every(Number.isFinite));
 return car;
}
const at30=simulate(30),at120=simulate(120);
assert(Math.hypot(at30.x-at120.x,at30.z-at120.z)<.001,'Driving must not change with display frame rate.');
assert(Math.abs(at120.longitudinal)<.05,'Braking must stop the car.');
assert(at120.z < -10 && at120.z > -70,'Acceleration and stop distance must remain plausible.');
const turn=simulate(120,.4);assert(turn.x>2,'Right steering must turn right.');
const reverse=createVehicle({x:0,z:0,yaw:0});
for(let i=0;i<360;i++)stepVehicle(reverse,{reverse:1,steer:0},1/120,world);
assert(reverse.z>0&&reverse.longitudinal<0,'Reverse must move backward.');
const impact=createVehicle({x:0,z:0,yaw:0});impact.longitudinal=5;
const collision=stepVehicle(impact,{throttle:1},1/120,{carCollides:()=>true});
assert(collision.collision&&impact.z===0,'Blocked movement must not cross the collision surface.');

const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const ids=new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]));
const app=fs.readFileSync(path.join(root,'reconstruction/viewer.js'),'utf8');
for(const m of app.matchAll(/\$\('#([^']+)'\)/g))assert(ids.has(m[1]),`Missing interface element: ${m[1]}`);
for(const m of html.matchAll(/(?:src|href)="(\.\/[^"#?]+)"/g))assert(fs.existsSync(path.resolve(root,m[1])),`Missing asset: ${m[1]}`);
for(const m of app.matchAll(/asset\('([^']+)'\)/g))assert(fs.existsSync(path.join(root,'reconstruction',m[1])),`Missing model resource: ${m[1]}`);
function imports(file,seen=new Set()){
 if(seen.has(file))return;seen.add(file);
 const text=fs.readFileSync(file,'utf8');
 for(const m of text.matchAll(/(?:from\s*|import\s*)['"]([^'"]+)['"]/g)){
  const spec=m[1];let target;
  if(spec==='three')target=path.join(root,'vendor/three.module.js');
  else if(spec.startsWith('three/addons/'))target=path.join(root,'vendor/addons',spec.slice(13));
  else if(spec.startsWith('.'))target=path.resolve(path.dirname(file),spec);
  else continue;
  assert(fs.existsSync(target),`Missing module: ${spec} from ${file}`);imports(target,seen);
 }
 return seen.size;
}
const modules=imports(path.join(root,'reconstruction/viewer.js'));
const glb=fs.readFileSync(path.join(root,'reconstruction/first-and-10th.glb'));
assert.equal(glb.readUInt32LE(0),0x46546c67);assert.equal(glb.readUInt32LE(8),glb.length);
assert(glb.length<25*1024*1024,'Model must fit the static hosting per-file limit.');
const model=JSON.parse(glb.subarray(20,20+glb.readUInt32LE(12)).toString());
assert(model.extensionsRequired.includes('KHR_draco_mesh_compression'));
assert(model.meshes.length>100&&model.materials.length>20);
assert(model.images.every(i=>i.bufferView!==undefined),'Model textures must be portable and embedded.');
for(const name of ['draco_decoder.wasm','draco_wasm_wrapper.js','draco_decoder.js'])assert(fs.statSync(path.join(root,'vendor/draco',name)).size>1000);
console.log(JSON.stringify({localModules:modules,modelMB:+(glb.length/1024/1024).toFixed(2),modelMeshes:model.meshes.length,images:model.images.length,driveStopDistance:+(-at120.z).toFixed(2),frameRateIndependent:true,reverseAndCollision:true},null,2));
