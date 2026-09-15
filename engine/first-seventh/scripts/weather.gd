extends Node3D

const S = preload("res://scripts/shapes.gd")
const NAMES = ["Golden hour", "Blue hour", "Passing rain"]
const PRESETS = [
	{"top":Color("6c8ba9"),"horizon":Color("eebf9c"),"cloud":Color("f7d6ba"),"ambient":Color("c1b3bf"),"sun":Color("ffd5a1"),"energy":1.15,"fog":Color("d9bba9"),"density":.0030,"dusk":.08,"wet":0.0,"cover":.2},
	{"top":Color("383951"),"horizon":Color("c3899b"),"cloud":Color("dbadba"),"ambient":Color("9195bd"),"sun":Color("f9b9b4"),"energy":.56,"fog":Color("8c829f"),"density":.0042,"dusk":1.0,"wet":.22,"cover":.36},
	{"top":Color("606f87"),"horizon":Color("a7aeba"),"cloud":Color("c6c4c7"),"ambient":Color("acb7ce"),"sun":Color("cfdbec"),"energy":.48,"fog":Color("969faa"),"density":.0060,"dusk":.7,"wet":1.0,"cover":.97}
]
var mode = 0
var current: Dictionary = PRESETS[0].duplicate()
var sky_material = ShaderMaterial.new()
var sun: DirectionalLight3D
var environment: Environment
var rain: CPUParticles3D
var car: Node3D
var world: Node3D
var auto_weather = false
var auto_timer = 0.0
var rain_sound: AudioStreamPlayer
var visual_timer = 0.0
var visual_initialized = false
var applied_top = Color(-1,-1,-1)
var applied_horizon = Color(-1,-1,-1)
var applied_cloud = Color(-1,-1,-1)
var applied_ambient = Color(-1,-1,-1)
var applied_fog = Color(-1,-1,-1)
var applied_sun = Color(-1,-1,-1)
var applied_cover = -1.0
var applied_density = -1.0
var applied_energy = -1.0
var applied_wet = -1.0
var applied_dusk = -1.0

func _ready():
	sky_material.shader = preload("res://shaders/sky.gdshader")
	var sky = Sky.new()
	sky.sky_material = sky_material
	sky.radiance_size = Sky.RADIANCE_SIZE_128
	sky.process_mode = Sky.PROCESS_MODE_INCREMENTAL
	environment = Environment.new()
	environment.background_mode = Environment.BG_SKY
	environment.sky = sky
	environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.ambient_light_energy = .65
	environment.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	environment.fog_enabled = true
	environment.fog_light_energy = .9
	var env = WorldEnvironment.new()
	env.environment = environment
	add_child(env)
	sun = DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-31,-38,0)
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 90
	sun.directional_shadow_mode = DirectionalLight3D.SHADOW_PARALLEL_2_SPLITS
	sun.shadow_bias = .035
	sun.shadow_normal_bias = .75
	add_child(sun)
	rain = CPUParticles3D.new()
	rain.amount = 620
	rain.lifetime = 1.25
	rain.preprocess = .5
	rain.local_coords = false
	rain.emission_shape = CPUParticles3D.EMISSION_SHAPE_BOX
	rain.emission_box_extents = Vector3(24,4,24)
	rain.direction = Vector3(-.13,-1,.06)
	rain.spread = 5
	rain.gravity = Vector3(0,-6,0)
	rain.initial_velocity_min = 22
	rain.initial_velocity_max = 27
	var streak = QuadMesh.new()
	streak.size = Vector2(.016,.5)
	var drop = S.material(Color(.75,.84,.95,.38),1,.15)
	drop.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	drop.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	drop.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	streak.material = drop
	rain.mesh = streak
	rain.emitting = false
	add_child(rain)
	apply()

func select(value: int, instant: bool = false):
	mode = posmod(value,NAMES.size())
	auto_timer = 0
	if instant:
		current = PRESETS[mode].duplicate()
		# The initial call happens after World has finished building, so force
		# one handoff even when the selected preset matches _ready's default.
		apply(true)

func _process(dt):
	auto_timer += dt
	if auto_weather and auto_timer > 85: select(mode+1)
	var weight = 1-exp(-dt*.48)
	for key in current:
		if current[key] is Color: current[key] = current[key].lerp(PRESETS[mode][key],weight)
		else: current[key] = lerp(float(current[key]),float(PRESETS[mode][key]),weight)
	# Environment and shader uniforms do not need to be submitted at display
	# rate. Keeping the interpolation at frame rate preserves smooth gameplay,
	# while a 30 Hz visual update avoids repeated driver work once the mood has
	# settled. Vehicle wetness/dusk below remain frame rate for handling/audio.
	visual_timer += dt
	if visual_timer >= 1.0/30.0:
		visual_timer = fmod(visual_timer,1.0/30.0)
		apply()
	if car:
		rain.global_position = car.global_position+Vector3(0,18,-3)
		car.wetness = current.wet
		car.set_dusk(current.dusk)

func apply(force: bool = false):
	if not force and visual_initialized and not visual_changed(): return
	sky_material.set_shader_parameter("zenith",current.top)
	sky_material.set_shader_parameter("horizon",current.horizon)
	sky_material.set_shader_parameter("cloud_color",current.cloud)
	sky_material.set_shader_parameter("cloud_cover",current.cover)
	sky_material.set_shader_parameter("sun_brightness",1.0-current.wet*.85)
	sky_material.set_shader_parameter("sun_direction",sun.global_basis.z)
	environment.ambient_light_color = current.ambient
	environment.fog_light_color = current.fog
	environment.fog_density = current.density
	sun.light_color = current.sun
	sun.light_energy = current.energy*.60
	rain.emitting = current.wet > .40
	if world: world.set_weather(current.dusk,current.wet,current.horizon)
	applied_top = current.top
	applied_horizon = current.horizon
	applied_cloud = current.cloud
	applied_ambient = current.ambient
	applied_fog = current.fog
	applied_sun = current.sun
	applied_cover = current.cover
	applied_density = current.density
	applied_energy = current.energy
	applied_wet = current.wet
	applied_dusk = current.dusk
	visual_initialized = true

func visual_changed() -> bool:
	# A sub-thousandth change is below the useful precision of these broad
	# atmosphere colors and avoids uniform churn at the interpolation tail.
	return color_changed(current.top,applied_top) \
		or color_changed(current.horizon,applied_horizon) \
		or color_changed(current.cloud,applied_cloud) \
		or color_changed(current.ambient,applied_ambient) \
		or color_changed(current.fog,applied_fog) \
		or color_changed(current.sun,applied_sun) \
		or abs(float(current.cover)-applied_cover) > .001 \
		or abs(float(current.density)-applied_density) > .00001 \
		or abs(float(current.energy)-applied_energy) > .001 \
		or abs(float(current.wet)-applied_wet) > .001 \
		or abs(float(current.dusk)-applied_dusk) > .001

func color_changed(a: Color,b: Color) -> bool:
	return abs(a.r-b.r) > .001 or abs(a.g-b.g) > .001 or abs(a.b-b.b) > .001
