extends RefCounted
## Split existing imported groups into self-contained immutable runtime scenes.
## Original material/texture resources are bundled, never replaced by paint shaders.

static func set_owners(node: Node, root_node: Node):
	for child in node.get_children():
		child.owner = root_node
		set_owners(child,root_node)

static func detach_textures(node: Node):
	var library = preload("res://scripts/protected_core_textures.gd")
	library.prepare()
	if node is MeshInstance3D:
		node.mesh = node.mesh.duplicate()
		var bindings: Array = []
		# Duplicate material resources, never mutate the imported source scene.
		for surface in node.mesh.get_surface_count():
			var material = node.mesh.surface_get_material(surface).duplicate()
			var slots: Dictionary = {}
			for slot in BaseMaterial3D.TEXTURE_MAX:
				var texture = material.get_texture(slot)
				if texture:
					var pixels = texture.get_image().duplicate()
					pixels.clear_mipmaps()
					var index = library.base_hashes.find(library.digest(pixels.get_data()))
					assert(index>=0,"Original texture not found in immutable library")
					slots[str(slot)] = index
					material.set_texture(slot,null)
			node.mesh.surface_set_material(surface,material)
			if not slots.is_empty(): bindings.append({"surface":surface,"slots":slots})
		if not bindings.is_empty(): node.set_meta("core_texture_bindings",bindings)
	for child in node.get_children(): detach_textures(child)

static func compile(stage: String, reuse_reviewed: bool = true) -> Dictionary:
	var metadata = JSON.parse_string(FileAccess.get_file_as_string("res://assets/protected-core.json"))
	assert(metadata is Dictionary and metadata.buildingOwners.size()==23 and metadata.sharedModels.size()==1)
	assert(FileAccess.get_sha256("res://assets/protected-core.glb")==metadata.convertedSha256)
	if reuse_reviewed:
		# Runtime scenes are already required tracked assets. ResourceSaver may
		# assign different serialization IDs after unrelated imports; retaining
		# the reviewed bytes preserves both resource identity and visual content.
		var frozen = JSON.parse_string(FileAccess.get_file_as_string("res://assets/protected-core-scenes.json"))
		assert(frozen.sourceSha256==metadata.sourceSha256 and frozen.convertedSha256==metadata.convertedSha256)
		assert(frozen.texturesSha256==FileAccess.get_sha256("res://assets/protected-core-textures.bin"))
		assert(frozen.assets.size()==24)
		var retained: Dictionary = {}
		for record in metadata.buildingOwners + metadata.sharedModels:
			var key = str(int(record.id))
			var entry = frozen.assets[key]
			var original = ProjectSettings.globalize_path("res://../../dist/seventh/areas/assets/"+entry.sha256+".scn")
			assert(FileAccess.get_sha256(original)==entry.sha256,"Missing or modified reviewed core scene: "+key)
			var bytes = FileAccess.get_file_as_bytes(original)
			assert(bytes.size()==int(entry.bytes))
			var temporary = stage.path_join("core-"+key+".scn")
			var file = FileAccess.open(temporary,FileAccess.WRITE)
			assert(file!=null)
			file.store_buffer(bytes)
			file.close()
			retained[key] = {"path":temporary,"sha256":entry.sha256,"bytes":bytes.size()}
		return retained
	var scene = load("res://assets/protected-core.glb")
	assert(scene is PackedScene)
	var source = scene.instantiate()
	var result: Dictionary = {}
	for record in metadata.buildingOwners + metadata.sharedModels:
		var group = source.get_node(NodePath(record.group))
		assert(group is Node3D and group.transform.is_equal_approx(Transform3D.IDENTITY))
		set_owners(group,group)
		detach_textures(group)
		var packed = PackedScene.new()
		assert(packed.pack(group)==OK)
		var temporary = stage.path_join("core-"+str(int(record.id))+".scn")
		assert(ResourceSaver.save(packed,temporary,ResourceSaver.FLAG_BUNDLE_RESOURCES | ResourceSaver.FLAG_COMPRESS)==OK)
		assert(ResourceLoader.get_dependencies(temporary).is_empty())
		var bytes = FileAccess.get_file_as_bytes(temporary)
		assert(bytes.size()>0 and bytes.size()<=8*1024*1024)
		result[str(int(record.id))] = {"path":temporary,"sha256":FileAccess.get_sha256(temporary),"bytes":bytes.size()}
	source.free()
	return result
