__author__ = 'Sumanth Srinivasan'

from pyo import *
import time

s = Server().boot()
# a = Sine(440, 0, 0.1).out()
s.start()

wav = SquareTable()
env = CosTable([(0,0.1), (90,1), (900,.3), (901,0)])
met = Metro(.125, 12).play()
amp = TrigEnv(met, table=env, mul=.1)
pit = TrigXnoiseMidi(met, dist='loopseg', x1=20, scale=1, mrange=(100,100))
out = Osc(table=wav, freq=100, mul=amp).out()
time.sleep(1)
s.stop()
