import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.auth.router import router as auth_router
from app.modules.rules.service import RuleViolation

from app.auth.security import hash_password
from app.db.session import SessionLocal
from app.modules.users.models import User, UserRole
from app.modules.users.routes import router as users_router
from app.modules.shifts.routes import router as shifts_router
from app.modules.attendance.routes import router as attendance_router
from app.modules.notifications.routes import router as notifications_router
from app.modules.reports.routes import router as reports_router

app = FastAPI(
    title="Shift API",
    swagger_ui_init_oauth={"usePkceWithAuthorizationCodeGrant": False},
)


def seed_initial_users():
    if os.getenv("AUTH_TEST_MODE", "").lower() == "true":
        return
    db = SessionLocal()
    try:
        seeds = [
            ("Admin", UserRole.admin),
            ("Manager", UserRole.manager),
        ]
        for full_name, role in seeds:
            exists = db.query(User).filter(User.full_name == full_name).first()
            if exists:
                continue
            user = User(
                full_name=full_name,
                role=role,
                is_active=True,
                password_hash=hash_password("admin123"),
                telegram_id=None,
                whatsapp_id=None,
            )
            db.add(user)
        db.commit()
    finally:
        db.close()


@app.on_event("startup")
def startup_seed():
    seed_initial_users()


# globální handler pro porušení pravidel
@app.exception_handler(RuleViolation)
async def rule_violation_handler(request: Request, exc: RuleViolation):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


# DŮLEŽITÉ: žádné prefixy tady, prefixy jsou definované v routerech
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(shifts_router)
app.include_router(attendance_router)
app.include_router(notifications_router)
app.include_router(reports_router)
