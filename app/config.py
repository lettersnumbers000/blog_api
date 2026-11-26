from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@db:5432/app"
    redis_url: str = "redis://redis:6379/0"
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    cors_origin: str = "http://localhost:3000"
    celery_eager: bool = False


settings = Settings()
