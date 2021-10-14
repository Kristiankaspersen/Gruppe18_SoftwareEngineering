from flask import Flask,  render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appDB.db'
app.config['SECRET_KEY'] = '5f4b0959c458e6b06c51097e'
db = SQLAlchemy(app)

from app_flask import routes