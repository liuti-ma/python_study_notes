import os
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired
import requests
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), '.env')
load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
# initialize the app with the extension
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    # new_movie = Movie(
    #     title="Phone Booth",
    #     year=2002,
    #     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    #     rating=7.3,
    #     ranking=10,
    #     review="My favourite character was the caller.",
    #     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
    # )
    # db.session.add(new_movie)
    # db.session.commit()
    # second_movie = Movie(
    #     title="Avatar The Way of Water",
    #     year=2022,
    #     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    #     rating=7.3,
    #     ranking=9,
    #     review="I liked the water.",
    #     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
    # )
    # db.session.add(second_movie)
    # db.session.commit()
    movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars()
    all_movies = movies.all()  # convert ScalarResult to Python List
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)

class MovieForm(FlaskForm):
    rating = StringField(u'Your rating out of 10 eg: 9.5 ', validators=[DataRequired()])
    review = StringField(u'Your Review ', validators=[DataRequired()])
    submit = SubmitField('Update')

class AddMovieForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')
@app.route("/update/<int:id>",methods=['GET', 'POST'])
def update(id):
    movie = db.get_or_404(Movie, id)
    form = MovieForm(obj=movie)
    if form.validate_on_submit():
        form.populate_obj(movie)  #
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit.html", form=form)

@app.route("/delete")
def delete():
    id = request.args.get("id")
    movie = db.get_or_404(Movie, id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/add",methods=['GET', 'POST'])
def add():
    form = AddMovieForm()

    if form.validate_on_submit():
         title=form.title.data
         print(title)
         url = f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=true&language=en-US&page=1"
         headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}"
         }
         response = requests.get(url, headers=headers, verify=False)
         data = response.json()
         print(data)
         return render_template('select.html', movies=data["results"])
    return render_template('add.html', form=form)

@app.route("/find",methods=['GET', 'POST'])
def find():
    movie_id = request.args.get("id")
    print(id)
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(url, headers=headers, verify=False)
    data = response.json()
    new_movie = Movie(
        title=data["title"],
        # The data in release_date includes month and day, we will want to get rid of.
        year=data["release_date"].split("-")[0],
        img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
        description=data["overview"]
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("update", id=new_movie.id))
@app.route("/select",methods=['GET', 'POST'])
def select():
    return render_template('select.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
