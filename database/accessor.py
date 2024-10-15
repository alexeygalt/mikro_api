from settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.get_db_uri)
Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session
