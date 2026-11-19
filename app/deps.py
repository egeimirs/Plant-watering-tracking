from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Необходимо войти в аккаунт")
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        request.session.clear()
        raise HTTPException(status_code=401, detail="Сессия недействительна")
    return user
