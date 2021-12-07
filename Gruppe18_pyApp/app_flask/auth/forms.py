from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app_flask.models import User, Store


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
    password1 = PasswordField(label="Write password", validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label="Confirm password", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label="Create account")

class RegisterStoreForm(FlaskForm):

    store_name = StringField(label="Chose name of store", validators=[Length(min=2, max=40), DataRequired()])
    street_number = StringField(label="Street number", validators=[DataRequired()])
    street_address = StringField(label="Address", validators=[DataRequired()])
    postal_code = IntegerField(label="Zip code", validators=[DataRequired()])
    province = StringField(label="Province", validators=[DataRequired()])
    store_email = StringField(label="Store email", validators=[Email(), DataRequired()])
    store_phone = IntegerField("Store phone number", validators=[DataRequired()])

    submit = SubmitField(label="Register store")

class LoginForm(FlaskForm):
    username = StringField(label="username", validators=[DataRequired()])
    password = PasswordField(label="Write password", validators=[DataRequired()])
    submit = SubmitField(label="Login")

class LoginFormUser(FlaskForm):
    # for user log in
    # email = StringField('email', validators=[DataRequired()])
    # password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField(label="Login normal user")


class LoginFormStore(FlaskForm):
    submit = SubmitField(label="Login store user")


class LoginFormAdmin(FlaskForm):
    submit = SubmitField(label="Login Admin")