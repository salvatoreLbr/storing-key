from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    hashed_password = Column(String)

    users = relationship("Keys", back_populates="keys")


class Keys(Base):
    __tablename__ = "Keys"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    key_name = Column(String(100), unique=True)
    hashed_secret = Column(String(100))

    keys = relationship("Users", back_populates="users")
