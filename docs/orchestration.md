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