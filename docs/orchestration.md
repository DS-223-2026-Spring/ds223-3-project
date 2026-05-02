# Orchestration

Prefect-based ETL pipeline runs on container start.

## Flows
1. `validate_data` — checks CSV schema before loading
2. `load_data` — inserts studios + classes into Postgres
3. `train_model` — runs prepare → augment → train pipeline

Chained in `flows/pipeline.py`.

## How to run Prefect

### Option 1: Inside Docker (default, used in production)

The etl service runs the full pipeline once on container start:

docker compose up --build etl
Expected output:
etl-1 | Validating data
etl-1 | Beginning subflow run for flow 'validate-data'
etl-1 | Loaded 23 studios, 159 classes
etl-1 | Beginning subflow run for flow 'train-model'
etl-1 | Saving Random Forest
etl-1 exited with code 0

### Option 2: Locally (for development)

Requires Python 3.11 and the DB running.

# 1. Start just the DB
docker compose up -d db

# 2. Set env vars
export DB_HOST=localhost
export DB_USER=admin
export DB_PASSWORD=admin
export DB_NAME=activityhub

# 3. Install Prefect
cd activityhub/etl
pip install -r requirements.txt

# 4. Run individual flows
python -m flows.validate_data    # CSV schema check
python -m flows.load_data        # load studios + classes
python -m flows.train_model      # train classifier

# Or run all chained:
python -m flows.pipeline
### Flow responsibilities

- validate_data.py — checks ds/data/*.csv files for required columns, fails fast on missing data
- load_data.py — inserts studios + classes into Postgres via SQLAlchemy
- train_model.py — calls prepare_survey.py → augment_training.py → train_model.py script chain to produce style_classifier.pkl
- pipeline.py — chains all three flows in order (validate → load → train)

### Verifying success

docker compose exec db psql -U admin -d activityhub \
  -c "SELECT COUNT(*) FROM studios; SELECT COUNT(*) FROM classes;"
Should return 23 and 159.


# Data Flow Architecture

How data moves between roles and services.

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
ETL (daily, scheduled by Prefect)
↓ pulls fresh quiz_responses + bookings + survey_responses
↓ runs prepare → augment → train
↓ writes new style_classifier.pkl
DS pipeline

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