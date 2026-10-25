extends SceneTree
## Read-only imported-core census and isolated packaging probe.
var rows: Array = []

func inspect(node: Node, parent_transform: Transform3D, group: String):
	var transform = parent_transform
	if node is Node3D: transform *= node.transform
	if str(node.name).begins_with("ProtectedCore_"): group = str(node.name).trim_prefix("ProtectedCore_")
	if node is MeshInstance3D:
		var triangles = 0
		var vertices = 0
		var materials: Array = []
		for surface in node.mesh.get_surface_count():
			var arrays = node.mesh.surface_get_arrays(surface)
			vertices += arrays[Mesh.ARRAY_VERTEX].size()
			triangles += arrays[Mesh.ARRAY_INDEX].size()/3 if arrays[Mesh.ARRAY_INDEX] != null else arrays[Mesh.ARRAY_VERTEX].size()/3
			var material = node.mesh.surface_get_material(surface)
			materials.append({"name":material.resource_name,"type":material.get_class()})
		var bounds: AABB = transform * node.mesh.get_aabb()
		rows.append({"name":str(node.name),"owner":group,"vertices":vertices,"triangles":triangles,"bounds":[bounds.position.x,bounds.position.y,bounds.position.z,bounds.end.x,bounds.end.y,bounds.end.z],"materials":materials})
	for child in node.get_children(): inspect(child,transform,group)

func assign_owner(node: Node, owner: Node):
	for child in node.get_children():
		child.owner = owner
		assign_owner(child,owner)

func _initialize():
	var args = OS.get_cmdline_user_args()
	assert(args.size()==1)
	var output = args[0]
	DirAccess.make_dir_recursive_absolute(output)
	var imported = ConfigFile.new()
	assert(imported.load("res://assets/protected-core.glb.import")==OK)
	var source: String = imported.get_value("remap","path")
	var scene = load(source)
	assert(scene is PackedScene)
	var root_node = scene.instantiate()
	inspect(root_node,Transform3D.IDENTITY,"")
	assert(rows.size()==521)
	var triangles = 0
	for row in rows: triangles += row.triangles
	assert(triangles==424497)
	var packages: Array = []
	for group in root_node.get_children():
		assign_owner(group,group)
		var packed = PackedScene.new()
		assert(packed.pack(group)==OK)
		var file = output.path_join(str(group.name)+".scn")
		assert(ResourceSaver.save(packed,file,ResourceSaver.FLAG_BUNDLE_RESOURCES)==OK)
		packages.append({"owner":str(group.name).trim_prefix("ProtectedCore_"),"bytes":FileAccess.get_file_as_bytes(file).size(),"sha256":FileAccess.get_sha256(file),"dependencies":Array(ResourceLoader.get_dependencies(file))})
	var report = {"engine":Engine.get_version_info().string,"meshes":rows,"triangles":triangles,"compiledSceneBytes":FileAccess.get_file_as_bytes(source).size(),"compiledDependencies":Array(ResourceLoader.get_dependencies(source)),"groups":packages,"scope":"Imported base-mesh counts, bounds/material census and isolated per-owner scene packaging; not visual acceptance."}
	var file = FileAccess.open(output.path_join("import-report.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"\t")+"\n")
	root_node.free()
	print("CORE_IMPORT_PROBE ",JSON.stringify({"meshes":rows.size(),"triangles":triangles,"groups":packages.size(),"compiledSceneBytes":report.compiledSceneBytes}))
	quit()
