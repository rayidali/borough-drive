extends SceneTree
## Runs the actual car and street/building colliders without loading render meshes.
func _initialize(): call_deferred("run")

func run():
	var world = preload("res://scripts/world.gd").new()
	root.add_child(world)
	world.data = preload("res://scripts/runtime_catalog.gd").with_protected_core(JSON.parse_string(FileAccess.get_file_as_string("res://assets/slice.json")))
	world.build_streets()
	for building in world.data.buildings: world.add_building_collision(building,world)
	var car = preload("res://scripts/car.gd").new()
	root.add_child(car)
	await physics_frame
	var results: Array = []
	var passed = true
	for route in [["first-north",0,-159,0,-291,-1,2],["first-south",0,-310,PI,-177,1,2],["eleventh-west",0,-304.3,PI/2,-182,-1,0],["eleventh-east",-202,-304.3,-PI/2,-12,1,0],["tenth-west",198,-228,PI/2,-172,-1,0],["tenth-east",-202,-228,-PI/2,184,1,0],["ninth-west",45,-154.7,PI/2,-45,-1,0],["ninth-east",-45,-154.7,-PI/2,45,1,0],["west-first-lane",-6,-160,0,-291,-1,2],["east-first-lane",6,-309,PI,-178,1,2]]:
		car.reset_car()
		car.position = Vector3(route[1],.12,route[2])
		car.rotation.y = route[3]
		car.enabled = true
		car.testing = true
		car.test_throttle = 0
		car.reset_physics_interpolation()
		for settle in 30:await physics_frame
		car.test_throttle = 1
		var initial_contacts = car.collision_count
		var hit_details: Array = []
		for i in 1500:
			await physics_frame
			for j in car.get_slide_collision_count():
				var hit = car.get_slide_collision(j)
				if abs(hit.get_normal().y)<.5 and hit_details.size()<8:
					hit_details.append({"body":str(hit.get_collider().get_path()),"position":str(hit.get_position()),"normal":str(hit.get_normal())})
			if route[5]*(car.position[route[6]]-route[4])>=0:break
		var reached = route[5]*(car.position[route[6]]-route[4])>=0
		car.test_throttle = -1
		for i in 300:
			await physics_frame
			if car.speed<.5:break
		car.test_throttle = 0
		var ok = reached and car.collision_count==initial_contacts
		passed = passed and ok
		var result = {"name":route[0],"position":[car.position.x,car.position.y,car.position.z],"reached":reached,"newContacts":car.collision_count-initial_contacts,"hitDetails":hit_details,"pass":ok}
		results.append(result)
		print("ELEVENTH_NATIVE_ROUTE ",JSON.stringify(result))
	var args=OS.get_cmdline_user_args()
	if args.size():
		var file=FileAccess.open(args[0],FileAccess.WRITE)
		file.store_string(JSON.stringify({"pass":passed,"routes":results,"scope":"Actual car, street and building colliders; native headless fixed physics step, no rendering or browser timing claims."},"\t")+"\n")
	quit(0 if passed else 1)
