import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.schemas import (
    HealthResponse,
    ServiceInfoResponse,
    MovieSearchRequest,
    MovieResult,
    MovieSearchResponse
)


class TestHealthResponse:
    def test_valid_response(self):
        response = HealthResponse(status="healthy")
        
        assert response.status == "healthy"


class TestMovieSearchRequest:
    def test_valid_request(self):
        request = MovieSearchRequest(description="action movie")
        
        assert request.description == "action movie"
    
    def test_too_short_description(self):
        with pytest.raises(ValidationError):
            MovieSearchRequest(description="ab")
    
    def test_too_long_description(self):
        with pytest.raises(ValidationError):
            MovieSearchRequest(description="a" * 501)


class TestMovieSearchResponse:
    def test_valid_response(self):
        movies = [
            MovieResult(
                id="tt1234567",
                title="Test Movie",
                description="Test description",
                image="https://example.com/image.jpg"
            )
        ]
        
        response = MovieSearchResponse(
            query="action movie",
            analysis="action superhero",
            movies=movies
        )
        
        assert response.query == "action movie"
        assert len(response.movies) == 1