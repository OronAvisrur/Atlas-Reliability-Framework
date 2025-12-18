import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from backend.services.google_books_service import GoogleBooksService


@pytest.fixture
def service():
    return GoogleBooksService()


@pytest.fixture
def mock_api_response():
    return {
        "totalItems": 100,
        "items": [
            {
                "volumeInfo": {
                    "title": "Book 1",
                    "authors": ["Author 1"],
                    "description": "Description 1",
                    "categories": ["Fiction"],
                    "imageLinks": {"thumbnail": "http://example.com/1.jpg"}
                }
            },
            {
                "volumeInfo": {
                    "title": "Book 2",
                    "authors": ["Author 2"],
                    "description": "Description 2",
                    "categories": ["Science"],
                    "imageLinks": {"thumbnail": "http://example.com/2.jpg"}
                }
            }
        ]
    }


class TestGoogleBooksService:
    @pytest.mark.asyncio
    async def test_search_books_returns_json(self, service, mock_api_response):
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
            
            keywords = {"keyword_1": "action", "keyword_2": "superhero", "keyword_3": "comics"}
            result = await service.search_books(keywords)
            
            assert result["total_items"] == 100
            assert len(result["items"]) == 2
            assert result["items"][0]["title"] == "Book 1"
            assert result["items"][0]["authors"] == ["Author 1"]
    
    @pytest.mark.asyncio
    async def test_search_books_empty_results(self, service):
        mock_response = MagicMock()
        mock_response.json.return_value = {"totalItems": 0, "items": []}
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
            
            keywords = {"keyword_1": "xyz", "keyword_2": "abc", "keyword_3": "def"}
            result = await service.search_books(keywords)
            
            assert result["total_items"] == 0
            assert result["items"] == []
    
    @pytest.mark.asyncio
    async def test_search_books_builds_query_correctly(self, service, mock_api_response):
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_get = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__.return_value.get = mock_get
            
            keywords = {"keyword_1": "action", "keyword_2": "superhero", "keyword_3": "comics"}
            await service.search_books(keywords)
            
            call_args = mock_get.call_args
            assert call_args.kwargs["params"]["q"] == "action+superhero+comics"
            assert call_args.kwargs["params"]["maxResults"] == 10
    
    @pytest.mark.asyncio
    async def test_search_books_handles_missing_fields(self, service):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "totalItems": 1,
            "items": [{"volumeInfo": {"title": "Incomplete Book"}}]
        }
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
            
            keywords = {"keyword_1": "test", "keyword_2": "book", "keyword_3": "search"}
            result = await service.search_books(keywords)
            
            assert result["items"][0]["title"] == "Incomplete Book"
            assert result["items"][0]["authors"] is None
            assert result["items"][0]["description"] is None