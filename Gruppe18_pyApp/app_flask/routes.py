from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from app_flask import app, db
from app_flask.forms import RegisterUserForm, LoginFormUser, LoginFormStore, FormGoods, BuyGoodsForm, RegisterStoreForm, \
    LoginFormAdmin
from app_flask.models import User, Goods, Store


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")


@app.route("/test")
def test_page():
    return "<h1>Home Page</h1>"


@app.route("/register", methods=['GET', 'POST'])
def register_user_page():
    form = RegisterUserForm()
    if form.validate_on_submit():
        creating_user_in_db = User(username=form.username.data,
                                   email=form.email.data,
                                   password=form.password1.data,
                                   profile_type=form.profile_type.data)
        db.session.add(creating_user_in_db)
        db.session.commit()
        return redirect(url_for('show_goods'))
    if form.errors != {}:  # This happens if the users do somthing wrong when creating a user
        for err_message in form.errors.values():
            flash(f"Error creating user: {err_message}")
    return render_template("registerUser.html", form=form)


@app.route("/registerStore", methods=["GET", "POST"])
def register_store():
    form = RegisterStoreForm()

    if form.validate_on_submit():
        create_store = Store(
                        store_name=form.store_name.data,
                        street_address=form.street_address.data,
                        street_number=form.street_number.data,
                        postal_code=form.postal_code.data,
                        province=form.province.data,
                        store_email=form.store_email.data,
                        store_phone=form.store_phone.data
                             )

        create_store.owner = current_user.id
        db.session.add(create_store)
        current_user.profile_type = 1
        db.session.commit()

        flash("You have made a new store")
        return redirect(url_for('market_page'))

    return render_template("registerStore.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form_user = LoginFormUser()
    form_store = LoginFormStore()
    # Admin
    form_admin = LoginFormAdmin()
    if form_user.validate_on_submit():
        if request.form.get('Geir') is not None:
            user_attempted = User.query.filter_by(username="Geir").first()
        elif request.form.get('Tor') is not None:
            user_attempted = User.query.filter_by(username="Tor").first()
            # Admin
        elif request.form.get('Admin') is not None:
            user_attempted = User.query.filter_by(username="Admin").first()
        else:
            user_attempted = None

        if (user_attempted is not None) and user_attempted.checking_password_with_hash(
                password_attempted="12345678"
        ):
            login_user(user_attempted)
            flash(f"You are logged in as: {user_attempted.username}")
            return redirect(url_for("store_page"))
        else:
            flash("Wrong password, or username")

    return render_template("login.html", form_user=form_user, form_store=form_store, form_admin=form_admin)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have logged out")
    return redirect(url_for('home_page'))


@app.route('/goods', methods=['GET', 'POST'])
def add_goods():
    form = FormGoods()
    if form.validate_on_submit():
        new_goods = Goods(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            product_number=form.product_number.data
        )
        # Clear the form ''
        form.name.data = ''
        form.description.data = ''
        form.price.data = ''
        db.session.add(new_goods)
        db.session.commit()
        flash("Item added to the store")

    db_goods = Goods.query.order_by(Goods.name)
    return render_template('addGoods.html', form=form, db_goods=db_goods)


def add_goods_with_parameter(name, description, price, seller_id):
    new_goods = Goods(name=name, description=description, price=price, seller_id=seller_id)
    db.session.add(new_goods)
    db.session.commit()


@app.route('/owned_goods', methods=['GET', 'POST'])
def show_owned_goods():
    db_goods = db.session.query(User, Goods).filter(User.id == Goods.user_owner).all()

    # return render_template('friends.html', userList=userList)
    # db_goods = Goods.query.order_by(Goods.name)

    return render_template('showGoods.html', db_goods=db_goods)


@app.route("/store", methods=["POST", "GET"])
def store_page():
    buy_form = BuyGoodsForm()

    if request.method == "POST":
        buy_item = request.form.get('bought_item')
        bought_item = Goods.query.filter_by(name=buy_item).first()
        print(bought_item)
        if bought_item is not None:
            if current_user.have_enough_cash(bought_item):
                bought_item.purchase(current_user)
                flash(f"You have bought {bought_item.name} for {bought_item.price}")
            else:
                flash(f"You don't have enough money to purchase {bought_item.name}")
        return redirect(url_for('store_page'))

    if request.method == "GET":
        # items = db.session.query(Goods, Store).join(Store).all()
        items = db.session.query(Goods, Store).filter(Store.id == Goods.store_owner).all()
        print(items)

        return render_template("store.html", items=items, buy_form=buy_form)


@app.route('/users', methods=['GET', 'POST'])
def show_users():

    db_users = User.query.order_by(User.username)
    # db_goods = Goods.query.order_by(Goods.name)

    return render_template('users.html', db_users=db_users)


@app.route('/delete/<int:id>')
def delete_goods(id):
    goods_to_delete = Goods.query.filter_by(id=id).first()
    form = FormGoods()
    db.session.delete(goods_to_delete)
    db.session.commit()
    db_goods = Goods.query.order_by(Goods.name)
    return render_template('index.html', form=form, db_goods=db_goods)
