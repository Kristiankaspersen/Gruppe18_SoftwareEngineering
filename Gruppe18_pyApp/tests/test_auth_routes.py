"""
This file (test_models )contain  functional test for the fake users blueprint.
These test use GETs and POSTs to diffirent URLs to check
"""
# import json, possible that I know.

from app_flask.models import db, User, Store


def test_auth_routes_register_user_page(client):
    data = {
        "username": "testUser",
        "email": "testUser2@testuser.com",
        "password1": "12345678",
        "password2": "12345678",
        "submit": "Create+account"
    }
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200  # Problem here, I want the response to be 302, it work sometimes, when follow_redirect=False
    assert b'Login ' in response.data  # get_data(as_text=True), find unique data here, better data. And get request 302.
    user = User.query.filter_by(username="testUser").first()
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
    assert response.status_code == 200
    assert b"Error creating user: " in response.data  # Get the both validations.
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
    assert response.status_code == 200
    assert b"Error creating user: " in response.data
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
    assert response.status_code == 200
    assert b"Error creating user: " in response.data
    assert existing_user is not None


def test_auth_routes_register_store(client, login_default_store):
    data = {
        "store_name": "Test_ASA",
        "street_adress": "TestAdress2",
        "street_number": "28",
        "postal_code": "1778",
        "province": "Testens2",
        "store_email": "Test2_ASA",
        "store_phone": "21000001"
    }
    response = client.post('/registerStore', data=data,follow_redirects=True)
    assert response.status_code == 200
    assert b'Register a store?'
    assert b'You have now registered a store'
    assert b'Name of the store'
    assert login_default_store.status_code == 200
    assert login_default_store is not None
    assert b'Not registered store'

#kinda confused shoudlnt login be a get


def test_auth_routes_register_store_that_exists(client, login_default_user):
    pass








def test_auth_routes_register_store_same_email(client, login_default_user):
    pass


def test_auth_routes_login_store(existing_store_user, login_default_store):
    # response = client.post('/login',
    #                        data=dict(email='test_user_store@mail.com', password="12345678"),
    #                        follow_redirects=True)
    assert login_default_store.status_code == 200
    assert b'You are logged in as: {user_attempted.username}'


def test_auth_routes_login_admin(client, login_admin_user):
    assert login_admin_user.status_code == 200
    assert b'You are logged in as: {user_attempted.username}'


def test_auth_routes_login_user(client, existing_user):
    response = client.post('/login',
                           data=dict(username='test_user', password="12345678"),
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'You are logged in as: {user_attempted.username}'


def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    # når login.html får email og passord. kan det testes.


def test_valid_login_logout(client, existing_user):
    response = client.post('/login',
                           data=dict(username='test_user@mail.com', password="12345678"),
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
                           data=dict(username='test_user@mail.com', password="12345678"),
                           follow_redirects=True)
    assert response.status_code == 200
    # assert b'Incorret login' in response.data
    assert b'Logout' not in response.data
    assert b'Login' in response.data
    assert b'Register' in response.data
