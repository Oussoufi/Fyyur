import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))


#SECRET_KEY = '373e5f1e8e36a63d8913352e9f8ef806'
# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Sefyu%401989@localhost:5432/fyyurdb'
SQLALCHEMY_TRACK_MODIFICATIONS = False