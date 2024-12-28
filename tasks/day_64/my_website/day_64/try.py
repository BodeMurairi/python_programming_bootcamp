from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os

# Load environment variables from a .env file
load_dotenv()

TMBD_API_KEY = os.getenv("TMBD_API_KEY")
SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
movie_title = None
films = None

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies_database.db'
Bootstrap5(app)
db.init_app(app)

# CREATE DB
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'

# Create the 'instance' folder if it doesn't exist
import os
if not os.path.exists('instance'):
    os.makedirs('instance')

# CREATE TABLE
with app.app_context():
    db.create_all()

class MovieForm(FlaskForm):
    rating = FloatField('Rating', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    submit = SubmitField('Update Movie')

class AddMovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')

@app.route("/")
def home():
    result = db.session.execute(db.select(Movies))
    all_movies = result.scalars().all()

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i

    return render_template("index.html", movies=all_movies)

@app.route("/index/add", methods=["GET", "POST"])
def add_movie():
    form = AddMovieForm()
    global movie_title, TMBD_API_PARAMS
    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(url=SEARCH_URL, params={"api_key": TMBD_API_KEY, "query": movie_title})
        response.raise_for_status()
        film_data = response.json()
        global films
        films = film_data["results"]
        return redirect(url_for("select"))
    return render_template("add.html", form=form)

@app.route("/index/find_movie/<string:movie_name>")  # Add closing quotation mark
def movie_info(movie_name):
    global TMBD_API_KEY, TMBD_API_PARAMS, MOVIE_DB_INFO_URL, MOVIE_DB_IMAGE_URL
    TMBD_API_PARAMS = {
        "api_key": TMBD_API_KEY,
        "query": movie_name
    }
    response = requests.get(url=SEARCH_URL, params=TMBD_API_PARAMS)
    movie_data = response.json()["results"][0]

    existing_movie = Movies.query.filter_by(title=movie_data["original_title"]).first()
    if existing_movie:
        flash(f"Movie '{movie_name}' already exists in your database!", "warning")
        return redirect(url_for("home"))

    try:
        added_movie = Movies(
            title=movie_data["original_title"],
            year=movie_data["release_date"][:4],
            description=movie_data["overview"],
            rating=0.0,  # Default rating
            ranking=0,  # Default ranking
            review="",  # Default review
            img_url=MOVIE_DB_IMAGE_URL + movie_data["poster_path"],
        )
        db.session.add(added_movie)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while adding the movie: {e}", "danger")
        return redirect(url_for("home"))

    return redirect(url_for("updates", id=added_movie.id))

@app.route("/updates", methods=["GET", "POST"])
def updates():
    form = MovieForm()
    movie_id = request.args.get("id")
    movie = db.session.get(Movies, movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form, movie=movie)

@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    movie = db.session.get(Movies, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/index/select")
def select():
    return render_template("select.html", all_movies=films)

if __name__ == '__main__':
    app.run(debug=True)