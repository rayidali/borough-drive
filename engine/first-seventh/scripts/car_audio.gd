extends Node
## Small original loops, crossfaded by drivetrain load rather than vehicle speed.
var car
var enabled = false
var idle: AudioStreamPlayer
var load_voice: AudioStreamPlayer
var coast: AudioStreamPlayer
var tires: AudioStreamPlayer
var road: AudioStreamPlayer
var impact: AudioStreamPlayer
var impact_cooldown = 0.0

func _ready():
	idle = voice("engine-idle")
	load_voice = voice("engine-load")
	coast = voice("engine-coast")
	tires = voice("tires")
	road = voice("road")
	impact = voice("impact",false)

func voice(name: String, loop = true) -> AudioStreamPlayer:
	var player = AudioStreamPlayer.new()
	var sample = load("res://assets/audio/"+name+".wav").duplicate()
	if loop:
		sample.loop_mode = AudioStreamWAV.LOOP_FORWARD
		sample.loop_begin = 0
		sample.loop_end = roundi(sample.get_length()*sample.mix_rate)
	player.stream = sample
	player.volume_db = -80
	add_child(player)
	return player

func set_enabled(value: bool):
	enabled = value
	for player in [idle,load_voice,coast,tires,road]:
		if enabled and not player.playing: player.play()
		elif not enabled: player.stop()
	if not enabled: impact.stop()

func _process(dt: float):
	if not car or not enabled: return
	var h = car.handling
	var rolling = Vector2(car.velocity.x,car.velocity.z).length()
	var running = 1.0 if car.enabled else .0
	var revs = smoothstep(1000.0,2100.0,h.rpm)
	idle.pitch_scale = clampf(h.rpm/1050.0,.65,2.0)
	load_voice.pitch_scale = clampf(h.rpm/2400.0,.32,2.55)
	coast.pitch_scale = load_voice.pitch_scale
	level(idle,(1.0-revs*.85)*.105*running,dt)
	level(load_voice,(.02+revs*.15)*h.engine_load*running,dt)
	level(coast,(.012+revs*.072)*(1.0-h.engine_load*.65)*running,dt)
	tires.pitch_scale = .86+minf(rolling,24)*.012
	level(tires,h.tire_scrub*.14*(1.0-car.wetness*.45)*running,dt)
	road.pitch_scale = .65+rolling*.038
	level(road,pow(clampf(rolling/24,0,1),1.6)*.042*running,dt)
	impact_cooldown = maxf(0,impact_cooldown-dt)
	if car.impact_strength>2 and impact_cooldown<=0:
		impact.volume_db = linear_to_db(minf(car.impact_strength*.013,.21))
		impact.pitch_scale = .9
		impact.play()
		impact_cooldown = .4

func level(player: AudioStreamPlayer, target: float, dt: float):
	var amplitude = lerpf(db_to_linear(player.volume_db),target,1-exp(-dt*12))
	player.volume_db = linear_to_db(maxf(amplitude,.0001))
