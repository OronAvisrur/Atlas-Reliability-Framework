# Atlas Reliability Framework

FastAPI service with Ollama LLM integration for book search, deployed on Kubernetes with high availability and monitoring.

## Architecture

- **FastAPI** - REST API with clean architecture
- **Ollama (gemma3:270m)** - LLM for keyword extraction
- **Google Books API** - Book database search
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

### GET /health
Health check for Kubernetes probes

### GET /info
Service information with version and timestamp

### GET /metrics
Prometheus metrics

### GET /fail
Simulated failure endpoint for testing self-healing

### POST /books/search
Search books using natural language description
```bash
curl -X POST http://localhost:30080/books/search \
  -H "Content-Type: application/json" \
  -d '{"description": "I am looking for action books that has super heroes and magic"}'
```

**Response:**
```json
{
  "total_items": 1254,
  "query_keywords": "action superhero magic",
  "items": [
    {
      "title": "Book Title",
      "authors": ["Author Name"],
      "description": "Book description...",
      "categories": ["Fiction", "Fantasy"],
      "thumbnail": "http://example.com/image.jpg"
    }
  ]
}
```

## Testing
```bash
pytest tests/
```

## How It Works

1. User sends book description to `/books/search`
2. Ollama extracts 3 search keywords from description
3. Keywords sent to Google Books API
4. Top 10 results returned

## Monitoring

- Prometheus metrics at `/metrics`
- Kubernetes liveness/readiness probes
- Request count, latency, and external API metrics

## High Availability

- 3 replicas for fault tolerance
- Ollama sidecar in each pod
- Automatic restart on health check failure

## Metrics Exposed

- `http_requests_total` - Total HTTP requests by method, endpoint, status
- `http_request_duration_seconds` - HTTP request latency
- `external_api_calls_total` - External API calls by service and status
- `external_api_duration_seconds` - External API call duration