from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return "This is the beginning of something great."


@app.route("/admin")
def admin():
    # return "this is admin page"
    return render_template("admin.html")


@app.route("/admin/add")
def add():
    return "this is admin add page"


app.run(debug=True)
