from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas import BookingRequest, BookingResponse

router = APIRouter()


@router.post("/", response_model=BookingResponse, summary="Record a class booking")
def create_booking(body: BookingRequest, db: Session = Depends(get_db)):
    """
    Accepts user_id, class_id, and an optional feedback score in the request body.
    Records that the user attended a class at an ActivityHub partner studio and stores their feedback for recommendation model improvement.
    Returns the generated booking_id.
    """
    row = db.execute(
        text("""INSERT INTO bookings (user_id, class_id, feedback)
                VALUES (:uid, :cid, :fb)
                RETURNING booking_id"""),
        {"uid": body.user_id, "cid": body.class_id, "fb": body.feedback},
    ).first()
    db.commit()
    return BookingResponse(booking_id=row[0], message="Feedback recorded")


@router.get("/{user_id}", summary="List user bookings")
def list_user_bookings(user_id: int, db: Session = Depends(get_db)):
    """
    Accepts user_id as a path parameter and returns a list of all classes the user has booked.
    Each entry is enriched with studio_name, activity_type, style, feedback score, and booked_at timestamp, ordered most recent first.
    Returns an empty list if the user has no bookings yet.
    """
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
