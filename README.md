<img width="953" height="599" alt="image" src="https://github.com/user-attachments/assets/209b4b86-d654-42be-b57d-9ed39ba34f66" />
# Task API — Dockerized Flask Microservice

A small REST API for managing tasks, built to demonstrate containerization
and cloud-native deployment practices: health checks, non-root containers,
and a production WSGI server (Gunicorn) instead of Flask's dev server.

## Features
- REST endpoints for creating, listing, retrieving, and deleting tasks
- Persisted to a real database via SQLAlchemy — SQLite by default,
  swappable to Postgres with one environment variable
- `/health` endpoint that checks actual database connectivity, not just
  that the web process is alive — and is ready to wire into a
  Kubernetes liveness/readiness probe
- Multi-stage Dockerfile for a lean, non-root runtime image
- `docker-compose.yml` with a persistent volume so data survives
  container restarts, plus a commented-out Postgres service

## Tech Stack
Python, Flask, SQLAlchemy, Gunicorn, Docker, Docker Compose, (optional) Postgres

## Switching to Postgres
By default this runs on SQLite with zero setup. To run against Postgres
instead, set the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

No code changes needed — `db.py` reads this at startup. The
`docker-compose.yml` has a commented-out Postgres service ready to
uncomment for local testing against a real Postgres instance.

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
- [x] Persist data with a real database (SQLAlchemy, SQLite/Postgres)
- [ ] Push image to Docker Hub / ECR / ACR
- [ ] Deploy to AWS EKS
- [ ] Deploy to Azure AKS
- [ ] Run against managed Postgres (AWS RDS / Azure Database for PostgreSQL)
- [ ] Wire up a GitHub Actions pipeline to build once, deploy to both clusters
- [ ] Add Prometheus metrics endpoint

## Why this project
Built as a portfolio piece to demonstrate hands-on skills in containerization,
API development, and cloud-native design patterns as part of a DevOps/Cloud
Engineer job search.
