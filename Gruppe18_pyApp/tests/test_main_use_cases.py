from app_flask.main.use_cases import add_auction_item, add_market_item, \
    buying_product, bidding_on_product, accepting_bidding_offer, show_current_highest_bidding_offer_in_store
from app_flask.models import db, User, Goods, Store, Bidding


# TC - 023
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


# TC-024
def test_main_use_cases_add_goods_item(client, existing_store_user):
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

# TC-025
def test_main_use_cases_buying_product_with_enough_money(client, existing_store_user, existing_user, existing_item_in_market):

    current_user_id = existing_user.id
    buy_item_product_number = existing_item_in_market.product_number
    bought_from_store = existing_store_user.id

    bool_value = buying_product(buy_item_product_number, bought_from_store, current_user_id)
    assert bool_value == True

# TC-025
def test_main_use_cases_buying_product_not_enough_money(client, existing_store_user, existing_user, existing_item_in_market):
    current_user_id = existing_user.id
    buy_item_product_number = existing_item_in_market.product_number
    bought_from_store = existing_store_user.id

    existing_user.cash = 0
    bool_value = buying_product(buy_item_product_number, bought_from_store, current_user_id)
    assert bool_value == False

# TC-026
def test_main_use_cases_bidding_on_product_with_enough_money(existing_user, existing_store_user, existing_item_in_auction, delete_test_bidding_item):
    bid_item_product_number = existing_item_in_auction.product_number
    offer = 811
    item_id = existing_item_in_auction.id
    item_name = existing_item_in_auction.name
    user_id = existing_user.id
    user_name = existing_user.username
    store_user_id = Store.query.filter_by(user_owner=existing_store_user.id).first().id

    bool_value = bidding_on_product(bid_item_product_number, offer, item_id, item_name, user_id, user_name, store_user_id)
    assert bool_value == True
# TC-026 ( samme , kun med ulik variabel)
def test_main_use_cases_bidding_on_product_not_enough_money(existing_user, existing_store_user,
                                                             existing_item_in_auction):

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


# TC- 027
def test_main_use_cases_accepting_bidding_offer_have_enough_cash(existing_user,existing_store_user,existing_item_in_auction):

    accept_item_id = existing_item_in_auction.id
    accept_from_user_id = existing_user.id
    current_user_store_id = existing_store_user.id

    bool_value = accepting_bidding_offer(accept_item_id, accept_from_user_id, current_user_store_id)

    assert bool_value is True
# TC- 027
def test_main_use_cases_accepting_bidding_offer_have_not_enough_cash(existing_user,existing_store_user,existing_item_in_auction):

    accept_item_id = existing_item_in_auction.id
    accept_from_user_id = existing_user.id
    current_user_store_id = existing_store_user.id
    existing_user.cash = 0

    bool_value = accepting_bidding_offer(accept_item_id, accept_from_user_id, current_user_store_id)

    assert bool_value is False

# TC- 028
def test_main_use_cases_accepting_bidding_offer_have_enough_cash_and_delete_item_from_Bidding_table(existing_user,existing_store_user,existing_item_in_auction, bidding_item):

    accept_item_id = existing_item_in_auction.id
    accept_from_user_id = existing_user.id
    current_user_store_id = existing_store_user.id

    assert Bidding.query.filter_by(item_id=accept_item_id).first() is not None
    bool_value = accepting_bidding_offer(accept_item_id, accept_from_user_id, current_user_store_id)
    assert Bidding.query.filter_by(item_id=accept_item_id).first() is None
    assert bool_value is True


# TC -029
def test_main_use_cases_show_current_highest_bidding_offer_in_store_with_store_user(existing_store_user, bidding_item):
    current_user_id = existing_store_user.id

    bidding_items = show_current_highest_bidding_offer_in_store(current_user_id)

    assert bidding_items is not None
    assert isinstance(bidding_item, Bidding)

# TC - 30
def test_main_use_cases_show_current_highest_bidding_offer_in_store_with_normal_user(existing_user, bidding_item):
    current_user_id = existing_user.id

    bidding_items = show_current_highest_bidding_offer_in_store(current_user_id)

    assert isinstance(bidding_items, list)
    assert len(bidding_items) == 0

