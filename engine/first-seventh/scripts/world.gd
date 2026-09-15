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

func street_void_rectangles() -> Array:
	# The exporter owns the frontage-to-map conversion. Only its explicit
	# `cutExtent` records are allowed to pierce shared street planes: guessing
	# from an address or building type would make a false basement opening.
	var rectangles: Array = []
	for well in data.get("groundVoids",[]):
		var extent = well.get("cutExtent",null)
		if extent is Array and extent.size()==4:
			rectangles.append({"x0":float(extent[0]),"x1":float(extent[1]),"z0":float(extent[2]),"z1":float(extent[3])})
		elif extent is Dictionary and extent.has("xMin") and extent.has("xMax") and extent.has("zMin") and extent.has("zMax"):
			rectangles.append({"x0":float(extent.xMin),"x1":float(extent.xMax),"z0":float(extent.zMin),"z1":float(extent.zMax)})
		elif (extent is float or extent is int) and well.get("runtimeCenter",[]).size()==2 and well.get("runtimeNormal",[]).size()==2:
			# The current exporter records a scalar curb-to-facade cut plus an
			# explicit runtime center/normal. Convert that supplied oriented box to
			# a conservative axis-aligned visual cut; never infer it from address.
			var normal=Vector2(float(well.runtimeNormal[0]),float(well.runtimeNormal[1])).normalized()
			var width=float(well.get("worldWidth",0.0));var depth=float(extent)
			if width<=0.0 or depth<=0.0 or normal.length_squared()<.99: continue
			var facade=Vector2(float(well.runtimeCenter[0]),float(well.runtimeCenter[1]))
			var center=facade+normal*depth*.5;var tangent=Vector2(-normal.y,normal.x)
			var half_x=abs(tangent.x)*width*.5+abs(normal.x)*depth*.5
			var half_z=abs(tangent.y)*width*.5+abs(normal.y)*depth*.5
			rectangles.append({"x0":center.x-half_x,"x1":center.x+half_x,"z0":center.y-half_z,"z1":center.y+half_z})
	return rectangles

func rect_hits_void(x0: float, x1: float, z0: float, z1: float, voids: Array) -> bool:
	for hole in voids:
		if x0 < hole.x1 and x1 > hole.x0 and z0 < hole.z1 and z1 > hole.z0: return true
	return false

func rectilinear_plane_with_voids(x0: float, x1: float, z0: float, z1: float, y: float, thickness: float, mat: Material, voids: Array, collision: bool):
	var x_edges: Array = [x0,x1]
	var z_edges: Array = [z0,z1]
	for hole in voids:
		if hole.x1 > x0 and hole.x0 < x1 and hole.z1 > z0 and hole.z0 < z1:
			x_edges.append(clamp(hole.x0,x0,x1))
			x_edges.append(clamp(hole.x1,x0,x1))
			z_edges.append(clamp(hole.z0,z0,z1))
			z_edges.append(clamp(hole.z1,z0,z1))
	x_edges.sort()
	z_edges.sort()
	for xi in range(x_edges.size()-1):
		for zi in range(z_edges.size()-1):
			var left=float(x_edges[xi]); var right=float(x_edges[xi+1])
			var near=float(z_edges[zi]); var far=float(z_edges[zi+1])
			if right-left < .001 or far-near < .001 or rect_hits_void(left,right,near,far,voids): continue
			var center=Vector3((left+right)*.5,y,(near+far)*.5)
			var size=Vector3(right-left,thickness,far-near)
			S.box(geometry,center,size,mat)
			if collision: S.solid_box(self,center,size,null)

func add_ground_void_collision_envelopes(voids: Array):
	# Imported stairs/railings occupy these cuts. A layer-1 invisible envelope
	# keeps the fixed-height vehicle out without adding a false visible floor or
	# putting the well on a camera-obstruction layer.
	for index in voids.size():
		var hole = voids[index]
		var body = S.solid_box(self,Vector3((hole.x0+hole.x1)*.5,.45,(hole.z0+hole.z1)*.5),Vector3(hole.x1-hole.x0,.90,hole.z1-hole.z0),null)
		body.name = "BasementWellCollision_"+str(index)
		body.collision_layer = 1
		body.collision_mask = 0

func build_streets():
	var voids = street_void_rectangles()
	S.solid_box(self,Vector3(-7,-.22,-26),Vector3(690,.4,265),null)
	# The global asphalt visual layer is tiled around below-grade envelopes too;
	# otherwise it caps imported well floors with an invented dark rectangle.
	rectilinear_plane_with_voids(-352,338,-158.5,106.5,-.015,.025,asphalt,voids,false)
	add_ground_void_collision_envelopes(voids)
	# Original mapped road centerlines and widths; the sidewalk fills the intervening blocks.
	var x_ranges = [[-350.0,-239.75],[-218.25,-10.75],[10.75,204.7],[223.3,335.0]]
	var z_ranges = [[-165.0,-82.85],[-72.95,-4.95],[4.95,108.0]]
	var curb = S.material(Color("c8bdab"))
	for xs in x_ranges:
		for zs in z_ranges:
			var center = Vector3((xs[0]+xs[1])*.5,.07,(zs[0]+zs[1])*.5)
			rectilinear_plane_with_voids(xs[0],xs[1],zs[0],zs[1],.07,.14,sidewalk,voids,true)
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

func bike_rod(root: Node3D, a: Vector3, b: Vector3, radius: float, mat: Material):
	var shape = CylinderMesh.new()
	shape.top_radius = radius
	shape.bottom_radius = radius
	shape.height = a.distance_to(b)
	shape.radial_segments = 6
	var item = S.mesh(root,(a+b)*.5,shape,mat)
	item.quaternion = Quaternion(Vector3.UP,(b-a).normalized())

func observed_bicycle(p: Vector3):
	# One parked bicycle is visible in the north-side 73-close source view.
	# This is a small authored silhouette, not a repeated street-prop recipe.
	var rubber = S.material(Color("242d2e"),.92)
	var frame = S.material(Color("9f5947"),.72)
	var chrome = S.material(Color("788687"),.62)
	var rear = p+Vector3(-.58,.35,0)
	var front = p+Vector3(.58,.35,0)
	for center in [rear,front]:
		var wheel = TorusMesh.new()
		wheel.inner_radius = .30
		wheel.outer_radius = .34
		wheel.rings = 12
		wheel.ring_segments = 4
		var wheel_item = S.mesh(geometry,center,wheel,rubber)
		wheel_item.rotation.x = PI*.5
		bike_rod(geometry,center-Vector3(0,0,.075),center+Vector3(0,0,.075),.018,chrome)
		for angle in [0.0,PI*.5,PI,PI*1.5]:
			bike_rod(geometry,center,center+Vector3(cos(angle)*.29,sin(angle)*.29,0),.012,chrome)
	var crank = p+Vector3(-.02,.43,0)
	var seat_post = p+Vector3(-.30,.74,0)
	var head = p+Vector3(.32,.73,0)
	for pair in [[rear,crank],[rear,seat_post],[seat_post,crank],[crank,head],[seat_post,head],[head,front]]:
		bike_rod(geometry,pair[0],pair[1],.026,frame)
	bike_rod(geometry,head,head+Vector3(.04,.20,0),.022,chrome)
	bike_rod(geometry,head+Vector3(.04,.20,-.13),head+Vector3(.04,.20,.13),.018,chrome)
	S.box(geometry,seat_post+Vector3(-.02,.035,0),Vector3(.23,.045,.12),frame)
	bike_rod(geometry,crank+Vector3(-.10,-.01,-.10),crank+Vector3(.10,-.01,.10),.014,chrome)
	var collision = S.solid_box(self,p+Vector3(0,.35,0),Vector3(1.45,.70,.38),null)
	collision.name = "ObservedBicycleCollision_73_75"

func build_props():
	build_vacant_church_site()
	var details = preload("res://scripts/street_detail.gd").new()
	details.dress(geometry)
	observed_bicycle(Vector3(-80,0,-6.4))
	build_observed_dining_structures()
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

func add_chain_link_segment(st: SurfaceTool, a: Vector3, b: Vector3, normal: Vector3):
	var offset = normal.cross((b-a).normalized())*.012
	for p in [a-offset,b-offset,b+offset,a-offset,b+offset,a+offset]: st.add_vertex(p)

func chain_link_fence(a: Vector3, b: Vector3, height: float, post: Material, wire: Material):
	# A connected diamond mesh, rather than spaced vertical wires, makes the
	# observed green E7 chain-link read as an actual enclosure.
	var axis = b-a
	var length = axis.length()
	var direction = axis/length
	var normal = Vector3.UP.cross(direction).normalized()
	var cell = .42
	var columns = int(floor(length/cell))
	var rows = int(floor(height/cell))
	var st = SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for col in range(columns):
		for row in range(rows):
			var center = a+direction*((col+.5)*cell)+Vector3.UP*((row+.5)*cell)
			var left = center-direction*cell*.5
			var right = center+direction*cell*.5
			var top = center+Vector3.UP*cell*.5
			var bottom = center-Vector3.UP*cell*.5
			add_chain_link_segment(st,left,top,normal)
			add_chain_link_segment(st,top,right,normal)
			add_chain_link_segment(st,right,bottom,normal)
			add_chain_link_segment(st,bottom,left,normal)
	S.mesh(geometry,Vector3.ZERO,st.commit(),wire)
	for step in range(int(floor(length/3.0))+1):
		var point = a+direction*min(float(step)*3.0,length)
		S.cylinder(geometry,point+Vector3.UP*(height*.5),.045,height,post,8)
	S.box(geometry,(a+b)*.5+Vector3.UP*.16,Vector3(length,.055,.055) if abs(direction.x)>.5 else Vector3(.055,.055,length),post)
	S.box(geometry,(a+b)*.5+Vector3.UP*(height-.08),Vector3(length,.055,.055) if abs(direction.x)>.5 else Vector3(.055,.055,length),post)

func pointed_arch_niche(center: Vector3, width: float, height: float, wall: Material, recess: Material):
	S.box(geometry,center+Vector3(0,height*.5,0),Vector3(width,height,.035),recess)
	for side in [-1.0,1.0]:
		var trim=S.box(geometry,center+Vector3(side*width*.32,height*.77,-.025),Vector3(.09,height*.48,.08),wall)
		trim.rotation.z=side*.54
	S.box(geometry,center+Vector3(0,.10,0),Vector3(width+.14,.11,.09),wall)

func construction_barrier(center: Vector3, width: float, orange: Material, yellow: Material):
	S.box(geometry,center+Vector3(0,.45,0),Vector3(width,.15,.22),orange)
	for x in [-width*.37,width*.37]: S.box(geometry,center+Vector3(x,.23,0),Vector3(.10,.46,.25),orange)
	S.box(geometry,center+Vector3(0,.90,0),Vector3(width,.07,.08),yellow)

func build_vacant_church_site():
	# The former 48 strip and the L-shaped church lot are kept separate. Their
	# envelopes are metric estimates from the dated street view and July LPC
	# current-condition material; the proposed portico is deliberately absent.
	var dirt = S.material(Color("665c49"),.98)
	var rubble = S.material(Color("877d68"),.96)
	var fence = S.material(Color("3e624f"),.84)
	var wire = S.material(Color("75917c"),.78)
	wire.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	wire.cull_mode = BaseMaterial3D.CULL_DISABLED
	# E7 former-tenement strip, then the rear L and its eastward return.
	S.box(geometry,Vector3(-201.5,.155,14.5),Vector3(33.0,.025,11.0),dirt)
	S.box(geometry,Vector3(-201.5,.155,29.5),Vector3(33.0,.025,19.0),dirt)
	S.box(geometry,Vector3(-179.5,.155,23.5),Vector3(11.0,.025,7.0),dirt)
	chain_link_fence(Vector3(-218,0,9.45),Vector3(-185,0,9.45),1.85,fence,wire)
	chain_link_fence(Vector3(-218,0,9.45),Vector3(-218,0,39),1.85,fence,wire)
	# Existing panel boards sit on the E7 strip over the chain link.
	for x in [-215.8,-211.8,-207.8]:
		var panel = S.material(Color("a99f85") if x==-215.8 else Color("875149") if x==-211.8 else Color("b8aa91"),.9)
		S.box(geometry,Vector3(x,1.10,9.39),Vector3(3.35,1.30,.035),panel)
		S.box(geometry,Vector3(x+.35,1.28,9.34),Vector3(.85,.11,.012),S.material(Color("4e5450"),.9))
	# Plywood bracing encloses the rear work area; it is construction material,
	# not the unbuilt glass proposal.
	var plywood=S.material(Color("93785a"),.93)
	for x in [-214,-207,-200,-193]:
		S.box(geometry,Vector3(x,1.45,38.7),Vector3(5.8,2.9,.12),plywood)
		var brace=S.box(geometry,Vector3(x,1.48,38.57),Vector3(.11,3.1,.11),S.material(Color("5a4a38"),.9))
		brace.rotation.z=.62
	# Remaining tan south party wall and its visible pointed niches.
	var tan=S.material(Color("9c805f"),.93)
	var dark_tan=S.material(Color("4e463c"),.92)
	S.box(geometry,Vector3(-195,4.1,20.05),Vector3(25.5,8.2,.32),tan)
	for x in [-204,-198,-192,-186]: pointed_arch_niche(Vector3(x,0,19.85),3.0,4.4,tan,dark_tan)
	# Salvaged carved stone, stored ironwork, excavation and temporary traffic kit.
	for p in [Vector3(-210,.34,24),Vector3(-208,.42,24.2),Vector3(-206,.31,24.1),Vector3(-201,.38,30),Vector3(-199,.28,30.2)]:
		S.box(geometry,p,Vector3(1.35,.42,.62),S.material(Color("c9c1ae"),.96))
		S.box(geometry,p+Vector3(.12,.25,0),Vector3(.60,.12,.18),S.material(Color("e1d7c0"),.96))
	var iron=S.material(Color("252c2c"),.75)
	for x in [-192.5,-191.8,-191.1]:
		S.cylinder(geometry,Vector3(x,1.25,31.5),.05,2.1,iron,8)
		S.cylinder(geometry,Vector3(x+.32,1.25,31.5),.05,2.1,iron,8)
		S.box(geometry,Vector3(x+.16,2.13,31.5),Vector3(.48,.06,.08),iron)
	for p in [Vector3(-211,0,18.8),Vector3(-205,0,27.1),Vector3(-186,0,22.0)]: construction_barrier(p,2.1,S.material(Color("d56c38"),.9),S.material(Color("d3b447"),.9))
	for p in [Vector3(-214,0,31),Vector3(-202,0,34),Vector3(-181,0,25)]:
		S.box(geometry,p+Vector3(0,.06,0),Vector3(2.5,.10,1.55),rubble)
		for i in range(4): S.box(geometry,p+Vector3(-.75+i*.45,.18,.18*(i%2)),Vector3(.34,.20,.28),S.material(Color("8d8069"),.94))

func build_observed_dining_shed(id: String, center: Vector3, width: float, depth: float, yubu: bool):
	var frame=S.material(Color("252b2a"),.72)
	var trim=S.material(Color("d5a63a") if yubu else Color("3b4340"),.78)
	var panel=S.material(Color("82938a"),.42)
	panel.transparency=BaseMaterial3D.TRANSPARENCY_ALPHA
	panel.cull_mode=BaseMaterial3D.CULL_DISABLED
	var side=S.material(Color("a3412f") if yubu else Color("3b403d"),.82)
	# A body collider makes both observed roadway structures non-drive-through.
	var collision = S.solid_box(self,center+Vector3(0,1.35,0),Vector3(width,2.7,depth),null)
	collision.name="DiningCollision_"+id
	for x in [-width*.5+.12,width*.5-.12]:
		for z in [-depth*.5+.12,depth*.5-.12]: S.box(geometry,center+Vector3(x,1.34,z),Vector3(.13,2.68,.13),frame)
	for z_step in range(10):
		var z=-depth*.5+(float(z_step)+.5)*depth/10.0
		var roof_y=2.73+(z/depth)*(-.22 if not yubu else .10)
		S.box(geometry,center+Vector3(0,roof_y,z),Vector3(width+.22,.085,depth/10.0+.025),frame)
	# North-side 77 faces the road on +Z: its photographed street face is
	# translucent above a dark lower panel. South-side Yubu faces -Z and keeps
	# the observed red/yellow street-end color rather than a generic dark box.
	var road_z=depth*.5-.045 if not yubu else -depth*.5+.045
	var rear_z=-road_z
	if yubu:
		S.box(geometry,center+Vector3(0,1.12,road_z),Vector3(width,2.15,.08),side)
		S.box(geometry,center+Vector3(-width*.30,1.42,road_z-.025),Vector3(width*.30,1.05,.025),trim)
		for x in [-width*.25,width*.25]: S.box(geometry,center+Vector3(x,1.38,rear_z),Vector3(width*.46,2.20,.07),panel)
	else:
		S.box(geometry,center+Vector3(0,.52,road_z),Vector3(width,.92,.08),side)
		for x in [-width*.25,width*.25]: S.box(geometry,center+Vector3(x,1.73,road_z+.01),Vector3(width*.46,1.45,.07),panel)
		S.box(geometry,center+Vector3(0,1.12,rear_z),Vector3(width,2.15,.08),side)
	S.box(geometry,center+Vector3(0,2.26,road_z-(.06 if yubu else -.06)),Vector3(width+.12,.12,.13),trim)
	if yubu:
		var sign=Label3D.new()
		sign.text="YUBU"
		sign.font_size=42
		sign.pixel_size=.010
		sign.outline_size=5
		sign.modulate=Color("f1c34a")
		sign.position=center+Vector3(0,1.72,road_z-.01)
		geometry.add_child(sign)

func build_observed_dining_structures():
	# Both are curb-anchored: they stop well clear of the fixed center route.
	build_observed_dining_shed("77-north",Vector3(-64.0,0,-3.75),6.4,2.4,false)
	build_observed_dining_shed("yubu-86-south",Vector3(-32.0,0,3.75),6.4,2.4,true)

func material_variant_key(value: Variant) -> String:
	if value is Resource:
		return "resource:"+str(value.get_instance_id())
	if value is Array:
		var values: Array[String] = []
		for entry in value: values.append(material_variant_key(entry))
		return "["+",".join(values)+"]"
	if value is Dictionary:
		var keys: Array[String] = []
		for key in value: keys.append(str(key)+"="+material_variant_key(value[key]))
		keys.sort()
		return "{"+",".join(keys)+"}"
	return str(value)

func material_key(mat: Material) -> String:
	# Shader materials carry uniforms and shader state that must stay isolated.
	# Standard materials can share when every stored property, including any
	# texture/resource identity, matches exactly.
	if not mat is StandardMaterial3D: return "identity:"+str(mat.get_instance_id())
	var properties: Array[String] = []
	for property in mat.get_property_list():
		if (int(property.usage) & PROPERTY_USAGE_STORAGE) == 0: continue
		var name = str(property.name)
		if name in ["resource_name","resource_path","resource_local_to_scene"]: continue
		properties.append(name+"="+material_variant_key(mat.get(name)))
	properties.sort()
	return "standard:"+"|".join(properties)

func batch_details():
	# Share static detail geometry globally per canonical material. Buildings
	# remain individual scene roots, retaining their own frustum/LOD culling.
	var groups = {}
	var canonical_materials = {}
	var material_keys = {}
	for item in geometry.get_children():
		if not item is MeshInstance3D: continue
		var mat = item.material_override
		var material_id = mat.get_instance_id()
		var canonical_key = material_keys.get(material_id,"")
		if canonical_key.is_empty():
			canonical_key = material_key(mat)
			material_keys[material_id] = canonical_key
		if not canonical_materials.has(canonical_key): canonical_materials[canonical_key] = mat
		mat = canonical_materials[canonical_key]
		var key = canonical_key
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
