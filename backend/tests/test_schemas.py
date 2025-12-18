import pytest
from datetime import datetime
from backend.models.schemas import (
    HealthResponse,
    ServiceInfoResponse,
    FailureResponse,
    BookSearchRequest,
    BookResult,
    BookSearchResponse
)


class TestHealthResponse:
    def test_health_response_creation(self):
        health = HealthResponse(status="healthy")
        
        assert health.status == "healthy"


class TestServiceInfoResponse:
    def test_service_info_response_creation(self):
        now = datetime.now()
        
        info = ServiceInfoResponse(
            service="test-service",
            timestamp=now,
            version="1.0.0"
        )
        
        assert info.service == "test-service"
        assert info.timestamp == now
        assert info.version == "1.0.0"


class TestFailureResponse:
    def test_failure_response_creation(self):
        failure = FailureResponse(status="failed")
        
        assert failure.status == "failed"


class TestBookSearchRequest:
    def test_valid_book_search_request(self):
        request = BookSearchRequest(
            description="I am looking for action books that has super heros and magic"
        )
        
        assert request.description == "I am looking for action books that has super heros and magic"
    
    def test_book_search_request_too_short_fails(self):
        with pytest.raises(ValueError):
            BookSearchRequest(description="ab")
    
    def test_book_search_request_too_long_fails(self):
        with pytest.raises(ValueError):
            BookSearchRequest(description="a" * 501)


class TestBookResult:
    def test_book_result_with_all_fields(self):
        book = BookResult(
            title="Test Book",
            authors=["Author One", "Author Two"],
            description="A test book description",
            categories=["Fiction", "Fantasy"],
            thumbnail="http://example.com/image.jpg"
        )
        
        assert book.title == "Test Book"
        assert book.authors == ["Author One", "Author Two"]
        assert book.description == "A test book description"
        assert book.categories == ["Fiction", "Fantasy"]
        assert book.thumbnail == "http://example.com/image.jpg"
    
    def test_book_result_with_optional_fields_none(self):
        book = BookResult()
        
        assert book.title is None
        assert book.authors is None
        assert book.description is None
        assert book.categories is None
        assert book.thumbnail is None


class TestBookSearchResponse:
    def test_book_search_response_creation(self):
        books = [
            BookResult(title="Book 1", authors=["Author 1"]),
            BookResult(title="Book 2", authors=["Author 2"])
        ]
        
        response = BookSearchResponse(
            total_items=2,
            query_keywords="action superhero magic",
            items=books
        )
        
        assert response.total_items == 2
        assert response.query_keywords == "action superhero magic"
        assert len(response.items) == 2
        assert response.items[0].title == "Book 1"
    
    def test_book_search_response_empty_items(self):
        response = BookSearchResponse(
            total_items=0,
            query_keywords="nonexistent words here",
            items=[]
        )
        
        assert response.total_items == 0
        assert len(response.items) == 0