import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'dev'  # change this to something strong for production
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
