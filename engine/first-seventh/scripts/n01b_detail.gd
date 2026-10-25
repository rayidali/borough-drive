extends RefCounted
## Only the observed N01B curb trees and pavement details.
const S=preload("res://scripts/shapes.gd")
func dress(root: Node3D,detail):
	var saved=detail.rng.state
	for row in [[-75.4,.78,335337],[-90.0,.30,333]]:
		var p=Vector3(row[0],0,-160.1)
		detail.rng.seed=int(row[2]);detail.tree(root,p,row[1],int(row[2])==335337)
		S.box(root,p+Vector3(0,.153,0),Vector3(1.03,.012,.95),S.material(Color("57543c")))
		for x in [-.57,.57]:S.box(root,p+Vector3(x,.19,0),Vector3(.08,.08,1.10),S.material(Color("989587")))
	detail.rng.state=saved
	var joint=S.material(Color("989587"))
	for x in [-65.0,-68.0,-71.0,-74.0,-77.0,-80.0,-83.0,-86.0,-89.0,-92.0,-95.0]:
		S.box(root,Vector3(x,.146,-161.2),Vector3(.022,.008,2.75),joint)
	# Visible paired cellar plates near the cleaner/salon seam.
	var plate=S.material(Color("3d433e"))
	for x in [-75.8,-76.5]:
		S.box(root,Vector3(x,.16,-161.2),Vector3(.66,.03,.90),plate)
		S.box(root,Vector3(x,.181,-161.2),Vector3(.02,.009,.87),joint)
