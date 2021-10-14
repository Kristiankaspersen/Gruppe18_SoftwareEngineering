
from flask import render_template
from app_flask import app
from app_flask.forms import RegisterUserForm
from app_flask.models import User
from app_flask import db

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")

@app.route("/test")
def test_page():
    return "<h1>Home Page</h1>"

@app.route("/register", methods=['GET', 'POST'])
def register_user_page():
    form = RegisterUserForm()
    if form.validate_on_submit():
        creating_user_in_db = User(username=form.username.data,
                                   email=form.email.data,
                                   password_hash=form.password1.data)
        db.session.add(creating_user_in_db)
        db.session.commit()
    return render_template("registerUser.html", form=form)

