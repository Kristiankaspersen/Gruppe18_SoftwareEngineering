import pytest

from app_flask.main.use_cases import delete_goods_from_store
from app_flask.models import Goods, db


def test_main_routes_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'This is homepage is not found'
    response = client.get('/homepage')
    assert response.status_code == 404
    assert b'This is homepage'


# remember this both post and get met

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
    item = Goods.query.filter_by(product_number="Test_Samsung").first()
    assert item is None







    pass


def test_main_routes_add_goods_add_market_product(client, login_default_user):
    pass


def test_main_routes_delete_goods_with_id_3(client):
    pass
    # response = client.get('delete_goods/3', follow_redirects=True)
    # assert response.status_code == 200
    # rows = db.session.query(Goods).count()
    # assert rows == 4


def test_main_routes_delete_goods():
    pass
