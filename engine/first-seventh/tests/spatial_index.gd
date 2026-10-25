extends SceneTree
const Index = preload("res://scripts/spatial_index.gd")
func _initialize(): call_deferred("run")
func run():
	var index = Index.new()
	index.insert("long-return",[-201,0,-49,201,30,49])
	index.insert("negative-cell",[-97,0,-97,-96,6,-96])
	index.insert("origin",[-2,0,-2,2,5,2])
	assert(index.near(Vector3(200,0,0),0)==["long-return"])
	assert(index.near(Vector3(-96,0,-96),0)==["negative-cell"])
	var near_origin = index.near(Vector3.ZERO,0)
	assert(near_origin.size()==2 and "origin" in near_origin and "long-return" in near_origin)
	assert(index.near(Vector3(1000,0,1000),20).is_empty())
	var viewport = SubViewport.new()
	viewport.size = Vector2i(1440,1000)
	root.add_child(viewport)
	var camera = Camera3D.new()
	camera.far = 370
	camera.fov = 82
	viewport.add_child(camera)
	var corners = Index.new()
	corners.insert("wide-corner",[400,0,-366,410,10,-360])
	corners.insert("past-far",[0,0,-410,10,10,-400])
	assert(camera.is_position_in_frustum(Vector3(405,5,-363)))
	assert("wide-corner" in corners.in_view(camera))
	assert("past-far" not in corners.in_view(camera))
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 600
	assert("wide-corner" in corners.in_view(camera))
	var city = Index.new()
	var began = Time.get_ticks_usec()
	for x in range(-100,100):
		for z in range(-250,250):
			city.insert(str(x)+":"+str(z),[x*35.0,0,z*35.0,x*35.0+18,24,z*35.0+22])
	var construction_ms = (Time.get_ticks_usec()-began)/1000.0
	var maximum = 0
	began = Time.get_ticks_usec()
	for i in range(100):
		var local = city.near(Vector3((i%10)*200-1000,0,(i/10)*200-1000),370)
		maximum = maxi(maximum,local.size())
		assert(local.size()<500,"Local query must not return the whole synthetic city")
	print("SPATIAL_INDEX_PASS ",JSON.stringify({"records":city.bounds.size(),"cells":city.cells.size(),"maxLocalResults":maximum,"constructMs":construction_ms,"hundredQueriesMs":(Time.get_ticks_usec()-began)/1000.0,"limits":"CPU metadata index only; synthetic boxes, not a100000-building browser render or memory benchmark"}))
	quit()
