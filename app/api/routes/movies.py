import time
from fastapi import APIRouter, HTTPException
from app.models.schemas import MovieSearchRequest, MovieSearchResponse
from app.core.metrics import record_request, record_request_duration
from app.services.ollama_service import ollama_service
from app.services.imdb_service import imdb_service

router = APIRouter()


@router.post("/search", response_model=MovieSearchResponse)
async def search_movies(request: MovieSearchRequest):
    start = time.time()
    
    try:
        keywords = await ollama_service.extract_keywords(request.description)
        movies = await imdb_service.search_movies(keywords)
        
        record_request("POST", "/movies/search", 200)
        record_request_duration("POST", "/movies/search", time.time() - start)
        
        return MovieSearchResponse(
            query=request.description,
            analysis=keywords,
            movies=movies
        )
    
    except Exception as e:
        record_request("POST", "/movies/search", 500)
        record_request_duration("POST", "/movies/search", time.time() - start)
        raise HTTPException(status_code=500, detail=str(e))