extends SceneTree
## Compile-time packaging only. Copies existing imported bytes; never reauthors meshes.
const WEST = [241833259,241833267,241833274,241833286,241833290,241833291,241833299,241833312,241833322,241845001,241845013,978475216]

func visual_bounds(node: Node, parent_transform: Transform3D, result: Array):
	var transform = parent_transform
	if node is Node3D: transform = parent_transform * node.transform
	if node is MeshInstance3D:
		var bounds: AABB = transform * node.mesh.get_aabb()
		if result.is_empty(): result.append(bounds)
		else: result[0] = result[0].merge(bounds)
	for child in node.get_children(): visual_bounds(child,transform,result)

func _initialize():
	var args = OS.get_cmdline_user_args()
	assert(args.size()==1,"Expected absolute export stage")
	var stage = args[0]
	assert(Engine.get_version_info().string.begins_with("4.7.2"),"Preserve reviewed import engine")
	var data = preload("res://scripts/runtime_catalog.gd").with_protected_core(JSON.parse_string(FileAccess.get_file_as_string("res://assets/slice.json")))
	var manifest = {"schema":1,"engine":"4.7.2","originShift":data.originShift,"assets":{},"areas":{"EVP-WEST":[],"EVP-REST":[]}}
	DirAccess.make_dir_recursive_absolute(stage.path_join("areas/assets"))
	var core_packages = preload("res://scripts/protected_core_package.gd").compile(stage)
	var entries: Array = data.buildings + data.sharedModels
	for b in entries:
		var key = str(int(b.id))
		var source: String
		if core_packages.has(key):
			source = core_packages[key].path
		else:
			var imported = ConfigFile.new()
			assert(imported.load(b.asset+".import")==OK)
			source = imported.get_value("remap","path")
		assert(ResourceLoader.get_dependencies(source).is_empty(),"External scene dependency requires explicit packaging")
		var bytes = FileAccess.get_file_as_bytes(source)
		var scene_limit = 16*1024*1024 if int(b.id) in [247852693,248142953] else 8*1024*1024
		assert(bytes.size()>0 and bytes.size()<=scene_limit,"Scene byte bound: "+key+" = "+str(bytes.size()))
		var hash = FileAccess.get_sha256(source)
		var relative = "areas/assets/"+hash+".scn"
		var file = FileAccess.open(stage.path_join(relative),FileAccess.WRITE)
		assert(file!=null)
		file.store_buffer(bytes)
		file.close()
		var scene = ResourceLoader.load(source,"PackedScene",ResourceLoader.CACHE_MODE_IGNORE_DEEP)
		assert(scene is PackedScene)
		var model = scene.instantiate()
		model.position = Vector3(b.position[0],0,b.position[2])
		var found: Array = []
		visual_bounds(model,Transform3D.IDENTITY,found)
		assert(found.size()==1)
		var bounds: AABB = found[0]
		var owner = "EVP-WEST" if int(b.id) in WEST else "EVP-REST"
		manifest.assets[key] = {"id":int(b.id),"owner":owner,"url":"/seventh/"+relative,"sha256":hash,"bytes":bytes.size(),"glbSha256":b.sha256,"bounds":[bounds.position.x,bounds.position.y,bounds.position.z,bounds.end.x,bounds.end.y,bounds.end.z]}
		if b.has("kind"): manifest.assets[key]["kind"] = b.kind
		manifest.areas[owner].append(key)
		model.free()
		scene = null
	for record in core_packages.values(): DirAccess.remove_absolute(record.path)
	assert(data.packetScope.id=="01-E11-21")
	var packet_ids: Array[int] = []
	for id in data.packetScope.buildingIds: packet_ids.append(int(id))
	assert(packet_ids==[247851916, 247851917, 247851918, 247851919, 247851921, 247851922, 247851923, 247851924, 247851925, 247851926, 247851927, 247851928, 247851929, 247851930, 247851931, 247851932, 247851933, 247851934, 247851936, 247851937, 247851941, 247851942])
	assert(manifest.assets.size()==398 and manifest.areas["EVP-WEST"].size()==12 and manifest.areas["EVP-REST"].size()==386)
	manifest["protectedCore"] = data.protectedCore
	for id in data.packetScope.buildingIds: assert(str(int(id)) in manifest.areas["EVP-REST"])
	manifest["release"] = JSON.stringify(manifest).sha256_text()
	var content = JSON.stringify(manifest,"\t")+"\n"
	var manifest_hash = content.sha256_text()
	var filename = "areas/manifest-"+manifest_hash+".json"
	for destination in [stage.path_join(filename),"res://assets/area_manifest.json"]:
		var file = FileAccess.open(destination,FileAccess.WRITE)
		assert(file!=null)
		file.store_string(content)
		file.close()
	var result = FileAccess.open(stage.path_join("area-export.json"),FileAccess.WRITE)
	result.store_string(JSON.stringify({"manifest":filename,"sha256":manifest_hash,"release":manifest.release,"engine":manifest.engine})+"\n")
	result.close()
	print("SEVENTH_AREAS_EXPORTED ",manifest.assets.size()," imported scenes")
	quit()
