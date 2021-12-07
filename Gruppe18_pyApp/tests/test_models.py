import pytest
from app_flask.models import User, db, Goods, Store, Bidding


def test_models_User_create_user(client):
    user = User(username="test_user", email='test_user@mail.com', password="12345678")
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(username="test_user").first()
    assert user
    db.session.delete(user)
    db.session.commit()

def test_models_user_update_user(new_object_of_user):
    """Testing if attributes can be updated"""
    new_object_of_user.username = "NewName"
    new_object_of_user.email = "super_duper@mail.com"
    new_object_of_user.cash = 3000
    assert new_object_of_user.username == "NewName"
    assert new_object_of_user.email == "super_duper@mail.com"
    assert new_object_of_user.cash == 3000

def test_models_Goods_create_goods(client):
    """Testing if model Goods can create an object"""
    goods = Goods(
        name='wrench',
        description='description',
        product_number='179459',
        price=50,
        goods_type=0
    )
    db.session.add(goods)
    db.session.commit()
    goods = Goods.query.filter_by(name='wrench').first()
    assert goods
    db.session.delete(goods)
    db.session.commit()

def test_models_store_create_store(client):
    """Testing if model Store can create an object"""
    store = Store(
        store_name='Aas_gjenbruk',
        street_address="Aas_vegen",
        street_number=1,
        postal_code=1434,
        province="Aas",
        store_email="Aas@gmail.com",
        store_phone=49676761
    )
    db.session.add(store)
    db.session.commit()
    goods = Store.query.filter_by(store_name="Aas_gjenbruk").first()
    assert goods
    db.session.delete(goods)
    db.session.commit()

def test_models_bidding_create_bid(client):
    bid = Bidding(
        item_id=30,
        item_name="Picture",
        user_id=5,
        user_name="test_seller",
        store_user_id=4,
        offer=60
    )
    db.session.add(bid)
    db.session.commit()
    bid = Bidding.query.filter_by(item_id=30).first()
    assert bid
    db.session.delete(bid)
    db.session.commit()


