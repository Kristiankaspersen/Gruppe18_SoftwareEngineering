from app_flask.main.use_cases import add_auction_item, add_market_item
from app_flask.models import db, User, Goods, Store
from app_flask import create_app



def test_main_use_cases_add_auction_item(client, existing_store_user):

    name = "Test_samsung"
    description = "En samsung 11"
    price = 1500
    product_number = "000000"
    store_owner = existing_store_user.id

    add_auction_item(name, description, price, product_number, store_owner)
    auction_item = Goods.query.filter_by(name="Test_samsung").first()
    assert auction_item is not None
    assert auction_item.goods_type == 1
    assert auction_item.name == "Test_samsung"
    assert auction_item.price == 1500
    assert auction_item.product_number == "000000"
    assert auction_item.store_owner == store_owner
    db.session.delete(auction_item)
    db.session.commit()

def test_main_use_cases_add_goods_item(client, existing_store_user):
    name = "Test_samsung"
    description = "En samsung 11"
    price = 1500
    product_number = "000000"
    store_owner = existing_store_user.id

    add_market_item(name, description, price, product_number, store_owner)
    auction_item = Goods.query.filter_by(name="Test_samsung").first()
    print(auction_item.goods_type)
    assert auction_item is not None
    assert auction_item.goods_type == 0
    assert auction_item.name == "Test_samsung"
    assert auction_item.price == 1500
    assert auction_item.product_number == "000000"
    assert auction_item.store_owner == store_owner
    db.session.delete(auction_item)
    db.session.commit()

    pass

def test_main_use_cases_buying_product_with_enough_money():
    data = {
        "name": "Test_Samsung",
        "description": "En samsung 11 som er brukt i 2 år",
        "price": "1500",
        "product_number": "000000",
        "auctionItem": "ItemForAuction",
        "submit": "Submit+ad",
    }
    pass

def test_main_use_cases_buying_product_not_enough_money():
    pass

def test_main_use_cases_bidding_on_product():
    pass

def test_main_use_cases_accepting_bidding_offer():
    pass

def test_main_use_cases_show_current_highest_bidding_offer_in_store():
    pass