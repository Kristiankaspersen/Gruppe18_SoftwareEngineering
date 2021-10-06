from app.routes import configure_routes
from flask import Flask


def test_home_page_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()

    response = client.get("/")
    assert response.get_data() == b'<h1>Home Page</h1>'
    assert response.status_code == 200
