import pytest
from app_flask.models import User, db

#User model

def test_models_User_create_user(client):
    user = User(username="test_user", email='test_user@mail.com', password="12345678")
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(username="test_user").first()
    assert user
    db.session.delete(user)
    db.session.commit()

def test_models_User_filer_and_read_user():
    pass

def test_models_User_delete_user():
    pass

def test_models_User_update_user():
    pass

def test_models_User_have_enough_cash():
    pass

def test_models_User_checking_password_with_hash():
    pass



#Goods model

def test_models_Goods_create_goods():
    pass

def test_models_Goods_filer_and_read_goods():
    pass

def test_models_Goods_delete_goods():
    pass

def test_models_Goods_update_goods():
    pass

def test_models_Goods_purchase():
    pass

# Store model

def test_models_Goods_create_goods():
    pass

def test_models_Goods_filer_and_read_goods():
    pass

def test_models_Goods_delete_goods():
    pass

def test_models_Goods_update_goods():
    pass

# Bidding model

def test_models_Bidding_create_bid():
    pass

def test_models_Bidding_filer_and_read_bid():
    pass

def test_models_Bidding_delete_bid():
    pass

def test_models_Bidding_update_bid():
    pass







