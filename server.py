"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/user-list')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/login-form')
def login():
    """This will show you the login form."""

    return render_template("login_form.html")

@app.route('/login', methods=['POST'])
def submit_login():
    """This form will submit login information & return you to the homepage."""
    
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Type it in again, foo!")
        return redirect("/login-form")

    if user.password != password:
        flash("Stop trying to break in!")
        return redirect("/login-form")


    session["logged_in"] = user.email
    flash("You have been successfully logged in!")
    return redirect('/user-page/%d' % user.user_id)


@app.route('/button')
def logout():
    """This form will logout users."""
    
    del session["logged_in"]
    flash("See you later! ;)")
    return redirect('/')

@app.route('/user-page/<int:user_id>')
def user_page(user_id):
    """ the user's personal webpage to remind us who they are, 
    cus sometimes we forget"""

    current_user = User.query.filter_by(user_id=user_id).first()
    email = current_user.email
    zipcode = current_user.zipcode
    age = current_user.age
    thing = current_user.user_id

    movie_list = db.session.query(Rating.score, 
        Movie.title).join(Movie).filter(Rating.user_id==thing).all()



    return render_template("user_page.html", email=email, user_id=user_id,
        zipcode=zipcode, age=age, movie_list=movie_list)

@app.route('/movies')
def full_list_of_movies():
    """this returns the full list of movies in the database. Includes link
    to individual movie page."""

    movie_list = Movie.query.order_by(Movie.title).all()
    return render_template('movie_list.html', movie_list=movie_list)

@app.route('/movie-page/<int:movie_id>')
def movie_page(movie_id):
    """Contains all of the information about a particular movie in our
    database."""

    current_movie = Movie.query.filter_by(movie_id=movie_id).first()
    title = current_movie.title
    released = current_movie.released_at
    url = current_movie.imdb_url
    thing = current_movie.movie_id

    movie_rating = db.session.query(Rating.score).join(Movie).filter(
        Movie.movie_id==thing).all()

    return render_template('movie_page.html', current_movie=current_movie, 
        title=title, released=released, url=url, movie_rating=movie_rating)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()