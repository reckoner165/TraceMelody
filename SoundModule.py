__author__ = 'Sumanth Srinivasan'

from math import cos
from math import pi

def oscTone(T, Ta, f1,Fs):

    N = int(T*Fs)    # N : Number of samples to play

    # r, omega values to build a filter
    om1 = 2.0*pi * float(f1)/Fs
    r = 0.01**(1.0/(Ta*Fs))

    # Difference equation coefficients
    a1 = -2*r*cos(om1)
    a2 = r**2

    # Initialization
    y1 = 0.0
    y2 = 0.0
    gain = 1000.0

    outBlock = [0 for n in range(0,N)]

    for n in range(0, N):


        # Use impulse as input signal
        if n == 0:
            x0 = 1.0
        else:
            x0 = 0.0

        # Difference equation
        y0 = x0 - a1 * y1 - a2 * y2

        # Delays
        y2 = y1
        y1 = y0

        # Output
        outBlock[n] = gain * y0

    return outBlock

def clip(fraction,gain,block):
    outBlock = [0 for n in range(0,len(block))]

    for n in range(0,len(block)):
        if block[n] >= (fraction * gain * block[n]):
            outBlock[n] = int(fraction * gain * block[n])
        else:
            outBlock[n] = int(gain * block[n])

    return outBlock

