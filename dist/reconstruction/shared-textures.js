// GLTFLoader normally caches images only within one model. These immutable,
// content-addressed surface maps are shared by many neighborhood sections.
// Cache their load/decode promises across models; keep per-parser texture state
// separate, and leave GLB buffers and embedded photographs out of this cache.
export function shareNeighborhoodTextures(loader){
 const cache=new Map();
 loader.register(parser=>({
  name:'BOROUGH_shared_surface_images',
  loadTexture(index){
   const definition=parser.json.textures[index],source=parser.json.images[definition.source];
   if(definition.extensions||!source?.uri||!/(?:^|\/)textures\/[a-f0-9]{20}\.(?:png|jpg)$/.test(source.uri))return null;
   const key=JSON.stringify([new URL(source.uri,parser.options.path).href,parser.json.samplers?.[definition.sampler]]);
   if(!cache.has(key))cache.set(key,parser.loadTexture(index).then(texture=>{if(!texture)cache.delete(key);return texture;},error=>{cache.delete(key);throw error;}));
   return cache.get(key).then(texture=>{if(!texture)return null;const copy=texture.clone();parser.associations.set(copy,{textures:index});return copy;});
  }
 }));
}
