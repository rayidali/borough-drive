extends RefCounted
const S = preload("res://scripts/shapes.gd")

# Dated Street View observations and mapped anchors, not surveyed positions.
# Source pixels are not embedded: painted panels are authored mesh strokes.
func dress(root: Node3D, detail):
	var iron=S.material(Color("303b38"))
	var gray=S.material(Color("8c9691"))
	var blue=S.material(Color("3476ad"))
	var ochre=S.material(Color("dc9b39"))
	var brown=S.material(Color("813d28"))
	var white=S.material(Color("d7d9c7"))
	var site=Node3D.new()
	site.name="ObservedStMarksPaintedGap_September2024"
	root.add_child(site)
	# South-side gap: viewer's left is east (larger mapped X).
	S.box(site,Vector3(99.99,1.77,-68.70),Vector3(2.94,3.22,.20),blue)
	S.box(site,Vector3(96.48,1.71,-68.70),Vector3(4.03,3.10,.20),iron)
	S.box(site,Vector3(93.96,1.68,-68.70),Vector3(.93,3.04,.20),iron)
	for j in range(35):S.box(site,Vector3(96.48,.22+j*.084,-68.81),Vector3(4.0,.016,.012),gray)
	label(site,Vector3(96.6,2.48,-68.85),"PUNK IS NOT",.006,white,PI)
	label(site,Vector3(96.3,1.91,-68.85),"DEAD",.007,white,PI)
	# Giraffe's four long legs, body, neck and looping antlers/neck motif.
	S.box(site,Vector3(100.05,.88,-68.83),Vector3(.70,.60,.015),ochre)
	for x in [99.77,99.96,100.16,100.32]:stroke(site,Vector3(x,.20,-68.85),Vector3(x+.02,.88,-68.85),.035,ochre)
	stroke(site,Vector3(100.31,1.04,-68.85),Vector3(100.40,1.62,-68.85),.052,ochre)
	for offset in [-.54,.05,.61]:
		for j in range(22):
			var a=j*TAU/22.0;var b=(j+1)*TAU/22.0
			stroke(site,Vector3(100.04+offset+cos(a)*.40,1.9+sin(a)*.43,-68.85),Vector3(100.04+offset+cos(b)*.40,1.9+sin(b)*.43,-68.85),.026,ochre)
	stroke(site,Vector3(100.40,2.2,-68.85),Vector3(100.28,3.23,-68.85),.028,ochre)
	for j in range(9):S.box(site,Vector3(99.82+(j%3)*.19,.72+floor(j/3.0)*.17,-68.862),Vector3(.11,.10,.006),brown)
	var green=S.material(Color("6ba341"));var pink=S.material(Color("b7558a"))
	for j in range(7):
		var mat=green if j%2 else pink
		stroke(site,Vector3(93.64+j*.09,.3,-68.84),Vector3(94.17-j*.06,1.58+j*.15,-68.84),.053,mat)
	S.box(site,Vector3(93.95,1.88,-68.85),Vector3(.74,.34,.016),blue)
	S.box(site,Vector3(93.98,1.55,-68.86),Vector3(.69,.18,.016),ochre)
	S.solid_box(site,Vector3(97.474,1.7,-68.7),Vector3(7.97,3.2,.23),null)
	# Observed curb trees. Their anchors, pit dimensions and crowns remain
	# estimated; no unseen street furniture is inferred between these points.
	var saved=detail.rng.state
	detail.rng.seed=10808
	for p in [Vector3(-204,0,-71.2),Vector3(-178,0,-85.3),Vector3(-155,0,-71.2),Vector3(-132,0,-85.3),Vector3(-107,0,-71.2),Vector3(-99,0,-85.3),Vector3(-55,0,-71.2),Vector3(-28,0,-85.3),Vector3(47,0,-71.2),Vector3(56,0,-85.3),Vector3(121,0,-71.2),Vector3(152,0,-85.3),Vector3(182,0,-71.2)]:
		detail.tree(root,p,.82,true)
		for side in [-1,1]:
			for j in range(8):S.box(root,p+Vector3(side*1.0,.43,-.68+j*.195),Vector3(.022,.57,.022),iron)
			S.box(root,p+Vector3(side*1.0,.72,0),Vector3(.035,.035,1.45),iron)
	detail.rng.state=saved
	for p in [Vector3(-216.1,0,-84.8),Vector3(201.7,0,-71.0)]:
		S.box(root,p+Vector3(.9,.62,.15),Vector3(.53,1.12,.44),gray)
		for j in range(4):S.box(root,p+Vector3(.79+(j%2)*.17,.43+floor(j/2.0)*.20,-.078),Vector3(.12,.13,.014),white)
		S.cylinder(root,p+Vector3(-.8,.43,0),.29,.80,iron,12)
		for j in range(12):
			var a=j*TAU/12;S.box(root,p+Vector3(-.8+cos(a)*.294,.45,sin(a)*.294),Vector3(.025,.68,.025),gray)
		label(root,p+Vector3(0,4.30,0),"ST MARKS PL",.004,white,0)
	var hp=Vector3(201.2,0,-73.4)
	S.cylinder(root,hp+Vector3(0,.46,0),.14,.73,iron)
	S.cylinder(root,hp+Vector3(0,.86,0),.19,.13,iron)
	S.box(root,hp+Vector3(0,.61,0),Vector3(.55,.18,.18),iron)
	for x in [-.62,.62]:S.cylinder(root,hp+Vector3(x,.38,0),.055,.76,iron)
	# Site meshes join the existing static batches; the collision stays named.
	for child in site.get_children():
		if child is MeshInstance3D:child.reparent(root,false)

func stroke(parent: Node3D,a: Vector3,b: Vector3,radius: float,mat: Material):
	var mesh=S.cylinder(parent,(a+b)*.5,radius,a.distance_to(b),mat,6)
	mesh.quaternion=Quaternion(Vector3.UP,(b-a).normalized())

func label(parent: Node3D,p: Vector3,text: String,size: float,mat: Material,angle: float):
	var mesh=TextMesh.new()
	mesh.text=text
	mesh.font_size=48
	mesh.pixel_size=size
	mesh.depth=.002
	S.mesh(parent,p,mesh,mat).rotation.y=angle
