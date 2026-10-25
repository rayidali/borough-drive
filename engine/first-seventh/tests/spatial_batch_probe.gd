extends SceneTree
func _initialize(): call_deferred("run")
func run():
	var world = preload("res://scripts/world.gd").new()
	root.add_child(world)
	world.data = preload("res://scripts/runtime_catalog.gd").with_protected_core(JSON.parse_string(FileAccess.get_file_as_string("res://assets/slice.json")))
	world.build_streets()
	world.build_props()
	var totals: Dictionary = {}
	for span in [48,128,256,384,512,1000000]:
		var groups: Dictionary = {}
		var keys: Dictionary = {}
		for item in world.geometry.get_children():
			if not item is MeshInstance3D: continue
			var mat = item.material_override
			var id = mat.get_instance_id()
			if not keys.has(id): keys[id] = world.material_key(mat)
			var center = item.transform * item.mesh.get_aabb().get_center()
			var cell = Vector2i(floori(center.x/span),floori(center.z/span)) if span<1000000 else Vector2i.ZERO
			groups[keys[id]+str(cell)] = true
		totals[str(span)] = groups.size()
	print("BATCH_GROUP_COUNTS ",JSON.stringify(totals))
	quit()
