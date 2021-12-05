from flask import Blueprint

bp = Blueprint('main', __name__)

from app_flask.main import routes1