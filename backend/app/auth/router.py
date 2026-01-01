from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.auth.schemas import LoginRequest, TokenResponse
from app.auth.security import create_access_token, verify_password
from app.db.deps import get_db
from app.modules.users.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        if request.headers.get("content-type", "").startswith("application/json"):
            raw = await request.json()
        else:
            form = await request.form()
            raw = {"username": form.get("username"), "password": form.get("password")}
        data = LoginRequest.model_validate(raw)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors(),
        )

    user: User | None = (
        db.query(User).filter(User.full_name == data.username).first()
    )
    role_value = user.role.value if user and hasattr(user.role, "value") else None

    if not user or not user.password_hash or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(
        data={
            "sub": user.full_name,
            "user_id": user.id,
            "role": role_value or user.role,
        },
        expires_delta=timedelta(hours=24),
    )

    return {"access_token": token}
