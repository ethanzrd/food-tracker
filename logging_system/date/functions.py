from flask import flash
from extensions import db
from models import Date, Food
from utils import format_date
from sqlalchemy.exc import IntegrityError


def get_date_dict(requested_date):
    def get_sum(nutrition):
        return sum([getattr(food, nutrition) for food in requested_date.foods])

    date_summary = {'date': requested_date.date,
                    'public_id': requested_date.public_id,
                    'protein': get_sum('proteins'),
                    'carbohydrate': get_sum('carbs'),
                    'fat': get_sum('fats'),
                    'calories': get_sum('calories')}
    return date_summary


def get_dates(dates):
    requested_dates = []
    for date in dates:
        requested_dates.append(get_date_dict(date))
    return requested_dates


def add_log(given_date):
    requested_date = format_date(given_date)
    existing_date = Date.query.filter_by(date=requested_date).first()
    if not existing_date:
        new_date = Date(date=requested_date)
        db.session.add(new_date)
        db.session.commit()
    else:
        flash("This date already exists.")


def delete_log(requested_date):
    db.session.delete(requested_date)
    db.session.commit()


def add_to_log(food_name, requested_date):
    requested_item = Food.query.filter_by(name=food_name).first()
    if requested_item:
        requested_date.foods.append(requested_item)
        try:
            db.session.commit()
        except IntegrityError:
            flash("This item already exists in this date's log.")
            db.session.rollback()
    else:
        flash("Could not find the requested food item.")


def delete_from_log(food_name, requested_date):
    for food in requested_date.foods:
        if food.name == food_name:
            requested_date.foods.remove(food)
            db.session.commit()
            break
    else:
        flash("This item does not exist in your log.")

