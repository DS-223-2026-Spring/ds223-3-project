"""Loads the three source CSVs (studios, classes, survey) into PostgreSQL tables."""
import pandas as pd
from sqlalchemy import text
from db.connection import engine


def load_studios(csv_path: str = "data/studios.csv") -> int:
    """Load studios.csv into the studios table. Returns row count."""
    df = pd.read_csv(csv_path)
    df.to_sql("studios", engine, if_exists="append", index=False)
    return len(df)


def load_classes(csv_path: str = "data/classes.csv") -> int:
    """Load classes.csv into the classes table. Returns row count."""
    df = pd.read_csv(csv_path)
    # Handle nullable price columns explicitly
    df["price_per_session_amd"] = df["price_per_session_amd"].astype("Int64")
    df["price_monthly_amd"] = df["price_monthly_amd"].astype("Int64")
    df.to_sql("classes", engine, if_exists="append", index=False)
    return len(df)


def row_counts() -> dict:
    """Return current row counts in every table for validation."""
    tables = ["users", "quiz_responses", "studios", "classes",
              "segments", "recommendations"]
    with engine.connect() as conn:
        return {t: conn.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar()
                for t in tables}


if __name__ == "__main__":
    print(f"Studios loaded: {load_studios()}")
    print(f"Classes loaded: {load_classes()}")
    print(f"Row counts: {row_counts()}")
