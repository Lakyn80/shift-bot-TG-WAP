from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.users.models import User


def require_manager(db: Session):
    manager_exists = (
        db.query(User)
        .filter(User.role == "manager")
        .first()
    )
    if not manager_exists:
        raise HTTPException(status_code=403, detail="Forbidden")
