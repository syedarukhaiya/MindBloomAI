from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import settings
import app.models


BASE_DIR = Path(__file__).resolve().parents[2]
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Private, safety-aware AI wellbeing companion for Indian youth.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(api_router, prefix="/api/v1")


# Serve React frontend
if STATIC_DIR.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=STATIC_DIR / "assets"),
        name="assets",
    )

    @app.get("/", include_in_schema=False)
    async def serve_frontend():
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_react_routes(full_path: str):
        # Keep API and documentation paths out of the frontend fallback.
        if full_path.startswith(("api/", "docs", "redoc", "openapi.json")):
            return {"detail": "Not Found"}

        requested_file = STATIC_DIR / full_path

        if requested_file.is_file():
            return FileResponse(requested_file)

        return FileResponse(STATIC_DIR / "index.html")

else:

    @app.get("/")
    async def root():
        return {"message": "MindBloomAI API", "docs": "/docs"}
