from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_url: str = "postgresql+asyncpg://nurik:nurik@localhost:5433/postgres"
    redis_url: str = "redis://localhost "  # "redis://localhost"
    fastapi_cache_prefix: str = "fastapi-cache"


settings = Settings()
