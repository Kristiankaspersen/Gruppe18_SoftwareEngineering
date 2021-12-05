import requests
from app_flask.models import User, db

url = "http://127.0.0.1:5000/login"
s = requests.Session()

register = s.post(url,
                  data=dict(username='test_user', password="12345678"
                            ))


