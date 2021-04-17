from models import Food, Date
from extensions import db
from flask import flash, redirect, url_for, abort, request
import requests
from settings import NUTRITIONIX_HEADERS
import uuid


def get_foods(foods, include_deleted=False):
    requested_foods = []
    count = 1
    for food in foods:
        if food.deleted and include_deleted or not food.deleted:
            requested_foods.append((count, food))
            count += 1
    return requested_foods


def food_natural_processing(food_name):
    data = {
        'query': food_name
    }
    if not food_name:
        return flash("Please provide a valid food description.")
    food_data = requests.post('https://trackapi.nutritionix.com/v2/natural/nutrients',
                              headers=NUTRITIONIX_HEADERS, data=data)
    if food_data.status_code == 404:
        return flash("Could not find the requested food item.")
    elif food_data.status_code != 200:
        return flash("An error occurred during the handling of your request.")
    elif food_data.status_code == 200:
        food_json = food_data.json()['foods'][0]
        food_arguments = {
            'name': f"{food_json['food_name'].title()} - "
                    f"{food_json['serving_qty']} {food_json['serving_unit'].title()}",
            'proteins': food_json['nf_protein'],
            'carbs': food_json['nf_total_carbohydrate'],
            'fats': food_json['nf_total_fat']
        }
        return food_arguments


def item_addition(food_arguments, manual=False):
    food_name = food_arguments['name']
    kwargs = {}
    if manual:
        kwargs['manual'] = True
    else:
        food_arguments = food_natural_processing(food_name)
    if isinstance(food_arguments, dict):
        requested_item = Food.query.filter_by(name=food_arguments['name']).first()
        if not requested_item:
            food_arguments['public_id'] = str(uuid.uuid4())
            save_item_addition(food_arguments)
            return redirect(url_for('food.add_food_item', **kwargs))
        else:
            if requested_item.deleted:
                restore_item(requested_item, food_arguments)
                return redirect(url_for('food.add_food_item', **kwargs))
            else:
                flash("This item already exists.")
                return redirect(url_for('food.add_food_item', **kwargs))
    else:
        if manual:
            flash("Malformed request.")
        return redirect(url_for('food.add_food_item', **kwargs))


def restore_item(requested_item, food_arguments):
    requested_item.deleted = False
    for arg in Food.get_arguments():
        setattr(requested_item, arg, food_arguments[arg])
    db.session.commit()


def save_item_addition(food_arguments):
    new_food = Food(**food_arguments)
    db.session.add(new_food)
    db.session.commit()


def handle_addition_processing(natural, form):
    if not natural:
        try:
            food_arguments = {'name': form['food-name'].title().strip(),
                              'proteins': form['protein'],
                              'carbs': form['carbohydrates'],
                              'fats': form['fat']}
        except KeyError:
            return abort(400)
    else:
        try:
            food_arguments = {'name': form['food-description'].strip()}
        except KeyError:
            return abort(400)
    return item_addition(food_arguments=food_arguments, manual=not natural)


def edit_item(requested_food, food_arguments, manual=False):
    kwargs = {}
    if manual:
        kwargs['manual'] = True
    requested_food.name = food_arguments['food-name']
    requested_food.proteins = food_arguments['protein']
    requested_food.carbs = food_arguments['carbohydrates']
    requested_food.fats = food_arguments['fat']
    db.session.commit()
    return redirect(url_for('food.add_food_item', **kwargs))


def delete_item(requested_item):
    kwargs = {}
    manual = request.args.get('manual', False)
    if manual:
        kwargs['manual'] = True
    for date in Date.query.all():
        if requested_item in date.foods:
            requested_item.deleted = True
            db.session.commit()
            return redirect(url_for('food.add_food_item'))
    db.session.delete(requested_item)
    db.session.commit()
    return redirect(url_for('food.add_food_item', **kwargs))
