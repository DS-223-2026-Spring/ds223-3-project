"""
User endpoints internal admin CRUD.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas import UserCreate, QuizResponse

router = APIRouter()


@router.get("/", summary="List all users")
def list_users(db: Session = Depends(get_db)):
    """
    Returns an array of all registered ActivityHub users with fields: user_id, age, gender, district, and data_source.
    Intended for internal admin use only — not exposed in the user-facing app.
    Each record reflects the user's demographic information and whether they are a real or synthetic data entry.
    """
    rows = db.execute(text("SELECT * FROM users")).mappings().all()
    return [dict(r) for r in rows]


@router.get("/{user_id}", summary="Get user by ID")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Accepts user_id as a path parameter and returns the matching user's profile fields: user_id, age, gender, district, and data_source.
    Returns 404 if no user with that ID exists in the ActivityHub database.
    """
    row = db.execute(
        text("SELECT * FROM users WHERE user_id = :uid"),
        {"uid": user_id},
    ).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(row)


@router.post("/", response_model=QuizResponse, summary="Create a new user")
def create_user(body: UserCreate, db: Session = Depends(get_db)):
    """
    Accepts age (int), gender (str), and district (str) in the request body and creates a new ActivityHub user record.
    Returns the generated user_id — the frontend should store this and immediately redirect to the quiz submission flow.
    """
    row = db.execute(
        text("""INSERT INTO users (age, gender, district, data_source)
                VALUES (:a, :g, :d, 'real')
                RETURNING user_id"""),
        {"a": body.age, "g": body.gender, "d": body.district},
    ).first()
    db.commit()
    return QuizResponse(user_id=row[0], message="User created successfully")


@router.delete("/{user_id}", summary="Delete user by ID")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Accepts user_id as a path parameter and permanently removes the user along with all associated data (quiz responses, recommendations, bookings).
    Returns 404 if the user does not exist. This action cannot be undone.
    """
    result = db.execute(
        text("DELETE FROM users WHERE user_id = :uid"),
        {"uid": user_id},
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User and all related data deleted"}
