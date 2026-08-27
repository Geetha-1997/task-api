# Task API — Dockerized Flask Microservice

A small REST API for managing tasks, built to demonstrate containerization
and cloud-native deployment practices: health checks, non-root containers,
and a production WSGI server (Gunicorn) instead of Flask's dev server.

## Features
- REST endpoints for creating, listing, retrieving, and deleting tasks
- `/health` endpoint for liveness/readiness checks (Docker `HEALTHCHECK`,
  and ready to wire into a Kubernetes probe)
- Multi-stage Dockerfile for a lean, non-root runtime image
- `docker-compose.yml` for one-command local startup

## Tech Stack
Python, Flask, Gunicorn, Docker, Docker Compose

## Run locally with Docker

```bash
docker build -t task-api .
docker run -p 5000:5000 task-api
```

Or with Docker Compose:

```bash
docker compose up --build
```

## API Reference

| Method | Endpoint        | Description          |
|--------|-----------------|-----------------------|
| GET    | `/health`       | Health check          |
| GET    | `/tasks`        | List all tasks        |
| POST   | `/tasks`        | Create a task          |
| GET    | `/tasks/<id>`   | Get a single task      |
| DELETE | `/tasks/<id>`   | Delete a task          |

### Example

```bash
curl http://localhost:5000/health

curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Kubernetes"}'

curl http://localhost:5000/tasks
```

## Roadmap
- [ ] Push image to Docker Hub / ECR / ACR
- [ ] Deploy to AWS EKS
- [ ] Deploy to Azure AKS
- [ ] Wire up a GitHub Actions pipeline to build once, deploy to both clusters
- [ ] Add Prometheus metrics endpoint

## Why this project
Built as a portfolio piece to demonstrate hands-on skills in containerization,
API development, and cloud-native design patterns as part of a DevOps/Cloud
Engineer job search.
