from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Daniel's API"
    NASA_OPEN_API_KEY: str = "PCZ90SXfrTeVimkMl66dJPxh1cHc2z5m3PUtBCJM"


settings = Settings()
