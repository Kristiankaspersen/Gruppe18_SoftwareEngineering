import pytest
from app_flask import app


# module byttes til hvis alle, function hører til routes
@pytest.fixture(scope='function')
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

        