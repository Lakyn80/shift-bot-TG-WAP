from sqlalchemy.orm import Session

from app.modules.shifts import models, schemas
from app.modules.shifts.models_assignment import ShiftAssignment


def create_shift(db: Session, data: schemas.ShiftCreate) -> models.Shift:
    shift = models.Shift(**data.model_dump())
    db.add(shift)
    db.commit()
    db.refresh(shift)
    return shift


def list_shifts(db: Session) -> list[models.Shift]:
    return db.query(models.Shift).all()


def assign_user_to_shift(db: Session, shift_id: int, user_id: int) -> ShiftAssignment:
    assignment = ShiftAssignment(shift_id=shift_id, user_id=user_id)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment
