from database import Base
from sqlalchemy import Column, ForeignKey, Integer, Boolean, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Crio a classe de users
class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    firstName = Column(String)
    lastName = Column(String)
    hashedPassword = Column(String)
    isActive = Column(Boolean, default=True)
    role = Column(String)


# aqui que é criado a tabela ToDo e o q terá cada coluna
class ToDos(Base):
    __tablename__ = 'ToDos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    # para o ForeignKey, eu aponto de qual tabela devo estar chamando
    ownerId = Column(Integer, ForeignKey("users.id"))
