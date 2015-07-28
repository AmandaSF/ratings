"""Utility file to seed ratings database from MovieLens data in seed_data/"""

import datetime
from model import User, Rating, Movie, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""
    
    with open("seed_data/u.user", "r") as input_text:    #opens file and reads it
        for line in input_text:                         #loops through data and turns into list of lists of CSV
            user_data = line.rstrip().split('|')        
    #         # print user_data                             #code check
            user_id = user_data[0]
            age = user_data[1]
            zipcode = user_data[4]
    #         # print user_id                                   #code check 
    #         # print age
    #         # print zipcode
            new_user = User(user_id=int(user_id), email=None, password=None, age=int(age), zipcode=zipcode)
    #     # print new_user                                #code check
            db.session.add(new_user)
        db.session.commit()


def load_movies():
    """Load movies from u.item into database."""
    
    with open("seed_data/u.item", "r") as input_text:  #opens file and reads it
        for line in input_text:                         #loops through data and turns into list of lists of CSV
            movie_data = line.rstrip().split('|')   
            # print movie_data                          #code check
            movie_id = movie_data[0]
            title_year = movie_data[1]
            released_UTC = movie_data[2]
            imdb_url = movie_data[4]
            # print movie_id                            #code check
            # print title_year
            # print released_UTC
            # print imdb_url
            title = title_year[:-6]
            # print title                                #code check
            if released_UTC:
                released_at = datetime.datetime.strptime(released_UTC, "%d-%b-%Y").date()
            else:       #use if/else bc of dirty data
                released_at = None
            # print released_at                          #code check
            new_movie = Movie(movie_id=movie_id, title=title, released_at=released_at, imdb_url=imdb_url)
        #     # print new_movie                           #code check
            db.session.add(new_movie)
        db.session.commit()
   

def load_ratings():
    """Load ratings from u.data into database."""

    with open("seed_data/u.data", "r") as input_text:    #opens file and reads it
        for line in input_text:                         #loops through data and turns into list of lists of CSV
            rating_data = line.rstrip().split('\t') 
#             # print rating_data                         #code check
            user_id = rating_data[0]
            movie_id = rating_data[1]
            score = rating_data[2]
#             # print user_id                             #code check
#             # print movie_id
#             # print score
            new_rating = Rating(user_id=int(user_id), movie_id=int(movie_id), score=int(score))
#             print new_rating                              #code check
            db.session.add(new_rating)
        db.session.commit()
  


if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_movies()
    load_ratings()
