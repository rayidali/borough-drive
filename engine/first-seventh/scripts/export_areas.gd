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
	var data = JSON.parse_string(FileAccess.get_file_as_string("res://assets/slice.json"))
	var manifest = {"schema":1,"engine":"4.7.2","originShift":data.originShift,"assets":{},"areas":{"EVP-WEST":[],"EVP-REST":[]}}
	DirAccess.make_dir_recursive_absolute(stage.path_join("areas/assets"))
	for b in data.buildings:
		var imported = ConfigFile.new()
		assert(imported.load(b.asset+".import")==OK)
		var source: String = imported.get_value("remap","path")
		assert(ResourceLoader.get_dependencies(source).is_empty(),"External scene dependency requires explicit packaging")
		var bytes = FileAccess.get_file_as_bytes(source)
		assert(bytes.size()>0 and bytes.size()<=8*1024*1024)
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
		var key = str(int(b.id))
		manifest.assets[key] = {"id":int(b.id),"owner":owner,"url":"/seventh/"+relative,"sha256":hash,"bytes":bytes.size(),"glbSha256":b.sha256,"bounds":[bounds.position.x,bounds.position.y,bounds.position.z,bounds.end.x,bounds.end.y,bounds.end.z]}
		manifest.areas[owner].append(key)
		model.free()
		scene = null
	assert(data.packetScope.id=="01-E09-1A")
	var packet_ids: Array[int] = []
	for id in data.packetScope.buildingIds: packet_ids.append(int(id))
	assert(packet_ids==[248142661, 248142662, 248142663, 248142664, 248142666, 248142668, 248142669, 248142672, 248142675, 248142676, 248142677, 248142679, 248142681, 248142682, 248142683, 248142684, 248142685, 248142702, 248142710, 248142713, 248142716, 248142921, 248142923, 248142925, 248142926, 248142927, 248142929, 248142930, 248142932, 248142934, 248142936, 248142938, 248142940, 248142942, 248142944, 248142945, 248142947, 248142948, 248142950, 248142955, 248142963])
	assert(manifest.assets.size()==295 and manifest.areas["EVP-WEST"].size()==12 and manifest.areas["EVP-REST"].size()==283)
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
