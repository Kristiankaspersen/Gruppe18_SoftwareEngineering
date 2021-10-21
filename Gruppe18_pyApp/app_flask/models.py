from app_flask import db


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=25), nullable=False, unique=True)
    email = db.Column(db.String(length=60), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    # Authenticated for the user set False:
    authenticated = db.Column(db.Boolean, default=False)
    # itemAd = db.relationship('ItemAd', backref='owned_by_user', lazy=True)


#  Need to connect with user
class Goods(db.Model):
    __bind_key__ = 'goods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(70), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Goods %r>' % self.name


# Return if the user is authenticated (true)
def is_the_user_authenticated(self):
    return self.authenticated

# add current_user


