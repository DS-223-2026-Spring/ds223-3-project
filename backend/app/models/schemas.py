from pydantic import BaseModel


# User schemas
class UserCreate(BaseModel):
    age: int
    gender: str
    activity_interest: list[str]
    preferred_style: str | None = None
    experience_level: str
    group_preference: str
    energy_preference: str
    structure_preference: str
    goal: str


# Quiz schemas
class QuizRequest(BaseModel):
    age: int
    gender: str
    activity_interest: list[str]
    preferred_style: str | None = None
    experience_level: str
    group_preference: str
    energy_preference: str
    structure_preference: str
    goal: str


class QuizResponse(BaseModel):
    user_id: int
    message: str


# Studio schemas
class Studio(BaseModel):
    studio_id: int
    name: str
    district: str
    address: str
    instagram: str | None = None
    price_tier: str
    studio_type: str


class StudioCreate(BaseModel):
    name: str
    district: str
    address: str
    instagram: str | None = None
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
