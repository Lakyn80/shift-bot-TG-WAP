from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.modules.rules.service import RuleViolation

from app.modules.users.routes import router as users_router
from app.modules.shifts.routes import router as shifts_router
from app.modules.attendance.routes import router as attendance_router
from app.modules.notifications.routes import router as notifications_router
from app.modules.reports.routes import router as reports_router

app = FastAPI()

# globální handler pro porušení pravidel
@app.exception_handler(RuleViolation)
async def rule_violation_handler(request: Request, exc: RuleViolation):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )

# DŮLEŽITÉ: žádné prefixy tady, prefixy jsou definované v routerech
app.include_router(users_router)
app.include_router(shifts_router)
app.include_router(attendance_router)
app.include_router(notifications_router)
app.include_router(reports_router)
