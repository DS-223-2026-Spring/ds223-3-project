"""
Production pipeline for ActivityHub.

Runs end-to-end on container start:
    validate CSVs → load DB → generate synthetic survey → train model → segment users

Each step is a Prefect flow with retries and logging. Failures in any step
will retry once before failing the pipeline.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prefect import flow, get_run_logger

from flows.validate_data import validate_flow
from flows.load_data import load_data_flow
from flows.train_model import train_flow
from flows.segment_users import segment_users_flow


@flow(name="activityhub-pipeline", retries=1, log_prints=True)
def full_pipeline():
    """
    Full production pipeline.

    Inputs:  ds/data/*.csv (studios, classes, survey)
    Outputs: Postgres tables (studios, classes, segments) + style_classifier.pkl

    Steps:
      1. validate_flow      - check CSV schemas
      2. load_data_flow     - load studios + classes into Postgres
      3. train_flow         - generate synthetic + prepare + augment + train
      4. segment_users_flow - K-means clustering → segments table

    Each subflow has its own retries. The whole pipeline retries once if
    any uncaught exception bubbles up.
    """
    logger = get_run_logger()
    logger.info("=== ActivityHub pipeline starting ===")

    logger.info("[1/4] Validating CSVs...")
    validate_flow()

    logger.info("[2/4] Loading data into Postgres...")
    load_data_flow()

    logger.info("[3/4] Training model...")
    train_flow()

    logger.info("[4/4] Segmenting users...")
    segment_users_flow()

    logger.info("Pipeline complete")


if __name__ == "__main__":
    full_pipeline()