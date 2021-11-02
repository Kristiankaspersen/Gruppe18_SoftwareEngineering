import pytest
from app_flask import app, db
from app_flask.routes import add_goods_with_parameter
from app_flask.models import Goods


def test_if_app_name_is_app_flask():
    assert app.name == "app_flask"


def test_if_app_secret_key_is_correct():
    assert app.secret_key == "5f4b0959c458e6b06c51097e"


def test_if_app_import_name_is_app_flask():
    assert app.import_name == "app_flask"


def test_if_app_template_folder_is_named_templates():
    assert app.template_folder == "templates"


def test_add_row_to_table_goods():  # Lagd en ny funksjon som tar parametere, testen er altså ikke helt rett
    add_goods_with_parameter("benk", "deilig og lite brukt", 69, 3)
    assert Goods.query.filter_by(name='benk').first()


def test_delete_row_from_table_goods():
    assert Goods.query.filter_by(name='benk').delete()
    db.session.commit()


@pytest.fixture(scope='module')
def new_item_to_goods():
    benk = Goods(name="benk", description="deilig og lite brukt", price=69, seller_id=3)
    return benk


def test_new_item_to_goods(new_item_to_goods):
    """Testing if Goods model work properly when creating a new 'goods'"""
    assert new_item_to_goods.name == "benk"
    assert new_item_to_goods.description == "deilig og lite brukt"
    assert new_item_to_goods.price == 69
    assert new_item_to_goods.seller_id == 3

