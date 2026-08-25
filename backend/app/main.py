from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import (
    MindBloomError,
    generic_error_handler,
    mindbloom_error_handler,
)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered personal wellbeing companion.",
)


app.add_exception_handler(
    MindBloomError,
    mindbloom_error_handler,
)

app.add_exception_handler(
    Exception,
    generic_error_handler,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to MindBloomAI API",
        "version": settings.app_version,
        "docs": "/docs",
    }


app.include_router(
    api_router,
    prefix="/api/v1",
)
