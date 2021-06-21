from models import db, Venue, Artist, GenresChoices, Genre, venue_artists
from app import app
from flask_sqlalchemy import SQLAlchemy
from flask import Flask 
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import ShowForm, VenueForm, ArtistForm
from flask_migrate import Migrate
from config import *
from models import *

# # Inserct New Records
# newVen = person2 = Venue(name='The Musical Hop')
# # This will queue up inserct statement in a transaction that is managed by db.session
# db.session.add(person)
# db.session.add(person2)
# # db.session.add_all([person, person2])
# db.session.commit()


Venue.query.with_entities(id, name).join()