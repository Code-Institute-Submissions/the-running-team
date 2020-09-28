import os
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


# Query mongoDB for all team members and send to template.
@app.route("/")
@app.route("/get_members")
def get_members():
    members = mongo.db.team_members.find()
    return render_template("members.html", members=members, active_tab="workout")


# Query mongoDB for all posts and send to template
@app.route("/get_posts/<active_tab>")
def get_posts(active_tab):
    if session.get("user"):
        posts = list(mongo.db.posts.find().sort("$natural", -1))
        comments = list(mongo.db.comments.find().sort("$natural", -1))
        attendants = list(mongo.db.attendants.find())
        print(active_tab)
        return render_template("training_blog.html", posts=posts,
                               comments=comments, attendants=attendants,
                               active_tab=active_tab)
    else:
        return redirect(url_for("login"))

'''
Route for adding a new post. First check if there's a user cookie. If
not, redirect user to login login route. If there's a user and and
request is POST, check if form action is 'blog' or 'workout'. Then
insert data from form into database. If not post, redirect to route for
'get_members'.
'''


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
                    "category": "workout"
                }
                mongo.db.posts.insert_one(new_post)
                return redirect(url_for("get_posts", active_tab="workout"))
        return redirect(url_for("get_posts"))
    return redirect(url_for("login"))


'''
Route for editing a workout. If method is post, insert data from
form into database. Else, render template.
'''


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
        return redirect(url_for("get_posts", active_tab="workout"))
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    return render_template("edit_workout.html", post=post)


'''
Route for editing a blog post. If method is post, insert data from
form into database. Else, render template.
'''


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
        return redirect(url_for("get_posts", active_tab="blog"))
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    return render_template("edit_blog.html", post=post)


'''
Route for editing a comment. If method is post, insert data from
form into database. Else, render template.
'''


@app.route("/edit_comment/<comment_id>/<post_id>", methods=["GET", "POST"])
def edit_comment(comment_id, post_id):
    if request.method == "POST":
        updated_comment = {
            "post_id": ObjectId(post_id),
            "comment": request.form.get("comment"),
            "author": session["user"]
        }
        mongo.db.comments.update(
            {"_id": ObjectId(comment_id)}, updated_comment)
        flash("Your comment was successfully updated.", "success-flash")
        return redirect(url_for("get_posts", active_tab="blog"))
    comment = mongo.db.comments.find_one({"_id": ObjectId(comment_id)})
    return render_template("edit_comment.html", comment=comment,
                           post_id=post_id)


# Route for deleting comment.
@app.route("/delete_comment/<comment_id>")
def delete_comment(comment_id):
    active_tab = "blog"
    mongo.db.comments.remove({"_id": ObjectId(comment_id)})
    flash("Comment successfully deleted", "success-flash")
    return redirect(url_for("get_posts", active_tab=active_tab))


'''
Route for deleting workout. When a workout is deleted, all attendants,
associated with the post via post_id are also deleted.
'''


@app.route("/delete_workout/<post_id>", methods=["GET", "POST"])
def delete_workout(post_id):
    active_tab = "workout"
    mongo.db.posts.remove({"_id": ObjectId(post_id)})
    mongo.db.attendants.remove({"post_id": ObjectId(post_id)})
    flash("Post successfully deleted", "success-flash")
    return redirect(url_for("get_posts", active_tab=active_tab))


'''
Route for deleting blog post. When a blog post is deleted, all
comments associated with the post via post_id are also deleted.
'''


@app.route("/delete_blog/<post_id>", methods=["GET", "POST"])
def delete_blog(post_id):
    active_tab = "post"
    mongo.db.comments.remove({"post_id": ObjectId(post_id)})
    mongo.db.posts.remove({"_id": ObjectId(post_id)})
    flash("Post successfully deleted", "success-flash")
    return redirect(url_for("get_posts", active_tab=active_tab))


'''
Route for registering a new user. First check if there's a user cookie.
If so, redirect to get_members route. Else check if method is POST. If
so, check if username is already in database. If so, flash an error
message and redirect. If not, insert data from form into database with
hashed password field. Redirect to profile page.
'''


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


'''
Route for logging in. First check for user cookie. If so, redirect to
get_members route. Else, if method is POST, check if username exists,
if not flash error message and redirect. Else, check if entered
password matches that of existing_user-variable. If so, assign username
to cookie and display success flash message. If not, display error
message and redirect.
'''


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
                    current_runner["first_name"]), "success-flash")
                return redirect(url_for("profile", username=session["user"]))
            else:
                flash("Username and/or password is incorrect.", "error-flash")
                return render_template("login.html")

        else:
            flash("Username does not exist", "error-flash")
            return redirect(url_for("login"))
    return render_template("login.html")


'''
Route for profile page. Check if there's a user cookie. If so,
Query database for all posts by user and all workout-potsts the user
is attending. Send these to template. If not, redirect to login.
'''


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
                               attendants=attendants)
    else:
        return redirect(url_for("login"))


@app.route("/edit_profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
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
            "quote": request.form.get("slogan")
        }

        mongo.db.team_members.update(
            {"_id": ObjectId(user_id)}, updated_profile)
        username = mongo.db.team_members.find_one(
            {"_id": ObjectId(user_id)})["username"]
        flash("Profile successfully updated", "success-flash")
        return redirect(url_for("profile", username=username))
    member = mongo.db.team_members.find_one({"_id": ObjectId(user_id)})
    return render_template("edit_profile.html", member=member)


@app.route("/edit_img/<member_id>", methods=["GET", "POST"])
def edit_img(member_id):
    if request.method == "POST":
        mongo.db.team_members.update({"_id": ObjectId(member_id)},
                                     {"$set":
                                     {"img": request.form.get("img-url")}})
        return redirect(url_for("profile", username=session["user"]))
    return redirect(url_for("profile", username=session["user"]))


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
    mongo.db.posts.remove({"author": mongo.db.team_members.find_one(
        {"_id": ObjectId(member_id)})["username"]})


@app.route("/add_comment/<username>/<post_id>", methods=["GET", "POST"])
def add_comment(username, post_id):
    if request.method == "POST":
        comment = {
            "post_id": ObjectId(post_id),
            "comment": request.form.get("comment"),
            "author": username
        }
        mongo.db.comments.insert_one(comment)
        return redirect(url_for("get_posts", active_tab="blog"))


@app.route("/attend/<username>/<post_id>")
def attend(username, post_id):
    print(username)
    attending_user = mongo.db.attendants.find_one(
        {"attendant": username, "post_id": ObjectId(post_id)})
    print(attending_user)
    if attending_user:
        mongo.db.attendants.remove(attending_user)
        return redirect(url_for("get_posts", active_tab="workout"))
    else:
        attendant = {
            "post_id": ObjectId(post_id),
            "attendant": username
        }
    mongo.db.attendants.insert_one(attendant)
    attendants = mongo.db.attendants.find()
    return redirect(url_for("get_posts", active_tab="workout", attendants=attendants))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('get_members'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
