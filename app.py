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
    if session.get("user"):
        if request.method == "POST":
            if request.form["action"] == "blog":
                print("this is a blog post")
                new_post = {
                    "title": request.form.get("title"),
                    "description": request.form.get("main-content"),
                    "author": session["user"],
                    "category": "blog-post",
                }
                mongo.db.posts.insert_one(new_post)
                return redirect(url_for("training_blog"))
            elif request.form["action"] == "workout":
                new_post = {
                    "title": request.form.get("title"),
                    "date": request.form.get("date"),
                    "time": request.form.get("time"), 
                    "duration": request.form.get("duration"),
                    "location": request.form.get("location"),
                    "description": request.form.get("description"),
                    "author": session["user"],
                    "category": "workout"
                }
                mongo.db.posts.insert_one(new_post)
                return redirect(url_for("training_blog"))
        posts = list(mongo.db.posts.find().sort("$natural", -1))
        comments = list(mongo.db.comments.find())
        attendants = list(mongo.db.attendants.find())
        attends = False
        return render_template("training_blog.html", posts=posts, comments=comments, attendants=attendants, attends=attends)
    return redirect(url_for("login"))


@app.route("/edit_workout/<post_id>", methods=["GET", "POST"])
def edit_workout(post_id):
    if request.method == "POST":
        updated_post = {
                    "title": request.form.get("title"),
                    "date": request.form.get("date"),
                    "time": request.form.get("time"), 
                    "duration": request.form.get("duration"),
                    "location": request.form.get("location"),
                    "description": request.form.get("description"),
                    "author": session["user"],
                    "category": "workout"
                }
        mongo.db.posts.update({"_id": ObjectId(post_id)}, updated_post)
        flash("Your post was successfully updated.", "success-flash")
        return redirect(url_for("training_blog"))
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    return render_template("edit_workout.html", post=post)


@app.route("/edit_blog/<post_id>", methods=["GET", "POST"])
def edit_blog(post_id):
    if request.method == "POST":
        updated_post = {
                    "title": request.form.get("title"),
                    "description": request.form.get("main-content"),
                    "author": session["user"],
                    "category": "blog-post"
                }
        mongo.db.posts.update({"_id": ObjectId(post_id)}, updated_post)
        flash("Your post was successfully updated.", "success-flash")
        return redirect(url_for("training_blog"))
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    return render_template("edit_blog.html", post=post)


@app.route("/delete_workout/<post_id>", methods=["GET", "POST"])
def delete_workout(post_id):
    mongo.db.posts.remove({"_id": ObjectId(post_id)})
    mongo.db.attendants.remove({"post_id": ObjectId(post_id)})
    flash("Post successfully deleted", "success-flash")
    return redirect(url_for("training_blog"))


@app.route("/delete_blog/<post_id>", methods=["GET", "POST"])
def delete_blog(post_id):
    mongo.db.comments.remove({"post_id": ObjectId(post_id)})
    mongo.db.posts.remove({"_id": ObjectId(post_id)})
    flash("Post successfully deleted", "success-flash")
    return redirect(url_for("training_blog"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get('user'):
        return redirect(url_for("get_members"))
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
                flash("Welcome, {}".format(
                    current_runner["first_name"]), "success-flash")
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
        users_posts = list(mongo.db.posts.find({"author": session["user"]}))
        all_posts = list(mongo.db.posts.find())
        attendants = list(mongo.db.attendants.find({"attendant": session["user"]}))   
        member = mongo.db.team_members.find_one(
            {"username": session["user"]})
        return render_template("profile.html", member=member, all_posts=all_posts, users_posts=users_posts, attendants=attendants)
    else:
        return redirect(url_for("login"))

    
@app.route("/edit_profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    if request.method == "POST":
        updated_profile = {
            "username": mongo.db.team_members.find_one({"_id": ObjectId(user_id)})["username"],
            "password": mongo.db.team_members.find_one({"_id": ObjectId(user_id)})["password"],
            "first_name": request.form.get("first_name").lower(),
            "last_name": request.form.get("last_name").lower(),
            "fitness": request.form.get("fitness"),
            "stamina": request.form.get("stamina"),
            "strength": request.form.get("strength"),
            "speed": request.form.get("speed"),
            "quote": request.form.get("slogan")
        }

        mongo.db.team_members.update({"_id": ObjectId(user_id)}, updated_profile)
        username = mongo.db.team_members.find_one({"_id": ObjectId(user_id)})["username"]
        flash("Profile successfully updated", "success-flash")
        return redirect(url_for("profile", username=username))
    member = mongo.db.team_members.find_one({"_id": ObjectId(user_id)})
    return render_template("edit_profile.html", member=member)


@app.route("/delete_member/<member_id>", methods=["GET", "POST"])
def delete_member(member_id):
    print(member_id)
    delete_posts(member_id)
    mongo.db.comments.remove({"author": session["user"]})
    mongo.db.attendants.remove({"attendant": session["user"]})
    mongo.db.team_members.remove({"_id": ObjectId(member_id)})
    flash("Team member deleted", "success-flash")
    return redirect(url_for("logout"))

def delete_posts(member_id):
    mongo.db.posts.remove({"author": mongo.db.team_members.find_one({"_id": ObjectId(member_id)})["username"]})


@app.route("/add_comment/<username>/<post_id>", methods=["GET", "POST"])
def add_comment(username, post_id):
    if request.method == "POST":
        comment = {
           "post_id": ObjectId(post_id),
           "comment": request.form.get("comment"),
           "author": username 
        }
        mongo.db.comments.insert_one(comment)
        return redirect(url_for("training_blog"))


@app.route("/attend/<username>/<post_id>")
def attend(username, post_id):
    print(username)
    attending_user = mongo.db.attendants.find_one({"attendant": username, "post_id": ObjectId(post_id)})
    print(attending_user)
    if attending_user:
        mongo.db.attendants.remove(attending_user)
        return redirect(url_for("training_blog"))
    else:
        attendant = {
            "post_id": ObjectId(post_id),
            "attendant": username
        }
    mongo.db.attendants.insert_one(attendant)
    attendants = mongo.db.attendants.find()
    return redirect(url_for("training_blog", attendants=attendants ))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('get_members'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
