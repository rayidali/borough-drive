shader_type spatial;
render_mode specular_schlick_ggx;
varying vec3 world_pos;
uniform float dusk : hint_range(0.0,1.0) = 0.0;
uniform bool luminous = false;
float hash(vec2 p) { return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
void vertex() { world_pos = (MODEL_MATRIX * vec4(VERTEX,1.0)).xyz; }
void fragment() {
    vec3 pigment = COLOR.rgb;
    float grain = hash(floor(world_pos.xz * 26.0) + floor(world_pos.y*26.0));
    pigment *= 0.97 + grain * 0.06;
    pigment = mix(pigment, vec3(0.77,0.61,0.54),0.055);
    ALBEDO = pigment;
    ROUGHNESS = 0.88;
    SPECULAR = 0.18;
    if (luminous) { EMISSION = pigment * mix(0.12,1.45,dusk); }
}
void light() {
    float shade = smoothstep(-0.1,0.75,dot(NORMAL,LIGHT));
    DIFFUSE_LIGHT += ALBEDO * LIGHT_COLOR * ATTENUATION * (0.20 + shade*0.8) / 3.14159;
}
