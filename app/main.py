import random
import time
from datetime import datetime
from typing import Dict, List

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest

app = FastAPI(title="Atlas Reliability Framework")

REQUEST_COUNT = Counter("http_requests_total", "Total requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["method", "endpoint"])

IMDB_API_KEY = "k_12345678"
IMDB_BASE_URL = "https://imdb-api.com"
OLLAMA_BASE_URL = "http://localhost:11434"

class MovieRequest(BaseModel):
    description: str

class MovieResult(BaseModel):
    id: str
    title: str
    description: str
    image: str

class MovieResponse(BaseModel):
    query: str
    analysis: str
    movies: List[MovieResult]

@app.get("/")
async def root():
    REQUEST_COUNT.labels(method="GET", endpoint="/", status=200).inc()
    return {"message": "Atlas Reliability Framework"}

@app.get("/health")
async def health():
    REQUEST_COUNT.labels(method="GET", endpoint="/health", status=200).inc()
    return {"status": "healthy"}

@app.get("/data")
async def get_data():
    REQUEST_COUNT.labels(method="GET", endpoint="/data", status=200).inc()
    data = {
        "service": "atlas-reliability-framework",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
    return data

@app.get("/fail")
async def fail():
    rand = random.random()
    if rand < 0.3:
        REQUEST_COUNT.labels(method="GET", endpoint="/fail", status=500).inc()
        raise HTTPException(status_code=500, detail="Simulated failure")
    elif rand < 0.5:
        time.sleep(5)
    REQUEST_COUNT.labels(method="GET", endpoint="/fail", status=200).inc()
    return {"status": "ok"}

@app.get("/metrics")
async def metrics():
    return generate_latest().decode("utf-8")

@app.post("/movies/search", response_model=MovieResponse)
async def search_movies(request: MovieRequest):
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient() as client:
            ollama_response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": "gemma3:270m",
                    "prompt": f"Extract 3-5 keywords for searching movies based on: {request.description}. Return only keywords separated by spaces.",
                    "stream": False
                },
                timeout=30.0
            )
            ollama_data = ollama_response.json()
            keywords = ollama_data.get("response", "").strip()
            
            imdb_response = await client.get(
                f"{IMDB_BASE_URL}/{IMDB_API_KEY}/Search/{keywords}",
                timeout=10.0
            )
            imdb_data = imdb_response.json()
            
            results = imdb_data.get("results", [])[:10]
            movies = [
                MovieResult(
                    id=r.get("id", ""),
                    title=r.get("title", ""),
                    description=r.get("description", ""),
                    image=r.get("image", "")
                )
                for r in results
            ]
            
            REQUEST_COUNT.labels(method="POST", endpoint="/movies/search", status=200).inc()
            REQUEST_LATENCY.labels(method="POST", endpoint="/movies/search").observe(time.time() - start_time)
            
            return MovieResponse(
                query=request.description,
                analysis=keywords,
                movies=movies
            )
    except Exception as e:
        REQUEST_COUNT.labels(method="POST", endpoint="/movies/search", status=500).inc()
        raise HTTPException(status_code=500, detail=str(e))