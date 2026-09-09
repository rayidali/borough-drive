import * as THREE from 'three';

// Thin clear storefront panes: retain the physical surface lighting and captured
// reflections, blending the already rendered interior through the pane. This
// approximates the former 6 mm refraction without rendering the city again.
export function createStorefrontGlass(){
 const material=new THREE.MeshPhysicalMaterial({name:'seventh glass',color:0xffffff,roughness:.008,metalness:0,ior:1.5,transparent:true,depthWrite:false,side:THREE.FrontSide});
 material.userData.paneTransmission={value:.96};
 material.onBeforeCompile=shader=>{
  shader.uniforms.paneTransmission=material.userData.paneTransmission;
  shader.fragmentShader='uniform float paneTransmission;\n'+shader.fragmentShader;
  shader.fragmentShader=shader.fragmentShader.replace('#include <transmission_fragment>',`
   vec3 paneFresnel = EnvironmentBRDF(geometryNormal, geometryViewDir, material.specularColor, material.specularF90, material.roughness);
   totalDiffuse *= 1.0 - paneTransmission;
   diffuseColor.a = 1.0 - paneTransmission * (1.0 - paneFresnel.r);
  `).replace('#include <opaque_fragment>','gl_FragColor = vec4(outgoingLight / max(diffuseColor.a, 0.001), diffuseColor.a);');
 };
 material.customProgramCacheKey=()=> 'borough-thin-pane-1';
 return material;
}
