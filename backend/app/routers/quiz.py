from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def quiz():
    return {"message": "coming soon"}
