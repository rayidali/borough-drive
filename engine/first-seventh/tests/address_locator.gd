extends SceneTree

const Locator = preload("res://scripts/address_locator.gd")
var failures: Array[String] = []

func check(condition: bool, message: String):
	if not condition: failures.append(message)

func _initialize():
	var locator = Locator.new()
	check(locator.frontages.size() == 76,"Retain the 39 west-block and 37 east-block frontages, including corner properties")
	var records_by_address = {}
	for record in locator.frontages:
		records_by_address[record.address] = record
		check(float(record.start.x) != float(record.end.x),"Every scoped frontage must have a mapped along-street extent")
		check(absf(float(record.frontage_z)) >= 8.0 and absf(float(record.frontage_z)) <= 12.0,"Every scoped frontage must sit on an E7 wall")
		check(int(record.side) == (1 if float(record.frontage_z)>0 else -1),"Frontage side must follow its explicit runtime z")
	var positive_z_addresses = ["48 1/2 East 7th Street","50 East 7th Street","52 East 7th Street","54 East 7th Street","56 East 7th Street","58 East 7th Street","60 East 7th Street","62 East 7th Street","64 East 7th Street","66 East 7th Street","68 East 7th Street","70 East 7th Street","72 East 7th Street","74 East 7th Street","76 East 7th Street","80 East 7th Street","82 East 7th Street","84 East 7th Street","86 East 7th Street"]
	var negative_z_addresses = ["118 2nd Avenue","49 East 7th Street","51 East 7th Street","53 East 7th Street","55 East 7th Street","57 East 7th Street","59 East 7th Street","61 East 7th Street","63 East 7th Street","65 East 7th Street","67 East 7th Street","69 East 7th Street","71 East 7th Street","73-75 East 7th Street","77 East 7th Street","79 East 7th Street","81 East 7th Street","83 East 7th Street","85 East 7th Street","115 1st Avenue"]
	for address in positive_z_addresses:
		var positive_record = records_by_address.get(address)
		check(positive_record != null,"Missing scoped frontage "+address)
		if positive_record != null: check(int(positive_record.side)==1,address+" must use the positive-z wall")
	for address in negative_z_addresses:
		var negative_record = records_by_address.get(address)
		check(negative_record != null,"Missing scoped frontage "+address)
		if negative_record != null: check(int(negative_record.side)==-1,address+" must use the negative-z wall")
	var first = locator.sample(Vector3(-170,.15,0),-PI/2)
	check(first in ["49 E 7TH ST","50 E 7TH ST"],"A mapped frontage should be selected on E7")
	var held = locator.sample(Vector3(-169,.15,0),-PI/2)
	check(held == first,"A small movement should not flicker the active address")
	check(locator.sample(Vector3(-226,.15,0),-PI/2).is_empty(),"Release hysteresis should clear the address before Second Avenue")
	check(locator.sample(Vector3(-219,.15,0),-PI/2) == "118 2ND AVE","Entry hysteresis should begin inside the Second Avenue margin")
	check(locator.sample(Vector3(-2,.15,0),-PI/2).is_empty(),"The First Avenue boundary must hide the E7 address")
	check(locator.sample(Vector3(-170,.15,0),0).is_empty(),"An inner turn across E7 must not show an E7 address")
	check(locator.sample(Vector3(-170,.15,9),-PI/2) == "50 E 7TH ST","The north wall must select its explicit address")
	check(locator.sample(Vector3(-170,.15,-9),-PI/2) == "49 E 7TH ST","The south wall must select its explicit address")
	check(locator.sample(Vector3(-180,.15,9),-PI/2) == "48 1/2 E 7TH ST","The half-address must remain intact")
	check(locator.sample(Vector3(-75,.15,-9),-PI/2) == "73-75 E 7TH ST","The negative frontage ID must retain the 73-75 display")
	check(locator.sample(Vector3(-155,.15,9),-PI/2) == "54 E 7TH ST","Selection must advance after two frontage lots")
	check(locator.sample(Vector3(-210,.15,-9),-PI/2) == "118 2ND AVE","The Second Avenue corner frontage must be included")
	check(locator.sample(Vector3(-20,.15,-9),-PI/2) == "115 1ST AVE","The First Avenue corner frontage must be included")
	var lateral = Locator.new()
	var east = Locator.new()
	check(east.sample(Vector3(3,.15,0),-PI/2).is_empty(),"First Avenue intersection remains unlabeled from the east")
	check(east.sample(Vector3(39,.15,-9),-PI/2) == "93 E 7TH ST","East north frontage must be selectable")
	check(east.sample(Vector3(98,.15,-9),-PI/2) == "109 E 7TH ST","Correct the duplicate rectory address east of the church")
	check(east.sample(Vector3(130,.15,9),-PI/2) == "116 E 7TH ST","Formerly unnamed south parcel must have its observed address")
	check(east.sample(Vector3(113,.15,-9),-PI/2) == "111–115 E 7TH ST","McKinley address range remains intact")
	check(east.sample(Vector3(195,.15,-9),-PI/2) == "111 AVE A","Include the Seventh return of the Avenue A corner")
	check(east.sample(Vector3(212,.15,0),-PI/2).is_empty(),"Release the address before Avenue A")
	check(east.sample(Vector3(237,.15,-9),-PI/2).is_empty(),"Do not expand the locator east of Avenue A")
	check(east.sample(Vector3(110,.15,0),0).is_empty(),"An east-block turn across Seventh hides its address")
	check(lateral.sample(Vector3(-170,.15,14.5),-PI/2).is_empty(),"Entry outside the lateral display envelope must stay hidden")
	check(lateral.sample(Vector3(-170,.15,13.0),-PI/2) == "50 E 7TH ST","Entry inside the lateral display envelope must appear")
	check(lateral.sample(Vector3(-170,.15,16.0),-PI/2) == "50 E 7TH ST","Keeping an address may use the wider lateral envelope")
	check(lateral.sample(Vector3(-170,.15,18.0),-PI/2).is_empty(),"Leaving the lateral keep envelope must clear the address")
	var heading = Locator.new()
	check(heading.sample(Vector3(-170,.15,0),asin(.50)).is_empty(),"Entry below the heading threshold must stay hidden")
	check(heading.sample(Vector3(-170,.15,0),asin(.60)) == "50 E 7TH ST","Entry above the heading threshold must appear")
	check(heading.sample(Vector3(-170,.15,0),asin(.40)) == "50 E 7TH ST","Keeping an address may use the wider heading envelope")
	check(heading.sample(Vector3(-170,.15,0),asin(.20)).is_empty(),"Leaving the heading keep envelope must clear the address")
	print("SEVENTH_ADDRESS_TEST ",JSON.stringify({"frontages":locator.frontages.size(),"first":first,"held":held,"failures":failures}))
	quit(0 if failures.is_empty() else 1)
