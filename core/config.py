from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://nurik:nurik@localhost:5433/postgres"


settings = Settings()
