"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""


def load_movies():
    """Load movies from u.item into database."""
    #dates are given as strings, we need to store date as actual date object
    #research Python datetime library to find function parsing string into object



def load_ratings():
    """Load ratings from u.data into database."""

    input_text = open("u.data")

    for strings in input_text:
        input_text.split('\t')
        user_id = input_text[0]
        movie_id = input_text[1]
        score = input_text[2]

INSERT INTO ratings (NULL, )

#we are currently trying to figure out how to use SQLAlchemy SYNTAX to insert our data
#into the database. We know how to use SQLite3, so see if that helps
#we have currently split our lines into indexes and we're ready to insert into tables
#we need to figure out how primary autoincremting keys will work if we don't know the value
#(EG, can we use null if it's not a null value)    

if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_movies()
    load_ratings()
