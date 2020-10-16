import os
import random
import string
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (Flask, flash, jsonify, render_template, redirect, request,
                   url_for, session)
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Custom 404 redirect
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Entry point of app.
@app.route("/")
@app.route("/get_events")
def get_events():
    events = list(mongo.db.events.find())
    if session.get("user"):
        user = mongo.db.team_members.find_one({"username": session["user"]})
        return render_template("events.html", events=events, user=user)
    return render_template("events.html", events=events)


# Add new event.
@app.route("/add_event", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        new_event = {
            "title": request.form.get("title"),
            "date": request.form.get("date"),
            "location": request.form.get("location"),
            "url": request.form.get("url"),
            "img": request.form.get("img-url"),
            "element_id": get_random_string(20)
        }
        mongo.db.events.insert_one(new_event)
        flash("Event added", "success-flash")
    return redirect(url_for("get_events"))


# Edit event.
@app.route("/edit_event/<event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    if session.get("user"):
        if request.method == "POST":
            updated_event = {
                "title": request.form.get("title"),
                "date": request.form.get("date"),
                "location": request.form.get("location"),
                "url": request.form.get("url"),
                "img": request.form.get("img-url"),
                "element_id": get_random_string(20)
            }
            mongo.db.events.update({"_id": ObjectId(event_id)}, updated_event)
            flash("Event updated.", "success-flash")
            return redirect(url_for("get_events"))
        event = mongo.db.events.find_one({"_id": ObjectId(event_id)})
        return render_template("edit_event.html", event=event)
    return redirect(url_for("login"))


# Delete event.
@app.route("/delete_event/<event_id>")
def delete_event(event_id):
    if session.get("user"):
        mongo.db.events.remove({"_id": ObjectId(event_id)})
        flash("Event deleted", "success-flash")
        return redirect(url_for("get_events"))
    return redirect(url_for("login"))


# Route for displaying team members.
@app.route("/get_members")
def get_members():
    members = mongo.db.team_members.find()
    return render_template("members.html", members=members,
                           active_tab="workout")


# Route for displaying all posts. active_tab tells template which tab
# top activate.
@app.route("/get_posts")
@app.route("/get_posts/<active_tab>")
def get_posts(active_tab="workouts"):
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


# Route for adding a new post. "action" attribute tells the function
# which fields to insert.
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
    return redirect(url_for("login"))


# Route for editing workout.
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


# Route for editing blog post.
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


# Route for editing comment.
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


# Route for deleting comment.
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


# Route for deleting workout post.
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


# Route for deleting blog post.
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


# Route for registering a new user.
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
            "img": request.form.get("img-url"),
            "is_admin": False
        }
        mongo.db.team_members.insert_one(new_member)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!", "success-flash")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


# Route for logging in.
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


# Route for profile page.
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


# Route for editing profile.
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
                    "img": request.form.get("img-url"),
                    "is_admin": mongo.db.team_members.find_one(
                        {"_id": ObjectId(user_id)})["is_admin"]
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


# Route for deleting profile.
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


# Helper function. Deletes all posts.
def delete_posts(member_id):
    mongo.db.posts.remove({"author": mongo.db.team_members.find_one(
        {"_id": ObjectId(member_id)})["username"]})


# Route for adding a comment.
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


# Route for attending a workout.
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


# Function for turning on/off admin rights. Triggered by clicking
# copyright symbol in footer. Remove before production.
@app.route("/toggle_admin")
def toggle_admin():
    if session.get("user"):
        username = session.get("user")
        is_admin = mongo.db.team_members.find_one(
                    {"username": username})["is_admin"]
        if is_admin:
            mongo.db.team_members.update({"username": username},
                                         {"$set":
                                         {"is_admin": False}})
            return jsonify(admin="Admin mode: off",
                           info="Refresh browser for changes to "
                           "take effect.")
        else:
            mongo.db.team_members.update({"username": username},
                                         {"$set":
                                         {"is_admin": True}})
            return jsonify(admin="Admin mode: on",
                           info="Refresh browser for changes to "
                           "take effect.")
    return jsonify(admin="Please log in",
                   info="Don't forget to keep in touch with your "
                   "team mates on social media.")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
