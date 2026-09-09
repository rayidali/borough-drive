// Extract the exact shared road materials/images from the preserved core GLB.
// This small startup asset avoids waiting for 24 MiB of distant buildings.
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const root=new URL('../dist/reconstruction/',import.meta.url);
const input=await fs.readFile(new URL('first-and-10th.glb',root));
const length=input.readUInt32LE(12),source=JSON.parse(input.subarray(20,20+length)),bin=input.subarray(28+length);
const names=['asphalt','sidewalk','curb granite','concrete seam','road paint','bike green','yellow paint'];
const gltf={asset:{version:'2.0',generator:'Borough Drive / prepare-street-materials.mjs',extras:{source:'first-and-10th.glb',sha256:createHash('sha256').update(input).digest('hex')}},scene:0,scenes:[{nodes:[]}],materials:[],textures:[],images:[],samplers:source.samplers,bufferViews:[],buffers:[]};
const textures=new Map(),images=new Map(),chunks=[];let offset=0;
function texture(id){
 if(textures.has(id))return textures.get(id);
 const t=structuredClone(source.textures[id]),image=source.images[t.source];
 if(!images.has(t.source)){
  const view=source.bufferViews[image.bufferView],bytes=bin.subarray(view.byteOffset||0,(view.byteOffset||0)+view.byteLength),padding=Buffer.alloc((4-bytes.length%4)%4);
  images.set(t.source,gltf.images.length);gltf.images.push({...image,bufferView:gltf.bufferViews.length});gltf.bufferViews.push({buffer:0,byteOffset:offset,byteLength:bytes.length});chunks.push(bytes,padding);offset+=bytes.length+padding.length;
 }
 t.source=images.get(t.source);textures.set(id,gltf.textures.length);gltf.textures.push(t);return gltf.textures.length-1;
}
for(const name of names){const material=structuredClone(source.materials.find(m=>m.name===name));assert(material,`Missing ${name}`);for(const owner of [material,material.pbrMetallicRoughness])for(const [key,value] of Object.entries(owner||{}))if(key.endsWith('Texture'))value.index=texture(value.index);gltf.materials.push(material);}
gltf.buffers.push({byteLength:offset});
const json=Buffer.from(JSON.stringify(gltf)),jsonPad=Buffer.alloc((4-json.length%4)%4,32),jsonChunk=Buffer.concat([json,jsonPad]),body=Buffer.concat(chunks),header=Buffer.alloc(20),binHeader=Buffer.alloc(8);
header.writeUInt32LE(0x46546c67,0);header.writeUInt32LE(2,4);header.writeUInt32LE(28+jsonChunk.length+body.length,8);header.writeUInt32LE(jsonChunk.length,12);header.writeUInt32LE(0x4e4f534a,16);binHeader.writeUInt32LE(body.length,0);binHeader.writeUInt32LE(0x004e4942,4);
const result=Buffer.concat([header,jsonChunk,binHeader,body]),destination=new URL('street-materials.glb',root);
if(process.argv.includes('--check'))assert.deepEqual(await fs.readFile(destination),result,'Street startup materials are stale. Run node scripts/prepare-street-materials.mjs');else await fs.writeFile(destination,result);
console.log(`Street materials: ${gltf.materials.length} exact materials, ${gltf.images.length} original images, ${(result.length/1024/1024).toFixed(2)} MiB; ${process.argv.includes('--check')?'reproduction verified':'saved'}.`);
