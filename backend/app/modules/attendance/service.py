from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.attendance.models import Attendance
from app.modules.shifts.models import Shift


def check_in(db: Session, payload):
    shift = db.query(Shift).filter(Shift.id == payload.shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    if shift.max_workers is None:
        raise HTTPException(status_code=500, detail="Shift max_workers not set")

    existing = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == payload.user_id,
            Attendance.shift_id == payload.shift_id,
            Attendance.check_out.is_(None),
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="User already checked in")

    active_count = (
        db.query(Attendance)
        .filter(
            Attendance.shift_id == payload.shift_id,
            Attendance.check_out.is_(None),
        )
        .count()
    )

    if active_count >= shift.max_workers:
        raise HTTPException(status_code=409, detail="Shift capacity full")

    attendance = Attendance(
        user_id=payload.user_id,
        shift_id=payload.shift_id,
        check_in=datetime.utcnow(),
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance


def check_out(db: Session, attendance_id: int):
    attendance = (
        db.query(Attendance)
        .filter(
            Attendance.id == attendance_id,
            Attendance.check_out.is_(None),
        )
        .first()
    )

    if not attendance:
        raise HTTPException(
            status_code=409,
            detail="Attendance not found or already checked out",
        )

    attendance.check_out = datetime.utcnow()
    db.commit()
    db.refresh(attendance)
    return attendance
def manual_update(db: Session, attendance_id: int, data):
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()

    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")

    if data.check_in is not None:
        attendance.check_in = data.check_in

    if data.check_out is not None:
        attendance.check_out = data.check_out

    db.commit()
    db.refresh(attendance)
    return attendance
