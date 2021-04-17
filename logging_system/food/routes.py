from flask import Blueprint, request, abort, render_template

from logging_system.food.functions import add_item, get_foods, edit_item, delete_item
from models import Food

food_routing = Blueprint('food', __name__, url_prefix='/food')


@food_routing.route('/add', methods=['GET', 'POST'])
def add_food_item():
    if request.method == 'POST':
        try:
            food_arguments = {'name': request.form['food-name'].title(),
                              'proteins': request.form['protein'],
                              'carbs': request.form['carbohydrates'],
                              'fats': request.form['fat']}
        except KeyError:
            return abort(400)
        else:
            add_item(food_arguments)
    return render_template('add.html', title='Add Food Item', foods=get_foods(Food.query.all()))


@food_routing.route('/edit/<public_id>', methods=['GET', 'POST'])
def edit_food_item(public_id):
    requested_food = Food.query.filter_by(public_id=public_id).first()
    if requested_food:
        if request.method == 'POST':
            return edit_item(requested_food, request.form)
        return render_template('edit.html', title="Edit Food Item", requested_food=requested_food)
    else:
        return abort(404)


@food_routing.route('/delete-item/<public_id>')
def delete_food_item(public_id):
    requested_item = Food.query.filter_by(public_id=public_id).first()
    if requested_item:
        return delete_item(requested_item)
    else:
        return abort(404)
