from fastapi import APIRouter

from app.models.schemas import Studio, StudioCreate, StudioResponse

router = APIRouter()

DUMMY_STUDIOS = [
    Studio(id=1, name="Cascade Dance Studio", location="Kentron, Yerevan", activity_type="dance"),
    Studio(id=2, name="ArmYoga Center", location="Arabkir, Yerevan", activity_type="yoga"),
]


@router.get("/", response_model=list[Studio])
def list_studios():
    return DUMMY_STUDIOS


@router.get("/{studio_id}", response_model=Studio)
def get_studio(studio_id: int):
    return next((s for s in DUMMY_STUDIOS if s.id == studio_id), DUMMY_STUDIOS[0])


@router.post("/", response_model=StudioResponse)
def create_studio(body: StudioCreate):
    return StudioResponse(message="Studio created", studio_id=1)


@router.put("/{studio_id}")
def update_studio(studio_id: int, body: StudioCreate):
    return {"message": "Studio updated successfully"}


@router.delete("/{studio_id}")
def delete_studio(studio_id: int):
    return {"message": "Studio deleted successfully"}
