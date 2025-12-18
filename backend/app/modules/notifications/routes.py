from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.modules.users.models import User
from app.modules.shifts.models import Shift

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
def list_notifications(
    db: Session = Depends(get_db),
    x_user_id: str = Header(...),
):
    user = db.query(User).filter(User.id == int(x_user_id)).first()

    if not user or user.role.value not in ("manager", "admin"):
        raise HTTPException(status_code=403, detail="Forbidden")

    shifts_count = db.query(Shift).count()

    if shifts_count == 0:
        return []

    return [
        {
            "type": "shift_created",
            "message": "New shift created",
        }
    ]
