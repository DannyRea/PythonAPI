from config import settings
import json
import requests
from starlette.responses import StreamingResponse
from io import BytesIO
import os
from datetime import date

nasa_api_key = settings.settings.NASA_OPEN_API_KEY


def apod():
    r = requests.get(
        "https://api.nasa.gov/planetary/apod?api_key={}".format(nasa_api_key), stream=True)

    io = BytesIO()

    url = json.loads(r.text)['url']
    image = requests.get(url)
    file_name = url.split('/')[-1]

    with open(file_name, 'wb') as f:
        io.write(image.content)
    os.unlink(file_name)
    io.seek(0)
    return StreamingResponse(io, media_type="image/jpg")


def mars_rover_photos():
    todays_date = str(date.today())
    r = requests.get(
        "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={}&api_key={}".format(todays_date, nasa_api_key), stream=True)
    json_data = json.loads(r.text)
    if not json_data["photos"]:
        return 'No photos today. The rover is off for the weekend :)'
    return json_data
