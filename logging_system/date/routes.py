from flask import Blueprint, request, render_template, abort, redirect, url_for
from flask_login import login_required, current_user

from forms import SelectItem
from logging_system.date.functions import add_to_log, get_date_dict, delete_from_log, delete_log
from logging_system.food.functions import get_foods
from models import Date
from utils import get_user_foods

date_routing = Blueprint('date', __name__, url_prefix='/date')


@date_routing.route('/summary/<public_id>', methods=['GET', 'POST'])
@login_required
def view_summary(public_id):
    form = SelectItem()
    form.item_choice.choices = get_user_foods()
    requested_date = Date.query.filter_by(public_id=public_id).first()
    if requested_date:
        if requested_date.user == current_user:
            if form.validate_on_submit():
                add_to_log(food_name=form.item_choice.data, requested_date=requested_date)
            return render_template('view.html', requested_date=get_date_dict(requested_date),
                                   foods=get_foods(requested_date.foods, include_deleted=True), form=form,
                                   all_foods=get_foods(current_user.foods), title='View Summary')
        else:
            return abort(403)
    else:
        return abort(404)


@date_routing.route('/delete/<public_id>')
def delete_date(public_id):
    requested_date = Date.query.filter_by(public_id=public_id).first()
    if requested_date:
        if requested_date.user == current_user:
            delete_log(requested_date)
            return redirect(url_for('main.home'))
        else:
            return abort(403)
    else:
        return abort(404)


@date_routing.route('/delete-item/<public_id>')
def delete_log_item(public_id):
    food_id = request.args.get('food_id')
    requested_date = Date.query.filter_by(public_id=public_id).first()
    if requested_date:
        if requested_date.user == current_user:
            delete_from_log(food_id, requested_date)
            return redirect(url_for('date.view_summary', public_id=public_id))
        else:
            return abort(403)
    else:
        return abort(404)
