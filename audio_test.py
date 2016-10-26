__author__ = 'Sumanth Srinivasan'

import pyaudio
import struct
import SoundModule as sm

Fs = 16000
# f1 = 440
# T = 2
# Ta = 1.6
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,
                        channels = 1,
                        rate = Fs,
                        input = False,
                        output = True)


out1 = sm.oscTone(10,7.5,750,Fs)
out = sm.clip(0.01,7,out1)
out2 = sm.vibrato(out1,20,0.5,Fs)
bass = sm.oscTone(10,7.5,750/4,Fs)
k = [sum(x) for x in zip(out2, bass)]
print len(out2),len(bass),len(k)
print out2
str_out = struct.pack('h'* len(k), *k)    # 'h' for 16 bits
stream.write(str_out)