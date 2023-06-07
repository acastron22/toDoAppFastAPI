from database import Base
from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# aqui que é criado a tabela ToDo e o q terá cada coluna
class ToDos(Base):
    __tablename__ = 'ToDos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
