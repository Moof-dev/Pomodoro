from pydantic_settings import BaseSettings
import os

class Setting(BaseSettings):
    #postgresql+psycopg2://user:password@hostname/database_name
    #DataBase settings
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_HOSTNAME: str = "0.0.0.0"
    DB_NAME: str = "database_name"
    #Redis settings
    REDIS_HOSTNAME: str = "127.0.0.1"
    REDIS_PORT: int = 6379



    class Config:
        # Читаем файл, путь к которому передан в ENV_FILE,
        # либо берем .local.env по умолчанию
        env_file = os.getenv("ENV_FILE", ".dev.env")
