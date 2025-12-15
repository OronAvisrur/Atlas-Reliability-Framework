from fastapi import FastAPI
from app.api.routes import health, books, auth
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version
    )
    
    app.include_router(health.router, tags=["Health"])
    app.include_router(books.router, prefix="/books", tags=["Books"])
    app.include_router(auth.router, tags=["Authentication"])
    
    return app


app = create_app()