from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_user, logout_user, current_user
from app_flask import db
from app_flask.auth import bp
from app_flask.auth.forms import RegisterUserForm, LoginFormUser, LoginFormStore, RegisterStoreForm, \
    LoginFormAdmin
from app_flask.models import User, Goods, Store, Bidding
from sqlalchemy.sql.expression import func


@bp.route("/register", methods=['GET', 'POST'])
def register_user_page():
    form = RegisterUserForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        creating_user_in_db = User(username=form.username.data,
                                   email=form.email.data,
                                   password=form.password1.data,
                                   profile_type=form.profile_type.data)
        db.session.add(creating_user_in_db)
        db.session.commit()
        return redirect(url_for('auth.show_owned_goods'))
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
        return redirect(url_for('main.store_page'))

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