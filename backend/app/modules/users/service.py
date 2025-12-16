from sqlalchemy.orm import Session

from app.modules.users import models, schemas


def create_user(db: Session, data: schemas.UserCreate) -> models.User:
    user = models.User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session) -> list[models.User]:
    return db.query(models.User).all()
