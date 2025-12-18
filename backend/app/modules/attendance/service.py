from datetime import datetime, timedelta
from io import StringIO
import csv

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.attendance.models import Attendance
from app.modules.shifts.models import Shift
from app.modules.attendance.settings import AttendanceRules


# =========================
# RULES LOADER (DÙLEŽITÉ)
# =========================

def get_rules() -> AttendanceRules:
    return AttendanceRules()


# =========================
# HELPERS
# =========================

def _shift_bounds(shift: Shift):
    start = datetime.combine(shift.date, shift.start_time)
    end = datetime.combine(shift.date, shift.end_time)
    if end <= start:
        end += timedelta(days=1)
    return start, end


def _week_bounds(dt: datetime):
    start = (dt - timedelta(days=dt.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return start, start + timedelta(days=7)


# =========================
# CHECK-IN / CHECK-OUT
# =========================

def check_in(db: Session, payload):
    rules = get_rules()  # ?? MUSÍ BÝT TADY, NE GLOBÁLNÌ

    shift = db.query(Shift).filter(Shift.id == payload.shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    shift_start, shift_end = _shift_bounds(shift)
    shift_hours = (shift_end - shift_start).total_seconds() / 3600

    # duplicate check-in
    if db.query(Attendance).filter(
        Attendance.user_id == payload.user_id,
        Attendance.shift_id == payload.shift_id,
        Attendance.check_out.is_(None),
    ).first():
        raise HTTPException(status_code=409, detail="Already checked in")

    # max workers
    active_count = db.query(Attendance).filter(
        Attendance.shift_id == payload.shift_id,
        Attendance.check_out.is_(None),
    ).count()

    if shift.max_workers is not None and active_count >= shift.max_workers:
        raise HTTPException(status_code=409, detail="Shift capacity full")

    # previous attendances
    previous = (
        db.query(Attendance, Shift)
        .join(Shift, Attendance.shift_id == Shift.id)
        .filter(
            Attendance.user_id == payload.user_id,
            Attendance.check_out.isnot(None),
        )
        .all()
    )

    # overlap check
    if rules.ENABLE_OVERLAP_CHECK:
        for _, s in previous:
            s_start, s_end = _shift_bounds(s)
            if not (shift_end <= s_start or shift_start >= s_end):
                raise HTTPException(status_code=409, detail="Overlapping shift")

    # daily hours
    day_hours = 0
    for _, s in previous:
        if s.date == shift.date:
            s_start, s_end = _shift_bounds(s)
            day_hours += (s_end - s_start).total_seconds() / 3600

    if rules.ENABLE_DAILY_LIMIT:
        if day_hours + shift_hours > rules.MAX_HOURS_PER_DAY:
            raise HTTPException(status_code=409, detail="Daily hours exceeded")

    # weekly hours
    w_start, w_end = _week_bounds(shift_start)
    week_hours = 0
    for _, s in previous:
        s_start, s_end = _shift_bounds(s)
        if w_start <= s_start < w_end:
            week_hours += (s_end - s_start).total_seconds() / 3600

    if rules.ENABLE_WEEKLY_LIMIT:
        if week_hours + shift_hours > rules.MAX_HOURS_PER_WEEK:
            raise HTTPException(status_code=409, detail="Weekly hours exceeded")

    # minimum rest
    if rules.ENABLE_MIN_REST and previous:
        last_shift = max(previous, key=lambda x: _shift_bounds(x[1])[1])[1]
        last_end = _shift_bounds(last_shift)[1]
        rest_hours = (shift_start - last_end).total_seconds() / 3600
        if rest_hours < rules.MIN_REST_HOURS:
            raise HTTPException(status_code=409, detail="Minimum rest not met")

    a = Attendance(
        user_id=payload.user_id,
        shift_id=payload.shift_id,
        check_in=datetime.utcnow(),
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


def check_out(db: Session, attendance_id: int):
    a = db.query(Attendance).filter(
        Attendance.id == attendance_id,
        Attendance.check_out.is_(None),
    ).first()
    if not a:
        raise HTTPException(status_code=409, detail="Attendance not found or already checked out")

    a.check_out = datetime.utcnow()
    db.commit()
    db.refresh(a)
    return a


# =========================
# ADMIN / MANAGER ACTIONS
# =========================

def manual_update(db: Session, attendance_id: int, payload):
    a = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Attendance not found")

    if payload.check_in is not None:
        a.check_in = payload.check_in
    if payload.check_out is not None:
        a.check_out = payload.check_out

    db.commit()
    db.refresh(a)
    return a


def export_csv(db: Session):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "user_id", "shift_id", "check_in", "check_out"])

    for a in db.query(Attendance).all():
        writer.writerow([
            a.id,
            a.user_id,
            a.shift_id,
            a.check_in,
            a.check_out,
        ])

    return output.getvalue()


def calculate_daily_hours(db: Session):
    rows = db.query(Attendance).filter(
        Attendance.check_in.isnot(None),
        Attendance.check_out.isnot(None),
    ).all()

    total_seconds = sum(
        (a.check_out - a.check_in).total_seconds() for a in rows
    )
    return {"total_hours": round(total_seconds / 3600, 2)}


def calculate_monthly_hours(db: Session):
    rows = db.query(Attendance).filter(
        Attendance.check_in.isnot(None),
        Attendance.check_out.isnot(None),
    ).all()

    total_seconds = sum(
        (a.check_out - a.check_in).total_seconds() for a in rows
    )
    return {"total_hours": round(total_seconds / 3600, 2)}
