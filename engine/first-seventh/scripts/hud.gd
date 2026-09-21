extends CanvasLayer

signal start_requested
signal camera_requested
signal weather_requested(mode: int)
signal reset_requested
signal pause_requested
signal audio_requested
signal photo_requested

# The HUD deliberately stays quieter than the world. These values also make
# it possible to tune the whole interface without changing individual nodes.
const INK = Color("f4f2eb")
const MUTED = Color("a8b3ad")
const CHARCOAL = Color("182426")
const SAGE = Color("aec4b5")
const WARM = Color("e7c9a9")
const BG = Color(0.094,0.141,0.149,0.91)

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
var pause_resume_button: Button
var distance_label: Label
var address_label: Label
var drivetrain_label: Label
var mood_label: Label
var status_label: Label
var audio_button: Button
var pause_button: Button
var minimap: Control
var is_started = false
var shown = true
var toast_time = 0.0
var address_locator
var vehicle: Node3D
var medium_font: FontVariation
var help_details: VBoxContainer
var controls_button: Button
var top_row: BoxContainer
var top_actions: HFlowContainer
var bottom_row: BoxContainer
var intro_row: BoxContainer

func style(color: Color = BG, radius: int = 8) -> StyleBoxFlat:
	var b = StyleBoxFlat.new()
	b.bg_color = color
	b.set_corner_radius_all(radius)
	b.content_margin_left = 16
	b.content_margin_right = 16
	b.content_margin_top = 10
	b.content_margin_bottom = 10
	b.set_border_width_all(1)
	b.border_color = Color(0.68,0.77,0.71,0.22)
	return b

func label(text: String, size: int, color: Color = INK) -> Label:
	var node = Label.new()
	node.text = text
	node.add_theme_font_size_override("font_size",size)
	if medium_font and size >= 14:
		node.add_theme_font_override("font",medium_font)
	node.add_theme_color_override("font_color",color)
	node.add_theme_color_override("font_shadow_color",Color(0,0,0,.28))
	node.add_theme_constant_override("shadow_offset_x",1)
	node.add_theme_constant_override("shadow_offset_y",1)
	return node

func button(text: String, callback: Callable, keyboard_focus: bool = false, accent: bool = false) -> Button:
	var node = Button.new()
	node.text = text
	node.focus_mode = Control.FOCUS_ALL if keyboard_focus else Control.FOCUS_NONE
	node.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	var normal_color = Color(.12,.18,.18,.84) if not accent else Color(.68,.77,.71,.96)
	var hover_color = Color(.22,.31,.29,.96) if not accent else Color(.78,.86,.79,1.0)
	var pressed_color = Color(.31,.43,.37,1.0) if not accent else Color(.61,.73,.65,1.0)
	node.add_theme_stylebox_override("normal",style(normal_color,7))
	node.add_theme_stylebox_override("hover",style(hover_color,7))
	node.add_theme_stylebox_override("pressed",style(pressed_color,7))
	node.add_theme_stylebox_override("disabled",style(Color(.12,.17,.17,.54),7))
	var focus_box = style(hover_color,7)
	focus_box.border_color = SAGE
	focus_box.set_border_width_all(2)
	node.add_theme_stylebox_override("focus",focus_box)
	node.add_theme_color_override("font_color",CHARCOAL if accent else INK)
	node.add_theme_color_override("font_hover_color",CHARCOAL if accent else INK)
	node.add_theme_color_override("font_pressed_color",CHARCOAL if accent else INK)
	node.add_theme_color_override("font_focus_color",CHARCOAL if accent else INK)
	node.add_theme_color_override("font_disabled_color",MUTED)
	node.add_theme_font_size_override("font_size",13)
	if medium_font: node.add_theme_font_override("font",medium_font)
	node.pressed.connect(callback)
	return node

func _ready():
	# The browser keeps the pointer visible so inspection gestures and compact
	# utility controls feel like one coherent interface.
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	address_locator = preload("res://scripts/address_locator.gd").new()
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
	var ui_font = preload("res://assets/fonts/InterVariable.ttf")
	var ui_theme = Theme.new()
	ui_theme.default_font = ui_font
	root.theme = ui_theme
	medium_font = FontVariation.new()
	medium_font.base_font = ui_font
	medium_font.variation_opentype = {"wght":550}

	build_top()
	build_bottom()
	build_intro()
	build_pause()
	# Keep the brand/location rail present while the neighborhood warms up.
	top.show()
	bottom.hide()
	root.resized.connect(layout_for_viewport)
	layout_for_viewport()

func layout_for_viewport():
	if root.size.x < 1: return
	var narrow = root.size.x < 680
	var margin = 16 if narrow else 24
	top_row.vertical = narrow
	bottom_row.vertical = narrow
	intro_row.vertical = narrow
	intro_row.add_theme_constant_override("separation",12 if narrow else 20)
	var action_width = 0.0
	for action in top_actions.get_children():
		if action.visible:
			action_width += action.get_combined_minimum_size().x + 5
	top_actions.custom_minimum_size.x = 0 if narrow else maxf(0,action_width-5)
	for rail in [top,bottom]:
		rail.add_theme_constant_override("margin_left",margin)
		rail.add_theme_constant_override("margin_right",margin)
	var launch_width = minf(640,root.size.x-margin*2)
	intro.offset_left = -launch_width*.5
	intro.offset_right = launch_width*.5
	intro.offset_top = -218 if narrow else -148
	intro.offset_bottom = -22
	# The route label/speed/address remain visible in narrow windows; the map
	# drawing yields space to the scene and the driving actions.
	minimap.visible = not narrow
	if pause_panel.visible: call_deferred("center_pause")

func build_top():
	top = MarginContainer.new()
	top.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	top.add_theme_constant_override("margin_left",24)
	top.add_theme_constant_override("margin_right",24)
	top.add_theme_constant_override("margin_top",20)
	top.add_theme_constant_override("margin_bottom",0)
	root.add_child(top)
	var row = BoxContainer.new()
	top_row = row
	row.add_theme_constant_override("separation",16)
	top.add_child(row)
	var brand = HBoxContainer.new()
	brand.add_theme_constant_override("separation",10)
	brand.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(brand)
	var logo = TextureRect.new()
	logo.texture = preload("res://assets/brand/drivearound-logo.png")
	logo.custom_minimum_size = Vector2(34,34)
	logo.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	logo.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	logo.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	logo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	brand.add_child(logo)
	var identity = VBoxContainer.new()
	identity.add_theme_constant_override("separation",1)
	identity.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	identity.alignment = BoxContainer.ALIGNMENT_CENTER
	brand.add_child(identity)
	identity.add_child(label("DriveAround.nyc",16,INK))
	mood_label = label("EAST VILLAGE  /  NEW YORK",10,MUTED)
	identity.add_child(mood_label)

	var actions = HFlowContainer.new()
	top_actions = actions
	actions.add_theme_constant_override("h_separation",5)
	actions.add_theme_constant_override("v_separation",5)
	row.add_child(actions)
	var names = ["Golden","Dusk","Rain"]
	for i in range(3):
		var weather = button(names[i],func(): weather_requested.emit(i))
		weather.add_theme_font_size_override("font_size",11)
		actions.add_child(weather)
		weather_buttons.append(weather)
	audio_button = button("Sound off",func(): audio_requested.emit())
	audio_button.add_theme_font_size_override("font_size",11)
	actions.add_child(audio_button)
	pause_button = button("Pause",func(): pause_requested.emit())
	pause_button.add_theme_font_size_override("font_size",11)
	actions.add_child(pause_button)
	pause_button.hide()

func build_bottom():
	bottom = MarginContainer.new()
	bottom.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
	bottom.grow_vertical = Control.GROW_DIRECTION_BEGIN
	bottom.add_theme_constant_override("margin_left",24)
	bottom.add_theme_constant_override("margin_right",24)
	bottom.add_theme_constant_override("margin_bottom",20)
	root.add_child(bottom)
	var lower = BoxContainer.new()
	bottom_row = lower
	lower.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	lower.add_theme_constant_override("separation",12)
	bottom.add_child(lower)

	var speed_panel = PanelContainer.new()
	speed_panel.custom_minimum_size = Vector2(232,0)
	speed_panel.add_theme_stylebox_override("panel",style(Color(.075,.12,.12,.90),8))
	lower.add_child(speed_panel)
	var instrument = VBoxContainer.new()
	instrument.add_theme_constant_override("separation",6)
	speed_panel.add_child(instrument)
	var map_header = HBoxContainer.new()
	map_header.add_child(label("EAST 7TH ST",10,MUTED))
	var map_spacer = Control.new()
	map_spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	map_header.add_child(map_spacer)
	map_header.add_child(label("NORTH  ↑",9,MUTED))
	instrument.add_child(map_header)
	minimap = preload("res://scripts/minimap.gd").new()
	minimap.custom_minimum_size = Vector2(198,78)
	instrument.add_child(minimap)
	var numbers = HBoxContainer.new()
	numbers.add_theme_constant_override("separation",8)
	instrument.add_child(numbers)
	speed_label = label("00",31,INK)
	speed_label.custom_minimum_size.x = 50
	numbers.add_child(speed_label)
	var units = VBoxContainer.new()
	units.alignment = BoxContainer.ALIGNMENT_CENTER
	numbers.add_child(units)
	units.add_child(label("MPH",10,MUTED))
	distance_label = label("JUST WANDER",9,MUTED)
	units.add_child(distance_label)
	address_label = label("",9,SAGE)
	address_label.custom_minimum_size = Vector2(130,0)
	address_label.visible = false
	units.add_child(address_label)
	drivetrain_label = label("D1  ·  850 RPM",9,MUTED)
	instrument.add_child(drivetrain_label)

	var breathing_room = Control.new()
	breathing_room.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	lower.add_child(breathing_room)
	var controls = VBoxContainer.new()
	controls.alignment = BoxContainer.ALIGNMENT_END
	controls.add_theme_constant_override("separation",6)
	lower.add_child(controls)
	status_label = label("",12,INK)
	status_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	controls.add_child(status_label)
	var hint = label("WASD to drive  ·  Esc for controls",11,MUTED)
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	controls.add_child(hint)
	var actions = HBoxContainer.new()
	actions.alignment = BoxContainer.ALIGNMENT_END
	actions.add_theme_constant_override("separation",6)
	controls.add_child(actions)
	camera_button = button("Camera  /  Chase",func(): camera_requested.emit())
	actions.add_child(camera_button)
	actions.add_child(button("Postcard  ·  P",func(): photo_requested.emit()))

func build_intro():
	intro = PanelContainer.new()
	intro.anchor_left = .5
	intro.anchor_right = .5
	intro.anchor_top = 1.0
	intro.anchor_bottom = 1.0
	intro.offset_left = -320
	intro.offset_right = 320
	intro.offset_top = -148
	intro.offset_bottom = -22
	intro.grow_horizontal = Control.GROW_DIRECTION_BOTH
	intro.grow_vertical = Control.GROW_DIRECTION_BEGIN
	intro.add_theme_stylebox_override("panel",style(Color(.075,.12,.13,.94),10))
	root.add_child(intro)
	var row = BoxContainer.new()
	intro_row = row
	row.add_theme_constant_override("separation",20)
	intro.add_child(row)
	var copy = VBoxContainer.new()
	copy.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	copy.alignment = BoxContainer.ALIGNMENT_CENTER
	copy.add_theme_constant_override("separation",3)
	row.add_child(copy)
	copy.add_child(label("EAST VILLAGE  /  NEW YORK",10,SAGE))
	intro_title = label("Seventh, slowly.",27,INK)
	copy.add_child(intro_title)
	copy.add_child(label("New York, at your own pace.",14,MUTED))
	loading_label = label("Opening the neighborhood…",10,MUTED)
	copy.add_child(loading_label)
	var action = VBoxContainer.new()
	action.custom_minimum_size = Vector2(190,0)
	action.alignment = BoxContainer.ALIGNMENT_CENTER
	action.add_theme_constant_override("separation",6)
	row.add_child(action)
	start_button = button("Start driving  →",func(): start_requested.emit(),true,true)
	start_button.custom_minimum_size = Vector2(190,42)
	start_button.add_theme_font_size_override("font_size",14)
	start_button.disabled = true
	action.add_child(start_button)
	var enter_hint = label("ENTER to begin",9,MUTED)
	enter_hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	action.add_child(enter_hint)

func build_pause():
	pause_panel = PanelContainer.new()
	pause_panel.anchor_left = .5
	pause_panel.anchor_right = .5
	pause_panel.anchor_top = .5
	pause_panel.anchor_bottom = .5
	pause_panel.offset_left = -180
	pause_panel.offset_right = 180
	pause_panel.offset_top = -126
	pause_panel.offset_bottom = 126
	pause_panel.grow_horizontal = Control.GROW_DIRECTION_BOTH
	pause_panel.grow_vertical = Control.GROW_DIRECTION_BOTH
	pause_panel.add_theme_stylebox_override("panel",style(Color(.075,.12,.13,.97),10))
	root.add_child(pause_panel)
	var box = VBoxContainer.new()
	box.add_theme_constant_override("separation",8)
	pause_panel.add_child(box)
	box.add_child(label("DriveAround.nyc",11,SAGE))
	box.add_child(label("Paused",25,INK))
	box.add_child(label("Take your time.",12,MUTED))
	pause_resume_button = button("Back to the drive",func(): pause_requested.emit(),true,true)
	pause_resume_button.custom_minimum_size.y = 36
	box.add_child(pause_resume_button)
	var reset = button("Return to First & Seventh",func(): reset_requested.emit(),true)
	reset.custom_minimum_size.y = 34
	box.add_child(reset)
	var fullscreen = button("Fullscreen",toggle_fullscreen,true)
	fullscreen.custom_minimum_size.y = 34
	box.add_child(fullscreen)
	controls_button = button("Controls  +",toggle_controls,true)
	box.add_child(controls_button)
	help_details = VBoxContainer.new()
	help_details.add_theme_constant_override("separation",5)
	box.add_child(help_details)
	for line in ["WASD / arrows   Drive, brake & reverse", "Space   Handbrake / drift", "C   Camera view    ·    V   Recenter camera", "Right-drag   Look around", "Shift + right-drag / middle-drag   Pan", "Scroll   Zoom    ·    R   Reset car", "T   Weather    ·    M   Sound", "P   Postcard    ·    H   Hide interface"]:
		help_details.add_child(label(line,11,MUTED))
	help_details.hide()
	pause_panel.hide()

func toggle_controls():
	help_details.visible = not help_details.visible
	controls_button.text = "Controls  −" if help_details.visible else "Controls  +"
	# Panel minimum size changes with the disclosure; recenter after layout.
	call_deferred("center_pause")

func center_pause():
	pause_panel.reset_size()
	pause_panel.position = (root.size - pause_panel.size) * .5

func toggle_fullscreen():
	var fullscreen_mode = DisplayServer.window_get_mode()==DisplayServer.WINDOW_MODE_FULLSCREEN
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED if fullscreen_mode else DisplayServer.WINDOW_MODE_FULLSCREEN)

func loaded(ok: bool):
	loading_label.text = "WASD or arrow keys to drive." if ok else "A neighborhood file is missing. Reload to try again."
	start_button.disabled = not ok
	if ok:
		start_button.call_deferred("grab_focus")

func begin():
	is_started = true
	intro.hide()
	start_button.release_focus()
	pause_button.show()
	layout_for_viewport()
	top.show()
	bottom.show()

func set_progress(value: float):
	loading_label.text = "Opening the neighborhood  ·  %d%%" % roundi(value*100)

func set_paused(value: bool):
	pause_panel.visible = value
	if value:
		call_deferred("center_pause")
		pause_resume_button.call_deferred("grab_focus")
	else:
		pause_resume_button.release_focus()
		help_details.hide()
		controls_button.text = "Controls  +"

func toggle_interface():
	shown = not shown
	top.visible = shown
	bottom.visible = shown and is_started

func toast(message: String):
	status_label.text = message
	toast_time = 4.0

func update_drivetrain(handling, handbrake: bool):
	var gear = "R" if handling.speed<-.3 else "D%d" % handling.gear
	var slide = "  ·  SLIDING" if absf(handling.slip)>.23 and absf(handling.speed)>4 else "  ·  HANDBRAKE" if handbrake else ""
	drivetrain_label.text = "%s  ·  %d RPM%s" % [gear,roundi(handling.rpm/50)*50,slide]
	drivetrain_label.modulate = WARM if not slide.is_empty() else Color.WHITE

func update_display(speed: float, distance: float, camera_name: String, weather_name: String, mood: int, dt: float):
	speed_label.text = "%02d" % roundi(abs(speed)*2.23694)
	distance_label.text = "%03d M  WANDERED" % roundi(distance)
	update_address()
	camera_button.text = "Camera  /  %s" % camera_name
	mood_label.text = "EAST VILLAGE  /  "+weather_name.to_upper()
	for i in weather_buttons.size():
		weather_buttons[i].modulate = SAGE if i==mood else Color(.70,.76,.73)
	if toast_time > 0:
		toast_time -= dt
		if toast_time <= 0: status_label.text = ""

func update_address():
	if not is_instance_valid(vehicle): return
	var address = address_locator.sample(vehicle.global_position,vehicle.rotation.y)
	address_label.text = address
	address_label.visible = not address.is_empty()

func address_state() -> Dictionary:
	return {"address":address_label.text if address_label.visible else "","addressId":address_locator.active_id,"addressVisible":address_label.visible}
