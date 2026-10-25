extends RefCounted
## April 2026 street-edge observation; dimensions/positions estimated from facade anchors.
const S = preload("res://scripts/shapes.gd")
func dress(root: Node3D, detail):
	var saved=detail.rng.state
	detail.rng.seed=138148
	var iron=S.material(Color("3a4037"))
	# Tree locations are independently observed, not a repeated spacing preset.
	detail.tree(root,Vector3(12.0,0,-123.6),.62,true)
	detail.tree(root,Vector3(12.1,0,-137.5),1.03,false)
	detail.rng.state=saved
	# Rectangular open guard surrounding the southern tree.
	var p=Vector3(12.0,0,-123.6)
	for side in [-1,1]:
		for j in range(9):
			var t=-.76+j*.19
			for pair in [[Vector3(side*.70,.16,t),Vector3(side*.70,.91,t)],[Vector3(t*.92,.16,side*.76),Vector3(t*.92,.91,side*.76)]]:
				detail.rod(root,p+pair[0],p+pair[1],.012,iron)
		for y in [.37,.80]:
			detail.rod(root,p+Vector3(side*.70,y,-.76),p+Vector3(side*.70,y,.76),.017,iron)
			detail.rod(root,p+Vector3(-.70,y,side*.76),p+Vector3(.70,y,side*.76),.017,iron)
	# Green bus pole and the observed stacked blue/white signs.
	p=Vector3(12.15,0,-131.0)
	var green=S.material(Color("30614c"))
	var blue=S.material(Color("2a5998"))
	var white=S.material(Color("dfdfcd"))
	S.cylinder(root,p+Vector3(0,2.03,0),.041,4.06,green)
	S.box(root,p+Vector3(-.06,3.24,0),Vector3(.035,.78,.56),white)
	S.box(root,p+Vector3(-.083,3.50,0),Vector3(.023,.20,.56),blue)
	var disk=S.cylinder(root,p+Vector3(-.065,3.96,0),.29,.035,blue,32)
	disk.rotation.z=PI/2
	var ring=S.cylinder(root,p+Vector3(-.055,3.96,0),.315,.027,white,32)
	ring.rotation.z=PI/2
	for item in [["M15",Vector3(-.10,3.50,-.13),26],["East Harlem",Vector3(-.10,3.50,.11),12]]:
		var label=Label3D.new();label.text=item[0];label.font_size=item[2];label.pixel_size=.0035
		label.outline_size=0;label.modulate=Color("f6f1da");label.position=p+item[1];label.rotation.y=-PI/2;root.add_child(label)
	# Observed bus pictogram; no invented BUS STOP wording on the blue disk.
	S.box(root,p+Vector3(-.091,3.98,0),Vector3(.018,.27,.27),white)
	S.box(root,p+Vector3(-.106,4.045,0),Vector3(.012,.11,.21),blue)
	for z in [-.092,.092]:
		S.box(root,p+Vector3(-.11,3.89,z),Vector3(.013,.035,.033),blue)
		S.box(root,p+Vector3(-.09,3.815,z),Vector3(.018,.060,.042),white)
	for y in [3.30,3.18,3.06]:S.box(root,p+Vector3(-.10,y,0),Vector3(.014,.010,.35),green)
	# Short dark utility cylinder with layered notice rectangles, north of bus pole.
	p=Vector3(12.3,0,-133.4)
	S.cylinder(root,p+Vector3(0,.83,0),.16,1.4,iron)
	for i in range(7):S.box(root,p+Vector3(-.155,.31+i*.17,0),Vector3(.016,.105,.16 if i%2 else .21),white if i%2 else blue)
