from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/mybooks')
def my_books():
    return render_template("mybooks.html")

@app.route('/authors')
def authors():
    return render_template("authors.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

