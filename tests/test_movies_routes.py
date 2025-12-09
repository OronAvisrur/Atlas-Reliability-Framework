import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import create_app
from app.models.schemas import MovieResult


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


class TestMoviesRoutes:
    def test_search_movies_success(self, client):
        mock_movies = [
            MovieResult(
                id="tt1234567",
                title="Test Movie",
                description="Test description",
                image="https://example.com/image.jpg"
            )
        ]
        
        with patch("app.services.ollama_service.ollama_service.extract_keywords", new_callable=AsyncMock) as mock_ollama:
            with patch("app.services.imdb_service.imdb_service.search_movies", new_callable=AsyncMock) as mock_imdb:
                mock_ollama.return_value = "action superhero"
                mock_imdb.return_value = mock_movies
                
                response = client.post(
                    "/movies/search",
                    json={"description": "action movie with superheroes"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["query"] == "action movie with superheroes"
                assert data["analysis"] == "action superhero"
                assert len(data["movies"]) == 1
    
    def test_search_movies_validation_error(self, client):
        response = client.post(
            "/movies/search",
            json={"description": "ab"}
        )
        
        assert response.status_code == 422
    
    def test_search_movies_service_error(self, client):
        with patch("app.services.ollama_service.ollama_service.extract_keywords", new_callable=AsyncMock) as mock_ollama:
            mock_ollama.side_effect = Exception("Service error")
            
            response = client.post(
                "/movies/search",
                json={"description": "action movie"}
            )
            
            assert response.status_code == 500