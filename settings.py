from pydantic_settings import BaseSettings
import os

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


    class Config:
        # Читаем файл, путь к которому передан в ENV_FILE,
        # либо берем .local.env по умолчанию
        env_file = os.getenv("ENV_FILE", ".dev.env")
