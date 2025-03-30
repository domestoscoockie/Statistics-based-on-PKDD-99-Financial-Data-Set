import pytest
from unittest.mock import patch, Mock
from flask import url_for
from werkzeug.test import Client
from PKDD.users.users_models import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from flask_bcrypt import check_password_hash
from PKDD import bcrypt

@patch('flask_login.utils._get_user')
def test_get(mock_user, client):
    mock_user.return_value = Mock(is_authenticated=False)
    response = client.get('/register', follow_redirects=False)
    assert response.status_code == 200


@patch('flask_login.utils._get_user')
def test_get_redirect_to_home(mock_user, client):
    mock_user.return_value = Mock(is_authenticated=True)
    response = client.get('/register', follow_redirects=False)
    assert response.status_code == 302



@patch('flask_login.utils._get_user')
@patch('PKDD.users.forms.RegistrationForm')
# @patch('PKDD.users.routes.recaptcha_register_verify', return_value=None)
def test_register_success(mock_form, mock_user, client: Client, db_session):
    mock_user.return_value = Mock(is_authenticated=False)
    mock_form.return_value.validate_on_submit.return_value = True
    with Session(db_session.engines['users']) as session:   
        response = client.post('/register',  data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Password123!',
        'confirm_password': 'Password123!',
        'submit': True}, follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.headers['Location']


@patch('flask_login.utils._get_user')
@patch('PKDD.users.forms.RegistrationForm')
# @patch('PKDD.users.routes.recaptcha_register_verify', return_value=None)
@patch('PKDD.users.routes.bcrypt.generate_password_hash', return_value=bcrypt.generate_password_hash('Password123!'))
def test_register_user_added_to_db( mock_hash_password, mock_form,
                           mock_user, client, db_session,app):
    mock_user.return_value = Mock(is_authenticated=False)
    mock_form.return_value.validate_on_submit.return_value = True
    mock_form.return_value.username.data = 'testuser'
    mock_form.return_value.email.data = 'test@example.com'
    mock_form.return_value.password.data = 'Password123!'
    mock_form.return_value.confirm_password.data = 'Password123!'

    with Session(db_session.engines['users']) as session:     
        assert session.scalars(select(User)
                .where(User.username == 'testuser')).fetchall() == []
        response = client.post('/register',  data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Password123!',
        'confirm_password': 'Password123!',
        'submit': True}, follow_redirects=False)
        session.commit()
        user =  session.scalars(select(User)
                    .where(User.username == 'testuser')).one_or_none()
    assert user is not None
    assert user.password != 'Password123!'
    assert check_password_hash(user.password,'Password123!')
    
    
        