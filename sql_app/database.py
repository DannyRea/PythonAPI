from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from broadcaster import Broadcast
from config import settings


engine = create_engine(settings.settings.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print("creating Base")
Base = declarative_base()

broadcast = Broadcast(settings.settings.SQLALCHEMY_DATABASE_URL)
