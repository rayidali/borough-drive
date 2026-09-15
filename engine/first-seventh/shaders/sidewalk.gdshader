shader_type spatial;
uniform vec3 tint : source_color = vec3(.57,.55,.49);
uniform sampler2D surface : source_color, filter_linear_mipmap_anisotropic, repeat_enable;
varying vec3 world_pos;
void vertex() { world_pos=(MODEL_MATRIX*vec4(VERTEX,1.0)).xyz; }
void fragment() {
    vec3 grit=texture(surface,world_pos.xz*.35).rgb;
    vec2 grid=abs(fract(world_pos.xz/1.5)-.5);
    float seam=smoothstep(.486,.498,max(grid.x,grid.y));
    ALBEDO=tint*clamp(grit/vec3(.43,.43,.41),vec3(.70),vec3(1.2))*(1.0-seam*.12);
    ROUGHNESS=.97;
    SPECULAR=.06;
}
