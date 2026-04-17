from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def segments():
    return {"message": "coming soon"}
