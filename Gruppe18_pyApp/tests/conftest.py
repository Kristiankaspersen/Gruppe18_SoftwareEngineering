import pytest
from app_flask import app
from app_flask.models import User, db


@pytest.fixture(scope='module')
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# kaller den init_db ( brukt for i add_user_in_db kun byttet)
@pytest.fixture(scope='module')
def init_db(client):
    # creats database and table by func called init_db
    db.create_all()
    # insert test users call it one
    user = User(email='test_user@mail.com', username="test_user", password="12345678")
    db.session.add(user)
    db.session.commit()

    user = User.query.filter_by(username="test_user").first()
    yield user
    db.session.delete(user)
    db.session.commit()

# TODO: Create a new fake_user and connect with test_routes and create def for test_valid_regist
# TODO: create full login.html, so it will be esaier to have more tests

# this has to get connected with login_validation, right now dont work


@pytest.fixture(scope='function')
def login_default_user(client):
    client.post('/login',
                data=dict(email='test_user@mail.com', password="12345678"),
                follow_redirects=True)
    yield
    client.get('/logout', follow_redirects=True)
