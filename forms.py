from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Email
from flask_login import current_user


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in", render_kw={"style": "margin-top: 20px; width: 100%"})


class NaturalProcessing(FlaskForm):
    description = StringField('Food Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ManualProcessing(FlaskForm):
    food_name = StringField('Food Name', validators=[DataRequired()])
    serving_unit = StringField('Serving Unit', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    protein = IntegerField('Protein', validators=[DataRequired()])
    carbs = IntegerField('Carbohydrates', validators=[DataRequired()])
    fat = IntegerField('Fat', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register', render_kw={"style": "margin-top: 20px; width: 100%"})


class NewDate(FlaskForm):
    date = DateField('Add a new date')
    submit = SubmitField('Add Date')


class SelectItem(FlaskForm):
    item_choice = SelectField('Add Food')
    submit = SubmitField('Add Food')


class ForgetPasswordForm(FlaskForm):
    new_password = PasswordField("Enter your new password:", validators=[DataRequired()])
    submit = SubmitField("Submit", render_kw={"style": "margin-top: 20px; width: 100%;"})


class ForgetHandlingForm(FlaskForm):
    email = StringField("Enter your email address:", validators=[DataRequired(), Email()])
    submit = SubmitField("Proceed", render_kw={"style": "margin-top: 20px; width: 100%;"})
