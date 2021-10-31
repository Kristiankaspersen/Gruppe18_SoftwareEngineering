
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user
from app_flask import app, db
from app_flask.forms import RegisterUserForm, LoginForm, FormGoods
from app_flask.models import User, Goods


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

@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user_attempted = User.query.filter_by(username="Seller").first() #If you want to change user, write Buyer
        if (user_attempted is not None) and user_attempted.checking_password_with_hash(
                password_attempted="12345678"
        ):
            login_user(user_attempted)
            flash(f"You are logged in as: {user_attempted.username}")
            return redirect(url_for("show_goods"))
        else:
            flash("Wrong password, or username")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have logged out")
    return redirect(url_for('home_page'))


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
        flash("Item added to the store")

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




