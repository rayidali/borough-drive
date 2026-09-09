import * as THREE from 'three';

// Keep every authored vertex, normal, UV and triangle. Smaller index buffers
// give the camera and shadow frusta useful bounds without duplicating vertices.
export async function partitionStaticMeshes(root,{cellSize=64,minTriangles=20000}={}){
 root.updateMatrixWorld(true);
 const meshes=[];root.traverse(o=>{if(o.isMesh&&!o.isInstancedMesh)meshes.push(o);});
 let yielded=performance.now();
 for(const mesh of meshes){
  const source=mesh.geometry,index=source.index,position=source.attributes.position;
  if(!index||index.count<minTriangles*3||Array.isArray(mesh.material)||mesh.material.transparent||mesh.material.transmission>0||source.groups.length>1)continue;
  const matrix=mesh.matrixWorld.elements,cells=new Map(),buckets=[],assignment=new Uint16Array(index.count/3);
  for(let i=0;i<index.count;i+=3){
   const a=index.getX(i),b=index.getX(i+1),c=index.getX(i+2);
   const x=(position.getX(a)+position.getX(b)+position.getX(c))/3,y=(position.getY(a)+position.getY(b)+position.getY(c))/3,z=(position.getZ(a)+position.getZ(b)+position.getZ(c))/3;
   const key=Math.floor((matrix[0]*x+matrix[4]*y+matrix[8]*z+matrix[12])/cellSize)+','+Math.floor((matrix[2]*x+matrix[6]*y+matrix[10]*z+matrix[14])/cellSize);
   let cell=cells.get(key);if(cell===undefined){cell=buckets.length;cells.set(key,cell);buckets.push({count:0,offset:0,bounds:new THREE.Box3()});}
   assignment[i/3]=cell;buckets[cell].count+=3;
  }
  if(buckets.length<2)continue;
  for(const bucket of buckets)bucket.indices=new index.array.constructor(bucket.count);
  const point=new THREE.Vector3();
  for(let i=0;i<index.count;i+=3){const bucket=buckets[assignment[i/3]];for(let j=0;j<3;j++){const vertex=index.getX(i+j);bucket.indices[bucket.offset++]=vertex;point.fromBufferAttribute(position,vertex);bucket.bounds.expandByPoint(point);}}
  for(const [cell,bucket] of buckets.entries()){
   const geometry=new THREE.BufferGeometry();
   for(const [name,attribute] of Object.entries(source.attributes))geometry.setAttribute(name,attribute);
   geometry.setIndex(new THREE.BufferAttribute(bucket.indices,1));geometry.boundingBox=bucket.bounds;geometry.boundingSphere=bucket.bounds.getBoundingSphere(new THREE.Sphere());
   const part=new THREE.Mesh(geometry,mesh.material);part.name=mesh.name+' · cell '+cell;part.position.copy(mesh.position);part.quaternion.copy(mesh.quaternion);part.scale.copy(mesh.scale);part.visible=mesh.visible;part.castShadow=mesh.castShadow;part.receiveShadow=mesh.receiveShadow;part.renderOrder=mesh.renderOrder;part.layers.mask=mesh.layers.mask;part.updateMatrix();part.matrixAutoUpdate=false;mesh.parent.add(part);
  }
  mesh.removeFromParent();source.dispose();
  // Decode and partition streamed streets without one long main-thread task.
  if(performance.now()-yielded>8){await new Promise(resolve=>setTimeout(resolve,0));yielded=performance.now();}
 }
 root.updateMatrixWorld(true);
}
