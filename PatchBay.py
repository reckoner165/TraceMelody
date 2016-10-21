__author__ = 'Srinivasan Srinivasan'

import pyaudio

class PatchBay:

    def __init__(self, CHANNELS, Fs, buffer_len, mode):
        self.channels = CHANNELS
        self.fs = Fs
        self.buffer_len = buffer_len
        self.p = pyaudio.PyAudio()
        if mode in ['i', 'I']:
            i = True
            o = False
        elif mode in ['o', 'O']:
            i = False
            o = True
        elif mode in ['io', 'IO']:
            i = True
            o = True
        else:
            print ('Invalid mode. Enter I, O or IO')
            return
        self.stream = self.p.open(format = pyaudio.paInt16,
                            channels = self.channels,
                            rate = self.fs,
                            input = False,
                            output = True)

    def to_master(self,output):
        self.stream.write(output)

