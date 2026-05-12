from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


# ── User ──────────────────────────────
class UserCreate(BaseModel):
    age: int
    gender: str
    district: Optional[str] = None


# ── Quiz ──────────────────────────────
class QuizRequest(BaseModel):
    age: int = Field(ge=10, le=100)
    gender: str
    district: Optional[str] = None
    experience_level: str
    group_preference: str
    energy_preference: str
    structure_preference: str
    goal: str
    budget_max_amd: Optional[int] = Field(ge=0, default=None)
    preferred_days: Optional[List[str]] = None
    preferred_time: Optional[str] = None
    max_travel_km: Optional[str] = None

    @field_validator("gender")
    @classmethod
    def lowercase_gender(cls, v: str) -> str:
        return v.lower()


class QuizResponse(BaseModel):
    user_id: int
    message: str


# ── Studios ───────────────────────────
class Studio(BaseModel):
    model_config = {"from_attributes": True}

    studio_id: int
    studio_name: str
    district: Optional[str] = None
    address: Optional[str] = None
    instagram: Optional[str] = None
    price_tier: Optional[str] = None
    studio_type: Optional[str] = None


class StudioCreate(BaseModel):
    studio_name: str
    district: str
    address: str
    instagram: Optional[str] = None
    price_tier: str
    studio_type: str


class StudioResponse(BaseModel):
    message: str
    studio_id: int


# ── Classes ───────────────────────────
class Class(BaseModel):
    model_config = {"from_attributes": True}

    class_id: int
    studio_id: int
    activity_type: str
    style: str
    day: str
    time: str
    duration_min: int
    price_amd: int
    experience_required: str
    group_or_private: str
    energy_level: str
    structure_level: str


# ── Recommendations ───────────────────
class RecommendRequest(BaseModel):
    """Triggers ML recommendation pipeline for the given user."""
    user_id: int


class RecommendationResponse(BaseModel):
    model_config = {"from_attributes": True}

    class_id: int
    studio_name: str
    activity_type: str
    style: str
    day: str
    time: str
    price_amd: int = Field(ge=0)
    score: float = Field(ge=0.0, le=1.0)
    rank: int = Field(ge=1)


class RecommendResponse(BaseModel):
    user_id: int
    recommendations: List[RecommendationResponse]


# ── Segments ──────────────────────────
class Segment(BaseModel):
    model_config = {"from_attributes": True}

    segment_id: int
    segment_name: str
    description: str
    size: int
    booking_likelihood: float


class SegmentCreate(BaseModel):
    segment_name: str
    description: str
    size: int
    booking_likelihood: float


# ── Bookings ──────────────────────────
class BookingRequest(BaseModel):
    user_id: int
    class_id: int
    feedback: Optional[str] = None


class BookingResponse(BaseModel):
    booking_id: int
    message: str
