extends CharacterBody3D

const S = preload("res://scripts/shapes.gd")
var speed = 0.0
var steering = 0.0
var wetness = 0.0
var enabled = false
var testing = false
var test_throttle = 0.0
var test_steer = 0.0
var distance_driven = 0.0
var collision_count = 0
var body: Node3D
var wheel_pivots: Array[Node3D] = []
var wheel_spins: Array[Node3D] = []
var cockpit_hidden: Array[Node3D] = []
var lamps: Array[Light3D] = []
var brake_material: StandardMaterial3D
var steering_wheel: Node3D
var throttle_value = 0.0

func _ready():
	collision_layer = 2
	collision_mask = 1
	floor_snap_length = .5
	var c = CollisionShape3D.new()
	var shape = BoxShape3D.new()
	shape.size = Vector3(1.76,1.15,3.94)
	c.shape = shape
	c.position.y = .575
	add_child(c)
	build_car()

func build_car():
	body = Node3D.new()
	add_child(body)
	var apricot = S.material(Color("d48571"),.38)
	var cream = S.material(Color("e8dac2"),.5)
	var chrome = S.material(Color("91a4a1"),.3)
	chrome.metallic = .65
	var dark = S.material(Color("26323c"))
	var glass = S.material(Color("526c78"),.24)
	var rubber = S.material(Color("1e2531"))
	var leather = S.material(Color("7f554f"))
	S.rings(body,[[-2.12,1.63,.40,.71],[-1.89,1.85,.33,.89],[-.68,1.87,.34,.99],[.95,1.87,.34,.95],[1.98,1.77,.42,.84],[2.08,1.59,.48,.78]],apricot)
	S.box(body,Vector3(0,.90,-1.35),Vector3(1.62,.055,1.0),apricot)
	var cabin = S.rings(body,[[-.78,1.62,.94,.99],[-.27,1.47,.98,1.52],[.75,1.46,.98,1.53],[1.29,1.60,.94,1.00]],glass)
	cockpit_hidden.append(cabin)
	var roof = S.box(body,Vector3(0,1.54,.22),Vector3(1.46,.075,1.03),cream)
	cockpit_hidden.append(roof)
	for x in [-.76,.76]:
		var pillar = S.box(body,Vector3(x,1.26,.32),Vector3(.055,.55,.075),cream)
		cockpit_hidden.append(pillar)
		S.box(body,Vector3(x*1.14,.98,.35),Vector3(.035,.055,1.9),chrome)
		S.box(body,Vector3(x*1.19,.89,.37),Vector3(.026,.037,.25),chrome)
		S.box(body,Vector3(x*1.18,.54,0),Vector3(.04,.12,3.6),dark)
		S.box(body,Vector3(x*1.22,1.10,-.50),Vector3(.16,.13,.23),apricot)
		S.box(body,Vector3(x*1.22,1.10,-.385),Vector3(.13,.085,.008),glass)
	for z in [-2.08,2.065]:
		S.box(body,Vector3(0,.51,z),Vector3(1.70,.13,.115),chrome)
		S.box(body,Vector3(0,.49,z*1.027),Vector3(1.54,.045,.045),dark)
	S.box(body,Vector3(0,.695,-2.12),Vector3(.63,.19,.025),dark)
	for x in range(-3,4):
		S.box(body,Vector3(x*.083,.695,-2.141),Vector3(.017,.16,.013),chrome)
	var headlight = S.material(Color("fff2cc"),.3,.45)
	brake_material = S.material(Color("d95b60"),.35,.5)
	for x in [-.59,.59]:
		S.box(body,Vector3(x,.72,-2.06),Vector3(.45,.19,.065),headlight)
		S.box(body,Vector3(x,.685,2.069),Vector3(.44,.18,.055),brake_material)
		var light = SpotLight3D.new()
		light.position = Vector3(x,.76,-2.13)
		light.light_color = Color("ffdaa0")
		light.light_energy = .0
		light.spot_range = 24
		light.spot_angle = 33
		light.shadow_enabled = false
		body.add_child(light)
		lamps.append(light)
	S.box(body,Vector3(0,.62,2.10),Vector3(.35,.15,.018),cream)
	var plate = Label3D.new()
	plate.text = "SLOWLY"
	plate.font_size = 36
	plate.pixel_size = .0015
	plate.modulate = Color("39494e")
	plate.outline_size = 0
	plate.position = Vector3(0,.62,2.114)
	plate.rotation.y = 0
	body.add_child(plate)
	for z in [-1.25,1.27]:
		for x in [-.87,.87]:
			var pivot = Node3D.new()
			pivot.position = Vector3(x,.34,z)
			add_child(pivot)
			var spin = Node3D.new()
			pivot.add_child(spin)
			var tire = S.cylinder(spin,Vector3.ZERO,.335,.235,rubber,18)
			tire.rotation.z = PI/2
			var hub = S.cylinder(spin,Vector3(sign(x)*.124,0,0),.214,.026,cream,12)
			hub.rotation.z = PI/2
			var cap = S.cylinder(spin,Vector3(sign(x)*.145,0,0),.11,.025,chrome,12)
			cap.rotation.z = PI/2
			wheel_pivots.append(pivot)
			wheel_spins.append(spin)
	# A complete authored cockpit keeps first-person useful alongside chase views.
	S.box(body,Vector3(0,.66,.23),Vector3(1.5,.12,1.8),dark)
	S.box(body,Vector3(0,1.02,-.47),Vector3(1.43,.17,.31),dark)
	for x in [-.4,.4]:
		S.box(body,Vector3(x,.78,.12),Vector3(.49,.16,.50),leather)
		S.box(body,Vector3(x,1.04,.38),Vector3(.49,.49,.13),leather)
		S.box(body,Vector3(x,1.35,.39),Vector3(.27,.19,.13),leather)
	S.box(body,Vector3(0,1.07,-.292),Vector3(.34,.095,.012),S.material(Color("dcbb91"),.6,.25))
	steering_wheel = Node3D.new()
	steering_wheel.position = Vector3(-.4,1.15,-.25)
	steering_wheel.rotation.x = -.28
	body.add_child(steering_wheel)
	var torus = TorusMesh.new()
	torus.inner_radius = .143
	torus.outer_radius = .175
	torus.rings = 16
	torus.ring_segments = 8
	var wheel = S.mesh(steering_wheel,Vector3.ZERO,torus,dark)
	wheel.rotation.x = PI/2
	S.box(steering_wheel,Vector3.ZERO,Vector3(.28,.04,.04),chrome)

func set_cockpit(value: bool):
	for part in cockpit_hidden: part.visible = not value

func set_dusk(value: float):
	for light in lamps: light.light_energy = value*1.6

func reset_car():
	global_position = Vector3(-.5,.12,8)
	rotation = Vector3.ZERO
	velocity = Vector3.ZERO
	speed = 0
	steering = 0
	reset_physics_interpolation()

func _physics_process(dt):
	var throttle = 0.0
	var turn = 0.0
	var handbrake = false
	if enabled:
		throttle = test_throttle if testing else Input.get_axis("brake","accelerate")
		turn = test_steer if testing else Input.get_axis("right","left")
		handbrake = Input.is_action_pressed("handbrake") and not testing
	throttle_value = throttle
	var before = global_position
	var previous_speed = speed
	if throttle > .01:
		speed = move_toward(speed, 17.5, (13.0 if speed < -.3 else 5.4)*throttle*dt)
	elif throttle < -.01:
		speed = move_toward(speed, -5.5, (13.0 if speed > .3 else 3.6)*-throttle*dt)
	else:
		speed = move_toward(speed,0,(.65+speed*speed*.012)*dt)
	if not enabled or handbrake:
		speed = move_toward(speed,0,(12.0 if not enabled else 9.0)*dt)
	steering = move_toward(steering,turn*.52/(1+abs(speed)*.04),dt*1.9)
	rotation.y += speed/2.52*tan(steering)*dt*(1.0-wetness*.10)
	var forward = -global_basis.z
	velocity.x = forward.x*speed
	velocity.z = forward.z*speed
	velocity.y = -1.0 if is_on_floor() else max(-18,velocity.y-19.6*dt)
	move_and_slide()
	if get_slide_collision_count() > 0:
		for i in get_slide_collision_count():
			var hit = get_slide_collision(i)
			if abs(hit.get_normal().y) < .4:
				if abs(speed)>1: collision_count += 1
				speed = Vector2(velocity.x,velocity.z).dot(Vector2(forward.x,forward.z))
				break
	distance_driven += Vector2(global_position.x-before.x,global_position.z-before.z).length()
	for i in wheel_pivots.size():
		wheel_pivots[i].rotation.y = steering if i < 2 else 0.0
		wheel_spins[i].rotation.x -= speed*dt/.335
	body.rotation.z = lerp(body.rotation.z,steering*speed*.012,1-exp(-dt*7))
	body.rotation.x = lerp(body.rotation.x,clamp((speed-previous_speed)/dt*.004,-.045,.045),1-exp(-dt*6))
	steering_wheel.rotation.z = -steering*1.8
	brake_material.emission_energy_multiplier = 2.5 if throttle < 0 and speed > 0.5 or handbrake else .55
	if global_position.y < -5: reset_car()
