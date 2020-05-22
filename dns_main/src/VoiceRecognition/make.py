#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from gtts import gTTS 
import os 
import speech_recognition as sr
import time
from InternetTest import *
#from keyboardControll import *
from googletrans import Translator
#from OfflineVoice import *
from VoiceRecognition import *
from ctypes import *
from contextlib import contextmanager
import pyaudio
#import example


######for my errors###
def reb_errore():
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

def repete_three(phrase,fName):
    translator = Translator()
    lang = 'en'
    translated = translator.translate('' + phrase, dest=lang)
    mytext = translated.text 
    language = lang
    myobj = gTTS(text=mytext, lang=language, slow=False) 
    myobj.save("{}".format(fName)) 
    os.system("mpg321 -q {}".format(fName))
    Connection = CheckingConnectionToGoogle()
    # if Connection[0] == True: 
    #     print(Connection, "Connected")
    if Connection == False:
        print("Connection lost")

repete_three('Where is the source of pain?','painsource.mp3')