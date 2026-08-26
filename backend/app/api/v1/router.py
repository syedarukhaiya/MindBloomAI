from fastapi import APIRouter
from app.api.v1.controllers.core_controller import router
api_router=APIRouter()
@api_router.get("/health")
def health(): return {"status":"healthy","service":"MindBloomAI API","version":"2.0.0","ai":"google-cloud-gemini"}
api_router.include_router(router)
