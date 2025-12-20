from collections.abc import Generator
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.modules.users.models import User


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_manager(
    x_user_id: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if not x_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    user = db.query(User).filter(User.id == int(x_user_id)).first()
    if not user or user.role.value != "manager":
        raise HTTPException(status_code=403, detail="Forbidden")

    return user
