import pytest
from unittest.mock import patch, Mock
from flask import url_for
from PKDD.users.users_models import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from PKDD.users.users_models import User
from PKDD import bcrypt

@patch('flask_login.utils._get_user', return_value=Mock(is_authenticated=False, username='TestUser', email='test@test.com'))
def test_render_template(mock_user, client):
    response = client.get('/reset_password', follow_redirects=False)
    assert response.status_code == 200
    
@patch('flask_login.utils._get_user', return_value=Mock(is_authenticated=True, username='TestUser', email='test@test.com' ))    
def test_is_authenticated(mock_user, client):
    response = client.get('/reset_password', follow_redirects=False)
    assert '/home' in response.headers['Location']

@patch('flask_login.utils._get_user', return_value=Mock(is_authenticated=False, username='TestUser', email='test@test.com' ))    
@patch('PKDD.users.forms.RequestResetForm')
@patch('PKDD.users.utils.send_delete_account_email', return_value=None)
@patch('PKDD.users.utils.mail.send', return_value=None)
def test_send_reset_email(mock_send_mail,mock_mail,mock_form, mock_user, client, db_session):
    with Session(db_session.engines['users']) as session:
        user = User(username='TestUser', email='test@test.com', password='Password123!')
        session.add(user)
        session.commit()
    mock_form.return_value.validate_on_submit = True
    mock_form.return_value.email.data = 'test@test.com'
    response = client.post('/reset_password',data={'submit':True, 'email':'test@test.com'}, follow_redirects=False)
    assert '/login' in response.headers['Location']
    assert response.status_code == 302
    response = client.post('/reset_password',data={'submit':True, 'email':'test@test.com'}, follow_redirects=True)
    assert b'An email with instructions has been sent' in response.data
    assert response.status_code == 200
    

