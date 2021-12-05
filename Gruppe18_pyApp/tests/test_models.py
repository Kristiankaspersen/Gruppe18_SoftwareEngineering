import pytest
from app_flask.models import User, db, Goods, Store, Bidding


# User model
def test_models_User_create_user(client):
    user = User(username="test_user", email='test_user@mail.com', password="12345678")
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(username="test_user").first()
    assert user
    db.session.delete(user)
    db.session.commit()


@pytest.fixture(scope='module')
def new_object_of_user():
    user = User(
        id=69,
        username='super_user',
        email='super_user@mail.com',
        password='12345678',
        profile_type='1',
        cash=5000
    )
    yield user


def test_if_object_user_username_is_equal_to_given_username(new_object_of_user):
    assert new_object_of_user.username == "super_user"


def test_models_user_update_user(new_object_of_user):
    """Testing if attributes can be updated"""
    new_object_of_user.username = "NewName"
    new_object_of_user.email = "super_duper@mail.com"
    new_object_of_user.cash = 3000
    assert new_object_of_user.username == "NewName"
    assert new_object_of_user.email == "super_duper@mail.com"
    assert new_object_of_user.cash == 3000


def test_models_user_have_enough_cash(new_object_of_user):
    assert new_object_of_user.cash > 2500


def test_models_user_checking_password_with_hash():
    pass


# Goods model
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


@pytest.fixture(scope='module')
def new_object_of_goods(client):
    goods = Goods(
        id=50,
        name='Bench',
        description='description',
        product_number='179459',
        price=50,
        goods_type=0
    )
    yield goods


def test_if_object_goods_name_is_equal_to_given_name(new_object_of_goods):
    assert new_object_of_goods.name == "Bench"


def test_if_object_goods_description_is_equal_to_given_description(new_object_of_goods):
    assert new_object_of_goods.description == "description"


def test_if_object_goods_product_number_is_equal_to_given_product_number(new_object_of_goods):
    assert new_object_of_goods.product_number == "179459"


def test_if_object_goods_price_is_equal_to_given_price(new_object_of_goods):
    assert new_object_of_goods.price == 50


def test_if_object_goods_type_is_equal_to_given_type(new_object_of_goods):
    assert new_object_of_goods.goods_type == 0


def test_models_goods_update_goods_object(new_object_of_goods):
    """Testing if attributes can be updated"""
    new_object_of_goods.name = "UpdatedName"
    new_object_of_goods.description = "This is a new description"
    new_object_of_goods.price = 55
    assert new_object_of_goods.name == "UpdatedName"
    assert new_object_of_goods.description == "This is a new description"
    assert new_object_of_goods.price == 55


def test_models_goods_purchase():
    pass


# Store model
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


def test_models_store_delete_store():
    pass


def test_models_store_update_store():
    pass


# Bidding model
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


def test_models_bidding_delete_bid():
    pass


def test_models_bidding_update_bid():
    pass
