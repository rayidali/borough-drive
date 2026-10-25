extends SceneTree
## Native read-only design probe. Run in an empty temporary project, not the game.
## Args: absolute PCK, census JSON, output JSON, temporary loose-file directory.

func signature(scene: PackedScene) -> Dictionary:
	var root = scene.instantiate()
	var pending = [root]
	var meshes = []
	var node_count = 0
	while not pending.is_empty():
		var node = pending.pop_back()
		node_count += 1
		for child in node.get_children(): pending.append(child)
		if node is MeshInstance3D:
			var surfaces = []
			for index in node.mesh.get_surface_count():
				var mat = node.mesh.surface_get_material(index)
				var stored = node.mesh.get("_surfaces")[index]
				surfaces.append({"arraysSha256":var_to_bytes(node.mesh.surface_get_arrays(index)).hex_encode().sha256_text(),"lodSha256":var_to_bytes(stored.get("lods",[])).hex_encode().sha256_text(),"lodCount":stored.get("lods",[]).size(),"materialName":mat.resource_name if mat else "","format":node.mesh.surface_get_format(index)})
			meshes.append({"name":str(root.get_path_to(node)),"transform":str(node.transform),"aabb":str(node.mesh.get_aabb()),"surfaces":surfaces,"shadowMeshPresent":node.mesh.shadow_mesh != null if node.mesh is ArrayMesh else false})
	root.free()
	return {"nodeCount":node_count,"meshes":meshes}

func _init():
	var args = OS.get_cmdline_user_args()
	if args.size() != 4:
		push_error("Expected PCK, census JSON, output JSON and scratch directory")
		quit(2)
		return
	var mounted = ProjectSettings.load_resource_pack(args[0],false)
	if not mounted:
		quit(3)
		return
	var census = JSON.parse_string(FileAccess.get_file_as_string(args[1]))
	var rows = []
	var samples = []
	var sample_ids = [248142404,241822151,248142407]
	DirAccess.make_dir_recursive_absolute(args[3])
	for e in census.entries:
		if not e.has("buildingId"): continue
		var source = "res://"+e.path
		var deps = ResourceLoader.get_dependencies(source)
		rows.append({"buildingId":e.buildingId,"resourcePath":source,"dependencies":Array(deps)})
		if not int(e.buildingId) in sample_ids: continue
		var bytes = FileAccess.get_file_as_bytes(source)
		var loose = args[3].path_join(str(int(e.buildingId))+".scn")
		var file = FileAccess.open(loose,FileAccess.WRITE)
		file.store_buffer(bytes)
		file.close()
		assert(FileAccess.get_sha256(loose) == e.sha256)
		var original = ResourceLoader.load(source,"PackedScene",ResourceLoader.CACHE_MODE_IGNORE_DEEP)
		var relocated = ResourceLoader.load(loose,"PackedScene",ResourceLoader.CACHE_MODE_IGNORE_DEEP)
		var a = signature(original)
		var b = signature(relocated)
		assert(not a.is_empty() and not b.is_empty() and not a.meshes.is_empty())
		var weak = weakref(relocated)
		var same = a == b
		assert(same)
		original = null
		relocated = null
		var released = weak.get_ref() == null
		DirAccess.remove_absolute(loose)
		samples.append({"buildingId":e.buildingId,"looseFileLoadsAsPackedScene":true,"dependencies":Array(deps),"sameNodeMeshArrayLodMaterialSignature":same,"packedSceneReleasedAfterDroppingRefs":released,"signature":a})
	var pack_methods = []
	for method in ProjectSettings.get_method_list():
		if "pack" in str(method.name): pack_methods.append(str(method.name))
	var result = {"engine":Engine.get_version_info(),"platform":OS.get_name(),"mode":"native headless resource inspection only; no HTTP/WebGL/browser or streaming implementation", "projectSettingsPackMethods":pack_methods,"dependencies":rows,"samples":samples}
	var output = FileAccess.open(args[2],FileAccess.WRITE)
	output.store_string(JSON.stringify(result,"\t")+"\n")
	output.close()
	print("EV001_RESOURCE_PROBE ",rows.size()," dependency records; ",samples.size()," relocated native samples")
	quit(0)
