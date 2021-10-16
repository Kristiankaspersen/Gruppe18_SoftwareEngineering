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
    name = StringField('navn', validators=[DataRequired()])
    description = StringField('beskrivelse', validators=[DataRequired()])
    price = IntegerField('pris', validators=[DataRequired()])
    submit = SubmitField('Submit')
