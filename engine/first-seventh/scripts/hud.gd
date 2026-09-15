extends CanvasLayer

signal start_requested
signal camera_requested
signal weather_requested(mode: int)
signal reset_requested
signal pause_requested
signal audio_requested
signal photo_requested

const INK = Color("f3e8d5")
const MUTED = Color("c3c9c2")
const BG = Color(.095,.14,.18,.83)
var root: Control
var top: MarginContainer
var bottom: MarginContainer
var speed_label: Label
var camera_button: Button
var weather_buttons: Array[Button] = []
var intro: PanelContainer
var intro_title: Label
var start_button: Button
var loading_label: Label
var pause_panel: PanelContainer
var distance_label: Label
var drivetrain_label: Label
var mood_label: Label
var status_label: Label
var audio_button: Button
var minimap: Control
var is_started = false
var shown = true
var toast_time = 0.0

func style(color: Color = BG, radius: int = 14) -> StyleBoxFlat:
	var b = StyleBoxFlat.new()
	b.bg_color = color
	b.set_corner_radius_all(radius)
	b.content_margin_left = 17
	b.content_margin_right = 17
	b.content_margin_top = 12
	b.content_margin_bottom = 12
	b.set_border_width_all(1)
	b.border_color = Color(1,1,1,.10)
	return b

func label(text: String, size: int, color: Color = INK) -> Label:
	var node = Label.new()
	node.text = text
	node.add_theme_font_size_override("font_size",size)
	node.add_theme_color_override("font_color",color)
	return node

func button(text: String, callback: Callable) -> Button:
	var node = Button.new()
	node.text = text
	node.focus_mode = Control.FOCUS_NONE
	node.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	node.add_theme_stylebox_override("normal",style(Color(.12,.18,.22,.76),10))
	node.add_theme_stylebox_override("hover",style(Color(.27,.38,.38,.91),10))
	node.add_theme_stylebox_override("pressed",style(Color(.34,.47,.42,.98),10))
	node.add_theme_color_override("font_color",INK)
	node.add_theme_font_size_override("font_size",14)
	node.pressed.connect(callback)
	return node

func _ready():
	root = Control.new()
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(root)
	var film = ColorRect.new()
	film.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	film.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var effect = ShaderMaterial.new()
	effect.shader = preload("res://shaders/film.gdshader")
	film.material = effect
	root.add_child(film)
	top = MarginContainer.new()
	top.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	top.add_theme_constant_override("margin_left",30)
	top.add_theme_constant_override("margin_right",30)
	top.add_theme_constant_override("margin_top",24)
	root.add_child(top)
	var row = HBoxContainer.new()
	row.add_theme_constant_override("separation",12)
	top.add_child(row)
	var identity = VBoxContainer.new()
	identity.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(identity)
	identity.add_child(label("B O R O U G H   D R I V E",13))
	identity.add_child(label("Seventh, slowly.",27))
	mood_label = label("EAST VILLAGE  /  GOLDEN HOUR",11,MUTED)
	identity.add_child(mood_label)
	var actions = VBoxContainer.new()
	row.add_child(actions)
	var moods = HBoxContainer.new()
	moods.add_theme_constant_override("separation",6)
	actions.add_child(moods)
	for i in range(3):
		var names = ["Golden","Dusk","Rain"]
		var b = button(names[i],func(): weather_requested.emit(i))
		moods.add_child(b)
		weather_buttons.append(b)
	var utilities = HBoxContainer.new()
	utilities.alignment = BoxContainer.ALIGNMENT_END
	utilities.add_theme_constant_override("separation",6)
	actions.add_child(utilities)
	audio_button = button("Sound off",func(): audio_requested.emit())
	utilities.add_child(audio_button)
	utilities.add_child(button("Pause",func(): pause_requested.emit()))
	bottom = MarginContainer.new()
	bottom.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
	bottom.grow_vertical = Control.GROW_DIRECTION_BEGIN
	bottom.add_theme_constant_override("margin_left",30)
	bottom.add_theme_constant_override("margin_right",30)
	bottom.add_theme_constant_override("margin_bottom",24)
	root.add_child(bottom)
	var lower = HBoxContainer.new()
	lower.alignment = BoxContainer.ALIGNMENT_END
	lower.add_theme_constant_override("separation",14)
	bottom.add_child(lower)
	var speed_panel = PanelContainer.new()
	speed_panel.add_theme_stylebox_override("panel",style())
	lower.add_child(speed_panel)
	var instrument = VBoxContainer.new()
	instrument.add_theme_constant_override("separation",10)
	speed_panel.add_child(instrument)
	minimap = preload("res://scripts/minimap.gd").new()
	instrument.add_child(minimap)
	var numbers = HBoxContainer.new()
	numbers.add_theme_constant_override("separation",12)
	instrument.add_child(numbers)
	speed_label = label("00",38)
	speed_label.custom_minimum_size.x = 55
	numbers.add_child(speed_label)
	var units = VBoxContainer.new()
	units.alignment = BoxContainer.ALIGNMENT_CENTER
	numbers.add_child(units)
	units.add_child(label("MPH",11,MUTED))
	distance_label = label("JUST WANDER",10,MUTED)
	units.add_child(distance_label)
	drivetrain_label = label("D1  ·  850 RPM",10,MUTED)
	instrument.add_child(drivetrain_label)
	var controls = VBoxContainer.new()
	controls.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	controls.alignment = BoxContainer.ALIGNMENT_END
	lower.add_child(controls)
	status_label = label("",13,INK)
	status_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	controls.add_child(status_label)
	var hint = label("WASD  drive / S  brake     SPACE  handbrake     C  camera     T  weather",12,INK)
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	controls.add_child(hint)
	var hint2 = label("Right-drag  look around     R  reset     H  hide interface",11,MUTED)
	hint2.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	controls.add_child(hint2)
	var views = VBoxContainer.new()
	views.alignment = BoxContainer.ALIGNMENT_END
	lower.add_child(views)
	camera_button = button("Camera  /  Chase   >",func(): camera_requested.emit())
	views.add_child(camera_button)
	views.add_child(button("Postcard  ·  P",func(): photo_requested.emit()))
	build_intro()
	build_pause()
	bottom.hide()
	top.hide()

func build_intro():
	intro = PanelContainer.new()
	intro.set_anchors_and_offsets_preset(Control.PRESET_CENTER_LEFT)
	intro.position = Vector2(46,-115)
	intro.custom_minimum_size = Vector2(420,270)
	intro.add_theme_stylebox_override("panel",style(Color(.09,.14,.19,.84),22))
	root.add_child(intro)
	var box = VBoxContainer.new()
	box.add_theme_constant_override("separation",13)
	intro.add_child(box)
	box.add_child(label("A LITTLE NEW YORK, AT YOUR OWN PACE",12,MUTED))
	intro_title = label("Seventh,\nslowly.",57)
	box.add_child(intro_title)
	box.add_child(label("A warm evening. A familiar corner.\nNowhere you need to be.",17,INK))
	loading_label = label("Opening the neighborhood…",13,MUTED)
	box.add_child(loading_label)
	start_button = button("Take a slow drive   >",func(): start_requested.emit())
	start_button.add_theme_font_size_override("font_size",18)
	start_button.disabled = true
	box.add_child(start_button)
	box.add_child(label("FIRST & SEVENTH  ·  EAST VILLAGE",11,MUTED))

func build_pause():
	pause_panel = PanelContainer.new()
	pause_panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	pause_panel.position = Vector2(-175,-145)
	pause_panel.custom_minimum_size = Vector2(350,260)
	pause_panel.add_theme_stylebox_override("panel",style(Color(.09,.14,.19,.95),20))
	root.add_child(pause_panel)
	var box = VBoxContainer.new()
	box.add_theme_constant_override("separation",12)
	pause_panel.add_child(box)
	box.add_child(label("Take your time.",30))
	box.add_child(button("Back to the drive",func(): pause_requested.emit()))
	box.add_child(button("Return to First & Seventh",func(): reset_requested.emit()))
	box.add_child(button("Fullscreen",func():
		var fullscreen = DisplayServer.window_get_mode()==DisplayServer.WINDOW_MODE_FULLSCREEN
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED if fullscreen else DisplayServer.WINDOW_MODE_FULLSCREEN)))
	box.add_child(label("A small neighborhood study.\nMapped buildings; authored atmosphere.",12,MUTED))
	pause_panel.hide()

func loaded(ok: bool):
	loading_label.text = "WASD to drive. Turn + tap Space to slide." if ok else "A neighborhood file is missing. Reload to try again."
	start_button.disabled = not ok

func begin():
	is_started = true
	intro.hide()
	top.show()
	bottom.show()

func set_progress(value: float):
	loading_label.text = "Opening the neighborhood  ·  %d%%" % roundi(value*100)

func set_paused(value: bool):
	pause_panel.visible = value

func toggle_interface():
	shown = not shown
	top.visible = shown and is_started
	bottom.visible = shown and is_started

func toast(message: String):
	status_label.text = message
	toast_time = 4.0

func update_drivetrain(handling, handbrake: bool):
	var gear = "R" if handling.speed<-.3 else "D%d" % handling.gear
	var slide = "  ·  SLIDING" if absf(handling.slip)>.23 and absf(handling.speed)>4 else "  ·  HANDBRAKE" if handbrake else ""
	drivetrain_label.text = "%s  ·  %d RPM%s" % [gear,roundi(handling.rpm/50)*50,slide]
	drivetrain_label.modulate = Color("edba8e") if not slide.is_empty() else Color.WHITE

func update_display(speed: float, distance: float, camera_name: String, weather_name: String, mood: int, dt: float):
	speed_label.text = "%02d" % roundi(abs(speed)*2.23694)
	distance_label.text = "%03d M  WANDERED" % roundi(distance)
	camera_button.text = "Camera  /  %s   >" % camera_name
	mood_label.text = "EAST VILLAGE  /  "+weather_name.to_upper()
	for i in weather_buttons.size():
		weather_buttons[i].modulate = Color(1.0,1.0,1.0) if i==mood else Color(.78,.82,.82)
	if toast_time > 0:
		toast_time -= dt
		if toast_time <= 0: status_label.text = ""
