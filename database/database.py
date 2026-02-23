from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import sessionmaker, session

import sqlite3
from settings import Setting

settings = Setting()
engine = create_engine("postgresql+psycopg2://"
                       f"{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}/{settings.DB_NAME}")
Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session