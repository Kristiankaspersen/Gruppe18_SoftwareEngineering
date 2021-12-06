from app_flask.models import db, User, Goods, Store
from app_flask import create_app

app = create_app()
ctx = app.app_context()
ctx.push()

# Deletes everything in the DB, og oppretter den på nytt med nye tabeller.

db.drop_all()
db.create_all()

# Makes the DB again and restores it with information in the tables.


# To make this user, you need the server up running, because it sends a post request with an attampted user creation.

user_exist = User.query.filter_by(username="Geir").first()
if user_exist is None:
    user = User(
        username="Geir",
        email="Geir@dsad.com",
        password="12345678",
        profile_type=0
    )

    db.session.add(user)
    db.session.commit()

user_exist = User.query.filter_by(username="Tor").first()
if user_exist is None:
    user = User(
        username="Tor",
        email="Tor@dsad.com",
        password="12345678",
        profile_type=1
    )

    db.session.add(user)
    db.session.commit()

user_exist = User.query.filter_by(username="Bob").first()
if user_exist is None:
    user = User(
        username="Bob",
        email="Bob@Bob.com",
        password="12345678",
        profile_type=1
    )

    db.session.add(user)
    db.session.commit()


user_exist = User.query.filter_by(username="Per Ove").first()
if user_exist is None:
    user = User(
        username="Per Ove",
        email="per_ove@email.com",
        password="12345678",
        profile_type=0
    )
    db.session.add(user)
    db.session.commit()


# Creating a admin user
user_exist = User.query.filter_by(username="Admin").first()
if user_exist is None:
    user = User(
        username="Admin",
        email="Admin@example.com",
        password="12345678",
        profile_type=1  # Vurdere å bruke noe annet en boolean? Slik at man kan ha flere enn to typer
    )

    db.session.add(user)
    db.session.commit()

# Makes items directly in the DB. Uses username Geir as owner of the items.
store_exist = Store.query.filter_by(store_name="Store_AS").first()
if store_exist is None:
    store = Store(
        store_name='Store_AS',
        street_address="StoreAsAdress",
        street_number=22,
        postal_code=4314,
        province="Sandnes",
        store_email="Store_AS@gmail.com",
        store_phone=67876787
    )

    store.user_owner = User.query.filter_by(username="Tor").first().id
    db.session.add(store)
    db.session.commit()

store_exist = Store.query.filter_by(store_name="Old_AS").first()
if store_exist is None:
    store = Store(
        store_name='Old_AS',
        street_address="OldAsAdress",
        street_number=24,
        postal_code=4329,
        province="Sandnes",
        store_email="Old_AS@gmail.com",
        store_phone=87678767
    )
    # iphone.owner = User.query.filter_by(username="Geir").first().id
    store.user_owner = User.query.filter_by(username="Bob").first().id
    db.session.add(store)
    db.session.commit()

laptop_exist = Goods.query.filter_by(name="Laptop").first()
if laptop_exist is None:
    laptop = Goods(
        name='Laptop',
        description='description',
        product_number='123457',
        price=800,
        goods_type=1
    )
    laptop.user_owner = User.query.filter_by(username="Geir").first().id
    db.session.add(laptop)
    db.session.commit()

item_exist = Goods.query.filter_by(name="Iphone 10").first()
if item_exist is None:
    iphone = Goods(
        name='Iphone 10',
        description='description',
        product_number='123458',
        price=800,
        goods_type=1
    )
    iphone.store_owner = Store.query.filter_by(store_name="Store_AS").first().id
    db.session.add(iphone)
    db.session.commit()

item_exist = Goods.query.filter_by(name="Radio").first()
if item_exist is None:
    radio = Goods(
        name='Radio',
        description='description',
        product_number='223458',
        price=800,
        goods_type=0
    )
    radio.store_owner = Store.query.filter_by(store_name="Store_AS").first().id
    db.session.add(radio)
    db.session.commit()

book_exist = Goods.query.filter_by(name="Book").first()
if book_exist is None:
    book = Goods(
        name='Book',
        description='description',
        product_number='123459',
        price=300,
        goods_type=0
    )
    book.store_owner = Store.query.filter_by(store_name="Old_AS").first().id
    db.session.add(book)
    db.session.commit()

item_exist = Goods.query.filter_by(name="Chair").first()
if item_exist is None:
    chair = Goods(
        name='Chair',
        description='description',
        product_number='1234569',
        price=500,
        goods_type=1
    )
    chair.store_owner = Store.query.filter_by(store_name="Old_AS").first().id
    db.session.add(chair)
    db.session.commit()

item_exist = Goods.query.filter_by(name="Teapot").first()
if item_exist is None:
    teapot = Goods(
        name='Teapot',
        description='White old teapot',
        product_number='534569',
        price=75,
        goods_type=1
    )
    teapot.store_owner = Store.query.filter_by(store_name="Old_AS").first().id
    db.session.add(teapot)
    db.session.commit()

item_exist = Goods.query.filter_by(name="Vase").first()
if item_exist is None:
    vase = Goods(
        name='Vase',
        description='Very fine',
        product_number='534169',
        price=120,
        goods_type=0
    )
    vase.store_owner = Store.query.filter_by(store_name="Old_AS").first().id
    db.session.add(vase)
    db.session.commit()

item_exist = Goods.query.filter_by(name="Doll").first()
if item_exist is None:
    doll = Goods(
        name='Doll',
        description='Kinda creepy',
        product_number='534129',
        price=230,
        goods_type=0
    )
    doll.store_owner = Store.query.filter_by(store_name="Store_AS").first().id
    db.session.add(doll)
    db.session.commit()

item_exist = Goods.query.filter_by(name="Jewelry").first()
if item_exist is None:
    jewelry = Goods(
        name='Jewelry',
        description='With diamonds',
        product_number='534139',
        price=10000,
        goods_type=1
    )
    jewelry.store_owner = Store.query.filter_by(store_name="Store_AS").first().id
    db.session.add(jewelry)
    db.session.commit()

item_exist = Goods.query.filter_by(name="Golden ring").first()
if item_exist is None:
    ring = Goods(
        name='Golden ring',
        description='Shiny nice ring',
        product_number='534149',
        price=5000,
        goods_type=0
    )
    ring.store_owner = Store.query.filter_by(store_name="Store_AS").first().id
    db.session.add(ring)
    db.session.commit()

item_exist = Goods.query.filter_by(name="Necklace").first()
if item_exist is None:
    necklace = Goods(
        name='Necklace',
        description='Owned by a famous singer',
        product_number='534159',
        price=999,
        goods_type=0
    )
    necklace.store_owner = Store.query.filter_by(store_name="Store_AS").first().id
    db.session.add(necklace)
    db.session.commit()

item_exist = Goods.query.filter_by(name="Bronze necklace").first()
if item_exist is None:
    bronze_necklace = Goods(
        name='Bronze necklace',
        description='Found in the dirt',
        product_number='534179',
        price=145,
        goods_type=0
    )
    bronze_necklace.store_owner = Store.query.filter_by(store_name="Old_AS").first().id
    db.session.add(bronze_necklace)
    db.session.commit()

item_exist = Goods.query.filter_by(name="Antique shoes").first()
if item_exist is None:
    antique_shoes = Goods(
        name='Antique shoes',
        description='Found in the dirt',
        product_number='534170',
        price=1450,
        goods_type=0
    )
    antique_shoes.store_owner = Store.query.filter_by(store_name="Old_AS").first().id
    db.session.add(antique_shoes)
    db.session.commit()

item_exist = Goods.query.filter_by(name="Viking helmet").first()
if item_exist is None:
    viking_helmet = Goods(
        name='Viking helmet',
        description='From Norway',
        product_number='534171',
        price=9001,
        goods_type=1
    )
    viking_helmet.store_owner = Store.query.filter_by(store_name="Old_AS").first().id
    db.session.add(viking_helmet)
    db.session.commit()

print(User.query.filter_by(username="Geir").first())
print(User.query.filter_by(username="Tor").first())
print(User.query.filter_by(username="Bob").first())
print(User.query.filter_by(username="Admin").first())
print(Goods.query.filter_by(name="Laptop").first())
print(Goods.query.filter_by(name="Iphone 10").first())
print(Goods.query.filter_by(name="book").first())
print(Goods.query.filter_by(name="Chair").first())
print(Store.query.filter_by(store_name="Store_AS").first())
print(Store.query.filter_by(store_name="Old_AS").first())

ctx.pop()
