import pytest
from unittest.mock import AsyncMock, patch
from app.services.imdb_service import IMDbService


class TestIMDbService:
    @pytest.mark.asyncio
    async def test_search_movies_success(self):
        service = IMDbService()
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "results": [
                {
                    "id": "tt1234567",
                    "title": "Test Movie",
                    "description": "Test description",
                    "image": "https://example.com/image.jpg"
                }
            ]
        }
        mock_response.raise_for_status = AsyncMock()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
            
            result = await service.search_movies("action superhero")
            
            assert len(result) == 1
            assert result[0].title == "Test Movie"
    
    @pytest.mark.asyncio
    async def test_search_movies_failure(self):
        service = IMDbService()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(side_effect=Exception("API error"))
            
            with pytest.raises(Exception):
                await service.search_movies("test")