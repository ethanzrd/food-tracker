from models import Date
import datetime as dt


def get_existing_records():
    return dict(existing_records=len(Date.query.all()))


def get_year():
    return dict(year=dt.datetime.now().year)
