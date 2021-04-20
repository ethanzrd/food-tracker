import datetime as dt
import uuid
from flask_login import current_user


def format_date(date):
    date_lst = date.split('-')
    date_lst[2].replace('0', '')
    date_lst[1].replace('0', '')
    for index, value in enumerate(date_lst):
        date_lst[index] = int(value)
    year, month, day = date_lst[0], date_lst[1], date_lst[2]
    months = [(i, dt.date(2008, i, 1).strftime('%B')) for i in range(1, 13)]
    current_month = [month_item for month_item in months if month == month_item[0]][0][1]
    return f'{current_month} {day}, {year}'


def get_current_date():
    now = dt.datetime.now()
    return format_date(f'{now.year}-{now.month}-{now.day}')


def generate_id():
    return str(uuid.uuid4())


def get_user_foods():
    try:
        requested_lst = [(food.name, food.name) for food in current_user.foods]
        return requested_lst
    except AttributeError:
        return []
