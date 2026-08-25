from fastapi import APIRouter
from sqlalchemy import text

from app.core.config import settings
from app.db.database import engine


router = APIRouter(
    prefix="/system",
    tags=["System"],
)


@router.get("/info")
def system_info():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "api_version": "v1",
    }


@router.get("/ready")
def readiness_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "ready",
            "database": "connected",
        }

    except Exception:
        return {
            "status": "not_ready",
            "database": "disconnected",
        }
