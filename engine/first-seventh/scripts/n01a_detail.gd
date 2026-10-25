extends RefCounted
## Dated north Ninth fixture observations, confined to N01A.
const S = preload("res://scripts/shapes.gd")
func dress(root: Node3D, detail):
	var silver=S.material(Color("979b91"));var blue=S.material(Color("285795"));var white=S.material(Color("e1e2cf"));var black=S.material(Color("363d36"))
	var p=Vector3(-39.1,0,-160.18)
	S.cylinder(root,p+Vector3(0,2.09,0),.038,3.90,silver,12)
	S.box(root,p+Vector3(0,3.24,0),Vector3(.41,.69,.037),white)
	for y in [3.11,3.29,3.49]:S.box(root,p+Vector3(0,y,.025),Vector3(.35,.085,.013),blue)
	preload("res://scripts/p03_detail.gd").new().label(root,"M8",p+Vector3(0,3.80,.035),0,62,blue)
	S.box(root,p+Vector3(0,3.80,0),Vector3(.41,.30,.04),white)
	p=Vector3(-46.0,0,-160.10)
	var saved=detail.rng.state;detail.rng.seed=345343
	detail.tree(root,p,.58,false);detail.rng.state=saved
	S.box(root,p+Vector3(0,.153,0),Vector3(1.04,.012,.84),S.material(Color("57543c")))
	for x in [-.56,.56]:S.box(root,p+Vector3(x,.20,0),Vector3(.06,.11,.95),black)
	for z in [-.48,.48]:S.box(root,p+Vector3(0,.20,z),Vector3(1.15,.11,.06),black)
	# Small corner hydrant visible in May 2024, placed at the curb rather than the door.
	p=Vector3(-17.2,0,-160.10)
	S.cylinder(root,p+Vector3(0,.47,0),.105,.63,black,12)
	S.cylinder(root,p+Vector3(0,.82,0),.145,.10,silver,12)
	S.box(root,p+Vector3(0,.60,0),Vector3(.37,.14,.16),black)
