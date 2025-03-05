import pytest
from unittest.mock import patch
from flask import current_app



def test_download_get(client):
    #app.config['LOGIN_DISABLED'] = True  (user logged in)
    response = client.get('/download')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/x-zip-compressed'
    assert 'attachment; filename=cleaned_csvs.zip' \
    in response.headers.get('Content-Disposition', '')


def test_download_post(client):
    response = client.post('/download')
    assert response.status_code == 405
    
def test_download_put(client):
    response = client.put('/download')
    assert response.status_code == 405


def test_download_delete(client):
    response = client.delete('/download')
    assert response.status_code == 405


@patch('os.path.exists', return_value=False)
def test_download_not_found(mock_exists, client, monkeypatch):
    monkeypatch.setitem(current_app.config, 'UPLOAD_DIRECTORY', '/some/fake/path')
    response = client.get('/download')
    assert response.status_code == 404

def test_download_authentication_redirect(client, monkeypatch):
    monkeypatch.setitem(client.application.config, 'LOGIN_DISABLED', False)
    response = client.get('/download', follow_redirects=False)
    assert response.status_code == 302

