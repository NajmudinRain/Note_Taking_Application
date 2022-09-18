
from datetime import datetime
import json
from flask import Flask,jsonify,request,session,redirect,url_for,render_template,flash
from passlib.hash import pbkdf2_sha256
import uuid
import pymongo
from bson.objectid import ObjectId

#Database
client=pymongo.MongoClient('127.0.0.1',27017) 
v1 = False
# session['logged_in'] = False
# 127.0.0.1
db=client.user_login_system

class User: 
    def get_database(self):
        return db
    v1 = False
    def start_session(self,user):
        del user['password']
        session['logged_in']=True
        session['user']=user
        return jsonify(user)
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
            v1=True
            return( self.start_session(user))

        return jsonify({"error":"signup failed"}),400

    
    def signout(self):
        v1=False
        session.clear()
        return redirect('/')

    def login(self):

        user=db.user.find_one({
            "email":request.form.get('email')
        })
        if user and pbkdf2_sha256.verify(request.form.get('password'),user['password']):
            v1=True
            return self.start_session(user)

        return jsonify({"error":"Invalid login credentials"}),401
    

class Notes(User):
    def addNotes(self):
        if request.method == 'POST':
            title = request.form.get('title')
            note = request.form.get('note')
        if len(note) < 1 :
            flash('Note is too short, please write in detail !!!',category="error")
        else:
        # new_note = Note(title=title,text=note,user_id=current_user.id)

            notes=db.notes.insert_one({  
             'id':session['user'] ['_id'],    
            'title':title,
            'note':note,
            'date_added':datetime.now()
        })
        # print(user['_id'])
    # return jsonify({'title':notes['title'],'note':notes['note']}),200
    # return jsonify({'result': "succesfully added note"}),200
    # for i in list(notes):
    #     print(i) 
        
       
        userid=session['user'] ['_id']
        # session['notes']=notes
        resnotes=db.notes.find({'id':userid}).sort('date_added',-1)
        resnoteslist=[]
        for i in resnotes:
            resnoteslist.append(i)
        # print(resnoteslist)
        # session['notes']=resnotes
        # print(session['notes'])
        # print(session['notes']['title'])
        
        flash('Note is added','success')
        return render_template('dashboard.html',notes=resnoteslist)

    def update_Note(self,id):
        if request.method=='GET':
            # print(id)
            update = db.notes.find({'_id':ObjectId(id)})
            oldvalues = []
            for i in update:
                # print(i)
                oldvalues.append(i)
            
        if request.method=='POST':
            title= request.form['title']
            note= request.form['note'] 
            userid= session["user"]["_id"]
            # db.note.update_one({'_id':ObjectId(id)},{'$set':{'title':title,'note':note}})
            # db.note.update_one({"_id":ObjectId(id)}, {'$set' : {"title":title, 'note':note}})
            # user = db.find_one({'email':uemail},{'_id':0,'name':1})
            db.notes.delete_many({'_id':ObjectId(id)})
            insertnewNote = db.notes.insert_one({'id':userid,
            'title':title,
            'note':note,
            'date_added':datetime.now()
            })
            
            

            resnotes=db.notes.find({}).sort('date_added',-1)
            resnoteslist=[]
            for i in resnotes:
             resnoteslist.append(i)
            flash('Post updated succesfully','success')

            return render_template('dashboard.html',notes=resnoteslist)

        return render_template("update.html",posts=oldvalues)
    
    def delete_Note(self,id):
        db.notes.delete_one({'_id':ObjectId(id)})
        resnotes=db.notes.find({})
        resnoteslist=[]
        for i in resnotes:
            resnoteslist.append(i)
        flash('post delete successfully','success')
        return render_template('dashboard.html',notes=resnoteslist)


    def showDashboard(self):
         userid=session['user'] ['_id']
         resnotes=db.notes.find({'id':userid}).sort('date_added',-1)
         resnoteslist=[]
         for i in resnotes:
            resnoteslist.append(i)

         return render_template('dashboard.html',notes=resnoteslist)




        




