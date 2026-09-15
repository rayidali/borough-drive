// Structural checks for reproducible architectural schedules. These cannot
// establish photographic accuracy, source rights or visual acceptance.
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const root=new URL('../',import.meta.url);
const {seventhEngine:schedule}=JSON.parse(await fs.readFile(new URL('model-source/storefront-details.json',root),'utf8'));
const shapes=new Set(['rectangle','round','segmental']);
const finite=(v,label)=>assert(Number.isFinite(v),label+' must be finite');
function span(at,width,label){
  finite(at,label+' position');finite(width,label+' width');
  assert(width>0 && at-width/2>=-.001 && at+width/2<=1.001,label+' exceeds facade bounds');
}
function panelUnit(u,label){
  assert(u.span?.length===2 && u.span[0]>=0 && u.span[0]<u.span[1] && u.span[1]<=1,label+' span');
  assert(Math.abs(u.design.panels.reduce((n,p)=>n+p[1],0)-1)<1e-5,label+' panel fractions');
  assert(u.design.panels.every(p=>p[1]>0 && ['window','door','double-door'].includes(p[0])),label+' panel kind');
  assert(u.observation?.length,label+' observation');
}
let explicit=0,preserved=0,windows=0,doors=0,unlettered=0;
for(const e of schedule.elevations){
  const a=e.architecture,label=e.address||String(e.buildingId);
  assert(a,label+' missing architecture');
  if(a.preserveRecipe){preserved++;continue;}
  explicit++;finite(a.height,label+' height');assert(a.height>0);
  assert(a.observation?.sources?.length,label+' architectural sources');
  for(const id of a.observation.sources)assert(schedule.sources[id],label+' missing source '+id);
  assert(a.observation.unknown?.length,label+' must retain limits');
  const openings=new Set();
  for(const w of a.windows||[]){
    const name=label+' window';span(w.at,w.width,name);finite(w.bottom,name);finite(w.height,name);
    assert(w.bottom>=0 && w.height>0 && w.bottom+w.height<=a.height+.1,name+' height outside envelope');
    assert(shapes.has(w.shape||'rectangle'),name+' shape');
    assert(Number.isInteger(w.columns||1) && (w.columns||1)>0,name+' columns');
    assert((w.rails||[]).every(v=>Number.isFinite(v)&&v>0&&v<1),name+' rails');
    const key=[w.at,w.bottom].join('/');assert(!openings.has(key),name+' duplicated opening '+key);openings.add(key);
    windows++;
  }
  for(const d of a.doors||[]){
    const name=label+' door';span(d.at,d.width,name);finite(d.top,name);
    assert(d.top>(d.bottom??.19) && d.top<a.height,name+' height');
    assert(shapes.has(d.shape||'rectangle'),name+' shape');
    assert([1,2].includes(d.leaves||1),name+' leaves');
    if(d.parts){
      assert(d.parts.every(p=>p.fraction>0),name+' fixed/operable part width');
      assert(Math.abs(d.parts.reduce((n,p)=>n+p.fraction,0)-1)<1e-6,name+' part fractions');
      assert(d.parts.filter(p=>!p.fixed).length===(d.leaves||1),name+' operable leaf count');
    }
    for(const p of d.panels||[])assert(p.y>0 && p.y<1 && p.height>0 && p.y-p.height/2>=0 && p.y+p.height/2<=1,name+' panel bounds');
    const access=d.access||{};
    assert(Number.isInteger(access.steps||0)&&(access.steps||0)>=0,name+' steps');
    if(access.steps)assert(access.rise>0 && access.run>0,name+' stair rise/run');
    if(access.ramp){
      const r=access.ramp;assert(r.start?.length===3 && r.end?.length===3 && r.width>0,name+' ramp geometry');
      assert([...r.start,...r.end].every(Number.isFinite),name+' ramp coordinates');
      assert(Math.hypot(r.end[0]-r.start[0],r.end[2]-r.start[2])>0,name+' zero-length ramp');
    }
    doors++;
  }
  for(const u of a.unletteredUnits||[]){panelUnit(u,label+' unlettered unit');unlettered++;}
}
for(const r of schedule.frontages){
  const p=r.design?.facadePath;if(!p)continue;
  assert(p.length===r.design.panels.length+1 && p[0][0]===0 && p.at(-1)[0]===1,r.id+' projected shop path');
  for(let j=0;j<p.length-1;j++){
    assert(p[j].length===2 && p[j].every(Number.isFinite),r.id+' projected coordinates');
    assert(p[j+1][0]>p[j][0] && Math.abs(p[j+1][0]-p[j][0]-r.design.panels[j][1])<1e-6,r.id+' projected pane order/width');
  }
  assert(p.at(-1).every(Number.isFinite),r.id+' last projection point');
}
console.log(`Verified architectural schedule: ${explicit} explicit / ${preserved} preserved elevations, ${windows} window groups, ${doors} entrances, ${unlettered} unlettered units. Visual acceptance is separate.`);
