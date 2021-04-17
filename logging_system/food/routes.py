from flask import Blueprint, request, abort, render_template, flash

from logging_system.food.functions import get_foods, edit_item, delete_item, handle_addition_processing
from models import Food
from settings import REQUIRED_MANUAL_ARGUMENTS, REQUIRED_NATURAL_ARGUMENTS
from utils import validate_form

food_routing = Blueprint('food', __name__, url_prefix='/food')


@food_routing.route('/add', methods=['GET', 'POST'])
def add_food_item():
    manual = request.args.get('manual', False)
    natural = not manual
    if request.method == 'POST':
        form_valid = validate_form(request.form, REQUIRED_NATURAL_ARGUMENTS if natural else REQUIRED_MANUAL_ARGUMENTS)
        if form_valid:
            return handle_addition_processing(form=request.form, natural=natural)
        else:
            flash("Please fill all of the fields.")
    return render_template('add.html', title='Add Food Item', foods=get_foods(Food.query.all()), natural=natural)


@food_routing.route('/edit/<public_id>', methods=['GET', 'POST'])
def edit_food_item(public_id):
    requested_food = Food.query.filter_by(public_id=public_id).first()
    manual = request.args.get('manual', False)
    if manual in ['True', 'False']:
        manual = eval(manual)
    if requested_food:
        if request.method == 'POST':
            return edit_item(requested_food, request.form, manual)
        return render_template('add.html', title="Edit Food Item", requested_food=requested_food, edit=True,
                               manual=manual)
    else:
        return abort(404)


@food_routing.route('/delete-item/<public_id>')
def delete_food_item(public_id):
    requested_item = Food.query.filter_by(public_id=public_id).first()
    if requested_item:
        return delete_item(requested_item)
    else:
        return abort(404)
