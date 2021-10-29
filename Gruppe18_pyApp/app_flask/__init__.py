from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Flask instance, convention calling it app
app = Flask(__name__)
# Config for our DB, so flask recognises our DB, pointing to our file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appDB.db'
app.config["SQLALCHEMY_BINDS"] = {'goods': 'sqlite:///goods.db'}  # Binds to be able to have multiple databases
# Secret key, security layer in order to display forms, and users to submit to DB
app.config['SECRET_KEY'] = '5f4b0959c458e6b06c51097e'
# SQLAlckemy instance, and its convention calling it db, takes in app as param
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from app_flask import routes
