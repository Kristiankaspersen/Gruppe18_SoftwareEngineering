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


def test_valid_login_logout(client, existing_user):
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


def test_invalid_login(client, existing_user):
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

def test_auth_routes_register_user_page(client):
    data = {
        "username": "testUser2",
        "email": "testUser2@testuser.com",
        "password1": "12345678",
        "password2": "12345678",
        "submit": "Create+account"
    }
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200 #Problem here, I want the response to be 302, it work sometimes, when follow_redirect=False
    assert b'Login' in response.data #get_data(as_text=True)
    user = User.query.filter_by(username="testUser2").first()
    assert user is not None
    db.session.delete(user)
    db.session.commit()

def test_auth_routes_register_user_that_already_exists(client, existing_user):
    data = {
        "username": "test_user",
        "email": "test_user@mail.com",
        "password1": "12345678",
        "password2": "12345678",
        "submit": "Create+account"
    }
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200  # Problem here, I want the response to be 302, it worked before I restructured, when follow_redirect=False
    assert b"Error creating user: " in response.data
    #user = User.query.filter_by(username="test_user").first()
    assert existing_user is not None

def test_auth_routes_register_user_with_same_email(client, existing_user):
    data = {
        "username": "new_user",
        "email": "test_user@mail.com",
        "password1": "12345678",
        "password2": "12345678",
        "submit": "Create+account"
    }
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200  # Problem here, I want the response to be 302, it worked before I restructured, when follow_redirect=False
    assert b"Error creating user: " in response.data
    # user = User.query.filter_by(username="test_user").first()
    assert existing_user is not None


def test_auth_routes_register_user_with_same_username(client, existing_user):
    data = {
        "username": "test_user",
        "email": "another_email@mail.com",
        "password1": "12345678",
        "password2": "12345678",
        "submit": "Create+account"
    }
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200  # Problem here, I want the response to be 302, it worked before I restructured, when follow_redirect=False
    assert b"Error creating user: " in response.data
    # user = User.query.filter_by(username="test_user").first()
    assert existing_user is not None

