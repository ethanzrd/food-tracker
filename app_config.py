import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///food-tracker.db')
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = os.environ.get('EMAIL')
MAIL_PASSWORD = os.environ.get('PASSWORD')
MAIL_USE_TLS = True
