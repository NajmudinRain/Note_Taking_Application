import speech_recognition as sr
import gtts
from playsound import playsound
import os

r = sr.Recognizer()

ACTIVATION_COMMAND= "take note"

def get_audio():
    with sr.Microphone() as source:
            print("Say as per instruction")
            audio= r.listen(source,phrase_time_limit=3)
    return audio

def audio_to_text(audio):
    text=""
    try:
        text=r.recognize_google(audio)
        #perform speech recognitoion in audio data
    except sr.UnknownValueError:
        print("speech recoginition could not understand audio")
    except sr.RequestError:
        print("could not request result from API")
    return text

def play_sound(text):
    try:
        tts=gtts.gTTS(text)
        tempfile="./temp.mp3"
        # with open('tempfile.mp3',mode='w') as tempfile:
        tts.save(tempfile)
        playsound(tempfile)
        os.remove(tempfile)
    except AssertionError:
        print("could not play sound")



if __name__=="__main__":
    i= 15
    while i:
        print("say Take Note")
        a=get_audio()
        command=audio_to_text(a)
        # print(command)
        if ACTIVATION_COMMAND in command.lower():
            print("activated")

            play_sound("say a title name?")
            
            titleAudio=get_audio()
            title=audio_to_text(titleAudio)
            if title:
                print(title)
                # play_sound(title)
            
            play_sound("speak your notes")
            NoteAudio=get_audio()
            Note=audio_to_text(NoteAudio)

            if Note:
                print(Note)   
            if(title and Note):
                break
            # if Note and title:
            #     break    
        

               


