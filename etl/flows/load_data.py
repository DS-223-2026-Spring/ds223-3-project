# Prefect flow: load studio and class CSVs into PostgreSQL.
from prefect import flow, task
import pandas as pd
from sqlalchemy import create_engine, text
import os

DB_URL = (
    f"postgresql://{os.getenv('DB_USER','admin')}:{os.getenv('DB_PASSWORD','admin')}"
    f"@{os.getenv('DB_HOST','db')}:{os.getenv('DB_PORT','5432')}/"
    f"{os.getenv('DB_NAME','activityhub')}"
)


@task
def load_studios(path="model/data/studios.csv"):
    engine = create_engine(DB_URL)
    df = pd.read_csv(path)
    df.to_sql("studios", engine, if_exists="append", index=False)
    return len(df)


@task
def load_classes(path="model/data/classes.csv"):
    engine = create_engine(DB_URL)
    df = pd.read_csv(path)
    df["price_per_session_amd"] = df["price_per_session_amd"].astype("Int64")
    df["price_monthly_amd"] = df["price_monthly_amd"].astype("Int64")
    df.to_sql("classes", engine, if_exists="append", index=False)
    return len(df)


@task
def verify():
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        s = conn.execute(text("SELECT COUNT(*) FROM studios")).scalar()
        c = conn.execute(text("SELECT COUNT(*) FROM classes")).scalar()
    return {"studios": s, "classes": c}


@flow(name="load-data")
def load_data_flow():
    s = load_studios()
    c = load_classes()
    counts = verify()
    print(f"Loaded {s} studios, {c} classes. Final counts: {counts}")
    return counts


if __name__ == "__main__":
    load_data_flow()
