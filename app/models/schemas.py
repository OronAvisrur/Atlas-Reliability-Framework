from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class HealthResponse(BaseModel):
    status: str


class ServiceInfoResponse(BaseModel):
    service: str
    timestamp: datetime
    version: str


class FailureResponse(BaseModel):
    status: str


class BookSearchRequest(BaseModel):
    description: str = Field(min_length=3, max_length=500)


class BookResult(BaseModel):
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    description: Optional[str] = None
    categories: Optional[List[str]] = None
    thumbnail: Optional[str] = None


class BookSearchResponse(BaseModel):
    total_items: int
    query_keywords: str
    items: List[BookResult]