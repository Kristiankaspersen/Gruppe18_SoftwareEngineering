from app_flask import db
from app_flask import bcrypt


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=25), nullable=False, unique=True)
    email = db.Column(db.String(length=60), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    # Authenticated for the user set False:
    authenticated = db.Column(db.Boolean, default=False)
    # adding a relationship between goods and user
    #goods = db.relationship('goods', backref='goods_owned_by_user', lazy=True)

    @property
    def password(self):
        return self.password

    #@property.setter
    #def password(self, plain_password_txt):
    #    self.password_hash = bcrypt.generate_password_hash(plain_password_txt).decode("utf-8")

#  Need to connect with user
class Goods(db.Model):
    __bind_key__ = 'goods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(70), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    # user.id foregin key in this table, to indicate the owner for the item.
    #goods_owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Goods %r>' % self.name


# Return if the user is authenticated (true)
def is_the_user_authenticated(self):
    return self.authenticated

# add current_user


