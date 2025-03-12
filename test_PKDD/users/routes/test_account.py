import pytest
from unittest.mock import patch, Mock
from flask import url_for
from flask_login import current_user

@patch('flask_login.utils._get_user', return_value=Mock(is_authenticated=False))
def test_render_template(mock_user,client):
    response = client.get('/account', follow_redirects=False)
    assert response.status_code == 200


@patch('PKDD.users.utils.send_delete_account_email', return_value = None)
@patch('PKDD.users.forms.UpdateAccountForm')
@patch('flask_login.utils._get_user', return_value=Mock(is_authenticated=True, username='TestUser', email='test@test.com'))
@patch('flask_mail.Mail.send', return_value=None)
def test_send_delete_email(mock_mail, mock_user, mock_form_class, mock_send_delete, client):
    form_instance = mock_form_class.return_value
    form_instance.validate_on_submit.return_value = True
    form_instance.delete_account.data = True
    form_instance.submit.data = False


    response = client.post('/account', 
            data={'delete_account': True, 'username':'TestUser',
                  'email':'test@test.com'},
              follow_redirects=False)
    assert response.status_code == 302
    assert '/account' in response.headers['Location'] 


@patch('PKDD.users.forms.UpdateAccountForm')
@patch('flask_login.utils._get_user', return_value=Mock(is_authenticated=True, username='TestUser', email='test@test.com'))
def test_change_user_data(mock_user , mock_form_class, client, db_session):
    form_instance = mock_form_class.return_value
    form_instance.validate_on_submit.return_value = True
    form_instance.delete_account.data = False
    form_instance.submit.data = True
    form_instance.username.data = 'newTestUser' 
    form_instance.email.data = 'newtest@test.com' 

    assert current_user.username == 'TestUser'
    assert current_user.email == 'test@test.com'


    response = client.post('/account', 
                data={ 'username':'newTestUser',
                  'email':'newtest@test.com', 'submit':True},
                follow_redirects=False)
    
    assert current_user.username == 'newTestUser'
    assert current_user.email == 'newtest@test.com'
    assert response.status_code == 302

@patch('flask_login.utils._get_user')
def test_get(mock_get_user, client):
    mock_user = Mock(is_authenticated=True, username='TestUser', email='test@test.com')
    mock_get_user.return_value = mock_user 

    response = client.get('/account')

    assert b'TestUser' in response.data  
    assert b'test@test.com' in response.data  
    assert response.status_code == 200 