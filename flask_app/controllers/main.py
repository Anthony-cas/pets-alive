from flask_app import app
from flask import render_template, session, url_for, redirect, request
from flask_app.models import dog, user
from flask import flash

@app.route("/dashboard")
def dashboard():
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    user_from_db = user.User.get_by_id({"id":int(session["logged_in"])})
    all_dogs = dog.Dog.get_all()
    print(all_dogs)
    return render_template("dashboard.html", all_dogs = all_dogs, user=user_from_db)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))