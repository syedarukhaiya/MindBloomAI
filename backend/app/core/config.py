from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "MindBloomAI API"
    app_version: str = "2.0.0"
    debug: bool = True
    database_url: str = "sqlite:///./mindbloom.db"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    jwt_secret_key: str = "change-this-secret-key-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 120
    google_cloud_project: str | None = None
    google_cloud_location: str = "us-central1"
    google_application_credentials: str | None = None
    gemini_model: str = "gemini-2.5-flash"
    ai_enabled: bool = True
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    @property
    def cors_origins_list(self):
        return [x.strip() for x in self.cors_origins.split(',') if x.strip()]

@lru_cache
def get_settings(): return Settings()
settings=get_settings()
