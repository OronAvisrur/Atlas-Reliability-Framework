import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from app.main import app
from app.db.models import User

client = TestClient(app)


@pytest.fixture
def mock_db_session():
    with patch("app.api.routes.auth.get_db") as mock:
        yield mock


def test_register_success(mock_db_session):
    mock_db = Mock()
    mock_db_session.return_value.__next__.return_value = mock_db
    
    with patch("app.api.routes.auth.register_user") as mock_register:
        mock_user = User(id=1, username="testuser", hashed_password="hash", is_active=True)
        mock_register.return_value = mock_user
        
        response = client.post("/auth/register", json={"username": "testuser", "password": "password123"})
        
        assert response.status_code == 201
        assert response.json()["username"] == "testuser"


def test_register_duplicate_username(mock_db_session):
    mock_db = Mock()
    mock_db_session.return_value.__next__.return_value = mock_db
    
    with patch("app.api.routes.auth.register_user") as mock_register:
        mock_register.side_effect = ValueError("Username already exists")
        
        response = client.post("/auth/register", json={"username": "testuser", "password": "password123"})
        
        assert response.status_code == 400
        assert "Username already exists" in response.json()["detail"]


def test_register_invalid_username():
    response = client.post("/auth/register", json={"username": "ab", "password": "password123"})
    
    assert response.status_code == 422


def test_login_success(mock_db_session):
    mock_db = Mock()
    mock_db_session.return_value.__next__.return_value = mock_db
    
    with patch("app.api.routes.auth.authenticate_user") as mock_auth:
        with patch("app.api.routes.auth.generate_token") as mock_token:
            mock_user = User(id=1, username="testuser", hashed_password="hash", is_active=True)
            mock_auth.return_value = mock_user
            mock_token.return_value = "fake.jwt.token"
            
            response = client.post("/auth/login", json={"username": "testuser", "password": "password123"})
            
            assert response.status_code == 200
            assert response.json()["access_token"] == "fake.jwt.token"
            assert response.json()["token_type"] == "bearer"


def test_login_invalid_credentials(mock_db_session):
    mock_db = Mock()
    mock_db_session.return_value.__next__.return_value = mock_db
    
    with patch("app.api.routes.auth.authenticate_user") as mock_auth:
        mock_auth.side_effect = ValueError("Invalid credentials")
        
        response = client.post("/auth/login", json={"username": "testuser", "password": "wrongpass"})
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]