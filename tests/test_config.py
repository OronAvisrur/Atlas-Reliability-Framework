import pytest
from app.core.config import Settings


class TestSettings:
    def test_default_app_settings(self):
        settings = Settings()
        
        assert settings.app_name == "Atlas Reliability Framework"
        assert settings.app_version == "1.0.0"
    
    def test_default_ollama_settings(self):
        settings = Settings()
        
        assert settings.ollama_base_url == "http://localhost:11434"
        assert settings.ollama_model == "gemma3:270m"
        assert settings.ollama_timeout == 30.0
    
    def test_default_google_books_settings(self):
        settings = Settings()
        
        assert settings.google_books_base_url == "https://www.googleapis.com/books/v1/volumes"
        assert settings.google_books_timeout == 10.0
    
    def test_custom_ollama_timeout(self):
        settings = Settings(ollama_timeout=60.0)
        
        assert settings.ollama_timeout == 60.0
    
    def test_custom_google_books_timeout(self):
        settings = Settings(google_books_timeout=20.0)
        
        assert settings.google_books_timeout == 20.0