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
    profile_type = BooleanField(label="Would you like to be, auctioneers?")
    password1 = PasswordField(label="Write password", validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label="Confirm password", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label="Create account")


class RegisterStoreForm(FlaskForm):
    store_name = StringField(label="Chose name of store", validators=[Length(min=2, max=40), DataRequired()])
    street_number = IntegerField(label="Street number", validators=[DataRequired()])
    street_address = StringField(label="Address", validators=[DataRequired()])
    postal_code = IntegerField(label="Zip code", validators=[DataRequired()])
    province = StringField(label="Province", validators=[DataRequired()])
    store_email = StringField(label="Store email", validators=[DataRequired()])
    store_phone = IntegerField("Store phone number", validators=[DataRequired()])

    submit = SubmitField(label="Register store")


class FormGoods(FlaskForm):
    name = StringField(label='Choose a title for the ad', validators=[Length(min=1, max=30), DataRequired()])
    description = StringField(label='Write a description', validators=[DataRequired()])
    price = IntegerField(label='Give the ad a price', validators=[DataRequired()])
    product_number = IntegerField(label="product number", validators=[DataRequired()])
    submit = SubmitField(label='Submit ad')


# log in
class LoginFormUser(FlaskForm):
    # for user log in
    # email = StringField('email', validators=[DataRequired()])
    # password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField(label="Login User")


class LoginFormStore(FlaskForm):
    submit = SubmitField(label="Login Store")


class LoginFormAdmin(FlaskForm):
    submit = SubmitField(label="Login Admin")


class BuyGoodsForm(FlaskForm):
    submit = SubmitField(label="Buy product")

class AuctionGoodsForm(FlaskForm):
    offer = IntegerField(label="What is your offer?")
    submit = SubmitField(label="bid for product")

class AcceptAuctionForm(FlaskForm):
    submit = SubmitField(label="Accept offer")