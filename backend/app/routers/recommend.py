from fastapi import APIRouter
from typing import Any

router = APIRouter()

DUMMY_RECOMMENDATIONS = [
    {
        "class_name": "Morning Vinyasa Flow",
        "studio": "ArmYoga Center",
        "match_score": 0.95,
        "schedule": "Mon/Wed/Fri 08:00",
        "price_amd": 12000,
    },
    {
        "class_name": "Latin Dance Beginner",
        "studio": "Cascade Dance Studio",
        "match_score": 0.88,
        "schedule": "Tue/Thu 19:00",
        "price_amd": 15000,
    },
    {
        "class_name": "Pilates Core",
        "studio": "FitLife Yerevan",
        "match_score": 0.81,
        "schedule": "Sat 10:00",
        "price_amd": 10000,
    },
]


@router.post("/")
def recommend(body: dict[str, Any]):
    return {"user_id": body.get("user_id", 1), "recommendations": DUMMY_RECOMMENDATIONS}


@router.get("/{user_id}")
def get_recommendations(user_id: int):
    return {"user_id": user_id, "recommendations": DUMMY_RECOMMENDATIONS}
