
from flask import render_template
from app_flask import app
from app_flask.forms import RegisterUserForm

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")

@app.route("/test")
def test_page():
    return "<h1>Home Page</h1>"

@app.route("/register")
def register_user_page():
    form = RegisterUserForm()
    return render_template("registerUser.html", form=form)

