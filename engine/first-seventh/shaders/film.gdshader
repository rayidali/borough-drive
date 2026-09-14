shader_type canvas_item;
render_mode unshaded;
void fragment() {
    vec2 p=UV-.5;
    float vignette=smoothstep(.19,.70,length(p));
    float grain=fract(sin(dot(floor(FRAGCOORD.xy),vec2(12.9898,78.233)))*43758.5453);
    COLOR=vec4(.075,.05,.14,vignette*.19+grain*.018);
}
