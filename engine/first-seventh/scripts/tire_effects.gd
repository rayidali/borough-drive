extends Node3D
## A fixed-size ring of marks: no unbounded nodes, decals or texture downloads.
const CAPACITY = 384
var car
var marks: MultiMesh
var material: ShaderMaterial
var cursor = 0
var last: Array[Vector3] = [Vector3.ZERO,Vector3.ZERO]
var connected = false
var timer = 0.0

func _ready():
	material = ShaderMaterial.new()
	material.shader = preload("res://shaders/tire_marks.gdshader")
	marks = MultiMesh.new()
	marks.transform_format = MultiMesh.TRANSFORM_3D
	marks.use_custom_data = true
	marks.mesh = QuadMesh.new()
	marks.instance_count = CAPACITY
	# Keep the tiny bounded batch in the frustum from startup, even while all
	# marks have zero area. This compiles its shader before the first drift.
	marks.custom_aabb = AABB(Vector3(-320,-1,-140),Vector3(640,10,215))
	for i in CAPACITY:
		marks.set_instance_transform(i,Transform3D(Basis.from_scale(Vector3.ZERO),Vector3.ZERO))
		marks.set_instance_custom_data(i,Color(0,0,0,0))
	var visible_marks = MultiMeshInstance3D.new()
	visible_marks.multimesh = marks
	visible_marks.material_override = material
	visible_marks.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(visible_marks)

func _process(dt: float):
	material.set_shader_parameter("clock_seconds",Time.get_ticks_msec()/1000.0)
	if not car: return
	timer += dt
	if timer < .045: return
	timer = 0
	if not car.enabled or not car.is_on_floor() or car.handling.tire_scrub<.18:
		connected = false
		return
	for i in 2:
		var p = car.global_transform*Vector3(-.87 if i==0 else .87,.025,1.27)
		var difference = p-last[i]
		difference.y = 0
		var length = difference.length()
		if connected and length>.07 and length<2.5:
			var along = difference/length
			var across = along.cross(Vector3.UP)
			var basis = Basis(across*.245,along*(length+.03),Vector3.UP)
			marks.set_instance_transform(cursor,Transform3D(basis,(p+last[i])*.5))
			marks.set_instance_custom_data(cursor,Color(Time.get_ticks_msec()/1000.0,car.handling.tire_scrub*(1-car.wetness*.55),0,0))
			cursor = (cursor+1)%CAPACITY
		last[i] = p
	connected = true
