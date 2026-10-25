extends RefCounted
## Keep new facade recipes separate from the immutable accepted core.
static func with_protected_core(slice: Dictionary) -> Dictionary:
	var core = JSON.parse_string(FileAccess.get_file_as_string("res://assets/protected-core.json"))
	assert(core is Dictionary and core.buildingOwners.size()==23)
	var result: Dictionary = slice.duplicate(true)
	var ids: Dictionary = {}
	for building in result.buildings: ids[int(building.id)] = true
	for building in core.buildingOwners:
		assert(not ids.has(int(building.id)),"Protected core has a duplicate building owner")
		ids[int(building.id)] = true
		result.buildings.append(building)
	result["sharedModels"] = core.sharedModels.duplicate(true)
	for model in result.sharedModels:
		assert(int(model.id)<0 and not ids.has(int(model.id)))
		assert(model.kind=="protected-core-details")
	result["protectedCore"] = {"buildingCount":core.buildingOwners.size(),"sharedModelCount":core.sharedModels.size(),"sourceSha256":core.sourceSha256,"convertedSha256":core.convertedSha256}
	return result
