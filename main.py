from flask import Flask, render_template, flash, redirect, url_for
from forms import LoginForm, SignupForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager
from flask_migrate import Migrate

#app config logic
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'dev_secret_key'

from models.db_models import Users

#Login logic
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#routes


#create logout page
@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/mybooks')
@login_required
def my_books():
    flash("You've been successfully logged in!")
    return render_template("mybooks.html")

@app.route('/authors')
def authors():
    return render_template("authors.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Users.query.filter_by(email=login_form.email.data).first()
        if user:
            if check_password_hash(user.password_hash, login_form.password.data):
                login_user(user)
                return redirect(url_for("my_books"))
            else: flash("Worng password!")

        else: flash("that user does not exist!")
    all_users = Users.query.order_by(Users.date_added)
    return render_template("login.html", login_form = login_form, all_users=all_users)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        user = Users.query.filter_by(email=signup_form.email.data).first()
        if user is None:
            pw_hash = generate_password_hash(signup_form.password.data)
            user = Users(name = signup_form.name.data, surname=signup_form.surname.data, username = signup_form.username.data, email=signup_form.email.data, password_hash=pw_hash)
            db.session.add(user)
            db.session.commit()
            flash("You've logged in successfully!")
        if signup_form.password.data != signup_form.password2.data:
            flash("Please typ identical passwords!")
        signup_form.name.data = ""
        signup_form.surname.data = ""
        signup_form.username.data = ""
        signup_form.email.data = ""
    all_users = Users.query.order_by(Users.date_added)
    return render_template("signup.html", signup_form=signup_form, all_users = all_users)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

