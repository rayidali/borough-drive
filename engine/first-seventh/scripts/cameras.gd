extends Node3D

const NAMES = ["Chase", "Hood", "Cockpit", "Overhead"]
const ORBIT_SENSITIVITY = .005
const PITCH_SENSITIVITY = .004
const PAN_SENSITIVITY = .045
const ZOOM_MIN = .58
const ZOOM_MAX = 2.8
const PAN_X_LIMIT = 15.0
const PAN_Y_LIMIT = 28.0
const PAN_Z_LIMIT = 18.0
var car: CharacterBody3D
var camera: Camera3D
var mode = 0
var orbit_yaw: float = 0.0
var orbit_pitch: float = 0.0
var zoom: float = 1.0
var pan_focus = Vector3.ZERO
var holding = false
var panning = false
var right_holding = false
var middle_holding = false
var right_pan = false
var input_enabled = false
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
	recenter_inspection()
	if car: car.set_cockpit(mode==2)

func set_input_enabled(value: bool):
	input_enabled = value
	if not value: clear_input()

func clear_input():
	holding = false
	panning = false
	right_holding = false
	middle_holding = false
	right_pan = false

func update_drag_state():
	holding = right_holding or middle_holding
	panning = middle_holding or (right_holding and right_pan)

func recenter_inspection():
	orbit_yaw = 0.0
	orbit_pitch = 0.0
	zoom = 1.0
	pan_focus = Vector3.ZERO
	clear_input()
	snap_next = true

func orbit_by(delta: Vector2):
	orbit_yaw = wrapf(orbit_yaw-delta.x*ORBIT_SENSITIVITY,-PI,PI)
	orbit_pitch = clampf(orbit_pitch+delta.y*PITCH_SENSITIVITY,-.52,1.03)

func pan_by(delta: Vector2):
	var screen_right = Vector3.RIGHT
	var screen_up = Vector3.UP
	if is_instance_valid(camera):
		screen_right = camera.global_transform.basis.x
		screen_up = camera.global_transform.basis.y
	# Pan follows the current screen, so dragging upward continues toward roofs
	# after orbiting. The resulting world offset is clamped around the car.
	pan_focus += (-screen_right*delta.x-screen_up*delta.y)*PAN_SENSITIVITY
	pan_focus.x = clampf(pan_focus.x,-PAN_X_LIMIT,PAN_X_LIMIT)
	pan_focus.y = clampf(pan_focus.y,-2.0,PAN_Y_LIMIT)
	pan_focus.z = clampf(pan_focus.z,-PAN_Z_LIMIT,PAN_Z_LIMIT)
	var horizontal = Vector2(pan_focus.x,pan_focus.z)
	if horizontal.length() > 22.0:
		horizontal = horizontal.normalized()*22.0
		pan_focus.x = horizontal.x
		pan_focus.z = horizontal.y

func zoom_by(steps: float):
	zoom = clampf(zoom*pow(.90,steps),ZOOM_MIN,ZOOM_MAX)

func _unhandled_input(event):
	if not input_enabled: return
	if event is InputEventKey and event.pressed and not event.echo and event.physical_keycode == KEY_V:
		recenter_inspection()
		return
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_RIGHT:
			right_holding = event.pressed
			right_pan = event.pressed and event.shift_pressed
			update_drag_state()
			return
		if event.button_index == MOUSE_BUTTON_MIDDLE:
			middle_holding = event.pressed
			update_drag_state()
			return
		if event.pressed and event.button_index == MOUSE_BUTTON_WHEEL_UP:
			zoom_by(1.0)
			return
		if event.pressed and event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			zoom_by(-1.0)
			return
	if event is InputEventMouseMotion and holding:
		if middle_holding or (right_holding and (right_pan or Input.is_key_pressed(KEY_SHIFT))): pan_by(event.relative)
		else: orbit_by(event.relative)

func _process(dt):
	if input_enabled:
		# A release can be consumed by a HUD Control or outside the canvas. Keep
		# the engine's drag state in sync with the physical buttons in that case.
		var physical_right = Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT)
		var physical_middle = Input.is_mouse_button_pressed(MOUSE_BUTTON_MIDDLE)
		if right_holding and not physical_right:
			right_holding = false
			right_pan = false
		if middle_holding and not physical_middle:
			middle_holding = false
		update_drag_state()
	if not is_instance_valid(car): return
	var pose = car.get_global_transform_interpolated()
	var origin = pose.origin
	var forward = -pose.basis.z
	var focus: Vector3
	var target: Vector3
	var desired: Vector3
	if mode == 0 or mode == 3:
		focus = origin+pan_focus
		var baseline = (pose.basis.z*(7.8+min(abs(car.speed)*.075,1.25))+Vector3.UP*3.5) if mode == 0 else Vector3(9,22,15)
		var offset = baseline.rotated(Vector3.UP,orbit_yaw)
		var orbit_right = pose.basis.x.rotated(Vector3.UP,orbit_yaw) if mode == 0 else Vector3.UP.cross(offset).normalized()
		if absf(orbit_pitch) > .0001: offset = offset.rotated(orbit_right,-orbit_pitch)
		var distance_scale = clampf(zoom,4.5/offset.length(),45.0/offset.length())
		offset *= distance_scale
		# Preserve the original height at zero inspection offset while keeping
		# roof inspection within a useful bounded range.
		offset.y = clampf(offset.y,1.0,30.0)
		desired = focus+offset
		target = focus+(forward*(2.4 if mode == 0 else 1.4))+Vector3.UP*(1.15 if mode == 0 else 0.0)
	else:
		# Hood and cockpit remain attached to the car while pan_focus moves the
		# camera and target together for roof and frontage inspection.
		var right = pose.basis.x
		var inspection_origin = origin+pan_focus
		desired = inspection_origin+(right*-.4-forward*.32 if mode == 2 else forward*1.52)+Vector3.UP*(1.40 if mode == 2 else 1.19)
		var look_direction = forward.rotated(Vector3.UP,orbit_yaw)
		var look_right = right.rotated(Vector3.UP,orbit_yaw)
		look_direction = look_direction.rotated(look_right,-orbit_pitch)
		target = desired+look_direction*(12.0*zoom)+Vector3.UP*(.15 if mode==2 else .10)
	if mode == 0 or mode == 3:
		var start = origin+Vector3.UP*1.3 if pan_focus.is_zero_approx() else focus+Vector3.UP*1.3
		var query = PhysicsRayQueryParameters3D.create(start,desired,1,[car.get_rid()])
		var hit = get_world_3d().direct_space_state.intersect_ray(query)
		if hit and hit.position.distance_to(focus)<45.0: desired = hit.position+hit.normal*.30
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
	var target_fov = 56.0 if mode==3 else 61.0+min(abs(car.speed)*.35,6)
	target_fov = clampf(target_fov*zoom,34.0,82.0)
	camera.fov = lerp(camera.fov,target_fov,1-exp(-dt*3))

func camera_state() -> Dictionary:
	return {"mode":mode,"position":[camera.global_position.x,camera.global_position.y,camera.global_position.z],"target":[look_point.x,look_point.y,look_point.z],"yaw":orbit_yaw,"pitch":orbit_pitch,"zoom":zoom,"pan":[pan_focus.x,pan_focus.y,pan_focus.z],"inspecting":absf(orbit_yaw)>.001 or absf(orbit_pitch)>.001 or absf(zoom-1.0)>.001 or pan_focus.length()>.001}
