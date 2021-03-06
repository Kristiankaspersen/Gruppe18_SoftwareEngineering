import pytest
from app_flask.main.use_cases import add_market_item
from app_flask import create_app
from app_flask.models import User, Store, db, Goods, Bidding


@pytest.fixture()
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        with app.test_client() as client:
            yield client

@pytest.fixture()
def existing_user(client):
    user = User(username="test_user", email='test_user@mail.com', password="12345678")
    db.session.add(user)
    db.session.commit()

    user = User.query.filter_by(username="test_user").first()
    yield user
    db.session.delete(user)
    db.session.commit()

@pytest.fixture()
def existing_store_user(client):
    user = User(username="test_user_store", email='test_user_store@mail.com', password="12345678", profile_type=1)
    db.session.add(user)
    db.session.commit()

    store = Store(
        store_name='Test_AS',
        street_address="TestAdress",
        street_number=28,
        postal_code=6329,
        province="Testnes",
        store_email="Test_AS@gmail.com",
        store_phone=67326732
    )
    db.session.add(store)
    db.session.commit()
    store.user_owner = User.query.filter_by(username="test_user_store").first().id
    user = User.query.filter_by(username="test_user_store").first()
    yield user
    db.session.delete(store)
    db.session.delete(user)
    db.session.commit()

@pytest.fixture()
def existing_store_with_user(client):
    user = User(username="test_user_store2", email='test_user_store2@mail.com', password="12345678", profile_type=1)
    db.session.add(user)
    db.session.commit()

    store = Store(
        store_name='Test_AS2',
        street_address="TestAdress",
        street_number=28,
        postal_code=6329,
        province="Testnes",
        store_email="Test_AS2@gmail.com",
        store_phone=67326732
    )
    db.session.add(store)
    db.session.commit()
    store.user_owner = User.query.filter_by(username="test_user_store2").first().id
    store = Store.query.filter_by(store_name="Test_AS2").first()
    yield store
    user = User.query.filter_by(username="test_user_store2").first()
    store = Store.query.filter_by(store_name="Test_AS2").first()
    db.session.delete(store)
    db.session.delete(user)
    db.session.commit()

@pytest.fixture()
def existing_item_owned_by_user(existing_user):
    test_item = Goods(
        name='test_item',
        description='description',
        product_number='010101',
        price=800,
    )
    test_item.user_owner = User.query.filter_by(username=existing_store_user.username).first().id
    db.session.add(test_item)
    db.session.commit()
    test_item = Goods.query.filter_by(product_number="010101").first()
    yield test_item
    db.session.delete(test_item)
    db.session.commit()

@pytest.fixture()
def existing_item_in_market(existing_store_with_user):
    test_item = Goods(
        name='test_item',
        description='description',
        product_number='010101',
        price=800,
        goods_type=0    #Market goods type 0
    )
    test_item.store_owner = Store.query.filter_by(id=existing_store_with_user.id).first().id
    db.session.add(test_item)
    db.session.commit()
    test_item = Goods.query.filter_by(product_number="010101").first()
    yield test_item
    test_item = Goods.query.filter_by(product_number="010101").first()
    db.session.delete(test_item)
    db.session.commit()

@pytest.fixture()
def existing_item_in_auction(existing_store_user):
    test_item = Goods(
        name='test_item',
        description='description',
        product_number="010101",
        price=800,
        goods_type=1    #Market goods type 0
    )
    test_item.user_owner = User.query.filter_by(username=existing_store_user.username).first().id
    db.session.add(test_item)
    db.session.commit()
    test_item = Goods.query.filter_by(product_number="010101").first()
    yield test_item
    test_item = Goods.query.filter_by(product_number="010101").first()
    db.session.delete(test_item)
    db.session.commit()


@pytest.fixture()
def login_normal_user(client, existing_user):
    response = client.post('/login',
                data=dict(username='test_user', password="12345678"),
                follow_redirects=True)
    yield response
    client.get('/logout', follow_redirects=True)

@pytest.fixture()
def login_store_user(client, existing_store_user):
    response = client.post('/login',
                data=dict(username='test_user_store', password="12345678"),
                follow_redirects=True)
    yield response
    client.get('/logout', follow_redirects=True)

@pytest.fixture
def login_admin_user(client):
    client.post('/login',
                data=dict(username='Admin', password="12345678"),
                follow_redirects=True)
    yield client
    client.get('/logout', follow_redirects=True)

@pytest.fixture()
def add_goods_item_function(client, existing_store_user):
    name = "Test_samsung"
    description = "En samsung 11"
    price = 1500
    product_number = "000000"
    store_user_owner = existing_store_user.id

    add_market_item(name, description, price, product_number, store_user_owner)
    auction_item = Goods.query.filter_by(name="Test_samsung").first()
    yield auction_item
    db.session.delete(auction_item)
    db.session.commit()

@pytest.fixture()
def delete_test_bidding_item(client, existing_item_in_auction):
    existing_item_in_auction = existing_item_in_auction.id
    yield None
    delete_items = Bidding.query.filter_by(item_id=existing_item_in_auction)
    for delete_item in delete_items:
        db.session.delete(delete_item)
    db.session.commit()

@pytest.fixture()
def bidding_item(existing_user, existing_store_user, existing_item_in_auction):
    new_bid = Bidding(
        item_id=existing_item_in_auction.id,
        item_name=existing_item_in_auction.name,
        user_id=existing_user.id,
        user_name=existing_user.username,
        store_user_id=existing_store_user.id,
        offer=900
    )
    db.session.add(new_bid)
    db.session.commit()
    new_bid = Bidding.query.filter_by(item_id=existing_item_in_auction.id).first()
    yield new_bid
    db.session.delete(new_bid)
    db.session.commit()

@pytest.fixture()
def doing_a_bid(client, existing_store_with_user, existing_item_in_auction, existing_user, login_normal_user):
    existing_user_id_value = existing_user.id
    existing_item_in_auction_id = existing_item_in_auction.id

    data = {
        "store_owner1": f"{existing_store_with_user.id}",
        "bid_item": f"{existing_item_in_auction.product_number}",
        "offer": "900",
        "submit": "bid+for+product"
    }
    response = client.post('/auction', data=data, follow_redirects=True)
    yield existing_user_id_value, existing_item_in_auction_id
    print("do this after")

@pytest.fixture()
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





