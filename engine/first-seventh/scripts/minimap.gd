extends Control

var car: Node3D
var elapsed = 0.0
const INK = Color("dac8a9")

func _ready():
	custom_minimum_size = Vector2(180,92)
	mouse_filter = Control.MOUSE_FILTER_IGNORE

func point(x: float, z: float) -> Vector2:
	return Vector2((x+280)*.46,(z+128)*.40)

func _process(dt):
	elapsed += dt
	if elapsed > .10:
		elapsed = 0
		queue_redraw()

func _draw():
	var road = Color("738c88")
	draw_rect(Rect2(point(-218,-73),point(-11,-5)-point(-218,-73)),Color("354c51"))
	for x in [-229,0]: draw_line(point(x,-119),point(x,57),road,4,true)
	for z in [-77.9,0]: draw_line(point(-269,z),point(77,z),road,2.5,true)
	var font = ThemeDB.fallback_font
	draw_string(font,Vector2(8,11),"2ND",HORIZONTAL_ALIGNMENT_LEFT,-1,8,INK)
	draw_string(font,Vector2(137,11),"1ST",HORIZONTAL_ALIGNMENT_LEFT,-1,8,INK)
	draw_string(font,Vector2(54,15),"ST MARKS",HORIZONTAL_ALIGNMENT_LEFT,-1,8,INK)
	draw_string(font,Vector2(57,66),"SEVENTH",HORIZONTAL_ALIGNMENT_LEFT,-1,8,INK)
	draw_string(font,Vector2(163,85),"N ^",HORIZONTAL_ALIGNMENT_LEFT,-1,8,INK)
	if car:
		var p = point(car.position.x,car.position.z)
		draw_circle(p,6,Color(.95,.74,.54,.15))
		var arrow = PackedVector2Array()
		for vertex in [Vector2(0,-5),Vector2(3.4,4),Vector2(0,2),Vector2(-3.4,4)]:
			arrow.append(vertex.rotated(-car.rotation.y)+p)
		draw_colored_polygon(arrow,Color("ffe0a8"))
