import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Atlas Reliability Framework"}

def test_health():
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_data():
    response = client.get("/data")
    
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "atlas-reliability-framework"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"

def test_fail_success():
    with patch("random.random", return_value=0.6):
        response = client.get("/fail")
        
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

def test_fail_error():
    with patch("random.random", return_value=0.1):
        response = client.get("/fail")
        
        assert response.status_code == 500
        assert "Simulated failure" in response.json()["detail"]

def test_metrics():
    response = client.get("/metrics")
    
    assert response.status_code == 200
    assert "http_requests_total" in response.text

@pytest.mark.asyncio
async def test_search_movies():
    mock_ollama = MagicMock()
    mock_ollama.json.return_value = {"response": "action adventure"}
    
    mock_imdb = MagicMock()
    mock_imdb.json.return_value = {
        "results": [
            {
                "id": "tt1234567",
                "title": "Test Movie",
                "description": "Action movie",
                "image": "http://test.jpg"
            }
        ]
    }
    
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = mock_client.return_value.__aenter__.return_value
        mock_instance.post = AsyncMock(return_value=mock_ollama)
        mock_instance.get = AsyncMock(return_value=mock_imdb)
        
        response = client.post("/movies/search", json={"description": "exciting action movie"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "exciting action movie"
        assert data["analysis"] == "action adventure"
        assert len(data["movies"]) == 1
        assert data["movies"][0]["title"] == "Test Movie"

@pytest.mark.asyncio
async def test_search_movies_error():
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = mock_client.return_value.__aenter__.return_value
        mock_instance.post = AsyncMock(side_effect=Exception("Ollama error"))
        
        response = client.post("/movies/search", json={"description": "test"})
        
        assert response.status_code == 500