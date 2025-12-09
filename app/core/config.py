from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Atlas Reliability Framework"
    app_version: str = "1.0.0"
    
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma3:270m"
    ollama_timeout: float = 30.0
    
    imdb_api_key: str = "k_12345678"
    imdb_base_url: str = "https://imdb-api.com"
    imdb_timeout: float = 10.0
    
    class Config:
        env_file = ".env"


settings = Settings()