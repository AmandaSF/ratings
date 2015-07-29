"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions
# Delete this line and put your User/Movie/Ratings model classes here.
class User(db.Model):
    """User of rating website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User user_id=%s email=%s>" % (self.user_id, self.email)

    @classmethod
    def get_by_email_password(cls, email, password):
        """get user information by email for login purposes"""

        User.query.filter_by(email=email).one()
        #from this point we need to create if statements
        #fix server.py to reconcile with new aspects of THIS fuction
        # 


        if not row:
            return None
        user = User(*row)

        return user

class Movie(db.Model):
    """Movie info in rating website."""

    __tablename__= "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(64))
    released_at = db.Column(db.DateTime)
    imdb_url = db.Column(db.String(200))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<Movie movie_id=%s title=%s released_at=%d>" % (
            self.movie_id, self.title, self.released_at)

class Rating(db.Model):
    """Rating information in ratings website."""

    __tablename__= "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer)

    #Define relationship to user
    user = db.relationship("User", 
                            backref=db.backref("ratings", order_by=rating_id))

    #Define relationship to movie
    movie = db.relationship("Movie",
                            backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>" % (
            self.rating_id, self.movie_id, self.user_id, self.score)


##############################################################################
# Helper functions



def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."