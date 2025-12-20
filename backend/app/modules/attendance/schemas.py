from datetime import datetime
from pydantic import BaseModel


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


# === CHYBĚJÍCÍ SCHEMA (PRO MANUAL EDIT) ===
class AttendanceManualEdit(BaseModel):
    check_in: datetime | None
    check_out: datetime | None
