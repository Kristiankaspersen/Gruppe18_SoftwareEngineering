from app_flask import db, bcrypt, login_manager
from flask_login import UserMixin


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

    # adding a relationship between goods and user
    goods = db.relationship('Goods', backref='goods_owned_by_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_password_txt):
        self.password_hash = bcrypt.generate_password_hash(plain_password_txt).decode("utf-8")

    def checking_password_with_hash(self, password_attempted):
        return bcrypt.check_password_hash(self.password_hash, password_attempted)


#  Need to connect with user
class Goods(db.Model):
    # __bind_key__ = 'goods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(70), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    seller_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    # user.id foregin key in this table, to indicate the owner for the item.
    # goods_owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Goods %r>' % self.name


# Return if the user is authenticated (true)
def is_the_user_authenticated(self):
    return self.authenticated

