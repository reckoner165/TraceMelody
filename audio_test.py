__author__ = 'Sumanth Srinivasan'

import pyaudio
import struct
import SoundModule as sm

Fs = 44100
# f1 = 440
# T = 2
# Ta = 1.6
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,
                        channels = 1,
                        rate = Fs,
                        input = False,
                        output = True)


out1 = sm.oscTone(10,7.5,14340,Fs)
out = sm.clip(0.01,7,out1)
str_out = struct.pack('h'* len(out), *out)    # 'h' for 16 bits
stream.write(str_out)