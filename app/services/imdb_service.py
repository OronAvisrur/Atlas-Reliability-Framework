import time
import httpx
from typing import List
from app.core.config import settings
from app.core.metrics import record_external_call, record_external_call_duration
from app.models.schemas import MovieResult


class IMDbService:
    def __init__(self):
        self.base_url = settings.imdb_base_url
        self.api_key = settings.imdb_api_key
        self.timeout = settings.imdb_timeout
    
    async def search_movies(self, keywords: str) -> List[MovieResult]:
        start = time.time()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/{self.api_key}/Search/{keywords}",
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                data = response.json()
                results = data.get("results", [])[:10]
                
                movies = [
                    MovieResult(
                        id=r.get("id", ""),
                        title=r.get("title", ""),
                        description=r.get("description", ""),
                        image=r.get("image", "")
                    )
                    for r in results
                ]
                
                record_external_call("imdb", "success")
                record_external_call_duration("imdb", time.time() - start)
                
                return movies
        
        except Exception as e:
            record_external_call("imdb", "failure")
            record_external_call_duration("imdb", time.time() - start)
            raise


imdb_service = IMDbService()