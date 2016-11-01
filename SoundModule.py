__author__ = 'Sumanth Srinivasan'

# Module containing real-time audio processing functions to generate tones and apply effects over a given block

import math
import struct
from math import cos
from math import pi

# Pans audio by applying different gains on left and right channels
def pan_stereo(x, gain_L, gain_R):

    x_stereo = [0 for n in range(0,2*len(x))]
    if gain_L > 1 or gain_L < 0 or gain_R > 1 or gain_R < 0:
        print "Invalid Gain. Try between 0 and 1"

    for n in range(0,len(x)):
        x_stereo[2*n] = gain_L * x[n]
        x_stereo[2*n + 1] = gain_R * x[n]

    stereo = struct.pack('h'*2*len(x), *x_stereo)  # 'h' for 16 bits
    return stereo

# All 
# Oscilators
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


# Effects modules
def clip(fraction,gain,block):
    outBlock = [0 for n in range(0,len(block))]

    for n in range(0,len(block)):
        if block[n] >= (fraction * gain * block[n]):
            outBlock[n] = int(fraction * gain * block[n])
        else:
            outBlock[n] = int(gain * block[n])

    return outBlock

def vibrato(block,fL,WL,RATE):
    outBlock = [0 for n in range(0,len(block))]
    buffer_MAX = len(block)                          # Buffer length
    bufferL = [0.0 for i in range(buffer_MAX)]

    # Buffer (delay line) indices
    krL = 0  # read index
    kwL = int(0.5 * buffer_MAX)  # write index (initialize to middle of buffer)


    for n in range(0,len(block)):
        kr_prev = int(math.floor(krL))
        kr_next = kr_prev + 1
        frac = krL - kr_prev    # 0 <= frac < 1
        if kr_next >= buffer_MAX:
            kr_next = kr_next - buffer_MAX

        # Compute output value using interpolation
        outBlock[n] = (1-frac) * bufferL[kr_prev] + frac * bufferL[kr_next]

        # Update buffer (pure delay)
        bufferL[kwL] = block[n]

        # Increment read index
        krL = krL + 1 + WL * math.sin( 2 * math.pi * fL * n / RATE )
            # Note: kr is fractional (not integer!)

        # Ensure that 0 <= kr < buffer_MAX
        if krL >= buffer_MAX:
            # End of buffer. Circle back to front.
            krL = 0

        # Increment write index
        kwL = kwL + 1
        if kwL == buffer_MAX:
            # End of buffer. Circle back to front.
            kwL = 0


    return outBlock