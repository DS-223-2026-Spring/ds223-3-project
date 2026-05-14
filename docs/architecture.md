# Architecture

ActivityHub runs as a microservice stack orchestrated through Docker Compose.

![Architecture](imgs/project_architecture_diagram.svg)

## Services

| Service | Tech | Role | Port |
|---------|------------|------|------|
| `app` | Streamlit | User-facing dashboard - quiz, recommendations, studio insights | 8501 |
| `api` | FastAPI | REST API exposing quiz, recommend, studios, segments, bookings | 8000 |
| `db` | PostgreSQL 17 | Storage for users, quiz responses, classes, recommendations, segments, bookings | 5432 |
| `etl` | Prefect | Pipeline: validate → load → train → segment. Runs once on container start | — |
| `prefect-server` | Prefect | Orchestration UI for flow run history and logs | 4200 |
| `pgadmin` | pgAdmin 4 | Database browser | 5050 |

## Data flow

```text
ETL pipeline
│
│ 1. Validates and loads CSVs into Postgres
│ 2. Trains style classifier, saves pkl
│ 3. Runs K-means segmentation
▼
PostgreSQL
│
│ 4. Stores all persistent state
▼
FastAPI
│
│ 5. Reads from DB, calls shared inference module for recommendations
▼
Streamlit
6. Calls FastAPI endpoints and renders pages at http://localhost:8501
```

## Local URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:8501 |
| API Swagger | http://localhost:8000/docs |
| Prefect UI | http://localhost:4200 |
| pgAdmin | http://localhost:5050 |