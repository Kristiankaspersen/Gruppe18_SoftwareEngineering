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


@pytest.fixture(scope='module')
def existing_user(client):
    user = User(username="test_user", email='test_user@mail.com', password="12345678")
    db.session.add(user)
    db.session.commit()

    user = User.query.filter_by(username="test_user").first()
    yield user
    db.session.delete(user)
    db.session.commit()

@pytest.fixture(scope='module')
def existing_store(client, existing_user):
    store = Store(
        store_name='Test_AS',
        street_address="TestAdress",
        street_number=28,
        postal_code=6329,
        province="Testnes",
        store_email="Test_AS@gmail.com",
        store_phone=67326732
    )
    # iphone.owner = User.query.filter_by(username="Geir").first().id
    store.user_owner = User.query.filter_by(username="test_user").first().id
    yield store
    db.session.add(store)
    db.session.commit()

@pytest.fixture(scope='function')
def login_default_user(client, existing_user):
    client.post('/login',
                data=dict(email='test_user@mail.com', password="12345678"),
                follow_redirects=True)
    yield
    client.get('/logout', follow_redirects=True)

@pytest.fixture(scope='function')
def login_default_store(client, existing_store):
    client.post('/login',
                data=dict(email='test_user@mail.com', password="12345678"),
                follow_redirects=True)
    yield
    client.get('/logout', follow_redirects=True)
