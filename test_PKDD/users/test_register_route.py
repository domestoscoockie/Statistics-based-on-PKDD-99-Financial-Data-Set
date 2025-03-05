import pytest
from unittest.mock import patch, Mock
from flask import url_for

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
@patch('PKDD.users.utils.recaptcha_register_verify', autospec=True)
@patch('PKDD.users.routes.bcrypt.generate_password_hash', return_value=b'hash123')
@patch('PKDD.users.routes.db.session.add', autospec=True)
@patch('PKDD.users.routes.db.session.commit', autospec=True)
def test_register_success(mock_commit, mock_add, mock_bcrypt, mock_recaptcha, mock_form, mock_user, client):
    mock_user.return_value = Mock(is_authenticated=False)

    mock_form_instance = mock_form.return_value
    mock_form_instance.is_submitted = Mock(return_value=True)  # Mockowanie is_submitted() na True
    mock_form_instance.validate = Mock(return_value=True) 
    mock_form.validate_on_submit = True
    mock_form_instance.username.data = 'testuser'
    mock_form_instance.email.data = 'test@example.com'
    mock_form_instance.password.data = 'Password123!'
    mock_form_instance.confirm_password.data = 'Password123!'
    response = client.post('/register', follow_redirects=False)
    assert response.status_code == 302
    assert url_for('users.login') in response.headers['Location']


