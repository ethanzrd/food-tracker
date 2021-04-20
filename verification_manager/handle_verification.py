from werkzeug.security import generate_password_hash

from notification_system.notifications import password_changed_notification
from verification_manager.helpers import load_token
from models import User
from utils import get_current_date
from extensions import db
from flask_login import login_user
from flask import flash, redirect, url_for, abort


def handle_email_verification(token, public_id):
    load_token(token=token, salt='email-verify', redirect_to='login_system.register')
    user = User.query.filter_by(public_id=public_id).first()
    if user:
        if not user.confirmed_email:
            user.confirmed_email = True
            user.join_date = get_current_date()
            db.session.commit()
            login_user(user)
            flash("You've confirmed your email successfully.")
        else:
            flash("You've already confirmed your email.")
        return redirect(url_for('main.home'))
    else:
        flash("This user does not exist.")
        return redirect(url_for('login_system.register'))


def handle_forgot_password(token, user, new_password):
    load_token(token=token, salt='forget-password', redirect_to='login')
    if user:
        new_password = generate_password_hash(password=new_password,
                                              method='pbkdf2:sha256', salt_length=8)
        try:
            user.password = new_password
        except AttributeError:
            return abort(400)
        db.session.commit()
        password_changed_notification(user.email, user.name, get_current_date())
        flash("Password changed successfully.")
        return redirect(url_for('login_system.login'))
    else:
        flash("Could not find a user with the specified email address.")
        return redirect(url_for('login_system.login'))
