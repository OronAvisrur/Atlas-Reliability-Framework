import httpx
from typing import Dict
from app.core.config import settings


class OllamaService:
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.timeout = settings.ollama_timeout
    
    async def extract_keywords(self, description: str) -> Dict[str, str]:
        prompt = f"Extract exactly 3 keywords from this book description: {description}. Return only 3 words separated by spaces."
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                data = response.json()
                keywords_text = data.get("response", "").strip()
                keywords_list = keywords_text.split()[:3]
                
                while len(keywords_list) < 3:
                    keywords_list.append("book")
                
                return {
                    "keyword_1": keywords_list[0],
                    "keyword_2": keywords_list[1],
                    "keyword_3": keywords_list[2]
                }
        
        except Exception as e:
            return {
                "keyword_1": "fiction",
                "keyword_2": "novel",
                "keyword_3": "book"
            }


ollama_service = OllamaService()