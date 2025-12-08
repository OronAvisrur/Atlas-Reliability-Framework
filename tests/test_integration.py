import pytest
import httpx
from unittest.mock import patch, AsyncMock, MagicMock

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_full_movie_search_flow():
    mock_ollama = MagicMock()
    mock_ollama.json.return_value = {"response": "action thriller"}
    
    mock_imdb = MagicMock()
    mock_imdb.json.return_value = {
        "results": [
            {
                "id": "tt0468569",
                "title": "The Dark Knight",
                "description": "Batman fights Joker",
                "image": "http://image.jpg"
            }
        ]
    }
    
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = mock_client.return_value.__aenter__.return_value
        mock_instance.post = AsyncMock(return_value=mock_ollama)
        mock_instance.get = AsyncMock(return_value=mock_imdb)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/movies/search",
                json={"description": "intense action movie"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "query" in data
            assert "analysis" in data
            assert "movies" in data
            assert len(data["movies"]) > 0

@pytest.mark.asyncio
async def test_health_endpoint():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_metrics_endpoint():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/metrics")
        assert response.status_code == 200
        assert "http_requests_total" in response.text