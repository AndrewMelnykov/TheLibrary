from flask import Flask, render_template, flash, redirect, url_for, jsonify
from forms import LoginForm, SignupForm, ReveiwForm, BookForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from flask_migrate import Migrate

#app config logic
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'dev_secret_key'

from models.db_models import Users, Review, Book, Library
from rest.rest import api_routes

app.register_blueprint(api_routes)
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

@app.route('/addbook', methods=['GET', 'POST'])
@login_required
def addbook():
    book_form = BookForm()
    if book_form.validate_on_submit():
        book = Book(title=book_form.title.data, author_name=book_form.author_name.data, author_surname=book_form.author_surname.data, year=book_form.year.data, genre=book_form.genre.data, description=book_form.description.data)
        db.session.add(book)
        db.session.commit()
    books = Book.query.all()
    return render_template("add_book.html", books=books, book_form=book_form)


@app.route('/home')
def home():
    books = Book.query.order_by(Book.id)
    return render_template("home.html", books=books)

@app.route('/delete/review/<int:id>', methods=["GET", "POST"])
@login_required
def delete_review(id):
    review = Review.query.get_or_404(id)
    if current_user.id == review.reviewer_id:
        if review:
            db.session.delete(review)
            db.session.commit()
        else:
            flash("something went with the review, try again!")
    else: flash("You have no permission to delete this review!")
    return redirect(url_for("book", id=review.book_id))



@app.route('/edit/review/<int:id>', methods=["GET", "POST"])
@login_required
def edit_review(id):
    review = Review.query.get_or_404(id)
    review_form = ReveiwForm()

    if review_form.validate_on_submit():

        review.text = review_form.text.data
        review.rating = review_form.rating.data
        db.session.commit()
        flash("Success!")
        return redirect(url_for('book', id=review.book_id))
    review_form.rating.data = review.rating
    review_form.text.data = review.text
    return render_template("review_edit.html", review_form=review_form, review=review)


@app.route('/books/<id>', methods=["GET", "POST"])
@login_required
def book(id):
    book = Book.query.get_or_404(id)
    review_form = ReveiwForm()
    if review_form.validate_on_submit():
        review = Review(text = review_form.text.data, rating = review_form.rating.data, reviewer_id=current_user.id, book_id=book.id)
        review_form.text.data = None
        review_form.rating.data = None
        db.session.add(review)
        db.session.commit()
    reviews = Review.query.filter_by(book_id=book.id).all()
    return render_template("book.html", book=book, reviews=reviews, review_form=review_form)

@app.route('/book/remove/<id>', methods=['GET', 'POST'])
@login_required
def remove_from_library(id):
    book = Book.query.get_or_404(id)
    library = Library.query.filter_by(book_id=book.id, user_id = current_user.id).first()
    if library:
        db.session.delete(library)
        db.session.commit()
    else:
        flash("something went wrong, try again!")
    return redirect(url_for('my_books'))

@app.route('/book/add/<id>', methods=['GET', 'POST'])
@login_required
def add_to_library(id):
    book = Book.query.get_or_404(id)
    if Library.query.filter_by(book_id=book.id, user_id = current_user.id).all():
       flash("You already have this book in your library!")
    else:
        library = Library(user_id=current_user.id , book_id=book.id)
        db.session.add(library)
        db.session.commit()

    return redirect(url_for('my_books'))

@app.route('/mybooks', methods = ['GET', 'POST'])
@login_required
def my_books():
    all_books = Library.query.filter_by(user_id=current_user.id)
    return render_template("mybooks.html", all_books=all_books)

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

