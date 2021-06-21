#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import enum
from flask_sqlalchemy import SQLAlchemy
from config import *
db = SQLAlchemy()
#app.config.from_object('config')


#----------------------------------------------------------------------------#
# Models.

#----------------------------------------------------------------------------#

# Associative table M-M relationship   
venue_genres = db.Table('venue_genres',
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
)

# Associative table M-M relationship   
artist_genres = db.Table('artist_genres',
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
)

#Show table - Associative table M-M relationship     
venue_artists = db.Table('Show',
    db.Column('Venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('Artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('start_time', db.DateTime, primary_key=True)
)
    




class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(150))

    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_desc = db.Column(db.String)
   
    # Relationship with Genres - M-M
    genres = db.relationship('Genre', secondary=venue_genres,
      backref=db.backref('venues', lazy = 'joined', 
                                   cascade="all",
                                   passive_deletes=True))

    # Relationship with Artists - M-M
    artists = db.relationship('Artist', secondary=venue_artists,
      backref=db.backref('venues', lazy = 'joined',
                                   cascade="all",
                                   passive_deletes=True))

    # TODO DONE : implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    # genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(150))

    seeking_performance = db.Column(db.Boolean, nullable=False, default=False)
    seeking_desc = db.Column(db.String)

    # Relationship with Genres - M-M
    genres = db.relationship('Genre', secondary=artist_genres,
      backref=db.backref('artists', lazy = 'joined',
                                   cascade="all",
                                   passive_deletes=True))
      
    # Relationship with Venues - M-M is Done via "venue_artists" table
    # TODO DONE : implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# Enum Class
class GenresChoices(enum.Enum):
    Alternative = 'Alternative'
    Blues = 'Blues'

    # @staticmethod
    # def fetch_names():
    #     return [c.value for c in GenresChoices]
    def __str__(self):
        return str(self.value)

   
class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    # name = db.Column(db.Enum(GenresChoices, values_callable=lambda x: [str(member.value) for member in GenresChoices]))
    # Enum.values_callable we can persist the values of Enum members instead of their names.





