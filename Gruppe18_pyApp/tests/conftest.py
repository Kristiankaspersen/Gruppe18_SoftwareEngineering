import pytest
from app_flask import create_app
from app_flask.models import User, db
import requests

@pytest.fixture(scope='module')
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        with app.test_client() as client:
            yield client

# kaller den init_db ( brukt for i add_user_in_db kun byttet)
@pytest.fixture(scope='module')
def existing_user(client):
    user = User(username="test_user", email='test_user@mail.com', password="12345678")
    db.session.add(user)
    db.session.commit()

    user = User.query.filter_by(username="test_user").first()
    yield user
    db.session.delete(user)
    db.session.commit()

@pytest.fixture(scope='function')
def login_default_user(client):
    client.post('/login',
                data=dict(email='test_user@mail.com', password="12345678"),
                follow_redirects=True)
    yield
    client.get('/logout', follow_redirects=True)
