import pyaudio
import wave
import sys
import numpy
from qhue import Bridge
import threading

'''
This script assumes you've got 2 lights hooked up to your hue bridge.
run.py <bridge-ip> <userid> <wav file>
'''

# Connect to the bridge and dim the lights for the start of the show
b = Bridge(sys.argv[1], sys.argv[2])
b('lights', 1, 'state', bri=1)
b('lights', 2, 'state', bri=1)

# Open wav file and read 128 samples at a time
CHUNK = 128
wf = wave.open(sys.argv[3], 'rb')
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
data = wf.readframes(CHUNK)

# Set up two threads so we can adjust the light levels to match both channels
def change_level(light, level):
    b('lights', light, 'state', bri=level)
def foo():
    return True
t1 = threading.Thread(target=foo, args=(), kwargs={})
t1.start()
t2 = threading.Thread(target=foo, args=(), kwargs={})
t2.start()

# For each CHUNK, update teh level of the light according to the amplitude of the wav file
while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)
    data_ord = list(ord(i) for i in list(data))
    
    if not t1.is_alive():
        left = data_ord[0::2]
        level_left = numpy.max(left) - numpy.min(left)
        t1 = threading.Thread(target=change_level, args=[1, level_left], kwargs={})
        t1.start()
        
    if not t2.is_alive():
        right = data_ord[1::2]
        level_right = numpy.max(right) - numpy.min(right)
        t2 = threading.Thread(target=change_level, args=[2, level_right], kwargs={})
        t2.start()

stream.stop_stream()
stream.close()
p.terminate()