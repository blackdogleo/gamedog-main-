from flask import Flask,render_template,flash,redirect,request,session,abort,url_for
import os
from flask_cors import CORS



rapp=Flask(__name__)
CORS(rapp)

@rapp.route('/home')
def home():
    return render_template("home.html")

@rapp.route('/2_home')
def second_home():
    if  session['logged_in'] == True:
        return render_template("profile.html")
    else:
        return home()

    
@rapp.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] =='leo468' and request.form['username'] == 'ruturaj':
        session['logged_in']= True
        return second_home() 
    else:
        flash('wrong credentials')
        return home() 

@rapp.route('/logout')
def logout():
    session['logged_in']=False
    return second_home() 
    
if __name__=="__main__":
    rapp.secret_key = os.urandom(12)
    rapp.run(debug=True)
