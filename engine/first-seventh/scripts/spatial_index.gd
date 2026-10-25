extends RefCounted
## Index full asset bounds, including long corner returns, in world-space cells.
const CELL = 96.0
var cells: Dictionary = {}
var bounds: Dictionary = {}

func insert(key: String, box: Array):
	bounds[key] = box
	for x in range(floori(box[0]/CELL),floori(box[3]/CELL)+1):
		for z in range(floori(box[2]/CELL),floori(box[5]/CELL)+1):
			var cell = Vector2i(x,z)
			if not cells.has(cell): cells[cell] = []
			cells[cell].append(key)

static func distance(point: Vector3, box: Array) -> float:
	return Vector2(maxf(maxf(box[0]-point.x,0),point.x-box[3]),maxf(maxf(box[2]-point.z,0),point.z-box[5])).length()

func near(point: Vector3, radius: float) -> Array:
	var result: Dictionary = {}
	for x in range(floori((point.x-radius)/CELL),floori((point.x+radius)/CELL)+1):
		for z in range(floori((point.z-radius)/CELL),floori((point.z+radius)/CELL)+1):
			for key in cells.get(Vector2i(x,z),[]):
				if not result.has(key) and distance(point,bounds[key])<=radius:
					result[key] = true
	return result.keys()

func in_view(camera: Camera3D, margin: float = 4.0) -> Array:
	var result: Array = []
	var planes = camera.get_frustum()
	# Far is camera-space depth, not a sphere radius. Wide and oblique views
	# can see corners much farther away horizontally than the far distance.
	var extent = camera.get_camera_projection().get_far_plane_half_extents()
	if camera.projection==Camera3D.PROJECTION_ORTHOGONAL:
		extent += Vector2(margin,margin)
	else:
		var slope = extent/camera.far
		extent += slope*margin+Vector2(sqrt(1+slope.x*slope.x),sqrt(1+slope.y*slope.y))*margin
	var radius = Vector3(extent.x,extent.y,camera.far+margin).length()
	for key in near(camera.get_camera_transform().origin,radius):
		var box: Array = bounds[key]
		var outside = false
		for plane in planes:
			var nearest = Vector3(box[0] if plane.normal.x>=0 else box[3],box[1] if plane.normal.y>=0 else box[4],box[2] if plane.normal.z>=0 else box[5])
			if plane.distance_to(nearest)>margin:
				outside = true
				break
		if not outside: result.append(key)
	return result
