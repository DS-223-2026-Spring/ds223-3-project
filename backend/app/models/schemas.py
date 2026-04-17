from pydantic import BaseModel


# Quiz schemas
class QuizRequest(BaseModel):
    age_group: str
    preferred_activities: list[str]
    availability: list[str]
    budget_amd: int
    location_preference: str
    experience_level: str


class QuizResponse(BaseModel):
    user_id: int
    message: str


# Studio schemas
class Studio(BaseModel):
    id: int
    name: str
    location: str
    activity_type: str


class StudioCreate(BaseModel):
    name: str
    location: str
    activity_type: str


class StudioResponse(BaseModel):
    message: str
    studio_id: int


# Recommendation schemas
class RecommendRequest(BaseModel):
    user_id: int


class RecommendedClass(BaseModel):
    class_name: str
    studio: str
    match_score: float
    schedule: str
    price_amd: int


class RecommendResponse(BaseModel):
    user_id: int
    recommendations: list[RecommendedClass]


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
