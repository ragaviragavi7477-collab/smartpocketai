import os

from pydantic_settings import BaseSettings
from functools import lru_cache

# Vercel serverless filesystem is read-only except /tmp, so point the
# SQLite file there when running on Vercel (data resets on cold starts;
# attach Vercel Postgres + DATABASE_URL env var for persistence).
_DEFAULT_DB = (
    "sqlite:////tmp/pocketsmart.db"
    if os.environ.get("VERCEL")
    else "sqlite:///./pocketsmart.db"
)

@lru_cache
def get_settings():
    class AppSettings(BaseSettings):
        model_config = {"env_file": ".env", "extra": "ignore"}

        GEMINI_API_KEY: str = "YOUR_GEMINI_API_KEY_HERE"
        DATABASE_URL: str = _DEFAULT_DB
        SECRET_KEY: str = "your-secret-key-change-this-in-production"
        ALGORITHM: str = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    return AppSettings()

settings = get_settings()
