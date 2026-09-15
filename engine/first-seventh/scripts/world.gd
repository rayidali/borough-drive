extends Node3D

signal progress(value: float)
const S = preload("res://scripts/shapes.gd")
var data: Dictionary
var paint = ShaderMaterial.new()
var glow = ShaderMaterial.new()
var glass: StandardMaterial3D
var asphalt = ShaderMaterial.new()
var geometry: Node3D
var street_lights: Array[MeshInstance3D] = []
var failed_assets: Array[String] = []
var visible_buildings = 0
var building_roots: Array[Node3D] = []
var sidewalk: Material
var road_paint: Material
var metal: Material
var local_lights: Array[OmniLight3D] = []

func _ready():
	paint.shader = preload("res://shaders/paint.gdshader")
	glow.shader = paint.shader
	glow.set_shader_parameter("luminous",true)
	for target in [paint,glow]:
		for entry in [["brick","red_brick_03"],["pale","white_bricks"],["stone","concrete_wall_006"]]:
			target.set_shader_parameter(entry[0]+"_color",load("res://assets/surfaces/"+entry[1]+"_diff_1k.jpg"))
			target.set_shader_parameter(entry[0]+"_normal",load("res://assets/surfaces/"+entry[1]+"_nor_gl_1k.jpg"))
	glass = S.material(Color(0.83,.90,.94,.32),.25)
	glass.vertex_color_use_as_albedo = true
	glass.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	glass.cull_mode = BaseMaterial3D.CULL_DISABLED
	asphalt.shader = preload("res://shaders/road.gdshader")
	sidewalk = ShaderMaterial.new()
	sidewalk.shader = preload("res://shaders/sidewalk.gdshader")
	sidewalk.set_shader_parameter("surface",load("res://assets/surfaces/concrete_wall_006_diff_1k.jpg"))
	road_paint = S.material(Color("dfd6b7"))
	metal = S.material(Color("48575b"),.65)
	geometry = Node3D.new()
	geometry.name = "Streets"
	add_child(geometry)

func build() -> bool:
	var file = FileAccess.open("res://assets/slice.json",FileAccess.READ)
	if file == null: return false
	var parsed = JSON.parse_string(file.get_as_text())
	if not parsed is Dictionary or not parsed.has("buildings"): return false
	data = parsed
	build_streets()
	build_props()
	batch_details()
	var entries = data.buildings.duplicate()
	entries.sort_custom(func(a,b): return Vector2(a.position[0],a.position[2]).length_squared()<Vector2(b.position[0],b.position[2]).length_squared())
	for i in entries.size():
		var b = entries[i]
		var scene = load(b.asset)
		if scene is PackedScene:
			var model = scene.instantiate()
			model.position = Vector3(b.position[0],0,b.position[2])
			model.name = "Building_"+str(b.id)
			add_child(model)
			apply_materials(model)
			building_roots.append(model)
			add_building_collision(b)
		else:
			failed_assets.append(b.asset)
		progress.emit(float(i+1)/entries.size())
		if i%30 == 0: print("SEVENTH_BUILDINGS ",i+1,"/",entries.size())
		if i%3 == 0: await get_tree().process_frame
	return failed_assets.is_empty()

func apply_materials(node: Node):
	if node is MeshInstance3D:
		for i in node.mesh.get_surface_count():
			var original = node.get_active_material(i)
			var material_name = original.resource_name.to_lower() if original else ""
			var chosen: Material = glass if "glass" in material_name else glow if "illuminated" in material_name else paint
			node.set_surface_override_material(i,chosen)
			if chosen == glass: node.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		node.lod_bias = .7
	for child in node.get_children(): apply_materials(child)

func add_building_collision(b: Dictionary):
	var body = StaticBody3D.new()
	body.name = "Collision_"+str(b.id)
	add_child(body)
	var faces = PackedVector3Array()
	var p = b.footprint
	for i in p.size():
		var a = Vector3(p[i][0],.12,p[i][1])
		var c = Vector3(p[(i+1)%p.size()][0],.12,p[(i+1)%p.size()][1])
		var top = Vector3.UP*float(b.height)
		faces.append_array([a,c,c+top,a,c+top,a+top])
	var collision = CollisionShape3D.new()
	var shape = ConcavePolygonShape3D.new()
	shape.backface_collision = true
	shape.set_faces(faces)
	collision.shape = shape
	body.add_child(collision)

func build_streets():
	S.solid_box(self,Vector3(-7,-.22,-26),Vector3(690,.4,265),null)
	S.box(geometry,Vector3(-7,-.015,-26),Vector3(690,.025,265),asphalt)
	# Original mapped road centerlines and widths; the sidewalk fills the intervening blocks.
	var x_ranges = [[-350.0,-239.75],[-218.25,-10.75],[10.75,204.7],[223.3,335.0]]
	var z_ranges = [[-165.0,-82.85],[-72.95,-4.95],[4.95,108.0]]
	var curb = S.material(Color("c8bdab"))
	for xs in x_ranges:
		for zs in z_ranges:
			var center = Vector3((xs[0]+xs[1])*.5,.07,(zs[0]+zs[1])*.5)
			S.solid_box(self,center,Vector3(xs[1]-xs[0],.14,zs[1]-zs[0]),null)
			S.box(geometry,center,Vector3(xs[1]-xs[0],.14,zs[1]-zs[0]),sidewalk)
			for x in xs:
				S.box(geometry,Vector3(x,.112,center.z),Vector3(.18,.105,zs[1]-zs[0]),curb)
			for z in zs:
				S.box(geometry,Vector3(center.x,.112,z),Vector3(xs[1]-xs[0],.105,.18),curb)
	var joint = S.material(Color("989587"))
	for x in [0.0,-229.0,214.0]:
		for z in range(-119,63,3):
			if x==214.0 and z < -37: continue
			if abs(z)<8 or abs(z+77.9)<8: continue
			for side in [-1,1]:
				S.box(geometry,Vector3(x+side*12.7,.147,z),Vector3(3.65,.006,.026),joint)
		for z in range(-112,56,6):
			if x==214.0 and z < -37: continue
			if abs(z)<12 or abs(z+77.9)<12: continue
			for line_x in [-3.45,3.45]:
				S.box(geometry,Vector3(x+line_x,.005,z),Vector3(.085,.012,2.4),road_paint)
			S.box(geometry,Vector3(x-7.0,.006,z),Vector3(.12,.012,4.0),road_paint)
		# Muted protected cycleway; continuous route interrupts at crossings.
		var cycle = S.material(Color("708e85"))
		for interval in [[-119.0,-88.0],[-67.0,-11.0],[11.0,56.0]]:
			if x==214.0: continue
			S.box(geometry,Vector3(x-9.25,.003,(interval[0]+interval[1])/2),Vector3(2.35,.008,interval[1]-interval[0]),cycle)
	for z in [0.0,-77.9]:
		for x in range(-298,286 if z==0.0 else 75,12):
			if abs(x)<17 or abs(x+229)<17 or abs(x-214)<17: continue
			# Directional lane markers on the existing one-way cross streets.
			S.box(geometry,Vector3(x,.006,z+2.0),Vector3(4.0,.012,.085),road_paint)
		for x in [0.0,-229.0,214.0]:
			if x==214.0 and z!=0.0: continue
			for side in [-1,1]:
				for mark in range(-7,8):
					S.box(geometry,Vector3(x+mark*1.12,.008,z+side*7.2),Vector3(.53,.015,2.6),road_paint)
				for mark in range(-3,4):
					S.box(geometry,Vector3(x+side*12.7,.01,z+mark*1.17),Vector3(2.75,.014,.56),road_paint)
	# Visible terminal barriers and solid limits make the small map deliberate.
	var barrier = S.material(Color("8faaa0"))
	for x in [0.0,-229.0,214.0]:
		for z in ([-38.0,57.0] if x==214.0 else [-119.0,57.0]):
			S.solid_box(self,Vector3(x,1.0,z),Vector3(21.5,2.0,.4),null)
			for sx in range(-9,10,3):
				S.box(geometry,Vector3(x+sx,.65,z),Vector3(2.5,.23,.20),barrier)
				for dx in [-.95,.95]: S.box(geometry,Vector3(x+sx+dx,.34,z),Vector3(.11,.70,.32),metal)
			boundary_sign(Vector3(x,1.40,z),"SLOW STREETS",PI if z<0 else 0.0)
	for z in [0.0,-77.9]:
		for x in ([-306.0,289.0] if z==0.0 else [-269.0,77.0]):
			S.solid_box(self,Vector3(x,1.0,z),Vector3(.4,2.0,9.9),null)
			for sz in [-3.0,0.0,3.0]:
				S.box(geometry,Vector3(x,.65,z+sz),Vector3(.20,.23,2.5),barrier)
				for dz in [-.95,.95]: S.box(geometry,Vector3(x,.34,z+sz+dz),Vector3(.32,.70,.11),metal)
	# World limits also catch attempts to drive around the visible road ends.
	for x in [-317,300]: S.solid_box(self,Vector3(x,10,-31),Vector3(1,30,190),null)
	for z in [-130,67]: S.solid_box(self,Vector3(-8,10,z),Vector3(620,30,1),null)
	S.solid_box(self,Vector3(190,10,-48),Vector3(225,30,1),null)
	S.solid_box(self,Vector3(81,10,-90),Vector3(1,30,84),null)

func boundary_sign(p: Vector3, text: String, angle: float):
	var label = Label3D.new()
	label.position = p
	label.text = text
	label.font_size = 32
	label.pixel_size = .008
	label.modulate = Color("e8d7b6")
	label.outline_modulate = Color("4c6660")
	label.outline_size = 9
	label.rotation.y = angle
	add_child(label)

func build_props():
	var details = preload("res://scripts/street_detail.gd").new()
	details.dress(geometry)
	var bulb = S.material(Color("ffdfaa"),.7,1.0)
	# These movable props are authored atmosphere, retaining the parent's uncertainty.
	for x in [0.0,-229.0]:
		for side in [-1,1]:
			for z in [-104.0,-54.0,-23.0,31.0]:
				var px = x+side*12.4
				S.cylinder(geometry,Vector3(px,3.9,z),.095,7.8,metal)
				S.box(geometry,Vector3(px-side*.7,7.8,z),Vector3(1.5,.085,.085),metal)
				S.box(geometry,Vector3(px-side*1.4,7.69,z),Vector3(.48,.12,.25),bulb)
	for z in [-77.9]:
		for side in [-1,1]:
			for x in [-204.0,-154.0,-107.0,-63.0,55.0]:
				var p = Vector3(x,0,z+side*7.3)
				details.tree(geometry,p,.83)
	var manhole = S.material(Color("555965"),.60)
	for p in [Vector3(-4,.008,1),Vector3(3,.008,-28),Vector3(-36,.008,-1),Vector3(-145,.008,-78),Vector3(-229,.008,-32)]:
		S.cylinder(geometry,p,.47,.02,manhole,24)
		for i in range(-2,3): S.box(geometry,p+Vector3(0,.015,i*.115),Vector3(.63,.008,.021),metal)
	var sign_green = S.material(Color("517774"))
	var signal_black = S.material(Color("39494b"))
	for x in [0.0,-229.0,214.0]:
		for z in [0.0,-77.9]:
			if x==214.0 and z!=0.0: continue
			for side in [-1,1]:
				var p = Vector3(x+side*12.0,0,z+side*6.5)
				S.cylinder(geometry,p+Vector3(0,3.2,0),.11,6.4,metal)
				S.box(geometry,p+Vector3(-side*2.8,6.3,0),Vector3(5.7,.10,.10),metal)
				S.box(geometry,p+Vector3(-side*5.4,5.85,0),Vector3(.34,.85,.30),signal_black)
				S.box(geometry,p+Vector3(0,4.3,0),Vector3(1.5,.26,.09),sign_green)
				S.box(geometry,p+Vector3(-side*5.4,5.65,-side*.17),Vector3(.18,.17,.035),S.material(Color("b9d491"),.6,1))
	# Benches and restrained parking provide depth without masking the corner shops.
	var wood = S.material(Color("a58b6c"))
	for p in [Vector3(-95,0,7.2),Vector3(-179,0,-7.2),Vector3(12.9,0,-36)]:
		for z in [-.24,0.0,.24]: S.box(geometry,p+Vector3(0,.57,z),Vector3(1.7,.075,.15),wood)
		for x in [-.65,.65]: S.box(geometry,p+Vector3(x,.3,0),Vector3(.085,.60,.57),metal)
	# Small unshadowed pools of actual light, with distance fading. Static furniture
	# remains batched; only lamps close enough to matter illuminate a street wall.
	for side in [-1,1]:
		for x in [-190,-111,-52,64,137,188]:
			var light = OmniLight3D.new()
			light.position = Vector3(x+1.25,5.8,side*6.15)
			light.light_color = Color("ffcf91")
			light.omni_range = 10.5
			light.omni_attenuation = 1.7
			light.shadow_enabled = false
			light.distance_fade_enabled = true
			light.distance_fade_begin = 55
			light.distance_fade_length = 18
			add_child(light)
			local_lights.append(light)

func batch_details():
	# One shared mesh per material for this finite low-poly street kit.
	# Buildings remain individual, with importer-generated LOD and frustum culling.
	var groups = {}
	for item in geometry.get_children():
		if not item is MeshInstance3D: continue
		var mat = item.material_override
		var key = mat.get_instance_id()
		if not groups.has(key): groups[key] = {"mat":mat,"tool":SurfaceTool.new(),"items":[]}
		if groups[key].items.is_empty(): groups[key].tool.begin(Mesh.PRIMITIVE_TRIANGLES)
		groups[key].tool.append_from(item.mesh,0,item.transform)
		groups[key].items.append(item)
	for entry in groups.values():
		entry.tool.index()
		var mesh_instance = MeshInstance3D.new()
		mesh_instance.mesh = entry.tool.commit()
		mesh_instance.material_override = entry.mat
		geometry.add_child(mesh_instance)
		for item in entry.items: item.free()

func set_weather(dusk: float, wet: float, reflection: Color):
	paint.set_shader_parameter("dusk",dusk)
	paint.set_shader_parameter("window_sky",Color("719ab2").lerp(reflection,.35+wet*.3))
	glow.set_shader_parameter("dusk",dusk)
	asphalt.set_shader_parameter("wetness",wet)
	asphalt.set_shader_parameter("reflection_tint",reflection)
	for light in local_lights: light.light_energy = dusk*1.35
