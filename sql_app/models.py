from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    admin_user = Column(Boolean, default=False)
class Note(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True, index=True)
    cardTitle = Column(String(50), nullable=False)
    cardBody = Column(String(250), nullable=False)
    removed = Column(String(10), default='1970-01-01')
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
