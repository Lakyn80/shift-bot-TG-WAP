from datetime import datetime
import csv
from io import StringIO

from sqlalchemy.orm import Session

from app.modules.attendance.models import Attendance
from app.modules.attendance.schemas import AttendanceCheckIn, AttendanceManualEdit
from app.modules.shifts.models import Shift
from app.modules.rules.service import apply_all_rules


def check_in(db: Session, payload: AttendanceCheckIn):
    shift = db.get(Shift, payload.shift_id)
    if not shift:
        raise ValueError("Shift not found")

    apply_all_rules(db, payload.user_id, shift)

    check_in_time = datetime.combine(shift.date, shift.start_time)

    attendance = Attendance(
        user_id=payload.user_id,
        shift_id=payload.shift_id,
        check_in=check_in_time,
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance


def check_out(db: Session, attendance_id: int):
    attendance = db.get(Attendance, attendance_id)
    if not attendance:
        raise ValueError("Attendance not found")

    if attendance.check_out is not None:
        raise ValueError("Attendance already checked out")

    shift = db.get(Shift, attendance.shift_id)
    if not shift:
        raise ValueError("Shift not found")

    attendance.check_out = datetime.combine(shift.date, shift.end_time)
    db.commit()
    db.refresh(attendance)
    return attendance


def manual_edit(db: Session, attendance_id: int, payload: AttendanceManualEdit):
    attendance = db.get(Attendance, attendance_id)
    if not attendance:
        raise ValueError("Attendance not found")

    attendance.check_in = payload.check_in
    attendance.check_out = payload.check_out

    db.commit()
    db.refresh(attendance)
    return attendance


# =========================
# REPORTS
# =========================

def calculate_daily_hours(db: Session, user_id: int | None = None):
    q = db.query(Attendance).filter(Attendance.check_out.isnot(None))

    if user_id is not None:
        q = q.filter(Attendance.user_id == user_id)

    total_hours = 0.0
    for a in q.all():
        total_hours += (a.check_out - a.check_in).total_seconds() / 3600

    return {"total_hours": total_hours}


def calculate_monthly_hours(
    db: Session,
    user_id: int | None = None,
    from_date=None,
    to_date=None,
):
    q = db.query(Attendance).filter(Attendance.check_out.isnot(None))

    if user_id is not None:
        q = q.filter(Attendance.user_id == user_id)

    if from_date is not None:
        q = q.filter(Attendance.check_in >= from_date)

    if to_date is not None:
        q = q.filter(Attendance.check_out <= to_date)

    total_hours = 0.0
    for a in q.all():
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


# Backwards-compatibility aliases expected by routes/tests
def hours_daily(db: Session):
    return calculate_daily_hours(db)


def hours_monthly(
    db: Session,
    user_id: int | None = None,
    from_date=None,
    to_date=None,
):
    return calculate_monthly_hours(
        db, user_id=user_id, from_date=from_date, to_date=to_date
    )
