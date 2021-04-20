from flask_mail import Message
from settings import EMAIL

from notification_system.functions import send_mail


def verify_email(name, email, link):
    msg = Message('Confirmation Email', sender=EMAIL, recipients=[email])
    msg.body = f"Hello {name}, please go to this link to finalize your registration to our Food Tracker.\n\n" \
               f"{link}\n\nNote: If you're unfamiliar with the source of this email, simply ignore it."
    return send_mail(msg, allow_redirects=False)


def reset_password_notification(name, email, link):
    msg = Message('Forget Password', sender=EMAIL, recipients=[email])
    msg.body = f"Hello {name}, you have recently requested a password change to our food tracker," \
               f" please go to this link to reset your password.\n\n{link}\n\n" \
               f"If this wasn't you, please contact us by replying to this email or via our website."
    return send_mail(msg)


def password_changed_notification(email, name, date):
    msg = Message(f'Password Changed', sender=EMAIL, recipients=[email])
    msg.body = f"Hello {name}, this is an automatic email from the food tracker service to notify you of recent" \
               f" events that occurred in regards to your account.\n\n" \
               f'Your account password was changed at {date}.\n\n' \
               f"If this wasn't you, contact us by replying to this email or via our website."
    send_mail(msg)
