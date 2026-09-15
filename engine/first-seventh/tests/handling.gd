extends SceneTree
const Handling = preload("res://scripts/handling.gd")
var failures: Array[String] = []
var report = {}

func check(condition: bool, message: String):
	if not condition: failures.append(message)

func run_for(h, seconds: float, throttle: float, steer: float, brake = false, wet = 0.0, rate = 60):
	for tick in roundi(seconds*rate): h.step(1.0/rate,throttle,steer,brake,wet)

func drift(wet = 0.0, turn = 1.0, handbrake = true):
	var h = Handling.new()
	run_for(h,2.5,1.0,0.0,false,wet)
	run_for(h,.6,1.0,turn,handbrake,wet)
	var peak = absf(rad_to_deg(h.slip))
	var moving = h.motion.length()
	var heading = h.heading
	run_for(h,2.0,.3,0.0,false,wet)
	return {"peakDegrees":peak,"speedDuringSlide":moving,"recoveredDegrees":absf(rad_to_deg(h.slip)),"turn":heading}

func _initialize():
	var h = Handling.new()
	run_for(h,4,1,0)
	check(h.speed>18 and h.speed<=24,"Acceleration must reach a useful speed without exceeding the cap")
	check(h.gear>=2 and h.rpm>2000 and h.rpm<6000,"The automatic drivetrain must upshift with bounded RPM")
	var before = h.speed
	run_for(h,1,-1,0)
	check(h.speed<before-10 and h.speed>0,"S must brake forward motion before reversing")
	run_for(h,3,-1,0)
	check(h.speed<-4 and h.speed>=-6.1,"Holding S must reverse at a limited speed")
	h.reset()
	check(h.motion==Vector2.ZERO and h.slide==0 and h.yaw_rate==0,"Reset must clear all momentum")
	run_for(h,2,0,1,true)
	check(h.motion==Vector2.ZERO and h.heading==0,"Steering and handbrake at rest must not spin the car")
	var dry = drift()
	var wet = drift(1)
	var normal = drift(0,1,false)
	var right = drift(0,-1)
	check(dry.peakDegrees>18 and dry.peakDegrees<75,"Handbrake must produce a visible, bounded drift")
	check(dry.speedDuringSlide>5,"Drift must retain forward momentum")
	check(dry.peakDegrees>normal.peakDegrees*2,"Handbrake must release tire grip compared with a normal turn")
	check(dry.recoveredDegrees<4,"Released steering/handbrake must recover stable grip")
	check(wet.peakDegrees>dry.peakDegrees,"Wet tires must show reduced grip")
	check(absf(dry.turn+right.turn)<.01,"Left and right handling must be symmetric")
	var speeds = []
	var yaws = []
	for hz in [30,60,120]:
		var model = Handling.new()
		run_for(model,2,1,0,false,0,hz)
		run_for(model,.6,1,.7,true,0,hz)
		run_for(model,1,.3,0,false,0,hz)
		speeds.append(model.motion.length())
		yaws.append(model.heading)
	check(absf(speeds[0]-speeds[2])<.03 and absf(yaws[0]-yaws[2])<.01,"Integration must be stable at 30/60/120 Hz")
	report = {"dry":dry,"wet":wet,"normal":normal,"rates":{"speed":speeds,"heading":yaws},"failures":failures}
	print("SEVENTH_HANDLING_TEST ",JSON.stringify(report))
	quit(0 if failures.is_empty() else 1)
