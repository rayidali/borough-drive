shader_type spatial;
render_mode specular_schlick_ggx, cull_disabled;
// Authored material microstructure in physical world units. These are generic
// material mechanics, with source-observed zones/colors set per storefront.
// No source photos or invented photographic texture scans are sampled.
varying vec3 world_pos;
varying vec3 world_normal;
uniform float wetness = 0.0;
float noise_at(vec2 p) { return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
void vertex() {
    world_pos = (MODEL_MATRIX*vec4(VERTEX,1.0)).xyz;
    world_normal = normalize(MODEL_NORMAL_MATRIX*NORMAL);
}
void fragment() {
    vec2 uv = abs(world_normal.y)>.70 ? world_pos.xz :
        (abs(world_normal.x)>abs(world_normal.z) ? vec2(world_pos.z,world_pos.y) : world_pos.xy);
    float kind=round(COLOR.a*16.0);
    vec3 pigment=COLOR.rgb;
    float footprint=max(length(dFdx(uv)),length(dFdy(uv)));
    float fine=mix(.5,noise_at(floor(uv*780.0)),1.0-smoothstep(.001,.004,footprint));
    ROUGHNESS=.68; SPECULAR=.35;
    if(kind<1.5) {
        // Painted frames: restrained surface variation without invented decay.
        pigment*=.985+.025*fine; ROUGHNESS=.50; SPECULAR=.45;
    } else if(kind<2.5) {
        float grain=sin(uv.x*280.0+sin(uv.y*7.0)*1.7+sin(uv.y*2.3)*3.0);
        pigment*=.97+.025*grain*(1.0-smoothstep(.003,.012,footprint))+.015*fine; ROUGHNESS=.57;
    } else if(kind<3.5) {
        // Small rectangular glazed tiles with continuous grout and bevel edge.
        vec2 grid=uv/vec2(.105,.055);
        grid.x+=mod(floor(grid.y),2.0)*.5;
        vec2 edge=min(fract(grid),1.0-fract(grid));
        float join=1.0-smoothstep(.026,.065,min(edge.x,edge.y));
        float tile=noise_at(floor(grid));
        pigment=mix(pigment*(.95+.08*tile),vec3(.40,.39,.35),join);
        ROUGHNESS=mix(.23,.91,join);SPECULAR=mix(.64,.12,join);
    } else if(kind<4.5) {
        pigment*=.96+.065*fine;ROUGHNESS=.92;SPECULAR=.12;
    } else if(kind<5.5) {
        // Woven canvas remains legible at a stopped close view; filter at distance.
        float weave=sin(uv.x*1400.0)*sin(uv.y*1400.0);
        pigment*=1.0+.045*weave*(1.0-smoothstep(.001,.005,footprint));
        ROUGHNESS=.95;SPECULAR=.10;
    } else if(kind<6.5) {
        pigment*=.99+.01*sin(uv.x*1500.0)*(1.0-smoothstep(.001,.004,footprint));METALLIC=.62;ROUGHNESS=.37;SPECULAR=.65;
    } else if(kind<7.5) {
        pigment*=.91+.13*fine;ROUGHNESS=.97;SPECULAR=.06;
    } else {
        pigment*=.985+.025*fine;ROUGHNESS=.81;SPECULAR=.16;
    }
    ALBEDO=pigment;
    ROUGHNESS=mix(ROUGHNESS,max(.27,ROUGHNESS*.78),wetness*.22);
}
void light() {
    float shade=smoothstep(-.1,.75,dot(NORMAL,LIGHT));
    DIFFUSE_LIGHT+=ALBEDO*LIGHT_COLOR*ATTENUATION*(.20+shade*.8)/3.14159;
}
