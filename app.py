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


@app.route("/training_blog", methods=["GET", "POST"])
def training_blog():
    if request.method == "POST":
        new_post = {
            "title": request.form.get("title"),
            "description": request.form.get("main-content"),
            "author": session["user"],
            "category": "blog-post",
        }
        mongo.db.posts.insert_one(new_post)
        return redirect(url_for("training_blog"))
    posts = list(mongo.db.posts.find().sort("$natural", -1))
    return render_template("training_blog.html", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    print("register in process")
    if request.method == "POST":
        existing_user = mongo.db.team_members.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists", "error-flash")
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

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!", "success-flash")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get('user'):
        print("User already logged in")
        return redirect(url_for("get_members"))
    elif request.method == "POST":
        existing_user = mongo.db.team_members.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                current_runner = mongo.db.team_members.find_one(
                    {"username": session["user"]})
                flash("Welcome, {}".format(current_runner["first_name"]), "success-flash")
                return redirect(url_for("profile", username=session["user"]))
            else:
                flash("Username and/or password is incorrect.", "error-flash")
                return render_template("login.html")

        else:
            flash("Username does not exist", "error-flash")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    if session.get('user'):
        first_name = mongo.db.team_members.find_one({"username": session["user"]})["first_name"]
        print(username)
        return render_template("profile.html", first_name=first_name)
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('get_members'))    

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
