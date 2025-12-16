from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.modules.attendance.schemas import AttendanceCheckIn, AttendanceRead
from app.modules.attendance import service

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("/check-in", response_model=AttendanceRead)
def check_in(
    payload: AttendanceCheckIn,
    db: Session = Depends(get_db),
):
    return service.check_in(db, payload.user_id, payload.shift_id)


@router.post("/check-out/{attendance_id}", response_model=AttendanceRead)
def check_out(
    attendance_id: int,
    db: Session = Depends(get_db),
):
    try:
        return service.check_out(db, attendance_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
