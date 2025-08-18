from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    fastapi_host: str
    fastapi_port: int
    fastapi_debug: bool
    fastapi_version: str

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    jwt_secret_key: str
    jwt_refresh_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    jwt_refresh_token_expire_days: int

    kafka_host: str
    kafka_port: int

    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str
    aws_s3_bucket_name: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def kafka_bootstrap_servers(self) -> str:
        return f"{self.kafka_host}:{self.kafka_port}"

    @property
    def jwt_access_token_cookie_max_age(self) -> int:
        return self.jwt_access_token_expire_minutes * 60

    @property
    def jwt_refresh_token_cookie_max_age(self) -> int:
        return self.jwt_refresh_token_expire_days * 24 * 60 * 60

    @property
    def s3_url(self) -> str:
        return (
            f"https://{self.aws_s3_bucket_name}.s3.{self.aws_region}.amazonaws.com"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
