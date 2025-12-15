import pytest
from datetime import datetime
from app.models.schemas import (
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
            keyword_1="action",
            keyword_2="superhero",
            keyword_3="comics"
        )
        
        assert request.keyword_1 == "action"
        assert request.keyword_2 == "superhero"
        assert request.keyword_3 == "comics"
    
    def test_book_search_request_empty_keyword_fails(self):
        with pytest.raises(ValueError):
            BookSearchRequest(
                keyword_1="",
                keyword_2="superhero",
                keyword_3="comics"
            )
    
    def test_book_search_request_too_long_keyword_fails(self):
        with pytest.raises(ValueError):
            BookSearchRequest(
                keyword_1="a" * 101,
                keyword_2="superhero",
                keyword_3="comics"
            )


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
            query_keywords="action superhero comics",
            items=books
        )
        
        assert response.total_items == 2
        assert response.query_keywords == "action superhero comics"
        assert len(response.items) == 2
        assert response.items[0].title == "Book 1"
    
    def test_book_search_response_empty_items(self):
        response = BookSearchResponse(
            total_items=0,
            query_keywords="nonexistent",
            items=[]
        )
        
        assert response.total_items == 0
        assert len(response.items) == 0