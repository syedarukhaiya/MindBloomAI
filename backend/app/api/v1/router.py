from fastapi import APIRouter
from app.api.v1.controllers.core_controller import router as core_router
from app.api.v1.controllers.circle_controller import router as circle_router
from app.api.v1.controllers.story_controller import router as story_router
from app.api.v1.controllers.personal_reflection_controller import router as reflection_router

api_router = APIRouter()

@api_router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "MindBloomAI API",
        "version": "2.0.0",
        "ai": "google-cloud-gemini",
    }

api_router.include_router(core_router)
api_router.include_router(circle_router)
api_router.include_router(story_router)
api_router.include_router(reflection_router)
