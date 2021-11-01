from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app_flask.models import User


class RegisterUserForm(FlaskForm):

    def validate_username(self, check_username):
        user = User.query.filter_by(username=check_username.data).first()
        if user is not None:
            raise ValidationError("Username is already in use! try a different username")

    def validate_email(self, check_email):
        email = User.query.filter_by(email=check_email.data).first()
        if email is not None:
            raise ValidationError('Email is already in use! Use another email')

    username = StringField(label="Choose user name", validators=[Length(min=2, max=40), DataRequired()])
    email = StringField(label="Write your E-mail", validators=[Email(), DataRequired()])
    profile_type = BooleanField(label="what type of user")
    password1 = PasswordField(label="Write password", validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label="Confirm password", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label="Create account")


class FormGoods(FlaskForm):
    name = StringField(label='Choose a title for the ad', validators=[Length(min=1, max=30), DataRequired()])
    description = StringField(label='Write a description', validators=[DataRequired()])
    price = IntegerField(label='Give the ad a price', validators=[DataRequired()])
    submit = SubmitField(label='Submit ad')


# log in
class LoginForm(FlaskForm):
    # for user log in
    # email = StringField('email', validators=[DataRequired()])
    # password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField(label="Login")
