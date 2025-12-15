import time
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import BookSearchRequest, BookSearchResponse, BookResult
from app.services.ollama_service import ollama_service
from app.services.google_books_service import google_books_service
from app.core.metrics import record_request, record_request_duration
from app.db.models import User
from app.core.dependencies import get_current_user

router = APIRouter()


@router.post("/search", response_model=BookSearchResponse)
async def search_books(
    request: BookSearchRequest,
    current_user: User = Depends(get_current_user)
):
    start = time.time()
    
    try:
        keywords = await ollama_service.extract_keywords(request.description)
        
        result = await google_books_service.search_books(keywords)
        
        books = [
            BookResult(
                title=item.get("title"),
                authors=item.get("authors"),
                description=item.get("description"),
                categories=item.get("categories"),
                thumbnail=item.get("thumbnail")
            )
            for item in result["items"]
        ]
        
        query_keywords = f"{keywords['keyword_1']} {keywords['keyword_2']} {keywords['keyword_3']}"
        
        record_request("POST", "/books/search", 200)
        record_request_duration("POST", "/books/search", time.time() - start)
        
        return BookSearchResponse(
            total_items=result["total_items"],
            query_keywords=query_keywords,
            items=books
        )
    
    except Exception as e:
        record_request("POST", "/books/search", 500)
        record_request_duration("POST", "/books/search", time.time() - start)
        raise HTTPException(status_code=500, detail=str(e))