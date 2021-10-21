from flask import Flask,  render_template
from flask_sqlalchemy import SQLAlchemy

#Flask instance, convention calling it app
app = Flask(__name__)
# Config for our DB, so flask recognises our DB, pointing to our file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appDB.db'
# Secret key, security layer in order to display forms, and users to submit to DB
app.config['SECRET_KEY'] = '5f4b0959c458e6b06c51097e'
# SQLAlckemy instance, and its convention calling it db, takes in app as param
db = SQLAlchemy(app)

from app_flask import routes