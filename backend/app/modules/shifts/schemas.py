from pydantic import BaseModel
from datetime import date, time
from enum import Enum


class ShiftStatus(str, Enum):
    open = "open"
    full = "full"
    cancelled = "cancelled"
    closed = "closed"


class ShiftBase(BaseModel):
    date: date
    start_time: time
    end_time: time
    location: str
    max_workers: int


class ShiftCreate(ShiftBase):
    pass


class ShiftRead(ShiftBase):
    id: int
    status: ShiftStatus

    class Config:
        from_attributes = True
