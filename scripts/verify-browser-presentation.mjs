import assert from 'node:assert/strict';
import {createRenderBudget} from '../dist/reconstruction/render-budget.js';
import {createVehicleView} from '../dist/reconstruction/vehicle-view.js';
import {wrap} from '../dist/reconstruction/vehicle.js';

const budget=createRenderBudget();
for(let i=0;i<180;i++)assert.equal(budget.sample(1000/60),null);
assert.deepEqual(budget.state(),{ratio:1,ambient:true},'A healthy 60 Hz view keeps its resolution.');
assert.equal(budget.sample(800),null,'A single loading stall is not a steady rendering sample.');
for(let i=0;i<225;i++)budget.sample(1000/30);
assert.deepEqual(budget.state(),{ratio:.7,ambient:false},'Sustained slow rendering reaches a bounded fallback.');
assert.deepEqual(budget.settle(),{ratio:1,ambient:true},'Stopped inspection restores sharpness/contact shading.');
assert.equal(budget.settle(),null,'Restoration happens once, so idle rendering can stop.');
for(let i=0;i<29;i++)assert.equal(budget.sample(33),null);
budget.reset();assert.equal(budget.sample(33),null,'Reset discards samples from the previous view.');

const presentation=createVehicleView();
const a={x:0,z:10,yaw:Math.PI-.02,pitch:0,roll:0};presentation.reset(a);
const b={x:2,z:6,yaw:-Math.PI+.02,pitch:.02,roll:-.02};
const mid=presentation.sample(b,.5);
assert.equal(mid.x,1);assert.equal(mid.z,8);
assert(Math.abs(wrap(mid.yaw-Math.PI))<1e-10,'Yaw interpolation takes the short path through north/south wrap.');
assert.equal(mid.pitch,.01);assert.equal(mid.roll,-.01);
assert.deepEqual(b,{x:2,z:6,yaw:-Math.PI+.02,pitch:.02,roll:-.02},'Presentation never alters simulation state.');
presentation.reset(b);assert.deepEqual(presentation.sample(b,0),b,'Travel reset must not interpolate from the old street.');
assert.deepEqual(presentation.sample(b,2),b,'Interpolation stays bounded after stalls.');
console.log('Browser presentation: sustained frame budget, idle recovery, yaw wrap, travel reset and physics isolation passed.');
