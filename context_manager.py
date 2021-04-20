from flask_login import current_user

from models import Date
import datetime as dt


def get_existing_records():
    dates = current_user.dates if current_user.is_authenticated else []
    return dict(existing_records=len(dates))


def get_year():
    return dict(year=dt.datetime.now().year)
