__author__ = 'Sumanth Srinivasan'


import pyshark
import base64
import random
import math

from math import cos
from math import pi
import pyaudio
import struct

capture = pyshark.LiveCapture('Wi-Fi')

# capture.sniff(timeout=20)



# def printHeader(pkt):
#     try:
#         protocol =  pkt.layers
#         # http_user= pkt.http.user_agent
#         # if "Firefox" in http_user:
#         #     http_user="Firefox"
#         # else:
#         #     http_user="Chrome"
#
#         #
#
#
#         ip_id=pkt.ip.id
#         # ok=""
#         # while random.random() > 0.1:
#         #     ok+="    "
#         ascii_string = str(base64.b16decode(pkt.ip_id))[2:-1]
#         print (ascii_string)
#         # ok=str(pkt.ip.id)
#         # print ok
#         # if pkt.ssl is not None:
#         #     print "SSL is here"
#         # handshake_length=pkt.ssl.handshake_length
#
#     except AttributeError as e:
#             #ignore packets that aren't TCP/UDP or IPv4
#             pass
#
# capture.apply_on_packets(printHeader, timeout=100)

# AUDIO TEST
Fs = 44100
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,
                        channels = 1,
                        rate = Fs,
                        input = False,
                        output = True)

# 16 bit/sample


def gene_tone(f1,T,Ta):
    # Fs = 32000

    # T = 2       # T : Duration of audio to play (seconds)
    N = int(T*Fs)    # N : Number of samples to play

    # Pole location
    # f1 = 700 + int(float(ipBroken[2]))   # Frequency
    # print f1
    om1 = 2.0*pi * float(f1)/Fs

    # Ta = 0.2 + (float(ipBroken[2]))     # Ta : Time till amplitude profile decays to 1% (in seconds)
    # Ta = 0.006
    r = 0.01**(1.0/(Ta*Fs))

    # print 'Fs = ', Fs
    # print 'r = ', r

    # Difference equation coefficients
    a1 = -2*r*cos(om1)
    a2 = r**2

    # print 'a1 = ', a1
    # print 'a2 = ', a2

    # Initialization
    y1 = 0.0
    y2 = 0.0
    gain = 1000.0



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
        out = gain * y0
        # print out
        # if out >= 2^15:
        #     out = 2^14

        str_out = struct.pack('h', out)    # 'h' for 16 bits

        stream.write(str_out)

def play_tone(pkt):
    try:
        # Fs : Sampling frequency (samples/second)
        # Fs = 8000

        ip_id = pkt.ip.src
        # ascii_string = str(base64.b16decode(pkt.ip_id))[2:-1]

        ipBroken = ip_id.split('.')

        #
        # min3 = 6/5.0
        # maj3 = 5/4.0
        # per4 = 4/4.0
        # per5 = 3/2.0
        # min7 = 16/9.0

        intervals = [1,1/2.0,6/5.0,5/4.0,4/4.0,3/2.0,16/9.0]

        gene_tone(700 + int(float(ipBroken[2])), 0.2 , max(0.2, (float(ipBroken[2]))))

        for mel in range(0,3):

            gene_tone(random.choice(intervals)*(700 + int(float(ipBroken[2]))), 0.2 , max(0.2 , (float(ipBroken[2]))))

        print ip_id

    except AttributeError as e:
        pass

capture.apply_on_packets(play_tone, timeout=100)

stream.stop_stream()
stream.close()
p.terminate()
