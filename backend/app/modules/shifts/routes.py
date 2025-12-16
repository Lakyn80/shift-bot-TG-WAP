from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.modules.shifts import schemas, service
from app.modules.shifts.schemas_assignment import (
    ShiftAssignmentCreate,
    ShiftAssignmentRead,
)
from app.modules.rules.service import RuleViolation

router = APIRouter(prefix="/shifts", tags=["shifts"])


@router.post("/", response_model=schemas.ShiftRead)
def create_shift(
    payload: schemas.ShiftCreate,
    db: Session = Depends(get_db),
):
    return service.create_shift(db, payload)


@router.get("/", response_model=list[schemas.ShiftRead])
def list_shifts(
    db: Session = Depends(get_db),
):
    return service.list_shifts(db)


@router.post("/assign", response_model=ShiftAssignmentRead)
def assign_user(
    payload: ShiftAssignmentCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.assign_user_to_shift(
            db,
            shift_id=payload.shift_id,
            user_id=payload.user_id,
        )
    except RuleViolation as e:
        raise HTTPException(status_code=400, detail=str(e))
