import pytest
from unittest.mock import AsyncMock, patch
from app.services.ollama_service import OllamaService


class TestOllamaService:
    @pytest.mark.asyncio
    async def test_extract_keywords_success(self):
        service = OllamaService()
        mock_response = AsyncMock()
        mock_response.json.return_value = {"response": "action superhero movie"}
        mock_response.raise_for_status = AsyncMock()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await service.extract_keywords("action movie with superheroes")
            
            assert result == "action superhero movie"
    
    @pytest.mark.asyncio
    async def test_extract_keywords_failure(self):
        service = OllamaService()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(side_effect=Exception("Connection error"))
            
            with pytest.raises(Exception):
                await service.extract_keywords("test")