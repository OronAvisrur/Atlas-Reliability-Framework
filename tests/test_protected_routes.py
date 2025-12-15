import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from app.main import app
from app.db.models import User

client = TestClient(app)


@pytest.fixture
def mock_current_user():
    return User(id=1, username="testuser", hashed_password="hash", is_active=True)


@pytest.fixture
def valid_token():
    return "Bearer valid.jwt.token"


def test_books_search_without_token():
    response = client.post("/books/search", json={"description": "action books"})
    
    assert response.status_code == 403


def test_books_search_with_invalid_token():
    response = client.post(
        "/books/search",
        json={"description": "action books"},
        headers={"Authorization": "Bearer invalid.token"}
    )
    
    assert response.status_code == 401


def test_books_search_with_valid_token(mock_current_user, valid_token):
    with patch("app.core.dependencies.get_current_user", return_value=mock_current_user):
        with patch("app.services.ollama_service.ollama_service.extract_keywords") as mock_ollama:
            with patch("app.services.google_books_service.google_books_service.search_books") as mock_books:
                mock_ollama.return_value = {"keyword_1": "action", "keyword_2": "books", "keyword_3": "adventure"}
                mock_books.return_value = {"total_items": 10, "items": []}
                
                response = client.post(
                    "/books/search",
                    json={"description": "action books"},
                    headers={"Authorization": valid_token}
                )
                
                assert response.status_code == 200
                assert "query_keywords" in response.json()


def test_books_search_inactive_user(valid_token):
    inactive_user = User(id=1, username="inactive", hashed_password="hash", is_active=False)
    
    with patch("app.core.dependencies.verify_token", return_value="inactive"):
        with patch("app.core.dependencies.get_db") as mock_db:
            mock_session = Mock()
            mock_session.query.return_value.filter.return_value.first.return_value = inactive_user
            mock_db.return_value.__next__.return_value = mock_session
            
            response = client.post(
                "/books/search",
                json={"description": "action books"},
                headers={"Authorization": valid_token}
            )
            
            assert response.status_code == 401
            assert "Inactive user" in response.json()["detail"]