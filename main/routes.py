from flask import Blueprint, request, flash, render_template, redirect, url_for

from extensions import db
from logging_system.date.functions import add_log, get_dates
from models import Date
from sqlalchemy.exc import OperationalError

main_routing = Blueprint('main', __name__)


@main_routing.route('/home', methods=['GET', 'POST'])
@main_routing.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        given_date = request.form.get('date')
        if '-' not in given_date:
            flash("Please provide a valid date.")
        else:
            add_log(given_date)
    try:
        requested_dates = Date.query.all()
    except OperationalError:
        db.create_all()
        return redirect(url_for('main.home'))
    return render_template('index.html', title='Home', dates=get_dates(requested_dates))
