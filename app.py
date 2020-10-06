import os
import random
import string
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (Flask, flash, render_template, redirect, request,
                   url_for, session)
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

@app.route("/")
@app.route("/get_events")
def get_events():
    events = list(mongo.db.events.find())
    if session.get("user"):
        user = mongo.db.team_members.find_one({"username": session["user"]})
        return render_template("events.html", events=events, user=user)
    return render_template("events.html", events=events)


# Query mongoDB for all team members and send to template.
@app.route("/get_members")
def get_members():
    members = mongo.db.team_members.find()
    return render_template("members.html", members=members,
                           active_tab="workout")


# Query mongoDB for all posts, comments and attendants and send to template.
@app.route("/get_posts")
@app.route("/get_posts/<active_tab>")
def get_posts(active_tab = "workouts"):
    if session.get("user"):
        workouts = list(mongo.db.posts.find(
            {"category": "workout"}).sort("$natural", -1))
        blogs = list(mongo.db.posts.find(
            {"category": "blog-post"}).sort("$natural", -1))
        comments = list(mongo.db.comments.find().sort("$natural", -1))
        attendants = list(mongo.db.attendants.find())
        return render_template("training_blog.html", workouts=workouts,
                               blogs=blogs, comments=comments,
                               attendants=attendants,
                               active_tab=active_tab, redirect_to="get_posts")
    return redirect(url_for("login"))


# Route for adding a new post. First check if there's a user cookie. If
# not, redirect user to login login route. If there's a user and and
# request is POST, check if form action is 'blog' or 'workout'. Then
# insert data from form into database. If not post, redirect to route for
# 'get_members'.
@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    if session.get("user"):
        if request.method == "POST":
            if request.form["action"] == "blog":
                new_post = {
                    "title": request.form.get("blog-title"),
                    "description": request.form.get("main-content"),
                    "author": session["user"],
                    "category": "blog-post",
                    "element_id": get_random_string(20)
                }
                mongo.db.posts.insert_one(new_post)
                return redirect(url_for("get_posts", active_tab="blog"))
            elif request.form["action"] == "workout":
                new_post = {
                    "title": request.form.get("workout-title"),
                    "date": request.form.get("date"),
                    "time": request.form.get("time"),
                    "duration": request.form.get("duration"),
                    "location": request.form.get("location"),
                    "description": request.form.get("description"),
                    "author": session["user"],
                    "category": "workout",
                    "element_id": get_random_string(20)
                }
                mongo.db.posts.insert_one(new_post)
                return redirect(url_for("get_posts"))
        return redirect(url_for("get_posts"))
    return redirect(url_for("login"))


# Route for editing workout. First check if there's a user cookie.
# If not, return to login. Else, check if user owns the post. If
# not, flash error message. Else, if POST, update record. Else, render
# template.
@app.route("/edit_workout/<post_id>/<redirect_to>", methods=["GET", "POST"])
def edit_workout(post_id, redirect_to):
    if session.get("user"):
        if owns_post(post_id):
            if request.method == "POST":
                updated_post = {
                    "title": request.form.get("title"),
                    "date": request.form.get("date"),
                    "time": request.form.get("time"),
                    "duration": request.form.get("duration"),
                    "location": request.form.get("location"),
                    "description": request.form.get("description"),
                    "author": session["user"],
                    "category": "workout",
                    "element_id": get_random_string(20)
                }
                mongo.db.posts.update({"_id": ObjectId(post_id)}, updated_post)
                flash("Your post was successfully updated.", "success-flash")
                if redirect_to == "profile":
                    return redirect(url_for(
                        "profile", username=session["user"]))
                return redirect(url_for("get_posts"))
            post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
            return render_template(
                "edit_workout.html", post=post, redirect_to=redirect_to)
        flash("Authentication failed", "error-flash")
    return redirect(url_for("login"))


# Route for editing blog post. First check if there's a user cookie.
# If not, return to login. Else, check if user owns the post. If
# not, flash error message. Else, if POST, update record. Else, render
# template page.
@app.route("/edit_blog/<post_id>/<redirect_to>", methods=["GET", "POST"])
def edit_blog(post_id, redirect_to):
    if session.get("user"):
        if owns_post(post_id):
            if request.method == "POST":
                updated_post = {
                    "title": request.form.get("title"),
                    "description": request.form.get("main-content"),
                    "author": session["user"],
                    "category": "blog-post",
                    "element_id": get_random_string(20)
                }
                mongo.db.posts.update({"_id": ObjectId(post_id)}, updated_post)
                flash("Your post was successfully updated.", "success-flash")
                if redirect_to == "profile":
                    return redirect(url_for(
                        "profile", username=session["user"]))
                return redirect(url_for("get_posts", active_tab="blog"))
            post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
            return render_template(
                "edit_blog.html", post=post, redirect_to=redirect_to)
        flash("Authentication failed.", "error-flash")
    return redirect(url_for("login"))


# Route for editing comment. First check if there's a user cookie.
# If not, return to login. Else, check if user owns the comment. If
# not, flash error message. Else, if POST, update record. Return to blog
# page. Else, render template.
@app.route("/edit_comment/<comment_id>/<post_id>", methods=["GET", "POST"])
def edit_comment(comment_id, post_id):
    if session.get("user"):
        if owns_comment(comment_id):
            if request.method == "POST":
                updated_comment = {
                    "post_id": ObjectId(post_id),
                    "comment": request.form.get("comment"),
                    "author": session["user"],
                    "element_id": get_random_string(20)
                }
                mongo.db.comments.update(
                    {"_id": ObjectId(comment_id)}, updated_comment)
                flash("Your comment was successfully updated.",
                      "success-flash")
                return redirect(url_for("get_posts", active_tab="blog"))
            comment = mongo.db.comments.find_one({"_id": ObjectId(comment_id)})
            return render_template("edit_comment.html", comment=comment,
                                   post_id=post_id)
        flash("Authentication failed", "error-flash")
    return redirect(url_for("login"))


# Route for deleting comment. First check if there's a user cookie.
# If not, return to login. Else, check if user owns the comment. If
# not, flash error message. Else, remove record. Return to blog page.
@app.route("/delete_comment/<comment_id>")
def delete_comment(comment_id):
    if session.get("user"):
        if owns_comment(comment_id):
            mongo.db.comments.remove({"_id": ObjectId(comment_id)})
            flash("Comment successfully deleted", "success-flash")
            return redirect(url_for("get_posts", active_tab="blog"))
        flash("Authentication failed", "error-flash")
        return redirect(url_for("get_posts", active_tab="blog"))
    return redirect(url_for("login"))


# Route for deleting workout post. First check if there's a user cookie.
# If not, return to login. Else, check if user owns the current post. If
# not, flash error message. Else, remove record. Return to blog page.
@app.route("/delete_workout/<post_id>/<redirect_to>", methods=["GET", "POST"])
def delete_workout(post_id, redirect_to):
    if session.get("user"):
        if owns_post(post_id):
            mongo.db.posts.remove({"_id": ObjectId(post_id)})
            mongo.db.attendants.remove({"post_id": ObjectId(post_id)})
            flash("Post successfully deleted", "success-flash")
            if redirect_to == "profile":
                return redirect(url_for("profile", username=session["user"]))
            return redirect(url_for("get_posts"))
        flash("Authentication failed.", "error-flash")
    return redirect(url_for("login"))


# Route for deleting blog post. First check if there's a user cookie.
# If not, return to login. Else, check if user owns the current post. If
# not, flash error message. Else, remove record. Return to blog page.
@app.route("/delete_blog/<post_id>/<redirect_to>", methods=["GET", "POST"])
def delete_blog(post_id, redirect_to):
    if session.get("user"):
        if owns_post(post_id):
            mongo.db.comments.remove({"post_id": ObjectId(post_id)})
            mongo.db.posts.remove({"_id": ObjectId(post_id)})
            flash("Post successfully deleted", "success-flash")
            if redirect_to == "profile":
                return redirect(url_for("profile", username=session["user"]))
            return redirect(url_for("get_posts", active_tab="blog"))
        flash("Authentication failed.", "error-flash")
    return redirect(url_for("login"))


# Route for registering a new user. First check if there's a user cookie.
# If so, redirect to get_members route. Else check if method is POST. If
# so, check if username is already in database. If so, flash an error
# message and redirect. If not, insert data from form into database with
# hashed password field. Redirect to profile page.
@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get('user'):
        return redirect(url_for("get_members"))
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
            "quote": request.form.get("slogan"),
            "img": request.form.get("img-url")
        }
        mongo.db.team_members.insert_one(new_member)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!", "success-flash")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


# Route for logging in. First check for user cookie. If so, redirect to
# get_members route. Else, if method is POST, check if username exists,
# if not flash error message and redirect. Else, check if entered
# password matches that of existing_user-variable. If so, assign username
# to cookie and display success flash message. If not, display error
# message and redirect.
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get('user'):
        return redirect(url_for("get_members"))
    elif request.method == "POST":
        existing_user = mongo.db.team_members.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            if check_password_hash(existing_user["password"],
                                   request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                current_runner = mongo.db.team_members.find_one(
                    {"username": session["user"]})
                flash("Welcome, {}".format(
                    current_runner["first_name"].capitalize()),
                    "success-flash")
                return redirect(url_for("profile", username=session["user"]))
            else:
                flash("Username and/or password is incorrect.", "error-flash")
                return render_template("login.html")
        else:
            flash("Username does not exist", "error-flash")
            return redirect(url_for("login"))
    return render_template("login.html")


# Route for profile page. Check if there's a user cookie. If so,
# Query database for all posts by user and all workout-potsts the user
# is attending. Send these to template. If not, redirect to login.
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    if session.get('user'):
        users_posts = list(mongo.db.posts.find({"author": session["user"]}))
        all_posts = list(mongo.db.posts.find())
        attendants = list(mongo.db.attendants.find(
            {"attendant": session["user"]}))
        member = mongo.db.team_members.find_one(
            {"username": session["user"]})
        return render_template("profile.html", member=member,
                               all_posts=all_posts, users_posts=users_posts,
                               attendants=attendants,
                               redirect_to="profile")
    return redirect(url_for("login"))


# Route for editing profile. First check for user cookie. If not, return
# to login. Else, check if user cookie matches user_id. If not, return to
# logout with error flash. Else, and if POST, update record. Else, return
# template.
@app.route("/edit_profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    if session.get("user"):
        if owns_account(user_id):
            if request.method == "POST":
                updated_profile = {
                    "username": mongo.db.team_members.find_one(
                        {"_id": ObjectId(user_id)})["username"],
                    "password": mongo.db.team_members.find_one(
                        {"_id": ObjectId(user_id)})["password"],
                    "first_name": request.form.get("first_name").lower(),
                    "last_name": request.form.get("last_name").lower(),
                    "fitness": request.form.get("fitness"),
                    "stamina": request.form.get("stamina"),
                    "strength": request.form.get("strength"),
                    "speed": request.form.get("speed"),
                    "quote": request.form.get("slogan"),
                    "img": request.form.get("img-url")
                }

                mongo.db.team_members.update(
                    {"_id": ObjectId(user_id)}, updated_profile)
                username = mongo.db.team_members.find_one(
                    {"_id": ObjectId(user_id)})["username"]
                flash("Profile successfully updated", "success-flash")
                return redirect(url_for("profile", username=username))
            member = mongo.db.team_members.find_one({"_id": ObjectId(user_id)})
            return render_template("edit_profile.html", member=member)
        flash("Authentication failed", "error-flash")
        return redirect(url_for("logout"))
    return redirect(url_for("login"))


# Route for updating image url. If POST, update record. Else, return
# template.
@app.route("/edit_img/<member_id>", methods=["GET", "POST"])
def edit_img(member_id):
    if request.method == "POST":
        mongo.db.team_members.update({"_id": ObjectId(member_id)},
                                     {"$set":
                                     {"img": request.form.get("img-url")}})
        return redirect(url_for("profile", username=session["user"]))
    return redirect(url_for("profile", username=session["user"]))


# Route for deleting profile. First, check for user cookie. If not,
# return to logout. Else, check that user owns the profile. If not,
# return to logout with error flash. Else, removeuser's records of
# comments, attendants and the profile itself. Return to logout.
@app.route("/delete_member/<member_id>", methods=["GET", "POST"])
def delete_member(member_id):
    if session.get("user"):
        if owns_account(member_id):
            delete_posts(member_id)
            mongo.db.comments.remove({"author": session["user"]})
            mongo.db.attendants.remove({"attendant": session["user"]})
            mongo.db.team_members.remove({"_id": ObjectId(member_id)})
            flash("Team member deleted", "success-flash")
            return redirect(url_for("logout"))
        flash("Authentication failed", "error-flash")
    return redirect(url_for("logout"))


def delete_posts(member_id):
    mongo.db.posts.remove({"author": mongo.db.team_members.find_one(
        {"_id": ObjectId(member_id)})["username"]})


# Route for adding a comment. If POST, insert data.
@app.route("/add_comment/<username>/<post_id>", methods=["GET", "POST"])
def add_comment(username, post_id):
    if request.method == "POST":
        comment = {
            "post_id": ObjectId(post_id),
            "comment": request.form.get("comment"),
            "author": username,
            "element_id": get_random_string(20)
        }
        mongo.db.comments.insert_one(comment)
        return redirect(url_for("get_posts", active_tab="blog"))
    return redirect(url_for("get_posts", active_tab="blog"))


# Route for attending a workout. First check if there's a record with
# the user's username and post_id matching post_id argument. If
# not, insert data. Else, remove record. Return to blog.
@app.route("/attend/<username>/<post_id>/<redirect_to>")
def attend(username, post_id, redirect_to):
    attending_user = mongo.db.attendants.find_one(
        {"attendant": username, "post_id": ObjectId(post_id)})
    if attending_user:
        mongo.db.attendants.remove(attending_user)
        if redirect_to == "profile":
            return redirect(url_for("profile", username=session["user"]))
        return redirect(url_for("get_posts"))
    else:
        attendant = {
            "post_id": ObjectId(post_id),
            "attendant": username
        }
        mongo.db.attendants.insert_one(attendant)
        if redirect_to == "profile":
            return redirect(url_for("profile", username=session["user"]))
        return redirect(url_for("get_posts"))


# Route for logging out. Removes session cookie.
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('get_members'))


# Generate random string. https://pynative.com/python-generate-random-string
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


# Defensive function to prevent brute force deleting and editing,
# of comments that the user did not create. Checks if the session user
# matches the "author" field of the comment.
def owns_comment(comment_id):
    comment = mongo.db.comments.find_one({"_id": ObjectId(comment_id)})
    if session.get("user") == comment["author"]:
        return True
    else:
        return False


# Defensive function to prevent brute force deleting and editing,
# of posts that the user did not create. Checks if the session user
# matches the "author" field of the comment.
def owns_post(post_id):
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    if session.get("user") == post["author"]:
        return True
    else:
        return False


# Defensive function to prevent brute force deleting and editing,
# of profile that the user did not create. Checks if the session user
# matches the "author" field of the comment.
def owns_account(member_id):
    user = mongo.db.team_members.find_one({"_id": ObjectId(member_id)})
    if session.get("user") == user["username"]:
        return True
    else:
        return False


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
