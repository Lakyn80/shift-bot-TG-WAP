from fastapi import APIRouter, Depends, HTTPException, Header, Response
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.modules.attendance import schemas, service
from app.modules.users.models import User

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("/check-in", response_model=schemas.AttendanceRead)
def check_in(
    payload: schemas.AttendanceCheckIn,
    db: Session = Depends(get_db),
):
    return service.check_in(db, payload)


@router.post("/check-out/{attendance_id}", response_model=schemas.AttendanceRead)
def check_out(attendance_id: int, db: Session = Depends(get_db)):
    return service.check_out(db, attendance_id)


@router.patch("/{attendance_id}", response_model=schemas.AttendanceRead)
def manual_edit_attendance(
    attendance_id: int,
    payload: schemas.AttendanceUpdate,
    db: Session = Depends(get_db),
    x_user_id: str = Header(...),
):
    user = db.query(User).filter(User.id == int(x_user_id)).first()

    if not user or user.role.value not in ("manager", "admin"):
        raise HTTPException(status_code=403, detail="Forbidden")

    return service.manual_update(db, attendance_id, payload)


@router.get("/export/csv")
def export_attendance_csv(
    db: Session = Depends(get_db),
    x_user_id: str = Header(...),
):
    user = db.query(User).filter(User.id == int(x_user_id)).first()

    if not user or user.role.value not in ("manager", "admin"):
        raise HTTPException(status_code=403, detail="Forbidden")

    csv_data = service.export_csv(db)

    return Response(content=csv_data, media_type="text/csv")


@router.get("/hours/daily")
def attendance_hours_daily(
    db: Session = Depends(get_db),
    x_user_id: str = Header(...),
):
    user = db.query(User).filter(User.id == int(x_user_id)).first()

    if not user or user.role.value not in ("manager", "admin"):
        raise HTTPException(status_code=403, detail="Forbidden")

    return service.calculate_daily_hours(db)


@router.get("/hours/monthly")
def attendance_hours_monthly(
    db: Session = Depends(get_db),
    x_user_id: str = Header(...),
):
    user = db.query(User).filter(User.id == int(x_user_id)).first()

    if not user or user.role.value not in ("manager", "admin"):
        raise HTTPException(status_code=403, detail="Forbidden")

    return service.calculate_monthly_hours(db)
