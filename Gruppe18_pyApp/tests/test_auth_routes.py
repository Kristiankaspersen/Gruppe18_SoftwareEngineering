"""
This file (test_models )contain  functional test for the fake users blueprint.
These test use GETs and POSTs to diffirent URLs to check
"""
# import json, possible that I know.

from app_flask.models import db, User, Store


def test_auth_routes_register_user_page_and_check_if_stored_in_db(client):
    data = {
        "username": "testUser",
        "email": "testUser2@testuser.com",
        "password1": "12345678",
        "password2": "12345678",
        "submit": "Create+account"
    }
    response = client.get('/register')
    assert response.status_code == 200
    client.post('/register', data=data, follow_redirects=True)
    user = User.query.filter_by(username="testUser").first()
    assert user is not None
    db.session.delete(user)
    db.session.commit()

def test_auth_routes_register_user_page_check_valid_user(client):
    data = {
        "username": "testUser",
        "email": "testUser2@testuser.com",
        "password1": "12345678",
        "password2": "12345678",
        "submit": "Create+account"
    }
    response = client.post('/register', data=data, follow_redirects=True)
    user = User.query.filter_by(username="testUser").first()
    db.session.delete(user)
    db.session.commit()
    assert b'You have made a user with username testUser' in response.data

def test_auth_routes_register_user_with_same_usename(client, existing_user):
    data = {
        "username": "test_user",
        "email": "another@mail.com",
        "password1": "12345678",
        "password2": "12345678",
        "submit": "Create+account"
    }
    assert existing_user is not None
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Username is already in use! try a different username' in response.data

def test_auth_routes_register_user_with_same_email(client, existing_user):
    data = {
        "username": "another_user_name",
        "email": "test_user@mail.com",
        "password1": "12345678",
        "password2": "12345678",
        "submit": "Create+account"
    }
    assert existing_user is not None
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Email is already in use! Use another email' in response.data

def test_auth_routes_register_user_that_already_exists(client, existing_user):
    data = {
        "username": "test_user",
        "email": "test_user@mail.com",
        "password1": "12345678",
        "password2": "12345678",
        "submit": "Create+account"
    }
    assert existing_user is not None
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Username is already in use! try a different username" in response.data
    assert b'Email is already in use! Use another email' in response.data

def test_auth_routes_register_store_with_store_that_dont_exist(client, login_normal_user):
    data = {
        "store_name": "Test_ASA",
        "street_address": "TestAdress",
        "street_number": "28",
        "postal_code": "1778",
        "province": "Testnes",
        "store_email": "Test_ASA@gmail.com",
        "store_phone": "21000001",
        "submit": "Register+store"
    }
    response = client.post('/registerStore', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert login_normal_user.status_code == 200
    assert b"you have made a new store with name Test_ASA" in response.data
    store = Store.query.filter_by(store_name="Test_ASA").first()
    assert store is not None
    db.session.delete(store)
    db.session.commit()

def test_auth_routes_register_store_with_same_store_name(client, login_normal_user, existing_store_with_user):
    data = {
        "store_name": "Test_AS2",
        "street_address": "TestAdress",
        "street_number": "28",
        "postal_code": "6329",
        "province": "Testnes",
        "store_email": "Test_AS2@gmail.com",
        "store_phone": "67326732",
        "submit": "Register+store"
    }
    assert existing_store_with_user is not None
    response = client.post('/registerStore', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert login_normal_user.status_code == 200
    assert b"Store name Test_AS2 is already in use! try a different store name" in response.data

def test_auth_routes_register_store_with_different_email_adress(client, login_normal_user, existing_store_with_user):
    data = {
        "store_name": "Another_username",
        "street_address": "TestAdress",
        "street_number": "28",
        "postal_code": "6329",
        "province": "Testnes",
        "store_email": "Test_AS2@gmail.com",
        "store_phone": "67326732",
        "submit": "Register+store"
    }
    assert existing_store_with_user is not None
    response = client.post('/registerStore', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert login_normal_user.status_code == 200
    assert b"Email Test_AS2@gmail.com is already in use! use a different email" in response.data

def test_auth_routes_register_store_that_already_exists(client, login_normal_user, existing_store_with_user):
    data = {
        "store_name": "Test_AS2",
        "street_address": "TestAdress",
        "street_number": "28",
        "postal_code": "6329",
        "province": "Testnes",
        "store_email": "Test_AS2@gmail.com",
        "store_phone": "67326732",
        "submit": "Register+store"
    }
    assert existing_store_with_user is not None
    response = client.post('/registerStore', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert login_normal_user.status_code == 200
    assert b"Store name Test_AS2 is already in use! try a different store name" in response.data



# kinda confused shoudlnt login be a get

"""def test_auth_routes_register_store_that_exists(client, login_default_user):"""


¨



def test_auth_routes_register_store_same_email(client, existing_store_user):
    data = {
        "store_name": "Test_Ltd",
        "street_adress": "TestAdress_ltd",
        "street_number": "289",
        "postal_code": "63291",
        "province": "Testens3",
        "store_email": "Test_AS@gmail.com",
        "store_phone": "673267325"
    }
    response = client.post('/registerStore', data=data, follow_redirects=True)
    assert response.status_code == 200
    #assert b"Error the email is taken: " in response.data
    assert existing_store_user is not None



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
