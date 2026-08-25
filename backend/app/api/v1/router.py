from fastapi import APIRouter

from app.api.v1.controllers.auth_controller import router as auth_router
from app.api.v1.controllers.diary_controller import router as diary_router
from app.api.v1.controllers.gamification_controller import router as gamification_router
from app.api.v1.controllers.security_controller import router as security_router


api_router = APIRouter()


@api_router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MindBloomAI API",
        "version": "1.0.0",
    }


api_router.include_router(auth_router)
api_router.include_router(security_router)
api_router.include_router(diary_router)
api_router.include_router(gamification_router)
