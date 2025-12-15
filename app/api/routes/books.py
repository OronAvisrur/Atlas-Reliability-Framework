from fastapi import APIRouter, HTTPException
from app.models.schemas import BookSearchRequest, BookSearchResponse, BookResult
from app.services.ollama_service import ollama_service
from app.services.google_books_service import google_books_service

router = APIRouter()


@router.post("/search", response_model=BookSearchResponse)
async def search_books(request: BookSearchRequest):
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
        
        return BookSearchResponse(
            total_items=result["total_items"],
            query_keywords=query_keywords,
            items=books
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))