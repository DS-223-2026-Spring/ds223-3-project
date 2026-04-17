from fastapi import APIRouter

from app.models.schemas import QuizRequest, QuizResponse

router = APIRouter()

DUMMY_ANSWERS = {
    "user_id": 1,
    "age_group": "18-25",
    "preferred_activities": ["yoga", "dance"],
    "availability": ["weekday_evenings", "weekend_mornings"],
    "budget_amd": 15000,
    "location_preference": "Kentron",
    "experience_level": "beginner",
}


@router.post("/", response_model=QuizResponse)
def submit_quiz(body: QuizRequest):
    return QuizResponse(user_id=1, message="Quiz submitted successfully")


@router.get("/{user_id}")
def get_quiz(user_id: int):
    return {**DUMMY_ANSWERS, "user_id": user_id}


@router.put("/{user_id}", response_model=QuizResponse)
def update_quiz(user_id: int, body: QuizRequest):
    return QuizResponse(user_id=user_id, message="Quiz updated successfully")


@router.delete("/{user_id}")
def delete_quiz(user_id: int):
    return {"message": "Quiz deleted successfully"}
