shader_type spatial;
render_mode cull_disabled, specular_disabled;
varying vec3 world_pos;
void vertex() {
    world_pos=(MODEL_MATRIX*vec4(VERTEX,1.0)).xyz;
    float breeze=sin(TIME*.85+world_pos.x*.37+world_pos.z*.23);
    VERTEX.x += breeze*.045*UV.y;
    VERTEX.z += cos(TIME*.65+world_pos.z*.41)*.025*UV.y;
}
void fragment() {
    float vein=1.0-smoothstep(.015,.045,abs(UV.x-.5));
    float small_veins=pow(max(0.0,cos((UV.y-abs(UV.x-.5)*.75)*60.0)),14.0)*.05;
    vec3 color=mix(COLOR.rgb*.72,COLOR.rgb*1.20,UV.y);
    ALBEDO=color*(1.0+vein*.15+small_veins);
    ROUGHNESS=.92;
}
void light() {
    float light_side=dot(NORMAL,LIGHT);
    DIFFUSE_LIGHT+=ALBEDO*LIGHT_COLOR*ATTENUATION*(.22+max(0.0,light_side)*.65+max(0.0,-light_side)*.28)/3.14159;
}
