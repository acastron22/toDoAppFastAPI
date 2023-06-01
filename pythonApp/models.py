from database import Base
from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ToDos(Base):
    __tablename__ = 'ToDos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
