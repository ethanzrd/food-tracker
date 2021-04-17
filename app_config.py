import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///food-tracker.db')
