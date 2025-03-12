import pytest
from unittest.mock import patch, Mock


@patch('flask_login.utils._get_user')
def test_logout_not_logged_in(mock_user, client):
    mock_user.return_value = Mock(is_authenticated=False)
    response = client.get('/logout', follow_redirects=False)
    assert response.status_code == 302
    

@patch('flask_login.utils._get_user')
def test_logout_logged_in(mock_user, client):
    mock_user.return_value = Mock(is_authenticated=True)
    response = client.get('/logout', follow_redirects=False)
    assert response.status_code == 302
    assert '/home' in response.headers['Location']

    