"""
This file (test_models )contain  functional test for the fake users blueprint.
These test use GETs and POSTs to diffirent URLs to check
"""
import json

from app_flask.models import db, User, Goods, Store
from app_flask import create_app


def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    # når login.html får email og passord. kan det testes.


def test_valid_login_logout(client, init_db):
    response = client.post('/login',
                           data=dict(email='test_user@mail.com', password="12345678"),
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'You are logged in as: {user_attempted.username}'
    assert b'Login' in response.data
    # not in register check

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have logged out' in response.data
    assert b'Logout' not in response.data
    assert b'Login' in response.data
    assert b'Register' in response.data


def test_invalid_login(client, init_db):
    response = client.post('/login',
                           data=dict(email='test_user@mail.com', password="12345678"),
                           follow_redirects=True)
    assert response.status_code == 200
    # assert b'Incorret login' in response.data
    assert b'Logout' not in response.data
    assert b'Login' in response.data
    assert b'Register' in response.data

""" 
 Test registeruser from conftest, by adding a new user
"""


def test_RegisterUserForm(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_routes_register_page(client):
    data = {
        "username": "testUser2",
        "email": "testUser2@testuser.com",
        "password1": "12345678",
        "password2": "12345678",
        "submit": "Create+account"
    }
    respoone = client.post('/register', data=data, follow_redirects=False)
    assert respoone.status_code == 302
    user = User.query.filter_by(username="testUser2").first()
    assert user is not None
    db.session.delete(user)
    db.session.commit()
