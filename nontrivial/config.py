import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('FLASKEMAIL')
    MAIL_PASSWORD = os.environ.get('FLASKPASSWORD')

    SECRET_KEY = "secret"
