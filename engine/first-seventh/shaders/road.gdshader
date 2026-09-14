shader_type spatial;
uniform float wetness : hint_range(0.0,1.0) = 0.0;
uniform vec3 reflection_tint : source_color = vec3(0.67,0.48,0.57);
varying vec3 world_pos;
float h(vec2 p) { vec3 p3=fract(vec3(p.xyx)*.1031);p3+=dot(p3,p3.yzx+33.33);return fract((p3.x+p3.y)*p3.z); }
float noise(vec2 p) { vec2 i=floor(p),f=fract(p);f=f*f*(3.0-2.0*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y); }
void vertex() { world_pos=(MODEL_MATRIX*vec4(VERTEX,1.0)).xyz; }
void fragment() {
    float n=noise(world_pos.xz*0.22);
    float fine=noise(world_pos.xz*18.0);
    vec3 dry=vec3(0.14,0.16,0.19)*(0.90+n*.14+fine*.035);
    float puddle=smoothstep(.45,.8,noise(world_pos.xz*.38))*wetness;
    float fresnel=pow(1.0-max(0.0,dot(NORMAL,VIEW)),3.0);
    ALBEDO=mix(dry,dry*.65,wetness);
    ALBEDO=mix(ALBEDO,reflection_tint*.16,puddle*(.08+fresnel*.18));
    ROUGHNESS=mix(.96,.64,wetness)-puddle*.04;
    SPECULAR=mix(.08,.14,wetness);
}
