extends Node
## EV-002: imported-scene residency; the current street/prop owner stays shared.
const RETAIN = 445.0
const EVICT = 475.0
const NETWORK_SLOTS = 2
const OPENING_NETWORK_SLOTS = 16
const STAGING_LIMIT = 32*1024*1024
const SCENE_LIMIT = 8*1024*1024
var world
var manifest: Dictionary = {}
var records: Dictionary = {}
var ordered: Array = []
var jobs: Dictionary = {}
var cache_dir = ""
var origin = "http://127.0.0.1:5173"
var configured = false
var opening = true
var west_wanted = true
var outside_seconds = 0.0
var last_distance = INF
var generation = 0
var staged_bytes = 0
var max_staged_bytes = 0
var max_requests = 0
var max_reserved_bytes = 0
var downloaded_bytes = 0
var retirements = 0
var activations = 0
var cancellations = 0
var retries = 0
var hold_count = 0
var held = false
var camera_held = false
var resize_pending = false
var last_error = ""
var events: Array = []
var retired_refs: Array = []
var max_decode_ms = 0.0
var max_activate_ms = 0.0
var measured_request_ms = 0.0

func event(kind: String, key: String = "", extra: Dictionary = {}):
	var record = {"ms":Time.get_ticks_msec(),"kind":kind,"id":key,"generation":generation}
	record.merge(extra)
	events.append(record)
	if events.size()>2000: events.pop_front()

func open(data: Dictionary) -> bool:
	var parsed = JSON.parse_string(FileAccess.get_file_as_string("res://assets/area_manifest.json"))
	if not parsed is Dictionary or parsed.get("schema")!=1 or parsed.get("engine")!="4.7.2": return false
	manifest = parsed
	if manifest.assets.size()!=data.buildings.size(): return false
	if OS.has_feature("web"): origin = str(JavaScriptBridge.eval("window.location.origin"))
	cache_dir = OS.get_cache_dir().path_join("drivearound/"+str(manifest.release))
	if DirAccess.make_dir_recursive_absolute(cache_dir)!=OK: return false
	var entries = data.buildings.duplicate()
	entries.sort_custom(func(a,b): return Vector2(a.position[0],a.position[2]).length_squared()<Vector2(b.position[0],b.position[2]).length_squared())
	for b in entries:
		var key = str(int(b.id))
		if not manifest.assets.has(key): return false
		var a: Dictionary = manifest.assets[key]
		if a.glbSha256!=b.sha256 or a.bytes<=0 or a.bytes>SCENE_LIMIT: return false
		if a.url!="/seventh/areas/assets/"+str(a.sha256)+".scn" or str(a.sha256).length()!=64: return false
		if a.owner not in ["EVP-WEST","EVP-REST"] or not key in manifest.areas[a.owner]: return false
		records[key] = {"asset":a,"building":b,"state":"absent","token":0,"attempts":0,"retryAt":0,"refs":[]}
		ordered.append(key)
	configured = true
	while world.building_roots.size()<records.size():
		if terminal_failure():
			world.failed_assets.append(last_error)
			return false
		world.progress.emit(float(world.building_roots.size())/records.size())
		await get_tree().process_frame
	opening = false
	event("opening-ready")
	return true

func desired(key: String) -> bool:
	return records[key].asset.owner=="EVP-REST" or west_wanted

func reserved_bytes() -> int:
	var total = staged_bytes
	for key in jobs: total += int(records[key].asset.bytes)
	return total

func _process(_dt):
	if not configured: return
	# Gameplay decodes one scene per frame. The opening overlay can batch up
	# to three small scenes, stopping after a 3 ms soft budget (a single load
	# cannot be preempted). Two requests remain the gameplay limit.
	var began = Time.get_ticks_usec()
	var loaded = 0
	for key in ordered:
		if records[key].state=="verified" and desired(key):
			activate(key)
			loaded += 1
			if loaded>=(3 if opening else 1) or Time.get_ticks_usec()-began>=3000: break
	for key in ordered:
		if jobs.size()>=(OPENING_NETWORK_SLOTS if opening else NETWORK_SLOTS): break
		var r: Dictionary = records[key]
		if not desired(key) or r.state not in ["absent","failed"]: continue
		if r.attempts>=3 or Time.get_ticks_msec()<int(r.retryAt): continue
		if reserved_bytes()+int(r.asset.bytes)>STAGING_LIMIT: continue
		request(key)
	max_requests = maxi(max_requests,jobs.size())
	max_reserved_bytes = maxi(max_reserved_bytes,reserved_bytes())

func request(key: String):
	var r: Dictionary = records[key]
	r.token += 1
	r.attempts += 1
	r.state = "fetching"
	var http = HTTPRequest.new()
	http.use_threads = false
	http.max_redirects = 0
	http.timeout = 20.0
	http.body_size_limit = int(r.asset.bytes)
	http.download_chunk_size = 1024*1024
	# 4.7.2's EOF/disconnected completion deletes download_file before the
	# web callback. Receive the bounded body, then own its temporary file.
	var temporary = cache_dir.path_join(str(r.asset.sha256)+"-"+str(r.token)+".part")
	add_child(http)
	jobs[key] = {"http":http,"token":r.token,"file":temporary,"started":Time.get_ticks_msec()}
	http.request_completed.connect(completed.bind(key,int(r.token)),CONNECT_ONE_SHOT)
	event("request",key,{"attempt":r.attempts})
	# An old-release 404 may have inherited an immutable host header. Explicit
	# retry revalidates instead of trusting a negatively cached response.
	var headers = PackedStringArray(["Cache-Control: no-cache"]) if r.attempts>1 or retries>0 else PackedStringArray()
	var result = http.request(origin+str(r.asset.url),headers)
	if result!=OK: fail(key,"request "+str(result))

func completed(result: int, code: int, _headers: PackedStringArray, _body: PackedByteArray, key: String, token: int):
	if not jobs.has(key) or int(jobs[key].token)!=token: return
	var job: Dictionary = jobs[key]
	var r: Dictionary = records[key]
	if result!=HTTPRequest.RESULT_SUCCESS or code!=200:
		fail(key,"HTTP "+str(code)+" / "+str(result))
		return
	var began = Time.get_ticks_usec()
	if _body.size()!=int(r.asset.bytes):
		fail(key,"asset integrity mismatch: response length")
		return
	var destination = FileAccess.open(job.file,FileAccess.WRITE)
	if destination==null:
		fail(key,"cache write failed")
		return
	destination.store_buffer(_body)
	destination.close()
	var file = FileAccess.open(job.file,FileAccess.READ)
	var size = file.get_length() if file else -1
	if file: file.close()
	var actual_hash = FileAccess.get_sha256(job.file)
	if size!=int(r.asset.bytes) or actual_hash!=r.asset.sha256:
		fail(key,"asset integrity mismatch: bytes="+str(size)+" expected="+str(int(r.asset.bytes))+" hash="+actual_hash+" body="+str(_body.size()))
		return
	var target = cache_dir.path_join(str(r.asset.sha256)+".scn")
	if DirAccess.rename_absolute(job.file,target)!=OK:
		fail(key,"cache rename failed")
		return
	job.http.queue_free()
	jobs.erase(key)
	r.state = "verified"
	r.file = target
	staged_bytes += int(r.asset.bytes)
	downloaded_bytes += int(r.asset.bytes)
	max_staged_bytes = maxi(max_staged_bytes,staged_bytes)
	var elapsed = Time.get_ticks_msec()-int(job.started)
	measured_request_ms = maxf(measured_request_ms,float(elapsed))
	event("verified",key,{"requestMs":elapsed,"verifyMs":(Time.get_ticks_usec()-began)/1000.0,"bytes":size})

func fail(key: String, reason: String):
	var r: Dictionary = records[key]
	if jobs.has(key):
		var job: Dictionary = jobs[key]
		job.http.cancel_request()
		job.http.queue_free()
		DirAccess.remove_absolute(job.file)
		jobs.erase(key)
	r.state = "failed"
	r.retryAt = Time.get_ticks_msec()+1500
	last_error = key+": "+reason
	event("failed",key,{"reason":reason,"attempt":r.attempts})
	print("SEVENTH_ASSET_FAILURE ",key," ",reason)

func mesh_refs(node: Node, result: Array):
	if node is MeshInstance3D: result.append(weakref(node.mesh))
	for child in node.get_children(): mesh_refs(child,result)

func activate(key: String):
	var r: Dictionary = records[key]
	r.state = "staging"
	var began = Time.get_ticks_usec()
	var scene = ResourceLoader.load(r.file,"PackedScene",ResourceLoader.CACHE_MODE_REUSE)
	var decode_ms = (Time.get_ticks_usec()-began)/1000.0
	DirAccess.remove_absolute(r.file)
	r.erase("file")
	staged_bytes -= int(r.asset.bytes)
	if not scene is PackedScene:
		fail(key,"compiled scene unavailable")
		return
	began = Time.get_ticks_usec()
	var owner: Node3D = world.activate_building(r.building,scene)
	r.refs = [weakref(scene)]
	mesh_refs(owner,r.refs)
	scene = null
	r.state = "active"
	r.attempts = 0
	activations += 1
	var activate_ms = (Time.get_ticks_usec()-began)/1000.0
	max_decode_ms = maxf(max_decode_ms,decode_ms)
	max_activate_ms = maxf(max_activate_ms,activate_ms)
	event("active",key,{"decodeMs":decode_ms,"activateMs":activate_ms})
	if opening and world.building_roots.size()%30==1: print("SEVENTH_BUILDINGS ",world.building_roots.size(),"/",records.size())

func distance_to_bounds(point: Vector3, bounds: Array) -> float:
	return Vector2(maxf(maxf(float(bounds[0])-point.x,0),point.x-float(bounds[3])),maxf(maxf(float(bounds[2])-point.z,0),point.z-float(bounds[5]))).length()

func west_distance(point: Vector3) -> float:
	var result = INF
	for key in manifest.areas["EVP-WEST"]: result = minf(result,distance_to_bounds(point,records[key].asset.bounds))
	return result

func west_ready() -> bool:
	for key in manifest.areas["EVP-WEST"]:
		if records[key].state!="active": return false
	return true

func ready_at(point: Vector3) -> bool:
	return west_distance(point)>RETAIN or west_ready()

func require_at(point: Vector3):
	if west_distance(point)<=RETAIN: west_wanted = true

func west_visible(camera: Camera3D) -> bool:
	var planes = camera.get_frustum()
	for key in manifest.areas["EVP-WEST"]:
		var bounds: Array = records[key].asset.bounds
		var outside = false
		for plane in planes:
			# The nearest box support point must be outside an outward-facing
			# plane to reject the entire box. An intersecting box stays pinned.
			var nearest = Vector3(bounds[0] if plane.normal.x>=0 else bounds[3],bounds[1] if plane.normal.y>=0 else bounds[4],bounds[2] if plane.normal.z>=0 else bounds[5])
			if plane.distance_to(nearest)>3.0:
				outside = true
				break
		if not outside: return true
	return false

func permit_camera(camera: Camera3D) -> bool:
	if west_ready():
		camera_held = false
		return true
	if west_visible(camera):
		west_wanted = true
		camera_held = true
		return false
	camera_held = false
	return true

func update_residency(point: Vector3, speed: float, dt: float, camera: Camera3D) -> bool:
	if opening or not configured: return false
	var distance = west_distance(point)
	var approaching = distance<last_distance-.001
	last_distance = distance
	# A measured-latency horizon plus room to stop before the full camera envelope.
	var lead = maxf(70.0,absf(speed)*(2.0+measured_request_ms*.006))
	if distance<=RETAIN or (approaching and distance<=RETAIN+lead): west_wanted = true
	if distance>EVICT and not approaching and not camera_held and not resize_pending and not west_visible(camera):
		outside_seconds += dt
		if outside_seconds>=3.0 and west_wanted: retire_west()
	else: outside_seconds = 0.0
	var needs_hold = (distance<=RETAIN+3.0 or camera_held or resize_pending) and not west_ready()
	if needs_hold and not held:
		hold_count += 1
		event("movement-hold")
	if held and not needs_hold: event("movement-resume")
	held = needs_hold
	return held

func retire_west():
	west_wanted = false
	generation += 1
	retired_refs.clear()
	for key in manifest.areas["EVP-WEST"]:
		var r: Dictionary = records[key]
		r.token += 1
		if jobs.has(key):
			var job: Dictionary = jobs[key]
			job.http.cancel_request()
			job.http.queue_free()
			DirAccess.remove_absolute(job.file)
			jobs.erase(key)
			cancellations += 1
		if r.has("file"):
			DirAccess.remove_absolute(r.file)
			r.erase("file")
			staged_bytes -= int(r.asset.bytes)
		retired_refs.append_array(r.refs)
		r.refs = []
		world.retire_building(key)
		r.state = "absent"
		r.attempts = 0
		r.retryAt = 0
	retirements += 1
	event("west-retired")

func retry_failed():
	for key in ordered:
		# Restart in-flight attempts as well: a response from the failed wave
		# must not exhaust its old retry budget after the user has pressed R.
		if jobs.has(key):
			var job: Dictionary = jobs[key]
			records[key].token += 1
			job.http.cancel_request()
			job.http.queue_free()
			DirAccess.remove_absolute(job.file)
			jobs.erase(key)
			records[key].state = "absent"
			cancellations += 1
		if records[key].state=="failed":
			records[key].state = "absent"
		if records[key].state=="absent":
			records[key].attempts = 0
			records[key].retryAt = 0
	last_error = ""
	retries += 1
	event("retry")

func terminal_failure() -> bool:
	for key in ordered:
		if desired(key) and records[key].state=="failed" and int(records[key].attempts)>=3: return true
	return false

func snapshot(verbose: bool = false) -> Dictionary:
	var live_refs = 0
	for reference in retired_refs:
		if reference.get_ref()!=null: live_refs += 1
	var result = {"catalogCount":records.size(),"residentCount":world.building_roots.size(),"residentIds":world.resident_owners.keys(),"westReady":west_ready(),"westWanted":west_wanted,"held":held,"holdCount":hold_count,"retirements":retirements,"activations":activations,"cancellations":cancellations,"retries":retries,"pendingRequests":jobs.size(),"maxRequests":max_requests,"stagedBytes":staged_bytes,"maxStagedBytes":max_staged_bytes,"maxReservedBytes":max_reserved_bytes,"downloadedBytes":downloaded_bytes,"retiredResourceRefsAlive":live_refs,"retiredResourceRefCount":retired_refs.size(),"generation":generation,"lastError":last_error,"maxDecodeMs":max_decode_ms,"maxActivateMs":max_activate_ms,"resourceCount":Performance.get_monitor(Performance.OBJECT_RESOURCE_COUNT),"nodeCount":Performance.get_monitor(Performance.OBJECT_NODE_COUNT),"renderBufferBytes":RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_BUFFER_MEM_USED),"renderTextureBytes":RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TEXTURE_MEM_USED),"cacheDirectory":cache_dir}
	result["terminalFailure"] = terminal_failure()
	result["cameraHeld"] = camera_held
	result["resizePending"] = resize_pending
	if verbose:
		result["events"] = events
		var owners: Dictionary = {}
		for child in world.get_children():
			if str(child.name).begins_with("Resident_"):
				var key = str(child.name).trim_prefix("Resident_")
				owners[key] = {"model":child.has_node("Building_"+key),"collision":child.has_node("Collision_"+key),"children":child.get_child_count()}
		result["treeOwners"] = owners
	return result

func _exit_tree():
	for key in jobs:
		jobs[key].http.cancel_request()
		DirAccess.remove_absolute(jobs[key].file)
	for key in records:
		if records[key].has("file"): DirAccess.remove_absolute(records[key].file)
