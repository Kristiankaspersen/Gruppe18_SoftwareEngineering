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
        "store_email": "EmailThatDontExist@gmail.com",
        "store_phone": "15352425",
        "submit": "Register+store"
    }
    response = client.post('/registerStore', data=data, follow_redirects=True)
    assert b"you have made a new store with name" in response.data
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

def test_auth_routes_login_with_correct_password_and_username(client, existing_user):
    data = {
        "username": "test_user",
        "password": "12345678",
        "submit": "Login"
    }
    response = client.get("/login")
    assert response.status_code == 200
    response = client.post('/login', data=data, follow_redirects=True)
    assert b"You are logged in as test_user" in response.data
    client.post('/logout')

def test_auth_routes_login_with_wrong_password(client, existing_user):
    data = {
        "username": "test_user",
        "password": "wrongPassword",
        "submit": "Login"
    }
    response = client.get("/login")
    assert response.status_code == 200
    response = client.post('/login', data=data, follow_redirects=True)
    assert b"Wrong password, or username" in response.data
    client.post('/logout')

def test_auth_routes_login_with_wrong_username(client, existing_user):
    data = {
        "username": "wrong_username",
        "password": "12345678",
        "submit": "Login"
    }
    response = client.get("/login")
    assert response.status_code == 200
    response = client.post('/login', data=data, follow_redirects=True)
    assert b"Wrong password, or username" in response.data
    client.post('/logout')







