shader_type spatial;
uniform float wetness : hint_range(0.0,1.0) = 0.0;
uniform vec3 reflection_tint : source_color = vec3(0.67,0.48,0.57);
varying vec3 world_pos;
float h(vec2 p) { return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
float noise(vec2 p) { vec2 i=floor(p),f=fract(p);f=f*f*(3.0-2.0*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y); }
void vertex() { world_pos=(MODEL_MATRIX*vec4(VERTEX,1.0)).xyz; }
void fragment() {
    float n=noise(world_pos.xz*0.22);
    float fine=h(floor(world_pos.xz*100.0));
    vec3 dry=vec3(0.20,0.225,0.26)*(0.85+n*.22+fine*.045);
    float puddle=smoothstep(.4,.76,noise(world_pos.xz*.52))*wetness;
    float fresnel=pow(1.0-max(0.0,dot(NORMAL,VIEW)),3.0);
    ALBEDO=mix(dry,dry*.58,wetness);
    ALBEDO=mix(ALBEDO,reflection_tint*.42,puddle*(.18+fresnel*.55));
    ROUGHNESS=mix(.92,.19,puddle);
    SPECULAR=mix(.12,.8,wetness);
}
