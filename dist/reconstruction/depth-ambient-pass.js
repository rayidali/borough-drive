import {CustomBlending, Vector2} from 'three';
import {SSAOPass} from 'three/addons/postprocessing/SSAOPass.js';

// Reuse the vendored Three.js SSAO kernel/blur and its MIT attribution. Derive
// geometric normals from the main scene depth instead of drawing the city again.
// Choose the nearer depth derivative at discontinuities to avoid silhouette halos.
export class DepthAmbientPass extends SSAOPass {
 constructor(scene,camera,width,height){
  super(scene,camera,width,height,16);
  this.ssaoMaterial.uniforms.depthTexel={value:new Vector2()};
  this.ssaoMaterial.fragmentShader=this.ssaoMaterial.fragmentShader
   .replace('uniform vec2 resolution;','uniform vec2 resolution;\n uniform vec2 depthTexel;')
   .replace('return unpackRGBToNormal( texture2D( tNormal, screenPosition ).xyz );',`
    float dc=getDepth(screenPosition);
    vec3 c=getViewPosition(screenPosition,dc,getViewZ(dc));
    vec2 l=clamp(screenPosition-vec2(depthTexel.x,0.0),depthTexel,1.0-depthTexel);
    vec2 r=clamp(screenPosition+vec2(depthTexel.x,0.0),depthTexel,1.0-depthTexel);
    vec2 b=clamp(screenPosition-vec2(0.0,depthTexel.y),depthTexel,1.0-depthTexel);
    vec2 t=clamp(screenPosition+vec2(0.0,depthTexel.y),depthTexel,1.0-depthTexel);
    float dl=getDepth(l),dr=getDepth(r),db=getDepth(b),dt=getDepth(t);
    vec3 vl=c-getViewPosition(l,dl,getViewZ(dl));
    vec3 vr=getViewPosition(r,dr,getViewZ(dr))-c;
    vec3 vb=c-getViewPosition(b,db,getViewZ(db));
    vec3 vt=getViewPosition(t,dt,getViewZ(dt))-c;
    vec3 dx=abs(vl.z)<abs(vr.z)?vl:vr;
    vec3 dy=abs(vb.z)<abs(vt.z)?vb:vt;
    vec3 normal=cross(dx,dy);
    return dot(normal,normal)>1e-12?normalize(normal):vec3(0.0,0.0,1.0);
   `);
 }
 render(renderer,writeBuffer,readBuffer){
  if(!readBuffer.depthTexture)throw Error('Ambient shading requires the main scene depth texture.');
  const u=this.ssaoMaterial.uniforms;
  u.tDepth.value=readBuffer.depthTexture;
  u.depthTexel.value.set(1/readBuffer.width,1/readBuffer.height);
  u.cameraProjectionMatrix.value.copy(this.camera.projectionMatrix);
  u.cameraInverseProjectionMatrix.value.copy(this.camera.projectionMatrixInverse);
  u.cameraNear.value=this.camera.near;u.cameraFar.value=this.camera.far;
  u.kernelRadius.value=this.kernelRadius;u.minDistance.value=this.minDistance;u.maxDistance.value=this.maxDistance;
  this._renderPass(renderer,this.ssaoMaterial,this.ssaoRenderTarget);
  this._renderPass(renderer,this.blurMaterial,this.blurRenderTarget);
  this.copyMaterial.uniforms.tDiffuse.value=this.blurRenderTarget.texture;
  this.copyMaterial.blending=CustomBlending;
  this._renderPass(renderer,this.copyMaterial,this.renderToScreen?null:readBuffer);
 }
}
