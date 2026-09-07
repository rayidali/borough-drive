// Geographic collision and navigation, independent of streamed visual meshes.
export function inPolygon(x,z,p){let yes=false;for(let i=0,j=p.length-1;i<p.length;j=i++){const a=p[i],b=p[j];if((a[1]>z)!==(b[1]>z)&&x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0])yes=!yes;}return yes;}
export function projectOnRoad(x,z,r){const dx=r.b[0]-r.a[0],dz=r.b[1]-r.a[1],t=Math.max(0,Math.min(1,((x-r.a[0])*dx+(z-r.a[1])*dz)/(dx*dx+dz*dz)));return {x:r.a[0]+dx*t,z:r.a[1]+dz*t,t};}
export function createNeighborhoodWorld(data){
 const cells=new Map(),size=24;
 for(const b of data.buildings){const bb=b.box;for(let x=Math.floor(bb[0]/size);x<=Math.floor(bb[2]/size);x++)for(let z=Math.floor(bb[1]/size);z<=Math.floor(bb[3]/size);z++){const key=x+','+z;if(!cells.has(key))cells.set(key,[]);cells.get(key).push(b);}}
 const bounds=data.driveBounds;
 function buildingAt(x,z){return (cells.get(Math.floor(x/size)+','+Math.floor(z/size))||[]).find(b=>x>=b.box[0]&&x<=b.box[2]&&z>=b.box[1]&&z<=b.box[3]&&inPolygon(x,z,b.p)&&!(b.holes||[]).some(h=>inPolygon(x,z,h)));}
 function roadAt(x,z,margin=0){return data.roads.find(r=>{const p=projectOnRoad(x,z,r);return Math.hypot(x-p.x,z-p.z)<=r.halfWidth-margin;});}
 function nearestRoad(x,z){let best;for(const road of data.roads){const p=projectOnRoad(x,z,road),distance=Math.hypot(x-p.x,z-p.z);if(!best||distance<best.distance)best={...p,distance,road};}return best;}
 const parked=data.parked||[];
 function hitsParked(x,z){for(const p of parked){if(Math.abs(x-p.x)>3||Math.abs(z-p.z)>3)continue;const c=Math.cos(p.angle),s=Math.sin(p.angle),dx=x-p.x,dz=z-p.z;if(Math.abs(c*dx-s*dz)<1&&Math.abs(s*dx+c*dz)<2.24)return true;}return false;}
 function carCollides(x,z,yaw){const sn=Math.sin(yaw),cs=Math.cos(yaw);for(const a of [-1.95,0,1.95])for(const b of [-.9,.9]){const xx=x+sn*a+cs*b,zz=z-cs*a+sn*b;if(!roadAt(xx,zz,.12)||buildingAt(xx,zz)||hitsParked(xx,zz))return true;}return false;}
 function walkable(x,z){if(x<bounds[0]||x>bounds[2]||z<bounds[1]||z>bounds[3])return false;for(const [a,b] of [[0,0],[.24,0],[-.24,0],[0,.24],[0,-.24]])if(buildingAt(x+a,z+b))return false;return true;}
 function spawn(x,z){x=Math.max(bounds[0]+3,Math.min(bounds[2]-3,x));z=Math.max(bounds[1]+3,Math.min(bounds[3]-3,z));const near=nearestRoad(x,z),yaw=near.road.axis==='avenue'?(near.road.oneway===1?Math.PI:0):(near.road.oneway===-1?-Math.PI/2:Math.PI/2);for(const offset of [0,6,-6,12,-12,20,-20]){const xx=near.x+(near.road.axis==='street'?offset:0),zz=near.z+(near.road.axis==='avenue'?offset:0);if(xx>=bounds[0]&&xx<=bounds[2]&&zz>=bounds[1]&&zz<=bounds[3]&&!carCollides(xx,zz,yaw))return {x:xx,z:zz,yaw};}return {x:1,z:45,yaw:0};}
 return {buildingAt,roadAt,nearestRoad,carCollides,walkable,spawn};
}
