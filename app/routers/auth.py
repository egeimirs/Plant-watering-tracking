from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserOut
from app.security import hash_password, verify_password
from app.deps import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Авторизация"])

@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    exists = db.execute(select(User).where(User.username == data.username)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Такой логин уже занят")
    user = User(username=data.username, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=UserOut)
def login(data: UserLogin, request: Request, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.username == data.username)).scalar_one_or_none()
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    request.session["user_id"] = user.id
    return user

@router.post("/logout", status_code=204)
def logout(request: Request):
    request.session.clear()

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
