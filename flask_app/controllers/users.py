from flask_app import app
from flask import render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models import user
bcrypt = Bcrypt(app)

@app.route("/")
def index():

    return render_template("index.html") 

@app.route("/register", methods=["POST"])
def register():
    if not user.User.is_valid(request.form):
        return redirect(url_for("index"))
    else:
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "username": request.form["username"],
            "email": request.form["email"],
            "password": bcrypt.generate_password_hash(request.form["password"])
        }
        user.User.create(data)
        return redirect(url_for("login_form"))
            
    
@app.route("/login_form")
def login_form():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    data = {
        "email": request.form["email"]
    }
    user_from_db = user.User.get_by_email(data)
    print(user_from_db)
    
    if not user_from_db:
        flash("Invalid login")
        return redirect(url_for("login_form"))
    if not bcrypt.check_password_hash(user_from_db.password, request.form["password"]):
        flash("Invalid login")
        return redirect(url_for("login_form"))
    
    session["logged_in"] = user_from_db.id
    return redirect(url_for("dashboard"))