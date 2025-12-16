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
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Context API** - Global authentication state
- **Jest & React Testing Library** - Unit testing

## Project Structure
```
atlas-reliability-framework/
├── app/                             # Backend (FastAPI)
│   ├── api/routes/
│   ├── core/
│   ├── db/
│   ├── models/
│   └── services/
├── frontend/                        # Frontend (React)
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── pages/
│   │   │   ├── LandingPage.js
│   │   │   ├── LoginPage.js
│   │   │   ├── RegisterPage.js
│   │   │   ├── QueryPage.js
│   │   │   └── __tests__/
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── authService.js
│   │   │   ├── booksService.js
│   │   │   └── __tests__/
│   │   ├── context/
│   │   │   └── AuthContext.js
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── .env.example
├── ansible/
│   ├── k8s/
│   ├── playbooks/
│   ├── group_vars/
│   └── inventory/
├── tests/                           # Backend tests
├── Dockerfile
└── pytest.ini
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

### 2. Deploy Backend Application
```bash
ansible-playbook playbooks/deploy-application.yml
```

### 3. Setup Frontend
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env if needed (default: REACT_APP_API_URL=http://localhost:30080)
npm start
```

### 4. Verify Deployment
```bash
kubectl get pods
# Expected: postgres-0 (1/1 Running) + atlas-service-xxx (2/2 Running, 3 replicas)

curl http://localhost:30080/health
# Expected: {"status":"healthy"}

# Frontend should be running at http://localhost:3000
```

## User Flow

### 1. Landing Page
- View system metrics (Total Requests, Active Requests, Avg Latency)
- See feature highlights
- Navigate to Login or Register

### 2. Register
- Create account with username (min 3 chars) and password (min 6 chars)
- Password confirmation validation
- Auto-redirect to login after success

### 3. Login
- Authenticate with credentials
- Receive JWT token (30-minute expiration)
- Auto-redirect to query page

### 4. Query Page (Protected)
- Search books using natural language description
- AI extracts keywords via Ollama LLM
- View search results from Google Books API
- See book thumbnails, titles, authors, categories, descriptions
- Logout to return to home

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

## How It Works

### Book Search Flow
1. User registers via frontend → POST /auth/register
2. User logs in via frontend → POST /auth/login → JWT token returned
3. Token stored in localStorage and added to all API requests
4. User enters book description in query page
5. Frontend sends description with Bearer token → POST /books/search
6. Backend validates JWT and retrieves user from PostgreSQL
7. Ollama LLM extracts 3 keywords from description
8. Keywords sent to Google Books API
9. Top 10 results returned to frontend
10. Results displayed in responsive card grid

### Authentication Flow
1. User registers → password hashed with bcrypt → stored in PostgreSQL
2. User logs in → password verified → JWT token generated (30-min expiration)
3. Frontend stores token in localStorage
4. Protected routes check authentication via AuthContext
5. Unauthenticated users redirected to login page
6. Token included in Authorization header for all protected API calls

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE);
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

Test coverage includes:
- **Backend:** Authentication service, routes, book search, health, metrics
- **Frontend:** All pages (Landing, Login, Register, Query), services (api, auth, books), AuthContext

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
- **Frontend Auth:** Token stored in localStorage, included in all protected API calls

## Configuration

### Backend Environment Variables
Configure via `app/core/config.py`:
- `database_url` - PostgreSQL connection string
- `jwt_secret_key` - Secret key for JWT signing
- `jwt_algorithm` - JWT signing algorithm (HS256)
- `jwt_expiration_minutes` - Token expiration (30 minutes)
- `ollama_base_url` - Ollama service URL
- `ollama_model` - LLM model name (gemma3:270m)
- `google_books_base_url` - Google Books API endpoint

### Frontend Environment Variables
Configure via `frontend/.env`:
- `REACT_APP_API_URL` - Backend API base URL (default: http://localhost:30080)

## Troubleshooting

### Backend Issues

#### Pods in CrashLoopBackOff
```bash
kubectl logs <pod-name> -c atlas-app
kubectl logs <pod-name> -c wait-for-postgres
kubectl logs <pod-name> -c init-db-schema
```

#### Authentication Errors
```bash
kubectl exec -it postgres-0 -- psql -U atlasuser -d atlasdb -c "SELECT * FROM users;"
```

#### Rebuild and Redeploy
```bash
cd ansible
ansible-playbook playbooks/deploy-application.yml
kubectl delete pods -l app=atlas-service
```

### Frontend Issues

#### Cannot connect to backend
- Check `REACT_APP_API_URL` in `.env`
- Verify backend is running: `curl http://localhost:30080/health`
- Check browser console for CORS errors

#### Authentication not working
- Clear localStorage: `localStorage.clear()` in browser console
- Check JWT token expiration (30 minutes)
- Verify backend authentication endpoints are accessible

## Development

### Backend Local Testing
```bash
pip install -r requirements.txt
pytest tests/ -v
uvicorn app.main:app --reload
```

### Frontend Local Development
```bash
cd frontend
npm install
npm start         # Development server at http://localhost:3000
npm test          # Run tests
npm run build     # Production build
```

## Color Scheme

Based on Atlas logo:
- **Navy Blue:** `#1e3a5f` (Headers, primary text)
- **Light Blue:** `#5ba3d0` (Buttons, accents, links)
- **Beige/Tan:** `#e8b67a` (Subtitle, username display)
- **Light Gray:** `#f5f5f5` (Background)

## License

© 2024 Atlas Reliability Framework
