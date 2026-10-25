extends SceneTree
const Index = preload("res://scripts/spatial_index.gd")
func _initialize(): call_deferred("run")
func run():
	var viewport = SubViewport.new()
	viewport.size = Vector2i(1440,1000)
	root.add_child(viewport)
	var camera = Camera3D.new()
	camera.far = 370
	viewport.add_child(camera)
	var streamer = preload("res://scripts/area_streamer.gd").new()
	root.add_child(streamer)
	for x in range(-40,40):
		for z in range(-60,40):
			var key = str(x)+":"+str(z)
			streamer.index.insert(key,[x*20.0,0,z*20.0,x*20.0+14,30,z*20.0+16])
			streamer.records[key] = {"state":"active","lastWanted":0}
	var checks = 0
	for i in range(240):
		camera.position = Vector3(i*.22-40,3,-i*.31)
		camera.rotation = Vector3(.02*sin(i*.015),i*.002,0)
		camera.fov = 55+i*.035
		assert(streamer.permit_camera(camera))
		var active: Dictionary = {}
		for key in streamer.camera_keys: active[key] = true
		for key in streamer.index.in_view(camera,4):
			assert(active.has(key),"Cached view omitted an actually visible owner at pose"+str(i)+":"+key)
		checks += 1
	assert(streamer.view_cache_hits>streamer.view_queries)
	print("CAMERA_CACHE_PASS ",JSON.stringify({"poses":checks,"catalog":streamer.records.size(),"queries":streamer.view_queries,"cacheHits":streamer.view_cache_hits,"scope":"Every exact4m-padded view remains inside cached12m-padded owner set while moving, turning, tilting and changing FOV. Metadata-only proof."}))
	quit()
