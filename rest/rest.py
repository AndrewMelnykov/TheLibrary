from main import app, db
from models.db_models import Users, Review, Book, Library
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

api_routes = Blueprint("api_routes", __name__)

#endpoint for getting all books
@api_routes.route('/api/get/allbooks', methods=['GET'])
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

    return jsonify(result_array)

#endpoint for getting user's books from db
@api_routes.route('/api/get/mybooks', methods=['GET'])
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

    return jsonify(result_array)

#endpoint for deleting the book from db
@api_routes.route('/api/delete/book/<id>', methods=["GET","DELETE"])
@login_required
def api_delete_book(id):

    book = Book.query.get_or_404(id)

    if book:
        db.session.delete(book)
        db.session.commit()

    return "Book deleted!"

#endpoint for updating the book info
@api_routes.route('/api/edit/book/<id>', methods=["GET","PUT"])
def api_edit_book(id):

    book = Book.query.get_or_404(id)
    if book:
        author_name = request.json['author_name']
        author_surname = request.json['author_surname']

        book.author_name = author_name
        book.author_surname = author_surname

        db.session.commit()

    return "Success"
