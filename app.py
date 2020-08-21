import os
from flask import Flask, flash, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_members")
def get_members():
    members = mongo.db.team_members.find()
    return render_template("members.html", members=members)


@app.route("/register", methods=["GET", "POST"])
def register():
    print("register in process")
    if request.method == "POST":
        existing_user = mongo.db.team_members.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        new_member = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "first_name": request.form.get("first_name").lower(),
            "last_name": request.form.get("last_name").lower(),
            "fitness": request.form.get("fitness"),
            "stamina": request.form.get("stamina"),
            "strength": request.form.get("strength"),
            "speed": request.form.get("speed"),
            "quote": request.form.get("slogan")
        }
        mongo.db.team_members.insert_one(new_member)

        session["member"] = request.form.get("username").lower()
        flash("Registration Successful!")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    print("loggin in")
    if request.method == "POST":
        print("it's a post method")
        existing_user = mongo.db.team_members.find_one(
            {"username": request.form.get("username").lower()})
        print(existing_user)
        if existing_user:
            print("this is an exisiting user")
            print(check_password_hash(existing_user["password"], request.form.get("password")))
            if check_password_hash(existing_user["password"], request.form.get("password")):
                print("Matching password")
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("get_members"))

        else:
            return redirect(url_for("login"))
    return render_template("login.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
