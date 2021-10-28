import pytest
from app_flask import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_routes_status_home_page(client):
    assert client.get("/").status_code == 200
    assert client.get("/home").status_code == 200

def test_routes_status_register_page(client):
    assert client.get("/register").status_code == 200

def test_routes_status_add_goods_page(client):
    assert client.get("/goods").status_code == 200

