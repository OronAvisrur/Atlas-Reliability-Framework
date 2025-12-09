import pytest
from app.core.config import Settings


class TestSettings:
    def test_default_values(self):
        settings = Settings()
        
        assert settings.app_name == "Atlas Reliability Framework"
        assert settings.app_version == "1.0.0"
        assert settings.ollama_timeout == 30.0
    
    def test_custom_values(self):
        settings = Settings(app_name="Custom App")
        
        assert settings.app_name == "Custom App"