shader_type spatial;
render_mode specular_schlick_ggx;
varying vec3 world_pos;
uniform sampler2D brick_color : source_color, filter_linear_mipmap_anisotropic, repeat_enable;
uniform sampler2D brick_normal : hint_normal, filter_linear_mipmap_anisotropic, repeat_enable;
uniform sampler2D pale_color : source_color, filter_linear_mipmap_anisotropic, repeat_enable;
uniform sampler2D pale_normal : hint_normal, filter_linear_mipmap_anisotropic, repeat_enable;
uniform sampler2D stone_color : source_color, filter_linear_mipmap_anisotropic, repeat_enable;
uniform sampler2D stone_normal : hint_normal, filter_linear_mipmap_anisotropic, repeat_enable;
uniform float dusk : hint_range(0.0,1.0) = 0.0;
uniform bool luminous = false;
uniform vec3 window_sky : source_color = vec3(.48,.63,.74);
float hash(vec2 p) { return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
void vertex() {
    world_pos = (MODEL_MATRIX * vec4(VERTEX,1.0)).xyz;
    vec3 n=normalize(MODEL_NORMAL_MATRIX*NORMAL);
    vec3 t; vec3 b;
    if (abs(n.y)>.70) {
        UV=vec2(world_pos.x,-world_pos.z*sign(n.y))*.55;
        t=vec3(1,0,0); b=vec3(0,0,-sign(n.y));
    } else if (abs(n.z)>abs(n.x)) {
        UV=vec2(world_pos.x*sign(n.z),world_pos.y)*.55;
        t=vec3(sign(n.z),0,0); b=vec3(0,1,0);
    } else {
        UV=vec2(-world_pos.z*sign(n.x),world_pos.y)*.55;
        t=vec3(0,0,-sign(n.x)); b=vec3(0,1,0);
    }
    TANGENT=transpose(MODEL_NORMAL_MATRIX)*t;
    BINORMAL=transpose(MODEL_NORMAL_MATRIX)*b;
}
void fragment() {
    vec3 pigment = COLOR.rgb;
    float kind = round(COLOR.a*8.0);
    if (kind>0.5 && kind<4.5) {
        vec3 surface;
        vec3 normal_map;
        if (kind<1.5) {
            surface=texture(brick_color,UV).rgb;
            normal_map=texture(brick_normal,UV).rgb;
            surface=surface/vec3(.37,.19,.12);
        } else if (kind<3.5) {
            surface=texture(pale_color,UV).rgb;
            normal_map=texture(pale_normal,UV).rgb;
            surface=surface/vec3(.66,.63,.58);
            if (kind>2.5) surface=mix(vec3(1.0),surface,.32);
        } else {
            surface=texture(stone_color,UV*.48).rgb;
            normal_map=texture(stone_normal,UV*.48).rgb;
            surface=surface/vec3(.43,.43,.41);
        }
        pigment *= clamp(mix(vec3(1.0),surface,.38),vec3(.76),vec3(1.24));
        NORMAL_MAP = normal_map;
        NORMAL_MAP_DEPTH = kind<3.5 ? .24 : .18;
        // Restrained lower-wall patina; uniform artistic wear, not a photo claim.
        pigment *= mix(.85,1.0,smoothstep(.15,1.4,world_pos.y));
    } else if (kind>4.5 && kind<5.5) {
        pigment *= .98+.02*sin(UV.x*160.0+sin(UV.y*9.0)*.65);
    } else if (kind>5.5) {
        // Opaque architectural glazing stays in the same building batch.
        // A restrained sky tint/fresnel makes the recess readable without
        // another reflection pass or invented room/photographic textures.
        float grazing=pow(1.0-clamp(dot(normalize(NORMAL),normalize(VIEW)),0.0,1.0),4.0);
        pigment=mix(pigment,window_sky,.32+grazing*.34);
    }
    pigment = mix(pigment, vec3(0.77,0.61,0.54),0.055);
    ALBEDO = pigment;
    ROUGHNESS = 0.88;
    SPECULAR = 0.18;
    if (kind>5.5) {
        ROUGHNESS=.24;
        SPECULAR=.55;
        EMISSION=window_sky*.07;
    }
    if (luminous) { EMISSION = pigment * mix(0.12,1.45,dusk); }
}
void light() {
    float shade = smoothstep(-0.1,0.75,dot(NORMAL,LIGHT));
    DIFFUSE_LIGHT += ALBEDO * LIGHT_COLOR * ATTENUATION * (0.20 + shade*0.8) / 3.14159;
}
