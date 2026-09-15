extends Node3D

const World = preload("res://scripts/world.gd")
const Car = preload("res://scripts/car.gd")
const Cameras = preload("res://scripts/cameras.gd")
const Weather = preload("res://scripts/weather.gd")
const HUD = preload("res://scripts/hud.gd")
const CarAudio = preload("res://scripts/car_audio.gd")
var world
var car
var cameras
var weather
var hud
var ready_to_play = false
var started = false
var paused = false
var audio_enabled = false
var music: AudioStreamPlayer
var car_audio
var rain_sound: AudioStreamPlayer
var initial_camera = 0
var initial_weather = 0
var frame_window: Array[float] = []
var scale_3d = 1.0
var seconds_stopped = 0.0
var budget_cooldown = 0.0
var session_time = 0.0
var review_mode = false
var review_dir = ""
var telemetry: Array[Dictionary] = []
var collect_frames = false
var started_ms = Time.get_ticks_msec()
var browser_review = false
var stats_timer = 0.0
var browser_focus_callback
var facade_review = false

func _ready():
	print("SEVENTH_OPENING")
	if OS.has_feature("web"):
		browser_review = bool(JavaScriptBridge.eval("window.boroughReview === true"))
		browser_focus_callback = JavaScriptBridge.create_callback(browser_focus_changed)
		JavaScriptBridge.get_interface("document").addEventListener("visibilitychange",browser_focus_callback)
		JavaScriptBridge.get_interface("window").addEventListener("blur",browser_focus_callback)
	for arg in OS.get_cmdline_user_args():
		if arg == "--facade-review": facade_review = true
		if arg.begins_with("--review-out="):
			review_mode = true
			review_dir = arg.trim_prefix("--review-out=")
	configure_input()
	if not review_mode: restore_settings()
	world = World.new()
	add_child(world)
	weather = Weather.new()
	add_child(weather)
	weather.world = world
	cameras = Cameras.new()
	add_child(cameras)
	hud = HUD.new()
	add_child(hud)
	world.progress.connect(hud.set_progress)
	hud.start_requested.connect(begin)
	hud.camera_requested.connect(change_camera)
	hud.weather_requested.connect(change_weather)
	hud.pause_requested.connect(toggle_pause)
	hud.reset_requested.connect(reset)
	hud.audio_requested.connect(toggle_audio)
	hud.photo_requested.connect(postcard)
	await get_tree().process_frame
	var ok = await world.build()
	if not ok:
		hud.loaded(false)
		push_error("The slice did not load completely: "+str(world.failed_assets))
		if OS.has_feature("web"): JavaScriptBridge.eval("window.seventhLoadFailed()")
		return
	car = Car.new()
	add_child(car)
	car.reset_car()
	var tire_effects = preload("res://scripts/tire_effects.gd").new()
	tire_effects.car = car
	add_child(tire_effects)
	cameras.car = car
	hud.minimap.car = car
	cameras.set_mode(initial_camera)
	weather.car = car
	weather.select(initial_weather,true)
	setup_audio()
	await warm_street_views()
	ready_to_play = true
	hud.loaded(true)
	print("SEVENTH_READY ",Time.get_ticks_msec()-started_ms," ms; ",world.building_roots.size()," building objects")
	if review_mode: call_deferred("run_review")

func warm_street_views():
	# Upload the two street walls/foliage while the opening screen is present.
	# First-visit profiling showed a hitch when turning onto Seventh; a few
	# hidden views move that work before the player takes control.
	cameras.set_process(false)
	for x in [-140.0,135.0]:
		for direction in [-1.0,1.0]:
			cameras.camera.position = Vector3(x,2.9,0)
			cameras.camera.look_at(Vector3(x+direction*45,2.9,0),Vector3.UP)
			await get_tree().process_frame
			await RenderingServer.frame_post_draw
	cameras.snap_next = true
	cameras.set_process(true)
	await get_tree().process_frame
	await RenderingServer.frame_post_draw

func configure_input():
	var bindings = {"accelerate":[KEY_W,KEY_UP],"brake":[KEY_S,KEY_DOWN],"left":[KEY_A,KEY_LEFT],"right":[KEY_D,KEY_RIGHT],"handbrake":[KEY_SPACE]}
	for action in bindings:
		if not InputMap.has_action(action): InputMap.add_action(action)
		for key in bindings[action]:
			var event = InputEventKey.new()
			event.physical_keycode = key
			InputMap.action_add_event(action,event)

func begin():
	if not ready_to_play: return
	started = true
	paused = false
	car.enabled = true
	hud.begin()
	if audio_enabled: apply_audio()

func change_camera():
	if not ready_to_play: return
	cameras.cycle()
	save_settings()

func change_weather(value: int):
	weather.select(value)
	save_settings()

func toggle_pause():
	if not started: return
	paused = not paused
	car.enabled = not paused
	if paused:
		car.stop_car()
	hud.set_paused(paused)

func reset():
	if not ready_to_play: return
	car.reset_car()
	cameras.set_process(true)
	cameras.camera.projection = Camera3D.PROJECTION_PERSPECTIVE
	car.visible = true
	if started:
		hud.top.visible = hud.shown
		hud.bottom.visible = hud.shown
	cameras.snap_next = true
	paused = false
	car.enabled = started
	hud.set_paused(false)
	hud.toast("Back at First & Seventh")

func _unhandled_input(event):
	if not event is InputEventKey or not event.pressed or event.echo: return
	if not started and event.physical_keycode in [KEY_ENTER,KEY_W,KEY_UP]: begin()
	match event.physical_keycode:
		KEY_C: change_camera()
		KEY_T: change_weather(weather.mode+1)
		KEY_R: reset()
		KEY_ESCAPE: toggle_pause()
		KEY_H: hud.toggle_interface()
		KEY_P: postcard()
		KEY_M: toggle_audio()
		KEY_F:
			var fullscreen = DisplayServer.window_get_mode()==DisplayServer.WINDOW_MODE_FULLSCREEN
			DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED if fullscreen else DisplayServer.WINDOW_MODE_FULLSCREEN)

func _notification(what):
	if what in [NOTIFICATION_APPLICATION_FOCUS_OUT,NOTIFICATION_WM_WINDOW_FOCUS_OUT] and started and not review_mode:
		pause_for_focus_loss()

func browser_focus_changed(_arguments: Array):
	if started and bool(JavaScriptBridge.eval("document.hidden || !document.hasFocus()")):
		pause_for_focus_loss()

func pause_for_focus_loss():
	paused = true
	car.enabled = false
	car.stop_car()
	cameras.holding = false
	hud.set_paused(true)
	for action in ["accelerate","brake","left","right","handbrake"]:
		Input.action_release(action)

func _process(dt):
	if not ready_to_play: return
	session_time += dt
	if browser_review:
		var command_text = JavaScriptBridge.eval("window.seventhReviewCommand ? JSON.stringify(window.seventhReviewCommand) : ''")
		if command_text is String and not command_text.is_empty():
			var command = JSON.parse_string(command_text)
			JavaScriptBridge.eval("window.seventhReviewCommand=null")
			if command is Dictionary:
				if command.get("type") == "pose":
					reset()
					car.position = Vector3(float(command.x),.15,float(command.z))
					car.rotation.y = float(command.yaw)
					car.reset_physics_interpolation()
				elif command.get("type") == "frontage":
					show_review_frontage(int(command.id),bool(command.get("close",false)),float(command.get("along",.5)),float(command.get("span",1.0)))
				JavaScriptBridge.eval("window.seventhReviewAck="+str(int(command.get("sequence",0))))
		stats_timer += dt
		if stats_timer >= .25:
			stats_timer = 0.0
			var stats = {"ready":ready_to_play,"started":started,"paused":paused,"frames":Engine.get_frames_drawn(),"fps":Engine.get_frames_per_second(),"drawCalls":RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME),"triangles":RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_PRIMITIVES_IN_FRAME),"scale":scale_3d,"position":[car.position.x,car.position.y,car.position.z],"yaw":car.rotation.y,"speed":car.speed,"camera":cameras.mode,"weather":weather.mode,"wetness":weather.current.wet,"sound":audio_enabled,"collisions":car.collision_count,"buildings":world.building_roots.size(),"persistent":OS.is_userfs_persistent()}
			stats["tickMs"] = Time.get_ticks_msec()
			stats["slipDegrees"] = rad_to_deg(car.handling.slip)
			stats["rpm"] = car.handling.rpm
			stats["gear"] = car.handling.gear
			stats["handbrake"] = car.handbraking
			stats["tireScrub"] = car.handling.tire_scrub
			JavaScriptBridge.eval("window.seventhStats="+JSON.stringify(stats))
	hud.update_display(car.speed,car.distance_driven,cameras.NAMES[cameras.mode],weather.NAMES[weather.mode],weather.mode,dt)
	hud.update_drivetrain(car.handling,car.handbraking)
	if collect_frames:
		telemetry.append({"ms":dt*1000,"calls":RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME),"primitives":RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_PRIMITIVES_IN_FRAME)})
	if started and session_time > 4 and not review_mode:
		adapt_resolution(dt)
	if audio_enabled:
		rain_sound.volume_db = linear_to_db(max(.0001,weather.current.wet*.20))

func adapt_resolution(dt):
	budget_cooldown = max(0,budget_cooldown-dt)
	if abs(car.speed) < .1:
		seconds_stopped += dt
		if seconds_stopped > 1.5 and scale_3d < 1:
			scale_3d = 1
			get_viewport().scaling_3d_scale = scale_3d
			frame_window.clear()
		return
	seconds_stopped = 0
	if dt > .12: return
	frame_window.append(dt)
	if frame_window.size() < 60: return
	var slow = 0
	for interval in frame_window:
		if interval > .020: slow += 1
	if slow > 30 and budget_cooldown <= 0 and scale_3d > .75:
		scale_3d = max(.75,scale_3d-.125)
		get_viewport().scaling_3d_scale = scale_3d
		budget_cooldown = 2.0
	frame_window.clear()

func restore_settings():
	var config = ConfigFile.new()
	if config.load("user://settings.cfg") != OK:
		if config.load("user://settings.backup.cfg") != OK: return
	initial_camera = clampi(int(config.get_value("drive","camera",0)),0,3)
	initial_weather = clampi(int(config.get_value("drive","weather",0)),0,2)
	audio_enabled = bool(config.get_value("drive","sound",false))

func save_settings():
	if review_mode or not ready_to_play: return
	var config = ConfigFile.new()
	config.set_value("drive","camera",cameras.mode)
	config.set_value("drive","weather",weather.mode)
	config.set_value("drive","sound",audio_enabled)
	var temp = "user://settings.next.cfg"
	if config.save(temp) != OK:
		hud.toast("Settings will last for this visit")
		return
	if FileAccess.file_exists("user://settings.cfg"):
		DirAccess.copy_absolute("user://settings.cfg","user://settings.backup.cfg")
	if DirAccess.rename_absolute(temp,"user://settings.cfg") != OK:
		hud.toast("Settings will last for this visit")

func setup_audio():
	music = make_loop("res://assets/audio/cornerlight.wav",-23)
	car_audio = CarAudio.new()
	car_audio.car = car
	add_child(car_audio)
	rain_sound = make_loop("res://assets/audio/rain.wav",-60)
	hud.audio_button.text = "Sound on" if audio_enabled else "Sound off"

func make_loop(path: String, level: float) -> AudioStreamPlayer:
	var player = AudioStreamPlayer.new()
	var sample = load(path).duplicate()
	if sample is AudioStreamWAV:
		sample.loop_mode = AudioStreamWAV.LOOP_FORWARD
		sample.loop_begin = 0
		sample.loop_end = roundi(sample.get_length()*sample.mix_rate)
	player.stream = sample
	player.volume_db = level
	add_child(player)
	return player

func toggle_audio():
	audio_enabled = not audio_enabled
	apply_audio()
	save_settings()

func apply_audio():
	car_audio.set_enabled(audio_enabled and started)
	for player in [music,rain_sound]:
		if not player: continue
		if audio_enabled and not player.playing: player.play()
		if not audio_enabled: player.stop()
	hud.audio_button.text = "Sound on" if audio_enabled else "Sound off"

func postcard():
	if not ready_to_play or not started: return
	var was_shown = hud.shown
	hud.top.hide()
	hud.bottom.hide()
	await RenderingServer.frame_post_draw
	var image = get_viewport().get_texture().get_image()
	var filename = "seventh-slowly-"+str(Time.get_unix_time_from_system()).replace(".","-")+".png"
	if OS.has_feature("web"):
		var encoded = Marshalls.raw_to_base64(image.save_png_to_buffer())
		JavaScriptBridge.eval("(()=>{const a=document.createElement('a');a.download='"+filename+"';a.href='data:image/png;base64,"+encoded+"';a.click();})()")
	else:
		DirAccess.make_dir_recursive_absolute("user://postcards")
		image.save_png("user://postcards/"+filename)
	hud.top.visible = was_shown
	hud.bottom.visible = was_shown
	hud.toast("Postcard saved")

func capture(name: String):
	await RenderingServer.frame_post_draw
	var image = get_viewport().get_texture().get_image()
	var result = image.save_png(review_dir+"/"+name+".png")
	assert(result==OK,"Review screenshot could not be saved")

func show_review_frontage(id: int, close: bool, along = .5, span = 1.0):
	# Explicit ?review=1 / native review only. Normal visits have no pose bridge.
	var record = null
	for entry in world.data.reviewFrontages:
		if int(entry.id)==id: record=entry;break
	if record == null: return
	car.stop_car()
	car.enabled = false
	car.visible = false
	cameras.set_process(false)
	var f = record.frontage
	var middle = Vector3(f.x+f.rx*f.length*along,0,f.z-228+f.rz*f.length*along)
	var normal = Vector3(-f.rz,0,f.rx)
	var height = 3.7 if close else float(record.height)
	var target = middle+Vector3.UP*(height*.51)
	var distance = minf(9.0,maxf(float(f.length)*span*.78,5.2)) if close else 9.0
	# A documented orthographic elevation pass stays inside the narrow street;
	# perspective closeups and gameplay captures are separate evidence.
	cameras.camera.projection = Camera3D.PROJECTION_PERSPECTIVE if close else Camera3D.PROJECTION_ORTHOGONAL
	cameras.camera.size = maxf(height*1.17,float(f.length)*.78)
	cameras.camera.global_position=middle+normal*distance+Vector3.UP*(2.1 if close else height*.51)
	cameras.camera.fov=58
	cameras.camera.look_at(target,Vector3.UP)
	hud.top.hide();hud.bottom.hide()

func run_review():
	DirAccess.make_dir_recursive_absolute(review_dir)
	var report = {"engine":Engine.get_version_info(),"renderer":"gl_compatibility","viewport":[get_viewport().size.x,get_viewport().size.y],"buildingObjects":world.building_roots.size(),"samples":[],"checks":{}}
	await get_tree().create_timer(2).timeout
	await capture("title")
	begin()
	car.testing = true
	if facade_review:
		weather.select(0,true)
		for entry in world.data.reviewFrontages:
			show_review_frontage(int(entry.id),false)
			await get_tree().create_timer(.16).timeout
			await capture("facade-"+str(int(entry.id)))
		print("SEVENTH_FACADE_REVIEW_COMPLETE ",world.data.reviewFrontages.size())
		get_tree().quit()
		return
	for mood in range(3):
		weather.select(mood,true)
		reset()
		for view in range(4):
			cameras.set_mode(view)
			await get_tree().create_timer(1).timeout
			await capture("mood-%d-camera-%d" % [mood,view])
		cameras.set_mode(0)
		reset()
		car.test_throttle = 1
		telemetry.clear()
		collect_frames = true
		await get_tree().create_timer(4).timeout
		collect_frames = false
		car.test_throttle = 0
		var elapsed = 0.0
		var calls = 0.0
		var primitives = 0.0
		var intervals = []
		for frame in telemetry:
			elapsed += frame.ms
			calls += frame.calls
			primitives += frame.primitives
			intervals.append(frame.ms)
		intervals.sort()
		report.samples.append({"weather":weather.NAMES[mood],"frames":telemetry.size(),"fps":telemetry.size()*1000/elapsed,"p95Ms":intervals[int(intervals.size()*.95)],"drawCalls":calls/telemetry.size(),"primitives":primitives/telemetry.size(),"position":[car.position.x,car.position.y,car.position.z]})
		assert(car.position.z < -8,"Throttle must move north into the map")
		await capture("drive-%d" % mood)
	# Collision sweep at a real frontage, then reverse and resets.
	reset()
	car.position = Vector3(-4,.15,-25)
	car.rotation.y = PI/2
	car.reset_physics_interpolation()
	car.test_throttle = 1
	await get_tree().create_timer(3).timeout
	assert(car.position.x > -17.0,"The car must not pass through the Tile Bar frontage")
	report.checks["building_collision"] = true
	reset()
	car.test_throttle = -1
	await get_tree().create_timer(1.5).timeout
	assert(car.position.z > 9,"Reverse must move south")
	report.checks["reverse"] = true
	car.test_throttle = 0
	reset()
	await get_tree().physics_frame
	assert(car.speed==0,"Reset must clear vehicle speed")
	report.checks["reset"] = true
	report.checks["cameras_weather_captured"] = 12
	# Exercise the whole closed street circuit, including all four turns. This
	# drives through the same controller and collisions as keyboard input.
	weather.select(1,true)
	car.testing = true
	var route = [Vector2(-12,0),Vector2(-216,0),Vector2(-229,-10),Vector2(-229,-65),Vector2(-218,-77.9),Vector2(-13,-77.9),Vector2(0,-67),Vector2(0,-12),Vector2(0,8)]
	var route_started = Time.get_ticks_msec()
	var route_collisions = car.collision_count
	for waypoint in route:
		while Vector2(car.position.x,car.position.z).distance_to(waypoint)>4:
			var difference = waypoint-Vector2(car.position.x,car.position.z)
			var angle = wrapf(atan2(-difference.x,-difference.y)-car.rotation.y,-PI,PI)
			var desired_speed = 6.5 if abs(angle)>.2 or difference.length()<16 else 10.0
			car.test_throttle = 1.0 if car.speed<desired_speed else -.15 if car.speed>desired_speed+1 else 0.0
			car.test_steer = clampf(angle*2.0,-1.0,1.0)
			if Time.get_ticks_msec()-route_started>125000:
				push_error("Street circuit timed out at "+str(car.position)+" toward "+str(waypoint))
				get_tree().quit(1)
				return
			await get_tree().physics_frame
		print("SEVENTH_WAYPOINT ",waypoint)
		if waypoint.x == -216: await capture("seventh-street")
	car.test_throttle = 0.0
	car.test_steer = 0.0
	report.checks["street_circuit"] = {"waypoints":route.size(),"seconds":(Time.get_ticks_msec()-route_started)/1000.0,"wallContacts":car.collision_count-route_collisions,"position":[car.position.x,car.position.z]}
	# Both directions through the newly connected Seventh Street extension.
	reset()
	car.position=Vector3(-275,.15,0);car.rotation.y=-PI/2
	car.reset_physics_interpolation()
	car.test_throttle=1
	var east_started=Time.get_ticks_msec()
	var east_collisions=car.collision_count
	while car.position.x<270:
		car.test_steer=clampf(wrapf(-PI/2-car.rotation.y,-PI,PI)*2.0,-1,1)
		if Time.get_ticks_msec()-east_started>55000:
			push_error("Seventh eastbound traversal timed out");get_tree().quit(1);return
		await get_tree().physics_frame
	report.checks["seventh_eastbound"]={"metres":car.position.x+275,"seconds":(Time.get_ticks_msec()-east_started)/1000.0,"wallContacts":car.collision_count-east_collisions}
	assert(car.collision_count==east_collisions,"Seventh must be connected through both blocks")
	await capture("avenue-a-arrival")
	car.test_throttle=0
	car.stop_car()
	reset()
	cameras.holding = true
	cameras.orbit_yaw = .85
	await get_tree().create_timer(1.5).timeout
	await capture("car-quarter-view")
	var file = FileAccess.open(review_dir+"/review.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"\t"))
	print("SEVENTH_REVIEW_COMPLETE ",JSON.stringify(report.samples))
	get_tree().quit()
