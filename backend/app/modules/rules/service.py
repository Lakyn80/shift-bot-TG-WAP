from sqlalchemy.orm import Session
from sqlalchemy import func as sa_func

from app.modules.shifts.models import Shift
from app.modules.shifts.models_assignment import ShiftAssignment


class RuleViolation(Exception):
    pass


def ensure_shift_exists(db: Session, shift_id: int) -> None:
    if not db.query(Shift).filter(Shift.id == shift_id).first():
        raise RuleViolation("Shift does not exist")


def ensure_not_duplicate_assignment(
    db: Session,
    shift_id: int,
    user_id: int,
) -> None:
    exists = (
        db.query(ShiftAssignment)
        .filter(
            ShiftAssignment.shift_id == shift_id,
            ShiftAssignment.user_id == user_id,
        )
        .first()
    )
    if exists:
        raise RuleViolation("User already assigned to this shift")


def ensure_shift_capacity(
    db: Session,
    shift_id: int,
) -> None:
    assigned_count = (
        db.query(sa_func.count(ShiftAssignment.id))
        .filter(ShiftAssignment.shift_id == shift_id)
        .scalar()
    )

    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if shift is None:
        raise RuleViolation("Shift does not exist")

    if assigned_count >= shift.max_workers:
        raise RuleViolation("Shift is already full")
