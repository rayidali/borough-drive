extends SceneTree

# Build-time utility: preserve the installed engine's license and third-party
# notices verbatim alongside the browser binary. This scene is never launched.
func _initialize():
	var destination = ProjectSettings.globalize_path("res://../../dist/seventh/godot-notices.txt")
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--credits-out="): destination = argument.trim_prefix("--credits-out=")
	var file = FileAccess.open(destination,FileAccess.WRITE)
	if file == null:
		push_error("Cannot write engine license notices")
		quit(1)
		return
	file.store_string("GODOT ENGINE AND THIRD-PARTY NOTICES\n\n")
	file.store_string(Engine.get_license_text()+"\n\n")
	for record in Engine.get_copyright_info():
		file.store_string(record.name+"\n")
		for part in record.parts:
			file.store_string("License: "+part.license+"\n")
			for copyright in part.copyright: file.store_string(copyright+"\n")
		file.store_string("\n")
	for name in Engine.get_license_info():
		file.store_string("\n"+name+"\n\n"+Engine.get_license_info()[name]+"\n")
	file.close()
	print("SEVENTH_LICENSES_SAVED")
	quit()
