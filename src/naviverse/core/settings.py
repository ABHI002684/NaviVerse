# Attempt to use pydantic-settings (pydantic v2). If not available, provide a minimal fallback.
try:
    from pydantic_settings import BaseSettings
    from typing import Optional

    class Settings(BaseSettings):
        GROQ_API_KEY: Optional[str] = None
        DATABASE_URL: Optional[str] = None
        AVIATIONSTACK_API_KEY: Optional[str] = None
        TAVILY_API_KEY: Optional[str] = None
        ENV: str = "development"

        class Config:
            env_file = ".env"

    settings = Settings()
except Exception:
    # Minimal fallback for test environments where pydantic-settings isn't installed
    import os
    class Settings:
        def __init__(self):
            self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
            self.DATABASE_URL = os.getenv("DATABASE_URL")
            self.AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
            self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
            self.ENV = os.getenv("ENV", "development")

    settings = Settings()
