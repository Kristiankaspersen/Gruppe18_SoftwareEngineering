import flask
import pytest
from app_flask import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.client() as client:
        yield client

# prøvd test client eller client samme problem

    """ 
def test_routes_status_home_page(test_client):
    assert test_client.get("/").status_code == 200
    assert test_client.get("/home").status_code == 200

def test_routes_status_register_page(test_client):
    assert test_client.get("/register").status_code == 200

def test_routes_status_add_goods_page(test_client):
    assert test_client.get("/goods").status_code == 200 
    """


# Post and get
""" config test for Flask app
    page is requested (get)
    validate 
"""


# TODO: error not found test_client

# get
def test_routes_status_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    response = test_client.get(flask.url_for('index.html'))
    assert response.status_code == 200
    assert b"Welcome to App" in response.data


def test_routes_status_login(test_client):
    response = test_client.get(flask.url_for('login.html'))
    assert response.status_code == 200
    assert b"you have now logged in" in response.data
    response = test_client.post(flask.url_for('login.html'))
    assert response.status_code == 405
    assert b"You have now logged in" not in response.data


def test_routes_status_logout(test_client):
    response = test_client.get(flask.url_for('index.html'))
    assert response.status_code == 200
    assert b"you have now logged out" in response.data
