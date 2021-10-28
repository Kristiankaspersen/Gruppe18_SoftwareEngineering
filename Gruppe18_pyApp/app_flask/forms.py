from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterUserForm(FlaskForm):
    username = StringField(label="Choose user name", validators=[Length(min=2, max=40), DataRequired()])
    email = StringField(label="Write your E-mail", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Write password", validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label="Confirm password", validators=[EqualTo("password1"), DataRequired()])
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