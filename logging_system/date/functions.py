from flask import flash
from flask_login import login_required, current_user

from extensions import db
from models import Date, Food
from utils import format_date
from sqlalchemy.exc import IntegrityError
import uuid


def get_date_dict(requested_date):
    def get_sum(nutrition):
        return round(sum([getattr(food, nutrition) for food in requested_date.foods]), 2)

    date_summary = {'date': requested_date.date,
                    'public_id': requested_date.public_id,
                    'protein': get_sum('proteins'),
                    'carbohydrate': get_sum('carbs'),
                    'fat': get_sum('fats'),
                    'calories': get_sum('calories')}
    return date_summary


def get_dates(dates):
    requested_dates = []
    try:
        for date in dates:
            requested_dates.append(get_date_dict(date))
    except TypeError:
        pass
    return requested_dates


@login_required
def add_log(given_date):
    requested_date = format_date(given_date)
    existing_date = Date.query.filter_by(date=requested_date).first()
    if not existing_date:
        new_date = Date(date=requested_date, public_id=str(uuid.uuid4()), user=current_user)
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


def delete_from_log(food_id, requested_date):
    requested_item = Food.query.filter_by(public_id=food_id).first()
    if requested_item:
        for food in requested_date.foods:
            if food.public_id == food_id:
                requested_date.foods.remove(food)
                db.session.commit()
                break
        else:
            return flash("This item does not exist in your log.")
        if requested_item.deleted:
            for date in Date.query.all():
                if requested_item in date.foods:
                    break
            else:
                db.session.delete(requested_item)
                db.session.commit()
    else:
        flash("This item does not exist in the food database.")
