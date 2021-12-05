from flask import flash

from app_flask.models import db, User, Goods, Store
from app_flask import create_app


def create_user_and_store_in_db(username, email, password, profile_type):
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    creating_user_in_db = User(username=username,
                               email=email,
                               password=password,
                               profile_type=profile_type)

    db.session.add(creating_user_in_db)
    db.session.commit()
    ctx.pop()
    return creating_user_in_db

def create_store_in_db(store_name, street_address, street_number, postal_code, province, store_email, store_phone, owner):
    app = create_app()
    ctx = app.app_context()
    ctx.push()

    create_store = Store(
        store_name=store_name,
        street_address=street_address,
        street_number=street_number,
        postal_code=postal_code,
        province=province,
        store_email=store_email,
        store_phone=store_phone
    )

    create_store.user_owner = owner
    current_user = User.query.filter_by(id=owner).first()
    current_user.profile_type = 1
    db.session.add(create_store)
    db.session.commit()
    ctx.pop()
    return create_store





