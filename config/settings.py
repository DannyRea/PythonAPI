from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Daniel's API"
    NASA_OPEN_API_KEY: str = "PCZ90SXfrTeVimkMl66dJPxh1cHc2z5m3PUtBCJM"
    MEAL_DB_API_KEY: str = "1"
    SQLALCHEMY_DATABASE_URL: str = "postgresql://postgres:555435@192.168.0.13:5432"


settings = Settings()
