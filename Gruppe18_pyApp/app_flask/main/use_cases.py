from flask import flash

from app_flask.models import db, User, Goods, Store
from app_flask import create_app


def add_auction_item(name, description, price, product_number, store_owner):
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    new_goods = Goods(
        name=name,
        description=description,
        price=price,
        product_number=product_number,
        store_owner=store_owner,
        goods_type=0
    )
    db.session.add(new_goods)
    db.session.commit()

    flash("Item added to the auction market")
    ctx.pop()
    # here put the item they have put inside
    return new_goods

def add_goods_item(name, description, price, product_number, store_owner):
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    new_goods = Goods(
        name=name,
        description=description,
        price=price,
        product_number=product_number,
        store_owner=store_owner,
        goods_type=1
    )
    db.session.add(new_goods)
    db.session.commit()
    #here put the item they have put inside
    flash("Item added to the auction market")
    ctx.pop()
    return new_goods

def buying_product(buy_item, bought_from_store, current_user_id):
    app = create_app()
    ctx = app.app_context()
    ctx.push()

    current_user = User.query.filter_by(id=current_user_id).first()

    # Change this to product_number:
    bought_item = Goods.query.filter_by(name=buy_item).first()
    store_owner_item = User.query.filter_by(id=bought_from_store).first()
    if (bought_item is not None) and (store_owner_item is not None):
        if current_user.have_enough_cash(bought_item):
            bought_item.purchase(current_user, store_owner_item)
            flash(f"You have bought {bought_item.name} for {bought_item.price}")
        else:
            flash(f"You don't have enough money to purchase {bought_item.name}")

    ctx.pop()


def