extends RefCounted
## Arcade tire model, in metres/seconds. Momentum survives changes of heading.
## Small fixed integration steps keep steering/grip stable at different tick rates.
const MAX_SPEED = 24.0
const REVERSE_SPEED = 6.0
const RATIOS = [3.3, 2.15, 1.53, 1.14]
var motion = Vector2.ZERO
var heading = 0.0
var steering = 0.0
var yaw_rate = 0.0
var speed = 0.0
var slip = 0.0
var slide = 0.0
var rpm = 850.0
var gear = 1
var shift_time = 0.0
var engine_load = 0.0
var tire_scrub = 0.0

func reset():
	motion = Vector2.ZERO
	steering = 0.0
	yaw_rate = 0.0
	speed = 0.0
	slip = 0.0
	slide = 0.0
	rpm = 850.0
	gear = 1
	shift_time = 0.0
	engine_load = 0.0
	tire_scrub = 0.0

func step(dt: float, throttle: float, turn: float, handbrake: bool, wet: float):
	var steps = maxi(1, ceili(dt / (1.0 / 120.0)))
	var h = dt / steps
	for i in steps: integrate(h, throttle, turn, handbrake, clampf(wet,0,1))

func integrate(dt: float, throttle: float, turn: float, handbrake: bool, wet: float):
	var forward = Vector2(-sin(heading),-cos(heading))
	var right = Vector2(cos(heading),-sin(heading))
	var longitudinal = motion.dot(forward)
	var lateral = motion.dot(right)
	var pace = motion.length()
	var driving = throttle * longitudinal >= -.25
	var power = abs(throttle) if driving else 0.0
	shift_time = maxf(0,shift_time-dt)
	var target_slide = 1.0 if handbrake and pace > 3.0 else 0.0
	# A short pull initiates the slide; releasing it progressively restores grip.
	slide = move_toward(slide,target_slide,dt*(5.5 if target_slide>slide else 1.05))
	var lock = lerpf(.60,.34,clampf(pace/24.0,0,1))
	var target_steer = turn*lock
	var steer_rate = 3.1 if signf(target_steer)!=signf(steering) else 2.2
	steering = move_toward(steering,target_steer,dt*steer_rate)
	slip = atan2(lateral,maxf(abs(longitudinal),1.0))
	var yaw_target = longitudinal/2.58*tan(steering)*(1.0+slide*.22)
	# Soft countersteer assistance catches a released drift without snapping it.
	yaw_target -= slip*1.8*(1.0-slide*.80)*clampf(pace/4.0,0,1)
	yaw_target = clampf(yaw_target,-2.1,2.1)
	yaw_rate = lerpf(yaw_rate,yaw_target,1-exp(-dt*10.0))
	heading = wrapf(heading+yaw_rate*dt,-PI,PI)
	forward = Vector2(-sin(heading),-cos(heading))
	right = Vector2(cos(heading),-sin(heading))
	longitudinal = motion.dot(forward)
	lateral = motion.dot(right)
	var traction = lerpf(12.0,1.45,slide)*(1.0-wet*.24)
	motion -= right*lateral*(1-exp(-traction*dt))
	var acceleration = 0.0
	if not driving:
		acceleration = throttle*15.0
	elif throttle > 0 and longitudinal < MAX_SPEED:
		acceleration = throttle*8.4*(1.0-.38*maxf(longitudinal,0)/MAX_SPEED)
	elif throttle < 0 and longitudinal > -REVERSE_SPEED:
		acceleration = throttle*5.0
	if shift_time > 0: acceleration *= .25
	motion += forward*acceleration*dt
	var drag = .28 + pace*pace*.007 + (4.2 if handbrake else 0.0)
	motion = motion.move_toward(Vector2.ZERO,drag*dt)
	if abs(throttle)<.01 and motion.length()<.08: motion = Vector2.ZERO
	if motion.length()>MAX_SPEED: motion = motion.normalized()*MAX_SPEED
	speed = motion.dot(forward)
	slip = atan2(motion.dot(right),maxf(abs(speed),1.0))
	tire_scrub = clampf((abs(slip)-.09)*1.45,0,1)*clampf(pace/6.0,0,1)
	if handbrake: tire_scrub = maxf(tire_scrub,clampf(pace/12.0,0,1)*.85)
	var wheel_rpm = abs(speed)*60.0/(TAU*.335)*3.7
	var connected_rpm = wheel_rpm*float(RATIOS[gear-1])
	if speed < -.2:
		gear = 1
	elif shift_time <= 0:
		if connected_rpm>5150 and gear<4:
			gear += 1
			shift_time = .18
		elif connected_rpm<2050 and gear>1:
			gear -= 1
			shift_time = .12
	var clutch_rpm = 850.0+power*1050.0+slide*power*1450.0
	var target_rpm = clampf(maxf(clutch_rpm,wheel_rpm*float(RATIOS[gear-1])),800,5900)
	rpm = lerpf(rpm,target_rpm,1-exp(-dt*(13.0 if target_rpm<rpm else 6.0)))
	engine_load = lerpf(engine_load,power*(.35 if shift_time>0 else 1.0),1-exp(-dt*8.0))
