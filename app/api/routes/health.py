from fastapi import APIRouter, Response
from app.models.schemas import HealthResponse
from app.core.metrics import record_request, get_metrics

router = APIRouter()


@router.get("/", response_model=dict)
async def root():
    record_request("GET", "/", 200)
    return {"message": "Atlas Reliability Framework"}


@router.get("/health", response_model=HealthResponse)
async def health():
    record_request("GET", "/health", 200)
    return HealthResponse(status="healthy")


@router.get("/metrics")
async def metrics():
    return Response(content=get_metrics(), media_type="text/plain; charset=utf-8")