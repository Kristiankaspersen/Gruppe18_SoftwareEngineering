from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, Length


class AddGoodsToMarket(FlaskForm):
    name = StringField(label='Choose a title for the ad', validators=[Length(min=1, max=30), DataRequired()])
    description = StringField(label='Write a description')
    price = IntegerField(label='Give the ad a price', validators=[DataRequired()])
    product_number = IntegerField(label="product number", validators=[DataRequired()])
    submit = SubmitField(label='Submit ad')

class AddGoodsToAuction(FlaskForm):
    name = StringField(label='Choose a title for the ad', validators=[Length(min=1, max=30), DataRequired()])
    description = StringField(label='Write a description')
    price = IntegerField(label='Give the ad a price', validators=[DataRequired()])
    product_number = IntegerField(label="product number", validators=[DataRequired()])
    submit = SubmitField(label='Submit ad')

class BuyGoodsForm(FlaskForm):
    submit = SubmitField(label="Buy product")

class AuctionGoodsForm(FlaskForm):
    offer = IntegerField(label="What is your offer?")
    submit = SubmitField(label="bid for product")

class AcceptAuctionForm(FlaskForm):
    submit = SubmitField(label="Accept offer")