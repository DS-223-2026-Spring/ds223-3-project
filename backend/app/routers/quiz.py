from fastapi import APIRouter

from app.models.schemas import QuizRequest, QuizResponse

router = APIRouter()

DUMMY_ANSWERS = {
    "user_id": 1,
    "age": 23,
    "gender": "female",
    "activity_interest": ["yoga", "dance"],
    "preferred_style": "hatha",
    "experience_level": "beginner",
    "group_preference": "group",
    "energy_preference": "calm",
    "structure_preference": "structured",
    "goal": "stress relief",
    "district": "Kentron",
    "budget_max_amd": 15000,
    "preferred_days": ["Monday", "Wednesday", "Friday"],
    "preferred_time": "evening",
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
