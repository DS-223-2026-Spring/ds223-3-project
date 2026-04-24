# etl/config.py
import os

DATA_DIR = os.getenv("DATA_DIR", "data/")
MODEL_DIR = os.getenv("MODEL_DIR", "model/models/")

STUDIO_CSV = os.path.join(DATA_DIR, "studios.csv")
CLASS_CSV = os.path.join(DATA_DIR, "classes.csv")
SURVEY_CSV = os.path.join(DATA_DIR, "survey.csv")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "activityhub"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "admin"),
}
