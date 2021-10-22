import bcrypt as bcrypt
import flask
from flask import render_template
from flask_login import current_user, login_required, login_user, logout_user
from app_flask import app, db
from app_flask.forms import RegisterUserForm, LoginForm, FormGoods
from app_flask.models import User, Goods
from app_flask.models import is_the_user_authenticated


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
                                   password_hash=form.password1.data)
        db.session.add(creating_user_in_db)
        db.session.commit()
    return render_template("registerUser.html", form=form)


@app.route('/goods', methods=['GET', 'POST'])
def add_goods():
    form = FormGoods()
    if form.validate_on_submit():
        new_goods = Goods(name=form.name.data, description=form.description.data, price=form.price.data)
        # Clear the form ''
        form.name.data = ''
        form.description.data = ''
        form.price.data = ''
        db.session.add(new_goods)
        db.session.commit()

    db_goods = Goods.query.order_by(Goods.name)
    return render_template('addGoods.html', form=form, db_goods=db_goods)


@app.route('/store', methods=['GET', 'POST'])
def show_goods():
    db_goods = Goods.query.order_by(Goods.name)
    return render_template('showGoods.html', db_goods=db_goods)


@app.route('/delete/<int:id>')
def delete_goods(id):
    goods_to_delete = Goods.query.filter_by(id=id).first()

    form = FormGoods()

    db.session.delete(goods_to_delete)
    db.session.commit()

    db_goods = Goods.query.order_by(Goods.name)
    return render_template('showGoods.html', form=form, db_goods=db_goods)

# log in
@app.route("/login", methods=["GET", "POST"])
def login():
    # import bcrypt , store info as bycrypt install
    # create func
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            # se if it store correct password
            if bcrypt.checkpw(user.password_hash, form.password1.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                flask.flash('logged in successfully')

                next = flask.request.args.get('next')
                # se if it works (no entry), if the user is not in db otherwise change and add parameter in model.py
                if not is_the_user_authenticated(next):
                    return flask.abort(400)
                return flask.redirect(next or flask.url_for('index'))
    return render_template('login.html', form=form)


# log out
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    # not finish, don't know why is not log out not working
    logout_user = ()
    # Todo: redirect to homepage or login
    return render_template("html")

# Todo: run this on app.py or the new temporary ( can someone do it )
