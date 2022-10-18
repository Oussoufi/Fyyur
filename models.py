from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
#from db_setup import db



# TODO: connect to a local postgresql database
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()




#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# Show Table Model
#----------------------------------------------------------------------------------------------

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  start_time = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())

  def __repr__(self):
    return f'<Show ID: {self.id}, venue id: {self.venue_id} , artist id: {self.artist_id}> '

# Show Table Model
#----------------------------------------------------------------------------------------------


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    genres = db.Column(ARRAY(db.String()))
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String())
    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
      return f'<Venue ID: {self.id}, Name: {self.name}, city: {self.city}, state: {self.state}, address: {self.address}, \
        phone: {self.phone}, image_link: {self.image_link}, facebook: {self.facebook_link}, genres: {self.genres}\
          website: {self.website_link}, seeking_talent: {self.seeking_talent}, seeking_description: {self.seeking_description} >'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


# Show Table Model
#----------------------------------------------------------------------------------------------

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean(), nullable=False, default=False)
    seeking_description = db.Column(db.String())
    shows = db.relationship('Show', backref='artist', lazy=True)
    
    def __repr__(self):
      return f'<Artist ID: {self.id}, Name: {self.name}, city: {self.city}, state: {self.state}, \
        phone: {self.phone}, image_link: {self.image_link}, facebook: {self.facebook_link}, genres: {self.genres}\
          website: {self.website_link}, seeking_venue: {self.seeking_venue}, seeking_description: {self.seeking_description} >'

