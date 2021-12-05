from flask import flash

from app_flask.models import db, User, Goods, Store, Bidding
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
    # here put the item they have put inside
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

def bidding_on_product(bid_item, bid_from_store, offer, item_id, item_name, user_id, user_name, store_user_id):
    app = create_app()
    ctx = app.app_context()
    ctx.push()

    item_bidded_on = Goods.query.filter_by(name=bid_item).first()
    store_bidding_from = User.query.filter_by(id=bid_from_store).first()
    if (item_bidded_on is not None) and (store_bidding_from is not None):
        if offer >= item_bidded_on.price + 10:  # current_price:
            item_bidded_on.price = offer
            new_bid = Bidding(
                item_id=item_id,
                item_name=item_name,
                user_id=user_id,
                user_name=user_name,
                store_user_id=store_user_id,
                offer=offer
            )
            db.session.add(new_bid)
            db.session.commit()
        else:
            flash("You have to bid more than that")

    ctx.pop()


def delete_goods_from_store(user_id):
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    goods_to_delete = Goods.query.filter_by(id=user_id).first()
    db.session.delete(goods_to_delete)
    db.session.commit()
    flash("Item deleted")
    ctx.pop()


def delete_user_from_platform(user_id):
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    user_to_delete = User.query.filter_by(id=user_id).first()
    # This will also delete the store
    db.session.query(Store).filter(Store.user_owner == user_id).delete()
    db.session.delete(user_to_delete)
    db.session.commit()
    flash("User deleted")
    ctx.pop()


def show_users_from_db():
    """Query all users that is not Admin"""
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    user_query = User.query.filter(User.username.isnot("Admin"))
    ctx.pop()
    return user_query
