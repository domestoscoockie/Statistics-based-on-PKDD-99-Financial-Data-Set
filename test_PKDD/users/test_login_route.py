import pytest
from unittest.mock import patch, Mock
from PKDD.users.users_models import User
from PKDD import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import Session
from flask_login import login_user

@patch('flask_login.utils._get_user')
def test_login_render_template(mock_user, client):
    mock_user.return_value = Mock(is_authenticated=False)
    response = client.get('/register', follow_redirects=False)
    assert response.status_code == 200


@patch('flask_login.utils._get_user')
def test_login_redirect(mock_user, client):
    mock_user.return_value = Mock(is_authenticated=True)
    response = client.post('/register', follow_redirects=False)
    assert response.status_code == 302
    assert '/home' in response.headers['Location']


@patch('flask_login.utils._get_user', return_value=Mock(is_authenticated=False))
@patch('PKDD.users.forms.LoginForm')
def test_login_success(mock_user, mock_form, client, db_session):
    mock_user.return_value = Mock(is_authenticated=None)
    mock_form.validate_on_submit.return_value = True
    mock_form.remember.return_value = True
    with Session(db_session.engines['users']) as session:
        password = bcrypt.generate_password_hash('Password123!').decode('utf-8')
        user = User(username='testuser', email='test@example.com',
                    password=password) 
        session.add(user)
        session.commit()
        response = client.post('/login',data={'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Password123!',
        'confirm_password': 'Password123!', 'submit':True}, follow_redirects=False)
        user = session.execute(select(User).where(User.email=='test@example.com')
                               ).scalar_one_or_none()
        with client.application.test_request_context():
            login_user(user, remember=mock_form.return_value)
        
        assert response.status_code == 302

@patch('flask_login.utils._get_user', return_value=Mock(is_authenticated=False))
@patch('PKDD.users.forms.LoginForm')
def test_login_not_success(mock_user, mock_form, client, db_session):
    mock_form.return_value.validate_on_submit.return_value = True
    
    with Session(db_session.engines['users']) as session:
        password = bcrypt.generate_password_hash('Password123!').decode('utf-8')
        user = User(username='testuser', email='test@example.com', password=password)
        session.add(user)
        session.commit()

        response = client.post('/login', data={
            'email': 'badtest@example.com',
            'password': 'WrongPassword123!',
            'remember': False
        }, follow_redirects=False)

        assert response.status_code == 200

 