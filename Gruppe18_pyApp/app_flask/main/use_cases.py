from flask import flash

from app_flask.models import db, User, Goods, Store, Bidding
from app_flask import create_app
from sqlalchemy.sql.expression import func, and_


def add_auction_item(name, description, price, product_number, store_user_owner):
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    store_owner = Store.query.filter_by(user_owner=store_user_owner).first().id
    new_goods = Goods(
        name=name,
        description=description,
        price=price,
        product_number=product_number,
        store_owner=store_owner,
        goods_type=1 #Auction goods type 1
    )
    db.session.add(new_goods)
    db.session.commit()
    new_goods = Goods.query.filter_by(product_number=product_number).first()

    ctx.pop()
    # here put the item they have put inside
    return new_goods


def add_market_item(name, description, price, product_number, store_owner):
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    store_owner = Store.query.filter_by(user_owner=store_owner).first().id
    new_goods = Goods(
        name=name,
        description=description,
        price=price,
        product_number=product_number,
        # user_owner?
        store_owner=store_owner,
        goods_type=0 #Market goods type 0
    )
    db.session.add(new_goods)
    db.session.commit()
    new_goods = Goods.query.filter_by(product_number=product_number).first()
    # here put the item they have put inside
    ctx.pop()
    return new_goods


def buying_product(buy_item_product_number, bought_from_store, current_user_id):
    app = create_app()
    ctx = app.app_context()
    ctx.push()

    current_user = User.query.filter_by(id=current_user_id).first()

    # Change this to product_number:
    bought_item = Goods.query.filter_by(product_number=buy_item_product_number).first()
    store_owner_item = User.query.filter_by(id=bought_from_store).first()
    if (bought_item is not None) and (store_owner_item is not None):
        if current_user.have_enough_cash(bought_item):
            bought_item.purchase(current_user, store_owner_item)
            ctx.pop()
            return True
        else:
            ctx.pop()
            return False
    ctx.pop()
    return #print("error: bought item, or store owner does not exist")



def bidding_on_product(bid_item, bid_from_store, offer, item_id, item_name, user_id, user_name, store_user_id):
    app = create_app()
    ctx = app.app_context()
    ctx.push()

    item_bidded_on = Goods.query.filter_by(product_number=bid_item).first()
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
        ctx.pop()
        return True
    else:
        ctx.pop()
        return False

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
            # Productnumber here?
            delete_items = Bidding.query.filter_by(item_name=accept_item)
            for delete_item in delete_items:
                db.session.delete(delete_item)
            db.session.commit()
        else:
            flash(f"{user_bidding_item.username} don't have enough money to purchase {accepting_item.name}")

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


def show_current_highest_bidding_offer_in_store(current_user_id):
    current_store = Store.query.filter_by(user_owner=current_user_id).first()
    if current_store is not None:
        bidding_items = Bidding.query. \
            with_entities(Bidding.item_name, Bidding.offer, Bidding.user_name, Bidding.user_id, Bidding.id,
                          func.max(Bidding.offer)) \
            .group_by(Bidding.item_name).filter_by(store_user_id=current_user_id)

        return bidding_items

    else:
        bidding_items = []

        return bidding_items
