import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


class TestHealthRoutes:
    def test_root(self, client):
        response = client.get("/")
        
        assert response.status_code == 200
        assert response.json() == {"message": "Atlas Reliability Framework"}
    
    def test_health(self, client):
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    def test_metrics(self, client):
        response = client.get("/metrics")
        
        assert response.status_code == 200
        assert "http_requests_total" in response.text