import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_keywords():
    return {
        "keyword_1": "action",
        "keyword_2": "superhero",
        "keyword_3": "magic"
    }


@pytest.fixture
def mock_google_books_result():
    return {
        "total_items": 50,
        "items": [
            {
                "title": "Book 1",
                "authors": ["Author 1"],
                "description": "Description 1",
                "categories": ["Fiction"],
                "thumbnail": "http://example.com/1.jpg"
            },
            {
                "title": "Book 2",
                "authors": ["Author 2"],
                "description": "Description 2",
                "categories": ["Science"],
                "thumbnail": "http://example.com/2.jpg"
            }
        ]
    }


@pytest.fixture
def mock_user():
    return {"id": 1, "username": "testuser", "is_active": True}


class TestBooksRouter:
    
    def test_search_books_success(self, mock_keywords, mock_google_books_result, mock_user):
        with patch("app.core.dependencies.get_current_user", return_value=mock_user):
            with patch("app.api.routes.books.ollama_service.extract_keywords", new_callable=AsyncMock) as mock_ollama:
                with patch("app.api.routes.books.google_books_service.search_books", new_callable=AsyncMock) as mock_google:
                    mock_ollama.return_value = mock_keywords
                    mock_google.return_value = mock_google_books_result
                    
                    response = client.post(
                        "/books/search",
                        json={"description": "I am looking for action books with superheroes and magic"},
                        headers={"Authorization": "Bearer fake.token"}
                    )
                    
                    assert response.status_code == 200
                    assert response.json()["total_items"] == 50
                    assert len(response.json()["items"]) == 2
    
    def test_search_books_empty_results(self, mock_keywords, mock_user):
        with patch("app.core.dependencies.get_current_user", return_value=mock_user):
            with patch("app.api.routes.books.ollama_service.extract_keywords", new_callable=AsyncMock) as mock_ollama:
                with patch("app.api.routes.books.google_books_service.search_books", new_callable=AsyncMock) as mock_google:
                    mock_ollama.return_value = mock_keywords
                    mock_google.return_value = {"total_items": 0, "items": []}
                    
                    response = client.post(
                        "/books/search",
                        json={"description": "Some random description"},
                        headers={"Authorization": "Bearer fake.token"}
                    )
                    
                    assert response.status_code == 200
                    assert response.json()["total_items"] == 0
    
    def test_search_books_invalid_request_too_short(self):
        response = client.post(
            "/books/search",
            json={"description": "ab"},
            headers={"Authorization": "Bearer fake.token"}
        )
        
        assert response.status_code == 422
    
    def test_search_books_ollama_error(self, mock_user):
        with patch("app.core.dependencies.get_current_user", return_value=mock_user):
            with patch("app.api.routes.books.ollama_service.extract_keywords", new_callable=AsyncMock) as mock_ollama:
                mock_ollama.side_effect = Exception("Ollama Error")
                
                response = client.post(
                    "/books/search",
                    json={"description": "I want action books"},
                    headers={"Authorization": "Bearer fake.token"}
                )
                
                assert response.status_code == 500
    
    def test_search_books_google_error(self, mock_keywords, mock_user):
        with patch("app.core.dependencies.get_current_user", return_value=mock_user):
            with patch("app.api.routes.books.ollama_service.extract_keywords", new_callable=AsyncMock) as mock_ollama:
                with patch("app.api.routes.books.google_books_service.search_books", new_callable=AsyncMock) as mock_google:
                    mock_ollama.return_value = mock_keywords
                    mock_google.side_effect = Exception("Google API Error")
                    
                    response = client.post(
                        "/books/search",
                        json={"description": "I want action books"},
                        headers={"Authorization": "Bearer fake.token"}
                    )
                    
                    assert response.status_code == 500