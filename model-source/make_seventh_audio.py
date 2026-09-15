"""Original synthesized loops for Seventh, slowly. No sampled recordings.
Run python3 model-source/make_seventh_audio.py. MIT, Borough Drive contributors.
"""
import math, random, wave, array
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'engine/first-seventh/assets/audio'
OUT.mkdir(parents=True,exist_ok=True)
RATE=22050

def save(name,samples):
    peak=max(max(abs(v) for v in samples),.01)
    pcm=array.array('h',(round(max(-1,min(1,v/peak*.76))*32767) for v in samples))
    with wave.open(str(OUT/name),'wb') as out:
        out.setnchannels(1);out.setsampwidth(2);out.setframerate(RATE);out.writeframes(pcm.tobytes())

music=[0.0]*(RATE*12)
chords=[[57,60,64,67],[53,57,60,64],[48,52,55,59],[55,59,62,65]]
rng=random.Random(710)
for bar,chord in enumerate(chords):
    for note in chord:
        freq=440*2**((note-69)/12)
        for i in range(RATE*3):
            t=i/RATE
            env=min(1,t/.04)*math.exp(-t/1.3)*min(1,(3-t)/.18)
            tone=math.sin(math.tau*freq*t)+.16*math.sin(math.tau*freq*2*t)*math.exp(-t*2)
            music[bar*RATE*3+i]+=tone*env*.09
    for beat in range(4):
        offset=round((bar*3+beat*.75)*RATE)
        freq=440*2**((chord[0]-24-69)/12)
        for i in range(round(RATE*.55)):
            t=i/RATE
            music[offset+i]+=math.sin(math.tau*freq*t)*math.exp(-t*5)*min(1,t/.025)*.16
            if beat%2==0:
                music[offset+i]+=math.sin(math.tau*(46*t+30*(1-math.exp(-t*24))/24))*math.exp(-t*17)*.21
            else:
                music[offset+i]+=(rng.random()-.5)*math.exp(-t*32)*.09
    for beat in range(8):
        offset=round((bar*3+beat*.375+.025*(beat%2))*RATE)
        for i in range(min(round(RATE*.055),len(music)-offset)):
            t=i/RATE
            music[offset+i]+=(rng.random()-.5)*math.exp(-t*80)*.025
save('cornerlight.wav',music)
# Four-cylinder firing pulses, exhaust harmonics and induction texture. Integer
# periods make the loops seamless; runtime pitch follows RPM and crossfades load.
# These are original synthesis, not a recording or an imitation of a named car.
def engine_loop(rpm, loaded):
    count=RATE*4
    crank=rpm/60
    samples=[]
    for i in range(count):
        t=i/RATE
        fire=math.tau*crank*2*t
        rumble=(math.sin(fire)+.48*math.sin(fire*2+.4)
                +.28*math.sin(fire*3+.8)+.15*math.sin(fire*5+.3)
                +.18*math.sin(fire*.5)+.10*math.sin(fire*1.5+.7))
        rasp=sum(math.sin(fire*k+.31*k)/(k**1.28) for k in range(6,22))
        induction=(math.sin(math.tau*179*t)+.5*math.sin(math.tau*283*t)
                   +.22*math.sin(math.tau*431*t))*.055
        rough=1+.035*math.sin(math.tau*7*t)+.018*math.sin(math.tau*13*t)
        samples.append(math.tanh((rumble*(.64 if loaded else .44)
                                  +rasp*(.64 if loaded else .12))*rough)+induction)
    return samples
save('engine-idle.wav',engine_loop(1050,False))
save('engine-load.wav',engine_loop(2400,True))
save('engine-coast.wav',engine_loop(2400,False))
# Cyclic, filtered noise avoids a click at every tire/road loop boundary.
def noise_loop(seed, decay):
    rand=random.Random(seed)
    raw=[rand.uniform(-1,1) for _ in range(RATE*4)]
    out=[]; low=0
    for value in raw[-RATE:]+raw:
        low=low*decay+value*(1-decay)
        out.append(low)
    return out[RATE:]
road=noise_loop(703,.94)
rubber=noise_loop(704,.53)
save('road.wav',road)
save('tires.wav',[v*.78+.05*math.sin(math.tau*913*i/RATE+1.8*math.sin(math.tau*9*i/RATE))
                  +.022*math.sin(math.tau*1373*i/RATE) for i,v in enumerate(rubber)])
save('impact.wav',[(road[i]*2+math.sin(math.tau*53*i/RATE)*.38)
                   *min(1,i/(RATE*.004))*math.exp(-i/RATE*15)
                   for i in range(round(RATE*.55))])
noise=[];previous=0
for i in range(RATE*4):
    previous=previous*.65+(rng.random()-.5)*.35
    noise.append(previous)
save('rain.wav',noise)
print('Original music, engine/load/coast, tire/road, impact and rain audio written')
