from flask import Flask, render_template, url_for
from forms import LoginForm


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
    login_form = LoginForm()
    return render_template("login.html", login_form = login_form)

@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

