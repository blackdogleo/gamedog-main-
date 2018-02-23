from flask import Flask,render_template,send_file,flash,redirect,request,session,abort,url_for,Response
import MySQLdb
import os
import time
from flask_cors import CORS

jink = MySQLdb.connect("Rsj","ruturaj","ruturaj","active")

cursor = jink.cursor()

mink = MySQLdb.connect("Rsj","ruturaj","ruturaj","active")
cursor2 = mink.cursor()

article_store = MySQLdb.connect("Rsj","ruturaj","ruturaj","active")
cursor3 = article_store.cursor()


app = Flask(__name__)
CORS(app)

APP_ROUTE = os.path.dirname(os.path.abspath(__file__))


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


@app.route('/login/myprofile/<user>')
def is_logged(user):

    if session['logged_in'] == True:

        return render_template("profile.html", value=user)



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


@app.route('/game_rec/<user>', methods=['GET','POST'])
def game_rec(user):
    genre = request.form['selected_genre']
    cursor2.execute("""SELECT game_link FROM game_rec WHERE genre=%s""", genre)
    link = cursor2.fetchone()
    link_ok = link[0]
    mink.commit()

    return render_template(link_ok,value=user)


@app.route('/login/myarticles/<user>')
def my_articles(user):

    return render_template('my_articles.html',value=user)


@app.route('/login/my_articles/<user>')
def pro_art(user):

    fout1= open('templates/profile_articles.html','w')
    fout2 = open('text files/your_art0', 'r')
    fout3 = open('text files/your_art1', 'r')
    begin_tag=fout2.read()
    fout1.write(begin_tag)
    cursor3.execute("""SELECT art_name,art_link,art_time FROM article_desk WHERE username=%s""", user)
    article_list = cursor3.fetchall()
    a_list = list(article_list)
    a_list.reverse()
    fout = open('text files/art_info.txt', 'w')

    for contents in a_list:
        post_name = contents[0]
        link_name = contents[1]
        time_data = contents[2]
        # tags needed
        start_tag = "<h4><a href='/gallery/" + link_name + "/"+user+"'>"
        middle_tag1 = post_name + "</a></h4>"
        middle_tag2 = "</br>"
        middle_tag3 = "<h6>Published on " + time_data + "</h6>"+"</br>"

        end_tag = "<hr>"
        all_tag = start_tag + middle_tag1 + middle_tag2 + middle_tag3 + end_tag
        fout.write(all_tag)

    fout = open('text files/art_info.txt', 'r')
    inter_tag=fout.read()
    fout1.write(inter_tag)
    last_tag=fout3.read()
    fout1.write(last_tag)
    fout1.close()
    article_store.commit()

    return render_template('profile_articles.html',value=user)

@app.route('/gallery/articles/<link_value>/<user>')
def gallery(link_value,user):
    art_link="articles/"+link_value
    return render_template(art_link,value=user)


@app.route('/login/2_articles/<user>', methods=['POST'])
def to_articles(user):
    # uploading images to our Server
    target=os.path.join(APP_ROUTE, 'static/articles')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    for filea in request.files.getlist('article_art'):
        print(filea)
        filename=filea.filename
        destination= '/'.join([target,filename])
        print(destination)
        filea.save(destination)
        image_link ='/'+ destination[41:]

    content = request.form['summer']
    heading = request.form['name_title']
    only_name=user+"_"+heading+".html"
    in_temp_file = "articles/" + only_name
    file_name="templates/"+in_temp_file

    fout = open(file_name,'w')
    fout0 = open('text files/before_content.txt', 'r')
    fout2 = open('text files/after_content.txt', 'r')
    content = content.encode('ascii', 'ignore').decode('ascii')
    heading = heading.encode('ascii', 'ignore').decode('ascii')
    head = "<h1>"+heading+"</h1>"
    start_tag = fout0.read()
    end_tag = fout2.read()
    fout.write(start_tag)
    fout.write(head)
    fout.write(content)
    fout.write(end_tag)
    fout.close()
    take_time = time.localtime()
    art_time = str(take_time[0])+"-"+str(take_time[1])+"-"+str(take_time[2])+" "+str(take_time[3])+"-"+str(take_time[4])+"-"+str(take_time[5])
    cursor3.execute("""INSERT INTO article_desk(username,art_name,art_link,art_time,image_link)VALUES(%s,%s,%s,%s,%s)""",
                    (user, heading, in_temp_file, art_time,image_link))
    article_store.commit()
    return pro_art(user)





@app.route('/explore/<user>')
def explore(user):
    fout1 = open('templates/explore.html', 'w')
    fout2 = open('text files/explore0', 'r')
    fout3 = open('text files/explore1', 'r')
    begin_tag = fout2.read()
    fout1.write(begin_tag)
    cursor3.execute("""SELECT username,art_name,art_link,art_time,image_link FROM article_desk""")
    article_list = cursor3.fetchall()
    a_list = list(article_list)
    a_list.reverse()
    fout = open('text files/explore_card_info.txt', 'w')

    for contents in a_list:
        user_name = contents[0]
        post_name = contents[1]
        link_name = contents[2]
        time_data = contents[3]
        img_link = contents[4]
        # tags needed

        start_tag='<div class="card" style="width: 24rem;">'
        img_tag = '<img class="card-img-top" src="' + img_link + '" alt="Card image cap">'
        after_img = ' <span class="border border-info">'
        after_img1 = '<div class="card-body" style="background-color:#f29941;">'
        post_tag = ' <h5 class="card-title">' + post_name + '</h5>'
        author_tag = '<p class="card-text" >' + 'published by ' + user_name + ' on ' + time_data + '</p>'
        link_tag = '<a href="' + '/gallery/' + link_name + '/' +user_name + '" class="btn btn-info">Go to article</a>'
        end_tag=' </div></span></div></br><hr>'
        all_tag = start_tag+img_tag + after_img + after_img1 + post_tag + author_tag + link_tag+end_tag
        fout.write(all_tag)

    fout = open('text files/explore_card_info.txt', 'r')
    inter_tag = fout.read()
    fout1.write(inter_tag)
    last_tag = fout3.read()
    fout1.write(last_tag)
    fout1.close()
    article_store.commit()
    return render_template('explore.html',value=user)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)