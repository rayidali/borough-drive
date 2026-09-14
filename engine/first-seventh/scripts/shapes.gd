extends RefCounted

static func material(color: Color, roughness: float = 0.8, emission: float = 0.0) -> StandardMaterial3D:
	var m = StandardMaterial3D.new()
	m.albedo_color = color
	m.roughness = roughness
	if emission > 0:
		m.emission_enabled = true
		m.emission = color
		m.emission_energy_multiplier = emission
	return m

static func box(parent: Node3D, p: Vector3, size: Vector3, mat: Material) -> MeshInstance3D:
	var m = BoxMesh.new()
	m.size = size
	return mesh(parent,p,m,mat)

static func mesh(parent: Node3D, p: Vector3, shape: Mesh, mat: Material) -> MeshInstance3D:
	var item = MeshInstance3D.new()
	item.mesh = shape
	item.material_override = mat
	item.position = p
	parent.add_child(item)
	return item

static func cylinder(parent: Node3D, p: Vector3, radius: float, height: float, mat: Material, sides: int = 10) -> MeshInstance3D:
	var m = CylinderMesh.new()
	m.top_radius = radius
	m.bottom_radius = radius
	m.height = height
	m.radial_segments = sides
	return mesh(parent,p,m,mat)

static func solid_box(parent: Node3D, p: Vector3, size: Vector3, mat: Material) -> StaticBody3D:
	var body = StaticBody3D.new()
	body.position = p
	parent.add_child(body)
	var collider = CollisionShape3D.new()
	var shape = BoxShape3D.new()
	shape.size = size
	collider.shape = shape
	body.add_child(collider)
	if mat: box(body,Vector3.ZERO,size,mat)
	return body

static func rings(parent: Node3D, profiles: Array, mat: Material) -> MeshInstance3D:
	# Hand-authored beveled car panels: [z, width, lower height, upper height].
	var st = SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var vertices: Array[Vector3] = []
	for r in profiles:
		vertices.append_array([Vector3(-r[1]*.5,r[2],r[0]),Vector3(r[1]*.5,r[2],r[0]),Vector3(r[1]*.5,r[3]-.08,r[0]),Vector3(r[1]*.42,r[3],r[0]),Vector3(-r[1]*.42,r[3],r[0]),Vector3(-r[1]*.5,r[3]-.08,r[0])])
	for row in range(profiles.size()-1):
		for col in range(6):
			var a=row*6+col
			var b=row*6+(col+1)%6
			for i in [a,b+6,b,a,a+6,b+6]: st.add_vertex(vertices[i])
	for end in [0,profiles.size()-1]:
		for col in range(1,5):
			var indices=[end*6,end*6+col,end*6+col+1]
			if end!=0: indices.reverse()
			for i in indices: st.add_vertex(vertices[i])
	st.generate_normals()
	return mesh(parent,Vector3.ZERO,st.commit(),mat)
