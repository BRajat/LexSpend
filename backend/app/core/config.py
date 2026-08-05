from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "******localhost:5432/lexspend"
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "gpt-4o-mini"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    SECRET_KEY: str = "change-me-in-production"


settings = Settings()
