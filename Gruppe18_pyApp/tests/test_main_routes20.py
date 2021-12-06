import pytest

from app_flask.main.use_cases import delete_goods_from_store
from app_flask.models import Goods, db



def test_main_routes_home_page(client):
    response = client.get('/homepage')
    response.status_code == 200
    response = client.get('/')
    response.status_code == 200
    assert b'This is hompage'


# remember this both post and get met

def test_main_routes_add_goods_add_auction_product(client, login_default_user):
    data = {
        "name": "Test_Samsung",
        "description": "En samsung 11 som er brukt i 2 år",
        "price": "1500",
        "product_number": "000000",
        "auctionItem": "ItemForAuction",
        "submit": "Submit+ad",
    }
    pass


def test_main_routes_add_goods_add_market_product(client, login_default_user):
    data = {
        "name": "Test_Samsung",
        "description": "En samsung 11 som er brukt i 2 år",
        "price": "1500",
        "product_number": "000000",
        "auctionItem": "ItemForAuction",
        "submit": "Submit+ad",
    }
    pass


def test_main_routes_delete_goods_with_id_3(client):
    response = client.get('delete_goods/3', follow_redirects=True)
    assert response.status_code == 200
    rows = db.session.query(Goods).count()
    assert rows == 4


def test_main_routes_delete_goods():
    pass
