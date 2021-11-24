from app_flask.models import db, User, Goods, Store

# Deletes everything in the DB, og oppretter den på nytt med nye tabeller.

db.drop_all()
db.create_all()

#Makes the DB again and restores it with information in the tables.


#To make this user, you need the server up running, because it sends a post request with an attampted user creation.

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

laptop_exist = Goods.query.filter_by(name="Laptop").first()
if laptop_exist is None:
    laptop = Goods(
        name='Laptop',
        description='description',
        product_number='123456',
        price=800
    )
    laptop.user_owner = User.query.filter_by(username="Geir").first().id
    db.session.add(laptop)
    db.session.commit()

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
    #iphone.owner = User.query.filter_by(username="Geir").first().id
    store.user_owner = User.query.filter_by(username="Bob").first().id
    db.session.add(store)
    db.session.commit()

laptop_exist = Goods.query.filter_by(name="Laptop").first()
if laptop_exist is None:
    laptop = Goods(
        name='Laptop',
        description='description',
        product_number='123457',
        price=800
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
        price=800
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
        price=800
    )
    radio.store_owner = Store.query.filter_by(store_name="Store_AS").first().id
    db.session.add(radio)
    db.session.commit()

book_exist = Goods.query.filter_by(name="book").first()
if book_exist is None:
    book = Goods(
        name='book',
        description='description',
        product_number='123459',
        price=300
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
        price=500
    )
    chair.store_owner = Store.query.filter_by(store_name="Old_AS").first().id
    db.session.add(chair)
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
