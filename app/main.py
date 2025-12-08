from fastapi import FastAPI, HTTPException, Response
from datetime import datetime
import random
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="Atlas Reliability Service")

request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)


@app.get("/")
async def root():
    request_count.labels(method='GET', endpoint='/', status='200').inc()
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    request_count.labels(method='GET', endpoint='/health', status='200').inc()
    return {"status": "healthy"}


@app.get("/data")
async def get_data():
    request_count.labels(method='GET', endpoint='/data', status='200').inc()
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "data": [
            {"id": 1, "name": "Service A", "status": "running"},
            {"id": 2, "name": "Service B", "status": "running"},
            {"id": 3, "name": "Service C", "status": "running"}
        ],
        "total_count": 3
    }


@app.get("/fail")
async def unstable_endpoint():
    failure_chance = random.random()
    
    if failure_chance < 0.3:
        request_count.labels(method='GET', endpoint='/fail', status='500').inc()
        raise HTTPException(status_code=500, detail="Simulated service failure")
    elif failure_chance < 0.5:
        import time
        time.sleep(2)
        request_count.labels(method='GET', endpoint='/fail', status='200').inc()
        return {"status": "slow_response", "message": "High latency simulation"}
    else:
        request_count.labels(method='GET', endpoint='/fail', status='200').inc()
        return {"status": "success", "message": "Request processed normally"}


@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)