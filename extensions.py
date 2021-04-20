from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()
csrf_protection = CSRFProtect()
mail = Mail()
