# Orchestration

Prefect-based ETL pipeline runs on container start.

## Flows
1. `validate_data` — checks CSV schema before loading
2. `load_data` — inserts studios + classes into Postgres
3. `train_model` — runs prepare → augment → train pipeline

Chained in `flows/pipeline.py`.