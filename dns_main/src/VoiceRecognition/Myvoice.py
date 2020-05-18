import random
import time
from gtts import gTTS 
import os 
import speech_recognition as sr

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    # set the list of words, maxnumber of guesses, and prompt limit
    WORDS = ["Right", "Left"]


    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while (1):
        while (1):
            print("Recording Message")
            guess = recognize_speech_from_mic(recognizer, microphone)
            print(guess)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        # if there was an error, stop
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        # show the user the transcription
        print("You said: {}".format(guess["transcription"]))
        message = guess["transcription"].lower() 
        right = ['right', 'rights', 'rite', 'lights']
        left  = ['left', 'list', 'lists', 'next', 'light', 'lift', 'lifts'] 
        if left[0] in message or left[1] in message or left[2] in message or left[3] in message or left[4] in message or left[5] in message or left[6] in message:
            mytext = 'Turning Left'
            language = 'en'
            myobj = gTTS(text=mytext, lang=language, slow=False) 
            myobj.save("welcome.mp3") 
            os.system("mpg321 welcome.mp3")   
        elif right[0] in message or right[1] in message or right[2] in message or right[3] in message: 
            mytext = 'Turning Right'
            language = 'en'
            myobj = gTTS(text=mytext, lang=language, slow=False) 
            myobj.save("welcome.mp3") 
            os.system("mpg321 welcome.mp3")         
        else:
            mytext = 'I can not hear you'
            language = 'en'
            myobj = gTTS(text=mytext, lang=language, slow=False) 
            myobj.save("welcome.mp3") 
            os.system("mpg321 welcome.mp3")     

     
