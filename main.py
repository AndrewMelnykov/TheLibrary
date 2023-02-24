from flask import Flask, render_template, url_for, request, flash
from forms import LoginForm, SignupForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_secret_key'


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
        username = login_form.username.data
        login_form.username.data = ''
        flash("You've logged in successfully!")

    return render_template("login.html", login_form = login_form, username=username)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    return render_template("signup.html", signup_form=signup_form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

