extends RefCounted
const S = preload("res://scripts/shapes.gd")
var rng = RandomNumberGenerator.new()
var metal = S.material(Color("495653"),.65)
var bark = S.material(Color("736a53"),.97)
var soil = S.material(Color("53594a"))
var wood = S.material(Color("a58b6c"))
var foliage = ShaderMaterial.new()

func _init():
	rng.seed = 7102
	foliage.shader = preload("res://shaders/foliage.gdshader")

func rod(root: Node3D, a: Vector3, b: Vector3, radius: float, mat: Material, top = -1.0):
	var shape = CylinderMesh.new()
	shape.top_radius = top if top>=0 else radius
	shape.bottom_radius = radius
	shape.height = a.distance_to(b)
	shape.radial_segments = 7
	var item = S.mesh(root,(a+b)*.5,shape,mat)
	item.quaternion = Quaternion(Vector3.UP,(b-a).normalized())

func tree(root: Node3D, p: Vector3, size = 1.0, mature = false):
	var height = (15.0 if mature else rng.randf_range(5.9,7.8))*size
	var trunk_top = p+Vector3(.08,height*(.38 if mature else .59),-.06)
	rod(root,p+Vector3(0,.14,0),trunk_top,.15*size,bark,.06*size)
	S.box(root,p+Vector3(0,.155,0),Vector3(1.65,.016,1.50)*size,soil)
	for x in [-.84,.84]:S.box(root,p+Vector3(x*size,.21,0),Vector3(.06,.12,1.58)*size,metal)
	for z in [-.79,.79]:S.box(root,p+Vector3(0,.21,z*size),Vector3(1.75,.12,.06)*size,metal)
	var clusters: Array[Vector3] = []
	for branch in range(9):
		var angle=branch*TAU/9+rng.randf_range(-.2,.2)
		var spread = 2.2 if mature else 1.0
		var tip=p+Vector3(cos(angle)*rng.randf_range(.8,1.9)*size*spread,height*rng.randf_range(.66,.93),sin(angle)*rng.randf_range(.8,1.7)*size*spread)
		rod(root,trunk_top-Vector3(0,(branch%3)*.42,0),tip,.046*size,bark,.015*size)
		clusters.append(tip)
	var st = SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	# Solid leaf silhouettes avoid expensive layers of transparent foliage.
	for i in range(700):
		var center = clusters[i%clusters.size()]+Vector3(rng.randf_range(-.8,.8),rng.randf_range(-.50,.85),rng.randf_range(-.8,.8))*size
		var tilt = Basis.from_euler(Vector3(rng.randf_range(-.9,.9),rng.randf_range(-PI,PI),rng.randf_range(-.9,.9)))
		var width=rng.randf_range(.10,.20)*size
		var length=rng.randf_range(.22,.40)*size
		var points=[Vector3(0,0,0),Vector3(-width*.72,.025,length*.25),Vector3(-width,.035,length*.60),Vector3(0,.05,length),Vector3(width,.035,length*.60),Vector3(width*.72,.025,length*.25)]
		var tint=Color("6e8a55").lerp(Color("b8ae73"),rng.randf_range(0,.52))
		for j in range(1,points.size()-1):
			for k in [0,j+1,j]:
				st.set_color(tint)
				st.set_uv(Vector2(points[k].x/(width*2)+.5,points[k].z/length))
				st.add_vertex(tilt*points[k]+center)
	st.generate_normals()
	S.mesh(root,Vector3.ZERO,st.commit(),foliage)

func hydrant(root: Node3D, p: Vector3):
	rod(root,p+Vector3(0,.17,0),p+Vector3(0,.94,0),.12,metal)
	for y in [.23,.70,.90]:S.cylinder(root,p+Vector3(0,y,0),.17,.055,metal,14)
	var head=SphereMesh.new();head.radius=.17;head.height=.24;head.radial_segments=12;head.rings=6
	S.mesh(root,p+Vector3(0,.94,0),head,metal)
	for x in [-1,1]:
		rod(root,p+Vector3(x*.09,.72,0),p+Vector3(x*.24,.72,0),.080,metal)
		rod(root,p+Vector3(x*.24,.72,0),p+Vector3(x*.275,.72,0),.096,metal)
	S.box(root,p+Vector3(0,1.075,0),Vector3(.065,.075,.065),metal)
	for j in range(8):rod(root,p+Vector3(-.24+j*.065,.57-sin(j/7.0*PI)*.16,.12),p+Vector3(-.20+j*.065,.57-sin((j+.6)/7.0*PI)*.16,.12),.009,metal)

func mailbox(root: Node3D, p: Vector3, blue: Material):
	S.box(root,p+Vector3(0,.68,0),Vector3(.60,.72,.52),blue)
	var hood = CylinderMesh.new();hood.top_radius=.30;hood.bottom_radius=.30;hood.height=.52;hood.radial_segments=20
	var item=S.mesh(root,p+Vector3(0,1.04,0),hood,blue);item.rotation.x=PI/2
	for x in [-.23,.23]:S.box(root,p+Vector3(x,.31,0),Vector3(.065,.32,.40),metal)
	S.box(root,p+Vector3(0,.90,.267),Vector3(.43,.065,.02),soil)
	S.box(root,p+Vector3(0,.78,.283),Vector3(.47,.04,.13),blue)
	S.box(root,p+Vector3(0,.63,.268),Vector3(.28,.19,.009),S.material(Color("d7d8c9")))

func street_lamp(root: Node3D, p: Vector3, bulb: Material):
	rod(root,p+Vector3(0,.15,0),p+Vector3(0,6.35,0),.085,metal,.043)
	S.cylinder(root,p+Vector3(0,.33,0),.18,.36,metal,12)
	rod(root,p+Vector3(0,6.35,0),p+Vector3(.64,6.62,0),.055,metal)
	rod(root,p+Vector3(.64,6.62,0),p+Vector3(1.28,6.45,0),.047,metal)
	S.box(root,p+Vector3(1.25,6.37,0),Vector3(.50,.09,.31),metal)
	S.box(root,p+Vector3(1.25,6.31,0),Vector3(.39,.025,.24),bulb)

func dress(root: Node3D):
	var blue=S.material(Color("3f6478"),.75)
	var bulb=S.material(Color("ffe0ad"),.60,1.0)
	# Recorded as authored placements. Source photographs establish object types,
	# not a present-day municipal furniture inventory or exact tree coordinates.
	for side in [-1,1]:
		var positions=[-197,-156,-124,-89,-58,47,73,110,146,178,253] if side<0 else [-206,-174,-138,-107,-78,-50,60,91,125,159,186,258]
		# April 2026 comparison places the mature church tree beside its right
		# entrance, not across the left double doors. Position/height estimated.
		for x in positions:tree(root,Vector3(x,0,side*7.25),1.0,side>0 and x==-174)
		for x in [-190,-111,-52,64,137,188]:street_lamp(root,Vector3(x,0,side*6.15),bulb)
		for x in [-246,-205,-42,34,177,237]:hydrant(root,Vector3(x,0,side*5.90))
	for p in [Vector3(-214,0,6.2),Vector3(14,0,-6.2),Vector3(201,0,6.0)]:mailbox(root,p,blue)
	# Catch basins, service covers and restrained curb-side litter.
	for side in [-1,1]:
		for x in [-212,-21,20,197,236]:
			var p=Vector3(x,.025,side*4.56)
			S.box(root,p,Vector3(.87,.025,.41),soil)
			for i in range(9):S.box(root,p+Vector3(-.36+i*.09,.018,0),Vector3(.025,.016,.37),metal)
		for x in [-166,-135,-78,79,150]:
			var p=Vector3(x,.151,side*6.3)
			S.box(root,p,Vector3(.72,.012,1.0),metal)
			for i in range(7):S.box(root,p+Vector3(-.27+i*.09,.009,0),Vector3(.012,.008,.87),soil)
