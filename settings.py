from pydantic_settings import BaseSettings
import os

class Setting(BaseSettings):
    #postgresql+psycopg2://user:password@hostname/database_name
    #DataBase settings
    DB_HOSTNAME: str = "localhost"
    DB_DRIVER: str = "postgresql+psycopg2"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "database_name"
    #Redis settings
    CACHE_HOSTNAME: str = "localhost"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOSTNAME}/{self.DB_NAME}"


    class Config:
        # Читаем файл, путь к которому передан в ENV_FILE,
        # либо берем .local.env по умолчанию
        env_file = os.getenv("ENV_FILE", ".dev.env")
