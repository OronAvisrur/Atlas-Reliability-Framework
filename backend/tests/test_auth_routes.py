import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from backend.main import app

client = TestClient(app)


def test_register_success():
    with patch("backend.api.routes.auth.get_db") as mock_get_db:
        with patch("backend.api.routes.auth.register_user") as mock_register:
            mock_conn = Mock()
            mock_get_db.return_value.__enter__.return_value = mock_conn
            mock_register.return_value = {"id": 1, "username": "testuser", "is_active": True}
            
            response = client.post("/auth/register", json={"username": "testuser", "password": "password123"})
            
            assert response.status_code == 201
            assert response.json()["username"] == "testuser"


def test_register_duplicate_username():
    with patch("backend.api.routes.auth.get_db") as mock_get_db:
        with patch("backend.api.routes.auth.register_user") as mock_register:
            mock_conn = Mock()
            mock_get_db.return_value.__enter__.return_value = mock_conn
            mock_register.side_effect = ValueError("Username already exists")
            
            response = client.post("/auth/register", json={"username": "testuser", "password": "password123"})
            
            assert response.status_code == 400
            assert "Username already exists" in response.json()["detail"]


def test_register_invalid_username():
    response = client.post("/auth/register", json={"username": "ab", "password": "password123"})
    
    assert response.status_code == 422


def test_login_success():
    with patch("backend.api.routes.auth.get_db") as mock_get_db:
        with patch("backend.api.routes.auth.authenticate_user") as mock_auth:
            with patch("backend.api.routes.auth.generate_token") as mock_token:
                mock_conn = Mock()
                mock_get_db.return_value.__enter__.return_value = mock_conn
                mock_auth.return_value = {"id": 1, "username": "testuser", "is_active": True}
                mock_token.return_value = "fake.jwt.token"
                
                response = client.post("/auth/login", json={"username": "testuser", "password": "password123"})
                
                assert response.status_code == 200
                assert response.json()["access_token"] == "fake.jwt.token"
                assert response.json()["token_type"] == "bearer"


def test_login_invalid_credentials():
    with patch("backend.api.routes.auth.get_db") as mock_get_db:
        with patch("backend.api.routes.auth.authenticate_user") as mock_auth:
            mock_conn = Mock()
            mock_get_db.return_value.__enter__.return_value = mock_conn
            mock_auth.side_effect = ValueError("Invalid credentials")
            
            response = client.post("/auth/login", json={"username": "testuser", "password": "wrongpass"})
            
            assert response.status_code == 401
            assert "Invalid credentials" in response.json()["detail"]