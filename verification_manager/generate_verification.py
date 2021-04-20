from flask import redirect, url_for, flash
from notification_system.notifications import verify_email, reset_password_notification
from settings import serializer
from models import User


def generate_email_verification(email, public_id, name):
    token = serializer.dumps(public_id, salt='email-verify')
    link = url_for('verification.verify_email', token=token, public_id=public_id, _external=True)
    status = verify_email(email=email, name=name, link=link)
    flash("A confirmation email has been sent to you." if status else \
              "No sender specified, please contact the website staff.")
    return redirect(url_for('login_system.login'))


def generate_password_reset(email):
    requesting_user = User.query.filter_by(email=email).first()
    if requesting_user:
        token = serializer.dumps(email, salt='forget-password')
        link = url_for('verification.forget_password', token=token, public_id=requesting_user.public_id, _external=True)
        status = reset_password_notification(requesting_user.name, email, link)
        flash("A password reset email has been sent to you.") if status else \
            flash("No sender, specified, please contact the website staff.")
        return redirect(url_for('login_system.login'))
    else:
        flash("Could not find a user with the specified email address.")
        return redirect(url_for('verification.generate_forget'))
