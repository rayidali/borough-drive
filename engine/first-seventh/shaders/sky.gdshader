shader_type sky;
uniform vec3 zenith : source_color = vec3(0.36,0.48,0.68);
uniform vec3 horizon : source_color = vec3(0.96,0.70,0.56);
uniform vec3 cloud_color : source_color = vec3(1.0,0.87,0.76);
uniform vec3 sun_direction = vec3(-0.4,0.3,0.5);
uniform float cloud_cover = 0.25;
uniform float sun_brightness = 1.0;
float h(vec2 p) { return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
float n(vec2 p) { vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y); }
void sky() {
    float y=max(EYEDIR.y,0.0);
    vec3 c=mix(horizon,zenith,pow(y,.55));
    vec2 p=EYEDIR.xz/max(.12,EYEDIR.y+.15)*1.8+vec2(TIME*.008,0.0);
    float cloud=n(p)*.6+n(p*2.1)*.28+n(p*4.1)*.12;
    cloud=smoothstep(.66-cloud_cover*.25,.83-cloud_cover*.25,cloud);
    c=mix(c,cloud_color,cloud*smoothstep(0.,.15,y)*.9);
    float d=dot(EYEDIR,normalize(sun_direction));
    c+=vec3(1.0,.58,.30)*pow(max(d,0.),18.)*.22*sun_brightness;
    c=mix(c,vec3(1.,.88,.59),smoothstep(.9984,.9992,d)*sun_brightness);
    COLOR=c;
}
