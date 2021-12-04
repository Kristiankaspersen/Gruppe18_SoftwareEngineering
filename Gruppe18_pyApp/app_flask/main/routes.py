from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_user, logout_user, current_user
from app_flask import db
from app_flask.main import bp
from app_flask.main.forms import RegisterUserForm, LoginFormUser, LoginFormStore, FormGoods, BuyGoodsForm, RegisterStoreForm, \
    LoginFormAdmin, AcceptAuctionForm, AuctionGoodsForm
from app_flask.models import User, Goods, Store, Bidding
from sqlalchemy.sql.expression import func

@bp.route("/")
@bp.route("/home")
def home_page():
    return render_template("index.html")


@bp.route("/test")
def test_page():
    return "<h1>Home Page</h1>"


@bp.route("/register", methods=['GET', 'POST'])
def register_user_page():
    form = RegisterUserForm()
    if form.validate_on_submit():
        creating_user_in_db = User(username=form.username.data,
                                   email=form.email.data,
                                   password=form.password1.data,
                                   profile_type=form.profile_type.data)
        db.session.add(creating_user_in_db)
        db.session.commit()
        return redirect(url_for('main.show_owned_goods'))
    if form.errors != {}:  # This happens if the users do somthing wrong when creating a user
        for err_message in form.errors.values():
            flash(f"Error creating user: {err_message}")
    return render_template("registerUser.html", form=form)


@bp.route("/registerStore", methods=["GET", "POST"])
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
        return redirect(url_for('main.market_page'))

    return render_template("registerStore.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for("main.store_page"))
        else:
            flash("Wrong password, or username")

    return render_template("login.html", form_user=form_user, form_store=form_store, form_admin=form_admin)


@bp.route("/logout")
def logout_page():
    logout_user()
    flash("You have logged out")
    return redirect(url_for('main.home_page'))


@bp.route('/goods', methods=['GET', 'POST'])
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


@bp.route('/owned_goods', methods=['GET', 'POST'])
def show_owned_goods():
    db_goods = db.session.query(User, Goods).filter(User.id == Goods.user_owner).all()

    # return render_template('friends.html', userList=userList)
    # db_goods = Goods.query.order_by(Goods.name)

    return render_template('showGoods.html', db_goods=db_goods)


@bp.route("/store", methods=["POST", "GET"])
def store_page():
    buy_form = BuyGoodsForm()
    auction_form = AuctionGoodsForm()
    accept_form = AcceptAuctionForm()

    if request.method == "POST":
        # Buying product:
        buy_item = request.form.get('bought_item')
        bought_from_store = request.form.get('store_owner')
        # Here it can be wise to pick up the product number instead
        bought_item = Goods.query.filter_by(name=buy_item).first()
        store_owner_item = User.query.filter_by(id=bought_from_store).first()
        if (bought_item is not None) and (store_owner_item is not None):
            if current_user.have_enough_cash(bought_item):
                bought_item.purchase(current_user, store_owner_item)
                flash(f"You have bought {bought_item.name} for {bought_item.price}")
            else:
                flash(f"You don't have enough money to purchase {bought_item.name}")

        # Bidding on product:
        bid_item = request.form.get('bid_item')
        # current_price = request.form.get('current_price')
        bid_from_store = request.form.get('store_owner1')
        # Here it can be wise to pick up the product number instead
        item_bidded_on = Goods.query.filter_by(name=bid_item).first()
        store_bidding_from = User.query.filter_by(id=bid_from_store).first()
        if (item_bidded_on is not None) and (store_bidding_from is not None):
            if auction_form.offer.data >= item_bidded_on.price + 10:  # current_price:
                item_bidded_on.price = auction_form.offer.data
                new_bid = Bidding(
                    item_id=item_bidded_on.id,
                    item_name=item_bidded_on.name,
                    user_id=current_user.id,
                    user_name=current_user.username,
                    store_user_id=store_bidding_from.id,
                    offer=auction_form.offer.data
                )
                db.session.add(new_bid)
                db.session.commit()
            else:
                flash("You have to bid more than that")

        accept_item = request.form.get('accepting_item')
        accept_from_user = request.form.get('accepting_user')
        accepting_item = Goods.query.filter_by(name=accept_item).first()
        user_bidding_item = User.query.filter_by(id=accept_from_user).first()
        if (accepting_item is not None) and (user_bidding_item is not None):
            if user_bidding_item.have_enough_cash(accepting_item):
                accepting_item.purchase(user_bidding_item, current_user)
                flash(f"You have accepted offer on {accepting_item.name} for {accepting_item.price}")
                delete_items = Bidding.query.filter_by(item_name=accept_item)
                for delete_item in delete_items:
                    db.session.delete(delete_item)
                db.session.commit()
            else:
                flash(f"{user_bidding_item.username} don't have enough money to purchase {accepting_item.name}")
        return redirect(url_for('main.store_page'))

    if request.method == "GET":
        # items = db.session.query(Goods, Store).join(Store).all()
        items = db.session.query(Goods, Store).filter(Store.id == Goods.store_owner).all()
        try:
            current_store = Store.query.filter_by(user_owner=current_user.id).first()
            if current_store is not None:
                bidding_items = Bidding.query. \
                    with_entities(Bidding.item_name, Bidding.offer, Bidding.user_name, Bidding.user_id, Bidding.id,
                                  func.max(Bidding.offer)) \
                    .group_by(Bidding.item_name).filter_by(store_user_id=current_user.id)
            else:
                bidding_items = []
        except AttributeError:
            bidding_items = []

        return render_template("store.html", items=items, buy_form=buy_form, auction_form=auction_form,
                               bidding_items=bidding_items, accept_form=accept_form)


@bp.route('/users', methods=['GET', 'POST'])
def show_users():
    db_users = User.query.filter(User.username.isnot("Admin"))
    return render_template('users.html', db_users=db_users)


@bp.route('/delete/<int:id>')
def delete_user(id):
    user_to_delete = User.query.filter_by(id=id).first()
    db.session.delete(user_to_delete)
    db.session.commit()
    db_users = User.query.order_by(User.username)
    return render_template('index.html', db_users=db_users)


@bp.route('/delete/<int:id>')
def delete_goods(id):
    goods_to_delete = Goods.query.filter_by(id=id).first()
    form = FormGoods()
    db.session.delete(goods_to_delete)
    db.session.commit()
    db_goods = Goods.query.order_by(Goods.name)
    return render_template('index.html', form=form, db_goods=db_goods)