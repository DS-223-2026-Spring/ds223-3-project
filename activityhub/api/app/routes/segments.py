"""
Reads from segments table ds/scripts/segment_users.py.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas import Segment, SegmentCreate

router = APIRouter()


@router.get("/", response_model=list[Segment], summary="List all segments")
def list_segments(db: Session = Depends(get_db)):
    """
    Returns an array of all ActivityHub user segments ordered by size (largest first).
    Each object includes segment_id, segment_name, description, size (number of users), and booking_likelihood.
    Used by the studio dashboard to display audience cluster breakdowns and targeting insights.
    """
    rows = db.execute(
        text("SELECT * FROM segments ORDER BY size DESC")
    ).mappings().all()
    return [Segment(**dict(r)) for r in rows]


@router.get("/studio/{studio_id}", response_model=list[Segment], summary="Segments by studio")
def segments_by_studio(studio_id: int, db: Session = Depends(get_db)):
    """
    Returns segments composed of users whose recommendations include classes
    from the given studio. Joins recommendations -> classes -> studios and
    aggregates by user_segments.
    """
    rows = db.execute(
        text("""
            SELECT s.segment_id, s.segment_name, s.description,
                   COUNT(DISTINCT us.user_id) AS size,
                   s.booking_likelihood
            FROM recommendations r
            JOIN classes c ON r.class_id = c.class_id
            JOIN user_segments us ON r.user_id = us.user_id
            JOIN segments s ON us.segment_id = s.segment_id
            WHERE c.studio_id = :sid
            GROUP BY s.segment_id, s.segment_name, s.description, s.booking_likelihood
            ORDER BY size DESC
        """),
        {"sid": studio_id},
    ).mappings().all()
    return [Segment(**dict(r)) for r in rows]

@router.get("/{segment_id}", response_model=Segment, summary="Get segment by ID")
def get_segment(segment_id: int, db: Session = Depends(get_db)):
    """
    Accepts segment_id as a path parameter and returns one segment's full details: segment_id, segment_name, description, size (user count), and booking_likelihood (float 0–1 probability).
    Returns 404 if the segment does not exist.
    """
    row = db.execute(
        text("SELECT * FROM segments WHERE segment_id = :sid"),
        {"sid": segment_id},
    ).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Segment not found")
    return Segment(**dict(row))


@router.post("/", summary="Create a segment")
def create_segment(body: SegmentCreate, db: Session = Depends(get_db)):
    """
    Accepts segment_name (str), description (str), size (int), and booking_likelihood (float 0–1) in the request body.
    Creates a new ActivityHub user segment record and returns the generated segment_id.
    Segments are normally produced by the automated segmentation pipeline — use this endpoint for manual additions or testing.
    """
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


@router.delete("/{segment_id}", summary="Delete a segment")
def delete_segment(segment_id: int, db: Session = Depends(get_db)):
    """
    Accepts segment_id as a path parameter and permanently removes the segment record.
    Returns 404 if no segment with that ID exists.
    """
    result = db.execute(
        text("DELETE FROM segments WHERE segment_id = :sid"),
        {"sid": segment_id},
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Segment not found")
    return {"message": "Segment deleted successfully"}
