from flask import render_template, url_for, flash, redirect, request, Blueprint,\
send_from_directory, current_app, abort
from PKDD import db
from flask import Blueprint
from PKDD.users.forms import RegistrationForm, LoginForm, UpdateAccountForm,\
      ResetPasswordForm, RequestResetForm 
from flask_login import login_user, current_user, logout_user, login_required
from PKDD.users.users_models import User 
from PKDD import bcrypt
from PKDD.users.utils import send_reset_email, send_delete_account_email
import requests
from sqlalchemy import select
from sqlalchemy.orm import Session


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # recaptcha_register_verify()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        with Session(db.engines['users']) as session:
            user = User(username=form.username.data, email=form.email.data,
                         password=hashed_password)
            session.add(user)
            session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title= 'Register',
                            form=form)


@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        with Session(db.engines['users']) as session:
            user = session.scalars(select(User).where(User.email == form.email.data)).one_or_none()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    
    return render_template('login.html', title='Login', form=form)


@users.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.delete_account.data:
            send_delete_account_email(current_user)
            flash('To confirm, please visit the link sent to your email', 'info')
            return redirect(url_for('users.account'))
        elif form.submit.data and form.validate():
            with Session(db.engines['users']) as session:
                user = session.scalars(select(User).where(User.id == current_user.id)).one_or_none()
                user.username = form.username.data
                user.email = form.email.data
                session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('users.account'))
        
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)



@users.route('/account/<token>', methods=['GET','POST'])
def delete_account(token):
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token!', 'warning')
        return redirect(url_for('main.home'))
    
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted!', 'success')
    return redirect(url_for('main.home'))

@users.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        with Session(db.engines['users']) as session:
            user = session.scalars(select(User).where(User.email == form.email.data)).one_or_none()
        send_reset_email(user)
        flash('An email with instructions has been sent', 'info')
        return redirect(url_for('users.login'))
    
    return render_template('reset_request.html', form=form, title='Reset Password')



@users.route('/reset_password/<token>', methods=['GET','POST'])
def reset_password_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    user = User.verify_token(token)
    if user == None:
        flash('That is an invalid or expired token!', 'warning')
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        with Session(db.engines['users']) as session:
            user.password = hashed_password
            db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('reset_password_token.html', form=form, title='nie')







