"""Reusable SQLAlchemy engine and session for the database service."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "activityhub")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASSWORD", "admin")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """Returns a new SQLAlchemy session. Caller must close it."""
    return SessionLocal()


def test_connection() -> bool:
    """Verifies DB connection works. Returns True on success."""
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"DB connection failed: {e}")
        return False


if __name__ == "__main__":
    print("OK" if test_connection() else "FAIL")
