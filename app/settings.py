from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Setting(BaseSettings):
    #postgresql+psycopg2://user:password@hostname/database_name
    #DataBase settings
    DB_HOSTNAME: str = "localhost"
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "database_name"
    #Redis settings
    CACHE_HOSTNAME: str = "localhost"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0

    JWT_SECRET_KEY: str = "secret"
    JWT_ENCODE_ALGORITHM: str = "HS256"

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_SECRET_KEY: str = ""
    GOOGLE_REDIRECT_URL: str = ""
    GOOGLE_TOKEN_URI: str = "https://accounts.google.com/o/oauth2/token"
    CELERY_REDIS_URL: str = "redis://localhost:6379"

    from_email: str = "moof.error@gmail.com"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 465
    SMTP_PASSWORD: str = ""





    @property
    def db_url(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOSTNAME}/{self.DB_NAME}"

    @property
    def google_redirect_url(self) -> str:
        return (f"https://accounts.google.com/o/oauth2/auth?"
                f"response_type=code&"
                f"client_id={self.GOOGLE_CLIENT_ID}&"
                f"redirect_uri={self.GOOGLE_REDIRECT_URL}&"
                f"scope=openid%"
                f"20profile%"
                f"20email&"
                f"access_type=offline")

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".local.env"),
        extra="ignore"
    )