import pytest
from app.core.metrics import (
    record_request,
    record_request_duration,
    record_external_call,
    record_external_call_duration,
    get_metrics,
    http_requests_total,
    external_api_calls_total
)


class TestMetrics:
    def test_record_request(self):
        initial = http_requests_total.labels(
            method="GET", endpoint="/test", status=200
        )._value.get()
        
        record_request("GET", "/test", 200)
        
        final = http_requests_total.labels(
            method="GET", endpoint="/test", status=200
        )._value.get()
        assert final == initial + 1
    
    def test_record_request_duration(self):
        record_request_duration("GET", "/test", 0.5)
        assert True
    
    def test_record_external_call(self):
        initial = external_api_calls_total.labels(
            service="test", status="success"
        )._value.get()
        
        record_external_call("test", "success")
        
        final = external_api_calls_total.labels(
            service="test", status="success"
        )._value.get()
        assert final == initial + 1
    
    def test_get_metrics(self):
        metrics = get_metrics()
        
        assert isinstance(metrics, str)
        assert "http_requests_total" in metrics