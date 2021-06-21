#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import ShowForm, VenueForm, ArtistForm
from flask_migrate import Migrate
from config import *
from models import *
from sqlalchemy.sql import func
from datetime import datetime
import datetime


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
db.init_app(app)
app.config.from_object('config')
# db = SQLAlchemy(app)


# TODO DONE : connect to a local postgresql database
# Use the Migrate class to link up flask app+ sqlAlchmy db
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# in models.py

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
      date = dateutil.parser.parse(value)
  else:
      date = value
  
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

# RETRIEVE VENUES BASED ON STATE
@app.route('/venues')
def venues():
  # TODO DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  # STEPS:
#  gather venues list per city first:
# -loop thro city
# -loop thro top-list and see if this top's city is like the first city in the loop
# if YS add this top data into Venus list
# if no more venus in the current city loop(loop top-list finished)
# -store the State
# -then add the city State in Dic obj "data" + Venues list
# -Go to next city & repeat 

   # SQL STEPS:
# select id, name, Count(shows.venu_id) num
# from venues, JOIN show
# group by state, city, id;

  
    list_of_tuples = [] # [(4, 'The Dueling Pianos Bar', 1, 'NY', 'New York'), (6, 'Park Square Live Music & Coffee', 1, 'CA', 'San Francisco')]
    # this list joins with Show to get Shows num
    with app.app_context():
        list_of_tuples = Venue.query.with_entities(Venue.id, Venue.name, func.count(Venue.id), Venue.state, Venue.city).join(venue_artists).join(Artist).filter((venue_artists.c.Venue_id == Venue.id) & (venue_artists.c.Artist_id == Artist.id)).group_by(Venue).all()
    
    # this list of items that doesn't have Show :(
    list_of_tuples2 = Venue.query.with_entities(Venue.id, Venue.name, Venue.state, Venue.city).all()
    venue_id_show = []
    for venue in list_of_tuples:
        venue_id_show.append(venue[0])

    list_of_tuples3 = []
    for venue1 in list_of_tuples2:
        if venue1[0] not in venue_id_show:
            list_of_tuples3.append( (venue1[0],venue1[1], 0, venue1[2], venue1[3]) ) 

    list_of_tuples = list_of_tuples + list_of_tuples3

    data = []
    exist_cities = [] # ['riyadh', 'jeddah', 'abha']
    state = ""
    for x in list_of_tuples:
        if x[4] not in exist_cities:
          exist_cities.append(x[4])

###########--  Make The data Dic --#####################
    for x in list_of_tuples:
        if x[4] not in exist_cities:
            exist_cities.append(x[4])


    for city in exist_cities:
        venues = []
        for tupley in list_of_tuples:
            if tupley[4] == city:
              venuObj = {
                  "id": tupley[0],
                  "name": tupley[1],
                  "num_upcoming_shows": tupley[2],
                }
              venues.append(venuObj)
              state = tupley[3]
 
        dataObj = {
             "city": city,
             "state": state,
             "venues": venues
            }
        data.append(dataObj)

    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  # we have to search in Venues Table
  search_term = request.form.get('search_term', '')
  search_term = '%' + search_term + '%'  
  query_result = Venue.query.with_entities(Venue.id, Venue.name, func.count(Venue.id)).join(venue_artists).join(Artist).filter((venue_artists.c.Venue_id == Venue.id) & (venue_artists.c.Artist_id == Artist.id)).group_by(Venue).filter(Venue.name.ilike(search_term)).all()
  # [(6, 'Park Square Live Music & Coffee', 1), (2, 'The Musical Hop', 3)]
  query_result2 = Venue.query.with_entities(Venue.id, Venue.name).filter(Venue.name.ilike(search_term)).all()
  venue_id_show = []
  for venue in query_result:
    venue_id_show.append(venue[0])

  query_result3 = []
  for venue1 in query_result2:
    if venue1[0] not in venue_id_show:
      query_result3.append( (venue1[0],venue1[1], 0) )

  query_result = query_result + query_result3

  count = len(query_result)
  data = []
  response = {}
  for venue in query_result:
    id = venue[0]
    name = venue[1]
    num_upcoming_shows = venue[2]
    dataObj = {
      "id": id,
      "name": name,
      "num_upcoming_shows": num_upcoming_shows
    }
    data.append(dataObj)

  response={
      "count": count,
      "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO DONE: replace with real venue data from the venues table, using venue_id
  VenueT = Venue.query.with_entities(Venue.id, Venue.name, Venue.address,Venue.city, Venue.state ,Venue.phone, Venue.image_link, Venue.facebook_link, Venue.website_link, Venue.seeking_talent, Venue.seeking_desc).filter(Venue.id == venue_id).all()

  genres_list = []
  genres = Genre.query.with_entities(Genre.name).join(venue_genres).filter((venue_genres.c.genre_id == Genre.id) & (venue_genres.c.venue_id == venue_id)).all()
  for genre in genres:
     genres_list.append(genre[0])


  list_show = db.session.query(Artist.id, Artist.name, Artist.image_link, venue_artists.c.start_time).join(Artist).filter(venue_artists.c.Venue_id == venue_id).all()

  now = datetime.datetime.now()
  past_shows = []
  comping_shows = []

  for show in list_show:
      if show[3] < now:
          newTime = show[3]
          past_showObj = {
      "artist_id": show[0],
      "artist_name":  show[1],
      "artist_image_link": show[2],
      "start_time": newTime
    }
          past_shows.append(past_showObj)
      else:
          newTime = show[3]
          comping_showObj = {
      "artist_id": show[0],
      "artist_name":  show[1],
      "artist_image_link": show[2],
      "start_time": newTime
    }
          comping_shows.append(comping_showObj)

  for ven in VenueT:
      data = {
    "id": ven[0],
    "name": ven[1],
    "genres": genres_list,
    "address": ven[2],
    "city": ven[3],
    "state": ven[4],
    "phone": ven[5],
    "website": ven[8],
    "facebook_link": ven[7],
    "seeking_talent": ven[9],
    "seeking_description":ven[10],
    "image_link": ven[6],
    "past_shows": past_shows,
    "upcoming_shows": comping_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(comping_shows),
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO DONE : insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
      seeking_talent = False
      if 'seeking_talent' in request.form:
        seeking_talent = True
      form = VenueForm()
      #if request.method == 'POST' and form.validate():
      new_venue = Venue(name=request.form['name'],
                                city=request.form['city'],
                                state=request.form['state'],
                                address=request.form['address'],
                                phone=request.form['phone'],
                                image_link=request.form['image_link'],
                                facebook_link=request.form['facebook_link'],
                                website_link=request.form['website_link'],
                                seeking_talent=seeking_talent,
                                seeking_desc=request.form['seeking_description']
                              )
      # Add the record to the session object
      db.session.add(new_venue)
      db.session.commit()

      genres=request.form['genres']
      genres_list = genres.split (",")
      genres_recods = []
      for genre in genres_list:
          genre_recod = Genre.query.filter(Genre.name == genre).first()
          new_venue.genres.append(genre_recod)

      db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
  
  # TODO DONE : on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  
  except sqlalchemy.exc.DataError as e:
    #if request.method == 'POST' and form.validate() == False:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    #if flash(form.name.validators[0].message):
      #flash('An error occurred. Venue ' + form.name.validators[0].message + ' could not be listed.')
 
  return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO DONE : Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
 
  try:
      # grab the existing record to delete it
      venue = Venue.query.get(venue_id)
      db.session.delete(venue) # or... Todo.query.filter_by(id=todo_id).delete()
      db.session.commit()
  except:
      db.session.rollback()
  finally:
      db.session.close()
      return jsonify(body) 

  # BONUS CHALLENGE DONE : Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO DONE : replace with real data returned from querying the database
  list_of_tuples = [] 
  list_of_tuples = Artist.query.with_entities(Artist.id, Artist.name).all()
  data = []

###########--  Make The data Dic --#####################

  for tupley in list_of_tuples:
    artistObj = {
       "id": tupley[0],
       "name": tupley[1],
        }
    data.append(artistObj)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  # we have to search in Artist Table
  search_term = request.form.get('search_term', '')
  search_term = '%' + search_term + '%'  
  query_result = Artist.query.with_entities(Artist.id, Artist.name, func.count(Artist.id)).join(venue_artists, isouter=True).join(Venue,isouter=True).filter((venue_artists.c.Artist_id == Artist.id) & (venue_artists.c.Venue_id == Venue.id)).group_by(Artist).filter(Artist.name.ilike(search_term)).all()
  query_result2 = Artist.query.with_entities(Artist.id, Artist.name).filter(Artist.name.ilike(search_term)).all()
  # [(3, 'Will Champion', 2), (2, 'Chris martin', 1)]
  
  data = []
  response = {}
  artist_id_show = []
  for artist in query_result:
    artist_id_show.append(artist[0])
 
  query_result3 = []
  for artist1 in query_result2:
    if artist1[0] in artist_id_show:
      query_result2.remove(artist1)
    else: 
      query_result3.append( (artist1[0],artist1[1], 0) )

  query_result = query_result + query_result3
  count = len(query_result)
  for artist in query_result:
    id = artist[0]
    name = artist[1]
    num_upcoming_shows = artist[2]
    dataObj = {
      "id": id,
      "name": name,
      "num_upcoming_shows": num_upcoming_shows
    }
    data.append(dataObj)

  response={
      "count": count,
      "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO DONE: replace with real artist data from the artist table, using artist_id
  ArtistT = Artist.query.with_entities(Artist.id, Artist.name, Artist.city, Artist.state ,Artist.phone, Artist.image_link, Artist.facebook_link, Artist.website_link, Artist.seeking_performance, Artist.seeking_desc).filter(Artist.id == artist_id).all()

  genres_list = []
  genres = Genre.query.with_entities(Genre.name).join(artist_genres).filter((artist_genres.c.genre_id == Genre.id) & (artist_genres.c.artist_id == artist_id)).all()
  for genre in genres:
     genres_list.append(genre[0])


  list_show = db.session.query(Venue.id, Venue.name, Venue.image_link, venue_artists.c.start_time).join(Venue).filter(venue_artists.c.Artist_id == artist_id).all()

  now = datetime.datetime.now()
  past_shows = []
  comping_shows = []

  for show in list_show:
      if show[3] < now:
          newTime = show[3]
          past_showObj = {
      "venue_id": show[0],
      "venue_name":  show[1],
      "venue_image_link": show[2],
      "start_time": newTime
    }
          past_shows.append(past_showObj)
      else:
          newTime = show[3]
          comping_showObj = {
      "artist_id": show[0],
      "artist_name":  show[1],
      "artist_image_link": show[2],
      "start_time": newTime
    }
          comping_shows.append(comping_showObj)

  
  for art in ArtistT:
      data = {
    "id": art[0],
    "name": art[1],
    "genres": genres_list,
  
    "city": art[2],
    "state": art[3],
    "phone": art[4],
    "website": art[7],
    "facebook_link": art[6],
    "seeking_venue": art[8],
    "seeking_description":art[9],
    "image_link": art[5],
    "past_shows": past_shows,
    "upcoming_shows": comping_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(comping_shows),

  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  art = Artist.query.with_entities(Artist.id, Artist.name, Artist.city, Artist.state ,Artist.phone, Artist.image_link, Artist.facebook_link, Artist.website_link, Artist.seeking_performance, Artist.seeking_desc).filter(Artist.id == artist_id).first()
  genres_list = []
  genres = Genre.query.with_entities(Genre.name).join(artist_genres).filter((artist_genres.c.genre_id == Genre.id) & (artist_genres.c.artist_id == artist_id)).all()
  for genre in genres:
     genres_list.append(genre[0])

  artist = {
    "id": art[0],
    "name": art[1],
    "genres": genres_list,
    "city": art[2],
    "state": art[3],
    "phone": art[4],
    "website": art[7],
    "facebook_link": art[6],
    "seeking_venue": art[8],
    "seeking_description":art[9],
    "image_link": art[5]
  }
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  # TODO DONE : populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO DONE : take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
      seeking_venue = False
      if 'seeking_venue' in request.form:
        seeking_venue = True
      form = VenueForm()
      #if request.method == 'POST' and form.validate():
      
      artist = Artist(name=request.form['name'],
                                city=request.form['city'],
                                state=request.form['state'],
                                phone=request.form['phone'],
                                image_link=request.form['image_link'],
                                facebook_link=request.form['facebook_link'],
                                website_link=request.form['website_link'],
                                seeking_performance=seeking_venue,
                                seeking_desc=request.form['seeking_description']
                              )
      # Add the record to the session object
      #edited_artist2 = Artist.query.get(artist_id).update(request.data)
      db.session.query(Artist).filter(Artist.id == artist_id).update({
        'name':request.form['name'],
        'city':request.form['city'],
        'state':request.form['state'],
        'phone':request.form['phone'],
        'image_link':request.form['image_link'],
        'facebook_link':request.form['facebook_link'],
        'website_link':request.form['website_link'],
        'seeking_performance':seeking_venue,
        'seeking_desc':request.form['seeking_description']
      })
      db.session.commit()

      edited_artist = Artist.query.get(artist_id)

      genres=request.form['genres']
      genres_list = genres.split (",")
      genres_recods = []
      for genre in genres_list:
          genre_recod = Genre.query.filter(Genre.name == genre).first()
          edited_artist.genres.append(genre_recod)

      db.session.commit()

      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully edited !')

  # TODO DONE : on unsuccessful db insert, flash an error instead.
  except sqlalchemy.exc.DataError as e:
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be edited.')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  ven = Venue.query.with_entities(Venue.id, Venue.name, Venue.address,Venue.city, Venue.state ,Venue.phone, Venue.image_link, Venue.facebook_link, Venue.website_link, Venue.seeking_talent, Venue.seeking_desc).filter(Venue.id == venue_id).first()
  genres_list = []
  genres = Genre.query.with_entities(Genre.name).join(venue_genres).filter((venue_genres.c.genre_id == Genre.id) & (venue_genres.c.venue_id == venue_id)).all()
  for genre in genres:
     genres_list.append(genre[0])

  venue = {
    "id": ven[0],
    "name": ven[1],
    "genres": genres_list,
    "address": ven[2],
    "city": ven[3],
    "state": ven[4],
    "phone": ven[5],
    "website": ven[8],
    "facebook_link": ven[7],
    "seeking_talent": ven[9],
    "seeking_description":ven[10],
    "image_link": ven[6]
  }
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  # TODO DONE : populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO DONE : take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
      seeking_talent = False
      if 'seeking_talent' in request.form:
        seeking_talent = True
      form = VenueForm()
      new_venue = Venue(name=request.form['name'],
                                city=request.form['city'],
                                state=request.form['state'],
                                address=request.form['address'],
                                phone=request.form['phone'],
                                image_link=request.form['image_link'],
                                facebook_link=request.form['facebook_link'],
                                website_link=request.form['website_link'],
                                seeking_talent=seeking_talent,
                                seeking_desc=request.form['seeking_description']
                              )
      db.session.query(Venue).filter(Venue.id == venue_id).update({
        'name':request.form['name'],
        'city':request.form['city'],
        'state':request.form['state'],
        'address':request.form['address'],
        'phone':request.form['phone'],
        'image_link':request.form['image_link'],
        'facebook_link':request.form['facebook_link'],
        'website_link':request.form['website_link'],
        'seeking_talent':seeking_talent,
        'seeking_desc':request.form['seeking_description']
      })
      db.session.commit()

      edited_venue = Venue.query.get(venue_id)

      genres=request.form['genres']
      genres_list = genres.split (",")
      genres_recods = []
      for genre in genres_list:
          genre_recod = Genre.query.filter(Genre.name == genre).first()
          edited_venue.genres.append(genre_recod)

      db.session.commit()

      flash('Venue ' + request.form['name'] + ' was successfully edited!')
  
  # TODO DONE : on unsuccessful db insert, flash an error instead.
  except sqlalchemy.exc.DataError as e:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be edited.')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO DONE : insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
      seeking_venue = False
      if 'seeking_venue' in request.form:
        seeking_venue = True
      form = VenueForm()
      #if request.method == 'POST' and form.validate():
      new_artist = Artist(name=request.form['name'],
                                city=request.form['city'],
                                state=request.form['state'],
                                phone=request.form['phone'],
                                image_link=request.form['image_link'],
                                facebook_link=request.form['facebook_link'],
                                website_link=request.form['website_link'],
                                seeking_performance=seeking_venue,
                                seeking_desc=request.form['seeking_description']
                              )
      # Add the record to the session object
      db.session.add(new_artist)
      db.session.commit()

      genres=request.form['genres']
      genres_list = genres.split (",")
      genres_recods = []
      for genre in genres_list:
          genre_recod = Genre.query.filter(Genre.name == genre).first()
          new_artist.genres.append(genre_recod)

      db.session.commit()
      
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')

  # TODO DONE: on unsuccessful db insert, flash an error instead.
  except sqlalchemy.exc.DataError as e:
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO DONE : replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = db.session.query(Venue.id, Venue.name, Artist.id, Artist.name, Artist.image_link, venue_artists.c.start_time).join(Venue).join(Artist).filter((venue_artists.c.Artist_id == Artist.id) & (venue_artists.c.Venue_id == Venue.id)).all()
  data = []
  for show in shows:
      showObj = {
        "venue_id": show[0],
        "venue_name": show[1],
        "artist_id": show[2],
        "artist_name": show[3],
        "artist_image_link": show[4],
        "start_time": show[5]
      }
      data.append(showObj)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO DONE : insert form data as a new Show record in the db, instead
  try:
      insert_stmnt = venue_artists.insert().values(Venue_id=request.form['venue_id'], Artist_id=request.form['artist_id'], start_time=request.form['start_time'])
      db.session.execute(insert_stmnt) 

      db.session.commit()
      # on successful db insert, flash success
      flash('Show was successfully listed!')

  # TODO DONE : on unsuccessful db insert, flash an error instead.
  except sqlalchemy.exc.DataError as e:
      flash('An error occurred. The Show could not be listed.')
  except sqlalchemy.exc.IntegrityError as e:
      flash('An error occurred. The Show could not be listed.')

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
