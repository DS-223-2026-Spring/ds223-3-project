# Orchestration

Prefect-based ETL pipeline that runs end-to-end on container start.

## Inputs & Outputs

| Flow | Inputs | Outputs |
|------|--------|---------|
| `validate_data` | `ds/data/*.csv` | dict of {path, rows, cols_ok}, raises on failure |
| `load_data` | studios.csv, classes.csv | rows in studios + classes (idempotent via TRUNCATE) |
| `train_model` | survey.csv | `ds/models/style_classifier.pkl`, metrics.csv |
| `segment_users` | survey_combined.csv | 4 personas in segments table |
| `pipeline` | (chains all above) | full DB + model state |
| `dev_pipeline` | studios.csv, classes.csv | DB rows only (fast iteration) |

## How to run

### Production (default — runs on `docker compose up`)

```bash
docker compose up --build
```

The `etl` service auto-runs `pipeline.py` on startup. Watch for `etl-1 exited with code 0`.

### Manual / dev runs

```bash
docker compose run --rm etl python flows/pipeline.py
docker compose run --rm etl python flows/dev_pipeline.py     # fast: validate + load only
docker compose run --rm etl python flows/segment_users.py    # just segmentation
```

### Local (no Docker)

```bash
docker compose up -d db
export DB_HOST=localhost
export DB_USER=admin
export DB_PASSWORD=admin
export DB_NAME=activityhub

cd activityhub/etl
pip install -r requirements.txt
python -m flows.pipeline
```

## Verifying success

```bash
docker compose exec db psql -U admin -d activityhub -c "
  SELECT COUNT(*) FROM studios; SELECT COUNT(*) FROM classes; SELECT COUNT(*) FROM segments;
"
```

Should return 23, 159, 4.

## Logs

Prefect logs to stdout. View with:

```bash
docker compose logs etl
```

Each task has `retries=1` or `retries=2` for transient DB issues.

## Data Flow Architecture

How data moves between roles and services:

```
User
  ↓ (fills quiz in browser)
Frontend (Streamlit)
  ↓ POST /quiz/
Backend (FastAPI)
  ↓ INSERT users, quiz_responses
Postgres (DB)

User
  ↓ (clicks "Get Recommendations")
Frontend
  ↓ POST /recommend/ {user_id}
Backend
  ↓ SELECT quiz, classes
Postgres
  ↓ (returns rows)
Backend
  ↓ calls shared.recommend.recommend_top_k(user, classes, k=3)
Shared inference module
  ↓ loads /app/ds/models/style_classifier.pkl
  ↓ returns ranked classes
Backend
  ↓ INSERT recommendations
Postgres
  ↓ returns response
Frontend (renders cards)

User clicks "I tried this"
  ↓ POST /bookings/
Backend
  ↓ INSERT bookings
Postgres
  ↓ (feeds future retraining)

ETL pipeline (on container start, or manual rerun)
  ↓ validate → load → train → segment
  ↓ writes style_classifier.pkl + segments table
DS pipeline
```

## Role responsibilities

| Role           | Owns                                       | Depends on                       |
|----------------|--------------------------------------------|----------------------------------|
| DB (Liana)     | init.sql, crud.py, connection.py, schemas  | PM endpoint spec                 |
| DS (Meline)    | model training, K-means, recommend_top_k   | DB tables, ETL pipeline trigger  |
| Backend (Ani)  | FastAPI routes, request/response schemas   | DB CRUD, DS inference function   |
| Frontend (Maria) | Streamlit pages, user-facing flow        | Backend endpoints, frontend spec |
| Orch (Hmayak)  | Prefect flows, scheduling, retraining      | DS scripts, DB connection        |
| PM (Anna)      | Specs, alignment, blockers, integration    | All                              |

## Key contracts

1. **`/recommend/` request shape** is fixed — `{ user_id: int }`. Frontend can't deviate; Backend can't add required fields.
2. **`recommend_top_k(user, classes_df, k)` signature** — DS owns this; Backend imports it; both must keep it stable.
3. **`segments` table schema** — DS writes K-means output here; Backend exposes via `/segments/`; Frontend renders.
4. **`bookings` table** — Backend writes on POST `/bookings/`; ETL reads as feature for retraining.
5. **Model file path** — `/app/ds/models/style_classifier.pkl` — agreed by DS + Backend, must not move.

## Failure-mode contracts

If a service is down, others should fail gracefully:

- Frontend without Backend → show "Service unavailable" not blank page
- Backend without DB → return 503 not 500
- Backend without model pkl → return 503 with "model not loaded"
- ETL without DB → fail flow, log error, exit non-zero

## Demo trigger

For demo runs: `docker compose up --build`. Pipeline runs once automatically. To re-trigger after changes, re-run `docker compose up --build etl`.