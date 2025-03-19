from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from flask_login import current_user
from PKDD.users.users_models import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from PKDD import db


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) 
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        with Session(db.engines['users']) as session:
            user = session.scalars(select(User).where(User.username == username.data)).one_or_none()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')
    def validate_email(self, email):
        with Session(db.engines['users']) as session:
            user = session.scalars(select(User).where(User.email == email.data)).one_or_none()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')
    delete_account = SubmitField('Delete account')

    def validate_username(self, username):
        if username.data != current_user.username:
            with Session(db.engines['users']) as session:
                user = session.scalars(select(User).where(User.username == username.data)).one_or_none()
            if user:
                raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            with Session(db.engines['users']) as session:
                user = session.scalars(select(User).where(User.email == email.data)).one_or_none()
            if user:
                raise ValidationError('That email is already taken. Please choose a different one.')
            

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):        
        with Session(db.engines['users']) as session:
            user = session.scalars(select(User).where(User.email == email.data)).one_or_none()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')



class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


