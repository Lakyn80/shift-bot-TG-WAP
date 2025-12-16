from pydantic import BaseModel
from enum import Enum


class UserRole(str, Enum):
    employee = "employee"
    manager = "manager"
    admin = "admin"


class UserBase(BaseModel):
    full_name: str
    role: UserRole
    is_active: bool = True


class UserCreate(UserBase):
    telegram_id: str | None = None
    whatsapp_id: str | None = None


class UserRead(UserBase):
    id: int
    telegram_id: str | None
    whatsapp_id: str | None

    class Config:
        from_attributes = True
