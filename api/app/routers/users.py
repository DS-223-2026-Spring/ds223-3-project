from fastapi import APIRouter

from app.models.schemas import UserCreate, QuizResponse

router = APIRouter()

DUMMY_USER = {
    "user_id": 1,
    "age": 23,
    "gender": "female",
    "activity_interest": ["yoga", "dance"],
    "preferred_style": "flow",
    "experience_level": "beginner",
    "group_preference": "group",
    "energy_preference": "low",
    "structure_preference": "flexible",
    "goal": "stress relief",
}


@router.post("/", response_model=QuizResponse)
def create_user(body: UserCreate):
    return QuizResponse(user_id=1, message="Quiz submitted successfully")


@router.get("/{user_id}")
def get_user(user_id: int):
    return {**DUMMY_USER, "user_id": user_id}


@router.put("/{user_id}", response_model=QuizResponse)
def update_user(user_id: int, body: UserCreate):
    return QuizResponse(user_id=user_id, message="Quiz updated successfully")


@router.delete("/{user_id}")
def delete_user(user_id: int):
    return {"message": "Quiz deleted successfully"}
