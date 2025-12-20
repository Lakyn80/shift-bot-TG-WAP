from datetime import date, time
from pydantic import BaseModel


class ShiftBase(BaseModel):
    name: str
    date: date
    start_time: time
    end_time: time
    location: str | None = None
    max_workers: int | None = None


class ShiftCreate(ShiftBase):
    pass


class ShiftRead(ShiftBase):
    id: int

    class Config:
        from_attributes = True
