extends Node3D

const NAMES = ["Chase", "Hood", "Cockpit", "Overhead"]
var car: CharacterBody3D
var camera: Camera3D
var mode = 0
var orbit_yaw: float = 0.0
var orbit_pitch: float = 0.0
var holding = false
var snap_next = true
var look_point = Vector3.ZERO

func _ready():
	physics_interpolation_mode = Node.PHYSICS_INTERPOLATION_MODE_OFF
	camera = Camera3D.new()
	camera.near = .06
	camera.far = 370
	camera.fov = 61
	camera.current = true
	add_child(camera)

func cycle():
	set_mode((mode+1)%NAMES.size())

func set_mode(value: int):
	mode = posmod(value,NAMES.size())
	orbit_yaw = 0.0
	orbit_pitch = 0.0
	snap_next = true
	if car: car.set_cockpit(mode==2)

func _unhandled_input(event):
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_RIGHT:
		holding = event.pressed
	if event is InputEventMouseMotion and holding:
		orbit_yaw -= event.relative.x*.005
		orbit_pitch = clamp(orbit_pitch+event.relative.y*.004,-.30,.65)

func _process(dt):
	if not is_instance_valid(car): return
	if not holding:
		orbit_yaw = lerp(orbit_yaw,0.0,1-exp(-dt*1.8))
		orbit_pitch = lerp(orbit_pitch,0.0,1-exp(-dt*1.8))
	var pose = car.get_global_transform_interpolated()
	var origin = pose.origin
	var forward = -pose.basis.z
	var target: Vector3
	var desired: Vector3
	match mode:
		0:
			var back = pose.basis.z.rotated(Vector3.UP,orbit_yaw)
			desired = origin+back*(7.8+min(abs(car.speed)*.075,1.25))+Vector3.UP*(3.5+orbit_pitch*6)
			target = origin+forward*2.4+Vector3.UP*1.15
		1:
			desired = origin+forward*1.52+Vector3.UP*1.19
			target = desired+forward.rotated(Vector3.UP,orbit_yaw)*12+Vector3.UP*.10
		2:
			desired = origin+pose.basis.x*-.4-forward*.32+Vector3.UP*1.40
			target = desired+forward.rotated(Vector3.UP,orbit_yaw)*12+Vector3.UP*.15
		3:
			desired = origin+Vector3(9,22,15)
			target = origin+forward*1.4
	if mode == 0 or mode == 3:
		var start = origin+Vector3.UP*1.3
		var query = PhysicsRayQueryParameters3D.create(start,desired,1,[car.get_rid()])
		var hit = get_world_3d().direct_space_state.intersect_ray(query)
		if hit: desired = hit.position+hit.normal*.30
	if snap_next:
		camera.global_position = desired
		look_point = target
		snap_next = false
	else:
		var weight = 1-exp(-dt*(7.5 if mode==0 else 16.0))
		camera.global_position = camera.global_position.lerp(desired,weight)
		look_point = look_point.lerp(target,weight)
	if camera.global_position.distance_squared_to(look_point) > .001:
		camera.look_at(look_point,Vector3.UP)
	camera.fov = lerp(camera.fov,56.0 if mode==3 else 61.0+min(abs(car.speed)*.35,6),1-exp(-dt*3))
