from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Atlas Reliability Framework"
    app_version: str = "1.0.0"
    
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma3:270m"
    ollama_timeout: float = 30.0
    
    google_books_base_url: str = "https://www.googleapis.com/books/v1/volumes"
    google_books_timeout: float = 10.0
    
    class Config:
        env_file = ".env"


settings = Settings()