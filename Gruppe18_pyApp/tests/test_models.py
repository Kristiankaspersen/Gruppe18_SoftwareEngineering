import pytest
from app_flask.models import User, db


@pytest.fixture
def add_user_in_db():
    user = User(username="test_user",
                email="test_user@mail.com",
                password="12345678",
                profile_type=True
                )
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(username="test_user").first()
    yield user
    db.session.delete(user)
    db.session.commit()


def test_models_create_user_in_db(add_user_in_db):
    assert add_user_in_db