import {wrap} from './vehicle.js';

// Interpolate completed 120 Hz physics steps. Never feed a visual pose back
// into collision or tire physics. The caller resets this history on travel.
export function createVehicleView(){
 const previous={x:0,z:0,yaw:0,pitch:0,roll:0};
 const fields=Object.keys(previous);
 const capture=car=>{for(const key of fields)previous[key]=car[key];};
 return {capture,reset:capture,sample(car,alpha){
  const t=Math.max(0,Math.min(1,alpha)),pose={};
  for(const key of fields)pose[key]=key==='yaw'?previous[key]+wrap(car[key]-previous[key])*t:previous[key]+(car[key]-previous[key])*t;
  return pose;
 }};
}
