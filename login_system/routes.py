from flask import Blueprint, url_for, flash, render_template, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

from login_system.functions import register_user
from validation_manager.wrappers import logout_required
from forms import LoginForm, RegisterForm
from models import User

login_system = Blueprint('login_system', __name__)


@login_system.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    form = LoginForm()
    user_name = None
    email = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            if user.confirmed_email:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('main.home'))
                else:
                    flash("Incorrect password, please try again.")
            else:
                email = user.email
                user_name = user.name
                flash("unconfirmed")
        else:
            flash("This email does not exist, please try again.")
    return render_template("login.html", form=form, email=email, user_name=user_name, title="Login",
                           redirected=request.args.get('redirected', False))


@login_system.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return register_user(name=form.name.data, email=form.email.data.lower(), password=form.password.data,)
    return render_template('login.html', form=form, title="Register")


@login_system.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_system.login'))
