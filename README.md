# Atlas Reliability Framework

FastAPI service with Ollama LLM integration for movie recommendations, deployed on Kubernetes with high availability and monitoring.

## Architecture

- **FastAPI** - REST API server
- **Ollama (llama3.2)** - LLM for extracting search keywords
- **IMDb API** - Movie database search
- **Prometheus** - Metrics collection
- **Kubernetes** - Container orchestration with 3 replicas

## Prerequisites

- Python 3.11+
- Docker
- K3s
- Ansible

## Quick Start

### Setup Infrastructure
```bash
cd ansible
ansible-playbook playbooks/setup-infrastructure.yml
```

### Deploy Application
```bash
ansible-playbook playbooks/deploy-application.yml
```

### Access Service
```bash
curl http://localhost:30080/health
```

## API Endpoints

### GET /health
Health check endpoint
```bash
curl http://localhost:30080/health
```

### GET /data
Service information
```bash
curl http://localhost:30080/data
```

### POST /movies/search
Search movies using natural language
```bash
curl -X POST http://localhost:30080/movies/search \
  -H "Content-Type: application/json" \
  -d '{"description": "exciting sci-fi movie with time travel"}'
```

### GET /fail
Simulate failures (30% error rate, 20% latency)
```bash
curl http://localhost:30080/fail
```

### GET /metrics
Prometheus metrics
```bash
curl http://localhost:30080/metrics
```

## Testing
```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio pyyaml
pytest
```

## How It Works

1. User sends movie description to `/movies/search`
2. Ollama (llama3.2) extracts search keywords
3. Keywords sent to IMDb API
4. Top 10 results returned to user

## Monitoring

- Prometheus metrics exposed at `/metrics`
- Kubernetes liveness/readiness probes on `/health`
- Self-healing: pods restart on probe failures

## High Availability

- 3 replicas for fault tolerance
- Ollama sidecar in each pod
- Automatic failover on pod failure