from flask import Flask, render_template, flash
from forms import LoginForm, SignupForm
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'dev_secret_key'

from models.db_models import Users

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/mybooks')
def my_books():
    return render_template("mybooks.html")

@app.route('/authors')
def authors():
    return render_template("authors.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = None
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = Users.query.filter_by(email=login_form.username.data).first()
        if user is None:
            user = Users(username=login_form.username.data, email=login_form.email.data)
            db.session.add(user)
            db.session.commit()
            username = login_form.username.data
            login_form.email.data = ""
            login_form.username.data = ""
            login_form.password.data = ""
            flash("You've logged in successfully!")
    all_users = Users.query.order_by(Users.date_added)
    return render_template("login.html", login_form = login_form, username=username, all_users=all_users)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    return render_template("signup.html", signup_form=signup_form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

