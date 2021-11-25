"""
This file (test_models )contain  functional test for the fake users blueprint.
These test use GETs and POSTs to diffirent URLs to check
"""


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

# response = client.get("/")

def test_routes_register_page(register_user):
    assert register_user


# def test_valid_registration
