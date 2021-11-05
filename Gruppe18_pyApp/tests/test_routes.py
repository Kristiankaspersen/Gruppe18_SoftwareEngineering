

def test_routes_status_home_page_with_fixture(client):
    response = client.get('/')
    assert response.status_code == 200
    response = client.get('/home')
    assert response.status_code == 200
    assert b"Welcome to App" in response.data


def test_routes_status_login(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"you have now logged in" in response.data
    response = client.post('/login')
    assert response.status_code == 405
    assert b"reenter log in" not in response.data


def test_routes_status_logout(client):
    response = client.get('/logout')
    assert response.status_code == 200
    assert b"you have now logged out" in response.data






def test_routes_status_register_page(client):
    assert client.get("/register").status_code == 200

def test_routes_status_add_goods_page(client):
    assert client.get("/goods").status_code == 200

