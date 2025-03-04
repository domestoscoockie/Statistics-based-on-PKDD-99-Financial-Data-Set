import pytest
from PKDD.main.routes import download, home
from test_PKDD import conftest
from unittest.mock import patch, Mock
import os
from flask import current_app

def test_invalid_route(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_home_get(client):
    response = client.get('/')
    assert response.status_code == 200
    

def test_home_post(client):
    response = client.post('/')
    assert response.status_code == 405
    

def test_home_put(client):
    response = client.put('/')
    assert response.status_code == 405
    

def test_home_delete(client):
    response = client.delete('/')
    assert response.status_code == 405
    


def test_download_get(client):
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
def test_download_not_found_mock_os(mock_exists, client, monkeypatch):
    monkeypatch.setitem(current_app.config, 'UPLOAD_DIRECTORY', '/some/fake/path')
    response = client.get('/download')
    assert response.status_code == 404