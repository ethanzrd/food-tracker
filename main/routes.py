from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user

from extensions import db
from forms import NewDate
from logging_system.date.functions import add_log, get_dates
from sqlalchemy.exc import OperationalError

main_routing = Blueprint('main', __name__)


@main_routing.route('/home', methods=['GET', 'POST'])
@main_routing.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        form = NewDate()
        if form.validate_on_submit():
            add_log(str(form.date.data))
        try:
            if current_user.is_authenticated:
                requested_dates = current_user.dates
            else:
                requested_dates = None
        except OperationalError:
            db.create_all()
            return redirect(url_for('main.home'))
        return render_template('index.html', title='Home', dates=get_dates(requested_dates), form=form)
    else:
        return redirect(url_for('login_system.login', redirected=True))
