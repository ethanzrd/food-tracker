from settings import serializer, TOKEN_AGE
from itsdangerous import SignatureExpired, BadTimeSignature
from flask import flash, url_for, redirect


def load_token(token, salt, redirect_to='home.home_page'):
    """Checks whether a token is valid or redirects the user."""
    try:
        confirmation = serializer.loads(token, salt=salt, max_age=TOKEN_AGE)
    except SignatureExpired:
        flash("The token is expired, please try again.")
        return redirect(url_for(redirect_to))
    except BadTimeSignature:
        flash("Incorrect token, please try again.")
        return redirect(url_for(redirect_to))
