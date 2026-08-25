from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(
    prefix="/system",
    tags=["Backend"],
)

@router.get("/status")
def backend_status(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "status": "healthy",
        "api": "MindBloomAI API",
        "database": "connected",
        "modules": [
            "authentication",
            "security",
            "diary",
            "gamification",
        ],
    }

@router.get("/info")
def backend_info():
    return {
        "name": "MindBloomAI",
        "version": "1.0.0",
        "description": "AI-powered personal wellbeing companion backend",
        "api_version": "v1",
    }
