from datetime import datetime
from sqlalchemy.orm import Session

from app.modules.attendance.models import Attendance
from app.modules.shifts.models import Shift


def _shift_bounds(shift: Shift):
    start = datetime.combine(shift.date, shift.start_time)
    end = datetime.combine(shift.date, shift.end_time)
    return start, end


def calculate_daily_hours(
    db: Session,
    user_id: int | None = None,
):
    q = (
        db.query(Attendance, Shift)
        .join(Shift, Attendance.shift_id == Shift.id)
        .filter(Attendance.check_out.isnot(None))
    )

    if user_id is not None:
        q = q.filter(Attendance.user_id == user_id)

    total = {}

    for a, s in q.all():
        day = s.date.isoformat()
        start, end = _shift_bounds(s)
        total.setdefault(day, 0)
        total[day] += (end - start).total_seconds() / 3600

    return {"total_hours": total}


def calculate_monthly_hours(
    db: Session,
    user_id: int | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
):
    q = (
        db.query(Attendance, Shift)
        .join(Shift, Attendance.shift_id == Shift.id)
        .filter(Attendance.check_out.isnot(None))
    )

    if user_id is not None:
        q = q.filter(Attendance.user_id == user_id)

    total = {}

    for a, s in q.all():
        start, end = _shift_bounds(s)

        if from_date and end < from_date:
            continue
        if to_date and start > to_date:
            continue

        key = s.date.strftime("%Y-%m")
        total.setdefault(key, 0)
        total[key] += (end - start).total_seconds() / 3600

    return {"total_hours": total}
