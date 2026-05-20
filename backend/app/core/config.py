
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "CMS Backend"
    app_version: str = "0.1.0"
    debug: bool = False
    secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30
    jwt_refresh_expiration_days: int = 7

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/cms"

    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "cms"

    redis_url: str = "redis://localhost:6379/0"

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "cms-images"
    minio_use_ssl: bool = False
    minio_public_url: str = "http://localhost:9000/cms-images"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
