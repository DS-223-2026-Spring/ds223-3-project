from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import Studio, StudioCreate, StudioResponse

router = APIRouter()

@router.get("/", response_model=list[Studio])
def list_studios(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM studios")).mappings().all()
    return [Studio(**dict(r)) for r in rows]

@router.get("/{studio_id}", response_model=Studio)
def get_studio(studio_id: int, db: Session = Depends(get_db)):
    row = db.execute(
        text("SELECT * FROM studios WHERE studio_id = :sid"),
        {"sid": studio_id},
    ).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Studio not found")
    return Studio(**dict(row))

@router.post("/", response_model=StudioResponse)
def create_studio(body: StudioCreate, db: Session = Depends(get_db)):
    next_id = db.execute(
        text("SELECT COALESCE(MAX(studio_id), 0) + 1 FROM studios")
    ).scalar()
    db.execute(
        text("""INSERT INTO studios (studio_id, studio_name, district, address,
                                     instagram, price_tier, studio_type)
                VALUES (:sid, :name, :dist, :addr, :ig, :tier, :stype)"""),
        {"sid": next_id, "name": body.studio_name, "dist": body.district,
         "addr": body.address, "ig": body.instagram,
         "tier": body.price_tier, "stype": body.studio_type},
    )
    db.commit()
    return StudioResponse(message="Studio created", studio_id=next_id)

@router.put("/{studio_id}")
def update_studio(studio_id: int, body: StudioCreate, db: Session = Depends(get_db)):
    result = db.execute(
        text("""UPDATE studios
                SET studio_name = :name, district = :dist, address = :addr,
                    instagram = :ig, price_tier = :tier, studio_type = :stype
                WHERE studio_id = :sid"""),
        {"sid": studio_id, "name": body.studio_name, "dist": body.district,
         "addr": body.address, "ig": body.instagram,
         "tier": body.price_tier, "stype": body.studio_type},
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Studio not found")
    return {"message": "Studio updated successfully"}

@router.delete("/{studio_id}")
def delete_studio(studio_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("DELETE FROM studios WHERE studio_id = :sid"),
        {"sid": studio_id},
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Studio not found")
    return {"message": "Studio deleted successfully"}
