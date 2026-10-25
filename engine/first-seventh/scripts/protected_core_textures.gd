extends RefCounted
## Original encoded images, decoded once and shared by all protected owners.
## No reference-image acquisition or image re-encoding occurs here.
static var textures: Array = []
static var base_hashes: Array = []

static func digest(bytes: PackedByteArray) -> String:
	var hashing = HashingContext.new()
	hashing.start(HashingContext.HASH_SHA256)
	hashing.update(bytes)
	return hashing.finish().hex_encode()

static func prepare():
	if not textures.is_empty(): return
	var metadata = JSON.parse_string(FileAccess.get_file_as_string("res://assets/protected-core-textures.json"))
	var bytes = FileAccess.get_file_as_bytes("res://assets/protected-core-textures.bin")
	assert(digest(bytes)==metadata.sha256)
	for row in metadata.images:
		var encoded = bytes.slice(int(row.offset),int(row.offset+row.length))
		assert(digest(encoded)==row.sha256)
		var pixels = Image.new()
		var error = pixels.load_jpg_from_buffer(encoded) if row.mime=="image/jpeg" else pixels.load_png_from_buffer(encoded)
		assert(error==OK)
		base_hashes.append(digest(pixels.get_data()))
		textures.append(ImageTexture.create_from_image(pixels))

static func bind(node: Node):
	prepare()
	if node is MeshInstance3D and node.has_meta("core_texture_bindings"):
		for row in node.get_meta("core_texture_bindings"):
			var material = node.mesh.surface_get_material(int(row.surface))
			for slot in row.slots: material.set_texture(int(slot),textures[int(row.slots[slot])])
	for child in node.get_children(): bind(child)
