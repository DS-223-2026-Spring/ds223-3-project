"""
User endpoints internal admin CRUD.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas import UserCreate, QuizResponse

router = APIRouter()


@router.get("/")
def list_users(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM users")).mappings().all()
    return [dict(r) for r in rows]


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    row = db.execute(
        text("SELECT * FROM users WHERE user_id = :uid"),
        {"uid": user_id},
    ).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(row)


@router.post("/", response_model=QuizResponse)
def create_user(body: UserCreate, db: Session = Depends(get_db)):
    row = db.execute(
        text("""INSERT INTO users (age, gender, district, data_source)
                VALUES (:a, :g, :d, 'real')
                RETURNING user_id"""),
        {"a": body.age, "g": body.gender, "d": body.district},
    ).first()
    db.commit()
    return QuizResponse(user_id=row[0], message="User created successfully")


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("DELETE FROM users WHERE user_id = :uid"),
        {"uid": user_id},
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User and all related data deleted"}
