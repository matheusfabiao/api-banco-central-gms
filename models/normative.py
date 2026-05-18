from sqlalchemy import Column, DateTime, Integer, String, Text

from config.database import database


class Normative(database.get_base()):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    title = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)
    normative_type = Column(String, nullable=False)
    url = Column(String, nullable=False)


class BcbNormative(Normative):
    __tablename__ = 'bcb_normatives'

    responsible = Column(String, nullable=False)
    number = Column(Integer, nullable=False)


class CvmNormative(Normative):
    __tablename__ = 'cvm_normatives'
