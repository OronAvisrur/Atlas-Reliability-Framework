# Atlas Reliability Framework

FastAPI service with PostgreSQL authentication, Ollama LLM integration for book search, deployed on Kubernetes with high availability and monitoring. Includes React frontend for user interaction.

## Architecture

**Backend:**
- **FastAPI** - REST API with clean architecture
- **PostgreSQL** - User authentication database
- **JWT** - Token-based authentication
- **Ollama (gemma3:270m)** - LLM for keyword extraction
- **Google Books API** - Book database search
- **Prometheus** - Metrics collection
- **Kubernetes (K3s)** - Container orchestration with 3 replicas
- **Ansible** - Infrastructure automation

**Frontend:**
- **React 18** - User interface library
- **Nginx** - Static file server and reverse proxy
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Context API** - Global authentication state
- **Jest & React Testing Library** - Unit testing

## Project Structure
```
atlas-reliability-framework/
├── app/                             # Backend (FastAPI)
│   ├── Dockerfile                   # Backend container image
│   ├── api/routes/
│   ├── core/
│   ├── db/
│   ├── models/
│   └── services/
├── frontend/                        # Frontend (React)
│   ├── Dockerfile                   # Frontend container image (nginx)
│   ├── nginx.conf                   # Nginx reverse proxy config
│   ├── public/
│   ├── src/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── context/
│   │   └── __tests__/
│   └── package.json
├── ansible/
│   ├── k8s/
│   │   ├── deployment.yaml              # Backend deployment
│   │   ├── service.yaml                 # Backend service
│   │   ├── frontend-deployment.yaml     # Frontend deployment
│   │   ├── frontend-service.yaml        # Frontend service
│   │   ├── postgres-secrets.yaml
│   │   ├── postgres-statefulset.yaml
│   │   ├── postgres-service.yaml
│   │   └── db-schema-configmap.yaml
│   └── playbooks/
│       ├── setup-infrastructure.yml
│       ├── setup-postgres.yml
│       ├── deploy-application.yml       # Deploy backend only
│       ├── deploy-frontend.yml          # Deploy frontend only
│       └── deploy-full-stack.yml        # Deploy everything
├── tests/                           # Backend tests
└── README.md
```

## Prerequisites

- Python 3.11+
- Node.js 16+
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

### 2. Deploy Full Stack (Backend + Frontend)
```bash
ansible-playbook playbooks/deploy-full-stack.yml
```

**OR Deploy Separately:**
```bash
# Backend only
ansible-playbook playbooks/deploy-application.yml

# Frontend only
ansible-playbook playbooks/deploy-frontend.yml
```

### 3. Verify Deployment
```bash
kubectl get pods,svc
# Expected: 
# - postgres-0 (1/1 Running)
# - atlas-service-xxx (2/2 Running, 3 replicas) 
# - atlas-frontend-xxx (1/1 Running, 3 replicas)

curl http://localhost:30080/health
# Expected: {"status":"healthy"}

# Access frontend at http://localhost:30080
```

## Services & Ports

| Service | Type | Port | NodePort | Purpose |
|---------|------|------|----------|---------|
| atlas-frontend | NodePort | 80 | 30080 | React UI (nginx) |
| atlas-service | ClusterIP | 8000 | - | FastAPI Backend |
| postgres | ClusterIP | 5432 | - | PostgreSQL Database |

**Important:** Frontend (nginx) serves on port 30080 and proxies API calls to backend internally.

## User Flow

### 1. Access Application
- Open browser: `http://localhost:30080`
- View landing page with system metrics

### 2. Register
- Click "Register" button
- Create account with username (min 3 chars) and password (min 6 chars)
- Auto-redirect to login

### 3. Login
- Enter credentials
- Receive JWT token (30-minute expiration)
- Auto-redirect to query page

### 4. Search Books
- Enter natural language description (e.g., "action superhero books")
- AI extracts keywords via Ollama LLM
- View results from Google Books API
- See thumbnails, titles, authors, categories, descriptions

### 5. Logout
- Click "Logout" to return to home

## API Endpoints

### Public Endpoints (via nginx proxy)

#### GET /
Landing page (served by nginx)

#### GET /health
Health check (proxied to backend)

#### GET /metrics
Prometheus metrics (proxied to backend)

#### POST /api/auth/register
Register new user (proxied to backend /auth/register)

#### POST /api/auth/login
Login and receive JWT (proxied to backend /auth/login)

### Protected Endpoints (Require JWT)

#### POST /api/books/search
Search books (proxied to backend /books/search)
- Requires `Authorization: Bearer <token>` header
- Frontend automatically includes token from localStorage

## Nginx Reverse Proxy

Frontend nginx proxies API requests:
- `/api/*` → `http://atlas-service:8000/`
- `/health` → `http://atlas-service:8000/health`
- `/metrics` → `http://atlas-service:8000/metrics`

This allows frontend and backend to communicate within the cluster.

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

### Backend Tests
```bash
pytest tests/ -v
pytest tests/ --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
npm test -- --coverage
```

## Monitoring

### Prometheus Metrics
Available at `http://localhost:30080/metrics`:
- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request latency
- `active_requests` - Active requests
- `external_api_calls_total` - External API calls
- `authenticated_requests_total` - Authenticated requests

### Kubernetes Health
```bash
kubectl get pods -w
kubectl logs -f deployment/atlas-frontend
kubectl logs -f deployment/atlas-service
```

## High Availability

### Application Layer
- **Backend:** 3 replicas (FastAPI + Ollama sidecar)
- **Frontend:** 3 replicas (nginx)
- **Automatic restart** on health check failure
- **Init containers** ensure PostgreSQL is ready

### Database Layer
- **PostgreSQL StatefulSet** with persistent storage (1Gi)
- **Liveness/Readiness probes**

## Security

- **Passwords:** Hashed with bcrypt
- **JWT Tokens:** HS256, 30-minute expiration
- **Kubernetes Secrets** for PostgreSQL credentials
- **Frontend:** Token stored in localStorage
- **Backend:** JWT validation on protected endpoints

## Development

### Backend Local Development
```bash
cd app
pip install -r requirements.txt
pytest ../tests/ -v
uvicorn main:app --reload
```

### Frontend Local Development
```bash
cd frontend
npm install
cp .env.example .env
# Edit REACT_APP_API_URL if needed
npm start       # http://localhost:3000
npm test
npm run build
```

## Troubleshooting

### Backend Issues
```bash
kubectl logs deployment/atlas-service
kubectl describe pod <atlas-service-pod>
```

### Frontend Issues
```bash
kubectl logs deployment/atlas-frontend
# Check nginx logs for proxy errors
```

### Database Issues
```bash
kubectl logs postgres-0
kubectl exec -it postgres-0 -- psql -U atlasuser -d atlasdb
```

### Rebuild & Redeploy
```bash
cd ansible
ansible-playbook playbooks/deploy-full-stack.yml
```

### Clear Everything
```bash
kubectl delete deployment atlas-frontend atlas-service
kubectl delete service atlas-frontend atlas-service
kubectl delete statefulset postgres
kubectl delete pvc postgres-pvc
```

## Color Scheme

- **Navy Blue:** `#1e3a5f` (Headers)
- **Light Blue:** `#5ba3d0` (Buttons, accents)
- **Beige/Tan:** `#e8b67a` (Subtitle)
- **Light Gray:** `#f5f5f5` (Background)

## License

© 2025 Atlas Reliability Framework
