# Atlas Reliability Framework

High availability Python FastAPI service with Kubernetes deployment and SRE practices.

## Prerequisites

- Ubuntu/Debian Linux
- Docker installed
- Ansible installed

## Quick Start

### 1. Setup Infrastructure (Install K3s)
```bash
cd ansible
ansible-playbook playbooks/setup-infrastructure.yml
```

### 2. Deploy Application
```bash
ansible-playbook playbooks/deploy-application.yml
```

### 3. Access Service

Service available at: http://localhost:30080

## Endpoints

- `GET /` - Hello World
- `GET /health` - Health check for probes
- `GET /data` - Simulated service data
- `GET /fail` - Unstable endpoint (30% error rate, 20% high latency)
- `GET /metrics` - Prometheus metrics

## Test Self-Healing
```bash
# Watch pods
kubectl get pods -w

# Trigger failures repeatedly
while true; do curl http://localhost:30080/fail; sleep 1; done