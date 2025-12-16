from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.modules.users import schemas, service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserRead)
def create_user(
    payload: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    return service.create_user(db, payload)


@router.get("/", response_model=list[schemas.UserRead])
def list_users(
    db: Session = Depends(get_db),
):
    return service.get_users(db)
