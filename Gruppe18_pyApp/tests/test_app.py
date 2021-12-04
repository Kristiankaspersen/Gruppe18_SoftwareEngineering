# import pytest
# from app_flask.models import User, db
# from app_flask.models import Goods
# from app_flask.routes import delete_goods


# def test_if_app_name_is_app_flask():
#     assert app.name == "app_flask"
#
#
# def test_if_app_secret_key_is_correct():
#     assert app.secret_key == "5f4b0959c458e6b06c51097e"
#
#
# def test_if_app_import_name_is_app_flask():
#     assert app.import_name == "app_flask"
#
#
# def test_if_app_template_folder_is_named_templates():
#     assert app.template_folder == "templates"
#
#
# # def test_delete_row_from_table_goods():
# #     assert Goods.query.filter_by(name='benk').delete()
# #     db.session.commit()
#
#
# @pytest.fixture(scope='module')
# def new_object_of_goods():
#     benk = Goods(name='Benk',
#                  description='Laget i tre',
#                  product_number='123459',
#                  price=50)
#     return benk
#
#
# def test_if_model_goods_can_create_object(new_object_of_goods):
#     """Testing if Goods model name, description and price work properly when creating a new items"""
#     assert new_object_of_goods.name == "Benk"
#     assert new_object_of_goods.description == "Laget i tre"
#     assert new_object_of_goods.price == 50
#
#
# def test_query_all_rows_from_goods():
#     rows = db.session.query(Goods).count()
#     assert rows == 5
#
#
# def test_remove_a_item_from_goods():
#     rows = db.session.query(Goods).count()
#     assert delete_goods(id=2)
#
#
# def test_if_admin_user_can_be_found_in_user_list(client):
#     user = client.get('/users')
#     assert b"Admin" not in user.data