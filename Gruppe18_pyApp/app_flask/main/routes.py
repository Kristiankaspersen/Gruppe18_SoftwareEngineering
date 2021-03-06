from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from app_flask import db
from app_flask.main import bp
from app_flask.main.forms import AddGoodsToMarket, AddGoodsToAuction, BuyGoodsForm, AcceptAuctionForm, AuctionGoodsForm
from app_flask.main.use_cases import buying_product, show_current_highest_bidding_offer_in_store, show_users_from_db, \
    delete_user_from_platform, delete_goods_from_store, add_market_item, add_auction_item, bidding_on_product, \
    accepting_bidding_offer
from app_flask.models import User, Goods, Store, Bidding
from sqlalchemy.sql.expression import and_


@bp.route("/")
@bp.route("/home")
def home_page():
    return render_template("index.html")


@bp.route('/goods', methods=['GET', 'POST'])
def add_goods():
    form_auction = AddGoodsToAuction(request.form, csrf_enabled=False)
    form_market = AddGoodsToMarket(request.form, csrf_enabled=False)

    if request.method == "POST":

        name = form_auction.name.data
        description = form_auction.description.data
        price = form_auction.price.data
        product_number = form_auction.product_number.data
        store_user_owner = current_user.id

        if not(isinstance(price, int)) or not(isinstance(product_number, int)):
            error_message = f"Product number and price needs to be a number, try again"
            flash(error_message)
            return redirect(url_for('main.add_goods'))
        if request.form.get('auctionItem') is not None:
            add_auction_item(name, description, price, product_number, store_user_owner)
            flash("(name of item) added to the auction market")
        else:
            add_market_item(name, description, price, product_number, store_user_owner)
            flash("(name of item) added to the store market")
        return redirect(url_for('main.add_goods'))

    if request.method == "GET":
        return render_template('addGoods.html', form_auction=form_auction, form_market=form_market)


@bp.route('/owned_goods', methods=['GET', 'POST'])
def show_owned_goods():
    db_goods = db.session.query(User, Goods).filter(User.id == Goods.user_owner).all()
    return render_template('showGoods.html', db_goods=db_goods)


@bp.route("/store", methods=["POST", "GET"])
def store_page():
    buy_form = BuyGoodsForm(request.form, csrf_enabled=False)

    if request.method == "POST":
        buy_item_product_number = request.form.get('bought_item')
        bought_from_store = request.form.get('store_owner')

        bool_value = buying_product(buy_item_product_number, bought_from_store, current_user.id)
        bought_item = Goods.query.filter_by(product_number=buy_item_product_number).first()
        if bool_value is True:
            bought_item = Goods.query.filter_by(product_number=buy_item_product_number).first()

            flash(f"You have bought {bought_item.name} for {bought_item.price} NOK")
        else:
            flash(f"You do not have enough money to purchase {bought_item.name}")

        return redirect(url_for('main.store_page'))
    if buy_form.errors != {}:
        for err_message in buy_form.errors.values():
            flash(f"Error creating store: {err_message}")

    if request.method == "GET":

        items = db.session.query(Goods, Store).filter(and_(Store.id == Goods.store_owner, Goods.goods_type == 0)).all()

        return render_template("store.html", items=items, buy_form=buy_form)


@bp.route("/auction", methods=["POST", "GET"])
def auction_page():
    auction_form = AuctionGoodsForm(request.form, csrf_enabled=False)
    accept_form = AcceptAuctionForm(request.form, csrf_enabled=False)

    if request.method == "POST":

        if not(isinstance(auction_form.offer.data, int)) and (request.form.get('bid_item') is not None):
            error_message = f"Your bid needs to be a number, try again"
            flash(error_message)
            return redirect(url_for('main.auction_page'))

        bid_item_product_number = request.form.get('bid_item')
        bid_from_store = request.form.get('store_owner1')
        user_id = current_user.id

        item_bidded_on = Goods.query.filter_by(product_number=bid_item_product_number).first()
        store_bidding_from = User.query.filter_by(id=bid_from_store).first()
        if (item_bidded_on is not None) and (store_bidding_from is not None):
            item_id = item_bidded_on.id
            item_name = item_bidded_on.name
            user_id = current_user.id
            user_name = current_user.username
            store_user_id = store_bidding_from.id
            offer = auction_form.offer.data


            bool_value_bidding_on_product = bidding_on_product(bid_item_product_number, offer, item_id, item_name, user_id, user_name, store_user_id)

            if bool_value_bidding_on_product is True:
                flash(f"You have bid on {item_name} for {offer} NOK")
            else:
                flash(f"You have to bid more than that {offer} NOK, at least 10 more NOK than current price")
        else:
            if request.form.get('accepting_item') is None:
                flash("Ups, something went wrong with the bid, either the store don't exist, or the item is no longer there")


        accept_item_id = request.form.get('accepting_item')
        accept_from_user_id = request.form.get('accepting_user')

        bool_value_accepting_offer = accepting_bidding_offer(accept_item_id, accept_from_user_id, user_id)
        accepting_item = Goods.query.filter_by(id=accept_item_id).first()
        user_bidding_on_item = User.query.filter_by(id=accept_from_user_id).first()
        if request.form.get('accepting_user') is not None:
            if bool_value_accepting_offer is True:
                flash(f"You have accepted offer on {accepting_item.name} for {accepting_item.price} NOK")
            else:
                flash(f"{user_bidding_on_item.username} do not have enough money to purchase {accepting_item.name}")

        return redirect(url_for('main.auction_page'))

    if request.method == "GET":
        items = db.session.query(Goods, Store).filter(and_(Store.id == Goods.store_owner, Goods.goods_type == 1)).all()
        try:
            current_user_id = current_user.id
            bidding_items = show_current_highest_bidding_offer_in_store(current_user_id)
            print(isinstance(bidding_items, Bidding))
        except AttributeError:
            bidding_items = []

        return render_template("auction.html", items=items, auction_form=auction_form, bidding_items=bidding_items,
                               accept_form=accept_form)

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
