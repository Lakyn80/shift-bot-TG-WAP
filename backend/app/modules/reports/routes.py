from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import require_role
from app.db.deps import get_db
from app.modules.attendance import service as attendance_service

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/hours/daily")
def report_daily_hours(
    user_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    data = attendance_service.calculate_daily_hours(db, user_id=user_id)

    # NORMALIZE RESPONSE
    if isinstance(data.get("total_hours"), dict):
        total = sum(data["total_hours"].values())
    else:
        total = data["total_hours"]

    return {
        "total_hours": total,
        "items": data.get("items", {}),
    }


@router.get("/hours/monthly")
def report_monthly_hours(
    user_id: int | None = Query(default=None),
    from_date=None,
    to_date=None,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
):
    data = attendance_service.calculate_monthly_hours(
        db,
        user_id=user_id,
        from_date=from_date,
        to_date=to_date,
    )

    # NORMALIZE RESPONSE
    if isinstance(data.get("total_hours"), dict):
        total = sum(data["total_hours"].values())
    else:
        total = data["total_hours"]

    return {
        "total_hours": total,
        "items": data.get("items", {}),
    }
