extends RefCounted
## Dated Ninth curb trees and paving; positions are visual estimates.
const S = preload("res://scripts/shapes.gd")
func dress(root: Node3D, detail):
	var saved = detail.rng.state
	var soil = S.material(Color("57543c"))
	var joint = S.material(Color("989587"))
	for row in [[-124.0,-160.1,.67,321],[-143.2,-160.1,.76,317],[-153.3,-160.1,.56,313],[-187.5,-160.1,.74,305],[-64.2,-147.4,.62,344],[-109.7,-147.5,.52,332],[-168.6,-147.4,.70,310],[-179.2,-147.4,.58,308],[-199.8,-147.5,.62,300],[-209.0,-147.5,.48,298]]:
		var p = Vector3(row[0],0,row[1])
		detail.rng.seed = int(row[3])
		detail.tree(root,p,row[2],false)
		S.box(root,p+Vector3(0,.153,0),Vector3(1.03,.012,.95),soil)
		for x in [-.57,.57]: S.box(root,p+Vector3(x,.19,0),Vector3(.08,.08,1.10),joint)
	detail.rng.state = saved
	for x in range(-98,-214,-3):
		S.box(root,Vector3(x,.146,-161.2),Vector3(.022,.008,2.75),joint)
	for x in range(-38,-214,-3):
		S.box(root,Vector3(x,.146,-146.1),Vector3(.022,.008,2.65),joint)
	var iron = S.material(Color("4b5250"))
	for x in [-115.0,-153.0,-194.0]:
		S.cylinder(root,Vector3(x,.014,-154.2),.40,.018,iron,24)
		for j in range(-2,3): S.box(root,Vector3(x,.028,-154.2+j*.11),Vector3(.56,.009,.018),joint)
