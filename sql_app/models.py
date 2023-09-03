from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
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
    removed = Column(String(10), default="1970-01-01")
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)


class Recipe(Base):
    __tablename__ = "recipe"
    id = Column(Integer, primary_key=True, index=True)
    recipeId = Column(Integer, unique=True, index=True)
    recipeName = Column(String(50))
    recipeUrl = Column(String(250))
    recipeImgUrl = Column(String(250))
    recipeVideoUrl = Column(String(250))
    ingredients = Column(Text)
    measurements = Column(Text)
    directions = Column(Text)


class CalenderEvent(Base):
    __tablename__ = "calender_event"
    id = Column(Integer, primary_key=True, index=True)
    eventTitle = Column(String(250), nullable=False)
    eventTimeStart = Column(String(5))
    eventTimeEnd = Column(String(5))
    eventDateStart = Column(String(10), nullable=False)
    eventDateEnd = Column(String(10))
    eventBody = Column(String(500))
    createdTime = Column(String(5))
    createdDate = Column(String(10))
    removed = Column(String(10), default="1970-01-01")
