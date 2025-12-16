from datetime import datetime
from sqlalchemy.orm import Session

from app.modules.attendance.models import Attendance


def check_in(db: Session, user_id: int, shift_id: int) -> Attendance:
    record = Attendance(
        user_id=user_id,
        shift_id=shift_id,
        check_in=datetime.utcnow(),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def check_out(db: Session, attendance_id: int) -> Attendance:
    record = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if record is None:
        raise ValueError("Attendance record not found")

    record.check_out = datetime.utcnow()
    db.commit()
    db.refresh(record)
    return record
