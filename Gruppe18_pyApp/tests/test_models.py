import pytest
from app_flask.models import User, db, Goods, Store


# User model
def test_models_User_create_user(client):
    user = User(username="test_user", email='test_user@mail.com', password="12345678")
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(username="test_user").first()
    assert user
    db.session.delete(user)
    db.session.commit()


def test_models_User_filer_and_read_user():
    pass


def test_models_User_delete_user():
    pass


def test_models_User_update_user():
    pass


def test_models_User_have_enough_cash():
    pass


def test_models_User_checking_password_with_hash():
    pass


# Goods model
def test_models_Goods_create_goods(client):
    """Testing if model Goods can create an object"""
    goods = Goods(
        name='benk',
        description='description',
        product_number='179459',
        price=50,
        goods_type=0
    )
    db.session.add(goods)
    db.session.commit()
    goods = Goods.query.filter_by(name='benk').first()
    assert goods
    db.session.delete(goods)
    db.session.commit()


@pytest.fixture(scope='module')
def new_object_of_goods(client):
    goods = Goods(
        name='Benk',
        description='description',
        product_number='179459',
        price=50,
        goods_type=0
    )
    return goods


def test_if_model_goods_can_create_object(new_object_of_goods):
    """Testing if Goods model name, description and price work properly when creating a new items"""
    assert new_object_of_goods.name == "Benk"
    assert new_object_of_goods.description == "description"
    assert new_object_of_goods.price == 50


def test_models_Goods_filer_and_read_goods():
    pass


def test_models_Goods_delete_goods():
    pass


def test_models_Goods_update_goods():
    pass


def test_models_Goods_purchase():
    pass


# Store model

def test_models_Store_create_store(client):
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


def test_models_Store_filer_and_read_store():
    pass


def test_models_Store_delete_store():
    pass


def test_models_Store_update_store():
    pass


# Bidding model

def test_models_Bidding_create_bid():
    pass


def test_models_Bidding_filer_and_read_bid():
    pass


def test_models_Bidding_delete_bid():
    pass


def test_models_Bidding_update_bid():
    pass
