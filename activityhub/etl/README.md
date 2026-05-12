# Orchestration (Prefect)

ETL service runs the full production pipeline once on container start, then exits.

## Inputs & Outputs

| Flow | Inputs | Outputs |
|------|--------|---------|
| validate_data | ds/data/studios.csv, ds/data/classes.csv | raises if schema/empty fails |
| load_data | studios.csv, classes.csv | rows in studios + classes tables (idempotent via TRUNCATE) |
| train_model | ds/data/survey.csv | ds/models/style_classifier.pkl, metrics.csv, survey_combined.csv |
| segment_users | ds/data/survey_combined.csv | rows in segments table |
| pipeline | (all above) | full DB + model state |
| dev_pipeline | studios.csv, classes.csv | DB rows only (fast iteration) |

## Flows

| Flow                  | Inputs                                       | Outputs                                |
|-----------------------|----------------------------------------------|----------------------------------------|
| `validate_data.py`    | `ds/data/studios.csv`, `ds/data/classes.csv` | dict of {path, rows, cols_ok} or raises|
| `load_data.py`        | studios.csv, classes.csv                     | rows in studios + classes tables       |
| `train_model.py`      | `ds/data/survey.csv`                         | `ds/models/style_classifier.pkl`, metrics.csv |
| `segment_users.py`    | `ds/data/survey_combined.csv` (or survey.csv)| rows in segments table                 |
| `pipeline.py`         | (chains all above)                           | full DB + model state                  |
| `dev_pipeline.py`     | studios.csv, classes.csv only                | DB rows only (fast iteration)          |

Each task uses `retries=1` or `retries=2` so transient DB connection issues don't fail the whole run.

## How to run

### Production (default — runs on `docker compose up`)
The `etl` service auto-runs `pipeline.py` on container start:
```bash
docker compose up --build
```
Watch for `etl-1 exited with code 0` — that's success.

### Manual one-shot run
After the stack is up, trigger any flow individually:
```bash
docker compose run --rm etl python flows/pipeline.py
docker compose run --rm etl python flows/dev_pipeline.py     # fast: validate + load only
docker compose run --rm etl python flows/segment_users.py    # just segmentation
```

### Local (no Docker)
From repo root:
```bash
cd activityhub/etl
pip install -r requirements.txt

# DB must be running:
docker compose up -d db

# Set env vars
export DB_HOST=localhost
export DB_USER=admin
export DB_PASSWORD=admin
export DB_NAME=activityhub

python -m flows.pipeline
```

## Logs and run statuses

Prefect logs every task with timestamps and run status.
Each flow run gets a unique name and color-coded status (Completed / Failed).

Inside Docker, logs stream to stdout — watch the `etl-1` lines in `docker compose up`.

To see a Prefect flow's logs from a finished run:
```bash
docker compose logs etl
```

## Verifying success

After `etl-1 exited with code 0`, verify:

```bash
# DB populated
docker compose exec db psql -U admin -d activityhub \
  -c "SELECT COUNT(*) FROM studios; SELECT COUNT(*) FROM classes; SELECT COUNT(*) FROM segments;"

# Should return: 23 studios, 159 classes, 4 segments

# Model artifact present
docker compose exec api ls -la /app/ds/models/
# Should show: style_classifier.pkl, metrics.csv
```

## Failure handling

- Tasks have built-in retries (1–2 attempts).
- The full `pipeline.py` flow itself retries once on any uncaught exception.
- If a CSV is missing or the DB is unreachable, the flow logs the error and exits non-zero. Other services (api, app) keep running but recommendations may fail until the next pipeline run.