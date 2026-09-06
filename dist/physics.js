export const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
export function nearestSegment(x,z,a,b){const dx=b[0]-a[0],dz=b[1]-a[1],l2=dx*dx+dz*dz;const t=l2?clamp(((x-a[0])*dx+(z-a[1])*dz)/l2,0,1):0;const px=a[0]+t*dx,pz=a[1]+t*dz;return {x:px,z:pz,d:Math.hypot(x-px,z-pz),t,dx,dz};}
export function inPolygon(x,z,p){let inside=false;for(let i=0,j=p.length-1;i<p.length;j=i++){const a=p[i],b=p[j];if((a[1]>z)!=(b[1]>z)&&x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0])inside=!inside;}return inside;}
export function createWorld(data){
 const segments=[];const collisionGrid=new Map();const size=35;
 for(const r of data.roads)for(let i=1;i<r.p.length;i++){const a=r.p[i-1],b=r.p[i];if(Math.hypot(b[0]-a[0],b[1]-a[1])<.1)continue;segments.push({a,b,road:r});}
 for(const b of data.buildings){if(b.base>3)continue;const xs=b.p.map(p=>p[0]),zs=b.p.map(p=>p[1]);b.box=[Math.min(...xs),Math.min(...zs),Math.max(...xs),Math.max(...zs)];for(let x=Math.floor(b.box[0]/size);x<=Math.floor(b.box[2]/size);x++)for(let z=Math.floor(b.box[1]/size);z<=Math.floor(b.box[3]/size);z++){const k=x+','+z;if(!collisionGrid.has(k))collisionGrid.set(k,[]);collisionGrid.get(k).push(b);}}
 function solid(x,z){for(const b of collisionGrid.get(Math.floor(x/size)+','+Math.floor(z/size))||[]){if(x<b.box[0]||x>b.box[2]||z<b.box[1]||z>b.box[3])continue;if(inPolygon(x,z,b.p))return true;}return false;}
 function nearest(x,z){let best={d:Infinity};for(const s of segments){const p=nearestSegment(x,z,s.a,s.b);if(p.d<best.d)best={...p,...s};}return best;}
 function carCollides(x,z,yaw){const f=[Math.sin(yaw),-Math.cos(yaw)],r=[Math.cos(yaw),Math.sin(yaw)];for(const u of [-1.65,0,1.65])for(const v of [-.82,.82])if(solid(x+f[0]*u+r[0]*v,z+f[1]*u+r[1]*v))return true;return false;}
 function spawn(x,z){const bounds=data.bounds;let s=nearest(x,z);const safe=p=>p.x>bounds[0]+20&&p.x<bounds[2]-20&&p.z>bounds[1]+20&&p.z<bounds[3]-20;if(!safe(s)){s={d:Infinity};for(const seg of segments){const p=nearestSegment(x,z,seg.a,seg.b);if(safe(p)&&p.d<s.d)s={...p,...seg};}}let yaw=Math.atan2(s.dx,-s.dz);if(s.road.reverse)yaw+=Math.PI;let offset=s.road.oneway?0:Math.min(2.2,s.road.w/4);let px=s.x+Math.cos(yaw)*offset,pz=s.z+Math.sin(yaw)*offset;if(carCollides(px,pz,yaw)){px=s.x;pz=s.z;}return {x:px,z:pz,yaw,speed:0,steer:0,road:s.road};}
 return {segments,solid,nearest,carCollides,spawn};
}
export function stepVehicle(car,input,dt,world,bounds){
 dt=Math.min(dt,1/30);const oldSpeed=car.speed;
 if(input.brake){car.speed=Math.sign(car.speed)*Math.max(0,Math.abs(car.speed)-22*dt);}
 else if(input.forward){car.speed+=car.speed<-.1?16*dt:7.5*dt;}
 else if(input.reverse){car.speed-=car.speed>.1?15*dt:4*dt;}
 else{car.speed=Math.sign(car.speed)*Math.max(0,Math.abs(car.speed)-(.45+Math.abs(car.speed)*.06)*dt);}
 car.speed-=car.speed*Math.abs(car.speed)*.006*dt;car.speed=clamp(car.speed,-6,25);
 const target=(input.left?1:0)-(input.right?1:0);car.steer+=(target-car.steer)*Math.min(1,dt*7);
 const yaw=car.yaw-car.steer*car.speed/2.75*Math.tan(.49/(1+Math.abs(car.speed)*.075))*dt;
 const x=car.x+Math.sin(yaw)*car.speed*dt,z=car.z-Math.cos(yaw)*car.speed*dt;
 const edge=x<bounds[0]+15||x>bounds[2]-15||z<bounds[1]+15||z>bounds[3]-15;
 const collision=world.carCollides(x,z,yaw);
 if(edge||collision){car.speed=0;return {collision,edge,distance:0};}
 car.x=x;car.z=z;car.yaw=yaw;return {collision:false,edge:false,distance:Math.abs((car.speed+oldSpeed)/2)*dt};
}
