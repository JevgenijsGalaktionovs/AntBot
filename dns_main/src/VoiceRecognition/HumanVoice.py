#!/usr/bin/env python
import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
from ctypes import *
from contextlib import contextmanager
import pyaudio


######for my errors###
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)
with noalsaerr():
    p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
#######################

#%matplotlib tk

CHUNK = 1024*4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44188

p = pyaudio.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)




fig, ax = plt.subplots(1, figsize=(15, 7))
#ax.plot(data_int, '-')
#plt.show()

x = np.arange(0, 2 * CHUNK, 2) 
line, = ax.plot(x, np.random.rand(CHUNK))
ax.set_ylim(0, 255)
ax.set_xlim(0, CHUNK)

while True:
    data = stream.read(CHUNK)
    data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')[::2]
    line.set_ydata(data_int)
    fig.canvas.draw()
    fig.canvas.flush_events()
