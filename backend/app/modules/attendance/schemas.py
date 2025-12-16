from pydantic import BaseModel
from datetime import datetime


class AttendanceCheckIn(BaseModel):
    user_id: int
    shift_id: int


class AttendanceRead(BaseModel):
    id: int
    user_id: int
    shift_id: int
    check_in: datetime | None
    check_out: datetime | None

    class Config:
        from_attributes = True
