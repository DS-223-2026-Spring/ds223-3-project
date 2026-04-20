from fastapi import APIRouter

from app.models.schemas import Segment, SegmentCreate

router = APIRouter()

DUMMY_SEGMENTS = [
    Segment(segment_id=1, segment_name="Active Young Adults", description="Ages 18-30, prefer evening classes, high activity variety", size=420, booking_likelihood=0.78),
    Segment(segment_id=2, segment_name="Wellness Seekers", description="Ages 28-45, prefer yoga and pilates, weekend mornings", size=310, booking_likelihood=0.65),
    Segment(segment_id=3, segment_name="Budget Conscious Students", description="Ages 18-24, price-sensitive, flexible schedule", size=255, booking_likelihood=0.52),
]


@router.get("/", response_model=list[Segment])
def list_segments():
    return DUMMY_SEGMENTS


@router.get("/{segment_id}", response_model=Segment)
def get_segment(segment_id: int):
    return next((s for s in DUMMY_SEGMENTS if s.segment_id == segment_id), DUMMY_SEGMENTS[0])


@router.post("/")
def create_segment(body: SegmentCreate):
    return {"message": "Segment created successfully"}


@router.delete("/{segment_id}")
def delete_segment(segment_id: int):
    return {"message": "Segment deleted successfully"}
