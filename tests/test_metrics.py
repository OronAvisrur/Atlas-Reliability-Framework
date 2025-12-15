import pytest
from app.core.metrics import (
    record_request,
    record_request_duration,
    record_external_call,
    record_external_call_duration,
    get_metrics
)


class TestMetrics:
    def test_record_request(self):
        record_request("GET", "/test", 200)
        metrics = get_metrics()
        
        assert b"http_requests_total" in metrics
        assert b'method="GET"' in metrics
        assert b'endpoint="/test"' in metrics
    
    def test_record_request_duration(self):
        record_request_duration("POST", "/test", 0.5)
        metrics = get_metrics()
        
        assert b"http_request_duration_seconds" in metrics
    
    def test_record_external_call(self):
        record_external_call("test_service", "success")
        metrics = get_metrics()
        
        assert b"external_api_calls_total" in metrics
        assert b'service="test_service"' in metrics
        assert b'status="success"' in metrics
    
    def test_get_metrics(self):
        record_request("GET", "/test", 200)
        metrics = get_metrics()
        
        assert isinstance(metrics, bytes)
        assert len(metrics) > 0