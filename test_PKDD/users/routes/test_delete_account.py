import pytest
from unittest.mock import patch, Mock
from flask import url_for
from PKDD.users.users_models import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from PKDD.users.users_models import User
from PKDD import bcrypt

@patch('PKDD.users.routes.User.verify_token')
@patch('flask_login.utils._get_user', return_value=Mock(is_authenticated=True, username='TestUser', email='test@test.com'))
def test_delete_account_valid_token(mock_get_user, mock_verify_token, client, db_session):
    with Session(db_session.engines['users']) as session:
        user = User(username='testuser', email='test@test.com',
                     password='password')
        session.add(user)
        session.commit()

    mock_verify_token.return_value = user

    response = client.get(url_for('users.delete_account', token='valid_token'), follow_redirects=True)

    assert b'Your account has been deleted!' in response.data
    assert response.status_code == 200
    with Session(db_session.engines['users']) as session:
        assert session.execute(select(User).where(User.username == 'testuser')).scalar_one_or_none() == None

@patch('PKDD.users.routes.User.verify_token')
@patch('flask_login.utils._get_user', return_value=Mock(is_authenticated=True, username='TestUser', email='test@test.com'))
def test_delete_account_invalid_token(mock_get_user, mock_verify_token, client):
    mock_verify_token.return_value = None

    response = client.get(url_for('users.delete_account', token='invalid_token'), follow_redirects=True)

    assert b'That is an invalid or expired token!' in response.data
    assert response.status_code == 200

