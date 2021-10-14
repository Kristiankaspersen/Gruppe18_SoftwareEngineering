from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField

class RegisterUserForm(FlaskForm):
    username = StringField(label="Choose user name")
    email = StringField(label="Write your E-mail")
    password1 = PasswordField(label="Write password")
    password2 = PasswordField(label="Confirm password")
    submit = SubmitField(label="Create account")

