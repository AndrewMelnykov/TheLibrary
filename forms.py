from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("username")
    password = PasswordField("password")
    submitbutton = SubmitField("Login")


class SignupForm(FlaskForm):
    name = StringField("name")
    surname = StringField("surname")
    username = StringField("username")
    password = PasswordField("password")
    submitbutton = SubmitField("Sign-up")