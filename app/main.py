from fastapi import FastAPI, HTTPException
from datetime import datetime
import random

app = FastAPI(title="Atlas Reliability Service")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/data")
async def get_data():
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
        raise HTTPException(status_code=500, detail="Simulated service failure")
    elif failure_chance < 0.5:
        import time
        time.sleep(2)
        return {"status": "slow_response", "message": "High latency simulation"}
    else:
        return {"status": "success", "message": "Request processed normally"}