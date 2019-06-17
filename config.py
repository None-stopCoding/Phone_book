import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tenzor_team_2_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "postgresql://postgres:12345@localhost/phone"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

