from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from app.database import get_db
from app.deps import get_current_user
from app.models import Plant, User, Watering
from app.schemas import WateringCreate, WateringOut

router = APIRouter(prefix="/api/plants/{plant_id}/waterings", tags=["Поливы"])

def get_owned_plant(db: Session, plant_id: int, user_id: int):
    plant = db.execute(select(Plant).where(Plant.id == plant_id, Plant.owner_id == user_id)).scalar_one_or_none()
    if plant is None:
        raise HTTPException(status_code=404, detail="Растение не найдено")
    return plant

@router.get("", response_model=list[WateringOut])
def list_waterings(plant_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    get_owned_plant(db, plant_id, user.id)
    return db.execute(select(Watering).where(Watering.plant_id == plant_id).order_by(Watering.watered_at.desc())).scalars().all()

@router.post("", response_model=WateringOut, status_code=201)
def create_watering(plant_id: int, data: WateringCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plant = get_owned_plant(db, plant_id, user.id)
    watering = Watering(**data.model_dump(), plant_id=plant.id)
    db.add(watering)
    from datetime import date
    plant.last_watered = date.today()
    db.commit(); db.refresh(watering)
    return watering

@router.delete("/{watering_id}", status_code=204)
def delete_watering(plant_id: int, watering_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    get_owned_plant(db, plant_id, user.id)
    result = db.execute(delete(Watering).where(Watering.id == watering_id, Watering.plant_id == plant_id))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Запись о поливе не найдена")
    db.commit()
