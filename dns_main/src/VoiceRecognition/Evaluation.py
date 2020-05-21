#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from gtts import gTTS 
import os 
import speech_recognition as sr
import time
from InternetTest import *
from googletrans import Translator
from OfflineVoice import *
from VoiceRecognition import *
from ctypes import *
from contextlib import contextmanager
import pyaudio
#import example  #Uncomment if you use face verification


######for my errors###
def error_check():
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

def voice_recorder(lang):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    print("Recording Message")
    if lang == 'da':
        guess = recognize_speech_from_mic(recognizer, microphone, 'da-DK')
    elif lang == 'sv':
        guess = recognize_speech_from_mic(recognizer, microphone, 'sv-SE')
    elif lang == 'ru':
        guess = recognize_speech_from_mic(recognizer, microphone, 'ru-Ru')
    else :
        guess = recognize_speech_from_mic(recognizer, microphone, 'en-UK')
    return guess

def repeat_three(phrase,lang):
    error_check()
    translator = Translator()
    for x in range(0,3):
        translated = translator.translate('' + phrase, dest=lang)
        mytext = translated.text 
        language = lang
        myobj = gTTS(text=mytext, lang=language, slow=False) 
        myobj.save("welcome.mp3") 
        os.system("mpg321 -q welcome.mp3")
        Connection = CheckingConnectionToGoogle()
        if Connection == False:
            print("Connection lost")
        guess = voice_recorder(lang)
        if guess["transcription"]:
            print('Try number: {}'.format(x))
            print("You said: {}".format(guess["transcription"]))
            break
        print('Try number: {}'.format(x))
    return guess    





def eye_opening(lang, name, day, accident, place ):
    total = 0
    translator = Translator() 
    translated_yes = translator.translate('Yes' , dest=lang)
    wordYes =[translated_yes.text.lower()]
    translated_no = translator.translate('No' , dest=lang)
    wordNo =[translated_no.text.lower()]
    translated_danish = translator.translate('Danish' , dest=lang)
    wordDanish =[translated_danish.text.lower()]
    translated_swedish = translator.translate('Swedish' , dest=lang)
    wordSwedish =[translated_swedish.text.lower()]
    translated_russian = translator.translate('Russian' , dest=lang)
    wordRussian =[translated_russian.text.lower()]
    translated_english = translator.translate('English' , dest=lang)
    wordEnglish =[translated_english.text.lower()]
    if lang == 'da':
        mothertongue = wordDanish[0]
    elif lang == 'se':
        mothertongue = wordSwedish[0]
    elif lang == 'ru':
        mothertongue = wordRussian[0]
    else:
        mothertongue = wordEnglish[0]

    e_score = 0
    v_score = 0
    m_score = 0
    translator = Translator()
    Connection = CheckingConnectionToGoogle()
    if Connection[0] == True: 
        print(Connection, "Connected")
    elif Connection == False:
        print("Connection lost")


    guess = repeat_three('Hello, I am here to help you. Can you hear me?', lang)
    if guess["transcription"]:
        guess = repeat_three('Please avoid moving your head. This can cause spinal cord injuries. Do you understand me?', lang)
        if guess["transcription"]:
            message =  guess["transcription"].lower()
            if wordYes[0] not in message:
                guess = repeat_three('Do you speak '+ '' + mothertongue, lang)
                if guess["transcription"]:
                    message = guess["transcription"].lower()
                    if wordNo[0] in message:
                        guess = repeat_three('Please choose between the following languages: English, Danish, Swedish or Russian',lang)
                        if guess["transcription"]:
                            message = guess["transcription"].lower() 
                            if wordEnglish[0] in message:
                                lang = 'en' 
                            elif wordDanish[0] in message:
                                lang = 'da' 
                            elif wordSwedish[0] in message:
                                lang = 'sv'
                            elif wordRussian[0] in message:
                                lang = 'ru'
                            else:
                                translated = translator.translate('Sorry, I can not continue the oral communication. I will report your location and continue my mission. Do not worry my team will assist you soon', dest=lang)
                                mytext = translated.text 
                                language = lang
                                myobj = gTTS(text=mytext, lang=language, slow=False) 
                                myobj.save("welcome.mp3") 
                                os.system("mpg321 -q welcome.mp3")

                            translated_yes = translator.translate('Yes' , dest=lang)
                            wordYes =[translated_yes.text.lower()]
                            translated_no = translator.translate('No' , dest=lang)
                            wordNo =[translated_no.text.lower()]
                            translated_danish = translator.translate('Danish' , dest=lang)
                            wordDanish =[translated_danish.text.lower()]
                            translated_swedish = translator.translate('Swedish' , dest=lang)
                            wordSwedish =[translated_swedish.text.lower()]
                            translated_russian = translator.translate('Russian' , dest=lang)
                            wordRussian =[translated_russian.text.lower()]
                            translated_english = translator.translate('English' , dest=lang)
                            wordEnglish =[translated_english.text.lower()]
                                    
                                    
                                 
                    


                            
            
            # guess = repete_three('I am a member of the search and rescue team. I am here to evaluate your condition and report it to my teammates. I am going to ask you a few questions. Are you ready?', lang)
            # if guess["transcription"]:
            #     message = guess["transcription"].lower()
            #     if wordYes[0] not in message:
            #         guess = repete_three('I am here to help you. I will report your location and condition to my teammates. They will find as soon as possible. Do you think that you are ready now?', lang)
            #         if guess["transcription"]:
            #             message = guess["transcription"].lower()
            #     if wordYes[0] in message:
            #         guess = repete_three('Please try to answer the following questions as concisely as you can. Can you open your eyes and see your surroundings?', lang)
            #         if guess["transcription"]:
            #             message = guess["transcription"].lower()
            #             if wordYes[0] in message:
            #                 e_score = 4
            #             v_score = verbal_response(lang, name, day, accident, place)
            #             m_score = motor_response(lang, name)
            #             evaluation(lang, name)
            #     else:
            #         guess = repete_three('Sorry,I can not provide more assistance. I will now send a report to my teammates and continue scouting for the others.', lang)
            # else:
            #     guess = repete_three('Sorry,I can not provide more assistance. I will now send a report to my teammates and continue scouting for the others.', lang) 
######hugo's suggestion:
            guess = repete_three('I am a member of the search and rescue team. I am here to evaluate your condition and report it to my teammates. I am going to ask you a few questions. Please try to answer them as concisely as you can. Can you open your eyes and see your surroundings?', lang)
            if guess["transcription"]:
                message = guess["transcription"].lower()
                if wordYes[0] in message:
                    e_score = 4
                v_score = verbal_response(lang, name, day, accident, place)
                m_score = motor_response(lang, name)
                evaluation(lang, name)



    guess = repete_three('' + name + ' wake up. Can you hear me?', lang) 
    if guess["transcription"]:
        guess = repete_three('Please avoid moving your head. This can cause spinal cord injuries. Do you understand me?', lang)
        if guess["transcription"]:
            message =  guess["transcription"].lower()
            if wordYes[0] not in message:
                guess = repete_three('Do you speak '+ '' + mothertongue, lang)
                if guess["transcription"]:
                    message = guess["transcription"].lower()
                    if wordNo[0] in message:
                        guess = repete_three('Please choose between the following languages: English, Danish, Swedish and Russian',lang)
                        if guess["transcription"]:
                            message = guess["transcription"].lower() 
                            if wordEnglish[0] in message:
                                lang = 'en' 
                            elif wordDanish[0] in message:
                                lang = 'da' 
                            elif wordSwedish[0] in message:
                                lang = 'sv'
                            elif wordRussian[0] in message:
                                lang = 'sr'
                            else:
                                translated = translator.translate('Sorry, I can not continue the oral communication. I will report your location and continue my mission. Do not worry my teammates will assist you as soon as poosible', dest=lang)
                                mytext = translated.text 
                                language = lang
                                myobj = gTTS(text=mytext, lang=language, slow=False) 
                                myobj.save("welcome.mp3") 
                                os.system("mpg321 -q welcome.mp3")

                            translated_yes = translator.translate('Yes' , dest=lang)
                            wordYes =[translated_yes.text.lower()]
                            translated_no = translator.translate('No' , dest=lang)
                            wordNo =[translated_no.text.lower()]
                            translated_danish = translator.translate('Danish' , dest=lang)
                            wordDanish =[translated_danish.text.lower()]
                            translated_swedish = translator.translate('Swedish' , dest=lang)
                            wordSwedish =[translated_swedish.text.lower()]
                            translated_russian = translator.translate('Russian' , dest=lang)
                            wordRussian =[translated_russian.text.lower()]
                            translated_english = translator.translate('English' , dest=lang)
                            wordEnglish =[translated_english.text.lower()]



                    if wordYes[0] in message:
                #     guess = repete_three('I am hear to evaluate your condition and report it to the search and rescue team. Are you ready?', lang)
                #     if guess["transcription"]:
                #         message = guess["transcription"].lower
                #         if wordYes[0] not in message:
                #             guess = repete_three('I am here to help you. I will report your location and condition to my teammates. They will soon find you and help you. Are you ready now?', lang)
                #             if guess["transcription"]:
                #                 message = guess["transcription"].lower()
                #         if wordYes[0] in message:
                #             guess = repete_three('Please try to answer the following questions as concisely as you can. Can you open your eyes and see your surroundings?', lang)
                #             if guess["transcription"]:
                #                 message = guess["transcription"].lower()
                #                 if wordYes[0] in message:
                #                     e_score = 3
                #                 v_score = verbal_response(lang,name, day, accident, place)
                #                 m_score = motor_response(lang,name)
                #                 total = e_score + v_score + m_score
                #                 evaluation(lang,name)
                        guess = repete_three('I am a member of the search and rescue team. I am here to evaluate your condition and report it to my teammates. I am going to ask you a few questions. Please try to answer them as concisely as you can. Can you open your eyes and see your surroundings?', lang)
                        if guess["transcription"]:
                            message = guess["transcription"].lower()
                            if wordYes[0] in message:
                                e_score = 3
                            v_score = verbal_response(lang, name, day, accident, place)
                            m_score = motor_response(lang, name)
                            total = e_score + v_score + m_score
                            evaluation(lang, name)           

                        else:
                            guess = repeat_three('Sorry I can not provide more assistance. I will now send a report to my team and continue scouting for others.', lang) 

    if not guess["success"]:
        print("ERROR: {}".format(guess["error"]))
    print("v_score: {}".format(v_score))
    print("e_score: {}".format(e_score))
    print("m_score: {}".format(m_score))
    print("Total score:{}".format(total))
    

    return [e_score, v_score]

def verbal_response(lang, name, day, accident, place):
    translator = Translator() 
    translated_yes = translator.translate('Yes' , dest=lang)
    wordYes =[translated_yes.text.lower()]
    translated_day = translator.translate(day , dest=lang)
    wordDay =[translated_day.text.lower()]
    translated_accident = translator.translate(accident , dest=lang)
    wordAccident =[translated_accident.text.lower()]
    translated_place = translator.translate(place , dest=lang)
    wordPlace =[translated_place.text.lower()]
    translated_name = translator.translate(name , dest=lang)
    wordName =[translated_name.text.lower()]
    score = 3
    translator = Translator()
    Connection = CheckingConnectionToGoogle()
    if Connection[0] == True: 
        print(Connection, "Connected")
    elif Connection == False:
        print("Connection lost")
    guess = repeat_three('Can you remember your name?', lang) 
    if guess["transcription"]:
        message = guess["transcription"].lower()
        if wordYes[0] in message:
            guess = repeat_three('What is your name?', lang)
            if guess["transcription"]:
                message = guess["transcription"].lower()
                if wordName[0] in message:
                    guess = repeat_three('What day of the week is it today?', lang)
                    if guess["transcription"]:
                        message = guess["transcription"].lower()
                        if wordDay[0] in message:
                            guess = repeat_three('What natural disaster happened to you just a few minutes ago?', lang)
                            if guess["transcription"]:
                                message = guess["transcription"].lower()
                                if wordAccident[0] in message:
                                    guess = repeat_three('Where are we right now?', lang)
                                    if guess["transcription"]:
                                        message = guess["transcription"].lower() 
                                        if wordPlace[0] in message:
                                            score = 5
                        else:
                            score = 4
        else:
            guess = repeat_three('Your name is :'+ '' + name + 'Is that correct?', lang)
            if guess["transcription"]:
                message = guess["transcription"].lower()
                if wordYes[0] in message:
                    guess = repeat_three('What day of the week is it today?', lang)
                    if guess["transcription"]:
                        message = guess["transcription"].lower()
                        if day in message:
                            guess = repeat_three('What natural disaster happened to you just a few minutes ago?', lang)
                            if guess["transcription"]:
                                message = guess["transcription"].lower()
                                if accident in message:
                                    guess = repeat_three('Where are we right now?', lang)
                                    if guess["transcription"]:
                                        message = guess["transcription"].lower() 
                                        if place in message:
                                            score = 5
                        else:
                            score = 4                
    return score


def motor_response(lang,name):
    score = 0
    translator = Translator()
    Connection = CheckingConnectionToGoogle()
    if Connection == False:
        print("Connection lost")
    translated_yes = translator.translate('Yes' , dest=lang)
    wordYes =[translated_yes.text.lower()]
    guess = repeat_three('Can you put your tongue out and put it back into your mouth again?', lang)
    if guess["transcription"]:
        message = guess["transcription"].lower()
        if wordYes[0] in message:
            score = 6
        else:
            score = 0

    return score

def evaluation(lang, name):
    translator = Translator() 
    translated_yes = translator.translate('Yes' , dest=lang)
    wordYes =[translated_yes.text.lower()]
    translated_no = translator.translate('No' , dest=lang)
    wordNo =[translated_no.text.lower()]
    translated_arm = translator.translate('Arm' , dest=lang)
    wordArm =[translated_arm.text.lower()]
    translated_abdomen = translator.translate('Abdomen' , dest=lang)
    wordAbdomen =[translated_abdomen.text.lower()]
    translated_head = translator.translate('Head' , dest=lang)
    wordHead =[translated_head.text.lower()]
    translated_stomach = translator.translate('Stomach' , dest=lang)
    wordStomach =[translated_stomach.text.lower()]
    if name == 'Rebecca':
        gender = 'She'
        gender_2 = 'her'
    else:
        gender = 'He'
        gender_2 = 'his'

    text_trapped = ''
    text_pain = ''
    text_limb = ''
    text_limbsmoving = ''
    text_bleed = ''
    text_feel = ''



    Connection = CheckingConnectionToGoogle()
    if Connection[0] == True: 
        print(Connection, "Connected")
    elif Connection == False:
        print("Connection lost")
    guess = repeat_three('Are you trapped?', lang)
    if guess["transcription"]:
        message = guess["transcription"].lower()
        if wordYes[0] in message:
            print('Victim is trapped.')
            text_trapped = 'I have found Dariush. He is trapped.'
        elif wordNo[0] in message:
            print('Victim is free.')
            text_trapped = 'I have found ' + '' + name + '' + gender +' is not trapped'
        guess = repeat_three('Can you move all your limbs?', lang)
        if guess["transcription"]:
            message = guess["transcription"].lower()
            if wordYes[0] in message:
                text_limbsmoving = '' + gender + 'can move all of the limbs.'
            if wordNo[0] in message:
                guess = repeat_three('Which is the limb that you can you not move?', lang)
                if guess["transcription"]:
                    message = guess["transcription"].lower()
                    if wordArm[0] in message:
                        text_limb = '' + gender + 'is not able to move' + '' + gender_2 + '' + wordArm[0]
                        guess = repeat_three('Can you still feel it?',lang)
                        if guess["transcription"]:
                            message = guess["transcription"].lower()
                            if wordYes[0] in message:
                                text_feel = 'and ' + '' + gender + 'does not feel it.'
                            
        guess = repeat_three('Are you bleeding?', lang)
        if guess["transcription"]:
            message = guess["transcription"].lower()
            if wordYes[0] in message:
                guess = repeat_three('Where is the source of blood?', lang)
                if guess["transcription"]:
                    message = guess["transcription"].lower()
                    if wordHead[0] in message:
                        print("Victim is bleeding from the head.")
                        text_bleed = '' + name + 'is bleeding from the head.'
                    elif wordAbdomen[0] or wordStomach[0] in message:
                        print("Victim is bleeding from the abdominal area.")
                        text_bleed = '' + name + 'is bleeding from abdominal area.'
                    elif wordArm[0] in message:
                        print("Victim's arm is bleeding")
            elif wordNo[0]:
                text_bleed = '' + name + 'is not bleeding externally.'
        guess = repeat_three('Do you feel severe pain?', lang)
        if guess["transcription"]:
            message = guess["transcription"].lower()
            if wordYes[0] in message:
                guess = repeat_three('Where is the source of pain?', lang)
                if guess["transcription"]:
                    message = guess["transcription"].lower()
                    if wordHead[0] is message:
                        print("Victim has pain from the head.")
                        text_pain = '' + gender + 'feels severe pain in the head.'
                    elif wordAbdomen[0] or wordStomach[0] in message:
                        print("Victim has pain from the abdominal area.")
                        text_pain = '' + gender + '' + 'feels severe abdominal pain.'
                    elif wordArm[0] in message:
                        print("victim's arm is painfull.")
                        text_pain = '' + gender + 'feels severe pain in' + '' + gender_2 + 'arm.'
            elif wordNo[0] in message:
                print("Victim doesn't feel severe pain.")
                text_pain = '' + gender + 'does not feel severe pain.'
    oral_report = '' + text_trapped + '' + text_limbsmoving + '' + text_limb + '' + text_feel + '' + text_bleed + '' + text_pain
    print(oral_report)
    guess = repeat_three('' + oral_report + 'Do you confirm?', lang)
if __name__ == "__main__":                                   
    eye_opening('en','Rebecca', 'Sunday', 'earthquake', 'home')