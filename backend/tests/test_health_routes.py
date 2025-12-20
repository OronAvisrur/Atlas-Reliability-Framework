import pytest
from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.api.routes.health import router


app = FastAPI()
app.include_router(router)


@pytest.fixture
def client():
    return TestClient(app)


class TestHealthRoutes:
    def test_root(self, client):
        response = client.get("/")
        assert response.status_code in [200, 404]
    
    def test_health(self, client):
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_metrics(self, client):
        response = client.get("/metrics")
        
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]
        assert "charset=utf-8" in response.headers["content-type"]