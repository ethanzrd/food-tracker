from flask import Blueprint, request, abort, render_template, flash, redirect, url_for

from forms import ForgetPasswordForm, ForgetHandlingForm
from models import User
from verification_manager.generate_verification import generate_password_reset
from verification_manager.handle_verification import handle_email_verification, handle_forgot_password
from verification_manager.helpers import load_token

verification = Blueprint('verification', __name__)


@verification.route('/verify-email/<token>')
def verify_email(token):
    public_id = request.args.get('public_id')
    if public_id:
        return handle_email_verification(token=token, public_id=public_id)
    else:
        return abort(400)


@verification.route('/generate-forget', methods=['GET', 'POST'])
def generate_forget():
    form = ForgetHandlingForm()
    if form.validate_on_submit():
        return generate_password_reset(form.email.data)
    return render_template('forgot-password.html', title="Password Recovery", generating=True, form=form)


@verification.route('/handle-forget/<token>', methods=['GET', 'POST'])
def forget_password(token):
    load_token(token=token, salt='forget-password', redirect_to='login_system.login')
    public_id = request.args.get('public_id')
    print(public_id)
    form = ForgetPasswordForm()
    user = User.query.filter_by(public_id=public_id).first()
    if user:
        if form.validate_on_submit():
            return handle_forgot_password(token=token, user=user, new_password=form.new_password.data)
        return render_template('forgot-password.html', title="Password Recovery", token=token, form=form,
                               public_id=public_id, handling=True)
    else:
        flash("Could not find a user with the specified email address.")
        return redirect(url_for('login_system.login'))
