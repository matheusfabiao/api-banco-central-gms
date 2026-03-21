from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import settings


class Database:
    def __init__(self):
        self.__engine = create_engine(settings.DATABASE_URL)
        self.__session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self.__engine
        )
        self.__base = declarative_base()

    def get_session(self):
        session = self.__session_local()
        try:
            yield session
        finally:
            session.close()

    def get_base(self):
        return self.__base


database = Database()
