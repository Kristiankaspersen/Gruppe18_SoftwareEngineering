from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_user, logout_user, current_user
from app_flask import db
from app_flask.auth import bp
from app_flask.auth.forms import RegisterUserForm, LoginFormUser, LoginFormStore, RegisterStoreForm, \
    LoginFormAdmin, LoginForm
from app_flask.models import User, Goods, Store, Bidding
from sqlalchemy.sql.expression import func
from app_flask.auth.use_cases import create_user_and_store_in_db, create_store_in_db


@bp.route("/register", methods=['GET', 'POST'])
def register_user_page():
    form = RegisterUserForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():

        username = form.username.data
        email = form.email.data
        password = form.password1.data
        profile_type = form.profile_type.data

        create_user_and_store_in_db(username, email, password, profile_type)

        flash(f"You have made a user with username: {username}")
        return redirect(url_for('auth.login_page'))
    if form.errors != {}:  # This happens if the users do somthing wrong when creating a user
        for err_message in form.errors.values():
            flash(f"Error creating user: {err_message}", category='danger')
    return render_template("registerUser.html", form=form)

@bp.route("/registerStore", methods=["GET", "POST"])
def register_store():
    form = RegisterStoreForm(request.form, csrf_enabled=False)

    if form.validate_on_submit():

        store_name = form.store_name.data
        street_address = form.street_address.data
        street_number = form.street_number.data
        postal_code = form.postal_code.data
        province = form.province.data
        store_email = form.store_email.data
        store_phone = form.store_phone.data
        owner = current_user.id

        if not(isinstance(postal_code, int) or isinstance(postal_code, int)):
            error_message = f"phone number and postal code needs to be a number, try again"
            flash(error_message, category='danger')
            return redirect(url_for('auth.register_store'))

        store_name_exists = Store.query.filter_by(store_name=store_name).first()

        if store_name_exists is not None:
            flash(f"Store name {store_name} is already in use! try a different store name", category='danger')
            return redirect(url_for('auth.register_store'))


        create_store_in_db(store_name, street_address, street_number, postal_code, province, store_email, store_phone, owner)

        flash(f"You have made a new store with name {store_name}")
        return redirect(url_for('main.store_page'))
    if form.errors != {}:  # This happens if the users do somthing wrong when creating a user
        for err_message in form.errors.values():
            flash(f"Error creating store: {err_message}")

    return render_template("registerStore.html", form=form)

@bp.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm(request.form, csrf_enabled=False)
    form_user = LoginFormUser(request.form, csrf_enabled=False)
    form_store = LoginFormStore(request.form, csrf_enabled=False)
    # Admin
    form_admin = LoginFormAdmin()
    if form_user.validate_on_submit():

        real_user_attempted = None
        user_attempted = None

        if request.form.get('Geir') is not None:
            user_attempted = User.query.filter_by(username="Geir").first()
        elif request.form.get('Tor') is not None:
            user_attempted = User.query.filter_by(username="Tor").first()
        elif request.form.get('Admin') is not None:
            user_attempted = User.query.filter_by(username="Admin").first()
        else:
            real_user_attempted = User.query.filter_by(username=form.username.data).first()


        if (user_attempted is not None) and user_attempted.checking_password_with_hash(
                password_attempted="12345678"
        ):
            login_user(user_attempted)
            flash(f"You are logged in as: {user_attempted.username}")
            # Changed store_page to home_page
            return redirect(url_for("main.home_page"))
        elif (real_user_attempted is not None) and real_user_attempted.checking_password_with_hash(
                password_attempted=form.password.data
            ):
            login_user(real_user_attempted)
            flash(f"You are logged in as: {real_user_attempted.username}")
            return redirect(url_for("main.store_page"))
        else:
            flash("Wrong password, or username")

    return render_template("login.html", form=form, form_user=form_user, form_store=form_store, form_admin=form_admin)

@bp.route("/logout")
def logout_page():
    logout_user()
    flash("You have logged out")
    return redirect(url_for('main.home_page'))