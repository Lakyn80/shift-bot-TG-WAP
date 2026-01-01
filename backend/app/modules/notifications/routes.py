from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_role
from app.db.deps import get_db
from app.modules.shifts.models import Shift

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
def list_notifications(
    db: Session = Depends(get_db),
    _=Depends(require_role("manager", "admin")),
):
    shifts_count = db.query(Shift).count()

    if shifts_count == 0:
        return []

    return [
        {
            "type": "shift_created",
            "message": "New shift created",
        }
    ]
