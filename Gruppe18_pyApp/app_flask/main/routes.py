from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_user, logout_user, current_user
from app_flask import db
from app_flask.main import bp
from app_flask.main.forms import AddGoodsToMarket,AddGoodsToAuction, BuyGoodsForm, AcceptAuctionForm, AuctionGoodsForm
from app_flask.models import User, Goods, Store, Bidding
from sqlalchemy.sql.expression import func, and_
from app_flask.main.use_cases import add_auction_item, add_goods_item, buying_product, bidding_on_product, accepting_bidding_offer


@bp.route("/")
@bp.route("/home")
def home_page():
    return render_template("index.html")

@bp.route('/goods', methods=['GET', 'POST'])
def add_goods():
    form_auction = AddGoodsToAuction()
    form_market = AddGoodsToMarket()

    if request.method == "POST":
        auction_value = request.form.get('auctionItem')
        name = form_auction.name.data
        description = form_auction.description.data
        price = form_auction.price.data
        product_number = form_auction.product_number.data
        store_owner = current_user.id

        if auction_value == "ItemForAuction":
            add_auction_item(name, description, price, product_number, store_owner)
        else:
            add_goods_item(name, description, price, product_number, store_owner)
        return redirect(url_for('main.add_goods'))

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
        buy_item = request.form.get('bought_item')
        bought_from_store = request.form.get('store_owner')

        buying_product(buy_item, bought_from_store, current_user.id)

        return redirect(url_for('main.store_page'))

    if request.method == "GET":

        #TODO: Make these to a function. And make more filters, for the user to filter what they want to see.
        #TODO: Users that don't have a profile can't buy or auction, so if they try, they get a message to log in.
        items = db.session.query(Goods, Store).filter(and_(Store.id == Goods.store_owner, Goods.goods_type == 0)).all()

        return render_template("store.html", items=items, buy_form=buy_form)

@bp.route("/auction", methods=["POST", "GET"])
def auction_page():
    auction_form = AuctionGoodsForm()
    accept_form = AcceptAuctionForm()

    if request.method == "POST":

        bid_item = request.form.get('bid_item')
        # current_price = request.form.get('current_price')
        bid_from_store = request.form.get('store_owner1')

        item_bidded_on = Goods.query.filter_by(name=bid_item).first()
        store_bidding_from = User.query.filter_by(id=bid_from_store).first()
        if (item_bidded_on is not None) and (store_bidding_from is not None):
            item_id = item_bidded_on.id
            print(item_bidded_on.id)
            item_name = item_bidded_on.name
            user_id = current_user.id
            user_name = current_user.username
            store_user_id = store_bidding_from.id
            offer = auction_form.offer.data
            bidding_on_product(bid_item, bid_from_store, offer, item_id, item_name, user_id, user_name, store_user_id)

        accept_item = request.form.get('accepting_item')
        accept_from_user = request.form.get('accepting_user')

        current_user_id = current_user.id
        accepting_bidding_offer(accept_item, accept_from_user, current_user_id)

        return redirect(url_for('main.auction_page'))

    if request.method == "GET":
        # items = db.session.query(Goods, Store).join(Store).all()
        # TODO: Make these to a function. And make more filters, for the user to filter what they want to see.
        # TODO: Users that don't have a profile can't buy or auction, so if they try, they get a message to log in.
        items = db.session.query(Goods, Store).filter(and_(Store.id == Goods.store_owner, Goods.goods_type == 1)).all()
        try:
            #TODO: make this in to a function.
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

        return render_template("auction.html", items=items, auction_form=auction_form, bidding_items=bidding_items, accept_form=accept_form)


@bp.route('/users', methods=['GET', 'POST'])
def show_users():

    db_users = User.query.filter(User.username.isnot("Admin"))
    return render_template('users.html', db_users=db_users)


@bp.route('/delete/<int:id>')
def delete_user(id):
    #TODO: make a function
    user_to_delete = User.query.filter_by(id=id).first()
    db.session.delete(user_to_delete)
    db.session.commit()
    return render_template('index.html')


@bp.route('/delete/<int:id>')
def delete_goods(id):
    #TODO: make a function
    goods_to_delete = Goods.query.filter_by(id=id).first()
    db.session.delete(goods_to_delete)
    db.session.commit()

    return render_template('index.html')