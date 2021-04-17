from flask import Blueprint, request, render_template, abort, redirect, url_for

from logging_system.date.functions import add_to_log, get_date_dict, delete_from_log
from logging_system.food.functions import get_foods
from models import Date, Food

date_routing = Blueprint('date', __name__, url_prefix='/date')


@date_routing.route('/summary/<public_id>', methods=['GET', 'POST'])
def view_summary(public_id):
    requested_date = Date.query.filter_by(public_id=public_id).first()
    if requested_date:
        if request.method == 'POST':
            add_to_log(food_name=request.form.get('food-select'), requested_date=requested_date)
        return render_template('view.html', requested_date=get_date_dict(requested_date),
                               foods=get_foods(requested_date.foods, include_deleted=True),
                               all_foods=get_foods(Food.query.all()))
    else:
        return abort(404)


@date_routing.route('/delete/<public_id>')
def delete_log_item(public_id):
    food_name = request.args.get('food_name')
    requested_date = Date.query.filter_by(public_id=public_id).first()
    if requested_date:
        delete_from_log(food_name, requested_date)
        return redirect(url_for('date.view_summary', public_id=public_id))
    else:
        return abort(404)
