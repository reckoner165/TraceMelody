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


capture = pyshark.LiveCapture('en1')

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
wf = wave.open('SERIAL_demo.wav', 'w')		# wf : wave file
wf.setnchannels(2);		# stereo
wf.setsampwidth(2)		# four bytes per sample
wf.setframerate(Fs)

# GLOBAL VARIABLES
mac_list = []
sound_list = []


def ip_tone(layer):

    # try:
    #
        ip_id = layer.src
        ipBroken = ip_id.split('.')
        print ip_id
    #     print ip_id, pkt.layers
    #     a = pkt.layers
    #     ssdp_flag = 'SSDP' in str(a[-1])
    #     igmp_flag = 'IGMP' in str(a[-1])
    #     # print 'IGMP', igmp_flag
    #
    #
        # src_port = layer.src
        src_port = 100
        dst_port = 4589
        # print src_port
        # dst_port = layer.dst
        # print dst_port
    #     if ssdp_flag:
    #         print 'SSDP', ssdp_flag, dst_port
    #     # Intervals are set around the minor scale
    #     # min3 = 6/5.0
    #     # maj3 = 5/4.0
    #     # per4 = 4/4.0
    #     # per5 = 3/2.0
    #     # min7 = 16/9.0
    #
        intervals = [1,1/2.0,6/5.0,5/4.0,4/4.0,3/2.0,16/9.0, 6/10.0, 5/8.0, 3/4.0, 16/18.0]
    #
        # OSC1
        T = max(0.2,0.6 - (float(ipBroken[1])/100))
        Ta = min(T, (float(ipBroken[2])/10))
        f1 = 500 + int(ipBroken[2]) - (65535/max(0.0001,float(dst_port)))

        # VIBRATO
        LFO = 10 + 0.1*65535/max(0.0001,float(dst_port))
        W = float(src_port)/65535
        # print W

        # FILTERBANK ARRAY
        filtArray = [2,3,4,5,6]

        osc = sm.oscTone(T,Ta,f1,Fs)
        vib = sm.vibrato(osc,LFO,W,Fs)
    #     if ssdp_flag:
    #         bass = sm.oscTone(T,Ta,f1/4,Fs)
    #     else:
        noise = sm.wnoise(T, Ta*1.5, Fs, 1)
        bass = sm.filterbank_22k(3,0.8,noise)
        try:
            out = sm.mix(sm.clip(0.5,1,vib),sm.clip(0.6,1,bass))
            to_master(out,1,1)
            # print 'sound out'
        except TypeError as blah:
            pass
    #     # print dir(pkt.ip)
    #     print 'TTL: ', pkt.ip.ttl
    #
        for mel in range(0,3):
            # if ssdp_flag:
            #     mel_out = sm.oscTone(0.8*T,0.8*Ta,random.choice(intervals)*f1,Fs)
            # else:
            ssl_noise = sm.wnoise(0.9*T, Ta*1.5, Fs, 1)
            mel_out = sm.filterbank_22k(random.choice(filtArray),0.8,ssl_noise)
            pan = random.random()
            to_master(mel_out, pan, 1-pan)
    #
    #     if pkt.ssl is not None:
    #         print "SSL is here"
    #         ssl_tone = sm.oscTone(T*2,T*2,f1*2,Fs)
    #         ssl_clipped = sm.clip(0.01,7,ssl_tone)
    #         # ssl_noise = sm.wnoise(T*2, Ta*1.5, Fs, 1)
    #         # ssl_filt = sm.filterbank_22k(2,0.8,ssl_noise)
    #         # ssl_out = sm.mix(ssl_filt,ssl_clipped)
    #         to_master(ssl_clipped,1,1)

def play_tone(pkt):
    # DEBUG TRY BLOCK MONITOR MODE
    try:



        # MAC ADDRESS AND SOUND MAPPING LISTS

        T = 0.5
        # FILTERBANK ARRAY
        filtArray = [2,3,4,5,6]

        all_layers=pkt.layers
        last_layer = all_layers[-1]
        # print last_layer
        dataString = last_layer.DATA_LAYER
        print '-------------'
        for layer in all_layers:
            layer_name=layer._layer_name

            # if "wlan" in layer_name:
            #     print layer

            if "radiotap" in layer_name:
                print "radio!"
                # print dir(layer);
                flag2ghz = int(layer.channel_flags_2ghz)
                flag5ghz = int(layer.channel_flags_5ghz)
                if flag2ghz == 1:
                    channel_freq = 3 + random.choice(range(1, 20))
                if flag5ghz == 1:
                    channel_freq = 400+random.choice(range(5, 20))
                ssl_tone = sm.oscTone(T,T,channel_freq,Fs)
                ssl_tone = sm.vibrato(ssl_tone,8,0.05,Fs)
                mix = sm.clip(0.9,1,ssl_tone)
                # to_master(sm.clip(0.9,1,ssl_tone),1,1)

            if "wlan" in layer_name:
                if "radio" not in layer_name:

                    if 'ta' in dir(layer):
                        trans_addr =layer.ta
                        if trans_addr in mac_list:
                            pass
                        else:
                            mac_list.append(trans_addr)
                            sound_list.append(100*random.choice(range(1,8))+10*random.choice(range(1,5)))

                        try:
                            device = mac_list.index(trans_addr)
                            device_freq = sound_list[device]
                            device_tone = sm.oscTone(T*random.random(),T,device_freq,Fs)
                            device_tone = sm.vibrato(device_tone,10,7,Fs)
                            to_master(device_tone,1,1)
                            print len(mac_list),len(sound_list),device,device_freq
                        except IndexError as I:
                            pass

                        if 'ra' in dir(layer):
                            rec_addr=layer.ra
                            # print 'trans: ', trans_addr, ',rec: ', rec_addr
                            if rec_addr == 'ff:ff:ff:ff:ff:ff':
                                print 'There\'s a BROADCAST from', trans_addr

                    noise = sm.wnoise(T,1.5*T,Fs,1)
                    filtered = sm.filterbank_22k(random.choice(filtArray),1,noise)
                    mix = sm.mix(sm.clip(0.9,1,ssl_tone),sm.clip(0.9,1,filtered))

                    if "wlan_mgt" in layer_name:
                        mgt_tone = sm.oscTone(T,T*0.5,1100,Fs)
                        mix = sm.mix(mix,sm.clip(0.9,1,mgt_tone))

            if "tcp" in layer_name:
                ssl_tone = sm.oscTone(2*T,1.2*T,500,Fs)
                mix = sm.mix(sm.clip(0.9,1,ssl_tone),sm.clip(0.9,1,mix))
                # print(layer)

            if "ip" in layer_name:
                    print "This packet wasn't secured."
                    ip_tone(layer)

        to_master(mix,1,1)

    except AttributeError as e:
        # pass
        print e
        pass

    except TypeError as te:
        pass


try:
    capture.apply_on_packets(play_tone, timeout=100)
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
