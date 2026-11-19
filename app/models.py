from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    plants: Mapped[list["Plant"]] = relationship(back_populates="owner", cascade="all, delete-orphan")

class Plant(Base):
    __tablename__ = "plants"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    species: Mapped[str | None] = mapped_column(String(100))
    room: Mapped[str | None] = mapped_column(String(100))
    watering_interval: Mapped[int] = mapped_column(Integer, default=7, nullable=False)
    last_watered: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    owner: Mapped["User"] = relationship(back_populates="plants")
    waterings: Mapped[list["Watering"]] = relationship(back_populates="plant", cascade="all, delete-orphan")

class Watering(Base):
    __tablename__ = "waterings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    watered_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    amount_ml: Mapped[int] = mapped_column(Integer, default=200, nullable=False)
    fertilizer_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    note: Mapped[str | None] = mapped_column(String(300))
    plant_id: Mapped[int] = mapped_column(ForeignKey("plants.id"), nullable=False, index=True)
    plant: Mapped["Plant"] = relationship(back_populates="waterings")
