from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = ""
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str | None = None
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "gpt-4o-mini"
    CORS_ORIGINS: list[str] = ["*", "http://localhost:3000"]
    SECRET_KEY: str = "change-me-in-production"


def get_db_url() -> str:
    """Return the effective database URL from .env settings."""
    if settings.DATABASE_URL:
        return settings.DATABASE_URL

    if settings.POSTGRES_USER and settings.POSTGRES_PASSWORD and settings.POSTGRES_DB:
        return (
            f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
            f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
            f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        )

    return "sqlite+aiosqlite:///./legal_spend.db"


settings = Settings()
