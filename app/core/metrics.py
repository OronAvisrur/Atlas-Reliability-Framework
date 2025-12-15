from prometheus_client import Counter, Histogram, Gauge, generate_latest
from typing import Literal


http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"]
)

active_requests = Gauge(
    "active_requests",
    "Number of active requests",
    ["endpoint"]
)

external_api_calls_total = Counter(
    "external_api_calls_total",
    "Total external API calls",
    ["service", "status"]
)

external_api_duration_seconds = Histogram(
    "external_api_duration_seconds",
    "External API call duration",
    ["service"]
)


def record_request(method: str, endpoint: str, status: int) -> None:
    http_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()


def record_request_duration(method: str, endpoint: str, duration: float) -> None:
    http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)


def record_external_call(service: str, status: Literal["success", "failure"]) -> None:
    external_api_calls_total.labels(service=service, status=status).inc()


def record_external_call_duration(service: str, duration: float) -> None:
    external_api_duration_seconds.labels(service=service).observe(duration)


def get_metrics() -> bytes:
    return generate_latest()