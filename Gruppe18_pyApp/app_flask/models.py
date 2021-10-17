from app_flask import db


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=25), nullable=False, unique=True)
    email = db.Column(db.String(length=60), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    # Authenticated for the user set False:
    authenticated = db.Column(db.Boolean, default=False)
    # itemAd = db.relationship('ItemAd', backref='owned_by_user', lazy=True)


#  need another model for the item ads, and we need to connect them with user


# Return if the user is authenticated (true)
def is_the_user_authenticated(self):
    return self.authenticated

# add current_user


