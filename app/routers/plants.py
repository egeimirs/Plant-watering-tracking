from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import delete, func, or_, select, update
from sqlalchemy.orm import Session
from app.database import get_db
from app.deps import get_current_user
from app.models import Plant, User
from app.schemas import PlantCreate, PlantOut, PlantUpdate

router = APIRouter(prefix="/api/plants", tags=["Растения"])

def owned_plant(db: Session, plant_id: int, user_id: int):
    plant = db.execute(select(Plant).where(Plant.id == plant_id, Plant.owner_id == user_id)).scalar_one_or_none()
    if plant is None:
        raise HTTPException(status_code=404, detail="Растение не найдено")
    return plant

@router.get("", response_model=list[PlantOut])
def list_plants(q: str | None = None, needs_water: bool | None = None,
                limit: int = 100, offset: int = 0,
                user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    limit = max(1, min(limit, 100))
    stmt = select(Plant).where(Plant.owner_id == user.id)
    if q:
        stmt = stmt.where(or_(Plant.name.ilike(f"%{q}%"), func.casefold(Plant.name).like(func.casefold(f"%{q}%"))))
    plants = db.execute(stmt.order_by(Plant.name).limit(limit).offset(max(offset, 0))).scalars().all()
    if needs_water is not None:
        today = date.today()
        plants = [p for p in plants if ((p.last_watered or date.min) + timedelta(days=p.watering_interval) <= today) == needs_water]
    return plants

@router.get("/{plant_id}", response_model=PlantOut)
def get_plant(plant_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return owned_plant(db, plant_id, user.id)

@router.post("", response_model=PlantOut, status_code=201)
def create_plant(data: PlantCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plant = Plant(**data.model_dump(), owner_id=user.id)
    db.add(plant); db.commit(); db.refresh(plant)
    return plant

@router.patch("/{plant_id}", response_model=PlantOut)
def update_plant(plant_id: int, data: PlantUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    changes = data.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=422, detail="Не переданы поля для изменения")
    result = db.execute(update(Plant).where(Plant.id == plant_id, Plant.owner_id == user.id).values(**changes))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Растение не найдено")
    db.commit()
    return owned_plant(db, plant_id, user.id)

@router.delete("/{plant_id}", status_code=204)
def delete_plant(plant_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plant = owned_plant(db, plant_id, user.id)
    db.delete(plant)
    db.commit()
