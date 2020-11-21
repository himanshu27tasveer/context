from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from app.saarthi import db
from wtforms.fields.html5 import URLField
from wtforms.validators import url


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        user = db.execute("SELECT * FROM users WHERE email = :email",{"email":email.data}).fetchone()
        if user:
            raise ValidationError('Email is already taken. Please choose a different one.')


class SearchForm(FlaskForm):
    url = URLField(validators=[url(), DataRequired()])
    submit = SubmitField('Fetch')