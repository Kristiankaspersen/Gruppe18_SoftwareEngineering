from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, IntegerField
from wtforms.validators import DataRequired


class RegisterUserForm(FlaskForm):
    username = StringField(label="Choose user name")
    email = StringField(label="Write your E-mail")
    password1 = PasswordField(label="Write password")
    password2 = PasswordField(label="Confirm password")
    submit = SubmitField(label="Create account")


class FormGoods(FlaskForm):
    name = StringField('Choose a title for the ad', validators=[DataRequired()])  # Change name to title?
    description = StringField('Write a description', validators=[DataRequired()])
    price = IntegerField('Give the ad a price', validators=[DataRequired()])
    submit = SubmitField('Submit')


# log in
class LoginForm(FlaskForm):
    # for user log in
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
