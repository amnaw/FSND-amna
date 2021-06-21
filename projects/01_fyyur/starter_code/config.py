import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = 'Aa123456'
    FLASK_HTPASSWD_PATH = '/secret/.htpasswd'
    FLASK_SECRET = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Aa123456@localhost:5432/Fyyurdb'
    DATABASE_URI = 'postgresql://postgres:Aa123456@localhost:5432/Fyyurdb'
    DB_SERVER = 'localhost'
    FLASK_ENV = 'development'

# TODO DONE : IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Aa123456@localhost:5432/Fyyurdb'
