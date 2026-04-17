from fastapi import APIRouter
from typing import Any

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


@router.post("/")
def submit_quiz(body: dict[str, Any]):
    return {"user_id": 1, "message": "Quiz submitted successfully"}


@router.get("/{user_id}")
def get_quiz(user_id: int):
    return {**DUMMY_ANSWERS, "user_id": user_id}


@router.put("/{user_id}")
def update_quiz(user_id: int, body: dict[str, Any]):
    return {"message": "Quiz updated successfully"}


@router.delete("/{user_id}")
def delete_quiz(user_id: int):
    return {"message": "Quiz deleted successfully"}
