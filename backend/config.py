import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


def resolve_env_file() -> tuple[str, ...]:
    """
    Resolves configuration file paths in precedence order:
    1. Render Mounted Secret File (/etc/secrets/.env)
    2. Project root /etc/secrets/.env
    3. Standard local .env
    """
    candidates = [
        Path("/etc/secrets/.env"),             # Render Secret File standard mount
        Path("/etc/secrets/config.env"),       # Alternate Render Secret File name
        Path(__file__).parent / ".env",        # backend/.env (local dev)
        Path(__file__).parent.parent / ".env", # project root .env
    ]
    
    # Return all existing paths so pydantic-settings reads the first available
    existing_files = [str(p) for p in candidates if p.is_file()]
    return tuple(existing_files) if existing_files else (".env",)


class Settings(BaseSettings):
    # Core Infrastructure
    DATABASE_URL: str = "postgresql://msme_user:password@localhost:5432/msmedb"
    
    # AI / LLM Engine
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "openai/gpt-oss-120b"
    
    # Authentication & Security
    JWT_SECRET: str = "default-fallback-insecure-key-32chars!"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # File Storage
    STORAGE_DIR: str = "/tmp/msme_vault"

    # Environment Identifier
    ENVIRONMENT: str = "production"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def clean_database_url(cls, v: str) -> str:
        """
        Fixes Render's legacy `postgres://` prefix for SQLAlchemy 2.0+ compatibility.
        """
        if isinstance(v, str) and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    model_config = SettingsConfigDict(
        # Discovers Render /etc/secrets/.env or fallback .env
        env_file=resolve_env_file(),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
