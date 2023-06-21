from flask_app import app
from flask import render_template, session, url_for, redirect, request
from flask_app.models import dog
from flask import flash

@app.route("/dogs/create")
def add_dog():
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    user_id = session['logged_in']
    return render_template("add_dog.html", user_id=user_id)

@app.route("/dog/process", methods=["POST"])
def create_dog():

    if not dog.Dog.is_valid(request.form):
        return redirect(url_for("add_dog"))
    else:
        data = {
            # "id" : id,
            "breed" : request.form["breed"],
            "name" : request.form["name"],
            "age" : request.form["age"],
            "description" : request.form["description"],
            "users_id" : int(session["logged_in"])
        }
        print(data)
        dog.Dog.create(data)
        return redirect("/dashboard")

@app.route("/dogs/edit/<int:id>")
def edit_dog(id):
    one_dog = dog.Dog.get_one_with_user({"id" : id})
    return render_template("edit_dog.html", one_dog = one_dog)


@app.route("/dog/update/<int:id>", methods=["POST"])
def update_dog(id):
    if not dog.Dog.is_valid(request.form):
        return redirect(url_for("edit_dog"))
    else:
        data = {
            "id" : id,
            "breed" : request.form["breed"],
            "name" : request.form["name"],
            "age" : request.form["age"],
            "description" : request.form["description"],
            "user_id" : int(session["logged_in"])
        }
        dog.Dog.update(data)
    return redirect("/dashboard")
    

@app.route("/dog/<int:id>")
def one_dog(id):
    user_id = int(session["logged_in"])
    dog_in_db = dog.Dog.get_one_with_user({"id": id})
    return render_template("one_dog.html", one_dog = dog_in_db, user_id = user_id)

@app.route("/dogs/delete/<int:id>")
def destroy(id):
    dog.Dog.destroy({"id": id})
    return redirect(url_for("dashboard"))