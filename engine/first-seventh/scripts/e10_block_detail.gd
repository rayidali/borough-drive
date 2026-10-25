extends RefCounted
## Tenth Second–Avenue A street owner. Approximate observed fixture positions.
const S = preload("res://scripts/shapes.gd")

func streets(world, voids: Array):
	var g = world.geometry
	var curb = S.material(Color("c8bdab"))
	# First connection and this block only; other avenue terminals stay bounded.
	for box in [[-17.0,17.0,-244.0,-171.0],[-217.0,-17.0,-244.0,-212.0],[17.0,211.0,-244.0,-212.0]]:
		world.rectilinear_plane_with_voids(box[0],box[1],box[2],box[3],-.22,.4,world.asphalt,voids,false)
		world.rectilinear_plane_with_voids(box[0],box[1],box[2],box[3],-.015,.025,world.asphalt,voids,false)
	# Horizontal collider triangles preserve the original -0.02 road level.
	# Box side walls at internal seams can catch the low car collision body.
	# Keep all cellar cuts, without adding a raised lip at the intersection.
	var running_surface = StaticBody3D.new()
	running_surface.name = "TenthContinuousRoadSurface"
	var running_shape = CollisionShape3D.new()
	var running_mesh = ConcavePolygonShape3D.new()
	var running_faces = PackedVector3Array()
	var road_rectangles = [[-217.0,211.0,-232.95,-223.05],[-10.75,10.75,-244.0,-232.95],[-10.75,10.75,-223.05,-171.0]]
	var floor_cuts = voids.duplicate()
	for box in road_rectangles:
		floor_cuts.append({"x0":box[0],"x1":box[1],"z0":box[2],"z1":box[3]})
		var x0=box[0];var x1=box[1];var z0=box[2];var z1=box[3]
		running_faces.append_array([Vector3(x0,-.02,z0),Vector3(x1,-.02,z1),Vector3(x1,-.02,z0),Vector3(x0,-.02,z0),Vector3(x0,-.02,z1),Vector3(x1,-.02,z1)])
	for box in [[-17.0,17.0,-244.0,-171.0],[-217.0,-17.0,-244.0,-212.0],[17.0,211.0,-244.0,-212.0]]:
		var xs: Array = [box[0],box[1]]; var zs: Array = [box[2],box[3]]
		for hole in floor_cuts:
			if hole.x1>box[0] and hole.x0<box[1] and hole.z1>box[2] and hole.z0<box[3]:
				xs.append(clamp(hole.x0,box[0],box[1]));xs.append(clamp(hole.x1,box[0],box[1]))
				zs.append(clamp(hole.z0,box[2],box[3]));zs.append(clamp(hole.z1,box[2],box[3]))
		xs.sort();zs.sort()
		for xi in xs.size()-1:
			for zi in zs.size()-1:
				var x0=float(xs[xi]);var x1=float(xs[xi+1]);var z0=float(zs[zi]);var z1=float(zs[zi+1])
				if x1-x0<.001 or z1-z0<.001 or world.rect_hits_void(x0,x1,z0,z1,floor_cuts):continue
				running_faces.append_array([Vector3(x0,-.02,z0),Vector3(x1,-.02,z1),Vector3(x1,-.02,z0),Vector3(x0,-.02,z0),Vector3(x0,-.02,z1),Vector3(x1,-.02,z1)])
	running_mesh.set_faces(running_faces)
	running_mesh.backface_collision = true
	running_shape.shape = running_mesh
	running_surface.add_child(running_shape)
	world.add_child(running_surface)
	for xs in [[-217.0,-10.75],[10.75,211.0]]:
		for zs in [[-244.0,-232.95],[-223.05,-212.0]]:
			world.rectilinear_plane_with_voids(xs[0],xs[1],zs[0],zs[1],.07,.14,world.sidewalk,voids,true)
	for xs in [[-17.0,-10.75],[10.75,17.0]]:
		world.rectilinear_plane_with_voids(xs[0],xs[1],-212,-171,.07,.14,world.sidewalk,voids,true)
	# Exact two assigned Second Avenue returns need pavement under their doors.
	# These curb-side strips do not add an avenue road or move its terminal.
	for ends in [[-244.960,-232.950],[-223.050,-198.605]]:
		world.rectilinear_plane_with_voids(-218.25,-212.80,ends[0],ends[1],.07,.14,world.sidewalk,voids,true)
		S.box(g,Vector3(-218.25,.112,(ends[0]+ends[1])*.5),Vector3(.18,.105,ends[1]-ends[0]),curb)
	for x in [-10.75,10.75]:
		for zs in [[-244.0,-232.95],[-223.05,-171.0]]:
			S.box(g,Vector3(x,.112,(zs[0]+zs[1])/2),Vector3(.18,.105,zs[1]-zs[0]),curb)
	for z in [-232.95,-223.05]:
		for xs in [[-217.0,-10.75],[10.75,211.0]]:S.box(g,Vector3((xs[0]+xs[1])*.5,.112,z),Vector3(xs[1]-xs[0],.105,.18),curb)
	for x in range(198,20,-12):S.box(g,Vector3(x,.006,-226),Vector3(4,.012,.085),world.road_paint)
	for x in range(-22,-211,-12):S.box(g,Vector3(x,.006,-226),Vector3(4,.012,.085),world.road_paint)
	for side in [-1,1]:
		for mark in range(-7,8):S.box(g,Vector3(mark*1.12,.008,-228+side*7.2),Vector3(.53,.015,2.6),world.road_paint)
	for mark in range(-3,4):
		for x in [-12.7,12.7]:S.box(g,Vector3(x,.01,-228+mark*1.17),Vector3(2.75,.014,.56),world.road_paint)
	var barrier = S.material(Color("8faaa0"))
	for x in [-213.0,207.0]:
		S.solid_box(world,Vector3(x,1,-228),Vector3(.4,2,9.9),null)
		for z in [-231.0,-228.0,-225.0]:
			S.box(g,Vector3(x,.65,z),Vector3(.20,.23,2.5),barrier)
			for dz in [-.95,.95]:S.box(g,Vector3(x,.34,z+dz),Vector3(.32,.70,.11),world.metal)
		world.boundary_sign(Vector3(x,1.4,-228),"SLOW STREETS",PI/2 if x<0 else -PI/2)
	for z in [-238.0,-218.0]:S.solid_box(world,Vector3(-117,10,z),Vector3(200,30,1),null)
	S.solid_box(world,Vector3(-217,10,-228),Vector3(1,30,20),null)
	for z in [-238.0,-218.0]:S.solid_box(world,Vector3(114,10,z),Vector3(194,30,1),null)
	S.solid_box(world,Vector3(211,10,-228),Vector3(1,30,20),null)
	# Pavement under the two assigned Avenue A returns, with the avenue still closed.
	for zs in [[-258.55,-232.95],[-223.05,-202.59]]:
		world.rectilinear_plane_with_voids(201.50,207.0,zs[0],zs[1],.07,.14,world.sidewalk,voids,true)
		S.box(g,Vector3(207.0,.112,(zs[0]+zs[1])*.5),Vector3(.18,.105,zs[1]-zs[0]),curb)

func dress(root: Node3D, detail, voids: Array = []):
	var saved=detail.rng.state
	var soil=S.material(Color("57543c"));var joint=S.material(Color("989587"));var iron=S.material(Color("4b5250"))
	# Source foliage obscures different facades; no repeated tree per parcel.
	for row in [[-181.0,-234.0,.67,205],[-153.0,-234.1,.58,211],[-116.0,-234.0,.53,221],[-73.0,-234.1,.62,233],[-160.0,-222.0,.57,208],[-138.0,-221.8,.58,214],[-109.0,-222.0,.54,220],[-82.0,-222.0,.54,228]]:
		detail.rng.seed=int(row[3]);var p=Vector3(row[0],0,row[1]);detail.tree(root,p,row[2],false)
		S.box(root,p+Vector3(0,.153,0),Vector3(1.10,.012,.95),soil)
		for x in [-.6,.6]:S.box(root,p+Vector3(x,.19,0),Vector3(.08,.08,1.10),joint)
	# Estimated positions from individually inspected September 2024 / July 2022 views.
	for row in [[62.5,-234.0,.53,253],[107.0,-234.1,.50,265],[139.5,-234.0,.57,273],[172.0,-234.0,.63,287],[66.0,-222.0,.53,256],[116.0,-221.9,.55,274],[147.0,-222.0,.54,280]]:
		detail.rng.seed=int(row[3]);var p=Vector3(row[0],0,row[1]);detail.tree(root,p,row[2],false)
		S.box(root,p+Vector3(0,.153,0),Vector3(1.05,.012,.94),soil)
	for x in [70.0,139.0,195.0]:S.cylinder(root,Vector3(x,.014,-228),.36,.018,iron,24)
	detail.rng.state=saved
	for x in range(-211,-18,3):
		for z in [-235.1,-220.7]:
			var segments = [[z-1.325,z+1.325]]
			for hole in voids:
				if x+.011<=hole.x0 or x-.011>=hole.x1:continue
				var retained=[]
				for interval in segments:
					if interval[1]<=hole.z0 or interval[0]>=hole.z1:retained.append(interval)
					else:
						if interval[0]<hole.z0:retained.append([interval[0],hole.z0])
						if interval[1]>hole.z1:retained.append([hole.z1,interval[1]])
				segments=retained
			for interval in segments:S.box(root,Vector3(x,.146,(interval[0]+interval[1])*.5),Vector3(.022,.008,interval[1]-interval[0]),joint)
	for x in [-191.0,-126.0,-65.0]:S.cylinder(root,Vector3(x,.014,-228),.38,.018,iron,24)
	# Single owner for the photographed Citi Bike docking line at the long corner.
	var blue=S.material(Color("326ba0"));var gray=S.material(Color("777c78"))
	for i in range(12):
		var x=-208.0+i*.70
		S.box(root,Vector3(x,.52,-232.4),Vector3(.16,.78,.32),gray)
		S.box(root,Vector3(x,.91,-232.4),Vector3(.19,.10,.35),blue)
	for x in [-203.0,-97.0]:
		S.cylinder(root,Vector3(x,1.75,-222.0),.025,3.2,gray,8)
		S.box(root,Vector3(x,2.70,-222.0),Vector3(.28,.40,.035),S.material(Color("ddd8c8")))
