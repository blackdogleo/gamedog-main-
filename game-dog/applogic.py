from flask import Flask,render_template,send_file,flash,redirect,request,session,abort,url_for
import MySQLdb
import os
from flask_cors import CORS

jink = MySQLdb.connect("Rsj","ruturaj","ruturaj","active")

cursor = jink.cursor()

mink = MySQLdb.connect("Rsj","ruturaj","ruturaj","active")
cursor2 = mink.cursor()



app = Flask(__name__)
CORS(app)



@app.route("/")
def start():

    return render_template("linkfrom.html")




@app.route("/article1")
def tur():
    u = "tolink"
    cursor.execute("""SELECT linkd FROM link WHERE namee=%s """, (u))
    b = cursor.fetchone()
    c = b[0]
    return send_file(c)


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/2_home')
def second_home():

    if session['logged_in'] == True:
        user = request.form['username']
        return render_template("profile.html",value=user)
    else:
        return home()


@app.route('/login', methods=['POST'])
def do_admin_login():
    check_user=request.form['username']
    if check_user=="":
        return home()
    if cursor2.execute("""SELECT pass_word FROM login_signup WHERE username=%s """ ,(check_user)) == True:
        pass_with = cursor2.fetchone()
        pass_out = pass_with[0]


        if request.form['password'] == pass_out and request.form['username'] == check_user:
            session['logged_in'] = True
            return second_home()
        else:
            flash('wrong credentials')
            return home()
    else:
        flash('wrong credentials')
        return home()





@app.route('/logout')
def logout():
    session['logged_in'] = False
    return second_home()


@app.route('/signup')
def sign_up():
    return render_template("sign_up.html")


@app.route('/ac_created',methods={'POST'})
def account():
    if request.form['first_name']=="":
        return sign_up()
    if request.form['last_name']=="":
        return sign_up()
    if request.form['username']=="":
        return sign_up()
    if request.form['password']=="":
        return sign_up()
    if request.form['email']=="":
        return sign_up()


    cursor2.execute("""INSERT INTO login_signup(username,first_name,last_name,pass_word ,email)VALUES(%s,%s,%s,%s,%s)""",(request.form['username'],request.form['first_name'],request.form['last_name'],request.form['password'],request.form['email']))
    mink.commit()
    f_name = request.form['first_name']
    session['logged_in'] = True
    return render_template('account.html', value=f_name)



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)