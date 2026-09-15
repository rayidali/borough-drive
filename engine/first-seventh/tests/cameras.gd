extends SceneTree

const Cameras = preload("res://scripts/cameras.gd")
var failures: Array[String] = []

func check(condition: bool, message: String):
	if not condition: failures.append(message)

func _initialize():
	var cameras = Cameras.new()
	check(cameras.NAMES.size() == 4,"Camera inspection must preserve all four vehicle modes")
	check(cameras.mode == 0,"Camera starts in Chase mode")
	cameras.orbit_by(Vector2(-100000,-100000))
	check(cameras.orbit_yaw <= PI and cameras.orbit_yaw >= -PI,"Orbit yaw must stay within one turn")
	check(cameras.orbit_pitch >= -.52 and cameras.orbit_pitch <= 1.03,"Orbit pitch must avoid poles")
	cameras.pan_by(Vector2(-100000,-100000))
	check(cameras.pan_focus.x <= cameras.PAN_X_LIMIT and cameras.pan_focus.x >= -cameras.PAN_X_LIMIT,"Horizontal pan must be bounded")
	check(cameras.pan_focus.y <= cameras.PAN_Y_LIMIT and cameras.pan_focus.y >= -2.0,"Vertical roof pan must be bounded")
	check(cameras.pan_focus.z <= cameras.PAN_Z_LIMIT and cameras.pan_focus.z >= -cameras.PAN_Z_LIMIT,"Depth pan must be bounded")
	cameras.zoom_by(1000.0)
	check(is_equal_approx(cameras.zoom,cameras.ZOOM_MIN),"Wheel zoom-in must stop at the near limit")
	cameras.zoom_by(-1000.0)
	check(is_equal_approx(cameras.zoom,cameras.ZOOM_MAX),"Wheel zoom-out must stop at the far limit")
	cameras.recenter_inspection()
	cameras.orbit_by(Vector2(-314.0,0.0))
	var yawed = cameras.orbit_yaw
	cameras.orbit_by(Vector2(0.0,100.0))
	check(absf(yawed)>1.4 and cameras.orbit_pitch>.3,"Pitch input must remain effective after a large yaw")
	cameras.set_mode(2)
	check(cameras.mode == 2,"Mode changes must keep Cockpit selectable")
	check(is_zero_approx(cameras.orbit_yaw) and is_zero_approx(cameras.orbit_pitch) and is_equal_approx(cameras.zoom,1.0),"Changing mode must recenter inspection state")
	cameras.set_input_enabled(true)
	cameras.right_holding = true
	cameras.middle_holding = true
	cameras.right_pan = true
	cameras.update_drag_state()
	cameras.right_holding = false
	cameras.update_drag_state()
	check(cameras.holding and cameras.panning,"Releasing right drag must preserve an active middle pan")
	cameras.middle_holding = false
	cameras.update_drag_state()
	check(not cameras.holding and not cameras.panning,"Releasing the final mouse button must stop camera drags")
	cameras.clear_input()
	check(not cameras.holding and not cameras.panning,"Focus loss clear must release camera drags")
	var mode_names = cameras.NAMES
	# This test creates the camera controller outside the scene tree, so release
	# its owned node before terminating the headless process.
	cameras.free()
	print("SEVENTH_CAMERA_TEST ",JSON.stringify({"failures":failures,"modes":mode_names}))
	quit(0 if failures.is_empty() else 1)
