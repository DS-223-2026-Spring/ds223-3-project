from typing import Any
from sqlalchemy import text
from sqlalchemy.orm import Session

ALLOWED_TABLES = {
    "users", "quiz_responses", "studios", "classes",
    "segments", "user_segments", "recommendations", "bookings"
}

def _validate_table(table: str) -> None:
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Table '{table}' is not allowed.")

def insert_row(session: Session, table: str, data: dict) -> None:
    """Insert a single row. Commits on success."""
    _validate_table(table)
    cols = ", ".join(data.keys())
    placeholders = ", ".join(f":{k}" for k in data.keys())
    session.execute(
        text(f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"),
        data,
    )
    session.commit()


def select_all(session: Session, table: str) -> list[dict]:
    _validate_table(table)
    """Return all rows in a table as a list of dicts."""
    result = session.execute(text(f"SELECT * FROM {table}")).mappings().all()
    return [dict(r) for r in result]


def select_by_id(session: Session, table: str, id_col: str, id_val: Any) -> dict | None:
    """Return one row by primary key. None if not found."""
    _validate_table(table)
    result = session.execute(
        text(f"SELECT * FROM {table} WHERE {id_col} = :id"),
        {"id": id_val},
    ).mappings().first()
    return dict(result) if result else None


def update_row(session: Session, table: str, id_col: str, id_val: Any, data: dict) -> None:
    """Update a row by primary key. Commits on success."""
    _validate_table(table)  
    set_clause = ", ".join(f"{k} = :{k}" for k in data.keys())
    session.execute(
        text(f"UPDATE {table} SET {set_clause} WHERE {id_col} = :id"),
        {**data, "id": id_val},
    )
    session.commit()


def delete_row(session: Session, table: str, id_col: str, id_val: Any) -> None:
    """Delete a row by primary key. Commits on success."""
    _validate_table(table)
    session.execute(
        text(f"DELETE FROM {table} WHERE {id_col} = :id"),
        {"id": id_val},
    )
    session.commit()
