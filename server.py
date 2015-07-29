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
    return redirect('/user-page')


@app.route('/button')
def logout():
    """This form will logout users."""
    
    del session["logged_in"]
    flash("See you later! ;)")
    return redirect('/')

@app.route('/user-page/<int:user_id>')
def user_page(user_id):

    user_id = session.get('email')

    render_template("user_page.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()