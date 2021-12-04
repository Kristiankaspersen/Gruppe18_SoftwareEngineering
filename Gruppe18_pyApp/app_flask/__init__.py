from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

picFolder = os.path.join('static', 'pics')


def create_app():
    app = Flask(__name__)
    # Config for our DB, so flask recognises our DB, pointing to our file
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appDB.db'
    # Secret key, security layer in order to display forms, and users to submit to DB
    app.config['SECRET_KEY'] = '5f4b0959c458e6b06c51097e'
    app.config['UPLOADE_FOLDER'] = picFolder
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app_flask.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app_flask.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
