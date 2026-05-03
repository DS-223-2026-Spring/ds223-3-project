"""
Dev/testing pipeline.

Skips model training (slow) and segmentation. Use for fast iteration when
you only need fresh data in the DB. The full production pipeline lives in
pipeline.py.

Usage in the etl container:
    python flows/dev_pipeline.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prefect import flow, get_run_logger

from flows.validate_data import validate_flow
from flows.load_data import load_data_flow


@flow(name="activityhub-dev-pipeline", log_prints=True)
def dev_pipeline():
    """Validate + load only. No training, no segmentation."""
    logger = get_run_logger()
    logger.info("Dev pipeline starting")
    validate_flow()
    load_data_flow()
    logger.info("Dev pipeline complete")


if __name__ == "__main__":
    dev_pipeline()