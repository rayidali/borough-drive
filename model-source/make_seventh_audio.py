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
save('engine.wav',[(math.sin(math.tau*55*i/RATE)+.27*math.sin(math.tau*110*i/RATE)+.12*math.sin(math.tau*165*i/RATE)) for i in range(RATE*2)])
noise=[];previous=0
for i in range(RATE*4):
    previous=previous*.65+(rng.random()-.5)*.35
    noise.append(previous)
save('rain.wav',noise)
print('Three original audio loops written')
