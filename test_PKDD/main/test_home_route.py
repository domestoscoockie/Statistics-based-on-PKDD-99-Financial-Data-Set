import pytest


def test_invalid_route(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_get(client):
    response = client.get('/')
    assert response.status_code == 200
    

def test_post(client):
    response = client.post('/')
    assert response.status_code == 405
    

def test_put(client):
    response = client.put('/')
    assert response.status_code == 405
    

def test_delete(client):
    response = client.delete('/')
    assert response.status_code == 405
    
def test_home_get(client):
    response = client.get('/home')
    assert response.status_code == 200
    

def test_home_post(client):
    response = client.post('/home')
    assert response.status_code == 405
    

def test_home_put(client):
    response = client.put('/home')
    assert response.status_code == 405
    

def test_home_delete(client):
    response = client.delete('/home')
    assert response.status_code == 405