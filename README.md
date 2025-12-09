# Atlas Reliability Framework

FastAPI service with Ollama LLM integration for movie search, deployed on Kubernetes with high availability and monitoring.

## Architecture

- **FastAPI** - REST API with clean architecture
- **Ollama (gemma3:270m)** - LLM for keyword extraction
- **IMDb API** - Movie database search
- **Prometheus** - Metrics collection
- **Kubernetes (K3s)** - Container orchestration with 3 replicas

## Project Structure
```
app/
├── api/routes/     # HTTP endpoints
├── core/           # Config & metrics
├── models/         # Pydantic schemas
└── services/       # Business logic
```

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

### GET /
Root endpoint

### GET /health
Health check for Kubernetes probes

### GET /metrics
Prometheus metrics

### POST /movies/search
Search movies using natural language
```bash
curl -X POST http://localhost:30080/movies/search \
  -H "Content-Type: application/json" \
  -d '{"description": "action movie with superheroes"}'
```

## Testing
```bash
pytest tests/
```

## How It Works

1. User sends movie description to `/movies/search`
2. Ollama extracts search keywords from description
3. Keywords sent to IMDb API
4. Top 10 results returned

## Monitoring

- Prometheus metrics at `/metrics`
- Kubernetes liveness/readiness probes
- Request count, latency, and external API metrics

## High Availability

- 3 replicas for fault tolerance
- Ollama sidecar in each pod
- Automatic restart on health check failure