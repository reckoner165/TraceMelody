__author__ = 'Sumanth Srinivasan'


import pyshark
import base64
import random
import math

import pyaudio
import struct
import SoundModule as sm

import wave

capture = pyshark.LiveCapture('Wi-Fi')

# capture.sniff(timeout=20)
def to_master(x, L, R):
    # TO-DO:
    # Include channel array/panning
    for k in range(0,len(x)):
        if x[k] > 32767:
            x[k] = 32767
        elif x[k] < -32768:
            x[k] = -32768

    str_out = sm.pan_stereo(x, L, R)
    stream.write(str_out)
    # wf.writeframes(str_out)


Fs = 16000
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,
                        channels = 2,
                        rate = Fs,
                        input = False,
                        output = True)


# RECORD TO FILE
# wf = wave.open('SERIAL_home.wav', 'w')		# wf : wave file
# wf.setnchannels(1);		# one channel (mono)
# wf.setsampwidth(2)		# four bytes per sample
# wf.setframerate(Fs)		# samples per second


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


def play_tone(pkt):

    try:

        ip_id = pkt.ip.src
        ipBroken = ip_id.split('.')
        # print ip_id

        src_port = pkt[pkt.transport_layer].srcport
        # print src_port
        dst_port = pkt[pkt.transport_layer].dstport
        # print dst_port

        # Intervals are set around the minor scale
        # min3 = 6/5.0
        # maj3 = 5/4.0
        # per4 = 4/4.0
        # per5 = 3/2.0
        # min7 = 16/9.0

        intervals = [1,1/2.0,6/5.0,5/4.0,4/4.0,3/2.0,16/9.0, 6/10.0, 5/8.0, 3/4.0, 16/18.0]

        # OSC1
        T = max(0.2,0.6 - (float(ipBroken[1])/100))
        Ta = min(T, (float(ipBroken[2])/10))
        f1 = 700 + int(ipBroken[2]) - (65535/max(0.0001,float(dst_port)))

        # VIBRATO
        LFO = 10 + 0.1*65535/max(0.0001,float(dst_port))
        W = float(src_port)/65535
        print W

        osc = sm.oscTone(T,Ta,f1,Fs)
        vib = sm.vibrato(osc,LFO,W,Fs)
        bass = sm.oscTone(T,Ta,f1/4,Fs)

        # TO-DO:
        # Write a MIXER function that weights and adds signal blocks
        out = [sum(x) for x in zip(sm.clip(0.5,1,vib), sm.clip(0.6,1,bass))]
        # clipOut = sm.clip(0.6,1,out)
        to_master(out,1,1)


        for mel in range(0,3):
            out = sm.oscTone(0.8*T,0.8*Ta,random.choice(intervals)*f1,Fs)
            to_master(out, random.random(), random.random())

        if pkt.ssl is not None:
            print "SSL is here"
            outC = sm.oscTone(T*2,T*2,f1*2,Fs)
            clipped = sm.clip(0.01,7,outC)
            to_master(clipped,1,1)




    except AttributeError as e:
        pass
        # print e



capture.apply_on_packets(play_tone, timeout=200)


stream.stop_stream()
stream.close()
p.terminate()
# wf.close()

# quit()
