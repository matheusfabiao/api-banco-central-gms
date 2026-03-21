from sqlalchemy import Column, DateTime, Integer, String, Text

from config.database import database


class Normative(database.get_base()):
    __tablename__ = 'normatives'

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    title = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)
    responsible = Column(String, nullable=False)
    normative_type = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
