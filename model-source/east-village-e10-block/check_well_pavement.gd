extends SceneTree
func _initialize():call_deferred("run")
func run():
	var world=load("res://scripts/world.gd").new()
	root.add_child(world)
	world.data=JSON.parse_string(FileAccess.get_file_as_string("res://assets/slice.json"))
	world.build_streets()
	var hits=[]
	for well in world.data.groundVoids:
		if int(well.get("buildingId",0)) not in [247851901,247852662,247852668]:continue
		for depth in [.1,.3,.5,.7,.9]:
			var p=Vector3(well.runtimeCenter[0]+well.runtimeNormal[0]*depth,0,well.runtimeCenter[1]+well.runtimeNormal[1]*depth)
			for mesh in world.geometry.get_children():
				if not mesh is MeshInstance3D or not mesh.mesh is BoxMesh:continue
				var box=mesh.global_transform*mesh.get_aabb()
				if p.x>box.position.x and p.x<box.end.x and p.z>box.position.z and p.z<box.end.z and box.end.y>-.1 and box.end.y<.3:hits.append({"well":well.faceId,"depth":depth,"box":[box.position,box.end]})
	print("WELL_CAPS ",JSON.stringify(hits))
	quit(0 if hits.is_empty() else 1)
