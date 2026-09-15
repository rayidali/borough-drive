extends RefCounted
## Selects a mapped E 7th Street frontage for the driving HUD.
##
## This is deliberately a small, local locator.  It reads the same footprint
## records used by the world and only exposes addresses between Second and
## First Avenues while the vehicle is aligned with Seventh Street.

const SECOND_AVENUE_X = -229.0
const FIRST_AVENUE_X = 0.0
const RUNTIME_ORIGIN_Z = 228.0
const DISPLAY_MARGIN = 4.0
const KEEP_MARGIN = 9.0
const DISPLAY_LATERAL_LIMIT = 14.0
const KEEP_LATERAL_LIMIT = 17.0
const HEADING_LIMIT = 0.55
const KEEP_HEADING_LIMIT = 0.32
const SWITCH_ADVANTAGE = 2.5

var frontages: Array[Dictionary] = []
var active_id = 0

func _init():
	_load_frontages()

func _load_frontages():
	var file = FileAccess.open("res://assets/slice.json",FileAccess.READ)
	if file == null: return
	var parsed = JSON.parse_string(file.get_as_text())
	if not parsed is Dictionary: return
	# reviewFrontages stores the explicit source frontage line before the
	# runtime origin shift.  Keep the line's direction and endpoints here;
	# this also retains the two avenue-addressed corner properties whose E7
	# frontage is part of the driveable segment.
	for entry in parsed.get("reviewFrontages",[]):
		var frontage = entry.get("frontage",{})
		if frontage.is_empty(): continue
		var start = Vector2(float(frontage.get("x",0)),float(frontage.get("z",0))-RUNTIME_ORIGIN_Z)
		var direction = Vector2(float(frontage.get("rx",0)),float(frontage.get("rz",0)))
		var end = start+direction*float(frontage.get("length",0))
		var min_x = minf(start.x,end.x)
		var max_x = maxf(start.x,end.x)
		var frontage_z = (start.y+end.y)*.5
		if absf(frontage_z)>DISPLAY_LATERAL_LIMIT: continue
		# A frontage wholly beyond either avenue is boundary context, not
		# part of the bounded address display.
		if max_x < SECOND_AVENUE_X or min_x > FIRST_AVENUE_X: continue
		frontages.append({
			"id":int(entry.get("id",0)),
			"address":str(entry.get("address","")),
			"min_x":min_x,
			"max_x":max_x,
			"center_x":(min_x+max_x)*.5,
			"frontage_z":frontage_z,
			"side":1 if frontage_z > 0 else -1,
			"start":start,
			"end":end,
		})
	frontages.sort_custom(func(a,b): return a.center_x < b.center_x)

func _interval_distance(value: float, low: float, high: float) -> float:
	if value < low: return low-value
	if value > high: return value-high
	return 0.0

func _score(record: Dictionary, position: Vector3, side_hint: int) -> float:
	var along = _interval_distance(position.x,float(record.min_x),float(record.max_x))
	var lateral = absf(position.z-float(record.frontage_z))
	# At the road centre either wall is valid.  Once the car is close to a
	# wall, a small opposite-side penalty prevents labels jumping across it.
	var opposite_penalty = 3.0 if side_hint != 0 and int(record.side) != side_hint else 0.0
	return along + lateral*.32 + opposite_penalty

func _eligible(position: Vector3, heading: float, entering: bool) -> bool:
	# Enter after a 9 m avenue margin, but keep the current address until
	# within 4 m of that boundary.  Both thresholds remain inside this block.
	var margin = KEEP_MARGIN if entering else DISPLAY_MARGIN
	# Entry uses the visible display envelope; once an address is active, the
	# wider/slacker keep envelope prevents a wall-parallel drive from flickering.
	var lateral_limit = DISPLAY_LATERAL_LIMIT if entering else KEEP_LATERAL_LIMIT
	var heading_limit = HEADING_LIMIT if entering else KEEP_HEADING_LIMIT
	if position.x < SECOND_AVENUE_X+margin or position.x > FIRST_AVENUE_X-margin: return false
	if absf(position.z) > lateral_limit: return false
	# rotation.y=0 points down -Z; Seventh is the X axis.  The absolute
	# value also permits a controlled reverse manoeuvre without inventing
	# direction-specific address precision.
	if absf(sin(heading)) < heading_limit: return false
	return true

func _record_by_id(id: int):
	for record in frontages:
		if int(record.id) == id: return record
	return null

func _compact_address(address: String) -> String:
	return address.replace("East 7th Street","E 7TH ST").replace("2nd Avenue","2ND AVE").replace("1st Avenue","1ST AVE")

## Returns an empty string outside the bounded segment or while not travelling
## along Seventh.  Address changes retain the current frontage until the next
## mapped interval is clearly nearer, which keeps intersections and lane
## changes readable.
func sample(position: Vector3, heading: float) -> String:
	var keeping = active_id != 0 and _eligible(position,heading,false)
	if not keeping:
		active_id = 0
		if not _eligible(position,heading,true): return ""
	var side_hint = 1 if position.z > 2.0 else -1 if position.z < -2.0 else 0
	var best = null
	var best_score = INF
	for record in frontages:
		var score = _score(record,position,side_hint)
		if score < best_score:
			best_score = score
			best = record
	if best == null: return ""
	if active_id != 0:
		var current = _record_by_id(active_id)
		if current != null:
			var current_score = _score(current,position,side_hint)
			if current_score <= best_score+SWITCH_ADVANTAGE:
				return _compact_address(str(current.address))
	active_id = int(best.id)
	return _compact_address(str(best.address))
