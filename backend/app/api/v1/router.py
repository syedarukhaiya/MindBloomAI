from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MindBloomAI API",
        "version": "1.0.0",
    }
