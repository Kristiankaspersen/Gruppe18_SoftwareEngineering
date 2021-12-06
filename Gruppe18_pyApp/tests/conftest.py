import pytest
from app_flask import create_app
from app_flask.models import User, Store, db, Goods
import requests

@pytest.fixture(scope='module')
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        with app.test_client() as client:
            yield client

@pytest.fixture(scope='module')
def context():
    pass

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
    yield test_item
    db.session.delete(test_item)
    db.session.commit()

@pytest.fixture()
def existing_item_in_market(existing_store_user):
    test_item = Goods(
        name='test_item',
        description='description',
        product_number='010101',
        price=800,
        goods_type=0    #Market goods type 0
    )
    test_item.user_owner = User.query.filter_by(username=existing_store_user.username).first().id
    db.session.add(test_item)
    db.session.commit()
    yield test_item
    db.session.delete(test_item)
    db.session.commit()

@pytest.fixture()
def existing_item_in_auction(existing_store_user):
    test_item = Goods(
        name='test_item',
        description='description',
        product_number='010101',
        price=800,
        goods_type=1    #Market goods type 0
    )
    test_item.user_owner = User.query.filter_by(username=existing_store_user.username).first().id
    db.session.add(test_item)
    db.session.commit()
    yield test_item
    db.session.delete(test_item)
    db.session.commit()


@pytest.fixture()
def login_default_user(client, existing_user):
    response = client.post('/login',
                data=dict(username='test_user', password="12345678"),
                follow_redirects=True)
    yield response
    client.get('/logout', follow_redirects=True)

@pytest.fixture()
def login_default_store(client, existing_store_user):
    response = client.post('/login',
                data=dict(username='test_user_store', password="12345678"),
                follow_redirects=True)
    yield response
    client.get('/logout', follow_redirects=True)

@pytest.fixture
def login_admin_user(client):
    response = client.post('/login',
                data=dict(username='Admin', password="12345678"),
                follow_redirects=True)
    yield response
    client.get('/logout', follow_redirects=True)

