from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.database import get_db
from app.deps import get_current_user
from app.models import Plant, Watering, User

router = APIRouter(prefix="/api/stats", tags=["Статистика"])

@router.get("")
def get_stats(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plants_count = db.execute(select(func.count(Plant.id)).where(Plant.owner_id == user.id)).scalar_one()
    watering_count = db.execute(
        select(func.count(Watering.id)).join(Plant).where(Plant.owner_id == user.id)
    ).scalar_one()
    today = date.today()
    plants = db.execute(select(Plant).where(Plant.owner_id == user.id, Plant.is_active == True)).scalars().all()
    due = sum(1 for p in plants if (p.last_watered or date.min) + timedelta(days=p.watering_interval) <= today)
    return {"plants": plants_count, "waterings": watering_count, "need_water": due}
