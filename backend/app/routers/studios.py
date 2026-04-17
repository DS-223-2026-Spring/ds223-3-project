from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def studios():
    return {"message": "coming soon"}
