extends Control
## A north-up neighborhood map. Only the small marker redraws while stationary.
const SCALE = .57
const CELL = 80.0
const PAPER = Color("172829")
const BLOCK = Color("223b39")
const EDGE = Color("304b45")
const ROAD = Color("849b87")
const INK = Color("c5d0bc")
const ACCENT = Color("f1c48b")
const ROADS = [
	[-229,-119,-229,57,20,"2 AV"], [0,-315.3,0,57,20,"1 AV"],
	[214,-38,214,57,20,"AV A"],
	[-269,-77.9,77,-77.9,12,"ST MARKS"], [-306,0,289,0,12,"E 7 ST"],
	[-213,-154.7,207,-154.7,12,"E 9 ST"],
	[-213,-228,207,-228,12,"E 10 ST"],
	[-213,-304.3,13,-304.3,12,"E 11 ST"]
]
var car: Node3D
var center = Vector2.ZERO
var elapsed = 0.0
var footprint_grid: Dictionary = {}
var marker: Control
var last_heading = INF
var last_position = Vector2.INF
var map_min = Vector2(-330,-365)
var map_max = Vector2(325,80)
var card: StyleBoxFlat
var map_viewport: SubViewport
var map_layer: Control
var cached_center = Vector2.INF
var cached_size = Vector2.ZERO
var map_rasterizations = 0

func _ready():
	custom_minimum_size = Vector2(228,156)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	clip_contents = true
	card = StyleBoxFlat.new()
	card.bg_color = PAPER
	card.set_corner_radius_all(8)
	card.border_color = Color("37534b")
	card.set_border_width_all(1)
	map_viewport = SubViewport.new()
	map_viewport.disable_3d = true
	map_viewport.transparent_bg = true
	map_viewport.render_target_update_mode = SubViewport.UPDATE_ONCE
	add_child(map_viewport)
	map_layer = Control.new()
	map_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	map_layer.draw.connect(draw_map)
	map_viewport.add_child(map_layer)
	marker = Control.new()
	marker.mouse_filter = Control.MOUSE_FILTER_IGNORE
	marker.draw.connect(draw_marker)
	add_child(marker)
	resized.connect(refresh_map)
	refresh_map()

func configure(data: Dictionary):
	footprint_grid.clear()
	map_min = Vector2.INF
	map_max = -Vector2.INF
	for b in data.buildings:
		var polygon = PackedVector2Array()
		var low = Vector2.INF
		var high = -Vector2.INF
		for v in b.footprint:
			var p = Vector2(v[0],v[1])
			map_min = map_min.min(p)
			map_max = map_max.max(p)
			polygon.append(p)
			low = low.min(p)
			high = high.max(p)
		if polygon.size()<3: continue
		var record = {"id":int(b.id),"polygon":polygon}
		for x in range(floori(low.x/CELL),floori(high.x/CELL)+1):
			for z in range(floori(low.y/CELL),floori(high.y/CELL)+1):
				var key = Vector2i(x,z)
				if not footprint_grid.has(key): footprint_grid[key] = []
				footprint_grid[key].append(record)
	map_min -= Vector2(24,24)
	map_max += Vector2(24,24)
	refresh_map(true)

func point(p: Vector2) -> Vector2:
	return size*.5+(p-center)*SCALE

func _process(dt):
	if not is_visible_in_tree() or not car: return
	elapsed += dt
	if elapsed<.05: return
	elapsed = 0.0
	var car_point = Vector2(car.position.x,car.position.z)
	# Follow within the authored neighborhood. Near a boundary, move the
	# marker across the map instead of centering a largely empty frontier.
	var half = size/(2*SCALE)
	var low = map_min+half
	var high = map_max-half
	var next = car_point-Vector2(0,45)
	next.x = clampf(next.x,low.x,high.x) if low.x<=high.x else (map_min.x+map_max.x)*.5
	next.y = clampf(next.y,low.y,high.y) if low.y<=high.y else (map_min.y+map_max.y)*.5
	if next.distance_squared_to(center)>.09:
		center = next
		refresh_map()
		marker.queue_redraw()
	if car_point.distance_squared_to(last_position)>.01:
		last_position = car_point
		marker.queue_redraw()
	if absf(car.rotation.y-last_heading)>.004:
		last_heading = car.rotation.y
		marker.queue_redraw()

func draw_marker():
	if not car: return
	var p = point(Vector2(car.position.x,car.position.z))
	marker.draw_circle(p,12,Color(0.94,.77,.54,.08))
	marker.draw_circle(p,8,Color(0.94,.77,.54,.17))
	var arrow = PackedVector2Array()
	for v in [Vector2(0,-6.5),Vector2(4.5,5),Vector2(0,2.5),Vector2(-4.5,5)]:
		arrow.append(v.rotated(-car.rotation.y)+p)
	marker.draw_colored_polygon(arrow,ACCENT)
	arrow.append(arrow[0])
	marker.draw_polyline(arrow,Color("fff0d7"),1,true)

func refresh_map(force: bool = false):
	if not map_viewport: return
	# Rasterize a bounded neighborhood patch with overscan. Normal motion
	# shifts a texture crop; it does not redraw hundreds of vector footprints.
	var displacement = (center-cached_center).abs()*SCALE
	if force or cached_size!=size or displacement.x>size.x*.4 or displacement.y>size.y*.4:
		cached_center = (center*SCALE).round()/SCALE
		cached_size = size
		map_viewport.size = Vector2i(maxi(1,int(size.x*2)),maxi(1,int(size.y*2)))
		map_layer.size = Vector2(map_viewport.size)
		map_layer.queue_redraw()
		map_viewport.render_target_update_mode = SubViewport.UPDATE_ONCE
		map_rasterizations += 1
	queue_redraw()

func cache_point(p: Vector2) -> Vector2:
	return Vector2(map_viewport.size)*.5+(p-cached_center)*SCALE

func _draw():
	if not map_viewport: return
	draw_style_box(card,Rect2(Vector2.ZERO,size))
	var origin = (Vector2(map_viewport.size)-size)*.5+(center-cached_center)*SCALE
	draw_texture_rect_region(map_viewport.get_texture(),Rect2(Vector2.ONE,size-Vector2(2,2)),Rect2(origin+Vector2.ONE,size-Vector2(2,2)))
	var font = get_theme_default_font()
	for road in ROADS:
		var a = point(Vector2(road[0],road[1]))
		var b = point(Vector2(road[2],road[3]))
		var vertical: bool = road[0]==road[2]
		var label_position = Vector2(a.x+9,clampf((a.y+b.y)/2,22,size.y-15)) if vertical else Vector2(clampf((a.x+b.x)/2,35,size.x-42),a.y-9)
		if label_position.distance_to(size*.5)<25: label_position.y += 34 if vertical else -8
		if Rect2(9,10,size.x-18,size.y-22).has_point(label_position):
			var text_width = font.get_string_size(road[5],HORIZONTAL_ALIGNMENT_LEFT,-1,9).x
			draw_rect(Rect2(label_position-Vector2(3,10),Vector2(text_width+6,14)),PAPER)
			draw_string(font,label_position,road[5],HORIZONTAL_ALIGNMENT_LEFT,-1,9,INK)
	# Scale remains screen-aligned while the cached neighborhood moves.
	draw_rect(Rect2(7,size.y-23,47,17),PAPER)
	draw_line(Vector2(12,size.y-10),Vector2(12+50*SCALE,size.y-10),INK,1,true)
	draw_line(Vector2(12,size.y-13),Vector2(12,size.y-8),INK,1,true)
	draw_line(Vector2(12+50*SCALE,size.y-13),Vector2(12+50*SCALE,size.y-8),INK,1,true)
	draw_string(font,Vector2(14,size.y-15),"50 m",HORIZONTAL_ALIGNMENT_LEFT,-1,8,INK)

func draw_map():
	var patch_size = Vector2(map_viewport.size)
	map_layer.draw_rect(Rect2(Vector2.ZERO,patch_size),PAPER)
	var half = patch_size/(2*SCALE)
	var low = Vector2i(floori((cached_center.x-half.x-70)/CELL),floori((cached_center.y-half.y-70)/CELL))
	var high = Vector2i(floori((cached_center.x+half.x+70)/CELL),floori((cached_center.y+half.y+70)/CELL))
	var seen: Dictionary = {}
	for x in range(low.x,high.x+1):
		for z in range(low.y,high.y+1):
			for record in footprint_grid.get(Vector2i(x,z),[]):
				if seen.has(record.id): continue
				seen[record.id] = true
				var shape = PackedVector2Array()
				for v in record.polygon: shape.append(cache_point(v))
				map_layer.draw_colored_polygon(shape,BLOCK)
				shape.append(shape[0])
				map_layer.draw_polyline(shape,EDGE,.65,true)
	for road in ROADS:
		var a = cache_point(Vector2(road[0],road[1]))
		var b = cache_point(Vector2(road[2],road[3]))
		var width: float = road[4]*SCALE
		map_layer.draw_line(a,b,Color("304c43"),width+4,true)
		map_layer.draw_line(a,b,ROAD,width,true)
		map_layer.draw_line(a,b,Color("b5c1a1"),.8,true)
