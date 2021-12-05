import pytest
from app_flask import create_app
from app_flask.models import User, Store, db
import requests

@pytest.fixture(scope='module')
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
def login_default_user(client, existing_user):
    client.post('/login',
                data=dict(username='test_user', password="12345678"),
                follow_redirects=True)
    yield client
    client.get('/logout', follow_redirects=True)

@pytest.fixture()
def login_default_store(client, existing_store_user):
    client.post('/login',
                data=dict(username='test_user_store', password="12345678"),
                follow_redirects=True)
    yield
    client.get('/logout', follow_redirects=True)

@pytest.fixture
def login_admin_user(client):
    client.post('/login',
                data=dict(username='Admin', password="12345678"),
                follow_redirects=True)
    yield
    client.get('/logout', follow_redirects=True)

