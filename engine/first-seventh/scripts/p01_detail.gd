extends RefCounted
## P01 street edge only. April 2026 sources and position estimates are in its ledger.
const S = preload("res://scripts/shapes.gd")

func dress(root: Node3D, detail):
	var saved=detail.rng.state
	detail.rng.seed=137143
	# The south tree is sparse in the source; its twig crown differs from the
	# leafy Kikoo tree. Both use authored geometry, not source imagery.
	var bark=S.material(Color("514b39"))
	var iron=S.material(Color("343d39"))
	for record in [[-107.7,9.8],[-135.7,10.3]]:
		var p=Vector3(-12.15,0,float(record[0]))
		var h=float(record[1])
		detail.rod(root,p+Vector3(0,.15,0),p+Vector3(.12,h*.50,0),.18,bark,.075)
		for j in range(8):
			var angle=j*TAU/8.0
			var tip=p+Vector3(cos(angle)*2.15,h*(.72+float(j%3)*.10),sin(angle)*2.0)
			detail.rod(root,p+Vector3(.12,h*.48,0),tip,.055,bark,.013)
			for k in [-1,1]:detail.rod(root,tip-Vector3(0,.8,0),tip+Vector3(k*.50,.55,k*.38),.015,bark,.004)
		S.box(root,p+Vector3(0,.15,0),Vector3(1.45,.018,1.65),detail.soil)
	detail.tree(root,Vector3(-12.1,0,-125.9),.69,true)
	detail.rng.state=saved
	# The signed streetlight between the burger shop and blue facade.
	var p=Vector3(-12.0,0,-114.9)
	var gray=S.material(Color("959d97"))
	var yellow=S.material(Color("ced342"))
	S.cylinder(root,p+Vector3(0,3.80,0),.062,7.6,gray)
	S.box(root,p+Vector3(.35,7.53,0),Vector3(.84,.07,.07),gray)
	S.box(root,p+Vector3(.68,7.48,0),Vector3(.33,.085,.19),iron)
	S.box(root,p+Vector3(.08,3.75,0),Vector3(.035,.57,.47),yellow)
	S.box(root,p+Vector3(.09,3.28,0),Vector3(.036,.26,.47),yellow)
	S.box(root,p+Vector3(.10,2.76,0),Vector3(.035,.58,.35),S.material(Color("dddcd0")))
	var text=Label3D.new()
	text.text="SCHOOL"
	text.font_size=28
	text.pixel_size=.0025
	text.outline_size=0
	text.modulate=Color("28322b")
	text.rotation.y=PI/2
	text.position=p+Vector3(.123,3.28,0)
	root.add_child(text)
	# A single observed inverted-U rack beside Paquitos, clear of the drive lane.
	var rack=Vector3(-12.0,0,-131.1)
	for z in [-.30,.30]:detail.rod(root,rack+Vector3(0,.16,z),rack+Vector3(0,.78,z),.025,iron)
	for j in range(12):
		var a=j*PI/12;var b=(j+1)*PI/12
		detail.rod(root,rack+Vector3(0,.78+sin(a)*.30,cos(a)*.30),rack+Vector3(0,.78+sin(b)*.30,cos(b)*.30),.025,iron)
