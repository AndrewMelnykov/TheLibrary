from main import app
from models.db_models import Users, Review, Book, Library
from flask import Blueprint
from flask_login import current_user, login_required

api_routes = Blueprint("api_routes", __name__)

@api_routes.route('/api/get/allbooks')
def api_books():

    books = Book.query.order_by(Book.id).all()
    result_array = {}

    for book in books:
            result_array[book.id] = {
                      'title' : book.title,
                      'author': book.author_name+' '+book.author_surname,
                      "year": book.year,
                      'genre': book.genre,
                      'description': book.description}

    return result_array

@app.route('/api/get/mybooks')
@login_required
def api_my_books():

    mylibrary=Library.query.filter_by(user_id=current_user.id).all()
    books = Book.query.order_by(Book.id).all()
    result_array = {}
    i=0
    for library in mylibrary:
        result_array[library.book_id] = {
                  'title' : Book.query.filter_by(id=library.book_id).first().title,
                   'author': Book.query.filter_by(id=library.book_id).first().author_name+' '+Book.query.filter_by(id=library.book_id).first().author_surname,
                   "year": Book.query.filter_by(id=library.book_id).first().year,
                   'genre': Book.query.filter_by(id=library.book_id).first().genre,
                   'description': Book.query.filter_by(id=library.book_id).first().description}
        i+=1

    return result_array
