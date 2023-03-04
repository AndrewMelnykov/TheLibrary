from datetime import datetime
from main import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    surname = db.Column(db.String(100), nullable=False, unique=False)
    username = db.Column(db.String(100), nullable=True, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    #User can have many reviews
    reviews = db.relationship("Review", backref='reviewer')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.name


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=False)
    author_name = db.Column(db.String(100), nullable=False, unique=False)
    author_surname = db.Column(db.String(100), nullable=True, unique=False)
    year = db.Column(db.String(100), nullable=False, unique=False)
    reviews = db.relationship("Review", backref='reviewed_book')
    #readers =


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    #reviews =
    #readers =