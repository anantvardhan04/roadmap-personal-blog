from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)

app = Flask(__name__)

app.secret_key = "your-unique-and-secret-key"


# User Model
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


# Mock user database
users = {"admin": User(1, "admin", "password123")}

# Initialize Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username].password == password:
            login_user(users[username])
            return redirect(url_for("admin"))
    return render_template("login.html")


# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/")
def index():
    # get the list of all files in the blog_data directory
    blog_list = []
    blog_file_list = os.listdir("blog_data")
    for blog_file in blog_file_list:
        if blog_file.endswith(".json"):
            with open(os.path.join("blog_data", blog_file), "r") as file:
                blog_content = json.load(file)
                blog_list.append(blog_content)
    return render_template("index.html", BLOGS=blog_list)


@app.route("/admin")
@login_required
def admin():
    blog_list = []
    blog_file_list = os.listdir("blog_data")
    for blog_file in blog_file_list:
        if blog_file.endswith(".json"):
            with open(os.path.join("blog_data", blog_file), "r") as file:
                blog_content = json.load(file)
                blog_list.append(blog_content)
    return render_template("admin.html", BLOGS=blog_list)


@app.route("/new", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    elif request.method == "POST":
        form_data = request.form
        current_time = datetime.now()
        title = form_data["title"]
        content = form_data["content"]
        current_time_formatted = current_time.strftime("%d %B, %Y")
        id = len(os.listdir("blog_data")) + 1
        blog_data = {
            "id": id,
            "title": title,
            "content": content,
            "published_date": current_time_formatted,
        }
        # save the content in a file
        with open(f"blog_data/{id}.json", "w") as file:
            json.dump(blog_data, file, indent=4)
        return redirect(url_for("blog", id=id))


@app.route("/blog/<id>")
def blog(id):
    with open(f"blog_data/{id}.json", "r") as file:
        data = json.load(file)
        print(data)
    return render_template("blog.html", BLOGS=data)


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "GET":
        return render_template("edit.html", ID=id)
    elif request.method == "POST":
        form_data = request.form
        current_time = datetime.now()
        title = form_data["title"]
        content = form_data["content"]
        current_time_formatted = current_time.strftime("%d %B, %Y")
        blog_data = {
            "id": id,
            "title": title,
            "content": content,
            "published_date": current_time_formatted,
        }
        # save the content in a file
        with open(f"blog_data/{id}.json", "w") as file:
            json.dump(blog_data, file, indent=4)
        return render_template("blog.html", BLOGS=blog_data)


@app.route("/delete/<id>", methods=["POST", "GET"])
def delete(id):
    if request.method == "GET":
        os.remove(f"blog_data/{id}.json")
        return redirect(url_for("admin"))


app.run(debug=True)
