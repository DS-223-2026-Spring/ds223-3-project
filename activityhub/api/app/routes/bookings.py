from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas import BookingRequest, BookingResponse

router = APIRouter()


@router.post("/", response_model=BookingResponse)
def create_booking(body: BookingRequest, db: Session = Depends(get_db)):
    row = db.execute(
        text("""INSERT INTO bookings (user_id, class_id, feedback)
                VALUES (:uid, :cid, :fb)
                RETURNING booking_id"""),
        {"uid": body.user_id, "cid": body.class_id, "fb": body.feedback},
    ).first()
    db.commit()
    return BookingResponse(booking_id=row[0], message="Feedback recorded")


@router.get("/{user_id}")
def list_user_bookings(user_id: int, db: Session = Depends(get_db)):
    rows = db.execute(
        text("""SELECT b.booking_id, b.class_id, b.feedback, b.booked_at,
                       c.studio_name, c.activity_type, c.style
                FROM bookings b
                JOIN classes c ON b.class_id = c.class_id
                WHERE b.user_id = :uid
                ORDER BY b.booked_at DESC"""),
        {"uid": user_id},
    ).mappings().all()
    return [dict(r) for r in rows]
