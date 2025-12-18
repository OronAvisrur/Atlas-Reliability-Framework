import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.core.dependencies import get_current_user

client = TestClient(app)


class TestMainApp:
    
    def test_app_created_successfully(self):
        assert app is not None
        assert app.title == "Atlas Reliability Framework"
        assert app.version == "1.0.0"
    
    def test_health_endpoint_registered(self):
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_books_endpoint_registered(self):
        mock_user = {"id": 1, "username": "testuser", "is_active": True}
        app.dependency_overrides[get_current_user] = lambda: mock_user
        try:
            response = client.post(
                "/books/search",
                json={"description": "test book search"}
            )
            assert response.status_code in [200, 500]
        finally:
            app.dependency_overrides = {}
    
    def test_openapi_docs_available(self):
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_openapi_schema_available(self):
        response = client.get("/openapi.json")
        assert response.status_code == 200