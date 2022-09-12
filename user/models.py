import json
from turtle import title
from flask import Flask,jsonify,request,session,redirect,url_for,render_template,flash
from passlib.hash import pbkdf2_sha256
import uuid
import pymongo

#Database
client=pymongo.MongoClient('127.0.0.1',27017) 
# 127.0.0.1
db=client.user_login_system
class User:
    def start_session(self,user):
        del user['password']
        session['logged_in']=True
        session['user']=user
        return jsonify(user),200
    def signup(self):
        # print(request.form.get(name))
        #create the user object
        user={
            # "_id":uuid.uuid4().hex,
            # "name":request.json['name'],
            # "email":request.json['email'],
            # "password":request.json['password']
            "_id":uuid.uuid4().hex,
            "name":request.form.get('name'),
            "email":request.form.get('email'),
            "password":request.form.get('password')
        }
         # print(request.form)
        # db.user.delete_many({"name":"najmudin"})
        user["password"]=pbkdf2_sha256.encrypt(user["password"])
        if db.user.find_one({"email":user['email']}):
            return jsonify({"error":"email address already in use"}),400
            
        if db.user.insert_one(user):
            return self.start_session(user)

        return jsonify({"error":"signup failed"}),400

    
    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):
        user=db.user.find_one({
            "email":request.form.get('email')
        })
        if user and pbkdf2_sha256.verify(request.form.get('password'),user['password']):
            return self.start_session(user)

        return jsonify({"error":"Invalid login credentials"}),401
    

class Notes:
    
   def addNotes(self):
    if request.method == 'POST':
        title = request.form.get('title')
        note = request.form.get('note')
    if len(note) < 1 :
            flash('Note is too short, please write in detail !!!',category="error")
    else:
        # new_note = Note(title=title,text=note,user_id=current_user.id)
        notes=db.notes.insert_one({
            'title':title,
            'note':note
        })
    # return jsonify({'title':notes['title'],'note':notes['note']}),200
    # return jsonify({'result': "succesfully added note"}),200
    for i in list(notes):
        print(i)
    return render_template('notes.html')


