from fastapi import APIRouter

from app.models.schemas import RecommendRequest, RecommendResponse, RecommendationResponse

router = APIRouter()

DUMMY_RECOMMENDATIONS = [
    RecommendationResponse(class_id=1, studio_name="ArmYoga Center", activity_type="yoga", style="vinyasa", day="Monday", time="08:00", price_amd=12000, score=0.95, rank=1),
    RecommendationResponse(class_id=2, studio_name="Cascade Dance Studio", activity_type="dance", style="latin", day="Tuesday", time="19:00", price_amd=15000, score=0.88, rank=2),
    RecommendationResponse(class_id=3, studio_name="FitLife Yerevan", activity_type="pilates", style="core", day="Saturday", time="10:00", price_amd=10000, score=0.81, rank=3),
]


@router.post("/", response_model=RecommendResponse)
def recommend(body: RecommendRequest):
    return RecommendResponse(user_id=body.user_id, recommendations=DUMMY_RECOMMENDATIONS)


@router.get("/{user_id}", response_model=RecommendResponse)
def get_recommendations(user_id: int):
    return RecommendResponse(user_id=user_id, recommendations=DUMMY_RECOMMENDATIONS)
