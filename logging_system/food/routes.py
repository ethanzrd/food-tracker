from flask import Blueprint, request, abort, render_template

from logging_system.food.functions import get_foods, edit_item, delete_item, handle_addition_processing
from models import Food
from forms import NaturalProcessing, ManualProcessing
from flask_login import login_required, current_user

food_routing = Blueprint('food', __name__, url_prefix='/food')


@food_routing.route('/add', methods=['GET', 'POST'])
@login_required
def add_food_item():
    manual = bool(request.args.get('manual', False))
    natural = not manual
    form = NaturalProcessing() if natural else ManualProcessing()
    if form.validate_on_submit():
        return handle_addition_processing(form=form, natural=natural)
    return render_template('add.html', title='Add Food Item', foods=get_foods(current_user.foods), form=form,
                           natural=natural)


@food_routing.route('/edit/<public_id>', methods=['GET', 'POST'])
@login_required
def edit_food_item(public_id):
    requested_food = Food.query.filter_by(public_id=public_id).first()
    if requested_food.user == current_user:
        manual = bool(request.args.get('manual', False))
        if requested_food:
            form = ManualProcessing(food_name=requested_food.name,
                                    serving_unit=requested_food.serving_unit,
                                    quantity=requested_food.quantity,
                                    protein=requested_food.proteins,
                                    carbs=requested_food.carbs,
                                    fat=requested_food.fats)
            if form.validate_on_submit():
                return edit_item(requested_food, form, manual)
            return render_template('add.html', title="Edit Food Item", requested_food=requested_food, edit=True,
                                   manual=manual, form=form)
        else:
            return abort(404)
    else:
        return abort(403)


@food_routing.route('/delete-item/<public_id>')
@login_required
def delete_food_item(public_id):
    requested_item = Food.query.filter_by(public_id=public_id).first()
    if requested_item.user == current_user:
        manual = bool(request.args.get('manual', False))
        if requested_item:
            return delete_item(requested_item, manual)
        else:
            return abort(404)
    else:
        return abort(403)
