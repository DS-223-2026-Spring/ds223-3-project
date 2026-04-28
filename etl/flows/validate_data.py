# Prefect flow: validate CSVs before loading.
from prefect import flow, task
import pandas as pd

REQUIRED_STUDIO_COLS = ["studio_id", "studio_name", "district", "price_tier", "studio_type"]
REQUIRED_CLASS_COLS = ["class_id", "studio_id", "activity_type", "style",
                       "experience_required", "group_or_private",
                       "energy_level", "structure_level"]


@task
def check_file(path, required_cols):
    df = pd.read_csv(path)
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"{path} missing columns: {missing}")
    if df.empty:
        raise ValueError(f"{path} is empty")
    return {"path": path, "rows": len(df), "cols_ok": True}


@flow(name="validate-data")
def validate_flow():
    s = check_file("ds/data/studios.csv", REQUIRED_STUDIO_COLS)
    c = check_file("ds/data/classes.csv", REQUIRED_CLASS_COLS)
    return [s, c]


if __name__ == "__main__":
    validate_flow()
