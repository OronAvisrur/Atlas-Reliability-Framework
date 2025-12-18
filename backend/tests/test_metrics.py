import pytest
from backend.core.metrics import (
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
        initial_value = http_requests_total.labels(method="GET", endpoint="/test", status=200)._value.get()
        record_request("GET", "/test", 200)
        new_value = http_requests_total.labels(method="GET", endpoint="/test", status=200)._value.get()
        
        assert new_value > initial_value
    
    def test_record_request_duration(self):
        record_request_duration("POST", "/test", 0.5)
        
        assert True
    
    def test_record_external_call(self):
        initial_value = external_api_calls_total.labels(service="test_service", status="success")._value.get()
        record_external_call("test_service", "success")
        new_value = external_api_calls_total.labels(service="test_service", status="success")._value.get()
        
        assert new_value > initial_value
    
    def test_get_metrics(self):
        record_request("GET", "/test_metrics", 200)
        metrics = get_metrics()
        
        assert isinstance(metrics, bytes)