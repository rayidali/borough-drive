extends RefCounted
const S = preload("res://scripts/shapes.gd")

# April 2026 browser observation, inspected September 23. This is the visible
# 108 street edge, not a measured reconstruction of the hidden rear building.
# See model-source/east-seventh-browser-07.json for source URLs and limits.
func dress(root: Node3D, detail):
	var iron = S.material(Color("303a34"),.82)
	var paving = S.material(Color("8a8980"),.98)
	var green = S.material(Color("537052"),.95)
	var paper = S.material(Color("d6d0be"),.92)
	var red = S.material(Color("9c5140"),.89)
	var site = Node3D.new()
	site.name = "Observed108StreetEdge_April2026"
	root.add_child(site)
	S.box(site,Vector3(99.96,.12,12.7),Vector3(7.22,.08,6.6),paving)
	# Two broad gates and the narrower pedestrian leaf beside 110.
	for x in [96.35,99.27,102.09,103.54]:
		S.box(site,Vector3(x,1.51,9.48),Vector3(.075,2.72,.08),iron)
	for y in [.24,1.32,1.70,2.72]:
		S.box(site,Vector3(99.96,y,9.48),Vector3(7.20,.045,.045),iron)
	for j in range(61):
		var x=96.36+j*7.18/60.0
		S.box(site,Vector3(x,1.47,9.48),Vector3(.021,2.45,.025),iron)
	for x in [97.81,100.68]:
		S.box(site,Vector3(x,1.22,9.47),Vector3(2.79,.41,.06),iron)
		S.box(site,Vector3(x,1.97,9.415),Vector3(.31,.46,.015),paper)
		for y in [1.86,1.96,2.06]:S.box(site,Vector3(x,y,9.403),Vector3(.24,.021,.005),red)
	# The fine notices are not legible enough to invent wording.
	S.box(site,Vector3(102.78,2.09,9.415),Vector3(.73,1.10,.018),paper)
	S.solid_box(site,Vector3(99.96,1.4,9.48),Vector3(7.20,2.8,.13),null)
	for x in [96.48,103.37]:
		S.box(site,Vector3(x,.28,11.15),Vector3(.34,.22,3.4),paving)
		var st=SurfaceTool.new()
		st.begin(Mesh.PRIMITIVE_TRIANGLES)
		for j in range(100):
			var center=Vector3(x,.40+(j%13)*.19,9.55+floor(j/13.0)*.40)
			var a=Vector3(.10,.13,.015)
			var b=Vector3(-.035,.02,.13)
			for v in [center-a,center+b,center+a,center-a,center-b,center+b]:st.add_vertex(v)
		st.generate_normals()
		S.mesh(site,Vector3.ZERO,st.commit(),green)
	var saved_seed=detail.rng.state
	detail.rng.seed=10807
	for x in [97.8,101.65]:detail.tree(site,Vector3(x,0,12.4),.63,false)
	detail.rng.state=saved_seed
	# world.batch_details() visits direct children only. The site transform is
	# identity, so moving its static meshes preserves every vertex/material
	# while including the gate and planting in the existing shared batches.
	# The gate's collision body stays grouped under the named site node.
	for item in site.get_children():
		if item is MeshInstance3D:item.reparent(root,false)
