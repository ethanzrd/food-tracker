from extensions import db
from flask import Flask
from context_manager import get_year, get_existing_records
from logging_system.date.routes import date_routing
from logging_system.food.routes import food_routing
from main.routes import main_routing


def create_app(config_file='app_config.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    app.register_blueprint(main_routing)
    app.register_blueprint(food_routing)
    app.register_blueprint(date_routing)

    return app


app = create_app()
app.app_context().push()
from models import Date

db.create_all()

app.context_processor(get_year)
app.context_processor(get_existing_records)

if __name__ == '__main__':
    app.run(debug=True)
