import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.routes.books import router


app = FastAPI()
app.include_router(router)
client = TestClient(app)


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
    def test_search_books_success(self, mock_google_books_result):
        with patch("app.api.routes.books.google_books_service.search_books", new_callable=AsyncMock) as mock_search:
            mock_search.return_value = mock_google_books_result
            
            response = client.post(
                "/search",
                json={
                    "keyword_1": "action",
                    "keyword_2": "superhero",
                    "keyword_3": "comics"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_items"] == 50
            assert data["query_keywords"] == "action superhero comics"
            assert len(data["items"]) == 2
            assert data["items"][0]["title"] == "Book 1"
    
    def test_search_books_empty_results(self):
        with patch("app.api.routes.books.google_books_service.search_books", new_callable=AsyncMock) as mock_search:
            mock_search.return_value = {"total_items": 0, "items": []}
            
            response = client.post(
                "/search",
                json={
                    "keyword_1": "xyz",
                    "keyword_2": "abc",
                    "keyword_3": "def"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_items"] == 0
            assert len(data["items"]) == 0
    
    def test_search_books_invalid_request_empty_keyword(self):
        response = client.post(
            "/search",
            json={
                "keyword_1": "",
                "keyword_2": "superhero",
                "keyword_3": "comics"
            }
        )
        
        assert response.status_code == 422
    
    def test_search_books_service_error(self):
        with patch("app.api.routes.books.google_books_service.search_books", new_callable=AsyncMock) as mock_search:
            mock_search.side_effect = Exception("API Error")
            
            response = client.post(
                "/search",
                json={
                    "keyword_1": "action",
                    "keyword_2": "superhero",
                    "keyword_3": "comics"
                }
            )
            
            assert response.status_code == 500
            assert "API Error" in response.json()["detail"]
    
    def test_search_books_missing_keyword(self):
        response = client.post(
            "/search",
            json={
                "keyword_1": "action",
                "keyword_2": "superhero"
            }
        )
        
        assert response.status_code == 422