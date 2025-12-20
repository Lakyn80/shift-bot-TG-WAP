from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session

from app.modules.attendance.models import Attendance
from app.modules.shifts.models import Shift


class RuleViolation(Exception):
    pass


class AttendanceRules:
    ENABLE_DAILY_LIMIT = True
    ENABLE_WEEKLY_LIMIT = True
    ENABLE_MIN_REST = True
    ENABLE_OVERLAP_CHECK = True

    MAX_HOURS_PER_DAY = 8
    MAX_HOURS_PER_WEEK = 40
    MIN_REST_HOURS = 11


# ======================================================
# HELPERS
# ======================================================
def _shift_bounds(shift: Shift):
    start = datetime.combine(shift.date, shift.start_time)
    end = datetime.combine(shift.date, shift.end_time)
    if end <= start:
        end += timedelta(days=1)
    return start, end


def _shift_hours(shift: Shift) -> float:
    start, end = _shift_bounds(shift)
    return (end - start).total_seconds() / 3600


# ======================================================
# RULE ORCHESTRATOR (OČEKÁVANÝ TESTY)
# ======================================================
def apply_all_rules(db: Session, user_id: int, shift: Shift):
    check_no_duplicate_checkin(db, user_id)
    check_max_hours_per_day(db, user_id, shift)
    check_max_hours_per_week(db, user_id, shift)
    check_min_rest_between_shifts(db, user_id, shift)


# ======================================================
# RULES
# ======================================================
def check_no_duplicate_checkin(db: Session, user_id: int):
    open_att = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user_id,
            Attendance.check_out.is_(None),
        )
        .first()
    )
    if open_att:
        raise RuleViolation("Already checked in")


def check_max_hours_per_day(db: Session, user_id: int, new_shift: Shift):
    if not AttendanceRules.ENABLE_DAILY_LIMIT:
        return

    target_day: date = new_shift.date
    new_hours = _shift_hours(new_shift)

    rows = (
        db.query(Attendance, Shift)
        .join(Shift, Attendance.shift_id == Shift.id)
        .filter(
            Attendance.user_id == user_id,
            Shift.date == target_day,
            Attendance.check_out.isnot(None),
        )
        .all()
    )

    total = sum(_shift_hours(s) for _, s in rows) + new_hours
    if total > AttendanceRules.MAX_HOURS_PER_DAY:
        raise RuleViolation("Daily hours limit exceeded")


def check_max_hours_per_week(db: Session, user_id: int, new_shift: Shift):
    if not AttendanceRules.ENABLE_WEEKLY_LIMIT:
        return

    new_start, _ = _shift_bounds(new_shift)
    week_start = new_start.date() - timedelta(days=new_start.weekday())
    week_end = week_start + timedelta(days=7)

    new_hours = _shift_hours(new_shift)

    rows = (
        db.query(Attendance, Shift)
        .join(Shift, Attendance.shift_id == Shift.id)
        .filter(
            Attendance.user_id == user_id,
            Shift.date >= week_start,
            Shift.date < week_end,
            Attendance.check_out.isnot(None),
        )
        .all()
    )

    total = sum(_shift_hours(s) for _, s in rows) + new_hours
    if total > AttendanceRules.MAX_HOURS_PER_WEEK:
        raise RuleViolation("Weekly hours limit exceeded")


def check_min_rest_between_shifts(db: Session, user_id: int, new_shift: Shift):
    if not AttendanceRules.ENABLE_MIN_REST:
        return

    new_start, _ = _shift_bounds(new_shift)

    last = (
        db.query(Attendance, Shift)
        .join(Shift, Attendance.shift_id == Shift.id)
        .filter(
            Attendance.user_id == user_id,
            Attendance.check_out.isnot(None),
        )
        .order_by(Shift.date.desc(), Shift.end_time.desc())
        .first()
    )

    if not last:
        return

    _, last_shift = last
    _, last_end = _shift_bounds(last_shift)

    rest_hours = (new_start - last_end).total_seconds() / 3600
    if rest_hours < AttendanceRules.MIN_REST_HOURS:
        raise RuleViolation("Minimum rest time not respected")
