import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.routes.books import router


app = FastAPI()
app.include_router(router)
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


class TestBooksRouter:
    def test_search_books_success(self, mock_keywords, mock_google_books_result):
        with patch("app.api.routes.books.ollama_service.extract_keywords", new_callable=AsyncMock) as mock_ollama:
            with patch("app.api.routes.books.google_books_service.search_books", new_callable=AsyncMock) as mock_google:
                mock_ollama.return_value = mock_keywords
                mock_google.return_value = mock_google_books_result
                
                response = client.post(
                    "/search",
                    json={"description": "I am looking for action books with superheroes and magic"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["total_items"] == 50
                assert data["query_keywords"] == "action superhero magic"
                assert len(data["items"]) == 2
                assert data["items"][0]["title"] == "Book 1"
    
    def test_search_books_empty_results(self, mock_keywords):
        with patch("app.api.routes.books.ollama_service.extract_keywords", new_callable=AsyncMock) as mock_ollama:
            with patch("app.api.routes.books.google_books_service.search_books", new_callable=AsyncMock) as mock_google:
                mock_ollama.return_value = mock_keywords
                mock_google.return_value = {"total_items": 0, "items": []}
                
                response = client.post(
                    "/search",
                    json={"description": "Some random description"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["total_items"] == 0
                assert len(data["items"]) == 0
    
    def test_search_books_invalid_request_too_short(self):
        response = client.post(
            "/search",
            json={"description": "ab"}
        )
        
        assert response.status_code == 422
    
    def test_search_books_ollama_error(self):
        with patch("app.api.routes.books.ollama_service.extract_keywords", new_callable=AsyncMock) as mock_ollama:
            mock_ollama.side_effect = Exception("Ollama Error")
            
            response = client.post(
                "/search",
                json={"description": "I want action books"}
            )
            
            assert response.status_code == 500
            assert "Ollama Error" in response.json()["detail"]
    
    def test_search_books_google_error(self, mock_keywords):
        with patch("app.api.routes.books.ollama_service.extract_keywords", new_callable=AsyncMock) as mock_ollama:
            with patch("app.api.routes.books.google_books_service.search_books", new_callable=AsyncMock) as mock_google:
                mock_ollama.return_value = mock_keywords
                mock_google.side_effect = Exception("Google API Error")
                
                response = client.post(
                    "/search",
                    json={"description": "I want action books"}
                )
                
                assert response.status_code == 500
                assert "Google API Error" in response.json()["detail"]