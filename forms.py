from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, TextAreaField,RadioField, IntegerField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submitbutton = SubmitField("Login")

class ReveiwForm(FlaskForm):
    text = TextAreaField("Review", validators=[DataRequired()])
    rating = RadioField('Rating', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    submitbutton = SubmitField("Submit")

class BookForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author_name = StringField("Author's name", validators=[DataRequired()])
    author_surname = StringField("Author's surname", validators=[DataRequired()])
    genre = StringField("Genre", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    year = IntegerField("Year Published", validators=[DataRequired()])
    submitbutton = SubmitField("Add Book")


class SignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    email = EmailField("E-mail", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat password", validators=[DataRequired(), EqualTo('password')])
    submitbutton = SubmitField("Sign-up")