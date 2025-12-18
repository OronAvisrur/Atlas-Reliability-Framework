import pytest
from unittest.mock import Mock, patch

from app.services.auth_service import register_user, authenticate_user, generate_token, verify_token


@pytest.fixture
def mock_conn():
    return Mock()


@pytest.fixture
def mock_cursor():
    cursor = Mock()
    cursor.fetchone = Mock()
    cursor.close = Mock()
    return cursor


def test_register_user_success(mock_conn, mock_cursor):
    with patch("app.services.auth_service.hash_password", return_value="hashed_pass"):
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [None, (1, "testuser", True)]
        
        user = register_user(mock_conn, "testuser", "password123")
        
        assert user["username"] == "testuser"
        assert user["id"] == 1
        assert user["is_active"] is True
        mock_cursor.close.assert_called()


def test_register_user_duplicate(mock_conn, mock_cursor):
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1,)
    
    with pytest.raises(ValueError, match="Username already exists"):
        register_user(mock_conn, "testuser", "password123")


def test_authenticate_user_success(mock_conn, mock_cursor):
    with patch("app.services.auth_service.verify_password", return_value=False):
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, "testuser", "hashed", True)
        
        with pytest.raises(ValueError, match="Invalid credentials"):
            authenticate_user(mock_conn, "testuser", "wrongpassword")


def test_authenticate_user_not_found(mock_conn, mock_cursor):
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    with pytest.raises(ValueError, match="Invalid credentials"):
        authenticate_user(mock_conn, "nonexistent", "password123")


def test_authenticate_user_inactive(mock_conn, mock_cursor):
    with patch("app.services.auth_service.verify_password", return_value=True):
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, "testuser", "hashed", False)
        
        with pytest.raises(ValueError, match="User is inactive"):
            authenticate_user(mock_conn, "testuser", "password123")


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