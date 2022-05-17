from flask import Flask, render_template,request,flash,redirect,url_for,session
import sqlite3
from sqlite3 import Error
import os


app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

#Login Page -- Home page
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect(r"database\shopifyimgrepo.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from users where email=? and pass=?",(name,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["fname"]
            session["userid"]=data["user_id"]
            return redirect("profile")
        else:
            print("Username and Password Mismatch")
    return redirect(url_for("index"))

# Register Page -- Home page
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            fname=request.form['fname']
            passw=request.form['lname']
            username=request.form['username']
            contact=request.form['contact']
            mail=request.form['mail']
            con=sqlite3.connect(r"database\shopifyimgrepo.db")
            cur=con.cursor()
            cur.execute("insert into users(user_id,email,fname,pass,phone)values(?,?,?,?,?)",(username,mail,fname,passw,contact))
            cur.execute("insert into login_info(email,pass)values(?,?)",(mail,passw))
            con.commit()
            print("Record Added  Successfully success")
        except:
            print("Error in Insert Operation danger")
        finally:
            con.close()
            return redirect(url_for("index"))
            
    return redirect(url_for("index"))

# Profile page -- after login
@app.route('/profile',methods=["GET","POST"])
def profile():
    return render_template("profile.html")

# Profile page -- logout button
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run()