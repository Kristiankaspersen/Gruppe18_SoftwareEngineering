import requests
from app_flask.models import User, db

url = "http://127.0.0.1:5000/register"
s = requests.Session()

register = s.post(url,  data={
    "username": "Geir",
    "email": "dsad@dsad.com",
    "password1": "12345678",
    "password2": "12345678",
    "submit": "Create+account"
})

