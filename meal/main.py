from config import settings
import json
import requests
from starlette.responses import StreamingResponse
from io import BytesIO
import os
from datetime import date

food_api_key = settings.settings.MEAL_DB_API_KEY


def random_meal():
    r = requests.get("http://www.themealdb.com/api/json/v1/1/random.php")
    return json.loads(r.text)



