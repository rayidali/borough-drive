extends Node
## Spatial residency: startup and per-frame work depend on the local view, not city size.
const Index = preload("res://scripts/spatial_index.gd")
const NEAR = 150.0
const COLLISION_GUARD = 45.0
const RETIRE_AFTER_MS = 8000
const PREFETCH_MAX = 240.0
const NETWORK_SLOTS = 4
const OPENING_NETWORK_SLOTS = 16
const STAGING_LIMIT = 32*1024*1024
const SCENE_LIMIT = 8*1024*1024
# The full 204 Tenth corner retains its detail; aggregate staging stays 32 MiB.
const LARGE_SCENE_LIMIT = 16*1024*1024
var world
var manifest: Dictionary = {}
var records: Dictionary = {}
var ordered: Array = []
var jobs: Dictionary = {}
var cache_dir = ""
var origin = "http://127.0.0.1:5173"
var configured = false
var opening = true
var warming = true
var startup_resident_count = 0
var work_queue: Array = []
var queue_dirty = true
var queue_focus = Vector3.INF
var index = Index.new()
var wanted: Dictionary = {}
var opening_keys: Array = []
var focus = Vector3.ZERO
var refresh_seconds = 0.0
var eviction_seconds = 0.0
var initial_resident_count = 0
var peak_resident_count = 0
var peak_resident_bytes = 0
var resident_bytes = 0
var camera_keys: Array = []
var collision_keys: Array = []
var retire_queue: Array = []
var camera_signature: Array = []
var cached_camera_pose = Transform3D.IDENTITY
var cached_camera_extent = Vector3.ZERO
var view_queries = 0
var view_cache_hits = 0
var camera_touch_ms = 0
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
var resize_radius = 445.0
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
	var entries: Array = data.buildings.duplicate()
	entries.append_array(data.get("sharedModels",[]))
	if manifest.assets.size()!=entries.size(): return false
	if OS.has_feature("web"): origin = str(JavaScriptBridge.eval("window.location.origin"))
	cache_dir = OS.get_cache_dir().path_join("drivearound/"+str(manifest.release))
	if DirAccess.make_dir_recursive_absolute(cache_dir)!=OK: return false
	for b in entries:
		var key = str(int(b.id))
		if not manifest.assets.has(key): return false
		var a: Dictionary = manifest.assets[key]
		var scene_limit = LARGE_SCENE_LIMIT if key in ["247852693","248142953"] else SCENE_LIMIT
		if a.glbSha256!=b.sha256 or a.bytes<=0 or a.bytes>scene_limit: return false
		if a.url!="/seventh/areas/assets/"+str(a.sha256)+".scn" or str(a.sha256).length()!=64: return false
		if a.owner not in ["EVP-WEST","EVP-REST"] or not key in manifest.areas[a.owner]: return false
		records[key] = {"asset":a,"building":b,"state":"absent","token":0,"attempts":0,"retryAt":0,"refs":[],"lastWanted":0}
		ordered.append(key)
		index.insert(key,a.bounds)
	configured = true
	opening_keys = index.near(Vector3.ZERO,NEAR)
	want(opening_keys)
	while not keys_ready(opening_keys):
		if terminal_failure():
			world.failed_assets.append(last_error)
			return false
		world.progress.emit(float(world.building_roots.size())/maxi(1,opening_keys.size()))
		await get_tree().process_frame
	opening = false
	initial_resident_count = world.building_roots.size()
	event("opening-ready","",{"initialCount":initial_resident_count,"catalogCount":records.size()})
	return true

func want(keys: Array):
	var now = Time.get_ticks_msec()
	for key in keys:
		if not wanted.has(key): queue_dirty = true
		wanted[key] = true
		records[key].lastWanted = now

func finish_warming():
	warming = false
	startup_resident_count = world.building_roots.size()
	event("startup-ready","",{"residentCount":startup_resident_count,"residentBytes":resident_bytes})

func keys_ready(keys: Array) -> bool:
	for key in keys:
		if records[key].state!="active": return false
	return true

func desired(key: String) -> bool:
	return wanted.has(key)

func reserved_bytes() -> int:
	var total = staged_bytes
	for key in jobs: total += int(records[key].asset.bytes)
	return total

func _process(dt):
	if not configured: return
	# Static review cameras and paused views also retain their visible owners.
	if Time.get_ticks_msec()-camera_touch_ms>=100:
		want(camera_keys)
		camera_touch_ms = Time.get_ticks_msec()
	# Gameplay decodes one scene per frame. The opening overlay can batch up
	# to three small scenes, stopping after a 3 ms soft budget (a single load
	# cannot be preempted). Two requests remain the gameplay limit.
	var began = Time.get_ticks_usec()
	var loaded = 0
	if queue_dirty or focus.distance_squared_to(queue_focus)>36:
		work_queue = wanted.keys()
		work_queue.sort_custom(func(a,b): return Index.distance(focus,records[a].asset.bounds)<Index.distance(focus,records[b].asset.bounds))
		queue_dirty = false
		queue_focus = focus
	var queue: Array = work_queue
	for key in queue:
		if records[key].state=="verified" and desired(key):
			activate(key)
			loaded += 1
			if loaded>=(3 if warming else 1) or Time.get_ticks_usec()-began>=3000: break
	for key in queue:
		if jobs.size()>=(OPENING_NETWORK_SLOTS if warming else NETWORK_SLOTS): break
		var r: Dictionary = records[key]
		if not desired(key) or r.state not in ["absent","failed"]: continue
		if r.attempts>=3 or Time.get_ticks_msec()<int(r.retryAt): continue
		if reserved_bytes()+int(r.asset.bytes)>STAGING_LIMIT: continue
		request(key)
	eviction_seconds += dt
	if eviction_seconds>=.5 and not warming:
		eviction_seconds = 0
		var now = Time.get_ticks_msec()
		for key in wanted.keys():
			if now-int(records[key].lastWanted)>RETIRE_AFTER_MS:
				wanted.erase(key)
				queue_dirty = true
				if key not in retire_queue: retire_queue.append(key)
	# At most one complete model/collider owner retires per frame.
	if not retire_queue.is_empty():
		var key: String = retire_queue.pop_front()
		if not wanted.has(key): retire(key)
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
	resident_bytes += int(r.asset.bytes)
	peak_resident_count = maxi(peak_resident_count,world.building_roots.size())
	peak_resident_bytes = maxi(peak_resident_bytes,resident_bytes)
	var activate_ms = (Time.get_ticks_usec()-began)/1000.0
	max_decode_ms = maxf(max_decode_ms,decode_ms)
	max_activate_ms = maxf(max_activate_ms,activate_ms)
	event("active",key,{"decodeMs":decode_ms,"activateMs":activate_ms})
	if opening and world.building_roots.size()%30==1: print("SEVENTH_BUILDINGS ",world.building_roots.size(),"/",records.size())

func ready_at(point: Vector3) -> bool:
	return keys_ready(index.near(point,NEAR))

func require_at(point: Vector3):
	focus = point
	want(index.near(point,NEAR))

func permit_camera(camera: Camera3D) -> bool:
	var pose = camera.get_camera_transform()
	var half = camera.get_camera_projection().get_far_plane_half_extents()
	var extent = Vector3(half.x,half.y,camera.far)
	var signature: Array = [camera.projection,camera.keep_aspect,camera.frustum_offset]
	# The cached frustum has12 m of padding. Reuse it only while translation,
	# rotation and projection changes displace any corner by at most6 m.
	# This retains more than the4 m safety margin without city scans per frame.
	var angle = pose.basis.get_rotation_quaternion().angle_to(cached_camera_pose.basis.get_rotation_quaternion())
	var change = pose.origin.distance_to(cached_camera_pose.origin)+(maxf(extent.length(),cached_camera_extent.length())+12)*angle+extent.distance_to(cached_camera_extent)
	if signature!=camera_signature or change>6.0:
		camera_signature = signature
		cached_camera_pose = pose
		cached_camera_extent = extent
		camera_keys = index.in_view(camera,12.0)
		view_queries += 1
	else: view_cache_hits += 1
	want(camera_keys)
	camera_held = not keys_ready(camera_keys)
	return not camera_held

func prepare_camera(camera: Camera3D):
	while not permit_camera(camera):
		await get_tree().process_frame

func update_residency(point: Vector3, speed: float, dt: float, camera: Camera3D) -> bool:
	if opening or not configured: return false
	focus = point
	refresh_seconds -= dt
	if refresh_seconds<=0:
		refresh_seconds = .15
		# Keep a local neighborhood and prefetch a bounded latency/speed horizon.
		var lead = clampf(NEAR+absf(speed)*(2.0+measured_request_ms*.001),NEAR,PREFETCH_MAX)
		want(index.near(point,lead))
		# Prepare geometry before it enters the visible frustum, including the
		# far plane during forward travel. The safety guard still uses 4 m.
		var view_lead = clampf(25.0+absf(speed)*(2.0+measured_request_ms*.001),25.0,90.0)
		want(index.in_view(camera,view_lead))
		collision_keys = index.near(point,COLLISION_GUARD)
	# Pin the last complete rendered camera as well as any proposed new view.
	if camera_held: want(index.in_view(camera))
	else: want(camera_keys)
	var needs_hold = not keys_ready(collision_keys) or camera_held or resize_pending
	if needs_hold and not held:
		hold_count += 1
		event("movement-hold")
	if held and not needs_hold: event("movement-resume")
	held = needs_hold
	return held

func request_resize(point: Vector3, camera: Camera3D, dimensions: Vector2):
	resize_pending = true
	# The new aspect ratio is not installed yet. Prepare its entire possible
	# camera envelope, then let the normal frustum residency reclaim excess.
	var aspect = dimensions.x/maxf(1.0,dimensions.y)
	var projection = Projection.create_perspective(82.0,aspect,camera.near,camera.far,camera.keep_aspect==Camera3D.KEEP_WIDTH)
	var extent = projection.get_far_plane_half_extents()
	var current_extent = camera.get_camera_projection().get_far_plane_half_extents()
	# Inspection can reach65 m from the car; include the old view as well.
	resize_radius = maxf(Vector3(extent.x,extent.y,camera.far).length(),Vector3(current_extent.x,current_extent.y,camera.far).length())+75.0
	want(index.near(point,resize_radius))

func resize_ready(point: Vector3) -> bool:
	var keys = index.near(point,resize_radius)
	want(keys)
	return keys_ready(keys)

func retire(key: String):
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
	# Keep diagnostics bounded too; weak references never retain the model.
	while retired_refs.size()>4096: retired_refs.pop_front()
	r.refs = []
	if r.state=="active": resident_bytes -= int(r.asset.bytes)
	world.retire_building(key)
	r.state = "absent"
	r.attempts = 0
	r.retryAt = 0
	retirements += 1
	generation += 1
	event("retired",key)

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
	for key in wanted:
		if records[key].state=="failed" and int(records[key].attempts)>=3: return true
	return false

func snapshot(verbose: bool = false) -> Dictionary:
	var live_refs = 0
	for reference in retired_refs:
		if reference.get_ref()!=null: live_refs += 1
	var result = {"catalogCount":records.size(),"residentCount":world.building_roots.size(),"residentIds":world.resident_owners.keys(),"initialResidentCount":initial_resident_count,"startupResidentCount":startup_resident_count,"peakResidentCount":peak_resident_count,"residentBytes":resident_bytes,"peakResidentBytes":peak_resident_bytes,"wantedCount":wanted.size(),"spatialCells":index.cells.size(),"held":held,"holdCount":hold_count,"retirements":retirements,"activations":activations,"cancellations":cancellations,"retries":retries,"pendingRequests":jobs.size(),"maxRequests":max_requests,"stagedBytes":staged_bytes,"maxStagedBytes":max_staged_bytes,"maxReservedBytes":max_reserved_bytes,"downloadedBytes":downloaded_bytes,"retiredResourceRefsAlive":live_refs,"retiredResourceRefCount":retired_refs.size(),"generation":generation,"lastError":last_error,"maxDecodeMs":max_decode_ms,"maxActivateMs":max_activate_ms,"resourceCount":Performance.get_monitor(Performance.OBJECT_RESOURCE_COUNT),"nodeCount":Performance.get_monitor(Performance.OBJECT_NODE_COUNT),"renderBufferBytes":RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_BUFFER_MEM_USED),"renderTextureBytes":RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TEXTURE_MEM_USED),"cacheDirectory":cache_dir}
	result["terminalFailure"] = terminal_failure()
	result["cameraHeld"] = camera_held
	result["viewQueries"] = view_queries
	result["viewCacheHits"] = view_cache_hits
	result["viewIds"] = camera_keys
	result["collisionIds"] = collision_keys
	result["resizePending"] = resize_pending
	if verbose:
		result["events"] = events
		var owners: Dictionary = {}
		for child in world.get_children():
			if str(child.name).begins_with("Resident_"):
				var key = str(child.name).trim_prefix("Resident_")
				owners[key] = {"model":child.has_node("Building_"+key),"collision":child.has_node("Collision_"+key),"children":child.get_child_count(),"kind":child.get_meta("model_kind","authored-building")}
		result["treeOwners"] = owners
	result["protectedCore"] = world.data.get("protectedCore",{})
	return result

func _exit_tree():
	for key in jobs:
		jobs[key].http.cancel_request()
		DirAccess.remove_absolute(jobs[key].file)
	for key in records:
		if records[key].has("file"): DirAccess.remove_absolute(records[key].file)
