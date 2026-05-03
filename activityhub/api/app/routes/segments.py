"""
Reads from segments table ds/scripts/segment_users.py.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas import Segment, SegmentCreate

router = APIRouter()


@router.get("/", response_model=list[Segment])
def list_segments(db: Session = Depends(get_db)):
    rows = db.execute(
        text("SELECT * FROM segments ORDER BY size DESC")
    ).mappings().all()
    return [Segment(**dict(r)) for r in rows]


@router.get("/{segment_id}", response_model=Segment)
def get_segment(segment_id: int, db: Session = Depends(get_db)):
    row = db.execute(
        text("SELECT * FROM segments WHERE segment_id = :sid"),
        {"sid": segment_id},
    ).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Segment not found")
    return Segment(**dict(row))


@router.post("/")
def create_segment(body: SegmentCreate, db: Session = Depends(get_db)):
    row = db.execute(
        text("""INSERT INTO segments
                (segment_name, description, size, booking_likelihood)
                VALUES (:n, :d, :s, :b)
                RETURNING segment_id"""),
        {"n": body.segment_name, "d": body.description,
         "s": body.size, "b": body.booking_likelihood},
    ).first()
    db.commit()
    return {"segment_id": row[0], "message": "Segment created successfully"}


@router.delete("/{segment_id}")
def delete_segment(segment_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("DELETE FROM segments WHERE segment_id = :sid"),
        {"sid": segment_id},
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Segment not found")
    return {"message": "Segment deleted successfully"}
