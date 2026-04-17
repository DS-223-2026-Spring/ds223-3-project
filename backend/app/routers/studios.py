from fastapi import APIRouter
from typing import Any

router = APIRouter()

DUMMY_STUDIOS = [
    {
        "id": 1,
        "name": "Cascade Dance Studio",
        "location": "Kentron, Yerevan",
        "activity_type": "dance",
    },
    {
        "id": 2,
        "name": "ArmYoga Center",
        "location": "Arabkir, Yerevan",
        "activity_type": "yoga",
    },
]


@router.get("/")
def list_studios():
    return DUMMY_STUDIOS


@router.get("/{studio_id}")
def get_studio(studio_id: int):
    return next((s for s in DUMMY_STUDIOS if s["id"] == studio_id), DUMMY_STUDIOS[0])


@router.post("/")
def create_studio(body: dict[str, Any]):
    return {"message": "Studio created", "studio_id": 1}


@router.put("/{studio_id}")
def update_studio(studio_id: int, body: dict[str, Any]):
    return {"message": "Studio updated successfully"}


@router.delete("/{studio_id}")
def delete_studio(studio_id: int):
    return {"message": "Studio deleted successfully"}
