from extensions import db, login_manager, bootstrap, csrf_protection, mail
from flask import Flask
from models import User
from context_manager import get_year, get_existing_records
from logging_system.date.routes import date_routing
from logging_system.food.routes import food_routing
from login_system.routes import login_system
from main.routes import main_routing
from verification_manager.routes import verification


def create_app(config_file='app_config.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    csrf_protection.init_app(app)
    mail.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        requested_user = User.query.get(user_id)
        return requested_user

    app.register_blueprint(main_routing)
    app.register_blueprint(food_routing)
    app.register_blueprint(date_routing)
    app.register_blueprint(login_system)
    app.register_blueprint(verification)

    return app


app = create_app()
app.app_context().push()
from models import Date

db.create_all()

app.context_processor(get_year)
app.context_processor(get_existing_records)

if __name__ == '__main__':
    app.run(debug=True)
