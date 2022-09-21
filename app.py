# from crypt import methods
import speech_recognition as sr
import gtts
from playsound import playsound
from functools import wraps
from urllib import request
from flask import Flask,render_template,session,redirect,url_for,flash
import speech
from user.models import Notes,User

app=Flask(__name__)
app.secret_key='thisisasecretkey' 

#Decorators
def login_required(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        if 'logged_in' in session:
            return f(*arg, **kwargs)
        else:
            flash('you are not signed in','success')
            return redirect('/loginpage')
            # return "<h1> you are not signed in"
    return wrap


#Routes
# this will be shown at homepage 
@app.route("/")
def homepage():                    
    # print(session['logged_in'])
    # return render_template("home.html")
    return render_template("startpage.html")

@app.route("/loginpage/",methods=['GET','POST'])
def loginpage():
    return render_template("login.html")

@app.route("/user/signin",methods=['GET','POST'])
def signin():
    return User().login()   

@app.route("/user/signup", methods=['POST'])
def signup():
    return User().signup()

@app.route("/user/signout")
@login_required 
def signout():
    return User().signout()

# once the user signup dashboard will be visible to him 
@app.route('/dashboard/')
@login_required
def dashboard():
    return Notes().showDashboard()
    # return User
    # return "<h1>welcome to dashboard<h1>"


@app.route("/notes/addnote/",methods=['GET','POST'])
@login_required
def addNotes():
    # print("najmudinr")
    # print(request.form['title'])
     return Notes().addNotes()

@app.route("/update_note/<id>", methods=['GET','POST'])
@login_required
def updateNote(id):
    return Notes().update_Note(id)
    # return render_template('update.html')

@app.route("/delete_note/<id>",methods=['GET','POST'])
@login_required
def deleteNote(id):
    return Notes().delete_Note(id)


@app.route("/use_audio",methods=['GET','POST'])
@login_required
def startAudio():
    return speech.startAudio()

@app.route("/about_us",methods=['GET','POST'])
def aboutus():
    return render_template("aboutus.html")

@app.route("/writeNotes",methods=['GET','POST'])
@login_required
def writeNotes():
    return Notes().showDashboard()
    

if __name__=="__main__":
    app.run(debug=True)
