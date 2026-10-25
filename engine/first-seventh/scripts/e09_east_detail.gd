extends RefCounted
## Dated Ninth east-block curb trees / fittings. Dimensions and positions are visual estimates.
const S = preload("res://scripts/shapes.gd")
func dress(root: Node3D, detail):
	var saved = detail.rng.state
	var soil = S.material(Color("57543c"))
	var joint = S.material(Color("989587"))
	var iron = S.material(Color("4b5250"))
	# Irregular observed trees; no per-property cadence.
	for row in [[39.0,-160.2,.72,122],[78.5,-160.3,.60,415],[100.5,-160.1,.64,421],[136.3,-160.0,.52,431],[170.5,-160.0,.64,441],[193.0,-160.1,.54,445],[51.8,-147.5,.62,406],[85.5,-147.4,.60,416],[107.5,-147.4,.63,422],[142.6,-147.4,.56,430],[164.6,-147.5,.50,436],[180.5,-147.4,.54,440]]:
		var p = Vector3(row[0],0,row[1])
		detail.rng.seed = int(row[3])
		detail.tree(root,p,row[2],false)
		S.box(root,p+Vector3(0,.153,0),Vector3(1.10,.012,.95),soil)
		for x in [-.60,.60]: S.box(root,p+Vector3(x,.19,0),Vector3(.08,.08,1.10),joint)
	detail.rng.state=saved
	for x in range(20,203,3):
		for z in [-161.1,-146.2]:S.box(root,Vector3(x,.146,z),Vector3(.022,.008,2.65),joint)
	for x in [64.0,112.0,178.0]:
		S.cylinder(root,Vector3(x,.014,-154.1),.40,.018,iron,24)
		for j in range(-2,3): S.box(root,Vector3(x,.028,-154.1+j*.11),Vector3(.56,.009,.018),joint)
	# Curb regulation poles / corner hydrant, separate from building-owned signs.
	var silver=S.material(Color("8d918a"))
	var white=S.material(Color("d4d0ba"))
	var red=S.material(Color("8e3930"))
	for x in [20.0,74.0,130.0,190.5]:
		S.cylinder(root,Vector3(x,1.78,-148.4),.028,3.3,silver,8)
		S.box(root,Vector3(x,2.72,-148.42),Vector3(.28,.40,.025),white)
		for y in [2.58,2.73,2.85]:S.box(root,Vector3(x,y,-148.44),Vector3(.22,.02,.008),red)
	S.cylinder(root,Vector3(200.5,.55,-148.2),.13,.80,iron,12)
	S.cylinder(root,Vector3(200.5,.97,-148.2),.18,.13,iron,12)
