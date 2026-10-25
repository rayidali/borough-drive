// The pinned Godot 4.7.2 unencrypted PCK v4 directory, used by export and CI.
import assert from 'node:assert/strict';
export function packEntries(buffer){
  assert.equal(buffer.subarray(0,4).toString(),'GDPC');
  assert.equal(buffer.readUInt32LE(4),4);assert.equal(buffer.readUInt32LE(20),2);
  const base=Number(buffer.readBigUInt64LE(24));let offset=Number(buffer.readBigUInt64LE(32));
  const count=buffer.readUInt32LE(offset),entries=[];offset+=4;
  for(let i=0;i<count;i++){
    const length=buffer.readUInt32LE(offset);offset+=4;
    const name=buffer.subarray(offset,offset+length).toString().replace(/\0+$/,'');offset+=length;
    const start=base+Number(buffer.readBigUInt64LE(offset)),bytes=Number(buffer.readBigUInt64LE(offset+8));
    assert.equal(buffer.readUInt32LE(offset+32),0);assert(start>=base&&start+bytes<=buffer.length);
    entries.push({name,start,bytes});offset+=36;
  }
  assert.equal(offset,buffer.length);assert.equal(new Set(entries.map(e=>e.name)).size,count);
  return entries;
}
