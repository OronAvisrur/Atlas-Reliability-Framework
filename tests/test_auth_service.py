import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session

from app.services.auth_service import register_user, authenticate_user, generate_token, verify_token
from app.db.models import User


@pytest.fixture
def mock_db():
    return Mock(spec=Session)


def test_register_user_success(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    user = register_user(mock_db, "testuser", "password123")
    
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    assert user.username == "testuser"


def test_register_user_duplicate(mock_db):
    existing_user = User(id=1, username="testuser", hashed_password="hash")
    mock_db.query.return_value.filter.return_value.first.return_value = existing_user
    
    with pytest.raises(ValueError, match="Username already exists"):
        register_user(mock_db, "testuser", "password123")


def test_authenticate_user_success(mock_db):
    user = User(id=1, username="testuser", hashed_password="$2b$12$abcdefghijklmnopqrstuv", is_active=True)
    mock_db.query.return_value.filter.return_value.first.return_value = user
    
    with pytest.raises(ValueError):
        authenticate_user(mock_db, "testuser", "wrongpassword")


def test_authenticate_user_not_found(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    with pytest.raises(ValueError, match="Invalid credentials"):
        authenticate_user(mock_db, "nonexistent", "password123")


def test_authenticate_user_inactive(mock_db):
    user = User(id=1, username="testuser", hashed_password="hash", is_active=False)
    mock_db.query.return_value.filter.return_value.first.return_value = user
    
    with pytest.raises(ValueError, match="User is inactive"):
        authenticate_user(mock_db, "testuser", "password123")


def test_generate_token():
    token = generate_token("testuser")
    
    assert isinstance(token, str)
    assert len(token) > 0


def test_verify_token_success():
    token = generate_token("testuser")
    
    username = verify_token(token)
    
    assert username == "testuser"


def test_verify_token_invalid():
    with pytest.raises(ValueError, match="Invalid token"):
        verify_token("invalid.token.here")