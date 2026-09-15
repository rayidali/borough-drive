// Reproduce the isolated browser build; no npm dependencies or cloud services.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
import {brotliCompress,constants} from 'node:zlib';
import {promisify} from 'node:util';
const root=fileURLToPath(new URL('../',import.meta.url));
const project=path.join(root,'engine/first-seventh');
const godot=process.env.BOROUGH_GODOT||path.join(root,'.tools/godot/Godot.app/Contents/MacOS/Godot');
async function run(command,args,cwd=project){
  await new Promise((resolve,reject)=>{
    const child=spawn(command,args,{cwd,stdio:'inherit'});
    child.on('error',reject);child.on('exit',code=>code===0?resolve():reject(Error(`${path.basename(command)} exited ${code}`)));
  });
}
const data=JSON.parse(await fs.readFile(path.join(project,'assets/slice.json'),'utf8'));
for(const [name,expected] of Object.entries({...data.recipeHashes,'model-source/storefront-details.json':data.detailSourceSha256})){
  const actual=createHash('sha256').update(await fs.readFile(path.join(root,name))).digest('hex');
  if(actual!==expected)throw Error('Re-export the Blender models after editing '+name);
}
for(const record of data.buildings){
  const filename=path.join(project,record.asset.replace('res://',''));
  let buffer;
  try{buffer=await fs.readFile(filename);}catch{throw Error('Missing neighborhood cache. Run the Blender export command in engine/first-seventh/README.md first.');}
  if(createHash('sha256').update(buffer).digest('hex')!==record.sha256)throw Error('Source asset hash mismatch: '+record.id);
}
await fs.mkdir(path.join(project,'exports'),{recursive:true});
const stage=await fs.mkdtemp(path.join(project,'exports/web-'));
try{
  await run(godot,['--headless','--path','.','--import']);
  await run(godot,['--headless','--path','.','--export-release','Web',path.join(stage,'index.html')]);
  await run(godot,['--headless','--path','.','--script','res://scripts/export_credits.gd','--','--credits-out='+path.join(stage,'godot-notices.txt')]);
  await fs.copyFile(path.join(project,'assets/credits.txt'),path.join(stage,'credits.txt'));
  await fs.copyFile(path.join(root,'LICENSE'),path.join(stage,'LICENSE.txt'));
  await fs.copyFile(path.join(root,'model-source/fonts/OFL.txt'),path.join(stage,'DAMION-OFL.txt'));
  for(const name of ['index.html','godot-notices.txt']){
    const filename=path.join(stage,name);
    const text=(await fs.readFile(filename,'utf8')).replace(/[ \t]+$/gm,'').replace(/\n+$/,'\n');
    await fs.writeFile(filename,text);
  }
  const manifest={schema:1,builtAt:new Date().toISOString(),engine:'Godot 4.7.2',renderer:'Compatibility / WebGL 2',threaded:false,buildings:data.buildings.length,sourceCommit:data.sourceCommit,geographySha256:data.sourceSha256,files:{},sources:{}};
  for(const name of (await fs.readdir(stage)).sort()){
    const buffer=await fs.readFile(path.join(stage,name));
    const record={bytes:buffer.length,sha256:createHash('sha256').update(buffer).digest('hex')};
    if(name.endsWith('.wasm')||name.endsWith('.pck')){
      const br=await promisify(brotliCompress)(buffer,{params:{[constants.BROTLI_PARAM_QUALITY]:6}});
      record.brotliBytes=br.length; // Potential transfer size; not a hosting measurement.
    }
    manifest.files[name]=record;
  }
  async function sources(directory){
    for(const entry of await fs.readdir(directory,{withFileTypes:true})){
      if(entry.name.startsWith('.')||entry.name==='exports'||entry.name==='neighborhood')continue;
      const filename=path.join(directory,entry.name);
      if(entry.isDirectory())await sources(filename);
      else if(/\.(gd|gdshader|tscn|godot|cfg|html|json|wav|txt|jpg|png|import)$/.test(entry.name)){
        manifest.sources[path.relative(root,filename)]=createHash('sha256').update(await fs.readFile(filename)).digest('hex');
      }
    }
  }
  await sources(project);
  for(const name of [...Object.keys(data.recipeHashes),'model-source/storefront-details.json','model-source/seventh-street-reference-02.json','model-source/make_seventh_audio.py','scripts/export-seventh.mjs']){
    manifest.sources[name]=createHash('sha256').update(await fs.readFile(path.join(root,name))).digest('hex');
  }
  await fs.writeFile(path.join(stage,'build.json'),JSON.stringify(manifest,null,2)+'\n');
  // Godot exports into an ignored staging directory; only a completed package
  // is copied into the separately served slice. The existing game stays intact.
  await fs.cp(stage,path.join(root,'dist/seventh'),{recursive:true});
  console.log('SEVENTH_EXPORT_COMPLETE',JSON.stringify({files:Object.keys(manifest.files).length,bytes:Object.values(manifest.files).reduce((n,f)=>n+f.bytes,0)}));
}finally{
  await fs.rm(stage,{recursive:true,force:true});
}
