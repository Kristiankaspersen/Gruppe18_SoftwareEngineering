from app_flask import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=25), nullable=False, unique=True)
    email = db.Column(db.String(length=60), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    # Authenticated for the user set False:
    profile_type = db.Column(db.Boolean(), nullable=False, default=False)
    cash = db.Column(db.Integer(), nullable=False, default=2000)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    # Adding a relationship between goods, user and store, user
    goods = db.relationship('Goods', backref='goods_owned_by_user', lazy=True)
    store = db.relationship('Store', backref='store_owner', lazy=True)

    def have_enough_cash(self, bought_item):
        return self.cash >= bought_item.price

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_password_txt):
        self.password_hash = bcrypt.generate_password_hash(plain_password_txt).decode("utf-8")

    def checking_password_with_hash(self, password_attempted):
        return bcrypt.check_password_hash(self.password_hash, password_attempted)

    def __repr__(self):
        return f"User table: \n id: {self.id} username: {self.username} | email: {self.email} " \
               f"| password_hash: {self.password_hash} | budget: {self.cash} | profile_type: {self.profile_type}" \
               f"| date_created: {self.date_created}"


class Goods(db.Model):
    # __bind_key__ = 'goods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(70), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    product_number = db.Column(db.String(length=6), nullable=False, unique=True)
    profile_type = db.Column(db.Boolean(), nullable=False, default=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    # Adding a relationship between goods, user and store
    user_owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    store_owner = db.Column(db.Integer(), db.ForeignKey('store.id'))

    def purchase(self, user, store_item_owner):
        self.user_owner = user.id
        self.store_owner = None
        user.cash -= self.price
        store_item_owner.cash += self.price
        db.session.commit()

    def __repr__(self):
        return f"Item table: \n id: {self.id} name: {self.name} | price: {self.price} | barcode {self.product_number} | " \
               f"description: {self.description} | user owner: {self.user_owner} | store owner {self.store_owner}  | date_created: {self.date_created}"


class Store(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    store_name = db.Column(db.String(length=30), nullable=False, unique=True)
    street_address = db.Column(db.String(length=40), nullable=False)
    street_number = db.Column(db.Integer(), nullable=False)
    postal_code = db.Column(db.Integer(), nullable=False)
    province = db.Column(db.String(length=50), nullable=False)
    store_email = db.Column(db.String(length=50), nullable=False, unique=True)
    store_phone = db.Column(db.Integer(), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    user_owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    goods = db.relationship('Goods', backref='owned_store', lazy=True)

    def __repr__(self):
        return f"Store table: \n id: {self.id} store_name: {self.store_name} | Address: {self.street_address} \n" \
               f" {self.street_number} | postal_code: {self.postal_code} | province: {self.province} \n  " \
               f"| store_email: {self.store_email} | phonenumber: {self.store_phone} | owner: {self.user_owner} " \
               f"| date_created: {self.date_created}"

class Bidding(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    item_id = db.Column(db.Integer(), nullable=False)
    item_name = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer(), nullable=False)
    user_name = db.Column(db.String(), nullable=False)
    store_user_id = db.Column(db.Integer(), nullable=False)
    offer = db.Column(db.Integer(), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)


# # Return if the user is authenticated (true)
# def is_the_user_authenticated(self):
#     return self.authenticated


