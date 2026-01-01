from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.auth.dependencies import require_role
from app.db.deps import get_db
from app.modules.attendance import schemas, service

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("/check-in", response_model=schemas.AttendanceRead)
def check_in(
    payload: schemas.AttendanceCheckIn,
    db: Session = Depends(get_db),
    _=Depends(require_role("employee")),
):
    try:
        return service.check_in(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/check-out/{attendance_id}", response_model=schemas.AttendanceRead)
def check_out(
    attendance_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("employee")),
):
    try:
        return service.check_out(db, attendance_id)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


# =========================
# Restricted endpoints
# =========================

@router.get("/export/csv")
def export_csv(
    db: Session = Depends(get_db),
    _=Depends(require_role("admin", "manager")),
):
    csv_data = service.export_csv(db)
    return Response(
        content=csv_data,
        media_type="text/csv",
    )


@router.patch("/{attendance_id}", response_model=schemas.AttendanceRead)
def manual_edit(
    attendance_id: int,
    payload: schemas.AttendanceManualEdit,
    db: Session = Depends(get_db),
    _=Depends(require_role("manager")),
):
    return service.manual_edit(db, attendance_id, payload)


@router.get("/hours/daily")
def hours_daily(
    db: Session = Depends(get_db),
    _=Depends(require_role("admin", "manager")),
):
    return service.hours_daily(db)


@router.get("/hours/monthly")
def hours_monthly(
    db: Session = Depends(get_db),
    _=Depends(require_role("admin", "manager")),
):
    return service.hours_monthly(db)
