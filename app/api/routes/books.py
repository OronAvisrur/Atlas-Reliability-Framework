import time
from fastapi import APIRouter, HTTPException
from app.models.schemas import BookSearchRequest, BookSearchResponse, BookResult
from app.services.google_books_service import google_books_service

router = APIRouter()


@router.post("/search", response_model=BookSearchResponse)
async def search_books(request: BookSearchRequest):
    start = time.time()
    
    try:
        keywords = {
            "keyword_1": request.keyword_1,
            "keyword_2": request.keyword_2,
            "keyword_3": request.keyword_3
        }
        
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
        
        return BookSearchResponse(
            total_items=result["total_items"],
            query_keywords=f"{request.keyword_1} {request.keyword_2} {request.keyword_3}",
            items=books
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))