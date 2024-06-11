from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import Length

class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField('Username', validators=[Length(min=4, max=25)])
    password = PasswordField('Password', validators=[Length(min=6, max=50)])
    email = StringField('Email', validators=[Length(min=6, max=50)])
    first_name = StringField('First Name', validators=[Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[Length(min=2, max=30)])


class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField('Username', validators=[Length(min=4, max=25)])
    password = PasswordField('Password', validators=[Length(min=6, max=50)])

class FeedbackForm(FlaskForm):
    """Form for adding feedback."""

    title = StringField('Title', validators=[Length(min=1, max=100)])
    content = TextAreaField('Content', validators=[Length(min=1, max=1000)])