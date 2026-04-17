from fastapi import APIRouter

from app.models.schemas import RecommendRequest, RecommendResponse, RecommendedClass

router = APIRouter()

DUMMY_RECOMMENDATIONS = [
    RecommendedClass(class_name="Morning Vinyasa Flow", studio="ArmYoga Center", match_score=0.95, schedule="Mon/Wed/Fri 08:00", price_amd=12000),
    RecommendedClass(class_name="Latin Dance Beginner", studio="Cascade Dance Studio", match_score=0.88, schedule="Tue/Thu 19:00", price_amd=15000),
    RecommendedClass(class_name="Pilates Core", studio="FitLife Yerevan", match_score=0.81, schedule="Sat 10:00", price_amd=10000),
]


@router.post("/", response_model=RecommendResponse)
def recommend(body: RecommendRequest):
    return RecommendResponse(user_id=body.user_id, recommendations=DUMMY_RECOMMENDATIONS)


@router.get("/{user_id}", response_model=RecommendResponse)
def get_recommendations(user_id: int):
    return RecommendResponse(user_id=user_id, recommendations=DUMMY_RECOMMENDATIONS)
