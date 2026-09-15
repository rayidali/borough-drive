// Structural checks for reproducible architectural schedules. These cannot
// establish photographic accuracy, source rights or visual acceptance.
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const root=new URL('../',import.meta.url);
const {seventhEngine:schedule}=JSON.parse(await fs.readFile(new URL('model-source/storefront-details.json',root),'utf8'));
const shapes=new Set(['rectangle','round','segmental']);
const finite=(v,label)=>assert(Number.isFinite(v),label+' must be finite');
const groundCorrections=schedule.observedGroundCorrections||{};
function overlap(a,b){
  return Math.min(a.right,b.right)-Math.max(a.left,b.left)>.003 &&
    Math.min(a.top,b.top)-Math.max(a.bottom,b.bottom)>.003;
}
function openingBounds(opening,kind){
  const bottom=opening.bottom??(kind==='door'?.19:0);
  const top=kind==='door'?opening.top:bottom+opening.height;
  return {left:opening.at-opening.width/2,right:opening.at+opening.width/2,bottom,top};
}
function effectiveArchitecture(record){
  const raw=record.architecture||{};
  const correction=groundCorrections[String(record.buildingId)]||{};
  const architecture={...raw,
    windows:[...(raw.windows||[]).map(window=>({...window,_observed:false}))],
    doors:[...(raw.doors||[]).map(door=>({...door,_observed:false}))],
    basementAreaways:[...(raw.basementAreaways||[])]};
  // Mirror fidelity_elevation(): each replacement list independently removes
  // stale low geometry before the observed openings are rendered.
  const replaceWindows=correction.replaceWindows??Boolean(correction.groundOpenings?.length);
  const replaceDoors=correction.replaceDoors??Boolean(correction.groundDoors?.length);
  if(replaceWindows){
    architecture.windows=architecture.windows.filter(window=>window.bottom===undefined||window.bottom>=3.55);
    const observed=[...(correction.groundOpenings||[]),...(correction.groundDoors||[])];
    architecture.windows=architecture.windows.filter(window=>!observed.some(opening=>
      overlap(openingBounds(window,'window'),openingBounds(opening,opening.top===undefined?'window':'door'))));
  }
  if(replaceDoors){
    architecture.doors=architecture.doors.filter(door=>door.bottom===undefined||door.bottom>=3.55);
  }
  architecture.windows.push(...(correction.groundOpenings||[]).map(window=>({
    ...window,_observed:true,shape:window.shape||'rectangle',columns:window.columns||1,rails:window.rails||[]
  })));
  architecture.doors.push(...(correction.groundDoors||[]).map(door=>({...door,_observed:true})));
  architecture.basementAreaways.push(...(correction.basementAreaways||[]));
  return architecture;
}
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
const elevationIds=new Set(schedule.elevations.map(e=>String(e.buildingId)));
for(const [id,correction] of Object.entries(groundCorrections)){
  assert(elevationIds.has(id),'Ground correction has no elevation '+id);
  assert(!correction.suppressAllWindows,id+' must use replaceWindows so observed ground work never removes upper windows');
  if(correction.suppressBusinessExteriorIds){
    const storefronts=new Set(schedule.frontages.filter(r=>String(r.buildingId)===id).map(r=>r.id));
    for(const storefront of correction.suppressBusinessExteriorIds){
      assert(storefronts.has(storefront),id+' suppresses an unknown storefront '+storefront);
    }
  }
}
for(const e of schedule.elevations){
  const a=effectiveArchitecture(e),label=e.address||String(e.buildingId);
  assert(a,label+' missing architecture');
  if(a.preserveRecipe){preserved++;continue;}
  explicit++;finite(a.height,label+' height');assert(a.height>0);
  assert(a.observation?.sources?.length,label+' architectural sources');
  for(const id of a.observation.sources)assert(schedule.sources[id],label+' missing source '+id);
  assert(a.observation.unknown?.length,label+' must retain limits');
  const openings=[];
  for(const w of a.windows||[]){
    const name=label+' window';span(w.at,w.width,name);finite(w.bottom,name);finite(w.height,name);
    assert(w.bottom>=0 && w.height>0 && w.bottom+w.height<=a.height+.1,name+' height outside envelope');
    assert(shapes.has(w.shape||'rectangle'),name+' shape');
    assert(Number.isInteger(w.columns||1) && (w.columns||1)>0,name+' columns');
    assert((w.rails||[]).every(v=>Number.isFinite(v)&&v>0&&v<1),name+' rails');
    const geometry={...openingBounds(w,'window'),type:'window',observed:w._observed};
    const windowConflict=openings.find(other=>geometry.observed&&other.observed&&overlap(geometry,other));
    assert(!windowConflict,name+' overlaps an effective '+windowConflict?.type+' opening');
    openings.push(geometry);
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
    const geometry={...openingBounds(d,'door'),type:'door',observed:d._observed};
    const doorConflict=openings.find(other=>geometry.observed&&other.observed&&overlap(geometry,other));
    assert(!doorConflict,name+' overlaps an effective '+doorConflict?.type+' opening');
    openings.push(geometry);
    doors++;
  }
  for(const well of a.basementAreaways||[]){
    const name=label+' basement areaway';span(well.at,well.width,name);
    finite(well.depth,name+' depth');assert(well.depth>0,name+' depth must be positive');
    if(well.depthBelow!==undefined){
      finite(well.depthBelow,name+' below-grade depth');
      assert(well.depthBelow>=0,name+' below-grade depth must be nonnegative');
    }
    assert(Number.isInteger(well.steps||0)&&(well.steps||0)>=0,name+' steps');
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
