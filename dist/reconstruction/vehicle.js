// Independent planar vehicle model. SI units: metres, seconds, kilograms, radians.
// Heading is clockwise from north; x is east and z is south. Steering is right-positive.
export const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
export const wrap=a=>Math.atan2(Math.sin(a),Math.cos(a));
const approach=(v,t,rate,dt)=>v+clamp(t-v,-rate*dt,rate*dt);
export const SPEC=Object.freeze({mass:1510,wheelbase:2.74,frontCG:1.19,rearCG:1.55,inertia:2450,frontStiffness:85000,rearStiffness:99000,grip:1.02,dragArea:.67,rolling:.013,maxDriveForce:5100,maxBrake:8.5,maxSteering:.56});
export function createVehicle(spawn){return {...spawn,speed:0,longitudinal:0,lateral:0,yawRate:0,steering:0,throttle:0,brake:0,gear:'D',rpm:800,reverseHold:0,roll:0,pitch:0,ax:0,ay:0,distance:0,collisionCooldown:0};}
export function resetVehicle(car,spawn){const distance=car.distance;Object.assign(car,createVehicle(spawn));car.distance=distance;}
export function stepVehicle(car,input,dt,world,bounds){
 dt=clamp(dt,0,1/60);if(!dt)return {collision:false,edge:false,distance:0};const p=SPEC,g=9.81;const oldV=car.longitudinal;
 const forward=clamp(input.throttle||0,0,1),reverse=clamp(input.reverse||0,0,1),handBrake=clamp(input.brake||0,0,1);
 let driveDirection=1,driveTarget=forward,brakeTarget=handBrake;
 if(reverse>.01){if(car.longitudinal>.15){driveTarget=0;brakeTarget=Math.max(brakeTarget,reverse);car.reverseHold=0;}else{car.reverseHold+=dt;if(car.reverseHold>.32){driveDirection=-1;driveTarget=reverse;}else{driveTarget=0;brakeTarget=1;}}}else car.reverseHold=0;
 if(forward>.01&&car.longitudinal<-.15){driveTarget=0;brakeTarget=Math.max(brakeTarget,forward);}
 if(handBrake>.05)driveTarget=0;
 car.throttle=approach(car.throttle,driveTarget,driveTarget>car.throttle?2.5:5.5,dt);car.brake=approach(car.brake,brakeTarget,5,dt);
 const speed=Math.abs(car.longitudinal);const maxSteer=Math.min(p.maxSteering,Math.atan(p.wheelbase*7.4/(speed*speed+13)));
 const requested=clamp(input.steer||0,-1,1)*maxSteer;car.steering=approach(car.steering,requested,Math.abs(requested)<.001?1.6:1.18,dt);
 const sign=Math.sign(car.longitudinal)||driveDirection;const drive=car.throttle*p.maxDriveForce*Math.max(.42,1-speed/58)*driveDirection*(driveDirection<0?.55:1);
 const resistance=sign*(.5*1.225*p.dragArea*speed*speed+p.rolling*p.mass*g*Math.min(speed/.25,1));
 let accel=(drive-resistance)/p.mass;
 if(car.brake>0){const amount=car.brake*p.maxBrake;if(Math.abs(car.longitudinal)<=amount*dt&&Math.abs(drive)<100){car.longitudinal=0;accel=0;}else accel-=sign*amount;}
 car.longitudinal=clamp(car.longitudinal+accel*dt,-5.6,34);
 if(car.brake>.9&&driveTarget===0&&speed<.15)car.longitudinal=0;
 // Saturating tire forces and yaw inertia provide grip limits without snapping heading.
 const v=Math.max(Math.abs(car.longitudinal),.7),delta=car.steering;
 const alphaFront=Math.atan2(car.lateral+p.frontCG*car.yawRate,v)-delta;
 const alphaRear=Math.atan2(car.lateral-p.rearCG*car.yawRate,v);
 const normalFront=p.mass*g*p.rearCG/p.wheelbase,normalRear=p.mass*g*p.frontCG/p.wheelbase;
 const grip=Math.max(.36,Math.sqrt(Math.max(0,1-Math.min(.9,Math.abs(accel)/(p.grip*g))**2)))*p.grip;
 const fyFront=normalFront*grip*Math.tanh(-p.frontStiffness*alphaFront/(normalFront*grip));
 const fyRear=normalRear*grip*Math.tanh(-p.rearStiffness*alphaRear/(normalRear*grip));
 const dynamicYaw=car.yawRate+(p.frontCG*fyFront*Math.cos(delta)-p.rearCG*fyRear)/p.inertia*dt;
 const dynamicLat=car.lateral+((fyFront*Math.cos(delta)+fyRear)/p.mass-car.yawRate*car.longitudinal)*dt;
 const beta=Math.atan(p.rearCG/p.wheelbase*Math.tan(delta));
 const kinYaw=car.longitudinal/p.wheelbase*Math.cos(beta)*Math.tan(delta);
 const kinLat=car.longitudinal*Math.sin(beta);
 const blend=car.longitudinal<0?0:clamp((v-2.5)/3,0,1);
 car.yawRate=(1-blend)*(car.yawRate+(kinYaw-car.yawRate)*Math.min(1,dt*14))+blend*dynamicYaw;
 car.lateral=(1-blend)*(car.lateral+(kinLat-car.lateral)*Math.min(1,dt*16))+blend*dynamicLat;
 if(v<.8){car.yawRate*=Math.exp(-dt*8);car.lateral*=Math.exp(-dt*8);}
 const yaw=wrap(car.yaw+car.yawRate*dt);
 const vx=Math.sin(yaw)*car.longitudinal+Math.cos(yaw)*car.lateral;
 const vz=-Math.cos(yaw)*car.longitudinal+Math.sin(yaw)*car.lateral;
 const x=car.x+vx*dt,z=car.z+vz*dt;
 const edge=bounds&&(x<bounds[0]||x>bounds[2]||z<bounds[1]||z>bounds[3]);
 const collision=world?.carCollides(x,z,yaw)||false;
 if(edge||collision){car.longitudinal=-car.longitudinal*.065;car.lateral*=.05;car.yawRate*=.2;car.throttle=0;car.speed=car.longitudinal;return {collision,edge,distance:0};}
 car.x=x;car.z=z;car.yaw=yaw;car.speed=car.longitudinal;car.ax=(car.longitudinal-oldV)/dt;car.ay=(fyFront+fyRear)/p.mass;
 car.pitch+=(-clamp(car.ax*.0035,-.033,.033)-car.pitch)*Math.min(1,dt*5);
 car.roll+=(-clamp(car.ay*.005,-.035,.035)-car.roll)*Math.min(1,dt*5);
 const gear=car.longitudinal<-.1?-1:v<7?1:v<13?2:v<20?3:v<28?4:5;
 car.gear=gear===-1?'R':String(gear);const ratios=[0,3.25,2.05,1.42,1.03,.82];
 car.rpm=Math.max(800,Math.abs(car.longitudinal)/(.32*2*Math.PI)*60*3.6*(ratios[Math.max(1,gear)]||3.25)+car.throttle*200);
 const distance=Math.hypot(vx,vz)*dt;car.distance+=distance;return {collision:false,edge:false,distance};
}
export function createFixedStepper(step,hz=120){let accumulator=0;return {advance(seconds){accumulator+=clamp(seconds,0,.15);let count=0;while(accumulator>=1/hz&&count<20){step(1/hz);accumulator-=1/hz;count++;}return accumulator*hz;},reset(){accumulator=0;}};}
