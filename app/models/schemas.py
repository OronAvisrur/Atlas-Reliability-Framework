from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class HealthResponse(BaseModel):
    status: str


class ServiceInfoResponse(BaseModel):
    service: str
    timestamp: datetime
    version: str


class FailureResponse(BaseModel):
    status: str


class MovieSearchRequest(BaseModel):
    description: str = Field(min_length=3, max_length=500)


class MovieResult(BaseModel):
    id: str
    title: str
    description: str
    image: str


class MovieSearchResponse(BaseModel):
    query: str
    analysis: str
    movies: List[MovieResult]