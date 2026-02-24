from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import sessionmaker, session

from settings import Setting

settings = Setting()

engine = create_engine(settings.db_url)
Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session