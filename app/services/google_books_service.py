import httpx
from typing import Dict, List


class GoogleBooksService:
    def __init__(self):
        self.base_url = "https://www.googleapis.com/books/v1/volumes"
        self.timeout = 10.0
    
    async def search_books(self, keywords: Dict[str, str]) -> Dict:
        query = "+".join(keywords.values())
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.base_url,
                params={
                    "q": query,
                    "maxResults": 10,
                    "printType": "books"
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            total_items = data.get("totalItems", 0)
            items = data.get("items", [])
            
            books = []
            for item in items:
                volume_info = item.get("volumeInfo", {})
                image_links = volume_info.get("imageLinks", {}) or {}
                
                books.append({
                    "title": volume_info.get("title"),
                    "authors": volume_info.get("authors"),
                    "description": volume_info.get("description"),
                    "categories": volume_info.get("categories"),
                    "thumbnail": image_links.get("thumbnail")
                })
            
            return {
                "total_items": total_items,
                "items": books
            }


google_books_service = GoogleBooksService()