// Authored presentation, not a reconstruction of weather in a reference photo.
// Static cloud layers preserve zero redraws when the player is idle.
export function addCornerClouds(sky){
 const material=sky.material;
 material.fragmentShader=material.fragmentShader.replace('void main() {',`
  float cloudHash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
  float cloudNoise(vec2 p){
   vec2 i=floor(p),f=fract(p);f=f*f*(3.0-2.0*f);
   return mix(mix(cloudHash(i),cloudHash(i+vec2(1,0)),f.x),mix(cloudHash(i+vec2(0,1)),cloudHash(i+vec2(1,1)),f.x),f.y);
  }
  float cloudField(vec2 p){
   float n=0.0,a=0.52;
   for(int i=0;i<5;i++){n+=a*cloudNoise(p);p=mat2(1.62,1.17,-1.17,1.62)*p+vec2(17.1,8.3);a*=0.48;}
   return n;
  }
  void main() {
 `).replace('gl_FragColor = vec4( retColor, 1.0 );',`
  vec2 cloudUv=direction.xz/max(direction.y+0.18,0.08)*1.7+vec2(9.0,4.0);
  float field=cloudField(cloudUv);
  float coverage=smoothstep(0.37,0.62,field)*smoothstep(0.015,0.20,direction.y);
  float edgeLight=cloudField(cloudUv+vSunDirection.xz*0.16);
  vec3 cloudLight=mix(vec3(0.56,0.65,0.72),vec3(1.45,1.40,1.26),clamp(0.55+(field-edgeLight)*4.0,0.0,1.0));
  retColor=mix(retColor,cloudLight,coverage*0.80);
  gl_FragColor=vec4(retColor,1.0);
 `);
 material.needsUpdate=true;
}

// Add low-frequency variation to the existing licensed surface maps. The mask
// is bounded to First & 7th; no new measured repair/pothole locations are claimed.
export function refineCornerRoadMaterial(material,{paint=false}={}){
 material.onBeforeCompile=shader=>{
  shader.vertexShader=shader.vertexShader.replace('#include <common>','#include <common>\n varying vec3 cornerSurfacePosition;')
   .replace('#include <project_vertex>','#include <project_vertex>\n cornerSurfacePosition=(modelMatrix*vec4(transformed,1.0)).xyz;');
  shader.fragmentShader=shader.fragmentShader.replace('#include <common>',`#include <common>
   varying vec3 cornerSurfacePosition;
   float roadHash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
   float roadNoise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.0-2.0*f);return mix(mix(roadHash(i),roadHash(i+vec2(1,0)),f.x),mix(roadHash(i+vec2(0,1)),roadHash(i+vec2(1,1)),f.x),f.y);}
  `).replace('#include <color_fragment>',`#include <color_fragment>
   vec2 roadP=cornerSurfacePosition.xz;
   float cornerMask=1.0-smoothstep(28.0,55.0,length(roadP-vec2(0.0,228.0)));
   float broad=roadNoise(roadP*0.21),fine=roadNoise(roadP*3.4);
   ${paint?`float wear=smoothstep(0.34,0.58,fine)*0.13+smoothstep(0.57,0.72,broad)*0.15;
   diffuseColor.rgb*=1.0-cornerMask*wear;`:`float aggregate=mix(0.87,1.08,fine);
   float pavementTone=mix(0.80,1.12,broad)*aggregate;
   diffuseColor.rgb*=mix(1.0,pavementTone,cornerMask);`}
  `);
 };
 material.customProgramCacheKey=()=>paint?'corner-paint-09':'corner-asphalt-09';
 material.needsUpdate=true;
}
