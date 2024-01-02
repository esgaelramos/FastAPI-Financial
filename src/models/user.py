"""Models for the User Table in the DataBase."""

from sqlalchemy import Column, Integer, String
from src.core.database import Base


class User(Base):
    """Represents a user in the database."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
