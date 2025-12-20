from fastapi import HTTPException


def require_manager(user):
    if user.role not in ("manager", "admin"):
        raise HTTPException(status_code=403, detail="Forbidden")
