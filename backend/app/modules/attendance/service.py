from datetime import datetime
import csv
from io import StringIO

from sqlalchemy.orm import Session

from app.modules.attendance.models import Attendance
from app.modules.attendance.schemas import AttendanceCheckIn, AttendanceManualEdit
from app.modules.shifts.models import Shift
from app.modules.rules.service import apply_all_rules


def check_in(db: Session, payload: AttendanceCheckIn):
    shift = db.query(Shift).get(payload.shift_id)
    if not shift:
        raise ValueError("Shift not found")

    apply_all_rules(db, payload.user_id, shift)

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
    attendance = db.query(Attendance).get(attendance_id)
    if not attendance:
        raise ValueError("Attendance not found")

    attendance.check_out = datetime.utcnow()
    db.commit()
    db.refresh(attendance)
    return attendance


def manual_edit(db: Session, attendance_id: int, payload: AttendanceManualEdit):
    attendance = db.query(Attendance).get(attendance_id)
    if not attendance:
        raise ValueError("Attendance not found")

    attendance.check_in = payload.check_in
    attendance.check_out = payload.check_out

    db.commit()
    db.refresh(attendance)
    return attendance


def hours_daily(db: Session):
    rows = db.query(Attendance).filter(Attendance.check_out.isnot(None)).all()

    total_hours = 0.0
    for a in rows:
        total_hours += (a.check_out - a.check_in).total_seconds() / 3600

    return {"total_hours": total_hours}


def hours_monthly(db: Session):
    rows = db.query(Attendance).filter(Attendance.check_out.isnot(None)).all()

    total_hours = 0.0
    for a in rows:
        total_hours += (a.check_out - a.check_in).total_seconds() / 3600

    return {"total_hours": total_hours}


def export_csv(db: Session):
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["attendance_id", "user_id", "shift_id", "check_in", "check_out"])

    rows = db.query(Attendance).all()
    for a in rows:
        writer.writerow([
            a.id,
            a.user_id,
            a.shift_id,
            a.check_in,
            a.check_out,
        ])

    return output.getvalue()
