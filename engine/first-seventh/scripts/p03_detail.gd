extends RefCounted
## P03 dated corner street edge. No next-Ninth building or generic prop grid.
const S = preload("res://scripts/shapes.gd")
func label(root: Node3D, text: String, p: Vector3, angle: float, size: int, color):
	var node=Label3D.new();node.text=text;node.position=p;node.rotation.y=angle
	var tint: Color = color.albedo_color if color is BaseMaterial3D else color
	node.font_size=size;node.pixel_size=.0035;node.outline_size=0;node.modulate=tint;root.add_child(node)

func dress(root: Node3D, detail):
	var wood=S.material(Color("82735c"));var iron=S.material(Color("43463d"))
	var silver=S.material(Color("a2a7a1"));var white=S.material(Color("e3e3cf"))
	var green=S.material(Color("218267"));var black=S.material(Color("202a26"))
	var p=Vector3(-21.9,0,-148.2)
	var saved=detail.rng.state;detail.rng.seed=145352
	detail.tree(root,p,.76,false);detail.rng.state=saved
	# Tree bench wraps an open soil pit, with visible boards, legs and wear.
	S.box(root,p+Vector3(0,.155,0),Vector3(1.70,.018,.94),S.material(Color("5a5942")))
	for side in [-1,1]:
		for j in range(3):S.box(root,p+Vector3(0,.47,side*(.53+j*.12)),Vector3(2.12,.055,.109),wood)
		for j in range(2):S.box(root,p+Vector3(side*(.89+j*.12),.47,0),Vector3(.109,.055,1.03),wood)
		for x in [-.84,.84]:S.box(root,p+Vector3(x,.29,side*.63),Vector3(.12,.35,.15),wood)
		S.box(root,p+Vector3(0,.25,side*.69),Vector3(1.86,.11,.05),wood)
	# Ninth curb drain; long axis along the curb, not a sidewalk decoration.
	p=Vector3(-18.7,.025,-149.60)
	S.box(root,p,Vector3(1.05,.032,.57),black)
	for j in range(12):S.box(root,p+Vector3(-.49+j*.088,.024,0),Vector3(.024,.031,.54),iron)
	for z in [-.27,.27]:S.box(root,p+Vector3(0,.025,z),Vector3(1.07,.03,.035),silver)
	# Small First Avenue inverted-U rack beside Baji's display.
	p=Vector3(-12.05,0,-138.30)
	for dz in [-.32,.32]:detail.rod(root,p+Vector3(0,.14,dz),p+Vector3(0,.78,dz),.035,iron)
	detail.rod(root,p+Vector3(0,.78,-.32),p+Vector3(0,.78,.32),.035,iron)
	# Observed southwest signal pole and mast; one owned corner fixture only.
	p=Vector3(-11.65,0,-144.20)
	S.box(root,p+Vector3(0,.23,0),Vector3(.43,.45,.43),silver)
	S.cylinder(root,p+Vector3(0,3.63,0),.086,6.95,silver,16)
	for yy in [.62,2.22,4.18]:S.box(root,p+Vector3(.097,yy,0),Vector3(.024,.11,.16),white)
	detail.rod(root,p+Vector3(0,6.31,0),p+Vector3(7.15,7.06,0),.043,silver)
	detail.rod(root,p+Vector3(0,5.93,0),p+Vector3(7.15,7.06,0),.036,silver)
	S.box(root,p+Vector3(4.7,6.49,0),Vector3(2.08,.47,.04),green)
	label(root,"1 AV",p+Vector3(4.7,6.49,.032),0,61,white)
	label(root,"1 AV",p+Vector3(4.7,6.49,-.032),PI,61,white)
	S.box(root,p+Vector3(.19,3.84,0),Vector3(.04,.30,.99),white)
	label(root,"ONE WAY →",p+Vector3(.217,3.84,0),PI/2,29,black)
	var yellow=S.material(Color("bd952f"))
	S.box(root,p+Vector3(.23,2.82,0),Vector3(.28,.61,.54),yellow)
	S.box(root,p+Vector3(.382,2.82,0),Vector3(.025,.50,.44),black)
	var hand=S.material(Color("ca7441"))
	S.box(root,p+Vector3(.402,2.80,0),Vector3(.012,.16,.18),hand)
	for j in range(4):S.box(root,p+Vector3(.402,2.94,-.071+j*.047),Vector3(.012,.18,.026),hand)
	# Tactile pads at the two curb ramps. Their observed reddish tone stays local.
	var pad=S.material(Color("b88670"))
	for item in [[Vector3(-10.28,.156,-143.55),Vector3(.75,.023,1.1)],[Vector3(-13.02,.156,-149.43),Vector3(1.13,.023,.66)]]:
		S.box(root,item[0],item[1],pad)
		for x in range(6):
			for z in range(5):S.cylinder(root,item[0]+Vector3((x-2.5)*item[1].x/7,.018,(z-2)*item[1].z/6),.015,.013,pad,6)
	# Short barrier/bicycle rail at the pizza service wall, leaving 352's path clear.
	for x in [-26.25,-29.0,-31.45]:
		for dx in [-1.25,1.25]:detail.rod(root,Vector3(x+dx,.17,-145.20),Vector3(x+dx,.92,-145.20),.02,iron)
		for yy in [.31,.86]:detail.rod(root,Vector3(x-1.25,yy,-145.20),Vector3(x+1.25,yy,-145.20),.017,iron)
		for j in range(12):detail.rod(root,Vector3(x-1.15+j*.21,.25,-145.20),Vector3(x-1.15+j*.21,.86,-145.20),.009,iron)
