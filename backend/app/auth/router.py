from datetime import timedelta

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import ValidationError

from app.auth.schemas import LoginRequest, TokenResponse
from app.auth.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

# Temporary hardcoded users for initial wiring.
# hash for password "admin123"
HASHED_FAKE_PASSWORD = "$2b$12$EDyNrEiKKzTLc3sctZAZ5.1vn7RGf0bvY785.xHyAuWywwSIhY8Fq"

FAKE_USERS = {
    "admin": {
        "password": HASHED_FAKE_PASSWORD,
        "role": "admin",
        "id": 1,
    },
    "manager": {
        "password": HASHED_FAKE_PASSWORD,
        "role": "manager",
        "id": 2,
    },
    "employee": {
        "password": HASHED_FAKE_PASSWORD,
        "role": "employee",
        "id": 3,
    },
}


@router.post("/login", response_model=TokenResponse)
async def login(request: Request):
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

    user = FAKE_USERS.get(data.username)
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(
        data={
            "sub": data.username,
            "user_id": user["id"],
            "role": user["role"],
        },
        expires_delta=timedelta(hours=24),
    )

    return {"access_token": token}
