shader_type spatial;
render_mode unshaded, cull_disabled, depth_draw_never;
uniform float clock_seconds = 0.0;
varying float born;
varying float strength;
void vertex() { born = INSTANCE_CUSTOM.r; strength = INSTANCE_CUSTOM.g; }
void fragment() {
    float edge = smoothstep(0.0,0.12,UV.x) * smoothstep(0.0,0.12,1.0-UV.x);
    float ribs = 0.78 + 0.22 * step(0.3,fract(UV.x*5.0));
    ALBEDO = vec3(0.055,0.065,0.075);
    ALPHA = edge*ribs*strength*0.46*(1.0-smoothstep(12.0,20.0,clock_seconds-born));
}
