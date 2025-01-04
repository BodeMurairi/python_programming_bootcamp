import werkzeug
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os
from dotenv import load_dotenv


# Creating Flask web application and setting the secret key
app = Flask(__name__)


# CREATE DATABASE


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = os.urandom(24) # Secret key
db = SQLAlchemy(model_class=Base)
db.init_app(app)
# CREATE TABLE IN DB

# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


#....................................My Web Application..........................................
@app.route('/')
def home():
    return render_template("index.html", logged_in= current_user.is_authenticated)


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    This function renders the register.html page.
    Then retrieve data from the form and store them into the database.
    '''
    if request.method == 'POST' :
        new_user = User(
            name = request.form['name'],
            password = werkzeug.security.generate_password_hash(user_password,
                                                                method='scrypt',
                                                                salt_length=16),
            email = request.form['email']
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully!")
        return redirect(url_for('login'))
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    This function renders the login.html authentication function
    '''
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            if check_password_hash(user.password, request.form['password']):
                # if check successful, login user
                flash("Logged in successfully!")
                login_user(user)
                return redirect(url_for('secrets'))
            else:
                flash("Incorrect password! Login failed. Try again.")
                return redirect(url_for('login'))
        else:
            flash("Incorrect email! Login failed. Try again.")
            return redirect(url_for('login'))

    return render_template("login.html")

# Only logged-in users can access the route
@app.route('/secrets')
@login_required
def secrets():
    '''
    This function renders the secrets.html page.
    '''
    return render_template("secrets.html", user=current_user.name)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download', methods=['POST'])
@login_required
def download():
    return send_from_directory('static', 'files/cheat_sheet.pdf', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
