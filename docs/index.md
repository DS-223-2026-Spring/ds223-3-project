# ActivityHub

A personalized activity matching platform for Yerevan that connects users with extracurricular studios (yoga, dance, fitness) based on personality, schedule, and budget.

## Architecture
The product runs as a microservice stack:
- **api** — FastAPI backend
- **app** — Streamlit frontend  
- **db** — PostgreSQL
- **model** — scikit-learn classifier
- **etl** — Prefect data pipeline

## Quick start
```bash
docker compose up --build
```

Visit http://localhost:8501

## Documentation
See sections in the left nav for each component.