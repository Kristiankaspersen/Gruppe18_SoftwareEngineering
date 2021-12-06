from app_flask.main.use_cases import add_auction_item, add_market_item, buying_product, bidding_on_product
from app_flask.models import db, User, Goods, Store, Bidding
from app_flask import create_app



def test_main_use_cases_add_auction_item(client, existing_store_user):

    name = "Test_samsung"
    description = "En samsung 11"
    price = 1500
    product_number = "000000"
    store_user_owner = existing_store_user.id

    add_auction_item(name, description, price, product_number, store_user_owner)
    auction_item = Goods.query.filter_by(name=name).first()
    store_owner = Store.query.filter_by(user_owner=store_user_owner).first().id
    assert auction_item is not None
    assert auction_item.goods_type == 1
    assert auction_item.name == "Test_samsung"
    assert auction_item.price == 1500
    assert auction_item.product_number == "000000"
    assert auction_item.store_owner == store_owner
    db.session.delete(auction_item)
    db.session.commit()

# def test_main_use_cases_add_auction_item2(add_goods_item_function):
#     assert add_goods_item_function is not None
#     assert add_goods_item_function.goods_type == 0
#     assert add_goods_item_function.name == "Test_samsung"
#     assert add_goods_item_function.price == 1500
#     assert add_goods_item_function.product_number == "000000"
#     assert add_goods_item_function.store_owner ==

def test_main_use_cases_add_goods_item(client, existing_store_user):
    # Må endre på disse testene, de trenger fixture.
    name = "Test_samsung"
    description = "En samsung 11"
    price = 1500
    product_number = "000000"
    store_user_owner = existing_store_user.id



    add_market_item(name, description, price, product_number, store_user_owner)
    auction_item = Goods.query.filter_by(name="Test_samsung").first()
    store_owner = Store.query.filter_by(user_owner=store_user_owner).first().id
    print(auction_item.goods_type)
    assert auction_item is not None
    assert auction_item.goods_type == 0
    assert auction_item.name == "Test_samsung"
    assert auction_item.price == 1500
    assert auction_item.product_number == "000000"
    assert auction_item.store_owner == store_owner
    db.session.delete(auction_item)
    db.session.commit()


def test_main_use_cases_buying_product_with_enough_money(client, existing_store_user, existing_user, existing_item_in_market):

    current_user_id = existing_user.id
    buy_item_product_number = existing_item_in_market.product_number
    bought_from_store = existing_store_user.id

    bool_value = buying_product(buy_item_product_number, bought_from_store, current_user_id)
    assert bool_value == True


def test_main_use_cases_buying_product_not_enough_money(client, existing_store_user, existing_user, existing_item_in_market):
    current_user_id = existing_user.id
    buy_item_product_number = existing_item_in_market.product_number
    bought_from_store = existing_store_user.id

    existing_user.cash = 0
    bool_value = buying_product(buy_item_product_number, bought_from_store, current_user_id)
    assert bool_value == False


def test_main_use_cases_bidding_on_product_with_enough_money(existing_user, existing_store_user, existing_item_in_auction):
    # data bid_item_product_number, offer, item_id, item_name, user_id, user_name, store_user_id
    bid_item_product_number = existing_item_in_auction.product_number
    offer = 811
    item_id = existing_item_in_auction.id
    item_name = existing_item_in_auction.name
    user_id = existing_user.id
    user_name = existing_user.username
    store_user_id = Store.query.filter_by(user_owner=existing_store_user.id).first().id

    bool_value = bidding_on_product(bid_item_product_number, offer, item_id, item_name, user_id, user_name, store_user_id)
    assert bool_value == True

def test_main_use_cases_bidding_on_product_not_enough_money(existing_user, existing_store_user,
                                                             existing_item_in_auction):
    # data bid_item_product_number, offer, item_id, item_name, user_id, user_name, store_user_id
    bid_item_product_number = existing_item_in_auction.product_number
    offer = 0
    item_id = existing_item_in_auction.id
    item_name = existing_item_in_auction.name
    user_id = existing_user.id
    user_name = existing_user.username
    store_user_id = Store.query.filter_by(user_owner=existing_store_user.id).first().id

    bool_value = bidding_on_product(bid_item_product_number, offer, item_id, item_name, user_id, user_name,
                                    store_user_id)
    assert bool_value == False





    # Fixtures jeg trenger. Item i auksjon, butikk det kjøpes fra,

    #Lag en fixture for Bidding item. Bid_item, bid_from_store


    pass

def test_main_use_cases_accepting_bidding_offer():
    pass

def test_main_use_cases_show_current_highest_bidding_offer_in_store():
    pass