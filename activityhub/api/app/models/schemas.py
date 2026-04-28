from typing import Optional
from pydantic import BaseModel


# User schemas
class UserCreate(BaseModel):
    age: int
    gender: str
    district: Optional[str] = None


# Quiz schemas
class QuizRequest(BaseModel):
    age: int
    gender: str
    district: Optional[str] = None
    experience_level: str
    group_preference: str
    energy_preference: str
    structure_preference: str
    goal: str
    budget_max_amd: Optional[int] = None
    preferred_days: Optional[list[str]] = None
    preferred_time: Optional[str] = None
    max_travel_km: Optional[str] = None


class QuizResponse(BaseModel):
    user_id: int
    message: str


# Studio schemas
class Studio(BaseModel):
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


# Class schemas
class Class(BaseModel):
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


# Recommendation schemas
class RecommendRequest(BaseModel):
    user_id: int


class RecommendationResponse(BaseModel):
    class_id: int
    studio_name: str
    activity_type: str
    style: str
    day: str
    time: str
    price_amd: int
    score: float
    rank: int


class RecommendResponse(BaseModel):
    user_id: int
    recommendations: list[RecommendationResponse]


# Segment schemas
class Segment(BaseModel):
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
