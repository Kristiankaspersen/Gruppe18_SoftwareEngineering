

def test_RegisterUserForm(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_RegisterStoreForm():
    pass

def test_LoginFormUser():
    pass