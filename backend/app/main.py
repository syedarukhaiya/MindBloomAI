from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings
from app.db.database import Base,engine
import app.models
app=FastAPI(title=settings.app_name,version=settings.app_version,description="Private, safety-aware AI wellbeing companion for Indian youth.")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origins_list,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.get("/")
def root(): return {"message":"MindBloomAI API","docs":"/docs"}
app.include_router(api_router,prefix="/api/v1")
