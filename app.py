from urllib import response
from flask import Flask, render_template,request,flash,redirect,url_for,session
import sqlite3
from sqlite3 import Error
import os
from werkzeug.utils import secure_filename

from util_shopify import *

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Home Page
@app.route('/')
def index():
    rows = []
    try:
        conn=sqlite3.connect(r"database\shopifyimgrepo.db")
        conn.row_factory=sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("select * from image_information")
        rows = cursor.fetchall()
        conn.close()
    except sqlite3.Error as error:
        print(error)
        flash("Something went wrong while uploading file to database!")
    return render_template('index.html', response=rows)

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
            flash("Username/Password incorrect!", "error")
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
            con.commit()
            print("Record Added  Successfully success")
            flash("User registered successfully!", "success")
        except:
            print("Error on registration!", "danger")
        finally:
            con.close()
            return redirect(url_for("index"))
            
    return redirect(url_for("index"))

# Profile page -- after login
@app.route('/profile',methods=["GET","POST"])
def profile():
    if session["userid"]:
        rows = []
        # print(session["userid"])
        try:
            conn=sqlite3.connect(r"database\shopifyimgrepo.db")
            conn.row_factory=sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("select * from image_information where seller=(?)",(session["userid"],))
            rows = cursor.fetchall()
            conn.close()
        except sqlite3.Error as error:
            print(error)
            flash("Something went wrong while uploading file to database!")
        return render_template('profile.html', response = rows)
    else:
        return render_template('index.html')

# Profile page -- logout button
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

# Upload images -- profile page
@app.route('/upload_img', methods=['GET','POST'])
def upload_img():
    if request.method == 'POST':
        # print(request.form)
        # print(request.files)
        name_img=request.form['iname']
        price=request.form['price']
        destination_path=""
        fileobj = request.files['file']
        file_extensions =  ["JPG","JPEG","PNG","GIF"]
        uploaded_file_extension = fileobj.filename.split(".")[1]
        #validating file extension
        if(uploaded_file_extension.upper() in file_extensions):
            destination_path= f"static/temp_imgs/{fileobj.filename}"
            fileobj.save(destination_path)
            destination_path= f"temp_imgs/{fileobj.filename}"
        try:   
            con=sqlite3.connect(r"database\shopifyimgrepo.db")
            cur=con.cursor()
            cur.execute("insert into image_information(seller,img_name,imgLink,discount,price)values(?,?,?,?,?)",(session["userid"],name_img,destination_path,0,price))
            con.commit()
            print("Record Added  Successfully success")
            flash("Image Added Successfully")
        except sqlite3.Error as error:
            flash(f"{error}", "danger")
        finally:
            con.close()
    return redirect(url_for("profile"))

# Remove image -- profile page
@app.route('/remove_img', methods=['GET','POST'])
def remove_img():
    if request.method == 'POST' and request.form['confirm'] == 'Confirm':
        id_img = request.form['id_img']
        try:
            conn=sqlite3.connect(r"database\shopifyimgrepo.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM image_information WHERE id=(?)",(id_img,))
            conn.commit()
            conn.close()
        except sqlite3.Error as error:
            print(error)
            flash("Something went wrong while uploading file to database!")
    return redirect(url_for("profile"))


# Add discount -- profile page
@app.route('/add_discount', methods=['GET','POST'])
def add_discount():
    id_img = request.form['id_img']
    discount = request.form['discount']
    print(request.form)
    try:
        conn=sqlite3.connect(r"database\shopifyimgrepo.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE image_information SET discount=(?) WHERE id=(?)",(discount,id_img))
        conn.commit()
        conn.close()
    except sqlite3.Error as error:
        print(error)
        flash("Something went wrong while uploading file to database!")
    return redirect(url_for("profile"))


# item bought -- Buy page
@app.route('/buy_page/<id_img>', methods=['GET','POST'])
def buy_page(id_img):
    if session["userid"]:
        try:
            conn=sqlite3.connect(r"database\shopifyimgrepo.db")
            conn.row_factory=sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("select * from image_information where id=(?)",(id_img,))
            row = cursor.fetchone()
            conn.close()
        except sqlite3.Error as error:
            print(error)
            flash("Something went wrong while uploading file to database!")
        return render_template('buy.html', response = row)
    else:
        return redirect(url_for("index"))


# Buy page
@app.route('/buy_item/<id_img>', methods=['GET','POST'])
def buy_item(id_img):
    if session["userid"]:
        try:
            conn=sqlite3.connect(r"database\shopifyimgrepo.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE image_information SET seller=(?) WHERE id=(?)",(session["userid"],id_img))
            conn.commit()
            conn.close()
        except sqlite3.Error as error:
            print(error)
            flash("Something went wrong while uploading file to database!")
        return render_template('order_confirmation.html')
    else:
        return redirect(url_for("index"))

if __name__ == '__main__':
    app.run()