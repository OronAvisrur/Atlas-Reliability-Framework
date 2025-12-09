import time
import httpx
from app.core.config import settings
from app.core.metrics import record_external_call, record_external_call_duration


class OllamaService:
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.timeout = settings.ollama_timeout
    
    async def extract_keywords(self, description: str) -> str:
        start = time.time()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": f"Extract 3-5 keywords for searching movies: {description}. Return only keywords separated by spaces.",
                        "stream": False
                    },
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                data = response.json()
                keywords = data.get("response", "").strip()
                
                record_external_call("ollama", "success")
                record_external_call_duration("ollama", time.time() - start)
                
                return keywords
        
        except Exception as e:
            record_external_call("ollama", "failure")
            record_external_call_duration("ollama", time.time() - start)
            raise


ollama_service = OllamaService()