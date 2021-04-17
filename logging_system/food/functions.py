from models import Food
from extensions import db
from flask import flash, redirect, url_for


def get_foods(foods, include_deleted=False):
    requested_foods = []
    count = 1
    for food in foods:
        if food.deleted and include_deleted or not food.deleted:
            requested_foods.append((count, food))
            count += 1
    return requested_foods


def add_item(food_arguments):
    requested_item = Food.query.filter_by(name=food_arguments['name']).first()
    if not requested_item:
        new_item = Food(**food_arguments)
        db.session.add(new_item)
        db.session.commit()
    else:
        if requested_item.deleted:
            requested_item.deleted = False
            for arg in Food.get_arguments():
                setattr(requested_item, arg, food_arguments[arg])
            db.session.commit()
        else:
            flash("This item already exists.")


def edit_item(requested_food, food_arguments):
    requested_food.name = food_arguments['food-name']
    requested_food.proteins = food_arguments['protein']
    requested_food.carbs = food_arguments['carbohydrates']
    requested_food.fats = food_arguments['fat']
    db.session.commit()
    return redirect(url_for('food.add_food_item'))


def delete_item(requested_item):
    requested_item.deleted = True
    db.session.commit()
    return redirect(url_for('food.add_food_item'))
