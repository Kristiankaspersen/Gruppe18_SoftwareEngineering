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

def bidding_on_product(bid_item, bid_from_store, offer, item_id, item_name, user_id, user_name, store_user_id ):
    app = create_app()
    ctx = app.app_context()
    ctx.push()

    item_bidded_on = Goods.query.filter_by(name=bid_item).first()
    store_bidding_from = User.query.filter_by(id=bid_from_store).first()

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

def accepting_bidding_offer(accept_item, accept_from_user, current_user_id):
    app = create_app()
    ctx = app.app_context()
    ctx.push()

    current_user = User.query.filter_by(id=current_user_id).first()
    accepting_item = Goods.query.filter_by(name=accept_item).first()
    user_bidding_item = User.query.filter_by(id=accept_from_user).first()
    if (accepting_item is not None) and (user_bidding_item is not None):
        if user_bidding_item.have_enough_cash(accepting_item):
            accepting_item.purchase(user_bidding_item, current_user)
            flash(f"You have accepted offer on {accepting_item.name} for {accepting_item.price}")
            #Productnumber here?
            delete_items = Bidding.query.filter_by(item_name=accept_item)
            for delete_item in delete_items:
                db.session.delete(delete_item)
            db.session.commit()
        else:
            flash(f"{user_bidding_item.username} don't have enough money to purchase {accepting_item.name}")

    ctx.pop()
    return None


