from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.modules.attendance import schemas, service

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("/check-in", response_model=schemas.AttendanceRead)
def check_in(
    payload: schemas.AttendanceCheckIn,
    db: Session = Depends(get_db),
):
    try:
        return service.check_in(db, payload)
    except HTTPException:
        raise


@router.post("/check-out/{attendance_id}", response_model=schemas.AttendanceRead)
def check_out(attendance_id: int, db: Session = Depends(get_db)):
    try:
        return service.check_out(db, attendance_id)
    except HTTPException:
        raise
