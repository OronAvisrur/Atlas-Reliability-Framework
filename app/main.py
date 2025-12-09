from fastapi import FastAPI
from app.api.routes import health, movies
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version
    )
    
    app.include_router(health.router, tags=["Health"])
    app.include_router(movies.router, prefix="/movies", tags=["Movies"])
    
    return app


app = create_app()