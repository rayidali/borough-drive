extends SceneTree
## Exercise the actual runtime activation path without changing street bounds.
var meshes = 0
var triangles = 0
var texture_checks = 0

func texture_digest(node: Node) -> Dictionary:
	var found: Dictionary = {}
	if node is MeshInstance3D:
		for surface in node.mesh.get_surface_count():
			var material = node.mesh.surface_get_material(surface)
			for slot in BaseMaterial3D.TEXTURE_MAX:
				var texture = material.get_texture(slot)
				if texture:
					var pixels = texture.get_image()
					assert(pixels != null and not pixels.is_empty())
					found[str(surface)+":"+str(slot)] = [pixels.get_width(),pixels.get_height(),pixels.get_format(),pixels.get_mipmap_count(),pixels.get_data().size(),preload("res://scripts/protected_core_textures.gd").digest(pixels.get_data())]
	for child in node.get_children():
		var values = texture_digest(child)
		for key in values: found[str(child.name)+"/"+key] = values[key]
	return found


func check_materials(node: Node):
	if node is MeshInstance3D:
		meshes += 1
		for surface in node.mesh.get_surface_count():
			assert(node.get_surface_override_material(surface)==null,"Protected core material was replaced")
			assert(node.mesh.surface_get_material(surface) is StandardMaterial3D)
			var arrays = node.mesh.surface_get_arrays(surface)
			triangles += arrays[Mesh.ARRAY_INDEX].size()/3 if arrays[Mesh.ARRAY_INDEX]!=null else arrays[Mesh.ARRAY_VERTEX].size()/3
	for child in node.get_children(): check_materials(child)

func _initialize(): call_deferred("run")

func run():
	var args = OS.get_cmdline_user_args()
	assert(args.size()==1)
	var output = args[0]
	DirAccess.make_dir_recursive_absolute(output)
	var packages = preload("res://scripts/protected_core_package.gd").compile(output)
	var metadata = JSON.parse_string(FileAccess.get_file_as_string("res://assets/protected-core.json"))
	var source = load("res://assets/protected-core.glb").instantiate()
	var world = preload("res://scripts/world.gd").new()
	root.add_child(world)
	world.data = {"auxiliaryFootprints":[]}
	var collisions = 0
	var owners: Array = []
	for record in metadata.buildingOwners + metadata.sharedModels:
		var key = str(int(record.id))
		var scene = load(packages[key].path)
		var owner = world.activate_building(record,scene)
		var model = owner.get_node("Building_"+key)
		var original_textures = texture_digest(source.get_node(NodePath(record.group)))
		var loaded_textures = texture_digest(model)
		if original_textures!=loaded_textures:
			print("TEXTURE_DIFF ",JSON.stringify({"source":original_textures,"loaded":loaded_textures}))
		assert(original_textures==loaded_textures,"Bundled textures changed for "+key)
		texture_checks += loaded_textures.size()
		assert(model.position==Vector3(0,0,-228))
		assert(owner.get_meta("model_kind")==record.kind)
		var has_collision = owner.has_node("Collision_"+key)
		assert(has_collision==(record.kind=="protected-core"))
		assert(owner.get_child_count()==(2 if has_collision else 1))
		if has_collision:
			collisions += 1
			assert(owner.get_node("Collision_"+key).get_child_count()==1)
		check_materials(model)
		owners.append({"id":int(record.id),"kind":record.kind,"collider":has_collision,"sceneBytes":packages[key].bytes,"sceneSha256":packages[key].sha256})
	assert(world.resident_owners.size()==24 and collisions==23)
	assert(meshes==521 and triangles==424497)
	var report = {"result":"pass","meshCount":meshes,"triangles":triangles,"buildingOwners":23,"sharedDetailOwners":1,"collisionOwners":collisions,"materialOverrides":0,"textureSlotsByteChecked":texture_checks,"translation":[0,0,-228],"owners":owners,"limits":"Isolated activation/packaging proof; served visual and road integration remain pending."}
	var file = FileAccess.open(output.path_join("ownership-report.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"\t")+"\n")
	print("CORE_OWNERSHIP_PASS ",meshes," meshes, ",collisions," collision owners")
	source.free()
	world.queue_free()
	await process_frame
	quit()
