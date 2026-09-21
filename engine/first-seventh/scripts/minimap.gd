extends Control

var car: Node3D
var elapsed = 0.0
const INK = Color("a8b3ad")

func _ready():
	custom_minimum_size = Vector2(198,78)
	mouse_filter = Control.MOUSE_FILTER_IGNORE

func point(x: float, z: float) -> Vector2:
	return Vector2((x+317)*.315,(z+128)*.40)

func _process(dt):
	elapsed += dt
	if elapsed > .10:
		elapsed = 0
		queue_redraw()

func _draw():
	var road = Color("aec4b5")
	draw_rect(Rect2(point(-218,-73),point(-11,-5)-point(-218,-73)),Color("243536"))
	draw_rect(Rect2(point(11,-40),point(205,-5)-point(11,-40)),Color("243536"))
	for x in [-229,0]: draw_line(point(x,-119),point(x,57),road,4,true)
	draw_line(point(214,-38),point(214,57),road,4,true)
	draw_line(point(-269,-77.9),point(77,-77.9),road,2.5,true)
	draw_line(point(-306,0),point(289,0),road,2.5,true)
	var font = ThemeDB.fallback_font
	draw_string(font,Vector2(18,11),"2ND",HORIZONTAL_ALIGNMENT_LEFT,-1,8,INK)
	draw_string(font,Vector2(94,11),"1ST",HORIZONTAL_ALIGNMENT_LEFT,-1,8,INK)
	draw_string(font,Vector2(164,30),"AVE A",HORIZONTAL_ALIGNMENT_LEFT,-1,8,INK)
	draw_string(font,Vector2(47,15),"ST MARKS",HORIZONTAL_ALIGNMENT_LEFT,-1,8,INK)
	draw_string(font,Vector2(60,68),"SEVENTH STREET",HORIZONTAL_ALIGNMENT_LEFT,-1,8,INK)
	draw_string(font,Vector2(185,70),"N ^",HORIZONTAL_ALIGNMENT_LEFT,-1,8,INK)
	if car:
		var p = point(car.position.x,car.position.z)
		draw_circle(p,6,Color(.68,.77,.71,.16))
		var arrow = PackedVector2Array()
		for vertex in [Vector2(0,-5),Vector2(3.4,4),Vector2(0,2),Vector2(-3.4,4)]:
			arrow.append(vertex.rotated(-car.rotation.y)+p)
		draw_colored_polygon(arrow,Color("f4f2eb"))
