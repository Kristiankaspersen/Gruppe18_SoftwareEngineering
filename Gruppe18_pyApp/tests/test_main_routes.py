import pytest

from app_flask.models import Goods, db, User


# TC - 012
def test_main_routes_add_goods_add_auction_product_item_exist(client, login_store_user):
    data = {
        "name": "Test_Samsung",
        "description": "Description",
        "price": "1500",
        "product_number": "000000",
        "auctionItem": "ItemForAuction",
        "submit": "Submit+ad"
    }
    assert login_store_user.status_code == 200
    response = client.get('/goods')
    assert response.status_code == 200
    response = client.post('/goods', data=data, follow_redirects=True)
    assert response.status_code == 200
    item = Goods.query.filter_by(product_number=000000).first()
    assert item is not None
    db.session.delete(item)
    db.session.commit()
# TC - 013
def test_main_routes_add_goods_add_auction_product_text_in_product_number(client, login_store_user):
    data = {
        "name": "Test_Samsung",
        "description": "Description",
        "price": "1500",
        "product_number": "text_in_product_number",
        "auctionItem": "ItemForAuction",
        "submit": "Submit+ad"
    }
    assert login_store_user.status_code == 200
    response = client.get('/goods')
    assert response.status_code == 200
    response = client.post('/goods', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Product number and price needs to be a number, try again' in response.data
    item = Goods.query.filter_by(product_number="Test_Samsung").first()
    assert item is None

# TC -014
def test_main_routes_add_goods_add_auction_product_text_in_price(client, login_store_user):
    data = {
        "name": "Test_Samsung",
        "description": "Description",
        "price": "text_in_product_number",
        "product_number": "000000",
        "auctionItem": "ItemForAuction",
        "submit": "Submit+ad"
    }
    assert login_store_user.status_code == 200
    response = client.get('/goods')
    assert response.status_code == 200
    response = client.post('/goods', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Product number and price needs to be a number, try again' in response.data
    item = Goods.query.filter_by(product_number=000000).first()
    assert item is None
# TC -015
def test_main_routes_add_goods_add_auction_product_text_in_product_number_and_price(client, login_store_user):
    data = {
        "name": "Test_Samsung",
        "description": "Description",
        "price": "text_in_product_number",
        "product_number": "dsadsad",
        "auctionItem": "ItemForAuction",
        "submit": "Submit+ad"
    }
    assert login_store_user.status_code == 200
    response = client.get('/goods')
    assert response.status_code == 200
    response = client.post('/goods', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Product number and price needs to be a number, try again' in response.data
    item = Goods.query.filter_by(product_number="Test_samsung").first()
    assert item is None
# TC -016
def test_main_routes_add_goods_add_market_product(client, login_store_user):
    data = {
        "name": "Test_item",
        "description": "Description",
        "price": "1500",
        "product_number": "000000",
        "submit": "Submit+ad"
    }
    assert login_store_user.status_code == 200
    response = client.get('/goods')
    assert response.status_code == 200
    response = client.post('/goods', data=data, follow_redirects=True)
    assert response.status_code == 200
    item = Goods.query.filter_by(product_number=000000).first()
    assert item is not None
    db.session.delete(item)
    db.session.commit()

def test_main_routes_show_owned_goods():
    pass

# TC -017
def test_main_routes_store_page_buy_product_enough_money(client, existing_store_with_user, existing_item_in_market, existing_user, login_normal_user):
    product_number = existing_item_in_market.product_number
    existing_user_id = existing_user.id
    data = {
        "store_owner": f"{existing_store_with_user.id}",
        "bought_item": f"{product_number}",
        "submit": "Buy+product"
    }

    assert existing_item_in_market.store_owner == existing_store_with_user.id

    response = client.get('/store')
    assert response.status_code == 200
    response = client.post('/store', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"You have bought test_item for 800 NOK" in response.data

# TC -018
def test_main_routes_store_page_buy_product_not_enough_money(client, existing_store_with_user, existing_item_in_market, existing_user, login_normal_user):
    product_number = existing_item_in_market.product_number
    existing_user_id = existing_user.id
    data = {
        "store_owner": f"{existing_store_with_user.id}",
        "bought_item": f"{product_number}",
        "submit": "Buy+product"
    }
    existing_user.cash = 0

    assert existing_item_in_market.store_owner == existing_store_with_user.id

    response = client.post('/store', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"You do not have enough money to purchase test_item" in response.data


def test_main_routes_store_page_buy_product_ownership_of_goods_change(client, existing_store_with_user, existing_item_in_market, existing_user, login_normal_user):
    product_number = existing_item_in_market.product_number
    existing_user_id = existing_user.id
    data = {
        "store_owner": f"{existing_store_with_user.id}",
        "bought_item": f"{product_number}",
        "submit": "Buy+product"
    }

    assert existing_item_in_market.store_owner == existing_store_with_user.id

    response = client.post('/store', data=data, follow_redirects=True)
    current_item_that_has_been_bought = Goods.query.filter_by(product_number=product_number).first()
    assert response.status_code == 200
    assert current_item_that_has_been_bought.store_owner is None
    assert current_item_that_has_been_bought.user_owner == existing_user_id

# TC -019
def test_main_routes_store_page_auction_page_bidding_on_goods_with_enough_cash(client, existing_store_with_user, existing_item_in_auction, existing_user, login_normal_user, delete_test_bidding_item):

    data = {
        "store_owner1": f"{existing_store_with_user.id}",
        "bid_item": f"{existing_item_in_auction.product_number}",
        "offer": "900",
        "submit": "bid+for+product"
    }

    response = client.get('/auction')
    assert response.status_code == 200
    response = client.post('/auction', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"You have bid on test_item for 900 NOK" in response.data

# TC -20
def test_main_routes_store_page_auction_page_bidding_on_goods_with_not_enough_cash(client, existing_store_with_user, existing_item_in_auction, existing_user, login_normal_user):

    data = {
        "store_owner1": f"{existing_store_with_user.id}",
        "bid_item": f"{existing_item_in_auction.product_number}",
        "offer": "300",
        "submit": "bid+for+product"
    }

    response = client.post('/auction', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"You have to bid more than that 300 NOK, at least 10 more NOK than current price" in response.data

# TC - 019
def test_main_routes_store_page_auction_page_bidding_on_goods_with_with_wrong_user_input(client, existing_store_with_user, existing_item_in_auction, existing_user, login_normal_user):
    data = {
        "store_owner1": f"{existing_store_with_user.id}",
        "bid_item": f"{existing_item_in_auction.product_number}",
        "offer": "dsadasda",
        "submit": "bid+for+product"
    }

    response = client.post('/auction', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Your bid needs to be a number, try again" in response.data

# TC - 021
def test_main_routes_store_page_auction_accept_bid_from_user_with_enough_cash(client, existing_user, login_store_user, existing_store_user,existing_item_in_auction, doing_a_bid):

    user_doing_a_bid_id = doing_a_bid[0]
    existing_item_in_auction_id = doing_a_bid[1]
    data = {
        "accepting_user": f"{user_doing_a_bid_id}",
        "accepting_item": f"{existing_item_in_auction_id}",
        "submit": "Accept+offer"
    }

    response = client.post('/auction', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"You have accepted offer on test_item for 900 NOK" in response.data

# TC - 022
def test_main_routes_store_page_auction_accept_bid_from_user_with_not_enough_cash(client, login_store_user, existing_user, existing_store_user,existing_item_in_auction, doing_a_bid):
    user_doing_a_bid_id = doing_a_bid[0]
    existing_item_in_auction_id = doing_a_bid[1]
    data = {
        "accepting_user": f"{user_doing_a_bid_id}",
        "accepting_item": f"{existing_item_in_auction_id}",
        "submit": "Accept+offer"
    }
    existing_user = User.query.filter_by(id=user_doing_a_bid_id).first()
    existing_user.cash = 0

    response = client.post('/auction', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"test_user do not have enough money to purchase test_item" in response.data

