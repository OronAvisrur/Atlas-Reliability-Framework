import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.ollama_service import OllamaService


@pytest.fixture
def service():
    return OllamaService()


class TestOllamaService:
    @pytest.mark.asyncio
    async def test_extract_keywords_success(self, service):
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "fantasy adventure magic"}
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await service.extract_keywords("A book about wizards and dragons")
            
            assert result["keyword_1"] == "fantasy"
            assert result["keyword_2"] == "adventure"
            assert result["keyword_3"] == "magic"
    
    @pytest.mark.asyncio
    async def test_extract_keywords_pads_if_less_than_three(self, service):
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "science"}
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await service.extract_keywords("Science book")
            
            assert result["keyword_1"] == "science"
            assert result["keyword_2"] == "book"
            assert result["keyword_3"] == "book"
    
    @pytest.mark.asyncio
    async def test_extract_keywords_takes_first_three_if_more(self, service):
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "action adventure thriller mystery suspense"}
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await service.extract_keywords("Action packed thriller")
            
            assert result["keyword_1"] == "action"
            assert result["keyword_2"] == "adventure"
            assert result["keyword_3"] == "thriller"
    
    @pytest.mark.asyncio
    async def test_extract_keywords_fallback_on_error(self, service):
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(side_effect=Exception("API Error"))
            
            result = await service.extract_keywords("Any description")
            
            assert result["keyword_1"] == "fiction"
            assert result["keyword_2"] == "novel"
            assert result["keyword_3"] == "book"
    
    @pytest.mark.asyncio
    async def test_extract_keywords_builds_correct_prompt(self, service):
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "test words here"}
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__.return_value.post = mock_post
            
            await service.extract_keywords("A fantasy book")
            
            call_args = mock_post.call_args
            json_data = call_args.kwargs["json"]
            assert "A fantasy book" in json_data["prompt"]
            assert json_data["model"] == "gemma3:270m"
            assert json_data["stream"] is False