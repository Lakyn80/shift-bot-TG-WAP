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
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class AttendanceUpdate(BaseModel):
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
