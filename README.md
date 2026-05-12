# ActivityHub

Personalized activity matching for Yerevan — yoga, dance, and fitness recommendations based on your personality, schedule, and budget.

[![CI](https://github.com/DS-223-2026-Spring/ds223-3-project/actions/workflows/ci.yaml/badge.svg)](https://github.com/DS-223-2026-Spring/ds223-3-project/actions)

## Links

- **Documentation:** https://ds-223-2026-spring.github.io/ds223-3-project/
- **Project board:** https://github.com/DS-223-2026-Spring/ds223-3-project/issues
- **License:** MIT — see [LICENSE](LICENSE)

## Quick start

```bash
docker compose up --build
```

Wait for `etl-1 exited with code 0`. Then open:

- **App (Streamlit):** http://localhost:8501
- **API docs (Swagger):** http://localhost:8000/docs
- **pgAdmin:** http://localhost:5050 (admin@admin.com / admin)

## What's in here

| Service | Folder | Purpose |
|---------|--------|---------|
| API | `activityhub/api/` | FastAPI — quiz, recommend, segments, bookings endpoints |
| App | `activityhub/app/` | Streamlit — quiz, recommendations, studio dashboard |
| DB | `activityhub/db/` | PostgreSQL schema + CRUD utilities |
| DS | `activityhub/ds/` | Multi-class classifier + K-means segmentation |
| ETL | `activityhub/etl/` | Prefect pipeline (validate → load → train → segment) |
| Shared | `activityhub/shared/` | Inference module shared between API and DS |

## Team

Group 3, DS-223 Spring 2026, AUA.

- Anna Khurshudyan — Product Manager
- Liana Zhamkochyan — Database Developer
- Meline Mamikonyan — Data Science
- Ani Kirakosyan — Backend
- Maria Petrosyan — Frontend
- Hmayak Paravyan — Orchestration

## Resetting state

```bash
docker compose down -v
docker compose up --build
```

That wipes the Postgres volume and reruns the full ETL pipeline.