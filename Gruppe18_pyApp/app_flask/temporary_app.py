from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterUserForm, FormGoods
import os.path

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file_users = "sqlite:///{}".format(
    os.path.join(project_dir, "users_v2.db"))  # Cowboy løsning # appDB-db should be here
database_file_goods = "sqlite:///{}".format(os.path.join(project_dir, "goods.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file_users
app.config["SQLALCHEMY_BINDS"] = {'goods': database_file_goods}  # Binds to be able to have multiple databases
app.config['SECRET_KEY'] = 'nice'
db = SQLAlchemy(app)


# Det blir sirkulær import hvis denne ligger i en egen fil.
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=25), nullable=False, unique=True)
    email = db.Column(db.String(length=60), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name


class Goods(db.Model):
    __bind_key__ = 'goods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(70), unique=True, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Goods %r>' % self.name


# --- Manually adding some data to the table, done once so the program can run ---
# Can maybe be fixed if something else return if a table is empty
# db.create_all()
# sofa = Goods(name='digg sofa', description='deilig og lite brukt', price=69)
# db.session.add(sofa)
# db.session.commit()

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


app.run(port=5000)  # Had to add this to get a local server
