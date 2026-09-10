// Automatic adjusts pixel work only. Building meshes/textures and physics stay
// intact; a settled inspection view returns to native CSS-pixel resolution.
export function createRenderBudget(){
 let ratio=1,ambient=true,frames=0,total=0;
 const state=()=>({ratio,ambient});
 const reset=()=>{ratio=1;ambient=true;frames=total=0;return state();};
 return {state,reset,sample(milliseconds){
  if(!Number.isFinite(milliseconds)||milliseconds<1||milliseconds>100)return null;
  total+=milliseconds;frames++;
  if(frames<30)return null;
  const mean=total/frames;frames=total=0;
  if(mean<=19.5)return null;
  if(ratio>.71){ratio=Math.max(.70,Math.round(ratio*.85*100)/100);return state();}
  if(ambient){ambient=false;return state();}
  return null;
 },settle(){return ratio<1||!ambient?reset():null;}};
}
