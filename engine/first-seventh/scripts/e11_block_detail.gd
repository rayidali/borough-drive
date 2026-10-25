extends RefCounted
## Eleventh Second–First street owner. Approximate observed fixture positions.
const S = preload("res://scripts/shapes.gd")

func streets(world, voids: Array):
	var g = world.geometry
	var curb = S.material(Color("c8bdab"))
	#310's inward garage ramps: exclude the supporting sidewalk underlay from
	#their observed recesses. Building collision still bounds this interior.
	voids=voids.duplicate()
	for span in [[.025,.405],[.535,.87]]:
		voids.append({"x0":-141.689-14.561*span[1],"x1":-141.689-14.561*span[0],"z0":-294.99,"z1":-290.73})
	# First connection and this block only; other avenue terminals stay bounded.
	for box in [[-17.0,17.0,-320.3,-244.0],[-217.0,-17.0,-320.3,-288.3]]:
		world.rectilinear_plane_with_voids(box[0],box[1],box[2],box[3],-.22,.4,world.asphalt,voids,false)
		world.rectilinear_plane_with_voids(box[0],box[1],box[2],box[3],-.015,.025,world.asphalt,voids,false)
	# Horizontal collider triangles preserve the original -0.02 road level.
	# Box side walls at internal seams can catch the low car collision body.
	# Keep all cellar cuts, without adding a raised lip at the intersection.
	var running_surface = StaticBody3D.new()
	running_surface.name = "EleventhContinuousRoadSurface"
	var running_shape = CollisionShape3D.new()
	var running_mesh = ConcavePolygonShape3D.new()
	var running_faces = PackedVector3Array()
	var road_rectangles = [[-217.0,17.0,-309.25,-299.35],[-10.75,10.75,-320.3,-309.25],[-10.75,10.75,-299.35,-244.0]]
	var floor_cuts = voids.duplicate()
	for box in road_rectangles:
		floor_cuts.append({"x0":box[0],"x1":box[1],"z0":box[2],"z1":box[3]})
		var x0=box[0];var x1=box[1];var z0=box[2];var z1=box[3]
		running_faces.append_array([Vector3(x0,-.02,z0),Vector3(x1,-.02,z1),Vector3(x1,-.02,z0),Vector3(x0,-.02,z0),Vector3(x0,-.02,z1),Vector3(x1,-.02,z1)])
	for box in [[-17.0,17.0,-320.3,-244.0],[-217.0,-17.0,-320.3,-288.3]]:
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
	for xs in [[-217.0,-10.75],[10.75,17.0]]:
		for zs in [[-320.3,-309.25],[-299.35,-288.3]]:
			world.rectilinear_plane_with_voids(xs[0],xs[1],zs[0],zs[1],.07,.14,world.sidewalk,voids,true)
	for xs in [[-17.0,-10.75],[10.75,17.0]]:
		world.rectilinear_plane_with_voids(xs[0],xs[1],-288.3,-244,.07,.14,world.sidewalk,voids,true)
	# Exact two assigned Second Avenue returns need pavement under their doors.
	# These curb-side strips do not add an avenue road or move its terminal.
	for ends in [[-320.99,-309.25],[-299.35,-276.93]]:
		world.rectilinear_plane_with_voids(-218.25,-212.80,ends[0],ends[1],.07,.14,world.sidewalk,voids,true)
		S.box(g,Vector3(-218.25,.112,(ends[0]+ends[1])*.5),Vector3(.18,.105,ends[1]-ends[0]),curb)
	for x in [-10.75,10.75]:
		for zs in [[-320.3,-309.25],[-299.35,-244.0]]:
			S.box(g,Vector3(x,.112,(zs[0]+zs[1])/2),Vector3(.18,.105,zs[1]-zs[0]),curb)
	for z in [-309.25,-299.35]:
		for xs in [[-217.0,-10.75],[10.75,17.0]]:S.box(g,Vector3((xs[0]+xs[1])*.5,.112,z),Vector3(xs[1]-xs[0],.105,.18),curb)
	for x in range(-22,-211,-12):S.box(g,Vector3(x,.006,-302.3),Vector3(4,.012,.085),world.road_paint)
	for side in [-1,1]:
		for mark in range(-7,8):S.box(g,Vector3(mark*1.12,.008,-304.3+side*7.2),Vector3(.53,.015,2.6),world.road_paint)
	for mark in range(-3,4):
		for x in [-12.7,12.7]:S.box(g,Vector3(x,.01,-304.3+mark*1.17),Vector3(2.75,.014,.56),world.road_paint)
	var barrier = S.material(Color("8faaa0"))
	for x in [-213.0,13.0]:
		S.solid_box(world,Vector3(x,1,-304.3),Vector3(.4,2,9.9),null)
		for z in [-307.3,-304.3,-301.3]:
			S.box(g,Vector3(x,.65,z),Vector3(.20,.23,2.5),barrier)
			for dz in [-.95,.95]:S.box(g,Vector3(x,.34,z+dz),Vector3(.32,.70,.11),world.metal)
		world.boundary_sign(Vector3(x,1.4,-304.3),"SLOW STREETS",PI/2 if x<0 else -PI/2)
	for z in [-314.3,-294.3]:S.solid_box(world,Vector3(-117,10,z),Vector3(200,30,1),null)
	S.solid_box(world,Vector3(-217,10,-304.3),Vector3(1,30,20),null)
	# The assigned school return receives pavement, while First north stays closed.
	world.rectilinear_plane_with_voids(-18.95,-10.75,-375.12,-309.25,.07,.14,world.sidewalk,voids,true)

func rod(root: Node3D, a: Vector3, b: Vector3, radius: float, mat: Material):
	var delta=b-a
	var m=S.cylinder(root,(a+b)*.5,radius,delta.length(),mat,6)
	if abs(delta.normalized().dot(Vector3.UP))<.999:m.quaternion=Quaternion(Vector3.UP,delta.normalized())

func chain(root: Node3D, a: Vector3, b: Vector3, height: float, mat: Material, gate=false):
	var dir=(b-a).normalized();var length=a.distance_to(b)
	for y in [.18,height]:rod(root,a+Vector3.UP*y,b+Vector3.UP*y,.022,mat)
	for i in range(int(ceil(length/2.5))+1):
		var p=a.lerp(b,float(i)/ceil(length/2.5));rod(root,p,p+Vector3.UP*height,.027,mat)
	# Diamond mesh built from clipped diagonals; the volume behind remains open.
	for sense in [-1,1]:
		for i in range(-int(ceil(height/.10)),int(ceil((length+height)/.10))+1):
			var x0=i*.10;var lo=max(0.0,-x0 if sense>0 else x0-length);var hi=min(height,length-x0 if sense>0 else x0)
			if hi<=lo:continue
			var wire_start=a+dir*(x0+sense*lo)+Vector3.UP*lo
			var wire_end=a+dir*(x0+sense*hi)+Vector3.UP*hi
			rod(root,wire_start,wire_end,.008,mat)
	if gate:
		rod(root,a,b+Vector3.UP*height,.023,mat)
		rod(root,a+Vector3.UP*height,b,.023,mat)
		for p in [a,b]:S.cylinder(root,p+Vector3(0,.14,0),.10,.12,mat,12).rotation.x=PI/2

func bicycle(root: Node3D,p:Vector3,blue:Material,iron:Material):
	for z in [-.56,.56]:
		var wheel=TorusMesh.new();wheel.inner_radius=.26;wheel.outer_radius=.30;wheel.rings=16;wheel.ring_segments=6
		var m=S.mesh(root,p+Vector3(0,.47,z),wheel,iron);m.rotation.z=PI/2
	for pair in [[Vector3(0,.47,-.56),Vector3(0,.55,0)],[Vector3(0,.55,0),Vector3(0,1.,-.12)],[Vector3(0,1.,-.12),Vector3(0,.47,-.56)],[Vector3(0,1.,-.12),Vector3(0,.98,.43)],[Vector3(0,.55,0),Vector3(0,.98,.43)],[Vector3(0,.98,.43),Vector3(0,.47,.56)]]:rod(root,p+pair[0],p+pair[1],.023,blue)
	S.box(root,p+Vector3(0,1.04,-.13),Vector3(.22,.055,.30),iron)
	rod(root,p+Vector3(-.25,1.10,.43),p+Vector3(.25,1.10,.43),.018,iron)
	S.box(root,p+Vector3(0,.80,.61),Vector3(.37,.30,.30),blue)

func batch_site(root: Node3D):
	# Merge only this new site's static geometry; preserve all actual vertices,
	# transforms/materials. Prior building scenes and global batching are untouched.
	var groups={}
	for item in root.get_children():
		if not item is MeshInstance3D:continue
		var mat=item.material_override;var key=mat.get_instance_id()
		if not groups.has(key):
			var st=SurfaceTool.new();st.begin(Mesh.PRIMITIVE_TRIANGLES)
			groups[key]={"mat":mat,"tool":st,"items":[]}
		groups[key].tool.append_from(item.mesh,0,item.transform);groups[key].items.append(item)
	for group in groups.values():
		group.tool.index();S.mesh(root,Vector3.ZERO,group.tool.commit(),group.mat)
		for item in group.items:item.free()

func ground_arc(root:Node3D,center:Vector3,radius:float,start:float,span:float,mat:Material):
	for i in range(48):
		var aa=start+span*i/48.0;var bb=start+span*(i+1)/48.0
		rod(root,center+Vector3(cos(aa)*radius,0,sin(aa)*radius),center+Vector3(cos(bb)*radius,0,sin(bb)*radius),.028,mat)

func dress(root: Node3D,detail):
	var site=Node3D.new();site.name="EleventhObservedSites";root.add_child(site)
	var iron=S.material(Color("464a43"));var gray=S.material(Color("8a8d83"));var white=S.material(Color("d4d0b9"));var blue=S.material(Color("2d658d"));var green=S.material(Color("4b755e"));var soil=S.material(Color("58513d"));var red=S.material(Color("8b493c"))
	# Open324lot: actual street gap, caster gate and exposed neighboring walls.
	S.box(site,Vector3(-103.22,.05,-286.0),Vector3(7.94,.12,18.0),gray)
	chain(site,Vector3(-107.12,.17,-295.03),Vector3(-99.30,.17,-295.03),2.20,iron,true)
	for x in [-106.3,-100.1]:S.box(site,Vector3(x,1.62,-295.06),Vector3(.26,.37,.025),white)
	# Exposed322/326party walls remain their original owners, only lot objects here.
	for row in [[-104.8,-286.0,blue],[-101.2,-281.7,red]]:
		var p=Vector3(row[0],.65,row[1]);S.box(site,p,Vector3(1.65,.65,3.7),row[2]);S.box(site,p+Vector3(0,.48,.1),Vector3(1.4,.50,1.8),iron)
		for dx in [-.82,.82]:
			for dz in [-1.12,1.12]:
				var wheel=S.cylinder(site,p+Vector3(dx,-.18,dz),.32,.17,iron,16);wheel.rotation.z=PI/2
				var hub=S.cylinder(site,p+Vector3(dx*1.01,-.18,dz),.17,.19,gray,12);hub.rotation.z=PI/2
		for dx in [-.56,.56]:
			S.box(site,p+Vector3(dx,.05,-1.87),Vector3(.35,.14,.04),white)
			S.box(site,p+Vector3(dx,.05,1.87),Vector3(.30,.14,.04),red)
		S.box(site,p+Vector3(0,-.13,-1.88),Vector3(.45,.14,.04),white)
		S.box(site,p+Vector3(0,.36,-.82),Vector3(1.26,.34,.035),blue)
	# Ornate300–304passage gate and visible open floor; rear extent estimated.
	S.box(site,Vector3(-176.16,.08,-288.5),Vector3(3.1,.10,13.),gray)
	for x in [-177.68,-174.65]:rod(site,Vector3(x,.18,-294.96),Vector3(x,2.75,-294.96),.035,iron)
	for y in [.30,1.95,2.55]:rod(site,Vector3(-177.68,y,-294.96),Vector3(-174.65,y,-294.96),.025,iron)
	for i in range(20):
		var x=-177.68+i*3.03/19;rod(site,Vector3(x,.18,-294.96),Vector3(x,2.50,-294.96),.012,iron)
		var ring=TorusMesh.new();ring.inner_radius=.065;ring.outer_radius=.080;ring.rings=12;ring.ring_segments=5;S.mesh(site,Vector3(x,2.21,-294.96),ring,iron).rotation.x=PI/2
	# Schoolyard: blue basketball west, trees/bench strip, green soccer east.
	S.box(site,Vector3(-97.46,.06,-328.9),Vector3(55.2,.12,30.0),gray)
	S.box(site,Vector3(-113.1,.13,-329.0),Vector3(22.6,.025,26.),blue)
	S.box(site,Vector3(-83.0,.13,-329.0),Vector3(24.0,.025,26.),green)
	for x in [-124.0,-102.2,-94.0,-72.0]:S.box(site,Vector3(x,.148,-329.0),Vector3(.06,.01,25.0),white)
	for z in [-341.5,-316.5]:
		for edges in [[-124.0,-102.2],[-94.0,-72.0]]:S.box(site,Vector3((edges[0]+edges[1])*.5,.148,z),Vector3(edges[1]-edges[0],.01,.06),white)
	for row in [[-113.1,21.8],[-83.,22.]]:
		S.box(site,Vector3(row[0],.155,-329),Vector3(row[1],.012,.06),white)
		ground_arc(site,Vector3(row[0],.155,-329),2.3,0,TAU,white)
	for z in [-338.7,-319.3]:
		var sign_z=1.0 if z< -329 else -1.0
		rod(site,Vector3(-113.1,.17,z),Vector3(-113.1,3.65,z),.07,gray);S.box(site,Vector3(-113.1,3.25,z+sign_z*.35),Vector3(1.6,1.0,.09),white)
		var hoop=TorusMesh.new();hoop.inner_radius=.24;hoop.outer_radius=.27;hoop.rings=18;hoop.ring_segments=6;S.mesh(site,Vector3(-113.1,2.91,z+sign_z*.75),hoop,red)
		for x in [-115.1,-111.1]:S.box(site,Vector3(x,.155,z+sign_z*2.),Vector3(.06,.012,4.0),white)
		S.box(site,Vector3(-113.1,.155,z+sign_z*4.),Vector3(4.0,.012,.06),white)
		ground_arc(site,Vector3(-113.1,.155,z+sign_z*4.),2.,0,TAU,white)
	for z in [-340.9,-317.1]:
		for x in [-85.0,-81.0]:rod(site,Vector3(x,.17,z),Vector3(x,2.30,z),.04,white);rod(site,Vector3(x,2.30,z),Vector3(x,.17,z+(-1 if z< -330 else 1)),.03,white)
		rod(site,Vector3(-85,2.3,z),Vector3(-81,2.3,z),.04,white)
		for i in range(17):rod(site,Vector3(-85+i*.25,.17,z),Vector3(-85+i*.25,2.3,z),.005,white)
		for i in range(9):rod(site,Vector3(-85,.17+i*.25,z),Vector3(-81,.17+i*.25,z),.005,white)
	chain(site,Vector3(-125.09,.17,-313.34),Vector3(-72.0,.17,-314.58),2.65,iron)
	chain(site,Vector3(-72.0,.17,-314.58),Vector3(-69.82,.17,-314.63),2.65,iron,true)
	chain(site,Vector3(-125.09,.17,-313.34),Vector3(-125.09,.17,-344.0),2.65,iron)
	chain(site,Vector3(-125.09,.17,-344),Vector3(-69.82,.17,-344),2.65,iron)
	for z in [-319.0,-326.0,-336.0]:
		S.box(site,Vector3(-98,.58,z),Vector3(1.8,.09,.45),iron)
		for x in [-98.7,-97.3]:S.box(site,Vector3(x,.35,z),Vector3(.10,.50,.35),iron)
		S.box(site,Vector3(-98,.89,z-.20),Vector3(1.8,.50,.055),iron)
	var saved=detail.rng.state
	for row in [[-169.,-298.,.52,304],[-141.,-310.2,.60,311],[-116.,-298.,.57,318],[-86.,-298.,.62,328],[-63.,-298.,.54,334],[-43.,-310.1,.55,19],[-198.,-298.,.55,300],[-98.,-323.,.65,191],[-98.,-335.,.70,192]]:
		detail.rng.seed=int(row[3]);var p=Vector3(row[0],0,row[1]);detail.tree(site,p,row[2],false);S.box(site,p+Vector3(0,.153,0),Vector3(1.2,.012,1.1),soil)
	detail.rng.state=saved
	# Single CitiBike line below the school bands, clear of the running lane.
	for i in range(39):
		var x=-66.+i*1.05;S.box(site,Vector3(x,.55,-310.0),Vector3(.18,.80,.34),gray);S.box(site,Vector3(x,.97,-310.0),Vector3(.23,.09,.38),white)
		if i%5!=0:bicycle(site,Vector3(x,0,-311.1),blue,iron)
	S.box(site,Vector3(-24.0,1.1,-310.3),Vector3(.40,1.85,.27),iron);S.box(site,Vector3(-24.0,2.08,-310.3),Vector3(.65,.06,.48),blue).rotation.x=.25
	for x in [-190.,-132.,-62.]:S.cylinder(site,Vector3(x,.014,-304.3),.36,.018,iron,24)
	batch_site(site)
