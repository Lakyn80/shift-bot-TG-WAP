from fastapi import FastAPI

from app.modules.users.routes import router as users_router
from app.modules.shifts.routes import router as shifts_router
from app.modules.attendance.routes import router as attendance_router

app = FastAPI(
    title="Shift Bot API",
    version="0.1.0",
)

app.include_router(users_router)
app.include_router(shifts_router)
app.include_router(attendance_router)
