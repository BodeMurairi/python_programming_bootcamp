from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from wtforms import Form, StringField, EmailField, PasswordField, validators
from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, URL, Email, EqualTo
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CREATE DATABASE


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
Bootstrap5(app)
# CREATE TABLE IN DB


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()

class UserRegisterForm (FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register')
def register():
    register_form = UserRegisterForm()
    '''
    This function renders the register.html page.
    Then retrieve data from the form and store them into the database.
    '''
    register_form = UserRegisterForm()
    if register_form.validate_on_submit():
        username = register_form.name.data
        user_email_address = register_form.email.data
        if register_form.password.data == register_form.confirm_password.data:
            user_password = register_form.password.data
            hashed_password = generate_password_hash(user_password, method='sha256')
        else:
            flash("Passwords do not match")
            return redirect(url_for('register'))

        new_user = User(
            name = username,
            password = user_password,
            email = user_email_address
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully!")
        return redirect(url_for('secrets'))
    return render_template("register.html", form= register_form)


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    pass


if __name__ == "__main__":
    app.run(debug=True)
