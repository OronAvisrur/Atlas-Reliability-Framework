# Atlas Reliability Framework

FastAPI service with PostgreSQL authentication, Ollama LLM integration for book search, deployed on Kubernetes with high availability and monitoring.

## Architecture

- **FastAPI** - REST API with clean architecture
- **PostgreSQL** - User authentication database
- **JWT** - Token-based authentication
- **Ollama (gemma3:270m)** - LLM for keyword extraction
- **Google Books API** - Book database search
- **Prometheus** - Metrics collection
- **Kubernetes (K3s)** - Container orchestration with 3 replicas
- **Ansible** - Infrastructure automation

## Project Structure
```
atlas-reliability-framework/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── books.py         # Book search endpoints
│   │       └── health.py        # Health check endpoints
│   ├── core/
│   │   ├── config.py            # Application settings
│   │   ├── dependencies.py      # JWT authentication dependency
│   │   ├── metrics.py           # Prometheus metrics
│   │   └── security.py          # Password hashing & JWT utils
│   ├── db/
│   │   ├── database.py          # PostgreSQL connection management
│   │   └── schema.sql           # Database schema
│   ├── models/
│   │   ├── auth_schemas.py      # Authentication Pydantic models
│   │   └── schemas.py           # Book search Pydantic models
│   └── services/
│       ├── auth_service.py      # Authentication business logic
│       ├── google_books_service.py
│       └── ollama_service.py
├── ansible/
│   ├── k8s/
│   │   ├── deployment.yaml              # Application deployment
│   │   ├── service.yaml                 # Application service
│   │   ├── postgres-secrets.yaml        # PostgreSQL credentials
│   │   ├── postgres-statefulset.yaml    # PostgreSQL StatefulSet
│   │   ├── postgres-service.yaml        # PostgreSQL service
│   │   └── db-schema-configmap.yaml     # Database schema ConfigMap
│   ├── playbooks/
│   │   ├── setup-infrastructure.yml     # K3s setup
│   │   ├── setup-postgres.yml           # PostgreSQL deployment
│   │   └── deploy-application.yml       # Application deployment
│   ├── group_vars/
│   ├── inventory/
│   └── ansible.cfg
├── tests/                       # Pytest test suite
├── Dockerfile                   # Container image definition
└── pytest.ini                   # Pytest configuration
```

## Prerequisites

- Python 3.11+
- Docker
- K3s
- Ansible
- kubectl

## Quick Start

### 1. Setup PostgreSQL
```bash
cd ansible
ansible-playbook playbooks/setup-postgres.yml
```

### 2. Deploy Application
```bash
ansible-playbook playbooks/deploy-application.yml
```

### 3. Verify Deployment
```bash
kubectl get pods
# Expected: postgres-0 (1/1 Running) + atlas-service-xxx (2/2 Running, 3 replicas)

curl http://localhost:30080/health
# Expected: {"status":"healthy"}
```

## Authentication Flow

### 1. Register User
```bash
curl -X POST http://localhost:30080/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "myuser",
    "password": "mypass123"
  }'
```

**Response:**
```json
{
  "id": 1,
  "username": "myuser",
  "is_active": true
}
```

### 2. Login
```bash
curl -X POST http://localhost:30080/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "myuser",
    "password": "mypass123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Use Protected Endpoints
Save the `access_token` from login response and use it in subsequent requests.

## API Endpoints

### Public Endpoints

#### GET /
Root endpoint

#### GET /health
Health check for Kubernetes probes

#### GET /info
Service information with version and timestamp

#### GET /metrics
Prometheus metrics endpoint

#### GET /fail
Simulated failure endpoint for testing self-healing

#### POST /auth/register
Register a new user
- **Request Body:** `{"username": "string", "password": "string"}`
- **Validation:** Username min 3 chars, password min 6 chars
- **Response:** User object with id, username, is_active

#### POST /auth/login
Login and receive JWT token
- **Request Body:** `{"username": "string", "password": "string"}`
- **Response:** `{"access_token": "string", "token_type": "bearer"}`

### Protected Endpoints (Require JWT)

#### POST /books/search
Search books using natural language description (requires authentication)
```bash
curl -X POST http://localhost:30080/books/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "description": "action superhero books"
  }'
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

**Without Token:**
```bash
curl -X POST http://localhost:30080/books/search \
  -H "Content-Type: application/json" \
  -d '{"description": "action books"}'
# Response: 401 Unauthorized
```

## How It Works

### Book Search Flow
1. User authenticates via `/auth/login` and receives JWT token
2. User sends book description to `/books/search` with Bearer token
3. JWT token validated and user retrieved from PostgreSQL
4. Ollama LLM extracts 3 search keywords from description
5. Keywords sent to Google Books API
6. Top 10 results returned to user

### Authentication Flow
1. User registers via `/auth/register` - password hashed with bcrypt
2. User credentials stored in PostgreSQL
3. User logs in via `/auth/login` - password verified
4. JWT token generated with 30-minute expiration
5. Token required for all `/books/*` endpoints
6. Token validated on each request via `get_current_user` dependency

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

## Testing
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_auth_service.py -v

# Run with coverage
pytest tests/ --cov=app
```

Test coverage includes:
- Authentication service (register, login, token generation)
- Authentication routes (register, login endpoints)
- Protected routes (JWT validation)
- Book search functionality
- Health endpoints
- Metrics collection

## Monitoring

### Prometheus Metrics
Available at `/metrics`:
- `http_requests_total` - Total HTTP requests by method, endpoint, status
- `http_request_duration_seconds` - HTTP request latency
- `active_requests` - Number of active requests by endpoint
- `external_api_calls_total` - External API calls by service and status
- `external_api_duration_seconds` - External API call duration
- `authenticated_requests_total` - Authenticated requests by username

### Kubernetes Probes
- **Liveness Probe:** `/health` - Restarts pod on failure
- **Readiness Probe:** `/health` - Stops traffic to unhealthy pods

## High Availability & Reliability

### Application Layer
- **3 replicas** for fault tolerance
- **Ollama sidecar** in each pod (no external dependency)
- **Automatic restart** on health check failure
- **Init containers** wait for PostgreSQL before app starts
- **Database schema** automatically created on first deployment

### Database Layer
- **PostgreSQL StatefulSet** with persistent storage (1Gi)
- **Headless service** for stable network identity
- **Liveness/Readiness probes** with `pg_isready`

### Self-Healing
- Kubernetes automatically restarts failed pods
- Init containers ensure dependencies are ready
- Health probes detect and recover from failures

## Security

- **Passwords:** Hashed with bcrypt (72-byte limit)
- **JWT Tokens:** HS256 algorithm, 30-minute expiration
- **Secrets:** Kubernetes Secrets for PostgreSQL credentials
- **SQL Injection:** Protected by psycopg2 parameterized queries
- **Protected Endpoints:** JWT validation via FastAPI dependencies

## Configuration

### Environment Variables
Configure via `app/core/config.py`:
- `database_url` - PostgreSQL connection string
- `jwt_secret_key` - Secret key for JWT signing
- `jwt_algorithm` - JWT signing algorithm (HS256)
- `jwt_expiration_minutes` - Token expiration (30 minutes)
- `ollama_base_url` - Ollama service URL
- `ollama_model` - LLM model name (gemma3:270m)
- `google_books_base_url` - Google Books API endpoint

## Troubleshooting

### Pods in CrashLoopBackOff
```bash
# Check logs
kubectl logs <pod-name> -c atlas-app

# Check init containers
kubectl logs <pod-name> -c wait-for-postgres
kubectl logs <pod-name> -c init-db-schema
```

### Authentication Errors
```bash
# Check PostgreSQL
kubectl exec -it postgres-0 -- psql -U atlasuser -d atlasdb -c "SELECT * FROM users;"

# Test registration
curl -X POST http://localhost:30080/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test123"}'
```

### Rebuild and Redeploy
```bash
cd ansible
ansible-playbook playbooks/deploy-application.yml
kubectl delete pods -l app=atlas-service
```

## Development

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt  # If you create one

# Run tests
pytest tests/ -v

# Run locally (without K8s)
uvicorn app.main:app --reload
```
