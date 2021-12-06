from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_user, logout_user, current_user
from app_flask import db
from app_flask.main import bp
from app_flask.main.forms import AddGoodsToMarket, AddGoodsToAuction, BuyGoodsForm, AcceptAuctionForm, AuctionGoodsForm
from app_flask.main.use_cases import buying_product, show_current_highest_bidding_offer_in_store, show_users_from_db, \
    delete_user_from_platform, delete_goods_from_store, add_market_item, add_auction_item, bidding_on_product, \
    accepting_bidding_offer
from app_flask.models import User, Goods, Store, Bidding
from sqlalchemy.sql.expression import func, and_


@bp.route("/")
@bp.route("/home")
def home_page():
    return render_template("index.html")


@bp.route('/goods', methods=['GET', 'POST'])
def add_goods():
    form_auction = AddGoodsToAuction()
    form_market = AddGoodsToMarket()

    if request.method == "POST":

        name = form_auction.name.data
        description = form_auction.description.data
        price = form_auction.price.data
        product_number = form_auction.product_number.data
        store_user_owner = current_user.id
        print(request.form.get('auctionItem'))
        if request.form.get('auctionItem') is not None:
            add_auction_item(name, description, price, product_number, store_user_owner)
            print("dog")
            flash("(name of item) added to the auction market")
        else:
            add_market_item(name, description, price, product_number, store_user_owner)
            flash("(name of item) added to the store market")
        return redirect(url_for('main.add_goods'))

    if form_auction.errors != {}:  # This happens if the users do somthing wrong when creating a user
        for err_message in form_auction.errors.values():
            flash(f"Error posting market product: {err_message}")

    if form_market.errors != {}:  # This happens if the users do somthing wrong when creating a user
        for err_message in form_market.errors.values():
            flash(f"Error posting market product: {err_message}")

    if request.method == "GET":
        return render_template('addGoods.html', form_auction=form_auction, form_market=form_market)


@bp.route('/owned_goods', methods=['GET', 'POST'])
def show_owned_goods():
    db_goods = db.session.query(User, Goods).filter(User.id == Goods.user_owner).all()
    # FIXME: Denne trenger og bare vise tingene som eies av en person, template skal ikke inneholde delete.
    # return render_template('friends.html', userList=userList)
    # db_goods = Goods.query.order_by(Goods.name)

    return render_template('showGoods.html', db_goods=db_goods)


@bp.route("/store", methods=["POST", "GET"])
def store_page():
    buy_form = BuyGoodsForm()

    if request.method == "POST":
        buy_item_product_number = request.form.get('bought_item')
        bought_from_store = request.form.get('store_owner')


        bool_value = buying_product(buy_item_product_number, bought_from_store, current_user.id)
        bought_item = Goods.query.filter_by(product_number=buy_item_product_number).first()
        if bool_value is True:
            bought_item = Goods.query.filter_by(product_number=buy_item_product_number).first()

            flash(f"You have bought {bought_item.name} for {bought_item.price} NOK")
        else:
            flash(f"You don't have enough money to purchase {bought_item.name} NOK")

        return redirect(url_for('main.store_page'))
    if buy_form.errors != {}:  # This happens if the users do somthing wrong when creating a user
        for err_message in buy_form.errors.values():
            flash(f"Error creating store: {err_message}")

    if request.method == "GET":
        # TODO: Make these to a function. And make more filters, for the user to filter what they want to see.
        # TODO: Users that don't have a profile can't buy or auction, so if they try, they get a message to log in.
        items = db.session.query(Goods, Store).filter(and_(Store.id == Goods.store_owner, Goods.goods_type == 0)).all()

        return render_template("store.html", items=items, buy_form=buy_form)


@bp.route("/auction", methods=["POST", "GET"])
def auction_page():
    auction_form = AuctionGoodsForm()
    accept_form = AcceptAuctionForm()

    if request.method == "POST":

        bid_item_product_number = request.form.get('bid_item')
        # current_price = request.form.get('current_price')
        bid_from_store = request.form.get('store_owner1')
        user_id = current_user.id

        item_bidded_on = Goods.query.filter_by(name=bid_item_product_number).first()
        store_bidding_from = User.query.filter_by(id=bid_from_store).first()
        if (item_bidded_on is not None) and (store_bidding_from is not None):
            item_id = item_bidded_on.id
            item_name = item_bidded_on.name
            user_id = current_user.id
            user_name = current_user.username
            store_user_id = store_bidding_from.id
            offer = auction_form.offer.data
            bool_value = bidding_on_product(bid_item_product_number, bid_from_store, offer, item_id, item_name, user_id, user_name, store_user_id)

            if bool_value is True:
                flash(f"You have bid on {item_name} for {offer} NOK")
            else:
                flash(f"You have to bid more than that {offer} NOK, at least 10 more NOK than current price")

        accept_item = request.form.get('accepting_item')
        accept_from_user = request.form.get('accepting_user')

        accepting_bidding_offer(accept_item, accept_from_user, user_id)

        return redirect(url_for('main.auction_page'))

    if auction_form.errors != {}:  # This happens if the users do somthing wrong when creating a user
        for err_message in auction_form.errors.values():
            flash(f"Error bidding on product: {err_message}")

    if accept_form.errors != {}:  # This happens if the users do somthing wrong when creating a user
        for err_message in auction_form.errors.values():
            flash(f"Error accepting offer: {err_message}")

    if request.method == "GET":
        # items = db.session.query(Goods, Store).join(Store).all()
        # TODO: Make these to a function. And make more filters, for the user to filter what they want to see.
        # TODO: Users that don't have a profile can't buy or auction, so if they try, they get a message to log in.
        items = db.session.query(Goods, Store).filter(and_(Store.id == Goods.store_owner, Goods.goods_type == 1)).all()
        try:
            current_user_id = current_user.id
            bidding_items = show_current_highest_bidding_offer_in_store(current_user_id)
        except AttributeError:
            bidding_items = []

        return render_template("auction.html", items=items, auction_form=auction_form, bidding_items=bidding_items,
                               accept_form=accept_form)


# Kan nok slettes
@bp.route('/users', methods=['GET', 'POST'])
def show_users():
    db_users = show_users_from_db()
    return render_template('users.html', db_users=db_users)


@bp.route('/admin_panel', methods=['GET', 'POST'])
def display_admin_panel():
    buy_form = BuyGoodsForm()
    db_users = show_users_from_db()
    auction_form = AuctionGoodsForm()
    items = db.session.query(Goods, Store).filter(and_(Store.id == Goods.store_owner, Goods.goods_type == 0)).all()
    auction_items = db.session.query(Goods, Store).filter(
        and_(Store.id == Goods.store_owner, Goods.goods_type == 1)).all()
    return render_template('adminPanel.html', db_users=db_users, items=items, auction_items=auction_items,
                           buy_form=buy_form, auction_form=auction_form)


@bp.route('/store_panel', methods=['GET', 'POST'])
def display_store_panel():
    buy_form = BuyGoodsForm()
    auction_form = AuctionGoodsForm()
    items = db.session.query(Goods, Store).filter(and_(Store.id == Goods.store_owner, Goods.goods_type == 0)).all()
    auction_items = db.session.query(Goods, Store).filter(
        and_(Store.id == Goods.store_owner, Goods.goods_type == 1)).all()
    return render_template('storePanel.html', items=items, auction_items=auction_items,
                           buy_form=buy_form, auction_form=auction_form)


@bp.route('/delete_user/<int:id>')
def delete_user(id):
    delete_user_from_platform(id)
    return render_template('index.html')


@bp.route('/delete_goods/<int:id>')
def delete_goods(id):
    delete_goods_from_store(id)
    return render_template('index.html')
