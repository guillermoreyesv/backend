from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)
url = '/v1/login'

@pytest.mark.asyncio
async def test_login_successful():
    user_data = {"username": "user@example.com", "password": "string"}
    
    response = client.post(url, data=user_data)
    
    assert response.status_code == 200
    
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_user_not_found():
    user_data = {"username": "nonexistentuser", "password": "testpassword"}

    response = client.post(url, data=user_data)
    
    assert response.status_code == 404
    assert response.json() == {'message': 'User nonexistentuser not found'}

@pytest.mark.asyncio
async def test_login_invalid_password():
    user_data = {"username": "user@example.com", "password": "incorrectpassword"}
    
    response = client.post(url, data=user_data)
    
    assert response.status_code == 404
    assert response.json() == {'message': 'User user@example.com not found'}