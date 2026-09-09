import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import * as THREE from '../dist/vendor/three.module.js';
// Resolve the browser's single import-map entry for this dependency-free check.
const module=await fs.readFile(new URL('../dist/reconstruction/spatial-batches.js',import.meta.url),'utf8');
const {partitionStaticMeshes}=await import('data:text/javascript;base64,'+Buffer.from(module.replace("'three'",JSON.stringify(new URL('../dist/vendor/three.module.js',import.meta.url).href))).toString('base64'));
const root=new THREE.Group();root.position.set(-37,5,91);root.rotation.y=.37;
const geometry=new THREE.BoxGeometry(130,12,90,5,2,4);geometry.clearGroups();
const material=new THREE.MeshStandardMaterial();
const mesh=new THREE.Mesh(geometry,material);mesh.position.set(24,2,-71);mesh.rotation.y=-.62;mesh.castShadow=mesh.receiveShadow=true;root.add(mesh);root.updateMatrixWorld(true);
const originalMatrix=mesh.matrixWorld.clone(),before=Array.from(geometry.index.array),attributes={...geometry.attributes};
await partitionStaticMeshes(root,{cellSize:32,minTriangles:1});
assert(root.children.length>1,'Test model must span several spatial batches.');
const triangles=[];
for(const part of root.children){
 assert(part.matrixWorld.equals(originalMatrix),'World placement must not change.');
 assert(part.material===material&&part.castShadow&&part.receiveShadow);
 for(const [name,attribute] of Object.entries(attributes))assert.equal(part.geometry.attributes[name],attribute,'Exact vertex data must remain shared.');
 const indices=part.geometry.index.array;
 for(let i=0;i<indices.length;i+=3){triangles.push([indices[i],indices[i+1],indices[i+2]].join(','));for(let j=0;j<3;j++)assert(part.geometry.boundingBox.containsPoint(new THREE.Vector3().fromBufferAttribute(attributes.position,indices[i+j])),'Bounds must include every triangle vertex, including triangles crossing a cell edge.');}
}
const original=[];for(let i=0;i<before.length;i+=3)original.push(before.slice(i,i+3).join(','));
assert.deepEqual(triangles.sort(),original.sort(),'No triangles may be lost, duplicated or have their winding changed.');
const transparent=new THREE.Mesh(new THREE.BoxGeometry(200,4,90),new THREE.MeshStandardMaterial({transparent:true,opacity:.2}));const glassRoot=new THREE.Group();glassRoot.add(transparent);await partitionStaticMeshes(glassRoot,{cellSize:32,minTriangles:1});assert.equal(glassRoot.children[0],transparent,'Do not reorder transparent surfaces.');
console.log(`Spatial batching: ${original.length} triangles preserved across ${root.children.length} batches; transforms, bounds, normals, UVs, shadows and transparency checked.`);
