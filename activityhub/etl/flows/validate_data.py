"""
Validate that CSVs exist with required columns before loading.

Inputs:  ds/data/studios.csv, ds/data/classes.csv
Outputs: dict of row counts (raises ValueError on schema/empty failures)
"""
from prefect import flow, task, get_run_logger
import pandas as pd

REQUIRED_STUDIO_COLS = ["studio_id", "studio_name", "district", "price_tier", "studio_type"]
REQUIRED_CLASS_COLS = ["class_id", "studio_id", "activity_type", "style",
                       "experience_required", "group_or_private",
                       "energy_level", "structure_level"]


@task(retries=2, retry_delay_seconds=3)
def check_file(path: str, required_cols: list) -> dict:
    """Verify a CSV exists, has required columns, and isn't empty."""
    logger = get_run_logger()
    df = pd.read_csv(path)
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"{path} missing columns: {missing}")
    if df.empty:
        raise ValueError(f"{path} is empty")
    logger.info(f"{path}: {len(df)} rows, schema OK")
    return {"path": path, "rows": len(df), "cols_ok": True}


@flow(name="validate-data", log_prints=True)
def validate_flow():
    """Validate studios.csv and classes.csv before they get loaded."""
    s = check_file("ds/data/studios.csv", REQUIRED_STUDIO_COLS)
    c = check_file("ds/data/classes.csv", REQUIRED_CLASS_COLS)
    return [s, c]


if __name__ == "__main__":
    validate_flow()