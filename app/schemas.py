from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str

class PlantCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    species: str | None = Field(default=None, max_length=100)
    room: str | None = Field(default=None, max_length=100)
    watering_interval: int = Field(default=7, ge=1, le=90)
    last_watered: date | None = None
    notes: str | None = None
    is_active: bool = True

class PlantUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    species: str | None = None
    room: str | None = None
    watering_interval: int | None = Field(default=None, ge=1, le=90)
    last_watered: date | None = None
    notes: str | None = None
    is_active: bool | None = None

class PlantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    species: str | None
    room: str | None
    watering_interval: int
    last_watered: date | None
    notes: str | None
    is_active: bool

class WateringCreate(BaseModel):
    amount_ml: int = Field(default=200, ge=1, le=10000)
    fertilizer_used: bool = False
    note: str | None = Field(default=None, max_length=300)

class WateringOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    watered_at: datetime
    amount_ml: int
    fertilizer_used: bool
    note: str | None
    plant_id: int
