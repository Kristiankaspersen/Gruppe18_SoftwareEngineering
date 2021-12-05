from app_flask.main.use_cases import add_auction_item
from app_flask.models import db, User, Goods, Store
from app_flask import create_app
app = create_app()
ctx = app.app_context()
ctx.push()


def test_main_use_cases_add_auction_item(client, existing_store_user):
    data = {
    "name": "Test_Samsung",
    "description": "En samsung 11 som er brukt i 2 år",
    "price": "1500",
    "product_number":"000000",
    "auctionItem": "ItemForAuction",
    "submit": "Submit+ad",
    }

    add_auction_item(data["name"], data["description"], data["price"], data["product_number"], existing_store_user.id)
    auction_item = Goods.query.filter(product_number=data["product_number"])
    assert auction_item is not None
    assert auction_item.goods_type == 0
    assert auction_item.name == "Test_Samsung"
    assert auction_item.price == 1500
    assert auction_item.product_number == 000000
    assert auction_item.store_owner == existing_store_user.id




# def add_auction_item(name, description, price, product_number, store_owner):
#     app = create_app()
#     ctx = app.app_context()
#     ctx.push()
#     new_goods = Goods(
#         name=name,
#         description=description,
#         price=price,
#         product_number=product_number,
#         store_owner=store_owner,
#         goods_type=0
#     )
#     db.session.add(new_goods)
#     db.session.commit()
#
#     flash("Item added to the auction market")
#     ctx.pop()
#     # here put the item they have put inside
#     return new_goods

def test_main_use_cases_add_goods_item():
    pass

def test_main_use_cases_buying_product():
    pass

def test_main_use_cases_bidding_on_product():
    pass

def test_main_use_cases_accepting_bidding_offer():
    pass

def test_main_use_cases_show_current_highest_bidding_offer_in_store():
    pass

ctx.pop()