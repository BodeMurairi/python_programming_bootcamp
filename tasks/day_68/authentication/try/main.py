import werkzeug
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os
from dotenv import load_dotenv

app = Flask(__name__)

class BaseModel(DeclarativeBase):
    pass

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = os.urandom(24) # Generate a secret key
db = SQLAlchemy(model_class=BaseModel)
db.init_app(app)

# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# Create the table inside my database
class User(UserMixin, db.Model):
    '''This class represents all the user in the database'''
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()



#.....................................Web Application..............................

@app.route('/')
def home():
    ''' This function renders the home page '''
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    ''' This function renders the register page '''
    if request.method == 'POST':
        new_user = User(first_name = request.form['First Name'],
                        last_name = request.form['Last Name'],
                        username = request.form['Username'],
                        email = request.form['Email'],
                        password= generate_password_hash(request.form["Password"], method='scrypt', salt_length=16)
                        )
        db.session.add(new_user)
        db.session.commit()

        flash("User saved successfully")

        # Login user after authentification
        login_user(new_user)

        return redirect(url_for('secret'))

    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' This function renders the login page '''
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user:
            # Check the hashed password
            if check_password_hash(user.password, request.form['Password']):
                login_user(user)
                flash("Logged in successfully")
                print("User logged in successfully")
                return redirect(url_for('secret'))
            else:
                flash("Login failed. Password does not match. Please try again.")
                print("Login failed: Password does not match")
                return redirect(url_for('login'))
        else:
            flash("User not found")
            print("Login failed: User not found")
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for('home'))


@app.route('/secret', methods=['GET', 'POST'])
@login_required
def secret():
    print(f"Accessing secret.html as user: {current_user.username}")
    return render_template("secret.html", user=current_user.username)

if __name__ == '__main__':
    app.run(debug=True, port=5001)