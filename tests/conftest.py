import pytest
from prometheus_client import REGISTRY

@pytest.fixture(autouse=True)
def reset_metrics():
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        try:
            REGISTRY.unregister(collector)
        except Exception:
            pass