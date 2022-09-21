from datetime import datetime
from time import sleep
from flask import session,render_template,flash
from user.models import Notes
# import user.models
import speech_recognition as sr
import gtts
from playsound import playsound
import os

r = sr.Recognizer()

ACTIVATION_COMMAND= "hi note"

def get_audio():
    with sr.Microphone() as source:
            print("Say as per instruction")
            audio= r.listen(source,phrase_time_limit=5)
            # 
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
        tempfile="temp.mp3"
        # with open("./temp.mp3") as tempfile:
        done = False
        while not done:
            try:
                tts.save(tempfile)
                playsound(tempfile)
                done = True
            except:
                continue
        
        # sleep(1)
        # playsound(tempfile)  
        # sleep(1)      
        os.remove(tempfile)
    except AssertionError:
        print("could not play sound")

i=0
def startAudio():
    global i
    while True:

        print("say Take Note")
        a=get_audio()
        command=audio_to_text(a)
        # print(command)
        if ACTIVATION_COMMAND in command.lower():
            print("activated")
            # flash("voice is activated",'success')
 
            while(i==0):
                play_sound("hi naaz say a title name?")
                i=i+1
            
            
            titleAudio=get_audio()
            title=audio_to_text(titleAudio)
            if title:
                print(title)
                # flash("title is recorded",'success')
                # play_sound(title)
            
            while(i==1):
                play_sound("speak your notes")
                i=i+1
            
            NoteAudio=get_audio()
            note=audio_to_text(NoteAudio)
            if note:
                print(note)   
            if(i==2):
                play_sound("note is added successfully")
                i=0
                break
    db=Notes().get_database()
    # useremail=session['user']['email']
    notes= db.notes.insert_one({
        'id':session['user'] ['_id'], 
        'title':title,
        'note':note,
        'date_added':datetime.now()
    })
    userid=session['user'] ['_id']
    resnotes=db.notes.find({'id':userid}).sort('date_added',-1)

    resnoteslist=[] 
    for i in resnotes:
            resnoteslist.append(i) 
    flash('Note is added','success')
    return render_template('dashboard.html',notes=resnoteslist)
    # return "<h1>u added note</h1>"
            # if Note and title:
            #     break    

# if __name__=="__main__":
#     startAudio()
               


