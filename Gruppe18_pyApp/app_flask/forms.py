from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, IntegerField
from wtforms.validators import DataRequired


class RegisterUserForm(FlaskForm):
    username = StringField(label="Choose user name")
    email = StringField(label="Write your E-mail")
    password1 = PasswordField(label="Write password")
    password2 = PasswordField(label="Confirm password")
    submit = SubmitField(label="Create account")


# changed into english
class FormGoods(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
    submit = SubmitField('Submit')


# log in
class LoginForm(FlaskForm):
    # for user log in
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
