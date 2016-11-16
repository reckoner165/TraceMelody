__author__ = 'Sumanth Srinivasan'

# Network Modules
import pyshark
import random

# Audio related Modules
import pyaudio
import SoundModule as sm
import wave

# Error Handling
from trollius.executor import TimeoutError


capture = pyshark.LiveCapture('Wi-Fi')

def to_master(x, L, R):
    # TO-DO:
    # Include channel array/panning

    # Clip amplitude to fit in bit range
    for k in range(0,len(x)):
        if x[k] > 32767:
            x[k] = 32767
        elif x[k] < -32768:
            x[k] = -32768

    str_out = sm.pan_stereo(x, L, R) # Returns a packed struct ready to write
    stream.write(str_out)



    wf.writeframes(str_out)



Fs = 22000
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,
                        channels = 2,
                        rate = Fs,
                        input = False,
                        output = True)


# RECORD TO FILE (for documenting)
wf = wave.open('SERIAL_home2.wav', 'w')		# wf : wave file
wf.setnchannels(2);		# stereo
wf.setsampwidth(2)		# four bytes per sample
wf.setframerate(Fs)



def play_tone(pkt):

    try:

        ip_id = pkt.ip.src
        ipBroken = ip_id.split('.')
        # print ip_id
        # print dir(pkt.layers)
        a = pkt.layers
        ssdp_flag = 'SSDP' in str(a[-1])
        igmp_flag = 'IGMP' in str(a[-1])
        # print 'IGMP', igmp_flag


        src_port = pkt[pkt.transport_layer].srcport
        # print src_port
        dst_port = pkt[pkt.transport_layer].dstport
        # print dst_port
        if ssdp_flag:
            print 'SSDP', ssdp_flag, dst_port
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

        # FILTERBANK ARRAY
        filtArray = [2,3,4,5,6]

        osc = sm.oscTone(T,Ta,f1,Fs)
        vib = sm.vibrato(osc,LFO,W,Fs)
        if ssdp_flag:
            bass = sm.oscTone(T,Ta,f1/4,Fs)
        else:
            noise = sm.wnoise(T, Ta*1.5, Fs, 1)
            bass = sm.filterbank_22k(random.choice(filtArray),0.8,noise)

        out = sm.mix(sm.clip(0.5,1,vib),sm.clip(0.6,1,bass))
        to_master(out,1,1)

        # print dir(pkt.ip)
        print pkt.ip.ttl

        for mel in range(0,3):
            out = sm.oscTone(0.8*T,0.8*Ta,random.choice(intervals)*f1,Fs)
            pan = random.random()
            to_master(out, pan, 1-pan)

        if pkt.ssl is not None:
            print "SSL is here"
            outC = sm.oscTone(T*2,T*2,f1*2,Fs)
            clipped = sm.clip(0.01,7,outC)
            to_master(clipped,1,1)


    except AttributeError as e:
        # pass
        # print e
        pass


try:
    capture.apply_on_packets(play_tone, timeout=200)
except TimeoutError as e2:
    # Graceful timeout

    wf.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
    print 'Timeout'
    quit()



#


# quit()
